<?php

declare(strict_types=1);

namespace Revaly\Sdk\Reconcile;

use Revaly\Sdk\Core\Model\PendingTransactionResponse;
use Revaly\Sdk\Core\Model\TransactionResponse;

/** A transaction (or pending intent) with this merchantTransactionId is visible. */
final class Found extends RapReconcileVerdict
{
    /** @internal constructed by the SDK only */
    public function __construct(
        private readonly RapTransactionOutcome $outcome,
        private readonly ?TransactionResponse $transaction,
        private readonly ?PendingTransactionResponse $pending,
        ?string $correlationId,
    ) {
        parent::__construct($correlationId);
    }

    /** The mapped outcome — always branch with a default for {@see RapTransactionOutcome::Unknown}. */
    public function getOutcome(): RapTransactionOutcome
    {
        return $this->outcome;
    }

    /** The terminal transaction record, when the record mapped to one; else null. */
    public function getTransaction(): ?TransactionResponse
    {
        return $this->transaction;
    }

    /** The pending intent record (outcome {@see RapTransactionOutcome::Pending}); else null. */
    public function getPending(): ?PendingTransactionResponse
    {
        return $this->pending;
    }
}
