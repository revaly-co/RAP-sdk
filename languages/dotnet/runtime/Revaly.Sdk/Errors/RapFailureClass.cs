namespace Revaly.Sdk.Errors;

/// <summary>
/// The three failure classes of the merchant-facing failover contract
/// (docs/failover-contract.md §2). The class determines the safe caller action;
/// it is derived exclusively by the normative classification algorithm — never
/// from error message text, latency, or wait heuristics.
/// </summary>
public enum RapFailureClass
{
    /// <summary>
    /// The platform received and rejected the request (HTTP 400/401/403/404/422).
    /// Fix or decline. Never fail over — the same request fails anywhere.
    /// </summary>
    PermanentRejection,

    /// <summary>
    /// The request definitively did not process: either the transport can prove it
    /// was never sent (connection refused, DNS or TLS failure before the request was
    /// accepted), or the platform proved non-dispatch (503 with code
    /// <c>not_processed</c>). Safe to route to the merchant's own gateway immediately.
    /// </summary>
    TransientFailure,

    /// <summary>
    /// The payment may have been processed (deadline exceeded after send, connection
    /// reset mid-flight, 500, 502/504, bare 503). Reconcile before acting — blind
    /// failover from this state risks a double charge.
    /// </summary>
    OutcomeUnknown,
}
