import { describe, expect, test } from 'vitest';
import { RapError, RapMockTransport } from '../runtime/src/index';
import { mockedClient, syntheticCardPayment } from './support/TestClients';

/**
 * ADR-SDK-004: no hidden retries anywhere; single-shot semantics. Every failure class
 * leaves EXACTLY ONE request on the wire — the explicit, caller-bounded reconcile
 * re-poll is the only loop this SDK owns (covered in reconcile.test.ts).
 */
describe('single-shot semantics', () => {
    const scenarios = [
        ['returnsPermanentRejection', (mock: RapMockTransport) => mock.charge().returnsPermanentRejection(400)],
        ['returnsNotProcessed503', (mock: RapMockTransport) => mock.charge().returnsNotProcessed503()],
        ['returnsServerError', (mock: RapMockTransport) => mock.charge().returnsServerError()],
        ['throwsConnectionRefused', (mock: RapMockTransport) => mock.charge().throwsConnectionRefused()],
        ['throwsConnectionReset', (mock: RapMockTransport) => mock.charge().throwsConnectionReset()],
    ] as const;

    for (const [name, script] of scenarios) {
        test(`${name}: exactly one dispatch, no retry`, async () => {
            const mock = new RapMockTransport();
            script(mock);
            const client = mockedClient(mock);

            await expect(client.charge(syntheticCardPayment())).rejects.toBeInstanceOf(RapError);

            expect(mock.requests).toHaveLength(1);
        });
    }

    test('success: exactly one dispatch', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();

        await mockedClient(mock).charge(syntheticCardPayment());

        expect(mock.requests).toHaveLength(1);
    });
});
