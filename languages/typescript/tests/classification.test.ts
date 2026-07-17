import { describe, expect, test } from 'vitest';
import {
    RapError,
    RapMockTransport,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransientFailure,
    RequiredError,
    SyntheticData,
    toRapResult,
} from '../runtime/src/index';
import { mockedClient, syntheticCardPayment } from './support/TestClients';

/**
 * The failover-contract §2 classification matrix, row by row, through the full client
 * stack (charge → transport → classification middleware). The CLASS is the contract;
 * these tests are the SDK's half of the §6 verification obligations.
 */

async function chargeFailure(mock: RapMockTransport, overrides = {}): Promise<RapError> {
    const client = mockedClient(mock, overrides);
    try {
        await client.charge(syntheticCardPayment());
    } catch (failure) {
        if (failure instanceof RapError) {
            return failure;
        }
        throw failure;
    }
    throw new Error('expected the charge to fail');
}

describe('PermanentRejection rows', () => {
    for (const status of [400, 401, 403, 404, 422]) {
        test(`HTTP ${status} classifies PermanentRejection`, async () => {
            const mock = new RapMockTransport();
            mock.charge().returnsPermanentRejection(status);

            const failure = await chargeFailure(mock);

            expect(failure).toBeInstanceOf(RapPermanentRejection);
            expect(failure.kind).toBe('PermanentRejection');
            expect(failure.status).toBe(status);
            expect(failure.apiError).toBe('synthetic rejection');
            expect(failure.correlationId).toBe(SyntheticData.DEFAULT_CORRELATION_ID);
            expect(failure.rawBody).toContain('synthetic rejection');
        });
    }

    test('a 400 with an unparseable body still classifies PermanentRejection', async () => {
        const mock = new RapMockTransport();
        mock.charge().returns(400, 'not json at all');

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapPermanentRejection);
        expect(failure.message).toContain('request rejected');
        expect(failure.code).toBeUndefined();
    });

    test('details pass through opaque', async () => {
        const mock = new RapMockTransport();
        mock.charge().returns(422, JSON.stringify({ error: 'invalid', details: { field: ['amount'] } }));

        const failure = await chargeFailure(mock);

        expect(failure.details).toEqual({ field: ['amount'] });
    });
});

describe('TransientFailure rows', () => {
    test('503 + code not_processed classifies TransientFailure (fast failover)', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapTransientFailure);
        expect(failure.status).toBe(503);
        expect(failure.code).toBe('not_processed');
    });

    test('on apiVersion 2.0 the not_processed signal is NOT honored (narrowed contract)', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();

        const failure = await chargeFailure(mock, { apiVersion: '2.0' });

        expect(failure).toBeInstanceOf(RapOutcomeUnknown);
        expect(failure.code).toBe('not_processed');
    });

    test('connection refused (happy-eyeballs AggregateError) is provably never sent', async () => {
        const mock = new RapMockTransport();
        mock.charge().throwsConnectionRefused();

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapTransientFailure);
        expect(failure.message).toContain('ECONNREFUSED');
        expect(failure.status).toBeUndefined();
    });

    test('DNS failure is provably never sent', async () => {
        const mock = new RapMockTransport();
        mock.charge().throwsDnsFailure();

        expect(await chargeFailure(mock)).toBeInstanceOf(RapTransientFailure);
    });

    test('TLS handshake failure is provably never sent', async () => {
        const mock = new RapMockTransport();
        mock.charge().throwsSslHandshakeFailure();

        expect(await chargeFailure(mock)).toBeInstanceOf(RapTransientFailure);
    });

    test('connect-phase timeout (UND_ERR_CONNECT_TIMEOUT) is provably never sent', async () => {
        const mock = new RapMockTransport();
        mock.charge().throwsConnectTimeout();

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapTransientFailure);
        expect(failure.message).toContain('UND_ERR_CONNECT_TIMEOUT');
    });
});

