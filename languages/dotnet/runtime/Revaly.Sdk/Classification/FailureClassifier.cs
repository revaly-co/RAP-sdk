using System.Text.Json;
using Revaly.Sdk.Errors;

namespace Revaly.Sdk.Classification;

/// <summary>
/// The normative failure-classification algorithm of failover-contract.md §2.
/// Every rule here is contract, not heuristic:
/// <code>
/// if transport error and request provably never sent          → TransientFailure
/// if HTTP status in {400, 401, 403, 404, 422}                 → PermanentRejection
/// if HTTP status == 503 and body.code == "not_processed"      → TransientFailure
/// if HTTP status >= 500                                        → OutcomeUnknown
/// if deadline exceeded after send / reset / ambiguous          → OutcomeUnknown
/// </code>
/// Never classify from <c>error</c> message text; treat <c>details</c> as opaque;
/// unrecognized <c>code</c> values are treated as absent; when the stack cannot prove
/// the request was never sent, classify OutcomeUnknown — never guess toward "safe".
/// </summary>
internal static class FailureClassifier
{
    private const string NotProcessed = "not_processed";

    /// <summary>
    /// Classifies a transport-level failure. Provably-never-sent detection uses the
    /// transport's own connect-vs-response phase semantics (<see cref="HttpRequestError"/>):
    /// name resolution, connection establishment, and TLS handshake failures all occur
    /// before the request was accepted, so they are <see cref="TransientFailureException"/>.
    /// Every other transport failure is ambiguous → <see cref="OutcomeUnknownException"/>.
    /// </summary>
    internal static RapCoreException ClassifyTransportFailure(HttpRequestException exception)
    {
        return exception.HttpRequestError switch
        {
            HttpRequestError.NameResolutionError or
            HttpRequestError.ConnectionError or
            HttpRequestError.SecureConnectionError =>
                new TransientFailureException(
                    errorMessage: $"request provably never sent ({exception.HttpRequestError})",
                    innerException: exception),
            _ => new OutcomeUnknownException(
                    errorMessage: $"transport failure without never-sent proof ({exception.HttpRequestError})",
                    innerException: exception),
        };
    }

    /// <summary>
    /// Classifies expiry of the overall deadline (or the underlying HttpClient timeout).
    /// Expiry after send is OutcomeUnknown by contract — never TransientFailure
    /// (runtime-tdd §1); since the timer cannot prove the request was never sent,
    /// the ambiguous case lands on the same conservative answer.
    /// </summary>
    internal static RapCoreException ClassifyDeadlineExpiry(OperationCanceledException exception)
    {
        return new OutcomeUnknownException(
            errorMessage: "deadline exceeded after send; reconcile before acting",
            innerException: exception);
    }

    /// <summary>
    /// Classifies a received non-success HTTP response. Returns the typed failure, or
    /// null for statuses that are not failures of the payment contract (2xx handled by
    /// the caller). Statuses outside the §2 table (e.g. 409, 3xx) are ambiguous and
    /// classify as OutcomeUnknown — reconcile reveals the true state.
    /// </summary>
    /// <param name="statusCode">The received HTTP status code.</param>
    /// <param name="rawBody">The raw response body (may be null/empty).</param>
    /// <param name="apiVersion">
    /// The pinned <c>X-Api-Version</c>. On <c>"2.0"</c> the <c>ErrorResponse.code</c>
    /// field is not part of the documented contract, so the fast-failover class narrows
    /// to client-provable never-sent failures only: 503 + <c>not_processed</c> is NOT
    /// honored and falls through to OutcomeUnknown (runtime-tdd §1 [Decided]).
    /// </param>
    /// <param name="correlationId">The response correlation id, if present.</param>
    internal static RapCoreException ClassifyResponse(
        int statusCode, string? rawBody, string apiVersion, string? correlationId)
    {
        var (code, error, details) = ParseErrorBody(rawBody);

        if (statusCode is 400 or 401 or 403 or 404 or 422)
        {
            return new PermanentRejectionException(statusCode, code, error, details, correlationId, rawBody);
        }

        if (statusCode == 503
            && string.Equals(code, NotProcessed, StringComparison.Ordinal)
            && !string.Equals(apiVersion, "2.0", StringComparison.Ordinal))
        {
            return new TransientFailureException(statusCode, code, error, details, correlationId, rawBody);
        }

        if (statusCode >= 500)
        {
            return new OutcomeUnknownException(statusCode, code, error, details, correlationId, rawBody);
        }

        return new OutcomeUnknownException(statusCode, code, error, details, correlationId, rawBody);
    }

    /// <summary>
    /// Parses <c>code</c>, <c>error</c>, and <c>details</c> from the raw error body.
    /// <c>code</c> is read as an OPEN STRING from the wire — deliberately not via the
    /// generated core's <c>ErrorResponse.CodeEnum</c> (ADR-SDK-023 uniform safety rule;
    /// repo rule 5): new values arrive with OQ-2 and must never break classification.
    /// Anything unparseable is treated as absent (→ the conservative branch).
    /// </summary>
    internal static (string? Code, string? Error, JsonElement? Details) ParseErrorBody(string? rawBody)
    {
        if (string.IsNullOrWhiteSpace(rawBody))
        {
            return (null, null, null);
        }

        try
        {
            using var document = JsonDocument.Parse(rawBody);
            if (document.RootElement.ValueKind != JsonValueKind.Object)
            {
                return (null, null, null);
            }

            string? code = null;
            if (document.RootElement.TryGetProperty("code", out var codeElement)
                && codeElement.ValueKind == JsonValueKind.String)
            {
                code = codeElement.GetString();
            }

            string? error = null;
            if (document.RootElement.TryGetProperty("error", out var errorElement)
                && errorElement.ValueKind == JsonValueKind.String)
            {
                error = errorElement.GetString();
            }

            JsonElement? details = null;
            if (document.RootElement.TryGetProperty("details", out var detailsElement))
            {
                details = detailsElement.Clone();
            }

            return (code, error, details);
        }
        catch (JsonException)
        {
            return (null, null, null);
        }
    }
}
