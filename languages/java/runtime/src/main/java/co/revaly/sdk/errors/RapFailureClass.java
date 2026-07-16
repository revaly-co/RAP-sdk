package co.revaly.sdk.errors;

/**
 * The three typed failure classes of the RAP failover contract (docs/failover-contract.md §2). The
 * class — never the message text, latency, or wait heuristics — is what licenses a failover
 * decision.
 */
public enum RapFailureClass {
    /**
     * The request was received and rejected (400/401/403/404/422). Fix or decline — never fail
     * over: the same request fails anywhere.
     */
    PERMANENT_REJECTION,

    /**
     * The payment was definitively not processed (client-provable never-sent, or 503 with {@code
     * code: not_processed}). Safe to route to your own gateway immediately.
     */
    TRANSIENT_FAILURE,

    /**
     * The payment may have been processed (deadline after send, 5xx, ambiguous transport failure).
     * Reconcile before acting — failing over blind risks a double charge.
     */
    OUTCOME_UNKNOWN
}
