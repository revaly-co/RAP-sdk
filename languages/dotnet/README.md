# Revaly RAP SDK for .NET

Server-side .NET SDK for the RAP V2 API. One package: a hand-written runtime
(`runtime/Revaly.Sdk`) over the generated API core (`core/`, produced by regeneration only).
Requires .NET 10.

> **Install:** `dotnet add package Revaly.Sdk` — published on NuGet (the generated core
> rides in as the `Revaly.Sdk.Core` dependency). GitHub release artifacts (asset +
> `.sha256` + `provenance.json`) remain the provenance anchor and fallback channel.

The quickstart below is the complete safety-critical path — **read the error handling,
not just the happy path**. Target: sandbox key in hand → first successful sandbox charge
in ≤ 15 minutes.

## 1. Initialize the client

```csharp
using Revaly.Sdk;

using var rap = new RapClient(new RapClientOptions
{
    // Enablement-issued sandbox-scoped key. Sandbox and live share the same URL —
    // your key's scope selects the environment (there is no separate sandbox host).
    ApiKey = Environment.GetEnvironmentVariable("RAP_API_KEY")!,
    // ApiVersion defaults to "2.1". Selecting "2.0" narrows fast failover: without the
    // ErrorResponse.code contract, a 503 + not_processed classifies OutcomeUnknown
    // (reconcile) instead of TransientFailure (immediate failover). Keep 2.1.
    // OverallDeadline defaults to 75 s (telemetry-ratified — ADR-SDK-027); expiry after
    // send classifies OutcomeUnknown, never TransientFailure. Set OverallDeadline to tighten
    // it to your checkout budget, or opt out with Timeout.InfiniteTimeSpan (HttpClient's 100 s
    // then applies).
    // ConnectTimeout defaults to 10 s (edge-verified — ADR-SDK-029); expiry is provably
    // never-sent and classifies TransientFailure (safe to fail over immediately). Opt out
    // with Timeout.InfiniteTimeSpan (SocketsHttpHandler then applies no connect bound).
});
```

Create **one client per configuration** and share it — it is thread-safe. The client
sends `Authorization: ApiKey <key>`, pins `X-Api-Version`, and stamps the SDK
`User-Agent` on every request automatically. Logging is **values-free by default**
(plug in your `ILoggerFactory` via `RapClientOptions.LoggerFactory`); no payload values,
PAN, CVV, or API keys ever appear in logs or exception messages.

> **Logging caution for raw core surfaces:** the values-free guarantee covers the
> runtime's typed errors and its own logs. Core response objects (`ApiResponse<T>`)
> expose the raw HTTP body (`RawContent`), and core-level exceptions can carry response
> content — response bodies can contain PII (names, emails, masked card data). Never log
> raw core responses or exception payloads; log the correlation id instead.

## 2. Charge — and handle all three failure classes

A failed `POST /payments` does **not** mean the payment didn't happen. Every failure the
SDK raises is one of three classes, and each has exactly one safe reaction:

```csharp
using Revaly.Sdk.Core.Client;
using Revaly.Sdk.Core.Model;
using Revaly.Sdk.Errors;
using Revaly.Sdk.Reconcile;

var merchantTransactionId = $"order-{Guid.NewGuid():N}"; // YOUR id — required, max 100 chars; keep ≤ 48 for gateway compatibility.
                                                         // It is the reconcile key: persist it
                                                         // BEFORE sending the request.

var request = new PaymentRequest(
    amount: 1999,                                        // minor units
    merchantTransactionId: merchantTransactionId,
    currency: new Option<string?>("USD"),
    // orderId + email: the sandbox simulator requires both for an approval.
    orderId: new Option<string?>(merchantTransactionId),
    // paymentMethodType is omitted — inferred from the one populated method object.
    paymentMethod: new Option<PaymentMethod?>(new PaymentMethod(
        fullName: new Option<string?>("Ada Lovelace"),    // creditCard requires a cardholder name
        email: new Option<string?>("ada@example.com"),
        creditCard: new Option<CreditCard?>(new CreditCard(
            "4111111111111111", "12", "2030",             // sandbox test card
            cardVerificationCode: new Option<string?>("123"))))));

try
{
    var response = await rap.Payments.ChargePaymentAsync(request);
    response.TryOk(out var transaction);
    Console.WriteLine($"approved: {transaction!.TransactionId}");
    // transaction.PaymentMethod?.VaultToken (spec >= 2.4.0) ties this charge back to the
    // stored credential it ran against — set only when a vault credential was used, and it
    // may reflect an Account Updater roll. Treat it as optional; absence proves nothing.
}
catch (PermanentRejectionException ex)
{
    // Received and rejected (400/401/403/404/422): fix the request or decline.
    // Failing over reproduces the same rejection at any gateway.
    Console.WriteLine($"rejected ({ex.StatusCode}): {ex.ErrorMessage} [correlation {ex.CorrelationId}]");
}
catch (TransientFailureException)
{
    // Definitively NOT processed (never-sent transport failure, or 503 with
    // code=not_processed): route this payment to your own gateway immediately.
    RouteToOwnGateway();
}
catch (OutcomeUnknownException ex)
{
    // The payment MAY have been processed (timeout after send, 500/502/504, bare 503).
    // Blind failover here can charge the cardholder twice. Reconcile first: ↓
    Console.WriteLine($"outcome unknown [correlation {ex.CorrelationId}] — reconciling…");
    await ReconcileBeforeActing(rap, merchantTransactionId);
}
```

