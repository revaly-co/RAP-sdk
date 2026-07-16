using System.Text.Json;

namespace Revaly.Sdk.Errors;

/// <summary>
/// The payment <b>may have been processed</b> (deadline exceeded after send,
/// connection reset mid-flight, 500, 502/504, bare 503). Reconcile before acting
/// (<c>RapClient.ReconcileAsync</c>) — blind failover from this state risks
/// charging the cardholder twice (failover-contract §1/§3).
/// </summary>
public sealed class OutcomeUnknownException : RapCoreException
{
    /// <summary>Creates an outcome-unknown failure (constructed by the SDK and by test doubles).</summary>
    public OutcomeUnknownException(
        int? statusCode = null,
        string? code = null,
        string? errorMessage = null,
        JsonElement? details = null,
        string? correlationId = null,
        string? rawErrorBody = null,
        Exception? innerException = null)
        : base(
            RapFailureClass.OutcomeUnknown,
            BuildMessage(RapFailureClass.OutcomeUnknown, statusCode, code, correlationId,
                errorMessage ?? "outcome unknown; reconcile before acting — do not blind-fail-over"),
            statusCode, code, errorMessage, details, correlationId, rawErrorBody, innerException)
    {
    }
}
