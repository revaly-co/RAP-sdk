# Revaly RAP SDK for .NET

Server-side .NET SDK for the RAP V2 API. One package: a hand-written runtime
(`runtime/Revaly.Sdk`) over the generated API core (`core/`, never hand-edited).
Requires .NET 10.

> **Install (interim):** packages are distributed as GitHub release artifacts until
> registry publishing opens (the NuGet id `Revaly.Sdk` is proposed, not final). Download
> the release asset, verify its `.sha256`, and reference the package locally. This
> section becomes `dotnet add package Revaly.Sdk` at GA.

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
    // OverallDeadline defaults to 30 s (telemetry-ratified — ADR-SDK-027); expiry after
    // send classifies OutcomeUnknown, never TransientFailure. Tighten it to your checkout
    // budget, or opt out with Timeout.InfiniteTimeSpan (HttpClient's 100 s then applies).
    // ConnectTimeout has no SDK default — that needs client-side edge data (OQ-11).
});
```

Create **one client per configuration** and share it — it is thread-safe. The client
sends `Authorization: ApiKey <key>`, pins `X-Api-Version`, and stamps the SDK
`User-Agent` on every request automatically. Logging is **values-free by default**
(plug in your `ILoggerFactory` via `RapClientOptions.LoggerFactory`); no payload values,
PAN, CVV, or API keys ever appear in logs or exception messages.

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
    // paymentMethodType is omitted — inferred from the one populated method object.
    paymentMethod: new Option<PaymentMethod?>(new PaymentMethod(
        fullName: new Option<string?>("Ada Lovelace"),    // creditCard requires a cardholder name
        creditCard: new Option<CreditCard?>(new CreditCard(
            "4111111111111111", "12", "2030",             // sandbox test card
            cardVerificationCode: new Option<string?>("123"))))));

try
{
    var response = await rap.Payments.ChargePaymentAsync(request);
    response.TryOk(out var transaction);
    Console.WriteLine($"approved: {transaction!.TransactionId}");
}
catch (PermanentRejectionException ex)
{
    // Received and rejected (400/401/403/404/422): fix the request or decline.
    // NEVER fail over — the same request fails at any gateway.
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
            // The money moved at RAP. Do NOT fail over; fulfil the order.
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

## What this SDK never does

No retries, no resubmission, no circuit breaker, no cross-request state. The only loop
is the explicit, caller-bounded reconcile poll above. Classification never derives from
error message text or latency heuristics — only from the normative algorithm
(`docs/failover-contract.md` §2).
