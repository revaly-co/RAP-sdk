using System.Text.Json;

namespace Revaly.Sdk.Errors;

/// <summary>
/// The request definitively did not process — safe to fail over to the merchant's
/// own gateway immediately (failover-contract §2). Raised only on client-provable
/// never-sent transport failures, on 503 with <c>code: not_processed</c>, or on a 403
/// blocked at the edge firewall (<see cref="RapCoreException.IsEdgeRejection"/>,
/// ADR-SDK-033).
/// </summary>
public sealed class TransientFailureException : RapCoreException
{
    /// <summary>Creates a transient failure (constructed by the SDK and by test doubles).</summary>
    public TransientFailureException(
        int? statusCode = null,
        string? code = null,
        string? errorMessage = null,
        JsonElement? details = null,
        string? correlationId = null,
        string? rawErrorBody = null,
        Exception? innerException = null,
        bool isEdgeRejection = false,
        string? edgeReference = null)
        : base(
            RapFailureClass.TransientFailure,
            BuildMessage(RapFailureClass.TransientFailure, statusCode, code, correlationId,
                errorMessage ?? (isEdgeRejection
                    ? "blocked at the edge firewall; request never reached the platform — safe to fail over"
                    : "request definitively not processed; safe to fail over")),
            statusCode, code, errorMessage, details, correlationId, rawErrorBody, innerException,
            isEdgeRejection, edgeReference)
    {
    }
}
