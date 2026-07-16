using Revaly.Sdk.Errors;
using Revaly.Sdk.Testing;
using Revaly.Sdk.Tests.TestSupport;

namespace Revaly.Sdk.Tests;

/// <summary>
/// Table-driven coverage of every row of the failover-contract §2 classification table,
/// exercised end-to-end through the real client + handler chain over the mock transport.
/// </summary>
public class ClassificationTests
{
    [Theory]
    [InlineData(400)]
    [InlineData(401)]
    [InlineData(403)]
    [InlineData(404)]
    [InlineData(422)]
    public async Task Received_and_rejected_statuses_are_PermanentRejection(int status)
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsRejected(status);
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<PermanentRejectionException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Equal(status, ex.StatusCode);
        Assert.Equal(RapFailureClass.PermanentRejection, ex.Class);
        Assert.Equal(SyntheticData.CorrelationId, ex.CorrelationId);
    }

    [Fact]
    public async Task Not_processed_503_is_TransientFailure_safe_to_fail_over()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsNotProcessed503();
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<TransientFailureException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Equal(503, ex.StatusCode);
        Assert.Equal("not_processed", ex.Code);
    }

    [Fact]
    public async Task Connection_refused_is_TransientFailure_provably_never_sent()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsConnectionRefused();
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<TransientFailureException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Null(ex.StatusCode);
    }

    [Fact]
    public async Task Dns_failure_is_TransientFailure()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsDnsFailure();
        using var client = TestClient.Create(mock);

        await Assert.ThrowsAsync<TransientFailureException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));
    }

    [Fact]
    public async Task Tls_failure_is_TransientFailure()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsTlsFailure();
        using var client = TestClient.Create(mock);

        await Assert.ThrowsAsync<TransientFailureException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));
    }

    [Fact]
    public async Task Bare_503_without_not_processed_is_OutcomeUnknown()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsBare503();
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<OutcomeUnknownException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Equal(503, ex.StatusCode);
    }

    [Fact]
    public async Task Outcome_unknown_503_is_OutcomeUnknown()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsOutcomeUnknown503();
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<OutcomeUnknownException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Equal("outcome_unknown", ex.Code);
    }

    [Theory]
    [InlineData(500)]
    [InlineData(502)]
    [InlineData(504)]
    public async Task Server_and_edge_5xx_are_OutcomeUnknown(int status)
    {
        var mock = new RapMockTransport();
        switch (status)
        {
            case 500: mock.Charge().Returns500(); break;
            case 502: mock.Charge().Returns502(); break;
            default: mock.Charge().Returns504(); break;
        }

        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<OutcomeUnknownException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Equal(status, ex.StatusCode);
    }

    [Fact]
    public async Task Deadline_expiry_after_send_is_OutcomeUnknown_never_TransientFailure()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsTimeoutAfterSend();
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<OutcomeUnknownException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Equal(RapFailureClass.OutcomeUnknown, ex.Class);
    }

    [Fact]
    public async Task Reset_mid_flight_is_OutcomeUnknown()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsResetMidFlight();
        using var client = TestClient.Create(mock);

        await Assert.ThrowsAsync<OutcomeUnknownException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));
    }

    [Fact]
    public async Task Unrecognized_code_values_are_treated_as_absent_and_stay_OutcomeUnknown()
    {
        var mock = new RapMockTransport();
        mock.Charge().Returns(
            System.Net.HttpStatusCode.ServiceUnavailable,
            "{\"error\":\"synthetic\",\"code\":\"some_future_oq2_code\"}");
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<OutcomeUnknownException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.Equal("some_future_oq2_code", ex.Code);
    }

    [Fact]
    public async Task Api_version_20_narrows_fast_failover_to_never_sent_only()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsNotProcessed503();
        using var client = TestClient.Create(mock, apiVersion: "2.0");

        // On the 2.0 pin, ErrorResponse.code is not part of the documented contract:
        // 503 + not_processed classifies OutcomeUnknown, not TransientFailure.
        await Assert.ThrowsAsync<OutcomeUnknownException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));
    }

    [Fact]
    public async Task Caller_cancellation_is_idiomatic_cancellation_not_a_failure_class()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock);
        using var cts = new CancellationTokenSource();
        cts.Cancel();

        await Assert.ThrowsAnyAsync<OperationCanceledException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest(), cancellationToken: cts.Token));
    }

    [Fact]
    public async Task Successful_charge_returns_the_transaction()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock);

        var response = await client.Payments.ChargePaymentAsync(TestClient.ChargeRequest());

        Assert.True(response.TryOk(out var transaction));
        Assert.Equal(SyntheticData.TransactionId, transaction!.TransactionId);
        Assert.Equal(1, transaction.TransactionStatus);
    }

    [Fact]
    public async Task Typed_errors_never_carry_the_api_key_or_pan_in_their_message()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsRejected(422);
        using var client = TestClient.Create(mock);

        var ex = await Assert.ThrowsAsync<PermanentRejectionException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));

        Assert.DoesNotContain(SyntheticData.TestApiKey, ex.ToString(), StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain(SyntheticData.TestPan, ex.ToString(), StringComparison.OrdinalIgnoreCase);
    }
}
