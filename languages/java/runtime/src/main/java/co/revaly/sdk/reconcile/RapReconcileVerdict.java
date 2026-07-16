package co.revaly.sdk.reconcile;

import co.revaly.sdk.core.model.PendingTransactionResponse;
import co.revaly.sdk.core.model.TransactionResponse;
import java.time.Duration;

/**
 * The reconcile helper's verdict (failover-contract §3; ADR-SDK-009). V1 deliberately has only two
 * concrete verdicts — {@link Found} and {@link NotFoundYet}; there is NO SafeToFailover in V1 ("not
 * found" means <i>not yet visible</i>, never "doesn't exist"). {@code SafeToFailover} arrives with
 * platform P-2 as a minor release.
 *
 * <p><b>The verdict hierarchy is designed open for extension</b> (runtime-tdd §4): the constructor
 * is package-private so new verdicts can arrive in minor releases, and every merchant branch MUST
 * carry a default:
 *
 * <pre>{@code
 * if (verdict instanceof RapReconcileVerdict.Found) {
 *     ...
 * } else if (verdict instanceof RapReconcileVerdict.NotFoundYet) {
 *     ...
 * } else {
 *     // Default branch — REQUIRED: future SDK minors add verdicts (e.g. SafeToFailover).
 *     escalatePerMerchantPolicy(verdict);
 * }
 * }</pre>
 */
public abstract class RapReconcileVerdict {

    private final String correlationId;

    RapReconcileVerdict(String correlationId) {
        this.correlationId = correlationId;
    }

    /**
     * The last observed {@code X-Correlation-ID}, if any response was received. Quote it in support
     * tickets (DX contract §c).
     */
    public String getCorrelationId() {
        return correlationId;
    }

    /** A transaction (or pending intent) with this merchantTransactionId is visible. */
    public static final class Found extends RapReconcileVerdict {

        private final RapTransactionOutcome outcome;
        private final TransactionResponse transaction;
        private final PendingTransactionResponse pending;

        Found(
                RapTransactionOutcome outcome,
                TransactionResponse transaction,
                PendingTransactionResponse pending,
                String correlationId) {
            super(correlationId);
            this.outcome = outcome;
            this.transaction = transaction;
            this.pending = pending;
        }

        /** The mapped outcome — always branch with a default for {@code UNKNOWN}. */
        public RapTransactionOutcome getOutcome() {
            return outcome;
        }

        /** The terminal transaction record, when the record mapped to one; else null. */
        public TransactionResponse getTransaction() {
            return transaction;
        }

        /** The pending intent record (outcome {@code PENDING}); else null. */
        public PendingTransactionResponse getPending() {
            return pending;
        }
    }

    /**
     * No record is visible yet. This is NOT proof of absence (platform visibility is asynchronous
     * and unbounded — widest exactly when RAP-core is degraded): hold and re-poll with backoff; on
     * sustained NotFoundYet, escalate per merchant policy. If a merchant chooses to fail over
     * anyway, that decision lives in their code against their risk policy — this SDK does not bless
     * it (failover-contract §3).
     */
    public static final class NotFoundYet extends RapReconcileVerdict {

        private final int attempts;
        private final Duration elapsed;
        private final Integer lastHttpStatus;

        NotFoundYet(
                int attempts, Duration elapsed, String lastCorrelationId, Integer lastHttpStatus) {
            super(lastCorrelationId);
            this.attempts = attempts;
            this.elapsed = elapsed;
            this.lastHttpStatus = lastHttpStatus;
        }

        /** GET attempts performed within the policy bounds. */
        public int getAttempts() {
            return attempts;
        }

        /** Wall-clock time spent polling. */
        public Duration getElapsed() {
            return elapsed;
        }

        /** The last HTTP status observed, if any response was received. */
        public Integer getLastHttpStatus() {
            return lastHttpStatus;
        }
    }
}
