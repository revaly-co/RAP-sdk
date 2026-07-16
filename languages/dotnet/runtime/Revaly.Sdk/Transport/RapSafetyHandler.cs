using Revaly.Sdk.Classification;
using Revaly.Sdk.Errors;

namespace Revaly.Sdk.Transport;

/// <summary>
/// The safety-contract enforcement point. Sits innermost in the handler chain (directly
/// over the wire transport) so that classification cannot be bypassed through the core
/// surface: every transport failure, deadline expiry, and non-success response is turned
/// into the typed failure of failover-contract §2 before the generated core ever sees it.
/// Single-shot semantics — this handler never retries anything (ADR-SDK-004).
/// </summary>
internal sealed class RapSafetyHandler : DelegatingHandler
{
    // Error bodies are small ({error, code, details}); cap the read defensively so a
    // misbehaving intermediary cannot balloon exception payloads.
    private const int MaxErrorBodyBytes = 64 * 1024;

    private readonly TimeSpan? _overallDeadline;
    private readonly string _apiVersion;

    internal RapSafetyHandler(TimeSpan? overallDeadline, string apiVersion)
    {
        _overallDeadline = overallDeadline;
        _apiVersion = apiVersion;
    }

    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        using var deadlineSource = _overallDeadline is { } deadline
            ? CancellationTokenSource.CreateLinkedTokenSource(cancellationToken)
            : null;
        deadlineSource?.CancelAfter(_overallDeadline!.Value);
        var effectiveToken = deadlineSource?.Token ?? cancellationToken;

        HttpResponseMessage response;
        try
        {
            response = await base.SendAsync(request, effectiveToken).ConfigureAwait(false);
        }
        catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
        {
            // The caller cancelled: idiomatic .NET cancellation, not a failure class.
            throw;
        }
        catch (OperationCanceledException oce)
        {
            // Overall deadline (or HttpClient.Timeout) expired. The timer cannot prove
            // the request was never sent → OutcomeUnknown, never TransientFailure.
            throw FailureClassifier.ClassifyDeadlineExpiry(oce);
        }
        catch (HttpRequestException hre)
        {
            // Connect-phase failures carry never-sent proof; everything else is ambiguous.
            throw FailureClassifier.ClassifyTransportFailure(hre);
        }

        if (response.IsSuccessStatusCode)
        {
            return response;
        }

        string? rawBody = null;
        try
        {
            rawBody = await ReadErrorBodyAsync(response, effectiveToken).ConfigureAwait(false);
        }
        catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
        {
            throw;
        }
        catch (Exception)
        {
            // A response line was received but the body could not be read (reset
            // mid-flight, deadline during body read). Ambiguous → classified below
            // with whatever we know: the status line and no body.
        }

        var correlationId = response.Headers.TryGetValues(RapHeaders.CorrelationId, out var values)
            ? values.FirstOrDefault()
            : null;
        var statusCode = (int)response.StatusCode;
        response.Dispose();

        throw FailureClassifier.ClassifyResponse(statusCode, rawBody, _apiVersion, correlationId);
    }

    private static async Task<string?> ReadErrorBodyAsync(
        HttpResponseMessage response, CancellationToken cancellationToken)
    {
        await response.Content.LoadIntoBufferAsync(MaxErrorBodyBytes, cancellationToken).ConfigureAwait(false);
        return await response.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);
    }
}
