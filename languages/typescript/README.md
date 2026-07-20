# Revaly RAP SDK for TypeScript

Server-side TypeScript/JavaScript SDK for the RAP V2 API: payments, payment methods,
transactions and notify — with a **merchant-facing failover contract** built in. Every
failed payment call rejects with exactly one of three typed classes that tell you what
you may safely do next.

> **Package status:** the npm name `revaly-sdk` is **[Proposed]** until registry
> provisioning (OQ-3), and registry publish is embargoed — install from the per-language
> GitHub release artifact until then. Requires Node.js ≥ 20.3 (or any runtime with
> WHATWG `fetch` and `AbortSignal.any`).

## Why the error classes matter (read this first)

A failed `charge(...)` does **not** mean the payment didn't happen. If you blind-fail-over
to your own gateway on an ambiguous failure, the cardholder can be charged **twice**.
The SDK classifies every failure so you never have to guess:

| Class | Meaning | What you do |
| --- | --- | --- |
| `RapPermanentRejection` | Received and rejected (400/401/403/404/422) | Fix or decline. **Never fail over** — the same request fails anywhere. |
| `RapTransientFailure` | **Definitively not processed** (provably never sent, or `503` + `code: not_processed`) | Route to your own gateway immediately. |
| `RapOutcomeUnknown` | **May have been processed** (timeout after send, reset, 5xx) | **Reconcile before acting** — see below. |

## Quickstart (sandbox key → first charge, ≤ 15 minutes)

Your API key's scope selects the environment: sandbox and live share the same URL —
there is no separate sandbox host. Use the sandbox-scoped key issued by Enablement.

```bash
# Download revaly-sdk-typescript.tgz from the release, verify its .sha256, then:
npm install ./revaly-sdk-typescript.tgz
```

```ts
import {
    RapClient,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransientFailure,
} from 'revaly-sdk';

const client = new RapClient({ apiKey: process.env.RAP_API_KEY! });

try {
    const transaction = await client.charge({
        amount: 1999,
        currency: 'USD',
        merchantTransactionId: 'order-1042', // required on every payment — it is your reconcile handle
        // paymentMethodType is omitted — inferred from the one populated method object
        paymentMethod: {
            fullName: 'Ada Lovelace', // creditCard requires a cardholder name
            creditCard: {
                number: '4111111111111111', // sandbox test PAN
                cardVerificationCode: '999',
                expiryMonth: '12',
                expiryYear: '2030',
            },
        },
    });
    console.log('approved', transaction.transactionId);
} catch (failure) {
    if (failure instanceof RapPermanentRejection) {
        // Fix or decline. Never fail over — the same request fails anywhere.
        console.log('rejected', failure.status, failure.apiError, failure.correlationId);
    } else if (failure instanceof RapTransientFailure) {
        // Definitively not processed — route to your own gateway immediately.
        routeToOwnGateway();
    } else if (failure instanceof RapOutcomeUnknown) {
        // May have been processed — reconcile BEFORE acting (double-charge hazard).
        const verdict = await client.reconcile('order-1042', {
            maxAttempts: 5,
            overallBudgetMs: 30_000,
            initialDelayMs: 500,
        });
        switch (verdict.kind) {
            case 'found':
                // The record IS visible. Found(Approved) means the money moved —
                // failing over now would double-charge.
                console.log('resolved', verdict.outcome, verdict.transaction?.transactionId);
                break;
            case 'notFoundYet':
                // Not visible YET — absence is not provable in V1. Hold and escalate
                // per your risk policy; do not treat this as "safe to fail over".
                console.log('hold', verdict.attempts, verdict.lastCorrelationId);
                break;
            default:
                // Verdicts are open for extension (SafeToFailover arrives with
                // platform P-2 as a minor release). Always keep this branch.
                escalateToOperator(verdict);
                break;
        }
    } else {
        throw failure; // not a payment outcome (cancellation, validation, bugs)
    }
}
```

Prefer results over exceptions? The same taxonomy is available as a discriminated
union:

