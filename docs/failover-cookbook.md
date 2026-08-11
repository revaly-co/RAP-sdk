# RAP Integration SDK — Failover Cookbook

Task-oriented recipes for building and testing a failover handler with the Revaly RAP SDK.

This is the practical companion to [`failover-contract.md`](failover-contract.md), which is the
normative specification. Where the two appear to differ, the contract wins — and please
[open an issue](https://github.com/revaly-co/RAP-sdk/issues), because that difference is a bug in
this file.

Code appears in the language that shows the idea most compactly; each language's complete,
copy-paste version lives in its own quickstart (`languages/<language>/README.md`).

**Contents**

1. [Choose a reconcile key](#1-choose-a-reconcile-key)
2. [Handle all three outcome classes](#2-handle-all-three-outcome-classes)
3. [Reconcile after an unknown outcome](#3-reconcile-after-an-unknown-outcome)
4. [Choose a reconcile policy](#4-choose-a-reconcile-policy)
5. [Decide what to do on sustained `NotFoundYet`](#5-decide-what-to-do-on-sustained-notfoundyet)
6. [Tune the deadlines](#6-tune-the-deadlines)
7. [Test the handler with no network](#7-test-the-handler-with-no-network)
8. [Debug a payment with correlation IDs](#8-debug-a-payment-with-correlation-ids)
9. [Keep the integration forward-compatible](#9-keep-the-integration-forward-compatible)
10. [Use the rest of the API surface](#10-use-the-rest-of-the-api-surface)

---

## 1. Choose a reconcile key

`merchantTransactionId` is required on every payment request, and it is the only handle that lets
you ask "what happened to that payment?" after an ambiguous failure. Treat it as part of your
order state, not as a log line.

**Do this**

- Generate it in your own system, before the call.
- Persist it — in the same transaction that records the payment attempt — before you send the
  charge. A key that only exists in memory disappears exactly when you need it.
- Keep it unique per *attempt*, and make the relationship to the order recoverable:
  `order-1042-attempt-1` is a good shape, because a second attempt gets its own key while staying
  greppable.
- Stay within 100 characters.

**Why per-attempt:** if attempt 1 ends in `OutcomeUnknown` and you later make attempt 2, distinct
keys let you reconcile each attempt independently. A shared key collapses two questions into one
ambiguous answer.

## 2. Handle all three outcome classes

Every failed payment call resolves to exactly one class, and each class has exactly one correct
reaction. Handle all three explicitly, then let anything else propagate — a cancellation, a
validation error in your own code, or a bug is not a payment outcome.

```ts
try {
    const transaction = await client.charge(request);
    return approved(transaction);
} catch (failure) {
    if (failure instanceof RapPermanentRejection) {
        // Received and rejected. Fix the request or decline the payment.
        // Sending it elsewhere reproduces the same rejection.
        return declined(failure.apiError, failure.correlationId);
    }
    if (failure instanceof RapTransientFailure) {
        // Definitively not processed. Route to your own gateway now.
        return routeToOwnGateway(request);
    }
    if (failure instanceof RapOutcomeUnknown) {
        // May have been processed. Reconcile first (recipe 3).
        return reconcileThenDecide(request.merchantTransactionId);
    }
    throw failure;
}
```

The same three branches, in each language's idiom:

| Language | Branch on |
| --- | --- |
| .NET | `catch (PermanentRejectionException)` / `TransientFailureException` / `OutcomeUnknownException` — all under `RapCoreException` |
| Java | `catch (PermanentRejectionException …)` / `TransientFailureException` / `OutcomeUnknownException` |
| PHP | `catch (PermanentRejectionException …)` / `TransientFailureException` / `OutcomeUnknownException` |
| TypeScript | `instanceof RapPermanentRejection` / `RapTransientFailure` / `RapOutcomeUnknown`, or `toRapResult()` and switch on `failure.kind` |
| Python | `except RapPermanentRejection` / `RapTransientFailure` / `RapOutcomeUnknown` |
| Go | `errors.As(err, &pr)` with `*revaly.PermanentRejection` / `*revaly.TransientFailure` / `*revaly.OutcomeUnknown` |

**Classify on the class only.** The human-readable `error` message, the latency, and how long you
waited are all inadmissible as evidence — the SDK has already applied the normative algorithm, and
the class is its conclusion. `details` is opaque: log it, don't branch on it.

## 3. Reconcile after an unknown outcome

`OutcomeUnknown` means the payment may have been processed. Reconcile converts that into something
you can act on:

```ts
const verdict = await client.reconcile(merchantTransactionId, policy);

switch (verdict.kind) {
    case 'Found':
        // The record IS visible. Found(Approved) means the money moved, so this
        // payment is complete — sending it anywhere else would charge twice.
        // Found(declined / terminal-failed) is a terminal state: your call, and
        // your own gateway is safe from here.
        return settle(verdict.outcome, verdict.transaction);

    case 'NotFoundYet':
        // Not visible YET. Absence is not provable in V1 (recipe 5).
        return holdAndEscalate(verdict.attempts, verdict.lastCorrelationId);

    default:
        // Verdict types are open for extension. SafeToFailover arrives with
        // platform P-2 as a minor release. Always keep this branch.
        return escalateToOperator(verdict);
}
```

Entry points: `rap.ReconcileAsync(id, new ReconcilePolicy(...))` (.NET) ·
`client.reconcile(id, ReconcilePolicy.builder()...build())` returning `RapReconcileVerdict.Found`
or `.NotFoundYet` (Java) · `$client->reconcile($id, new ReconcilePolicy(...))` returning
`Revaly\Sdk\Reconcile\Found` or `NotFoundYet` (PHP) · `client.reconcile(id, {...})` (TypeScript) ·
`client.reconcile(id, ...)` (Python) · `client.Reconcile(ctx, id, revaly.ReconcilePolicy{...})`
(Go).

The helper is GET-only and side-effect-free. Calling it never sends a payment, so it is safe to
call again after a `NotFoundYet` — that is how you re-poll beyond one policy budget.

## 4. Choose a reconcile policy

V1 ships no default policy on purpose: the right bounds depend on what your checkout can wait for,
and shipping a number would imply a promise about platform visibility lag that isn't measured yet.
Pass a policy explicitly.

A policy bounds three things:

| Bound | Question it answers |
| --- | --- |
| Backoff schedule | How fast do I ask again? (exponential with jitter is the sensible default shape) |
| Per-attempt deadline | How long may one GET take? |
| Overall budget | When does this loop stop, regardless of attempts? |

Two shapes that work:

- **Inline hold (synchronous checkout).** A few attempts inside a short overall budget — long
  enough for typical visibility lag, short enough that the customer isn't watching a spinner. On
  `NotFoundYet`, escalate rather than extending the loop in the request path.
- **Deferred resolution (worker).** A short inline attempt for the common case, then hand the key
  to a background worker that re-polls on a longer schedule and settles the order later. This is
  the shape to prefer when your checkout cannot hold.

Pass cancellation in the language's idiom — `CancellationToken`, `context.Context`,
`AbortSignal` — so a shutdown or an abandoned checkout stops the loop cleanly.

## 5. Decide what to do on sustained `NotFoundYet`

`NotFoundYet` means *not visible yet*, never *didn't happen*. Platform visibility is asynchronous
and unbounded, and the lag is widest exactly when RAP-core is degraded — which is exactly when you
are asking.

So V1 gives you two verdicts and no third one that says "safe to fail over." What to do with a
sustained `NotFoundYet` is a risk decision that belongs to you:

- **Hold and escalate** is the default the contract supports: park the order in a
  needs-resolution state, alert an operator, keep re-polling on a slower schedule.
- **Fail over anyway** is a decision some merchants will make. If you make it, make it
  deliberately, in your own code, against your own policy — and know that you are accepting a
  double-charge risk the SDK cannot quantify for you.

Diagnostics on the verdict help you tell the two situations apart: `attempts`, `elapsed`,
`lastCorrelationId`, and `lastHttpStatus`. A **null last HTTP status with attempts > 0** means no
attempt ever got an HTTP response at all — RAP-core was unreachable for the whole budget, rather
than answering "not found." The merchant action is the same, but the alert you raise should differ.

**Coming with platform P-2:** a synchronous intent reservation makes absence provable, and the
helper gains a `SafeToFailover` verdict as a minor release. Code written with a default branch
today picks it up without a rewrite.

## 6. Tune the deadlines

| Bound | Default | On expiry |
| --- | --- | --- |
| Connect | **10 s** (ADR-SDK-029) | Provably never sent → `TransientFailure`, safe to fail over immediately |
| Overall | **75 s** (ADR-SDK-027) | After send → `OutcomeUnknown`, always. Reconcile; never resubmit |

Both defaults are ratified from production data rather than chosen for roundness: the overall
deadline clears every observed gateway tail cluster, and the connect default matches the
edge-verified behaviour. The asymmetry is deliberate — a connect timeout proves non-dispatch, and
a timeout after send proves nothing.

Tighten the overall deadline to your checkout budget if you like, remembering that RAP routes
gateways server-side, so the bound must cover the slowest common class rather than the median.
Per-language notes: TypeScript exposes no `connectTimeout` (WHATWG fetch cannot bound the connect
phase per request; Node's undici default is already the ratified 10 s, tunable with a dispatcher),
and PHP's errno 28 keeps timeouts on `OutcomeUnknown` because it cannot separate the phases.

## 7. Test the handler with no network

Every SDK ships a first-class mock transport that scripts each row of the taxonomy, both reconcile
verdicts, and consecutive outcomes — using synthetic data only. Testing your failover handler is a
supported first-class scenario, not a workaround.

```ts
const mock = new RapMockTransport();
mock.charge().returnsNotProcessed503();                       // → RapTransientFailure
mock.reconcile('order-1042').notFoundYet(2).thenFoundApproved();

const client = new RapClient({ apiKey: 'sk-synthetic', transport: mock });

// Script a sequence to exercise your own escalation logic:
mock.charge().returnsBare503().throwsConnectionRefused().returnsApproved();
```

Scenario vocabulary mirrors the contract, so a test names the row it covers:
`returnsPermanentRejection(status)`, `returnsNotProcessed503()`, `returnsBare503()`,
`returnsServerError()`, `throwsConnectionRefused()`, `throwsDnsFailure()`,
`throwsSslHandshakeFailure()`, `throwsConnectTimeout()`, `throwsTimeoutAfterSend()`,
`throwsConnectionReset()`, `hangsUntilAborted()`, `pending()`, plus reconcile scripting and raw
escapes. Method casing follows each language.

Where the mock lives: `Revaly.Sdk.Testing` (.NET) · `co.revaly.sdk.testing` (Java) ·
`Revaly\Sdk\Testing` (PHP) · `@revaly/sdk` (TypeScript) · `revaly_sdk.testing` (Python) ·
`github.com/revaly-co/rap-sdk/languages/go/raptest` (Go).

**A handler is covered when its tests include:** each of the three classes; `Found(approved)`
after one or more `NotFoundYet`; `Found(declined)`; sustained `NotFoundYet` to your escalation
path; the default verdict branch; and a non-payment exception propagating untouched. The mock also
records requests and asserts the SDK `User-Agent` leads each one, so you can assert on what your
code actually sent.

For end-to-end coverage, sandbox BIN-routing test cards exercise the real path — sandbox and live
share one URL, and your key's scope selects the environment.

## 8. Debug a payment with correlation IDs

Every response and every typed error carries the request correlation ID (`X-Correlation-ID`).

- **Log it on every branch**, including the happy path. It is the join key between your logs and
  RAP-core telemetry.
- **Quote it in support tickets.** One correlation ID plus one `merchantTransactionId` is
  everything Enablement needs to trace a payment end to end.
- **On `NotFoundYet`, log `lastCorrelationId`** — it identifies the last reconcile read, which is
  what tells the platform side where to look.

For deep escalations, the wire-trace hook gives you a request/response observer whose payloads
arrive already scrubbed by the runtime's central allowlist scrubber, so structured observability
never becomes a PCI exposure.

**Log safely by default.** Default verbosity is values-free: operation, status, class, correlation
ID. Debug level carries allowlist-scrubbed payloads only, and the API key appears in neither logs
nor exception messages. One caution when you go beyond payments: raw core operations surface the
generator's own error types carrying full response bodies, which can contain names, emails and
masked card data. Log the correlation ID and the typed runtime errors instead of raw core errors or
response bodies.

## 9. Keep the integration forward-compatible

Four habits keep your handler working across SDK minors:

1. **Always keep the default verdict branch.** `SafeToFailover` is coming as a *minor* release,
   and an exhaustive switch without a default silently mishandles it.
2. **Treat `code` and `transactionType` as open strings.** Don't build a closed enum or an
   exhaustive match over them; an unrecognized `code` is handled as absent, which lands on
   `OutcomeUnknown` — the cautious direction.
3. **Branch on class, not status.** Status codes are inputs to the algorithm, and the algorithm can
   gain rows. The three classes are the stable surface.
4. **Pin `X-Api-Version: 2.1`** (the default). Selecting `2.0` drops `ErrorResponse.code` from the
   documented surface, which narrows fast failover to provable never-sent failures — worth knowing
   if you inherit a frozen 2.0 integration.

Support policy: current and previous minor per package, deprecations announced in release notes and
registry metadata, a migration guide per major, and security patches on the latest GA of every
supported major.

## 10. Use the rest of the API surface

Payments are the safety-critical path, and the full generated V2 surface ships in the same package,
flowing through the same transport, headers, and classification: payment methods, transactions, and
notify.

```ts
const methods = await client.paymentMethods.listPaymentMethods({ /* ... */ });
const byId = await client.transactions.getTransactionByIdRaw({ transactionId: 'txn-1' });
```

Prefer the runtime's typed helpers where they exist — `reconcile()` classifies a transaction lookup
for you, where the raw core operation hands back a response for you to interpret. And keep the
logging caution from recipe 8 in mind on this surface.
