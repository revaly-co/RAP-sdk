using System.Diagnostics;
using Revaly.Sdk.Core.Client;
using Revaly.Sdk.Core.Model;
using Revaly.Sdk.Errors;
using Revaly.Sdk.Logging;
using Revaly.Sdk.Reconcile;

namespace Revaly.Sdk.Smoke;

/// <summary>
/// Stage-4 contract smoke (ADR-SDK-024, pipeline stage 4): a thin, live
/// runtime-contract check of THIS SDK against the environment named by
/// RAP_SMOKE_BASE_URL / RAP_SMOKE_API_KEY (interim: Backbone staging; at GA:
/// the merchant sandbox key-scope). Its single purpose is proving the SDK's
/// classification against reality — it deliberately does not replicate
/// platform test coverage.
///
/// Environment contract (same across all six languages):
/// RAP_SMOKE_BASE_URL (required), RAP_SMOKE_API_KEY (required),
/// RAP_SMOKE_GATEWAY_ROUTING_ID (optional — included in charge payloads when
/// set; staging routes by it), RAP_SMOKE_FAULT_INJECT (optional — sent as the
/// platform's X-Backbone-Fault-Inject header to trigger the
/// 503+not_processed row; the scenario SKIPs when unset).
///
/// Scenarios mirror the quickstart shape (README). Output is values-free
/// (ADR-SDK-020): identifiers, statuses, classes and correlation ids only —
/// never payload values, never the key, never the target host.
///
/// Exit codes: 0 all pass (skips allowed) · 1 at least one failed · 2 not
/// configured.
/// </summary>
internal static class Program
{
    private const string FaultInjectHeader = "X-Backbone-Fault-Inject";
    // The fault-injected charge must not present as a first attempt — the route
    // it takes depends on it. See charge-not-processed-503.
    private const int FaultRetryCount = 1;
    // One synthetic test PAN; the EXPIRY drives the outcome
    // (staging-verified matrix 2026-07-18: 12/2027 approves, 12/2020 declines).
    private const string TestPan = "4111111111111111";

