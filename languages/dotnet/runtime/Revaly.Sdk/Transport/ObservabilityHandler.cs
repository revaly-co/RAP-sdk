using System.Diagnostics;
using Microsoft.Extensions.Logging;
using Revaly.Sdk.Errors;
using Revaly.Sdk.Logging;

namespace Revaly.Sdk.Transport;

/// <summary>
/// Values-free logging and the wire-trace hook (runtime-tdd §6, ADR-SDK-020).
/// Sits outermost in the handler chain so it observes the final outcome of every
/// exchange, including typed failures raised by the safety handler.
/// Default (Information) output carries no payload values — method, path, status,
/// failure class, correlation id and elapsed time only. Debug adds payloads scrubbed
/// by the central allowlist scrubber. The hook receives scrubbed material only, and
/// hook exceptions are swallowed: an observer must never affect the payment path.
/// </summary>
internal sealed class ObservabilityHandler : DelegatingHandler
{
    private readonly ILogger _logger;
    private readonly Action<RapWireTrace>? _wireTraceHook;

    internal ObservabilityHandler(ILogger logger, Action<RapWireTrace>? wireTraceHook)
    {
        _logger = logger;
        _wireTraceHook = wireTraceHook;
    }

    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        var wantsPayloads = _wireTraceHook is not null || _logger.IsEnabled(LogLevel.Debug);
        var method = request.Method.Method;
        var path = request.RequestUri?.AbsolutePath ?? "-";

        string requestBody = string.Empty;
        if (wantsPayloads && request.Content is not null)
        {
            var raw = await request.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
            requestBody = RapScrubber.ScrubJson(raw);
        }

        var stopwatch = Stopwatch.StartNew();
        try
        {
            var response = await base.SendAsync(request, cancellationToken).ConfigureAwait(false);
            stopwatch.Stop();

            var correlationId = response.Headers.TryGetValues(RapHeaders.CorrelationId, out var values)
                ? values.FirstOrDefault()
                : null;
            var status = (int)response.StatusCode;

            _logger.LogInformation(
                "RAP {Method} {Path} -> {StatusCode} correlation={CorrelationId} elapsed={ElapsedMs}ms",
                method, path, status, correlationId ?? "-", stopwatch.ElapsedMilliseconds);

            string? responseBody = null;
            if (wantsPayloads)
            {
                var raw = await response.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
                responseBody = RapScrubber.ScrubJson(raw);
                _logger.LogDebug(
                    "RAP {Method} {Path} scrubbed request={RequestBody} response={ResponseBody}",
                    method, path, requestBody, responseBody);
            }

            EmitTrace(new RapWireTrace(
                method, path,
                RapScrubber.ScrubHeaders(request.Headers), requestBody,
                status, RapScrubber.ScrubHeaders(response.Headers), responseBody,
                correlationId, stopwatch.Elapsed, FailureClass: null));

            return response;
        }
        catch (RapCoreException ex)
        {
            stopwatch.Stop();
            _logger.LogWarning(
                "RAP {Method} {Path} -> {StatusCode} class={FailureClass} code={Code} correlation={CorrelationId} elapsed={ElapsedMs}ms",
                method, path, ex.StatusCode?.ToString(System.Globalization.CultureInfo.InvariantCulture) ?? "-",
                ex.Class, ex.Code ?? "-", ex.CorrelationId ?? "-", stopwatch.ElapsedMilliseconds);

            string? responseBody = null;
            if (wantsPayloads && ex.RawErrorBody is not null)
            {
                responseBody = RapScrubber.ScrubJson(ex.RawErrorBody);
                _logger.LogDebug(
                    "RAP {Method} {Path} scrubbed request={RequestBody} errorResponse={ResponseBody}",
                    method, path, requestBody, responseBody);
            }

            EmitTrace(new RapWireTrace(
                method, path,
                RapScrubber.ScrubHeaders(request.Headers), requestBody,
                ex.StatusCode, ResponseHeaders: null, responseBody,
                ex.CorrelationId, stopwatch.Elapsed, ex.Class.ToString()));

            throw;
        }
        catch (OperationCanceledException)
        {
            stopwatch.Stop();
            _logger.LogInformation(
                "RAP {Method} {Path} cancelled by caller after {ElapsedMs}ms", method, path, stopwatch.ElapsedMilliseconds);
            throw;
        }
    }

    private void EmitTrace(RapWireTrace trace)
    {
        if (_wireTraceHook is null)
        {
            return;
        }

        try
        {
            _wireTraceHook(trace);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "RAP wire-trace hook threw; observer errors are ignored");
        }
    }
}
