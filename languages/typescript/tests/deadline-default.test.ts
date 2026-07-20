import { describe, expect, test } from 'vitest';
import { DEFAULT_OVERALL_DEADLINE_MS, RapMockTransport } from '../runtime/src/index';
import { resolveOverallDeadlineMs } from '../runtime/src/RapClient';
import { mockedClient, syntheticCardPayment } from './support/TestClients';

/**
 * ADR-SDK-027 deadline-default semantics: an omitted overallDeadlineMs resolves to the
 * 30-second ratified default, an explicit null opts out entirely, explicit values pass
 * through, and zero/negative values are still rejected.
 */

describe('deadline defaults (ADR-SDK-027)', () => {
    test('the ratified default is 30 seconds', () => {
        expect(DEFAULT_OVERALL_DEADLINE_MS).toBe(30_000);
    });

    test('omitted resolves to the default, null disables, values pass through', () => {
        expect(resolveOverallDeadlineMs(undefined)).toBe(DEFAULT_OVERALL_DEADLINE_MS);
        expect(resolveOverallDeadlineMs(null)).toBeUndefined();
        expect(resolveOverallDeadlineMs(5_000)).toBe(5_000);
    });

    test('a null (disabled) deadline is accepted at construction and requests still flow', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();

        await mockedClient(mock, { overallDeadlineMs: null }).charge(syntheticCardPayment());

        expect(mock.requests.length).toBe(1);
    });

    test('zero and negative deadlines are still rejected', () => {
        expect(() => mockedClient(new RapMockTransport(), { overallDeadlineMs: 0 })).toThrow(
            'overallDeadlineMs must be positive',
        );
        expect(() => mockedClient(new RapMockTransport(), { overallDeadlineMs: -5 })).toThrow(
            'overallDeadlineMs must be positive',
        );
    });
});
