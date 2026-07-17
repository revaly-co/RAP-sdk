<?php

declare(strict_types=1);

namespace Revaly\Sdk\Reconcile;

/**
 * The reconcile helper's verdict (failover-contract §3; ADR-SDK-009). V1 deliberately
 * has only two concrete verdicts — {@see Found} and {@see NotFoundYet}; there is NO
 * SafeToFailover in V1 ("not found" means *not yet visible*, never "doesn't exist").
 * `SafeToFailover` arrives with platform P-2 as a minor release.
 *
 * The verdict hierarchy is designed OPEN for extension (runtime-tdd §4): new verdicts
 * can arrive in minor releases, so every merchant branch MUST carry a default:
 *
 * ```php
 * if ($verdict instanceof Found) {
 *     // ...
 * } elseif ($verdict instanceof NotFoundYet) {
 *     // ...
 * } else {
 *     // Default branch — REQUIRED: future SDK minors add verdicts (e.g. SafeToFailover).
 *     escalatePerMerchantPolicy($verdict);
 * }
 * ```
 */
abstract class RapReconcileVerdict
{
    /** @internal constructed by the SDK only; merchants branch on the concrete type */
    protected function __construct(private readonly ?string $correlationId)
    {
    }

    /**
     * The last observed `X-Correlation-ID`, if any response was received. Quote it in
     * support tickets (DX contract §c).
     */
    public function getCorrelationId(): ?string
    {
        return $this->correlationId;
    }
}
