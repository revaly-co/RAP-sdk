import { describe, expect, test } from 'vitest';
import {
    RapClient,
    RapMockTransport,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransientFailure,
    toRapResult,
} from '../runtime/src/index';
import { syntheticCardPayment } from './support/TestClients';

/**
 * The README quickstart, executed (DX contract §b): init → charge → handle ALL THREE
 * error classes → reconcile with the default branch. If this test drifts from the
 * README, the README is wrong.
 */

describe('quickstart flow', () => {
    test('charge → three-class handling → reconcile with default branch', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        mock.reconcile('order-1042').notFoundYet(1).thenFoundApproved();

        // -- init (quickstart step 1; transport is the mock so the flow runs with no network)
        const client = new RapClient({ apiKey: 'sk-synthetic-quickstart', transport: mock });

        // -- charge + all three error classes (quickstart step 2)
        const journal: string[] = [];
        try {
            await client.charge(syntheticCardPayment('order-1042'));
            journal.push('paid');
        } catch (failure) {
            if (failure instanceof RapPermanentRejection) {
                journal.push('declined-permanently'); // fix or decline — never fail over
            } else if (failure instanceof RapTransientFailure) {
                journal.push('fail-over-now'); // definitively not processed
            } else if (failure instanceof RapOutcomeUnknown) {
                journal.push('reconcile-first'); // may have been processed
            } else {
                throw failure; // not a payment outcome
            }
        }
        expect(journal).toEqual(['fail-over-now']);

        // -- reconcile worked example (quickstart step 3) — always with the default branch
        const verdict = await client.reconcile('order-1042', {
            maxAttempts: 5,
            overallBudgetMs: 30_000,
            initialDelayMs: 1,
        });
        switch (verdict.kind) {
            case 'Found':
                journal.push(`found:${verdict.outcome}`);
                break;
            case 'NotFoundYet':
                journal.push(`hold:${verdict.attempts}`);
                break;
            default:
                journal.push('escalate'); // future verdicts (SafeToFailover, post-P-2) land here
                break;
        }
        expect(journal).toEqual(['fail-over-now', 'found:Approved']);
    });

    test('the result-union variant reads without try/catch', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const client = new RapClient({ apiKey: 'sk-synthetic-quickstart', transport: mock });

        const result = await toRapResult(() => client.charge(syntheticCardPayment()));

        if (result.ok) {
            expect(result.value.transactionId).toBe('txn-synthetic-1');
        } else {
            switch (result.failure.kind) {
                case 'PermanentRejection':
                case 'TransientFailure':
                case 'OutcomeUnknown':
                default:
                    expect.unreachable('this charge succeeds');
            }
        }
    });

    test('merchant failover-handler testing with scripted consecutive outcomes (DX §d)', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsBare503().returnsNotProcessed503().returnsApproved();
        const client = new RapClient({ apiKey: 'sk-synthetic-quickstart', transport: mock });

        const outcomes: string[] = [];
        for (let attempt = 0; attempt < 3; attempt++) {
            const result = await toRapResult(() => client.charge(syntheticCardPayment(`order-${attempt}`)));
            outcomes.push(result.ok ? 'ok' : result.failure.kind);
        }

        expect(outcomes).toEqual(['OutcomeUnknown', 'TransientFailure', 'ok']);
    });
});
