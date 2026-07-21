# Revaly RAP SDK for PHP

The official PHP SDK for the RAP V2 API (`api.revaly.co`): payments, payment methods,
transactions, and notify — with a **merchant-facing failover contract** built in. One
package (`revaly/sdk`), one import namespace (`Revaly\Sdk`); the generated API core
ships inside it as `Revaly\Sdk\Core`.

> Package name and registry availability are provisional until registry provisioning
> completes (OQ-3). Interim distribution is via this repository's per-language GitHub
> release artifacts — nothing is on Packagist yet.

Requires PHP 8.1+ with `ext-curl`, `ext-json`, `ext-mbstring`; HTTP via Guzzle 7.

## Why the error classes matter (read this first)

A failed `POST /payments` does **not** mean the payment didn't happen. If you blindly
fail over to your own gateway on an ambiguous failure, the cardholder can be charged
**twice**. Every payment operation on `RapClient` therefore throws exactly one of three
typed failure classes, and the class — never the message text, never latency — is what
licenses failover:

| Exception | Meaning | What you do |
| --- | --- | --- |
| `PermanentRejectionException` | Received and rejected (400/401/403/404/422) | Fix or decline. **Never fail over** — the same request fails anywhere. |
| `TransientFailureException` | **Definitively not processed** (provably never sent, or `503` + `code: not_processed`) | Route to your own gateway immediately. |
| `OutcomeUnknownException` | **May have been processed** (timeout after send, 500/502/504, bare 503, reset) | **Reconcile before acting** — see the quickstart. |

## Quickstart (sandbox key → first charge, ≤ 15 minutes)

Install (interim, from a GitHub release artifact of this repository):

```bash
# Download revaly-sdk-php.zip from the release, verify its .sha256, then:
composer config repositories.revaly artifact ./path/to/release-artifacts/
composer require revaly/sdk
```

Charge a payment and handle **all three** failure classes — the failover + reconcile
example is part of the quickstart because it is the safety-critical path:

```php
<?php

use Revaly\Sdk\Core\Model\CreditCard;
use Revaly\Sdk\Core\Model\PaymentMethod;
use Revaly\Sdk\Core\Model\PaymentRequest;
use Revaly\Sdk\Errors\OutcomeUnknownException;
use Revaly\Sdk\Errors\PermanentRejectionException;
use Revaly\Sdk\Errors\TransientFailureException;
use Revaly\Sdk\RapClient;
use Revaly\Sdk\Reconcile\Found;
use Revaly\Sdk\Reconcile\NotFoundYet;
use Revaly\Sdk\Reconcile\RapTransactionOutcome;
use Revaly\Sdk\Reconcile\ReconcilePolicy;

$client = new RapClient(
    // Enablement-issued sandbox-scoped key, sent as `Authorization: ApiKey <key>`.
    // Sandbox and live share the same URL — your key's scope selects the environment
    // (there is no separate sandbox host).
    apiKey: getenv('REVALY_API_KEY'),
);

$request = new PaymentRequest();
$request->setAmount(1999);                     // smallest currency unit (cents)
$request->setCurrency('USD');
$request->setMerchantTransactionId('order-1042-attempt-1'); // required — reconcile key

$card = new CreditCard();
$card->setNumber('4111111111111111');          // sandbox test card
$card->setExpiryMonth('12');
$card->setExpiryYear('2030');
$card->setCardVerificationCode('123');

$method = new PaymentMethod();
$method->setFullName('Ada Lovelace');          // creditCard requires a cardholder name
$method->setCreditCard($card);
$request->setPaymentMethod($method);           // paymentMethodType is omitted —
                                               // inferred from the one populated method object

try {
    $transaction = $client->charge($request);
    echo "approved: {$transaction->getTransactionId()}\n";
} catch (PermanentRejectionException $e) {
    // Fix or decline. NEVER fail over — the same request fails anywhere.
    echo "rejected [{$e->getStatusCode()}]: {$e->getApiError()} (ref {$e->getCorrelationId()})\n";
} catch (TransientFailureException $e) {
    // Definitively not processed — route to your own gateway immediately.
    chargeOnFallbackGateway($request);
} catch (OutcomeUnknownException $e) {
    // May have been processed — reconcile BEFORE acting (double-charge hazard).
    $verdict = $client->reconcile(
        $request->getMerchantTransactionId(),
        new ReconcilePolicy(
            maxAttempts: 5,
            overallBudgetSeconds: 30.0,
            initialDelaySeconds: 1.0,   // doubles each attempt, ±20% jitter
        ),
    );

    if ($verdict instanceof Found) {
        match ($verdict->getOutcome()) {
            RapTransactionOutcome::Approved => acknowledgeSuccess($verdict->getTransaction()),
            RapTransactionOutcome::Declined,
            RapTransactionOutcome::Error => decideOnFallbackPerYourRiskPolicy(),
            // Pending, Unknown, and future outcomes: hold conservatively.
            default => holdAndEscalate($verdict),
        };
    } elseif ($verdict instanceof NotFoundYet) {
        // NOT proof of absence — platform visibility is asynchronous and widest
        // exactly when RAP-core is degraded. Hold and escalate per your policy.
        holdAndEscalate($verdict);
    } else {
        // Default branch — REQUIRED. Verdicts are open for extension: SafeToFailover
        // arrives with platform P-2 as a minor release.
        holdAndEscalate($verdict);
    }
}
```

