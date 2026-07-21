import { describe, expect, test } from 'vitest';
import type { RapReconcileVerdict, ReconcilePolicy } from '../runtime/src/index';
import { RapMockTransport, RapPermanentRejection, SyntheticData } from '../runtime/src/index';
import { CollectingLogger } from './support/CollectingLogger';
import { mockedClient } from './support/TestClients';

/**
 * The failover-contract §3 procedure: both V1 verdicts, the poll-continue semantics of
 * degraded reads, the PermanentRejection escape, and the caller-bounded loop — the
 * only loop this SDK owns (ADR-SDK-004).
 */

const MTX = 'mtx-synthetic-1';

function immediatePolicy(maxAttempts = 1): ReconcilePolicy {
    return { maxAttempts, overallBudgetMs: 60_000, initialDelayMs: 0 };
}

describe('Found verdicts', () => {
    test.each([
        [1, 'Approved'],
        [2, 'Declined'],
        [3, 'Error'],
        [99, 'Unknown'],
    ])('transactionStatus %d maps to outcome %s', async (status, outcome) => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).returnsUnmappedStatus(status);

        const verdict = await mockedClient(mock).reconcile(MTX, immediatePolicy());

        expect(verdict.kind).toBe('Found');
        if (verdict.kind === 'Found') {
            expect(verdict.outcome).toBe(outcome);
            expect(verdict.transaction?.merchantTransactionId).toBe(MTX);
            expect(verdict.correlationId).toBe(SyntheticData.DEFAULT_CORRELATION_ID);
        }
    });

    test('a pending intent (post-P-2 shape) is Found(Pending) with the pending record', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).pending();

        const verdict = await mockedClient(mock).reconcile(MTX, immediatePolicy());

        expect(verdict.kind).toBe('Found');
        if (verdict.kind === 'Found') {
            expect(verdict.outcome).toBe('Pending');
            expect(verdict.pending?.state).toBe('pending');
            expect(verdict.pending?.merchantTransactionId).toBe(MTX);
            expect(verdict.transaction).toBeUndefined();
        }
    });

    test('a grouped envelope is Found(Unknown) — found-but-unmapped is still FOUND', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).returnsTransactionGroup();

        const verdict = await mockedClient(mock).reconcile(MTX, immediatePolicy());

        expect(verdict.kind).toBe('Found');
        if (verdict.kind === 'Found') {
            expect(verdict.outcome).toBe('Unknown');
        }
    });

    test('a state-bearing record this SDK cannot bind is still a sighting (Found Unknown)', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).returns(200, JSON.stringify({ state: 'reserved-for-p2' }));

        const verdict = await mockedClient(mock).reconcile(MTX, immediatePolicy());

        expect(verdict.kind).toBe('Found');
        if (verdict.kind === 'Found') {
            expect(verdict.outcome).toBe('Unknown');
        }
    });
});