    private static async Task<int> Main()
    {
        var baseUrl = Environment.GetEnvironmentVariable("RAP_SMOKE_BASE_URL");
        var apiKey = Environment.GetEnvironmentVariable("RAP_SMOKE_API_KEY");
        var routingId = Environment.GetEnvironmentVariable("RAP_SMOKE_GATEWAY_ROUTING_ID");
        var faultValue = Environment.GetEnvironmentVariable("RAP_SMOKE_FAULT_INJECT");
        if (string.IsNullOrEmpty(baseUrl) || string.IsNullOrEmpty(apiKey))
        {
            Console.Error.WriteLine("smoke: RAP_SMOKE_BASE_URL and RAP_SMOKE_API_KEY must be set (ADR-SDK-024) — refusing to run.");
            return 2;
        }

        // One client per configuration, quickstart-shaped. The wire-trace hook
        // is the designed observer for correlation ids on the success path
        // (DX §c); events arrive already scrubbed by the runtime.
        RapWireTrace? lastTrace = null;
        using var client = new RapClient(new RapClientOptions
        {
            ApiKey = apiKey,
            BaseUrl = new Uri(baseUrl),
            ConnectTimeout = TimeSpan.FromSeconds(5),
            OverallDeadline = TimeSpan.FromSeconds(15),
            WireTraceHook = trace => lastTrace = trace,
        });

        // A separately configured client whose key is a synthetic invalid
        // value — the auth-rejection row.
        using var badKeyClient = new RapClient(new RapClientOptions
        {
            ApiKey = "sk_smoke_synthetic_invalid",
            BaseUrl = new Uri(baseUrl),
            ConnectTimeout = TimeSpan.FromSeconds(5),
            OverallDeadline = TimeSpan.FromSeconds(15),
        });

        // A client whose transport stamps the platform's fault-inject header —
        // every charge through it deterministically fails pre-dispatch
        // (503 + code=not_processed). Only built when the scenario is enabled.
        using var faultClient = string.IsNullOrEmpty(faultValue)
            ? null
            : new RapClient(new RapClientOptions
            {
                ApiKey = apiKey,
                BaseUrl = new Uri(baseUrl),
                OverallDeadline = TimeSpan.FromSeconds(15),
                Transport = new HeaderInjectingHandler(FaultInjectHeader, faultValue),
            });

        // Charged ids feed the reconcile scenarios: the verdicts — through the
        // runtime's own outcome mapping — are the proof the charge outcomes
        // were what the smoke claims.
        var chargedId = FreshId("charge");
        var declinedId = FreshId("decline");

        var scenarios = new (string Name, Func<Task<string>> Run)[]
        {
            ("charge-approved", async () =>
            {
                var response = await client.Payments.ChargePaymentAsync(BuildCharge(chargedId, TestPan, "2027", routingId));
                if (!response.TryOk(out var transaction) || transaction is null)
                {
                    throw new SmokeFailure("2xx response did not bind a TransactionResponse");
                }
                if (string.IsNullOrEmpty(transaction.TransactionId))
                {
                    throw new SmokeFailure("transactionId is empty on the success surface");
                }
                // Assert the OUTCOME, not just that a transaction bound: a decline
                // arrives on this same success surface, so without this the scenario
                // would pass against a gateway that never approves.
                if (transaction.TransactionStatus != 1)
                {
                    throw new SmokeFailure($"expected transactionStatus=1 (approved), got {transaction.TransactionStatus?.ToString() ?? "-"}");
                }
                if (string.IsNullOrEmpty(lastTrace?.CorrelationId))
                {
                    throw new SmokeFailure("no X-Correlation-ID observed on the success path (DX §c)");
                }
                return $" (txn={transaction.TransactionId} correlation={lastTrace!.CorrelationId})";
            }
            ),

            ("charge-declined", async () =>
            {
                // An expired expiry declines deterministically (same PAN). A decline is a
                // business outcome on the SUCCESS surface — not a failure
                // class; reconcile-found-declined proves the mapping below.
                var response = await client.Payments.ChargePaymentAsync(BuildCharge(declinedId, TestPan, "2020", routingId));
                if (!response.TryOk(out var transaction) || transaction is null)
                {
                    throw new SmokeFailure("2xx response did not bind a TransactionResponse on the declined path");
                }
                if (string.IsNullOrEmpty(transaction.TransactionId))
                {
                    throw new SmokeFailure("transactionId is empty on the declined-charge surface");
                }
                // Assert the decline actually happened. Without this the scenario
                // passes against a gateway that approves the expired card, and the
                // failure only surfaces later in reconcile-found-declined.
                if (transaction.TransactionStatus != 2)
                {
                    throw new SmokeFailure($"expected transactionStatus=2 (declined), got {transaction.TransactionStatus?.ToString() ?? "-"} — the staging gateway must be one where expiry drives the outcome");
                }
                if (string.IsNullOrEmpty(lastTrace?.CorrelationId))
                {
                    throw new SmokeFailure("no X-Correlation-ID observed on the declined-charge path (DX §c)");
                }
                return $" (txn={transaction.TransactionId} correlation={lastTrace!.CorrelationId})";
            }
            ),

            ("charge-validation-rejected", async () =>
            {
                // A NAMELESS charge (no fullName / firstName / lastName)
                // passes every client-side model — php/python cores reject an
                // empty PAN locally, so the PAN stays valid — and fails the
                // server's cardholder-name business validation: the rejection
                // is proven to come from reality (HTTP 400; 4xx carries no
                // code).
                try
                {
                    await client.Payments.ChargePaymentAsync(BuildCharge(FreshId("validation"), TestPan, "2027", routingId, withName: false));
                }
                catch (PermanentRejectionException ex)
                {
                    if (ex.StatusCode is not (400 or 422))
                    {
                        throw new SmokeFailure($"expected HTTP 400/422, got {ex.StatusCode}");
                    }
                    if (string.IsNullOrEmpty(ex.CorrelationId))
                    {
                        throw new SmokeFailure("no X-Correlation-ID on the rejection (DX §c)");
                    }
                    return $" (status={ex.StatusCode} correlation={ex.CorrelationId})";
                }
                throw new SmokeFailure("server accepted an empty card number — expected PermanentRejection");
            }
            ),

            ("charge-auth-rejected", async () =>
            {
                try
                {
                    await badKeyClient.Payments.ChargePaymentAsync(BuildCharge(FreshId("auth"), TestPan, "2027", routingId));
                }
                catch (PermanentRejectionException ex)
                {
                    if (ex.StatusCode is not (401 or 403))
                    {
                        throw new SmokeFailure($"expected HTTP 401/403, got {ex.StatusCode}");
                    }
                    if (string.IsNullOrEmpty(ex.CorrelationId))
                    {
                        throw new SmokeFailure("no X-Correlation-ID on the auth rejection (DX §c)");
                    }
                    return $" (status={ex.StatusCode} correlation={ex.CorrelationId})";
                }
                throw new SmokeFailure("server accepted a synthetic invalid key — expected PermanentRejection");
            }
            ),

            ("charge-not-processed-503", async () =>
            {
                // The fast-failover row (503 + code=not_processed): valid
                // input cannot reach it deterministically, so the platform's
                // fault injector fails the charge pre-dispatch.
                // TransientFailure is the ONLY acceptable class here — it is
                // the row that licenses immediate failover.
                if (faultClient is null)
                {
                    throw new SmokeSkip("RAP_SMOKE_FAULT_INJECT not set (injector is staging-only)");
                }
                // retryCount > 0 keeps this charge on the route that carries the
                // seam. Backbone admits only FIRST attempts to the direct path
                // (DirectPathAttemptEligibility.IsFirstAttempt ==
                // "recovery.retryCount is not > 0"), and the pre-dispatch
                // injector exists only on the TransactionApi dispatch path — so
                // on a direct-path-enrolled account a first-attempt charge takes
                // the direct-send fork, never reaches the injector, and approves
                // (nightly 30983100997: red 6/6, 2026-08-05).
                var faultCharge = BuildCharge(FreshId("fault"), TestPan, "2027", routingId);
                faultCharge.Recovery = new Recovery(retryCount: new Option<int?>(FaultRetryCount));
                try
                {
                    await faultClient.Payments.ChargePaymentAsync(faultCharge);
                }
                catch (TransientFailureException ex)
                {
                    if (ex.StatusCode is not 503)
                    {
                        throw new SmokeFailure($"expected HTTP 503, got {ex.StatusCode}");
                    }
                    if (ex.Code != "not_processed")
                    {
                        throw new SmokeFailure($"expected code=not_processed, got \"{ex.Code}\"");
                    }
                    if (string.IsNullOrEmpty(ex.CorrelationId))
                    {
                        throw new SmokeFailure("no X-Correlation-ID on the not-processed failure (DX §c)");
                    }
                    return $" (status=503 code={ex.Code} correlation={ex.CorrelationId})";
                }
                throw new SmokeFailure("fault-injected charge succeeded — expected TransientFailure");
            }
            ),

            ("reconcile-found-approved", async () =>
            {
                // Found(Approved) through the runtime's own outcome mapping is
                // the approval proof for the first charge; visibility is
                // asynchronous, hence the budget.
                var verdict = await ReconcileSettledAsync(client, chargedId);
                return ExpectFound(verdict, RapTransactionOutcome.Approved);
            }
            ),

            ("reconcile-found-declined", async () =>
            {
                // The declined charge must reconcile as Found(Declined) — the
                // outcome branch that tells a merchant their own gateway is
                // safe.
                var verdict = await ReconcileSettledAsync(client, declinedId);
                return ExpectFound(verdict, RapTransactionOutcome.Declined);
            }
            ),

            ("reconcile-not-found-yet", async () =>
            {
                // A fresh, never-used merchantTransactionId (ADR-SDK-024): the
                // only correct verdict is NotFoundYet, and it must come from
                // real 404s — not from a transport that never reached the API.
                var verdict = await client.ReconcileAsync(FreshId("absent"), new ReconcilePolicy(
                    maxAttempts: 2,
                    overallBudget: TimeSpan.FromSeconds(10),
                    initialDelay: TimeSpan.FromMilliseconds(500)));
                switch (verdict)
                {
                    case NotFoundYetVerdict notFound:
                        if (notFound.LastHttpStatus != 404)
                        {
                            throw new SmokeFailure($"expected last HTTP status 404, got {notFound.LastHttpStatus}");
                        }
                        if (string.IsNullOrEmpty(notFound.LastCorrelationId))
                        {
                            throw new SmokeFailure("no X-Correlation-ID on the NotFoundYet verdict (DX §c)");
                        }
                        return $" (attempts={notFound.Attempts} correlation={notFound.LastCorrelationId})";
                    case FoundVerdict:
                        throw new SmokeFailure("a never-used id reconciled as Found");
                    default:
                        throw new SmokeFailure($"unrecognized verdict {verdict.GetType().Name}");
                }
            }
            ),
        };

        // Advisory preflight: asserts nothing and can never fail the suite. The
        // elapsed time is printed so a cold path stays VISIBLE rather than hidden.
        using var warmClient = new RapClient(new RapClientOptions
        {
            ApiKey = apiKey,
            BaseUrl = new Uri(baseUrl),
            ConnectTimeout = TimeSpan.FromSeconds(5),
            OverallDeadline = WarmupDeadline,
        });
        var warmStarted = Stopwatch.StartNew();
        string warmDetail;
        try
        {
            await warmClient.ReconcileAsync(FreshId("warmup"), new ReconcilePolicy(
                maxAttempts: 1,
                overallBudget: WarmupDeadline,
                initialDelay: TimeSpan.FromMilliseconds(500)));
            warmDetail = $"ready in {warmStarted.Elapsed.TotalSeconds:F1}s";
        }
        catch (Exception warmFailure)
        {
            warmDetail = $"not confirmed after {warmStarted.Elapsed.TotalSeconds:F1}s ({warmFailure.GetType().Name})";
        }

        Console.WriteLine($"RAP contract smoke (dotnet): {scenarios.Length} scenarios");
        Console.WriteLine($"WARM reconcile path {warmDetail}");
        var failures = 0;
        var skips = 0;
        foreach (var (name, run) in scenarios)
        {
            try
            {
                var detail = await run();
                Console.WriteLine($"PASS {name}{detail}");
            }
            catch (SmokeSkip skip)
            {
                skips++;
                Console.WriteLine($"SKIP {name} ({skip.Message})");
            }
            catch (SmokeFailure failure)
            {
                failures++;
                Console.WriteLine($"FAIL {name}: {failure.Message}");
            }
            catch (RapCoreException ex)
            {
                // Typed-class messages are values-free by construction
                // (class, status, code, correlation only).
                failures++;
                Console.WriteLine($"FAIL {name}: unexpected {ex.Message}");
            }
            catch (Exception ex)
            {
                // Never print raw exception messages — transport error chains
                // can carry endpoint details into CI logs.
                failures++;
                Console.WriteLine($"FAIL {name}: unexpected {ex.GetType().Name}");
            }
        }

        var passed = scenarios.Length - failures - skips;
        if (failures > 0)
        {
            Console.WriteLine($"RESULT: FAIL ({passed}/{scenarios.Length} passed, {skips} skipped)");
            return 1;
        }
        Console.WriteLine($"RESULT: PASS ({passed}/{scenarios.Length} passed, {skips} skipped)");
        return 0;
    }

