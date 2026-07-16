using System.Text.Json;

namespace Revaly.Sdk.Errors;

/// <summary>
/// The platform received and rejected the request (HTTP 400/401/403/404/422).
/// Fix the request or decline the payment. <b>Never fail over</b> — the same
/// request fails at any gateway (failover-contract §2).
/// </summary>
public sealed class PermanentRejectionException : RapCoreException
{
    /// <summary>Creates a permanent-rejection failure (constructed by the SDK and by test doubles).</summary>
    public PermanentRejectionException(
        int statusCode,
        string? code = null,
        string? errorMessage = null,
        JsonElement? details = null,
        string? correlationId = null,
        string? rawErrorBody = null,
        Exception? innerException = null)
        : base(
            RapFailureClass.PermanentRejection,
            BuildMessage(RapFailureClass.PermanentRejection, statusCode, code, correlationId,
                errorMessage ?? "request rejected by the platform; fix or decline — do not fail over"),
            statusCode, code, errorMessage, details, correlationId, rawErrorBody, innerException)
    {
    }
}
