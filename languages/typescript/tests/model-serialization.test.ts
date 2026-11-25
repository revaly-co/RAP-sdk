import { describe, expect, test } from 'vitest';
import {
    ErrorResponseFromJSON,
    GetTransactionById200ResponseFromJSON,
    GetTransactionByMerchantTransactionId200ResponseFromJSON,
    instanceOfTransactionListItem,
    instanceOfTransactionListPaymentMethodItem,
    ListTransactions200ResponseInnerFromJSON,
    PaymentRequestToJSON,
    RapMockTransport,
    StoredCredentialReasonTypeFromJSON,
    TransactionResponseFromJSON,
} from '../runtime/src/index';
import type {
    PendingTransactionResponse,
    TransactionGroupResponse,
    TransactionListItem,
    TransactionListPaymentMethodItem,
    TransactionResponse,
} from '../runtime/src/index';
import { mockedClient, syntheticCardPayment } from './support/TestClients';

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

const flatListRow = {
    transactionId: 't-1',
    transactionDate: '2025-09-13T03:19:54.86Z',
    transactionStatus: 1,
    responseCode: '10000',
    transactionType: 'Charge',
    amount: 2500,
    currencyCode: 'USD',
};

const paymentMethodListRow = {
    transaction: {
        transactionId: 't-2',
        transactionDate: '2025-12-02T14:44:42.209Z',
        transactionStatus: 1,
        message: 'Succeeded!',
        responseCode: '10000',
        transactionType: 'CreateCreditCard',
        paymentMethod: {
            paymentMethodId: 'pm-1',
            lastFourDigits: '1111',
            firstSixDigits: '411111',
            cardType: 'VISA',
            storageState: 'Cached',
            issuerIdentificationNumber: '41111111',
        },
    },
};

describe('listTransactions item wrapper (oneOf TransactionListItem | TransactionListPaymentMethodItem)', () => {
    // Stock typescript-fetch oneOf: the first branch whose required-field instanceOf
    // guard matches wins (TransactionListItem requires `transactionId`,
    // TransactionListPaymentMethodItem requires `transaction`); no branch matching
    // yields `{}`.
    test('a flat row binds TransactionListItem with its fields readable', () => {
        const bound = ListTransactions200ResponseInnerFromJSON(flatListRow);

        expect(instanceOfTransactionListItem(bound)).toBe(true);
        expect(instanceOfTransactionListPaymentMethodItem(bound)).toBe(false);
        const item = bound as TransactionListItem;
        expect(item.transactionId).toBe('t-1');
        expect(item.transactionDate?.toISOString()).toBe('2025-09-13T03:19:54.860Z');
        expect(item.transactionStatus).toBe(1);
        expect(item.responseCode).toBe('10000');
        expect(item.transactionType).toBe('Charge');
        expect(item.amount).toBe(2500);
        expect(item.currencyCode).toBe('USD');
    });

    test('a payment-method row binds TransactionListPaymentMethodItem with the nested card readable', () => {
        const bound = ListTransactions200ResponseInnerFromJSON(paymentMethodListRow);

        expect(instanceOfTransactionListPaymentMethodItem(bound)).toBe(true);
        expect(instanceOfTransactionListItem(bound)).toBe(false);
        const item = bound as TransactionListPaymentMethodItem;
        expect(item.transaction.transactionId).toBe('t-2');
        expect(item.transaction.transactionDate.toISOString()).toBe('2025-12-02T14:44:42.209Z');
        expect(item.transaction.transactionType).toBe('CreateCreditCard');
        expect(item.transaction.paymentMethod?.paymentMethodId).toBe('pm-1');
        expect(item.transaction.paymentMethod?.lastFourDigits).toBe('1111');
        expect(item.transaction.paymentMethod?.firstSixDigits).toBe('411111');
    });

    test('a flat row with an unknown additive field still binds TransactionListItem', () => {
        const bound = ListTransactions200ResponseInnerFromJSON({ ...flatListRow, futureAdditiveField: 'x' });

        expect(instanceOfTransactionListItem(bound)).toBe(true);
        expect(instanceOfTransactionListPaymentMethodItem(bound)).toBe(false);
        expect((bound as TransactionListItem).transactionId).toBe('t-1');
    });

    test('a payment-method row with an unknown additive field still binds TransactionListPaymentMethodItem', () => {
        const bound = ListTransactions200ResponseInnerFromJSON({ ...paymentMethodListRow, futureAdditiveField: 'x' });

        expect(instanceOfTransactionListPaymentMethodItem(bound)).toBe(true);
        expect(instanceOfTransactionListItem(bound)).toBe(false);
        expect((bound as TransactionListPaymentMethodItem).transaction.paymentMethod?.lastFourDigits).toBe('1111');
    });

    test('a row of neither shape does not masquerade as TransactionListItem: it maps to {}', () => {
        const bound = ListTransactions200ResponseInnerFromJSON({
            transactionDate: '2025-09-13T03:19:54.86Z',
            transactionStatus: 1,
            responseCode: '10000',
        });

        expect(instanceOfTransactionListItem(bound)).toBe(false);
        expect(instanceOfTransactionListPaymentMethodItem(bound)).toBe(false);
        expect(bound).toEqual({});
    });

    test('listTransactions through the mock transport decodes each row to its own branch', async () => {
        const mock = new RapMockTransport();
        mock.stub('GET', '/transactions').returns(200, JSON.stringify([flatListRow, paymentMethodListRow]));

        const rows = await mockedClient(mock).transactions.listTransactions();

        expect(rows).toHaveLength(2);
        expect(instanceOfTransactionListItem(rows[0] as object)).toBe(true);
        expect((rows[0] as TransactionListItem).transactionId).toBe('t-1');
        expect(instanceOfTransactionListPaymentMethodItem(rows[1] as object)).toBe(true);
        expect(instanceOfTransactionListItem(rows[1] as object)).toBe(false);
        expect((rows[1] as TransactionListPaymentMethodItem).transaction.paymentMethod?.lastFourDigits).toBe('1111');
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