## 3. Reconcile — the OutcomeUnknown procedure

```csharp
async Task ReconcileBeforeActing(RapClient rap, string merchantTransactionId)
{
    var verdict = await rap.ReconcileAsync(
        merchantTransactionId,
        // All bounds are explicit and yours to choose: this loop is how long your
        // checkout holds before escalating. (Deliberately explicit — reconcile defaults
        // await visibility-lag telemetry; ADR-SDK-027 ratified only the request deadline.)
        new ReconcilePolicy(
            maxAttempts: 6,
            overallBudget: TimeSpan.FromSeconds(45),
            initialDelay: TimeSpan.FromSeconds(1)));

    switch (verdict)
    {
        case FoundVerdict { Outcome: RapTransactionOutcome.Approved } found:
            // The money moved at RAP: this payment is complete — fulfil the order.
            Console.WriteLine($"already approved: {found.Transaction!.TransactionId}");
            break;

        case FoundVerdict { IsTerminal: true } found:
            // Declined / errored at RAP (terminal): your own gateway is now safe
            // to use — that decision is your risk policy, not the SDK's.
            Console.WriteLine($"terminal outcome: {found.Outcome}");
            break;

        case FoundVerdict found:
            // Pending intent reservation (platform P-2): keep polling.
            Console.WriteLine($"visible but not terminal ({found.Outcome}) — poll again");
            break;

        case NotFoundYetVerdict notFound:
            // NOT proof of absence — visibility is asynchronous, and widest exactly
            // when RAP is degraded. Hold and escalate per your policy; quote the
            // correlation id in support tickets.
            Console.WriteLine(
                $"not visible after {notFound.Attempts} attempts / {notFound.Elapsed}: " +
                $"hold + escalate [correlation {notFound.LastCorrelationId}]");
            break;

        default:
            // The verdict set is OPEN: SafeToFailover arrives with platform P-2 as a
            // minor release. Treat verdicts you don't recognize conservatively.
            Console.WriteLine("unrecognized verdict — hold and escalate");
            break;
    }
}
```

## 4. Test your failover handler with no network

The mock transport ships in the package (`Revaly.Sdk.Testing`) and simulates every row
of the failure taxonomy with synthetic data only:

```csharp
using Revaly.Sdk.Testing;

var mock = new RapMockTransport();
mock.Charge().ReturnsNotProcessed503();                    // → TransientFailureException
mock.Reconcile("order-1").ReturnsNotFoundYet()             // script consecutive outcomes
                         .ReturnsApproved();

using var rap = new RapClient(new RapClientOptions
{
    ApiKey = "sk_synthetic_test",
    Transport = mock,                                       // no network
});

// exercise YOUR handler exactly like production code
```

Also available: `ReturnsApproved/Declined/Rejected(status)`, `ReturnsBare503`,
`Returns500/502/504`, `ReturnsTimeoutAfterSend`, `ReturnsConnectionRefused/DnsFailure/
TlsFailure/ResetMidFlight`, `ReturnsPending`, and `Stub(method, path)` for anything else.
`mock.Requests` records every request (the mock also asserts the SDK `User-Agent` is
present — it is part of the platform's adoption telemetry, ADR-SDK-005).

## Design guarantees

- **Each charge is sent exactly once.** Retry policy stays yours, with the
  classification that makes it safe to exercise.
- **Every call stands alone** — no cross-request state, no circuit breaker, so
  behaviour under load is the behaviour you tested.
- **The reconcile poll above is the only loop the SDK owns**, and you bound it.
- **Classification rests on evidence only**: HTTP status and `ErrorResponse.code`, via the
  normative algorithm (`docs/failover-contract.md` §2). Message text and latency are
  reported to you and excluded from the verdict.
- **Recovery beyond this boundary belongs to RAP-core** — resubmission and
  `bypassPlatform` are platform-internal, so a payment's outcome stays unambiguous.

Normative form: [`docs/failover-contract.md`](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-contract.md) §5 and
Appendix A.

## Where to go next

- [Failover cookbook](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-cookbook.md) — recipes for each outcome, choosing a
  reconcile policy, testing offline, debugging with correlation ids.
- [Failover contract](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-contract.md) — the normative specification, with
  sequence diagrams and the verbatim prohibitions in Appendix A.
- [AGENTS.md](https://github.com/revaly-co/RAP-sdk/blob/main/AGENTS.md) — the whole contract on one page, for AI coding agents.
- [Support](https://github.com/revaly-co/RAP-sdk/blob/main/SUPPORT.md) · [Contributing](https://github.com/revaly-co/RAP-sdk/blob/main/CONTRIBUTING.md) · [Security](https://github.com/revaly-co/RAP-sdk/blob/main/SECURITY.md)
