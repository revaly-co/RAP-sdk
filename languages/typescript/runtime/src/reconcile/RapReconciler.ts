import type { TransactionsApi } from '../../../core/apis/index';
import {
    instanceOfPendingTransactionResponse,
    PendingTransactionResponseFromJSON,
} from '../../../core/models/PendingTransactionResponse';
import { TransactionResponseFromJSON } from '../../../core/models/TransactionResponse';
import { RapError, RapPermanentRejection } from '../errors/RapError';
import type { RapLogger } from '../logging/RapLogger';
import { scrubJson } from '../logging/RapScrubber';
import type { RapWireTraceHook } from '../logging/RapWireTrace';
import { CORRELATION_ID } from '../transport/RapHeaders';
import { delayForAttempt, validatePolicy, type ReconcilePolicy } from './ReconcilePolicy';
import type { Found, NotFoundYet, RapReconcileVerdict, RapTransactionOutcome } from './verdicts';

export interface ReconcileOptions {
    /** Cancels the loop (including waits). Cancellation rethrows the abort reason. */
    readonly signal?: AbortSignal;
}

/**
 * The OutcomeUnknown reconciliation procedure (failover-contract §3): GET-only,
 * side-effect-free, caller-bounded — the only loop the runtime owns (ADR-SDK-004).
 *
 * The GET goes through the same generated api / transport / classification stack as
 * every other SDK request, but verdicts are read from the RAW response body, never the
 * core's typed wrapper (repo rule 5): reconciliation is the safety path, so it must not
 * depend on generated discrimination logic — server-newer-than-spec shapes still count
 * as sightings here. The raw body's required `state` field discriminates a pending
 * intent, and terminal records bind directly to TransactionResponse.
 */
export class RapReconciler {
    constructor(
        private readonly transactions: TransactionsApi,
        private readonly logger: Required<RapLogger>,
        private readonly wireTraceHook: RapWireTraceHook | undefined,
    ) {}

    /**
     * Runs the reconcile loop until a record is visible or the policy bounds are spent.
     *
     * Throws a typed failure only for a rejected READ that polling can never fix
     * (PermanentRejection other than 404 — bad credentials, malformed id); 404 is the
     * NotFoundYet signal, and degraded reads (5xx/timeouts/transport failures) keep
     * polling within the budget — exactly the window where visibility is widest.
     */
    async reconcile(
        merchantTransactionId: string,
        policy: ReconcilePolicy,
        options: ReconcileOptions = {},
    ): Promise<RapReconcileVerdict> {
        if (merchantTransactionId.trim() === '') {
            throw new TypeError('merchantTransactionId is required');
        }
        validatePolicy(policy);

        const path = '/transactions/merchant/{merchantTransactionId}';
        const start = Date.now();
        let attempts = 0;
        let lastCorrelationId: string | undefined;
        let lastHttpStatus: number | undefined;

        while (true) {
            attempts++;

            let outcome: Found | undefined;
            try {
                const apiResponse = await this.transactions.getTransactionByMerchantTransactionIdRaw(
                    { merchantTransactionId },
                    { signal: options.signal ?? null },
                );
                lastHttpStatus = apiResponse.raw.status;
                const correlationId = apiResponse.raw.headers.get(CORRELATION_ID) ?? undefined;
                if (correlationId !== undefined) {
                    lastCorrelationId = correlationId;
                }
                const rawBody = await apiResponse.raw.clone().text();
                this.trace(path, apiResponse.raw.status, correlationId, rawBody);

                outcome = this.readFound(rawBody, lastCorrelationId, attempts);
            } catch (failure) {
                if (options.signal?.aborted) {
                    // Caller cancellation is not a read outcome — it propagates.
                    throw failure;
                }
                if (failure instanceof RapPermanentRejection && failure.status === 404) {
                    // Not yet visible — the NotFoundYet signal, not an error (§3).
                    lastHttpStatus = 404;
                    if (failure.correlationId !== undefined) {
                        lastCorrelationId = failure.correlationId;
                    }
                    this.trace(path, 404, failure.correlationId, failure.rawBody);
                    this.logger.debug('rap.reconcile not visible yet (404)', { attempt: attempts });
                } else if (failure instanceof RapPermanentRejection) {
                    // 400/401/403/422 escape: polling will never fix a rejected read
                    // (bad credentials, malformed id) — the caller must see it.
                    throw failure;
                } else if (failure instanceof RapError) {
                    // Degraded read path (5xx/timeout/transport failure/unreadable 2xx
                    // on the GET): the WRITE's status is still unknown — keep polling
                    // within the caller's budget.
                    if (failure.status !== undefined) {
                        lastHttpStatus = failure.status;
                    }
                    if (failure.correlationId !== undefined) {
                        lastCorrelationId = failure.correlationId;
                    }
                    this.trace(path, failure.status, failure.correlationId, failure.rawBody);
                    this.logger.warn('rap.reconcile degraded read; continuing within policy', {
                        attempt: attempts,
                        status: failure.status,
                        class: failure.kind,
                    });
                } else {
                    // Not a wire outcome (request validation, programming error) — never
                    // absorbed into the poll loop.
                    throw failure;
                }
            }

            if (outcome !== undefined) {
                return outcome;
            }

            if (attempts >= policy.maxAttempts) {
                break;
            }
            const elapsed = Date.now() - start;
            const delay = delayForAttempt(policy, attempts);
            if (elapsed + delay >= policy.overallBudgetMs) {
                break;
            }
            if (delay > 0) {
                await abortableSleep(delay, options.signal);
            }
        }

        const elapsedMs = Date.now() - start;
        this.logger.info('rap.reconcile verdict=NotFoundYet', {
            attempts,
            elapsedMs,
            lastStatus: lastHttpStatus,
            correlation: lastCorrelationId,
        });

        const verdict: NotFoundYet = {
            kind: 'notFoundYet',
            attempts,
            elapsedMs,
            lastCorrelationId,
            lastHttpStatus,
        };
        return verdict;
    }

