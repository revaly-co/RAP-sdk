namespace Revaly.Sdk.Logging;

/// <summary>
/// One scrubbed request/response observation delivered to the wire-trace hook
/// (DX contract §c, for Enablement escalations). Scrubbing happens inside the runtime
/// before this record is constructed — the hook consumer never sees raw payloads,
/// and the merchant API key is never present.
/// </summary>
/// <param name="Method">The HTTP method.</param>
/// <param name="Path">The request path (no query string).</param>
/// <param name="RequestHeaders">Scrubbed request headers.</param>
/// <param name="RequestBody">Scrubbed request body (allowlisted fields only).</param>
/// <param name="StatusCode">The response status code, when a response was received.</param>
/// <param name="ResponseHeaders">Scrubbed response headers, when a response was received.</param>
/// <param name="ResponseBody">Scrubbed response body, when one was read.</param>
/// <param name="CorrelationId">The response correlation id, when present.</param>
/// <param name="Elapsed">Wall-clock duration of the exchange.</param>
/// <param name="FailureClass">The typed failure class name when the exchange failed, otherwise null.</param>
public sealed record RapWireTrace(
    string Method,
    string Path,
    IReadOnlyDictionary<string, string> RequestHeaders,
    string RequestBody,
    int? StatusCode,
    IReadOnlyDictionary<string, string>? ResponseHeaders,
    string? ResponseBody,
    string? CorrelationId,
    TimeSpan Elapsed,
    string? FailureClass);
