import { describe, expect, test } from 'vitest';
import { REDACTED, SCRUBBED, scrubHeaders, scrubJson, scrubValue } from '../runtime/src/index';
import { SYNTHETIC_CVV, SYNTHETIC_PAN, syntheticCardPayment } from './support/TestClients';

/**
 * The central allowlist scrubber (ADR-SDK-020): only known-safe identifier/status
 * fields pass; every other scalar — and therefore every PAN/CVV/PII field — scrubs.
 * Schema evolution fails safe: a NEW field is scrubbed until the allowlist review says
 * otherwise.
 */

describe('scrubJson', () => {
    test('allowlisted identifier/status fields pass verbatim', () => {
        const scrubbed = JSON.parse(
            scrubJson(
                JSON.stringify({
                    transactionId: 'txn-1',
                    merchantTransactionId: 'mtx-1',
                    transactionStatus: 1,
                    responseCode: '00',
                    currency: 'USD',
                    code: 'not_processed',
                    error: 'synthetic error',
                    state: 'pending',
                }),
            ),
        ) as Record<string, unknown>;

        expect(scrubbed).toEqual({
            transactionId: 'txn-1',
            merchantTransactionId: 'mtx-1',
            transactionStatus: 1,
            responseCode: '00',
            currency: 'USD',
            code: 'not_processed',
            error: 'synthetic error',
            state: 'pending',
        });
    });

    test('non-allowlisted scalars scrub — including amount and message', () => {
        const scrubbed = JSON.parse(
            scrubJson(JSON.stringify({ amount: 1999, message: 'approved', customerId: 'c-1' })),
        ) as Record<string, unknown>;

        expect(scrubbed).toEqual({ amount: SCRUBBED, message: SCRUBBED, customerId: SCRUBBED });
    });

    test('a full card payment scrubs PAN, CVV and holder PII at every depth', () => {
        const scrubbed = scrubJson(JSON.stringify(syntheticCardPayment()));

        expect(scrubbed).not.toContain(SYNTHETIC_PAN);
        expect(scrubbed).not.toContain(SYNTHETIC_CVV);
        expect(scrubbed).not.toContain('Shopper');
        expect(scrubbed).not.toContain('shopper@example.test');
        // Structure is preserved; the safe identifier still joins support tickets.
        expect(scrubbed).toContain('mtx-synthetic-1');
    });

    test('array elements keep only their parent key status', () => {
        const scrubbed = JSON.parse(
            scrubJson(JSON.stringify({ transactions: [{ transactionId: 't-1', amount: 5 }], panList: ['4111'] })),
        ) as { transactions: Array<Record<string, unknown>>; panList: string[] };

        expect(scrubbed.transactions[0]).toEqual({ transactionId: 't-1', amount: SCRUBBED });
        expect(scrubbed.panList).toEqual([SCRUBBED]);
    });

    test('non-JSON input never leaks raw text', () => {
        expect(scrubJson('PAN=4111111111111111')).toBe('[unparseable:scrubbed]');
    });

    test('empty input scrubs to the empty string', () => {
        expect(scrubJson('')).toBe('');
        expect(scrubJson(undefined)).toBe('');
    });
});

describe('scrubValue', () => {
    test('scrubs an in-memory model the same way as its wire form', () => {
        const scrubbed = scrubValue(syntheticCardPayment());

        expect(scrubbed).not.toContain(SYNTHETIC_PAN);
        expect(scrubbed).toContain('merchantTransactionId');
    });

    test('an unserializable value degrades to the scrub token', () => {
        const cyclic: Record<string, unknown> = {};
        cyclic['self'] = cyclic;

        expect(scrubValue(cyclic)).toBe(SCRUBBED);
    });
});

describe('scrubHeaders', () => {
    test('Authorization is redacted — never emitted, not even by length', () => {
        const scrubbed = scrubHeaders({ Authorization: 'ApiKey sk-synthetic-1', 'Content-Type': 'application/json' });

        expect(scrubbed['Authorization']).toBe(REDACTED);
        expect(scrubbed['Content-Type']).toBe('application/json');
    });

    test('allowlisted headers pass; unknown headers redact (fail-safe)', () => {
        const scrubbed = scrubHeaders({
            'X-Api-Version': '2.1',
            'X-Correlation-ID': 'corr-1',
            'api-supported-versions': ['2.0', '2.1'],
            'X-Internal-Routing': 'edge-7',
        });

        expect(scrubbed['X-Api-Version']).toBe('2.1');
        expect(scrubbed['X-Correlation-ID']).toBe('corr-1');
        expect(scrubbed['api-supported-versions']).toBe('2.0, 2.1');
        expect(scrubbed['X-Internal-Routing']).toBe(REDACTED);
    });

    test('accepts a fetch Headers instance', () => {
        const scrubbed = scrubHeaders(
            new Headers({ Authorization: 'ApiKey sk-x', 'User-Agent': 'revaly-sdk-typescript/0.0.0' }),
        );

        expect(scrubbed['authorization']).toBe(REDACTED);
        expect(scrubbed['user-agent']).toBe('revaly-sdk-typescript/0.0.0');
    });
});