    /// <summary>
    /// Charge request with the minimal live-approving field set (staging-verified
    /// 2026-07-18): a cardholder name is SERVER-required for creditCard (per-type
    /// rule, spec-documented since 2.3.0); paymentMethodType is optional since
    /// spec 2.3.0 (Backbone #251 inference) — sent explicitly here to keep the
    /// wire shape deterministic across the six languages. orderId + email are
    /// additionally required by the staging simulator for an approval.
    /// Synthetic test cards only.
    /// </summary>
    private static PaymentRequest BuildCharge(string merchantTransactionId, string pan, string expiryYear, string? routingId, bool withName = true)
        => new(
            amount: 1999,
            merchantTransactionId: merchantTransactionId,
            paymentMethodType: new Option<PaymentRequest.PaymentMethodTypeEnum?>(PaymentRequest.PaymentMethodTypeEnum.CreditCard),
            currency: new Option<string?>("USD"),
            orderId: new Option<string?>(merchantTransactionId),
            gatewayRoutingId: string.IsNullOrEmpty(routingId) ? default : new Option<string?>(routingId),
            paymentMethod: new Option<PaymentMethod?>(new PaymentMethod(
                fullName: withName ? new Option<string?>("Smoke Test") : default,
                email: new Option<string?>("smoke@example.com"),
                creditCard: new Option<CreditCard?>(new CreditCard(
                    pan, "12", expiryYear,
                    cardVerificationCode: new Option<string?>("123"))))));

