package co.revaly.sdk.reconcile;

import java.time.Duration;
import java.util.concurrent.ThreadLocalRandom;

/**
 * The caller-bounded polling policy for {@code RapClient.reconcile} — the ONLY loop this SDK owns
 * (ADR-SDK-004). All bounds are explicit constructor arguments: the SDK ships no default attempt
 * counts, budgets, or delays until the OQ-6 telemetry-derived recommendations land
 * (docs/open-items.md — deliberately not invented here). The backoff shape is exponential with
 * jitter ([Proposed]: multiplier 2.0, full jitter ±20%).
 */
public final class ReconcilePolicy {

    private static final double MULTIPLIER = 2.0;
    private static final double JITTER_RATIO = 0.2;

    private final int maxAttempts;
    private final Duration overallBudget;
    private final Duration initialDelay;
    private final Duration maxDelay;

    /**
     * Creates a polling policy without a per-wait delay cap.
     *
     * @see #ReconcilePolicy(int, Duration, Duration, Duration)
     */
    public ReconcilePolicy(int maxAttempts, Duration overallBudget, Duration initialDelay) {
        this(maxAttempts, overallBudget, initialDelay, null);
    }

    /**
     * Creates a polling policy. Choose bounds per your risk policy: reconciliation is how an
     * OutcomeUnknown payment is resolved, so the budget bounds how long your checkout holds before
     * escalating.
     *
     * @param maxAttempts maximum GET attempts (≥ 1)
     * @param overallBudget total wall-clock budget across all attempts and waits
     * @param initialDelay delay before the second attempt; doubles each attempt (with jitter)
     * @param maxDelay optional cap on the per-wait delay; null leaves growth uncapped within the
     *     budget
     */
    public ReconcilePolicy(
            int maxAttempts, Duration overallBudget, Duration initialDelay, Duration maxDelay) {
        if (maxAttempts < 1) {
            throw new IllegalArgumentException("maxAttempts: at least one attempt is required");
        }
        if (overallBudget == null || overallBudget.isZero() || overallBudget.isNegative()) {
            throw new IllegalArgumentException(
                    "overallBudget: the overall budget must be positive");
        }
        if (initialDelay == null || initialDelay.isNegative()) {
            throw new IllegalArgumentException(
                    "initialDelay: the initial delay cannot be negative");
        }
        this.maxAttempts = maxAttempts;
        this.overallBudget = overallBudget;
        this.initialDelay = initialDelay;
        this.maxDelay = maxDelay;
    }

    /** Maximum GET attempts. */
    public int getMaxAttempts() {
        return maxAttempts;
    }

    /** Total wall-clock budget across all attempts and waits. */
    public Duration getOverallBudget() {
        return overallBudget;
    }

    /** Delay before the second attempt (exponential growth afterwards). */
    public Duration getInitialDelay() {
        return initialDelay;
    }

    /** Optional cap on the per-wait delay; null when uncapped. */
    public Duration getMaxDelay() {
        return maxDelay;
    }

    Duration delayForAttempt(int completedAttempts) {
        if (initialDelay.isZero()) {
            return Duration.ZERO;
        }

        double raw = initialDelay.toMillis() * Math.pow(MULTIPLIER, completedAttempts - 1);
        if (maxDelay != null && raw > maxDelay.toMillis()) {
            raw = maxDelay.toMillis();
        }

        double jitterSpan = raw * JITTER_RATIO;
        double jittered =
                raw + ((ThreadLocalRandom.current().nextDouble() * 2.0) - 1.0) * jitterSpan;
        return Duration.ofMillis((long) Math.max(0, jittered));
    }
}
