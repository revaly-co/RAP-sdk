using Microsoft.Extensions.Logging;
using Revaly.Sdk.Errors;
using Revaly.Sdk.Logging;
using Revaly.Sdk.Testing;
using Revaly.Sdk.Tests.TestSupport;

namespace Revaly.Sdk.Tests;

/// <summary>
/// The ADR-SDK-020 CI log-capture obligation: run a charge + a failure + a reconcile
/// against the mock transport at default and debug levels; assert no PAN/CVV/key
/// material in any output, and that correlation ids ARE present (DX contract §c).
/// </summary>
public class LogCaptureTests
{
    private static async Task ExerciseFullFlow(RapClient client)
    {
        await client.Payments.ChargePaymentAsync(TestClient.ChargeRequest());
        await Assert.ThrowsAsync<TransientFailureException>(
            () => client.Payments.ChargePaymentAsync(TestClient.ChargeRequest()));
        await client.ReconcileAsync(
            SyntheticData.MerchantTransactionId,
            new Reconcile.ReconcilePolicy(2, TimeSpan.FromSeconds(10), TimeSpan.FromMilliseconds(1)));
    }

    private static RapMockTransport ScriptedMock()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved().ReturnsNotProcessed503();
        mock.Reconcile(SyntheticData.MerchantTransactionId).ReturnsNotFoundYet().ReturnsApproved();
        return mock;
    }

    private static void AssertNoSensitiveMaterial(string output)
    {
        Assert.DoesNotContain(SyntheticData.TestPan, output, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain(SyntheticData.TestCvv + "\"", output, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain(SyntheticData.TestApiKey, output, StringComparison.OrdinalIgnoreCase);
        Assert.DoesNotContain("ApiKey sk_", output, StringComparison.OrdinalIgnoreCase);
    }

    [Fact]
    public async Task Default_level_output_is_values_free()
    {
        var logs = new CapturingLoggerFactory(LogLevel.Information);
        using (var client = TestClient.Create(ScriptedMock(), loggerFactory: logs))
        {
            await ExerciseFullFlow(client);
        }

        var output = logs.AllOutput;
        Assert.NotEmpty(logs.Lines);
        AssertNoSensitiveMaterial(output);
        // No payload values at default verbosity, ever: the synthetic amount must not appear.
        Assert.DoesNotContain("1999", output, StringComparison.Ordinal);
        // Correlation ids ARE present — support tickets join RAP-core telemetry directly.
        Assert.Contains(SyntheticData.CorrelationId, output, StringComparison.Ordinal);
    }

    [Fact]
    public async Task Debug_level_output_is_fully_scrubbed()
    {
        var logs = new CapturingLoggerFactory(LogLevel.Debug);
        using (var client = TestClient.Create(ScriptedMock(), loggerFactory: logs))
        {
            await ExerciseFullFlow(client);
        }

        var output = logs.AllOutput;
        AssertNoSensitiveMaterial(output);
        Assert.Contains(Logging.RapScrubber.Scrubbed, output, StringComparison.Ordinal);
        // Allowlisted identifiers survive scrubbing — that is the point of debug output.
        Assert.Contains(SyntheticData.MerchantTransactionId, output, StringComparison.Ordinal);
    }

    [Fact]
    public async Task Wire_trace_hook_receives_only_scrubbed_material()
    {
        var traces = new List<RapWireTrace>();
        using (var client = TestClient.Create(ScriptedMock(), wireTraceHook: traces.Add))
        {
            await ExerciseFullFlow(client);
        }

        Assert.NotEmpty(traces);
        foreach (var trace in traces)
        {
            var flattened = trace.RequestBody + trace.ResponseBody
                + string.Join(";", trace.RequestHeaders.Select(h => $"{h.Key}={h.Value}"))
                + string.Join(";", (trace.ResponseHeaders ?? new Dictionary<string, string>()).Select(h => $"{h.Key}={h.Value}"));
            AssertNoSensitiveMaterial(flattened);
        }

        // The failed charge's trace carries the failure class and correlation id.
        Assert.Contains(traces, t => t.FailureClass == nameof(RapFailureClass.TransientFailure));
        Assert.Contains(traces, t => t.CorrelationId == SyntheticData.CorrelationId);
    }

    [Fact]
    public async Task Hook_exceptions_never_affect_the_payment_path()
    {
        var mock = new RapMockTransport();
        mock.Charge().ReturnsApproved();
        using var client = TestClient.Create(mock, wireTraceHook: _ => throw new InvalidOperationException("observer bug"));

        var response = await client.Payments.ChargePaymentAsync(TestClient.ChargeRequest());

        Assert.True(response.TryOk(out _));
    }
}
