# Revaly RAP SDK for Python

Server-side Python SDK for the RAP V2 API: payments, payment methods, transactions and
notify — with a **merchant-facing failover contract** built in. Every failed payment
call raises exactly one of three typed classes that tell you what you may safely do
next.

> **Install:** `pip install revaly-sdk` — published on PyPI. Requires Python ≥ 3.9.
> GitHub release artifacts remain the provenance anchor and fallback channel.

## Why the error classes matter (read this first)

A failed `charge(...)` does **not** mean the payment didn't happen. If you
blind-fail-over to your own gateway on an ambiguous failure, the cardholder can be
charged **twice**. The SDK classifies every failure so you never have to guess:

| Class | Meaning | What you do |
| --- | --- | --- |
| `RapPermanentRejection` | Received and rejected (400/401/403/404/422) | Fix or decline — failing over reproduces the same rejection anywhere. |
| `RapTransientFailure` | **Definitively not processed** (provably never sent, or `503` + `code: not_processed`) | Route to your own gateway immediately. |
| `RapOutcomeUnknown` | **May have been processed** (timeout after send, reset, 5xx) | **Reconcile before acting** — see below. |

## Quickstart (sandbox key → first charge, ≤ 15 minutes)

Your API key's scope selects the environment: sandbox and live share the same URL —
there is no separate sandbox host. Use the sandbox-scoped key issued by Enablement.

```bash
pip install revaly-sdk
```

> Prefer to install from a verified artifact? Every release attaches
> `revaly-sdk-python.tar.gz` and a wheel, each with a `.sha256` and a `provenance.json`;
> verify the checksum, then `pip install ./revaly-sdk-python.tar.gz` — either file installs
> the same package.

```python
import os

from revaly_sdk import (
    CreditCard,
    Found,
    NotFoundYet,
    PaymentMethod,
    PaymentRequest,
    RapClient,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransactionOutcome,
    RapTransientFailure,
    ReconcilePolicy,
)

client = RapClient(os.environ["RAP_API_KEY"])

request = PaymentRequest(
    amount=1999,
    currency="USD",
    merchant_transaction_id="order-1042",  # required on every payment — it is your reconcile handle
    order_id="order-1042",  # orderId + email below: the sandbox simulator requires both for an approval
    # paymentMethodType is omitted — inferred from the one populated method object
    payment_method=PaymentMethod(
        full_name="Ada Lovelace",  # creditCard requires a cardholder name
        email="ada@example.com",
        credit_card=CreditCard(
            number="4111111111111111",  # sandbox test PAN
            card_verification_code="999",
            expiry_month="12",
            expiry_year="2030",
        )
    ),
)

try:
    transaction = client.charge(request)
    print("approved", transaction.transaction_id)
    # transaction.payment_method.vault_token (spec >= 2.4.0) ties this charge back to the
    # stored credential it ran against — set only when a vault credential was used, and it
    # may reflect an Account Updater roll. Treat it as optional; absence proves nothing.
except RapPermanentRejection as failure:
    # Fix or decline — failing over reproduces the same rejection anywhere.
    print("rejected", failure.status, failure.api_error, failure.correlation_id)
except RapTransientFailure:
    # Definitively not processed — route to your own gateway immediately.
    route_to_own_gateway()
except RapOutcomeUnknown:
    # May have been processed — reconcile BEFORE acting (double-charge hazard).
    verdict = client.reconcile(
        "order-1042",
        ReconcilePolicy(max_attempts=5, overall_budget=30.0, initial_delay=0.5),
    )
    if isinstance(verdict, Found):
        # The record IS visible. Found(APPROVED) means the money moved —
        # failing over now would double-charge.
        print("resolved", verdict.outcome, verdict.correlation_id)
    elif isinstance(verdict, NotFoundYet):
        # Not visible YET — absence is not provable in V1. Hold and escalate
        # per your risk policy; do not treat this as "safe to fail over".
        print("hold", verdict.attempts, verdict.last_correlation_id)
    else:
        # Verdicts are open for extension (SafeToFailover arrives with
        # platform P-2 as a minor release). Always keep this branch.
        escalate_to_operator(verdict)
```

### Timeouts

`overall_deadline` defaults to **75 seconds** (`DEFAULT_OVERALL_DEADLINE`) — ratified
from production latency telemetry (ADR-SDK-027): it clears every observed gateway
tail cluster (the worst non-hung tail seen in 14 fleet days was 64 s), clips ≲0.007%
of charges, and still classifies well before the platform's own ≈100 s ceiling.
Tighten it per your checkout budget (RAP routes gateways server-side, so the default
must cover the slowest common class), or pass an explicit `overall_deadline=None` to
disable the SDK deadline. `connect_timeout` defaults to **10 seconds**
(`DEFAULT_CONNECT_TIMEOUT`) — ratified from the OQ-11 edge verification (ADR-SDK-029):
roughly 25× the observed cold client→edge TLS envelope, and 65 s below the overall
deadline. Pass an explicit `connect_timeout=None` to disable the SDK connect bound.
All timeouts are seconds:

```python
client = RapClient(api_key, connect_timeout=3.0, overall_deadline=10.0)
# or per call:
client.charge(request, overall_deadline=5.0)
```