describe('NotFoundYet and the poll loop', () => {
    test('404s then a terminal record: polls until Found', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).notFoundYet(2).thenFoundApproved();

        const verdict = await mockedClient(mock).reconcile(MTX, {
            maxAttempts: 5,
            overallBudgetMs: 60_000,
            initialDelayMs: 1,
        });

        expect(verdict.kind).toBe('Found');
        expect(mock.requests).toHaveLength(3);
    });

    test('NotFoundYet carries attempts, elapsed, last correlation id and last status', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).notFoundYet(3);

        const verdict = await mockedClient(mock).reconcile(MTX, {
            maxAttempts: 3,
            overallBudgetMs: 60_000,
            initialDelayMs: 0,
        });

        expect(verdict.kind).toBe('NotFoundYet');
        if (verdict.kind === 'NotFoundYet') {
            expect(verdict.attempts).toBe(3);
            expect(verdict.elapsedMs).toBeGreaterThanOrEqual(0);
            expect(verdict.lastHttpStatus).toBe(404);
            expect(verdict.lastCorrelationId).toBe(SyntheticData.DEFAULT_CORRELATION_ID);
        }
        expect(mock.requests).toHaveLength(3);
    });

    test('the overall budget bounds the loop even with attempts remaining', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).notFoundYet(1);

        const verdict = await mockedClient(mock).reconcile(MTX, {
            maxAttempts: 50,
            overallBudgetMs: 30,
            initialDelayMs: 100,
        });

        // The first wait (100ms) would already exceed the 30ms budget: stop after one attempt.
        expect(verdict.kind).toBe('NotFoundYet');
        if (verdict.kind === 'NotFoundYet') {
            expect(verdict.attempts).toBe(1);
        }
    });

    test('degraded reads (5xx on the GET) keep polling within the budget', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).returnsServerError().thenFoundApproved();

        const verdict = await mockedClient(mock).reconcile(MTX, immediatePolicy(3));

        expect(verdict.kind).toBe('Found');
        expect(mock.requests).toHaveLength(2);
    });

    test('transport failures on the GET keep polling within the budget', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).throwsConnectionRefused().thenFoundApproved();

        const verdict = await mockedClient(mock).reconcile(MTX, immediatePolicy(3));

        expect(verdict.kind).toBe('Found');
    });

    test('a 2xx with an unreadable body is an ambiguous read — poll again', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).returns(200, 'not json').thenFoundApproved();

        const verdict = await mockedClient(mock).reconcile(MTX, immediatePolicy(3));

        expect(verdict.kind).toBe('Found');
        expect(mock.requests).toHaveLength(2);
    });

    test('a rejected READ that polling can never fix escapes typed (401)', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).returnsPermanentRejection(401);

        await expect(mockedClient(mock).reconcile(MTX, immediatePolicy(5))).rejects.toBeInstanceOf(
            RapPermanentRejection,
        );
        expect(mock.requests).toHaveLength(1);
    });
});

describe('caller bounds and cancellation', () => {
    test('an empty merchantTransactionId is a caller error', async () => {
        await expect(mockedClient(new RapMockTransport()).reconcile('  ', immediatePolicy())).rejects.toThrow(
            'merchantTransactionId is required',
        );
    });

    test.each([
        [{ maxAttempts: 0, overallBudgetMs: 1000, initialDelayMs: 0 }, 'maxAttempts'],
        [{ maxAttempts: 1, overallBudgetMs: 0, initialDelayMs: 0 }, 'overallBudgetMs'],
        [{ maxAttempts: 1, overallBudgetMs: 1000, initialDelayMs: -1 }, 'initialDelayMs'],
    ])('invalid policy %j is rejected', async (policy, messagePart) => {
        await expect(mockedClient(new RapMockTransport()).reconcile(MTX, policy)).rejects.toThrow(messagePart);
    });

    test('aborting during a wait cancels the loop with the abort reason', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).notFoundYet(10);
        const controller = new AbortController();
        setTimeout(() => controller.abort(new Error('checkout gave up')), 20);

        await expect(
            mockedClient(mock).reconcile(
                MTX,
                { maxAttempts: 10, overallBudgetMs: 60_000, initialDelayMs: 5_000 },
                { signal: controller.signal },
            ),
        ).rejects.toThrow('checkout gave up');
    });

    test('the loop dispatches exactly its attempts — no hidden extra requests', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).notFoundYet(4);

        await mockedClient(mock).reconcile(MTX, { maxAttempts: 4, overallBudgetMs: 60_000, initialDelayMs: 0 });

        expect(mock.requests).toHaveLength(4);
    });
});

describe('verdict handling pattern', () => {
    test('the union forces a default branch (open for extension, ADR-SDK-009)', async () => {
        const mock = new RapMockTransport();
        mock.reconcile(MTX).returnsApproved();
        const logger = new CollectingLogger();

        const verdict: RapReconcileVerdict = await mockedClient(mock, { logger }).reconcile(
            MTX,
            immediatePolicy(),
        );

        // The quickstart's switch shape: every merchant integration writes this default.
        let handled: string;
        switch (verdict.kind) {
            case 'Found':
                handled = `found:${verdict.outcome}`;
                break;
            case 'NotFoundYet':
                handled = 'hold';
                break;
            default:
                // Future verdicts (SafeToFailover arrives with P-2) land here.
                handled = 'escalate';
                break;
        }
        expect(handled).toBe('found:Approved');
    });
});
