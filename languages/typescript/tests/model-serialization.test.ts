import { describe, expect, test } from 'vitest';
import {
    ErrorResponseFromJSON,
    GetTransactionById200ResponseFromJSON,
    GetTransactionByMerchantTransactionId200ResponseFromJSON,
    PaymentRequestToJSON,
    StoredCredentialReasonTypeFromJSON,
    TransactionResponseFromJSON,
} from '../runtime/src/index';
import type {
    PendingTransactionResponse,
    TransactionGroupResponse,
    TransactionResponse,
} from '../runtime/src/index';
import { syntheticCardPayment } from './support/TestClients';

/**
 * Pinned probes of the generated core's serialization behaviour — the per-language trap
 * checklist every runtime runs before shipping (dotnet: optional-enum defect, FIXED by
 * template fork; java: oneOf multi-match throw, FIXED by template fork; php: merged
 * blob, benign). These tests PIN what the typescript-fetch core does today so any
 * change (regeneration, generator upgrade, template fork) is a visible diff here.
 */

const terminalBody = {
    transactionId: 'txn-synthetic-1',
    transactionStatus: 1,
    merchantTransactionId: 'mtx-synthetic-1',
    transactionType: 'charge',
    currency: 'USD',
    amount: 1999,
};

describe('union wrapper discrimination (fixed by the modelGeneric template fork)', () => {
    // Stock typescript-fetch emitted `return true` instanceOf checks for all-optional
    // models, so the group branch matched ANY object and terminal bodies came back
    // emptied. The fork (pipeline/typescript/config.yaml) requires at least one
    // declared property, so each branch now binds only its own shape. The runtime
    // reconciler still reads RAW bodies by design (repo rule 5) — these probes pin
    // the core's behaviour for direct consumers of the typed lookups.
    test('by-merchant-id wrapper: a terminal body binds TransactionResponse with data intact', () => {
        const bound = GetTransactionByMerchantTransactionId200ResponseFromJSON(
            terminalBody,
        ) as TransactionResponse;

        expect(bound.transactionId).toBe('txn-synthetic-1');
        expect(bound.transactionStatus).toBe(1);
        expect(bound.merchantTransactionId).toBe('mtx-synthetic-1');
        expect((bound as { transaction?: unknown }).transaction).toBeUndefined();
    });

    test('by-id wrapper: same correct binding', () => {
        const bound = GetTransactionById200ResponseFromJSON(terminalBody) as TransactionResponse;

        expect(bound.transactionId).toBe('txn-synthetic-1');
        expect(bound.transactionStatus).toBe(1);
    });

    test('the pending branch IS discriminated correctly (required `state` guard)', () => {
        const bound = GetTransactionByMerchantTransactionId200ResponseFromJSON({
            state: 'pending',
            merchantTransactionId: 'mtx-synthetic-1',
        }) as PendingTransactionResponse;

        expect(bound.state).toBe('pending');
        expect(bound.merchantTransactionId).toBe('mtx-synthetic-1');
    });

    test('a real group envelope binds the group branch with its transactions', () => {
        const bound = GetTransactionByMerchantTransactionId200ResponseFromJSON({
            transactions: [terminalBody],
        }) as TransactionGroupResponse;

        expect(bound.transactions).toHaveLength(1);
        expect(bound.transactions?.[0]?.transactionId).toBe('txn-synthetic-1');
    });
});

describe('optional-enum serialization (the dotnet-core defect does NOT reproduce here)', () => {
    test('an unset optional enum never reaches the wire body', () => {
        const request = syntheticCardPayment();
        // storedCredential (and its reasonType enum) deliberately unset.
        const wire = JSON.stringify(PaymentRequestToJSON(request));

        expect(wire).not.toContain('storedCredential');
        expect(wire).not.toContain('reasonType');
        expect(wire).not.toContain('cardType');
    });

    test('a set optional enum serializes verbatim', () => {
        const request = { ...syntheticCardPayment(), storedCredential: { reasonType: 'recurring' as const } };
        const wire = JSON.parse(JSON.stringify(PaymentRequestToJSON(request))) as {
            storedCredential: { reasonType: string };
        };

        expect(wire.storedCredential.reasonType).toBe('recurring');
    });
});

describe('open strings stay open (bake-off §A3: unknown wire values pass through verbatim)', () => {
    test('a standalone enum accepts a server-newer-than-spec value at runtime', () => {
        expect(StoredCredentialReasonTypeFromJSON('brand-new-reason')).toBe('brand-new-reason');
    });

    test('a nested unknown enum value survives response mapping', () => {
        const bound = TransactionResponseFromJSON({
            ...terminalBody,
            storedCredential: { reasonType: 'brand-new-reason' },
        });

        expect(bound.storedCredential?.reasonType).toBe('brand-new-reason');
    });

    test('ErrorResponse.code passes through verbatim — no coercion (unlike the php core)', () => {
        const bound = ErrorResponseFromJSON({ error: 'synthetic', code: 'never_seen_before' });

        expect(bound.code).toBe('never_seen_before');
    });

    test('transactionType is an open string', () => {
        const bound = TransactionResponseFromJSON({ ...terminalBody, transactionType: 'FutureOperation' });

        expect(bound.transactionType).toBe('FutureOperation');
    });
});
