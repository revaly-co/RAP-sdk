<?php

declare(strict_types=1);

namespace Revaly\Sdk\Reconcile;

/**
 * No record is visible yet. This is NOT proof of absence (platform visibility is
 * asynchronous and unbounded — widest exactly when RAP-core is degraded): hold and
 * re-poll with backoff; on sustained NotFoundYet, escalate per merchant policy. If a
 * merchant chooses to fail over anyway, that decision lives in their code against their
 * risk policy — this SDK does not bless it (failover-contract §3).
 */
final class NotFoundYet extends RapReconcileVerdict
{
    /** @internal constructed by the SDK only */
    public function __construct(
        private readonly int $attempts,
        private readonly float $elapsedSeconds,
        ?string $lastCorrelationId,
        private readonly ?int $lastHttpStatus,
    ) {
        parent::__construct($lastCorrelationId);
    }

    /** GET attempts performed within the policy bounds. */
    public function getAttempts(): int
    {
        return $this->attempts;
    }

    /** Wall-clock time spent polling, in seconds. */
    public function getElapsedSeconds(): float
    {
        return $this->elapsedSeconds;
    }

    /** The last HTTP status observed, if any response was received. */
    public function getLastHttpStatus(): ?int
    {
        return $this->lastHttpStatus;
    }
}
