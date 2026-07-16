using Revaly.Sdk.Errors;
using Revaly.Sdk.Reconcile;
using Revaly.Sdk.Testing;
using Revaly.Sdk.Tests.TestSupport;

namespace Revaly.Sdk.Tests;

/// <summary>
/// Mirrors the quickstart (languages/dotnet/README.md) against the mock transport —
/// the DX-contract §d requirement that our own quickstart tests use the mock. If this
/// test needs to change shape, the README changes with it.
/// </summary>
public class QuickstartTests
{
    private static async Task<string> RunQuickstartFlow(RapClient client, string merchantTransactionId)
    {
        try
        {
            var response = await client.Payments.ChargePaymentAsync(
                TestClient.ChargeRequest(merchantTransactionId));
            response.TryOk(out var transaction);
            return $"approved:{transaction!.TransactionId}";
        }
        catch (PermanentRejectionException ex)
        {
            // Fix or decline. Never fail over — the same request fails anywhere.
            return $"rejected:{ex.StatusCode}";
        }
        catch (TransientFailureException)
        {
            // Definitively not processed — route to your own gateway immediately.
            return "failover";
        }
        catch (OutcomeUnknownException)
        {
            // May have been processed — reconcile before acting.
            var verdict = await client.ReconcileAsync(
                merchantTransactionId,
                new ReconcilePolicy(
                    maxAttempts: 5,
                    overallBudget: TimeSpan.FromSeconds(30),
                    initialDelay: TimeSpan.FromMilliseconds(1)));

            return verdict switch
            {
                FoundVerdict { Outcome: RapTransactionOutcome.Approved } => "reconciled-approved",
                FoundVerdict { IsTerminal: true } => "reconciled-terminal",
                FoundVerdict => "reconciled-keep-polling",
                NotFoundYetVerdict => "hold-and-escalate",
                // The verdict set is open for extension (SafeToFailover arrives with
                // P-2): unknown verdicts are treated conservatively.
                _ => "hold-and-escalate",
            };
        }
    }

    [Fact]
    public async Task Success_path()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock);

        Assert.Equal($"approved:{SyntheticData.TransactionId}", await RunQuickstartFlow(client, SyntheticData.MerchantTransactionId));
    }

    [Fact]
    public async Task Rejection_path()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsRejected(422);
        using var client = TestClient.Create(mock);

        Assert.Equal("rejected:422", await RunQuickstartFlow(client, SyntheticData.MerchantTransactionId));
    }

    [Fact]
    public async Task Fast_failover_path()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsNotProcessed503();
        using var client = TestClient.Create(mock);

        Assert.Equal("failover", await RunQuickstartFlow(client, SyntheticData.MerchantTransactionId));
    }

    [Fact]
    public async Task Outcome_unknown_then_reconciled_approved_path()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsTimeoutAfterSend();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsNotFoundYet().ReturnsApproved();
        using var client = TestClient.Create(mock);

        Assert.Equal("reconciled-approved", await RunQuickstartFlow(client, SyntheticData.MerchantTransactionId));
    }

    [Fact]
    public async Task Outcome_unknown_then_sustained_absence_path()
    {
        var mock = new RapMockTransport();
        mock.Charge().Returns500();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsNotFoundYet();
        using var client = TestClient.Create(mock);

        Assert.Equal("hold-and-escalate", await RunQuickstartFlow(client, SyntheticData.MerchantTransactionId));
    }
}
