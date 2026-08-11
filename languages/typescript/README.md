# Revaly RAP SDK for TypeScript

Server-side TypeScript/JavaScript SDK for the RAP V2 API: payments, payment methods,
transactions and notify — with a **merchant-facing failover contract** built in. Every
failed payment call rejects with exactly one of three typed classes that tell you what
you may safely do next.

> **Install:** `npm install @revaly/sdk` — published on npm. Requires Node.js ≥ 20.3
> (or any runtime with WHATWG `fetch` and `AbortSignal.any`). GitHub release artifacts
> remain the provenance anchor and fallback channel.

## Why the error classes matter (read this first)

A failed `charge(...)` does **not** mean the payment didn't happen. If you blind-fail-over
to your own gateway on an ambiguous failure, the cardholder can be charged **twice**.
The SDK classifies every failure so you never have to guess:

| Class | Meaning | What you do |
| --- | --- | --- |
| `RapPermanentRejection` | Received and rejected (400/401/403/404/422) | Fix or decline — failing over reproduces the same rejection anywhere. |
| `RapTransientFailure` | **Definitively not processed** (provably never sent, or `503` + `code: not_processed`) | Route to your own gateway immediately. |
| `RapOutcomeUnknown` | **May have been processed** (timeout after send, reset, 5xx) | **Reconcile before acting** — see below. |

## Quickstart (sandbox key → first charge, ≤ 15 minutes)

Your API key's scope selects the environment: sandbox and live share the same URL —
there is no separate sandbox host. Use the sandbox-scoped key issued by Enablement.

```bash
npm install @revaly/sdk
```

> Prefer to install from a verified artifact? Every release also attaches
> `revaly-sdk-typescript.tgz` with a `.sha256` and a `provenance.json`; verify the checksum, then
> `npm install ./revaly-sdk-typescript.tgz`.

> **TypeScript config note:** the generated core's packaged typings reference WHATWG-fetch
> type aliases (`RequestCredentials`, `WindowOrWorkerGlobalScope`) that `@types/node` does
> not declare globally. A strict Node-only project compiling with `skipLibCheck: false`
> and no `"DOM"` lib therefore fails on the packaged `.d.ts`; compile with
> `skipLibCheck: true` (the `tsc --init` default) or add `"DOM"` to `compilerOptions.lib`.
> The hand-written runtime typings are Node-clean; emitting the core's typings without
> the DOM aliases is tracked for the pre-GA generator-template review (ADR-SDK-023).

```ts
import {
    RapClient,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransientFailure,
} from '@revaly/sdk';

const client = new RapClient({ apiKey: process.env.RAP_API_KEY! });

try {
    const transaction = await client.charge({
        amount: 1999,
        currency: 'USD',
        merchantTransactionId: 'order-1042', // required on every payment — it is your reconcile handle
        orderId: 'order-1042', // orderId + email below: the sandbox simulator requires both for an approval
        // paymentMethodType is omitted — inferred from the one populated method object
        paymentMethod: {
            fullName: 'Ada Lovelace', // creditCard requires a cardholder name
            email: 'ada@example.com',
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
        // Fix or decline — failing over reproduces the same rejection anywhere.
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
            case 'Found':
                // The record IS visible. Found(Approved) means the money moved —
                // failing over now would double-charge.
                console.log('resolved', verdict.outcome, verdict.transaction?.transactionId);
                break;
            case 'NotFoundYet':
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
import { toRapResult } from '@revaly/sdk';

const result = await toRapResult(() => client.charge(request));
if (!result.ok) {
    switch (result.failure.kind) {
        case 'TransientFailure': /* fail over */ break;
        case 'PermanentRejection': /* fix or decline */ break;
        default: /* OutcomeUnknown and anything future: reconcile / escalate */ break;
    }
}
```

### Timeouts

`overallDeadlineMs` defaults to **75 seconds** (`DEFAULT_OVERALL_DEADLINE_MS`) —
ratified from production latency telemetry (ADR-SDK-027): it clears every observed
gateway tail cluster (the worst non-hung tail seen in 14 fleet days was 64 s), clips
≲0.007% of charges, and still classifies well before the platform's own ≈100 s ceiling.
Tighten it per your checkout budget (RAP routes gateways server-side, so the default
must cover the slowest common class), or pass `overallDeadlineMs: null` to disable the
SDK deadline. Expiry after send classifies `RapOutcomeUnknown` (reconcile), never
TransientFailure.

**Connect bounding comes from your dispatcher rather than an SDK option** — WHATWG fetch
cannot bound the connect phase per request, so the SDK stays out of its way instead of
implying control it doesn't have. The OQ-11-ratified connect default is **10 seconds**
(ADR-SDK-029) — exactly undici's own default, so on Node you are bounded at the
ratified number with zero configuration. A connect-phase timeout is reported
structurally and — because it proves the request never left — classifies
`RapTransientFailure`. To tune the bound, pass a dispatcher (the example pins the
ratified 10 s explicitly; tighten per your own budget):

```ts
import { Agent } from 'undici'; // your app's dependency, not the SDK's

const client = new RapClient({
    apiKey: process.env.RAP_API_KEY!,
    dispatcher: new Agent({ connect: { timeout: 10_000 } }),
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
import { RapClient, RapMockTransport } from '@revaly/sdk';

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

Normative form: [`docs/failover-contract.md`](../../docs/failover-contract.md) §5 and
Appendix A.

## Beyond payments

The full generated V2 surface ships in the same package and flows through the same
transport, headers and classification:

```ts
const methods = await client.paymentMethods.listPaymentMethods({ /* ... */ });
const byId = await client.transactions.getTransactionByIdRaw({ transactionId: 'txn-1' });
```

One logging caution on this surface: raw core operations reject with the generator's
error types (e.g. `ResponseError`, carrying the full `Response`), not the three typed
classes. Response bodies can contain PII (names, emails, masked card data) — never log
raw core errors or response bodies; log the correlation id and the typed runtime errors
(values-free by design) instead.

## Where to go next

- [Failover cookbook](../../docs/failover-cookbook.md) — recipes for each outcome, choosing a
  reconcile policy, testing offline, debugging with correlation ids.
- [Failover contract](../../docs/failover-contract.md) — the normative specification, with
  sequence diagrams and the verbatim prohibitions in Appendix A.
- [AGENTS.md](../../AGENTS.md) — the whole contract on one page, for AI coding agents.
- [Support](../../SUPPORT.md) · [Contributing](../../CONTRIBUTING.md) · [Security](../../SECURITY.md)
