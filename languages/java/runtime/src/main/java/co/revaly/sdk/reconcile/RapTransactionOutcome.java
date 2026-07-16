package co.revaly.sdk.reconcile;

/**
 * The terminal-or-pending outcome carried by a {@code Found} reconcile verdict. Mapped from the
 * wire's {@code transactionStatus} (1/2/3) or the pending {@code state} discriminator; anything
 * unrecognized maps to {@link #UNKNOWN} — always branch with a default (runtime-tdd §4: verdicts
 * and outcomes are open for extension).
 */
public enum RapTransactionOutcome {
    /** The payment succeeded at RAP-core. Failing over now would double-charge. */
    APPROVED,

    /** Terminal decline — your own gateway is now safe, per your risk policy (§3). */
    DECLINED,

    /** Terminal error recorded at RAP-core — merchant decision, as with a decline. */
    ERROR,

    /**
     * A pending payment intent (post-P-2 surface): the platform accepted the payment but no
     * transaction record is visible yet. Hold and re-poll.
     */
    PENDING,

    /**
     * Found, but this SDK version cannot map the record (new status value, envelope shape, or
     * post-P-2 variant). A sighting is still a sighting — treat conservatively; do not fail over on
     * UNKNOWN.
     */
    UNKNOWN
}
