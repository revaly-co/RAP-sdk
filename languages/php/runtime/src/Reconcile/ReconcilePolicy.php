<?php

declare(strict_types=1);

namespace Revaly\Sdk\Reconcile;

/**
 * The caller-bounded polling policy for {@see \Revaly\Sdk\RapClient::reconcile()} — the
 * ONLY loop this SDK owns (ADR-SDK-004). All bounds are explicit constructor arguments:
 * the SDK ships no default attempt counts, budgets, or delays until the OQ-6
 * telemetry-derived recommendations land (docs/open-items.md — deliberately not
 * invented here). The backoff shape is exponential with jitter ([Proposed]: multiplier
 * 2.0, full jitter ±20%).
 */
final class ReconcilePolicy
{
    private const MULTIPLIER = 2.0;
    private const JITTER_RATIO = 0.2;

    /**
     * Choose bounds per your risk policy: reconciliation is how an OutcomeUnknown
     * payment is resolved, so the budget bounds how long your checkout holds before
     * escalating.
     *
     * @param int $maxAttempts maximum GET attempts (≥ 1)
     * @param float $overallBudgetSeconds total wall-clock budget across all attempts and waits
     * @param float $initialDelaySeconds delay before the second attempt; doubles each attempt (with jitter)
     * @param float|null $maxDelaySeconds optional cap on the per-wait delay; null leaves
     *        growth uncapped within the budget
     */
    public function __construct(
        private readonly int $maxAttempts,
        private readonly float $overallBudgetSeconds,
        private readonly float $initialDelaySeconds,
        private readonly ?float $maxDelaySeconds = null,
    ) {
        if ($maxAttempts < 1) {
            throw new \InvalidArgumentException('maxAttempts: at least one attempt is required');
        }
        if ($overallBudgetSeconds <= 0) {
            throw new \InvalidArgumentException('overallBudgetSeconds: the overall budget must be positive');
        }
        if ($initialDelaySeconds < 0) {
            throw new \InvalidArgumentException('initialDelaySeconds: the initial delay cannot be negative');
        }
    }

    /** Maximum GET attempts. */
    public function getMaxAttempts(): int
    {
        return $this->maxAttempts;
    }

    /** Total wall-clock budget across all attempts and waits, in seconds. */
    public function getOverallBudgetSeconds(): float
    {
        return $this->overallBudgetSeconds;
    }

    /** Delay before the second attempt (exponential growth afterwards), in seconds. */
    public function getInitialDelaySeconds(): float
    {
        return $this->initialDelaySeconds;
    }

    /** Optional cap on the per-wait delay, in seconds; null when uncapped. */
    public function getMaxDelaySeconds(): ?float
    {
        return $this->maxDelaySeconds;
    }

    /** @internal the jittered wait after the given number of completed attempts */
    public function delayForAttempt(int $completedAttempts): float
    {
        if ($this->initialDelaySeconds <= 0) {
            return 0.0;
        }

        $raw = $this->initialDelaySeconds * (self::MULTIPLIER ** ($completedAttempts - 1));
        if ($this->maxDelaySeconds !== null && $raw > $this->maxDelaySeconds) {
            $raw = $this->maxDelaySeconds;
        }

        $jitterSpan = $raw * self::JITTER_RATIO;
        $unit = mt_rand() / mt_getrandmax();
        $jittered = $raw + (($unit * 2.0) - 1.0) * $jitterSpan;

        return max(0.0, $jittered);
    }
}