```ts
import { toRapResult } from 'revaly-sdk';

const result = await toRapResult(() => client.charge(request));
if (!result.ok) {
    switch (result.failure.kind) {
        case 'TransientFailure': /* fail over */ break;
        case 'PermanentRejection': /* fix or decline */ break;
        default: /* OutcomeUnknown and anything future: reconcile / escalate */ break;
    }
}
```

### Timeouts are yours to choose (for now)

The SDK ships **no default deadlines** — the telemetry-derived recommendations are an
open item (OQ-6) and land before Wave-1 GA. Set `overallDeadlineMs` per your checkout
budget; expiry after send classifies `RapOutcomeUnknown` (reconcile), never
TransientFailure.

There is deliberately **no `connectTimeout` option**: WHATWG fetch cannot bound the
connect phase per request. On Node the platform's own connect timeout applies (undici
default 10s), is reported structurally, and — because a connect-phase timeout proves
the request never left — classifies `RapTransientFailure`. To tune it, pass a
dispatcher:

```ts
import { Agent } from 'undici'; // your app's dependency, not the SDK's

const client = new RapClient({
    apiKey: process.env.RAP_API_KEY!,
    overallDeadlineMs: 10_000,
    dispatcher: new Agent({ connect: { timeout: 3_000 } }),
});
```

### API versioning

Requests pin `X-Api-Version: 2.1` by default. `"2.0"` is selectable
(`apiVersion: '2.0'`) but narrows the contract: `ErrorResponse.code` is not part of the
2.0 documented surface, so a `503` + `not_processed` classifies `RapOutcomeUnknown`
(reconcile) instead of `RapTransientFailure` (immediate failover). Pin 2.1 unless you
have a frozen 2.0 integration.

## Testing your failover handler — no network

The mock transport scripts every row of the failure taxonomy and both reconcile
verdicts, and asserts your requests carry the SDK User-Agent:

```ts
import { RapClient, RapMockTransport } from 'revaly-sdk';

const mock = new RapMockTransport();
mock.charge().returnsNotProcessed503(); // → RapTransientFailure
mock.reconcile('order-1042').notFoundYet(2).thenFoundApproved();

const client = new RapClient({ apiKey: 'sk-synthetic', transport: mock });
// exercise YOUR suppression/escalation logic against scripted consecutive outcomes:
mock.charge().returnsBare503().throwsConnectionRefused().returnsApproved();
```

Scenario methods mirror the contract: `returnsPermanentRejection(status)`,
`returnsNotProcessed503()`, `throwsConnectionRefused()`, `throwsDnsFailure()`,
`throwsSslHandshakeFailure()`, `throwsConnectTimeout()`, `throwsTimeoutAfterSend()`,
`throwsConnectionReset()`, `returnsBare503()`, `returnsServerError()`,
`hangsUntilAborted()`, `pending()`, and raw escapes `returns(...)` / `throwsIo(...)`.
Synthetic data only — no real PAN/CVV/PII ever appears in the mock.

## Logging & debugging

- `logger`: console-compatible (`console` works as-is). Default output is
  **values-free** — operation, status, class, correlation id. Debug level carries
  **allowlist-scrubbed** payloads only; PAN/CVV/PII and the API key can never appear
  (the API key is also absent from every error message).
- `wireTraceHook`: a request/response observer for Enablement escalations — payloads
  arrive already scrubbed by the runtime's central allowlist scrubber.
- Every response and every typed error carries the `X-Correlation-ID`; quote it in
  support tickets to join RAP-core telemetry directly.

## What this SDK never does

No hidden retries, no resubmission, no circuit breaker, no cross-request state, no
`bypassPlatform`. The explicit, caller-bounded reconcile re-poll is the only loop the
SDK owns. Classification never derives from message text, latency, or wait heuristics.

## Beyond payments

The full generated V2 surface ships in the same package and flows through the same
transport, headers and classification:

```ts
const methods = await client.paymentMethods.listPaymentMethods({ /* ... */ });
const byId = await client.transactions.getTransactionByIdRaw({ transactionId: 'txn-1' });
```