`reconcile()` is GET-only and side-effect-free; its bounds are yours (`ReconcilePolicy`
has no defaults). On sustained `NotFoundYet`, escalate per your risk policy — V1 has no
`SafeToFailover` verdict, deliberately.

### Timeouts

`overallDeadline` defaults to **75 seconds** — ratified from production latency
telemetry (ADR-SDK-027): it clears every observed gateway tail cluster (the worst
non-hung tail seen in 14 fleet days was 64 s), clips ≲0.007% of charges, and still
classifies well before the platform's own ≈100 s ceiling. Tighten it per your checkout
budget (RAP routes gateways server-side, so the default must cover the slowest common
class), or pass an explicit `overallDeadline: null` to disable the SDK deadline.
`connectTimeout` defaults to **10 seconds** — ratified from the OQ-11 edge verification
(ADR-SDK-029): roughly 25× the observed cold client→edge TLS envelope, and 65 s below
the overall deadline. Pass an explicit `connectTimeout: null` to disable the SDK
connect bound. One PHP-specific caveat: curl reports connect-phase timeouts and
after-send deadline expiry with the **same error** (errno 28), so this SDK classifies
**every timeout as `OutcomeUnknown`** (reconcile), never as safe-to-failover — it
cannot prove the request was never sent. Provable never-sent (connection refused, DNS,
TLS handshake) still classifies `TransientFailureException`.

### API versioning

The client pins `X-Api-Version: 2.1` by default; `2.0` is selectable
(`apiVersion: '2.0'`). **Behavioural difference on 2.0:** the `ErrorResponse.code`
field is not part of the 2.0 documented contract, so `503` + `code: not_processed`
classifies as `OutcomeUnknown` (reconcile) instead of `TransientFailureException`
(immediate failover). Pin 2.1 unless you have a frozen 2.0 integration.

## Testing your failover handler — no network

`RapMockTransport` scripts every row of the failure taxonomy, so your failover handler
is unit-testable with no network and **synthetic data only**:

```php
use Revaly\Sdk\RapClient;
use Revaly\Sdk\Testing\RapMockTransport;

$mock = new RapMockTransport();
$mock->charge()->returnsNotProcessed503();          // TransientFailure: fail over now
$mock->reconcile('order-1042-attempt-1')
    ->notFoundYet(2)                                // two 404s...
    ->thenFoundApproved();                          // ...then the record appears

$client = new RapClient(apiKey: 'sk-test-synthetic', transport: $mock);

// Drive your handler; then assert what it did:
$requests = $mock->getRequests();                   // recorded, with headers
```

Scenario methods cover the whole §2 table: `returnsPermanentRejection(422)`,
`returnsNotProcessed503()`, `throwsConnectionRefused()`, `throwsDnsFailure()`,
`throwsSslHandshakeFailure()`, `returnsBare503()`, `returnsServerError()`,
`returnsBadGateway()`, `returnsGatewayTimeout()`, `throwsTimeoutAfterSend()`,
`throwsConnectTimeout()`, `throwsConnectionReset()`, plus reconcile scripting
(`notFoundYet()`, `pending()`, `thenFoundApproved()`, `thenFoundDeclined()`) and raw
escapes (`returns()`, `throwsIo()`).

## Logging & debugging

- Pass any PSR-3 `logger`. **Default output is values-free**: operation, HTTP status,
  failure class, and correlation id — never payload values, never the API key.
- Debug level carries payloads scrubbed by a central **allowlist** (only known-safe
  identifier/status fields survive; PAN/CVV/PII cannot appear).
- Every response and every typed error carries the **`X-Correlation-ID`** — quote it in
  support tickets; it joins your request directly to platform telemetry.
- `wireTraceHook` receives a scrubbed request/response observer (`RapWireTrace`) for
  escalations; observer exceptions are swallowed.

## What this SDK never does

No retries, no resubmission, no circuit breaker, no redirect-following, no cross-request
state. The only loop is the explicit, caller-bounded reconcile poll. Failover execution
belongs to your code against your risk policy — the SDK's job is to tell you, honestly,
which failure class you are in.

## Beyond payments

The full generated V2 surface is available through the same client and transport:
`$client->payments()`, `$client->transactions()`, `$client->paymentMethods()`,
`$client->notifyApi()`. One note on the transactions lookups: the generated 200-response
wrappers merge all response variants (terminal / pending / grouped) into one flattened
class without discrimination — check the discriminating field yourself (`state` is
present only on pending records), or prefer `$client->reconcile()`, which classifies
from the raw body.
