using Revaly.Sdk.Errors;
using Revaly.Sdk.Testing;
using Revaly.Sdk.Tests.TestSupport;

namespace Revaly.Sdk.Tests;

/// <summary>
/// ADR-SDK-004: no hidden retries anywhere — single-shot semantics except the explicit,
/// caller-bounded reconcile loop. One call = exactly one wire request, on every path.
/// </summary>
public class NoRetryTests
{
    [Fact]
    public async Task A_successful_charge_sends_exactly_one_request()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock);

        await client.Payments.ChargePaymentAsync(TestClient.ChargeRequest());

        Assert.Single(mock.Requests);
    }

    [Fact]
    public async Task An_OutcomeUnknown_500_is_never_retried()
    {
        var mock = new RapMockTransport();
        mock.Charge().Returns500();
        using var client = TestClient.Create(mock);

        await Assert.ThrowsAsync<OutcomeUnknownException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Single(mock.Requests);
    }

    [Fact]
    public async Task A_TransientFailure_is_never_retried_failover_is_the_callers_move()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsNotProcessed503();
        using var client = TestClient.Create(mock);

        await Assert.ThrowsAsync<TransientFailureException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Single(mock.Requests);
    }

    [Fact]
    public async Task Reconcile_with_a_single_attempt_policy_sends_exactly_one_request()
    {
        var mock = new RapMockTransport();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsNotFoundYet();
        using var client = TestClient.Create(mock);

        await client.ReconcileAsync(
            SyntheticData.MerchantTransactionId,
            new Reconcile.ReconcilePolicy(1, TimeSpan.FromSeconds(5), TimeSpan.Zero));

        Assert.Single(mock.Requests);
    }
}
