using Revaly.Sdk.Errors;
using Revaly.Sdk.Reconcile;
using Revaly.Sdk.Testing;
using Revaly.Sdk.Tests.TestSupport;

namespace Revaly.Sdk.Tests;

/// <summary>
/// The reconcile helper per failover-contract §3: both V1 verdicts, the post-P-2 pending
/// state, caller-bounded polling, and the open-for-extension default branch.
/// </summary>
public class ReconcileTests
{
    private static ReconcilePolicy QuickPolicy(int attempts = 3)
        => new(attempts, TimeSpan.FromSeconds(30), TimeSpan.FromMilliseconds(1));

    [Fact]
    public async Task Sustained_absence_returns_NotFoundYet_with_diagnostics()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsNotFoundYet();
        using var client = TestClient.Create(mock);

        var verdict = await client.ReconcileAsync(SyntheticData.MerchantTransactionId, QuickPolicy(3));

        var notFound = Assert.IsType<NotFoundYetVerdict>(verdict);
        Assert.Equal(3, notFound.Attempts);
        Assert.Equal(404, notFound.LastHttpStatus);
        Assert.Equal(SyntheticData.CorrelationId, notFound.LastCorrelationId);
        Assert.Equal(3, mock.Requests.Count);
    }

    [Theory]
    [InlineData(1, RapTransactionOutcome.Approved)]
    [InlineData(2, RapTransactionOutcome.Declined)]
    [InlineData(3, RapTransactionOutcome.Error)]
    [InlineData(99, RapTransactionOutcome.Unknown)]
    public async Task Found_maps_documented_transaction_statuses_and_defaults_unknown(
        int transactionStatus, RapTransactionOutcome expected)
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId).Returns(
            System.Net.HttpStatusCode.OK,
            $"{{\"transactionId\":\"{SyntheticData.TransactionId}\",\"transactionStatus\":{transactionStatus}," +
            $"\"merchantTransactionId\":\"{SyntheticData.MerchantTransactionId}\"}}");
        using var client = TestClient.Create(mock);

        var verdict = await client.ReconcileAsync(SyntheticData.MerchantTransactionId, QuickPolicy(1));

        var found = Assert.IsType<FoundVerdict>(verdict);
        Assert.Equal(expected, found.Outcome);
        Assert.Equal(expected is not RapTransactionOutcome.Unknown, found.IsTerminal);
        Assert.NotNull(found.Transaction);
    }

    [Fact]
    public async Task Pending_intent_reservation_surfaces_as_Found_pending()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsPending();
        using var client = TestClient.Create(mock);

        var verdict = await client.ReconcileAsync(SyntheticData.MerchantTransactionId, QuickPolicy(1));

        var found = Assert.IsType<FoundVerdict>(verdict);
        Assert.Equal(RapTransactionOutcome.Pending, found.Outcome);
        Assert.False(found.IsTerminal);
        Assert.NotNull(found.Pending);
        Assert.Equal(SyntheticData.MerchantTransactionId, found.Pending!.MerchantTransactionId);
    }

    [Fact]
    public async Task Scripted_not_found_then_found_resolves_on_the_later_attempt()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId)
            .ReturnsNotFoundYet()
            .ReturnsNotFoundYet()
            .ReturnsApproved();
        using var client = TestClient.Create(mock);

        var verdict = await client.ReconcileAsync(SyntheticData.MerchantTransactionId, QuickPolicy(5));

        var found = Assert.IsType<FoundVerdict>(verdict);
        Assert.Equal(RapTransactionOutcome.Approved, found.Outcome);
        Assert.Equal(3, mock.Requests.Count);
    }

    [Fact]
    public async Task Degraded_reads_keep_polling_within_the_budget()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId)
            .Returns500()
            .ReturnsApproved();
        using var client = TestClient.Create(mock);

        var verdict = await client.ReconcileAsync(SyntheticData.MerchantTransactionId, QuickPolicy(3));

        Assert.IsType<FoundVerdict>(verdict);
        Assert.Equal(2, mock.Requests.Count);
    }

    [Fact]
    public async Task Rejected_reads_other_than_404_escape_immediately()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsRejected(401, "bad key");
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<PermanentRejectionException>(
            () => client.ReconcileAsync(SyntheticData.MerchantTransactionId, QuickPolicy(5)));

        Assert.Equal(401, ex.StatusCode);
        Assert.Single(mock.Requests);
    }

    [Fact]
    public async Task Cancellation_stops_polling_immediately()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsNotFoundYet();
        using var client = TestClient.Create(mock);
        using var cts = new CancellationTokenSource();

        var policy = new ReconcilePolicy(1000, TimeSpan.FromMinutes(10), TimeSpan.FromMilliseconds(50));
        var task = client.ReconcileAsync(SyntheticData.MerchantTransactionId, policy, cts.Token);
        cts.CancelAfter(TimeSpan.FromMilliseconds(120));

        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => task);
        Assert.True(mock.Requests.Count < 1000);
    }

    [Fact]
    public async Task The_budget_bounds_total_time_even_with_attempts_remaining()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsNotFoundYet();
        using var client = TestClient.Create(mock);

        var policy = new ReconcilePolicy(
            maxAttempts: 1000, overallBudget: TimeSpan.FromMilliseconds(200), initialDelay: TimeSpan.FromMilliseconds(80));
        var verdict = await client.ReconcileAsync(SyntheticData.MerchantTransactionId, policy);

        var notFound = Assert.IsType<NotFoundYetVerdict>(verdict);
        Assert.True(notFound.Attempts < 1000);
    }

    [Fact]
    public async Task Verdicts_switch_with_a_default_branch_the_quickstart_shape()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsApproved();
        using var client = TestClient.Create(mock);

        var verdict = await client.ReconcileAsync(SyntheticData.MerchantTransactionId, QuickPolicy(1));

        // The verdict hierarchy is open for extension (SafeToFailover arrives with P-2):
        // this is the branch shape every consumer must use — including the default.
        var action = verdict switch
        {
            FoundVerdict { Outcome: RapTransactionOutcome.Approved } => "done",
            FoundVerdict { IsTerminal: true } => "merchant-decision",
            FoundVerdict => "keep-polling",
            NotFoundYetVerdict => "hold-and-escalate",
            _ => "treat-conservatively",
        };

        Assert.Equal("done", action);
    }

    [Fact]
    public void Policy_rejects_unbounded_configurations()
    {
        Assert.Throws<ArgumentOutOfRangeException>(
            () => new ReconcilePolicy(0, TimeSpan.FromSeconds(1), TimeSpan.Zero));
        Assert.Throws<ArgumentOutOfRangeException>(
            () => new ReconcilePolicy(1, TimeSpan.Zero, TimeSpan.Zero));
        Assert.Throws<ArgumentOutOfRangeException>(
            () => new ReconcilePolicy(1, TimeSpan.FromSeconds(1), TimeSpan.FromSeconds(-1)));
    }
}