Note the per-call asymmetry: passing `overall_deadline=None` (or omitting it) on a call
means "use the client's configured value", never "disable" — disabling the deadline is
a client-construction decision only (`RapClient(..., overall_deadline=None)`),
deliberately without a per-call equivalent (the safe direction). The same asymmetry
applies to `connect_timeout`.

- `overall_deadline` expiry **after send** classifies `RapOutcomeUnknown` (reconcile),
  never TransientFailure.
- `connect_timeout` expiry proves the request never left the client and classifies
  `RapTransientFailure` — urllib3 reports the connect phase distinctly even when only
  an overall deadline is set.

Python has no ambient cancellation token: bound calls with these timeout arguments and
bound reconciliation with the `ReconcilePolicy` budget — that is this SDK's
cancellation idiom.

### API versioning

Requests pin `X-Api-Version: 2.1` by default. `"2.0"` is selectable
(`api_version="2.0"`) but narrows the contract: `ErrorResponse.code` is not part of
the 2.0 documented surface, so a `503` + `not_processed` classifies
`RapOutcomeUnknown` (reconcile) instead of `RapTransientFailure` (immediate failover).
Pin 2.1 unless you have a frozen 2.0 integration.

## Testing your failover handler — no network

The mock transport scripts every row of the failure taxonomy and both reconcile
verdicts, and asserts your requests carry the SDK User-Agent. It replaces only the
wire: header injection and classification run exactly as in production.

```python
from revaly_sdk import RapClient
from revaly_sdk.testing import RapMockTransport

mock = RapMockTransport()
mock.charge().returns_not_processed_503()  # → RapTransientFailure
mock.reconcile().not_found_yet(2).then_found_approved()

client = RapClient("sk-synthetic", transport=mock)
# exercise YOUR suppression/escalation logic against scripted consecutive outcomes:
mock.charge().returns_bare_503().throws_connection_refused().returns_approved()
```

Scenario methods mirror the contract: `returns_permanent_rejection(status)`,
`returns_not_processed_503()`, `throws_connection_refused()`, `throws_dns_failure()`,
`throws_ssl_handshake_failure()`, `throws_connect_timeout()`,
`throws_timeout_after_send()`, `throws_connection_reset()`, `returns_bare_503()`,
`returns_server_error()`, `pending()`, and raw escapes `returns(...)` /
`throws_io(...)`. Transport failures are simulated with real urllib3 exception
instances, so classification in your tests exercises the production code path.
Synthetic data only — no real PAN/CVV/PII ever appears in the mock.

## Logging & debugging

- Logging uses the stdlib `logging` module (logger name `revaly_sdk`; silent until
  your application configures handlers, or pass `logger=`). Default output is
  **values-free** — operation, status, class, correlation id. `DEBUG` level carries
  **allowlist-scrubbed** payloads only; PAN/CVV/PII and the API key can never appear
  (the API key is also absent from every error message).
- `wire_trace_hook`: a request/response observer for Enablement escalations —
  payloads arrive already scrubbed by the runtime's central allowlist scrubber.
- Every response and every typed error carries the `X-Correlation-ID`; quote it in
  support tickets to join RAP-core telemetry directly.

## Design guarantees

- **Each charge is sent exactly once.** Retry policy stays yours, with the
  classification that makes it safe to exercise.
- **Every call stands alone** — no cross-request state, no circuit breaker, so
  behaviour under load is the behaviour you tested.
- **The reconcile re-poll you bound is the only loop the SDK owns.**
- **Classification rests on evidence only**: HTTP status and `ErrorResponse.code`.
  Message text, latency and wait length are reported to you and excluded from the
  verdict.
- **Recovery beyond this boundary belongs to RAP-core** — resubmission and
  `bypassPlatform` are platform-internal, so a payment's outcome stays unambiguous.

Concretely, on the transport: urllib3's default connect retries and redirect-following are
switched off per request, so a `307` on `POST /payments` arrives as a response and
classifies `RapOutcomeUnknown` rather than being silently re-sent.

Normative form: [`docs/failover-contract.md`](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-contract.md) §5 and
Appendix A.

## Beyond payments

The full generated V2 surface ships in the same package and flows through the same
transport, headers and classification:

```python
methods = client.payment_methods.list_payment_methods()
raw = client.transactions.get_transaction_by_id_without_preload_content("txn-1")
```

One logging caution on this surface: raw core operations raise the generator's
`ApiException`, not the three typed classes — and `str(ApiException)` embeds the full
HTTP response body. Response bodies can contain PII (names, emails, masked card data):
never log raw core exceptions or response bodies; log the correlation id and the typed
runtime errors (values-free by design) instead.

## Where to go next

- [Failover cookbook](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-cookbook.md) — recipes for each outcome, choosing a
  reconcile policy, testing offline, debugging with correlation ids.
- [Failover contract](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-contract.md) — the normative specification, with
  sequence diagrams and the verbatim prohibitions in Appendix A.
- [AGENTS.md](https://github.com/revaly-co/RAP-sdk/blob/main/AGENTS.md) — the whole contract on one page, for AI coding agents.
- [Support](https://github.com/revaly-co/RAP-sdk/blob/main/SUPPORT.md) · [Contributing](https://github.com/revaly-co/RAP-sdk/blob/main/CONTRIBUTING.md) · [Security](https://github.com/revaly-co/RAP-sdk/blob/main/SECURITY.md)