describe('OutcomeUnknown rows', () => {
    test('bare 503 (no code) may have been dispatched', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsBare503();

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapOutcomeUnknown);
        expect(failure.status).toBe(503);
        expect(failure.code).toBeUndefined();
    });

    test('503 with an unrecognized code treats the code as absent — and keeps it verbatim', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsUnknownCode503('brand_new_signal');

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapOutcomeUnknown);
        // Open string, straight off the wire (OQ-2 adds values later).
        expect(failure.code).toBe('brand_new_signal');
    });

    for (const [scenario, status] of [
        ['returnsServerError', 500],
        ['returnsBadGateway', 502],
        ['returnsGatewayTimeout', 504],
    ] as const) {
        test(`HTTP ${status} classifies OutcomeUnknown`, async () => {
            const mock = new RapMockTransport();
            mock.charge()[scenario]();

            const failure = await chargeFailure(mock);

            expect(failure).toBeInstanceOf(RapOutcomeUnknown);
            expect(failure.status).toBe(status);
        });
    }

    test('a status outside the §2 table (409) is ambiguous → OutcomeUnknown', async () => {
        const mock = new RapMockTransport();
        mock.charge().returns(409, SyntheticData.errorBody('conflict'));

        expect(await chargeFailure(mock)).toBeInstanceOf(RapOutcomeUnknown);
    });

    test('a redirect is never followed and classifies OutcomeUnknown', async () => {
        const mock = new RapMockTransport();
        mock.charge().returns(307, '', { Location: 'https://elsewhere.example.test/payments' });

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapOutcomeUnknown);
        expect(failure.status).toBe(307);
        // And the transport asked for manual redirect handling in the first place.
        expect(mock.requests).toHaveLength(1);
    });

    test('timeout after send (UND_ERR_HEADERS_TIMEOUT) carries no never-sent proof', async () => {
        const mock = new RapMockTransport();
        mock.charge().throwsTimeoutAfterSend();

        expect(await chargeFailure(mock)).toBeInstanceOf(RapOutcomeUnknown);
    });

    test('connection reset mid-flight carries no never-sent proof', async () => {
        const mock = new RapMockTransport();
        mock.charge().throwsConnectionReset();

        expect(await chargeFailure(mock)).toBeInstanceOf(RapOutcomeUnknown);
    });

    test('an unrecognized transport failure classifies OutcomeUnknown — never guess toward safe', async () => {
        const mock = new RapMockTransport();
        mock.charge().throwsIo(new Error('something novel went wrong'));

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapOutcomeUnknown);
        expect(failure.message).toContain('without never-sent proof');
    });

    test('overall deadline expiry classifies OutcomeUnknown (may already have been sent)', async () => {
        const mock = new RapMockTransport();
        mock.charge().hangsUntilAborted();

        const failure = await chargeFailure(mock, { overallDeadlineMs: 25 });

        expect(failure).toBeInstanceOf(RapOutcomeUnknown);
        expect(failure.message).toContain('deadline exceeded');
    });

    test('a 2xx with an unreadable body classifies OutcomeUnknown (post-dispatch)', async () => {
        const mock = new RapMockTransport();
        mock.charge().returns(200, '<html>a proxy answered</html>', { 'Content-Type': 'text/html' });

        const failure = await chargeFailure(mock);

        expect(failure).toBeInstanceOf(RapOutcomeUnknown);
        expect(failure.status).toBe(200);
        expect(failure.message).toContain('unreadable');
    });
});

describe('what is NOT a payment outcome', () => {
    test('caller cancellation rethrows the abort reason, untyped', async () => {
        const mock = new RapMockTransport();
        mock.charge().hangsUntilAborted();
        const client = mockedClient(mock);
        const controller = new AbortController();
        setTimeout(() => controller.abort(), 10);

        await expect(client.charge(syntheticCardPayment(), { signal: controller.signal })).rejects.toSatisfy(
            (failure: unknown) => !(failure instanceof RapError),
        );
    });

    test('an already-aborted caller signal rejects without classification', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const client = mockedClient(mock);
        const controller = new AbortController();
        controller.abort(new Error('merchant cancelled'));

        await expect(client.charge(syntheticCardPayment(), { signal: controller.signal })).rejects.toSatisfy(
            (failure: unknown) => !(failure instanceof RapError),
        );
    });

    test('core request validation (RequiredError) rethrows untyped — a caller error', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const client = mockedClient(mock);

        await expect(
            client.payments.chargePayment({ paymentRequest: undefined as never }),
        ).rejects.toBeInstanceOf(RequiredError);
        // It never reached the wire.
        expect(mock.requests).toHaveLength(0);
    });
});

describe('the re-exported core surface classifies identically', () => {
    test('a generated api method rejects with the same typed classes', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        const client = mockedClient(mock);

        await expect(
            client.payments.chargePayment({ paymentRequest: syntheticCardPayment() }),
        ).rejects.toBeInstanceOf(RapTransientFailure);
    });

    test('toRapResult folds the taxonomy into the discriminated union', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        const client = mockedClient(mock);

        const result = await toRapResult(() => client.charge(syntheticCardPayment()));

        expect(result.ok).toBe(false);
        if (!result.ok) {
            expect(result.failure.kind).toBe('TransientFailure');
        }
    });

    test('toRapResult rethrows non-taxonomy failures', async () => {
        await expect(
            toRapResult(() => Promise.reject(new Error('programming error'))),
        ).rejects.toThrow('programming error');
    });
});
