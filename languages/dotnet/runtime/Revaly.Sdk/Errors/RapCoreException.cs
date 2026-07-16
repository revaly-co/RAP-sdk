using System.Text.Json;

namespace Revaly.Sdk.Errors;

/// <summary>
/// Base type for the three typed failure classes of the RAP failover contract
/// (docs/failover-contract.md §2; runtime-tdd.md §3). Catch the subclasses —
/// <see cref="PermanentRejectionException"/>, <see cref="TransientFailureException"/>,
/// <see cref="OutcomeUnknownException"/> — to branch failover logic.
/// </summary>
/// <remarks>
/// The exception <see cref="Exception.Message"/> is values-free by construction
/// (class, HTTP status, code, correlation id only — ADR-SDK-020): it never embeds
/// request payloads, API keys, or the raw response body. The raw error body remains
/// available on <see cref="RawErrorBody"/> for programmatic use.
/// </remarks>
public abstract class RapCoreException : Exception
{
    private protected RapCoreException(
        RapFailureClass failureClass,
        string message,
        int? statusCode,
        string? code,
        string? errorMessage,
        JsonElement? details,
        string? correlationId,
        string? rawErrorBody,
        Exception? innerException)
        : base(message, innerException)
    {
        Class = failureClass;
        StatusCode = statusCode;
        Code = code;
        ErrorMessage = errorMessage;
        Details = details;
        CorrelationId = correlationId;
        RawErrorBody = rawErrorBody;
    }

    /// <summary>The failure class assigned by the normative classification algorithm.</summary>
    public RapFailureClass Class { get; }

    /// <summary>The HTTP status code, when a response was received; otherwise null.</summary>
    public int? StatusCode { get; }

    /// <summary>
    /// The <c>ErrorResponse.code</c> machine-readable safety signal, verbatim from the
    /// wire, when present. This is an open string: values beyond today's
    /// <c>not_processed</c> / <c>outcome_unknown</c> arrive with OQ-2 (the full
    /// error-code taxonomy) and unrecognized values are treated as absent for
    /// classification. Never a closed enum (repo rule 5).
    /// </summary>
    public string? Code { get; }

    /// <summary>The human-readable <c>error</c> message from the response body, if any.</summary>
    public string? ErrorMessage { get; }

    /// <summary>
    /// The opaque <c>details</c> member of the error body, if any. The SDK never
    /// interprets it (failover-contract §2) and it may contain merchant payload echoes —
    /// treat as sensitive when logging (it is excluded from <see cref="Exception.Message"/>).
    /// </summary>
    public JsonElement? Details { get; }

    /// <summary>
    /// The request correlation id (<c>X-Correlation-ID</c> response header), when a
    /// response was received. Quote it in support tickets — it joins directly to
    /// RAP-core telemetry (DX contract §c).
    /// </summary>
    public string? CorrelationId { get; }

    /// <summary>
    /// The raw error response body, when one was received. Kept out of
    /// <see cref="Exception.Message"/> and <c>ToString()</c>; scrub before logging
    /// (see <c>RapScrubber</c>).
    /// </summary>
    public string? RawErrorBody { get; }

    private protected static string BuildMessage(
        RapFailureClass failureClass, int? statusCode, string? code, string? correlationId, string detail)
    {
        var status = statusCode is null ? "-" : statusCode.Value.ToString(System.Globalization.CultureInfo.InvariantCulture);
        return $"RAP request failed [class={failureClass} status={status} code={code ?? "-"} correlation={correlationId ?? "-"}]: {detail}";
    }
}
