import { describe, expect, test } from 'vitest';
import type { RapWireTrace } from '../runtime/src/index';
import { RapError, RapMockTransport } from '../runtime/src/index';
import { CollectingLogger } from './support/CollectingLogger';
import { mockedClient, SYNTHETIC_API_KEY, SYNTHETIC_CVV, SYNTHETIC_PAN, syntheticCardPayment } from './support/TestClients';

/**
 * The ADR-SDK-020 log-capture obligation: everything the runtime emits — every level,
 * messages AND context values, wire traces, error messages — is captured and scanned
 * for payload values, PAN/CVV/PII and the API key. This is the CI-enforced PCI
 * assertion for this runtime.
 */

const SENSITIVE = [SYNTHETIC_PAN, SYNTHETIC_CVV, SYNTHETIC_API_KEY, 'Shopper', 'shopper@example.test'];

describe('values-free logging (default verbosity)', () => {
    test('a successful charge logs operation, status and correlation only', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const logger = new CollectingLogger();

        await mockedClient(mock, { logger }).charge(syntheticCardPayment());

        const info = logger.ofLevel('info');
        expect(info).toHaveLength(1);
        expect(info[0]!.message).toBe('rap.request');
        expect(info[0]!.context).toEqual({ operation: 'charge', status: 200, correlation: 'corr-synthetic-1' });
    });

    test('a failed charge warns with class, status, code, correlation — no payload', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        const logger = new CollectingLogger();

        await expect(mockedClient(mock, { logger }).charge(syntheticCardPayment())).rejects.toBeInstanceOf(RapError);

        const warn = logger.ofLevel('warn');
        expect(warn).toHaveLength(1);
        expect(warn[0]!.context).toEqual({
            operation: 'charge',
            class: 'TransientFailure',
            status: 503,
            code: 'not_processed',
            correlation: 'corr-synthetic-1',
        });
    });
});

describe('no sensitive material at ANY level (ADR-SDK-020)', () => {
    test('success path, debug enabled: nothing sensitive in any line', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const logger = new CollectingLogger();

        await mockedClient(mock, { logger }).charge(syntheticCardPayment());

        const all = logger.all();
        for (const secret of SENSITIVE) {
            expect(all).not.toContain(secret);
        }
        // Debug DID carry the scrubbed payload — the safe identifiers survive.
        expect(all).toContain('mtx-synthetic-1');
    });

    test('failure path: nothing sensitive in any line', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsServerError();
        const logger = new CollectingLogger();

        await expect(mockedClient(mock, { logger }).charge(syntheticCardPayment())).rejects.toBeInstanceOf(RapError);

        const all = logger.all();
        for (const secret of SENSITIVE) {
            expect(all).not.toContain(secret);
        }
    });

    test('reconcile path: nothing sensitive in any line', async () => {
        const mock = new RapMockTransport();
        mock.reconcile('mtx-synthetic-1').notFoundYet(1).thenFoundApproved();
        const logger = new CollectingLogger();

        await mockedClient(mock, { logger }).reconcile('mtx-synthetic-1', {
            maxAttempts: 3,
            overallBudgetMs: 60_000,
            initialDelayMs: 0,
        });

        const all = logger.all();
        for (const secret of SENSITIVE) {
            expect(all).not.toContain(secret);
        }
    });

    test('typed error messages and stacks never carry the API key', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsPermanentRejection(401);

        try {
            await mockedClient(mock).charge(syntheticCardPayment());
            expect.unreachable('charge must fail');
        } catch (failure) {
            const error = failure as RapError;
            expect(error.message).not.toContain(SYNTHETIC_API_KEY);
            expect(error.stack ?? '').not.toContain(SYNTHETIC_API_KEY);
            expect(JSON.stringify({ ...error })).not.toContain(SYNTHETIC_API_KEY);
        }
    });
});

describe('wire-trace hook (runtime-tdd §6)', () => {
    test('receives scrubbed payloads only — never raw material', async () => {
        const traces: RapWireTrace[] = [];
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();

        await mockedClient(mock, { wireTraceHook: (trace) => traces.push(trace) }).charge(syntheticCardPayment());

        expect(traces).toHaveLength(1);
        const trace = traces[0]!;
        expect(trace.operation).toBe('charge');
        expect(trace.method).toBe('POST');
        expect(trace.path).toBe('/payments');
        expect(trace.status).toBe(200);
        expect(trace.correlationId).toBe('corr-synthetic-1');
        const material = JSON.stringify(traces);
        for (const secret of SENSITIVE) {
            expect(material).not.toContain(secret);
        }
        expect(trace.scrubbedRequestBody).toContain('mtx-synthetic-1');
        expect(trace.scrubbedResponseBody).toContain('transactionId');
    });

    test('reconcile traces are scrubbed the same way', async () => {
        const traces: RapWireTrace[] = [];
        const mock = new RapMockTransport();
        mock.reconcile('mtx-synthetic-1').returnsApproved();

        await mockedClient(mock, { wireTraceHook: (trace) => traces.push(trace) }).reconcile('mtx-synthetic-1', {
            maxAttempts: 1,
            overallBudgetMs: 60_000,
            initialDelayMs: 0,
        });

        expect(traces).toHaveLength(1);
        expect(traces[0]!.operation).toBe('reconcile');
        // The template path never embeds the live merchant transaction id.
        expect(traces[0]!.path).toBe('/transactions/merchant/{merchantTransactionId}');
    });

    test('a throwing observer is swallowed and the payment still succeeds', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const logger = new CollectingLogger();

        const response = await mockedClient(mock, {
            logger,
            wireTraceHook: () => {
                throw new Error('observer exploded');
            },
        }).charge(syntheticCardPayment());

        expect(response.transactionId).toBe('txn-synthetic-1');
        expect(logger.all()).toContain('rap.wiretrace hook threw; ignored');
    });

    test('a throwing logger never changes payment control flow', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const hostileLogger = {
            info: () => {
                throw new Error('logger exploded');
            },
        };

        const response = await mockedClient(mock, { logger: hostileLogger }).charge(syntheticCardPayment());

        expect(response.transactionId).toBe('txn-synthetic-1');
    });
});
