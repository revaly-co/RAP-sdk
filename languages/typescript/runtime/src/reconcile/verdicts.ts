import type { PendingTransactionResponse, TransactionResponse } from '../../../core/models/index';

/**
 * Terminal outcome of a found transaction, mapped from the record's
 * `transactionStatus` (1=Approved, 2=Declined, 3=Error). `Pending` is the post-P-2
 * intent state; `Unknown` covers unmapped statuses and record shapes this SDK version
 * cannot read — found-but-unmapped is still FOUND. Values match the other language
 * runtimes' tokens so cross-language log lines join cleanly.
 */
export type RapTransactionOutcome = 'Approved' | 'Declined' | 'Error' | 'Pending' | 'Unknown';

/**
 * A record for the merchantTransactionId IS visible at RAP-core (failover-contract §3).
 * `Found(Approved)` means the money moved — failing over now would double-charge.
 */
export interface Found {
    readonly kind: 'found';
    readonly outcome: RapTransactionOutcome;
    /** The terminal record, when the sighting was a terminal transaction. */
    readonly transaction?: TransactionResponse;
    /** The pending intent, when the sighting was a post-P-2 pending state. */
    readonly pending?: PendingTransactionResponse;
    readonly correlationId?: string;
}

/**
 * No record is visible YET (failover-contract §3): platform visibility is asynchronous
 * and unbounded — absence is NOT provable in V1. Hold and re-poll; on sustained
 * NotFoundYet, escalate per merchant policy.
 */
export interface NotFoundYet {
    readonly kind: 'notFoundYet';
    readonly attempts: number;
    readonly elapsedMs: number;
    readonly lastCorrelationId?: string;
    readonly lastHttpStatus?: number;
}

/**
 * Verdicts are designed OPEN FOR EXTENSION (ADR-SDK-009): `SafeToFailover` arrives with
 * platform P-2 as a **minor** release. This sentinel member exists purely so an
 * exhaustive switch over the union does not compile without a default branch — it is
 * never constructed at runtime. Always write the default branch (the quickstart shows
 * it).
 */
export interface ReconcileVerdictExtension {
    readonly kind: 'reconcileVerdictExtension';
}

/**
 * The reconcile verdict union — V1 returns `Found` or `NotFoundYet` only, and the union
 * is non-exhaustive by design (runtime-tdd §4): branch with a default.
 */
export type RapReconcileVerdict = Found | NotFoundYet | ReconcileVerdictExtension;