    /// <summary>
    /// Asserts a Found verdict carrying the wanted outcome and a correlation
    /// id. The verdict set is open — an unrecognized verdict is a real finding
    /// here, not a pass.
    /// </summary>
    private static string ExpectFound(RapReconcileVerdict verdict, RapTransactionOutcome want)
    {
        switch (verdict)
        {
            case FoundVerdict found when found.Outcome == want:
                if (string.IsNullOrEmpty(found.CorrelationId))
                {
                    throw new SmokeFailure("no X-Correlation-ID on the Found verdict (DX §c)");
                }
                return $" (outcome={found.Outcome} correlation={found.CorrelationId})";
            case FoundVerdict found:
                throw new SmokeFailure($"expected outcome {want}, got {found.Outcome}");
            case NotFoundYetVerdict notFound:
                throw new SmokeFailure($"charge not visible after {notFound.Attempts} attempts ({notFound.Elapsed}) — expected Found");
            default:
                throw new SmokeFailure($"unrecognized verdict {verdict.GetType().Name}");
        }
    }

    /// <summary>
    /// Reconciles until the outcome settles. Under load a charge can be visible
    /// (Found) while its outcome is still Pending — a transient truth, not a
    /// verdict miss — so Found(Pending) gets a bounded re-poll instead of an
    /// instant assert. The loop lives in the harness because the caller owns
    /// the re-poll budget (ADR-SDK-009); NotFoundYet and settled outcomes
    /// return immediately.
    /// </summary>
    private static async Task<RapReconcileVerdict> ReconcileSettledAsync(RapClient client, string merchantTransactionId)
    {
        var policy = new ReconcilePolicy(
            maxAttempts: 5,
            overallBudget: TimeSpan.FromSeconds(30),
            initialDelay: TimeSpan.FromSeconds(1));
        var verdict = await client.ReconcileAsync(merchantTransactionId, policy);
        for (var settle = 0; settle < SettleAttempts; settle++)
        {
            if (verdict is not FoundVerdict found || found.Outcome != RapTransactionOutcome.Pending)
            {
                break;
            }
            await Task.Delay(SettleDelay);
            verdict = await client.ReconcileAsync(merchantTransactionId, policy);
        }
        return verdict;
    }