    /**
     * Maps a 2xx body to a Found verdict from the RAW json. Returns undefined for a
     * body this SDK cannot read at all (→ poll-continue: an ambiguous read is not a
     * sighting).
     */
    private readFound(rawBody: string, correlationId: string | undefined, attempt: number): Found | undefined {
        let root: unknown;
        try {
            root = JSON.parse(rawBody);
        } catch {
            root = undefined;
        }
        if (typeof root !== 'object' || root === null || Array.isArray(root)) {
            this.logger.warn('rap.reconcile 2xx with an unreadable body; continuing within policy', {
                attempt,
            });
            return undefined;
        }

        // `state` exists only on the pending schema — its presence is authoritative
        // (the spec marks it the discriminator).
        const record = root as Record<string, unknown>;
        if (typeof record['state'] === 'string') {
            if (instanceOfPendingTransactionResponse(root)) {
                this.logger.info('rap.reconcile verdict=Found outcome=Pending', { correlation: correlationId });
                return {
                    kind: 'found',
                    outcome: 'Pending',
                    pending: PendingTransactionResponseFromJSON(root),
                    correlationId,
                };
            }
            // A pending-shaped record this SDK version cannot bind is still a
            // sighting — surface it conservatively rather than polling on.
            return { kind: 'found', outcome: 'Unknown', correlationId };
        }

        // Terminal records bind DIRECTLY to TransactionResponse — never through the
        // core's union wrapper (see the class doc). A shape this SDK version does not
        // recognize (e.g. a grouped envelope or a post-P-2 variant) maps to
        // Found(Unknown): found-but-unmapped is still FOUND.
        const transaction = TransactionResponseFromJSON(root);
        const outcome = mapOutcome(transaction.transactionStatus);
        this.logger.info('rap.reconcile verdict=Found', { outcome, correlation: correlationId });
        return { kind: 'found', outcome, transaction, correlationId };
    }

    private trace(
        path: string,
        status: number | undefined,
        correlationId: string | undefined,
        rawResponseBody: string | undefined,
    ): void {
        if (this.wireTraceHook === undefined) {
            return;
        }
        try {
            this.wireTraceHook({
                operation: 'reconcile',
                method: 'GET',
                path,
                status,
                correlationId,
                scrubbedResponseBody: rawResponseBody === undefined ? undefined : scrubJson(rawResponseBody),
            });
        } catch (hookFailure) {
            // Observer exceptions are swallowed (runtime-tdd §6) — tracing must never
            // change payment control flow.
            this.logger.debug('rap.wiretrace hook threw; ignored', {
                exception: hookFailure instanceof Error ? hookFailure.name : typeof hookFailure,
            });
        }
    }
}

function mapOutcome(transactionStatus: number | null | undefined): RapTransactionOutcome {
    switch (transactionStatus) {
        case 1:
            return 'Approved';
        case 2:
            return 'Declined';
        case 3:
            return 'Error';
        default:
            return 'Unknown';
    }
}

function abortableSleep(ms: number, signal: AbortSignal | undefined): Promise<void> {
    return new Promise((resolve, reject) => {
        if (signal?.aborted) {
            reject(abortReason(signal));
            return;
        }
        const onAbort = (): void => {
            clearTimeout(timer);
            reject(abortReason(signal));
        };
        const timer = setTimeout(() => {
            signal?.removeEventListener('abort', onAbort);
            resolve();
        }, ms);
        signal?.addEventListener('abort', onAbort, { once: true });
    });
}

function abortReason(signal: AbortSignal | undefined): unknown {
    return signal?.reason ?? new DOMException('The operation was aborted.', 'AbortError');
}
