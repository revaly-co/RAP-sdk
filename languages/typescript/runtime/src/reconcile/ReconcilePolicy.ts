/**
 * The caller-bounded polling policy for {@link RapClient.reconcile} — the ONLY loop
 * this SDK owns (ADR-SDK-004). All bounds are explicit: the SDK ships no default
 * attempt counts, budgets, or delays until the OQ-6 telemetry-derived recommendations
 * land (docs/open-items.md — deliberately not invented here). The backoff shape is
 * exponential with jitter ([Proposed]: multiplier 2.0, full jitter ±20%).
 *
 * Choose bounds per your risk policy: reconciliation is how an OutcomeUnknown payment
 * is resolved, so the budget bounds how long your checkout holds before escalating.
 */
export interface ReconcilePolicy {
    /** Maximum GET attempts (≥ 1). */
    readonly maxAttempts: number;
    /** Total wall-clock budget across all attempts and waits, in milliseconds. */
    readonly overallBudgetMs: number;
    /** Delay before the second attempt, in milliseconds; doubles each attempt (with jitter). */
    readonly initialDelayMs: number;
    /** Optional cap on the per-wait delay; omit to leave growth uncapped within the budget. */
    readonly maxDelayMs?: number;
}

const MULTIPLIER = 2.0;
const JITTER_RATIO = 0.2;

/** @internal */
export function validatePolicy(policy: ReconcilePolicy): void {
    if (!Number.isInteger(policy.maxAttempts) || policy.maxAttempts < 1) {
        throw new TypeError('maxAttempts: at least one attempt is required');
    }
    if (!(policy.overallBudgetMs > 0)) {
        throw new TypeError('overallBudgetMs: the overall budget must be positive');
    }
    if (!(policy.initialDelayMs >= 0)) {
        throw new TypeError('initialDelayMs: the initial delay cannot be negative');
    }
}

/** @internal the jittered wait after the given number of completed attempts, in milliseconds */
export function delayForAttempt(policy: ReconcilePolicy, completedAttempts: number): number {
    if (policy.initialDelayMs <= 0) {
        return 0;
    }

    let raw = policy.initialDelayMs * MULTIPLIER ** (completedAttempts - 1);
    if (policy.maxDelayMs !== undefined && raw > policy.maxDelayMs) {
        raw = policy.maxDelayMs;
    }

    const jitterSpan = raw * JITTER_RATIO;
    const jittered = raw + (Math.random() * 2 - 1) * jitterSpan;

    return Math.max(0, jittered);
}