    private const int SettleAttempts = 6;
    private static readonly TimeSpan SettleDelay = TimeSpan.FromSeconds(2);

    /// <summary>
    /// The reconcile path (Backbone to Olympus) is COLD after hours of idle: on the
    /// 06:00 UTC nightly the first byMerchantTransactionId lookup was served in 41 s
    /// against ~100 ms warm (run 31078676574, 2026-08-06 — 7.4 h idle gap), and the
    /// three suites whose 15 s deadline expired first reported NotFoundYet with no
    /// HTTP status. That warm-up cost is an environment property, not SDK behaviour,
    /// so it is paid ONCE before the scenarios, which keeps every scenario assert
    /// strict instead of loosening the 404 check into a timeout tolerance.
    /// </summary>
    private static readonly TimeSpan WarmupDeadline = TimeSpan.FromSeconds(90);

    /// <summary>
    /// Unique merchantTransactionId — every reconcile scenario uses a fresh one
    /// (ADR-SDK-024). Kept under ~48 chars: the staging CyberSource simulator
    /// declines charges whose merchant reference exceeds ~50 (live-bisected
    /// 2026-07-18), even though the platform accepts up to 100.
    /// </summary>
    private static string FreshId(string label)
        => $"smoke-dotnet-{label}-{DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()}-{Guid.NewGuid().ToString("N")[..8]}";
}

/// <summary>A scenario assertion failure (values-free message).</summary>
internal sealed class SmokeFailure : Exception
{
    public SmokeFailure(string message)
        : base(message)
    {
    }
}

/// <summary>A scenario that cannot run in this environment (reported, never silently dropped).</summary>
internal sealed class SmokeSkip : Exception
{
    public SmokeSkip(string reason)
        : base(reason)
    {
    }
}

/// <summary>
/// A real-HTTP transport that stamps one extra header on every request. It
/// sits at the RapClientOptions.Transport seam, INSIDE the runtime's own
/// header injection, so auth/UA/version behaviour is unchanged. Used to send
/// the platform's fault-inject header (Backbone ADR 014 test affordance).
/// </summary>
internal sealed class HeaderInjectingHandler : DelegatingHandler
{
    private readonly string _name;
    private readonly string _value;

    public HeaderInjectingHandler(string name, string value)
        : base(new SocketsHttpHandler())
    {
        _name = name;
        _value = value;
    }

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        request.Headers.TryAddWithoutValidation(_name, _value);
        return base.SendAsync(request, cancellationToken);
    }
}
