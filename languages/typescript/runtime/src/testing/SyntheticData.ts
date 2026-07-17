/**
 * Synthetic wire bodies for the mock transport. SYNTHETIC DATA ONLY (ADR-SDK-020):
 * every identifier is an obvious placeholder and no real PAN/CVV/PII ever appears here.
 */

export const DEFAULT_MERCHANT_TRANSACTION_ID = 'mtx-synthetic-1';
export const DEFAULT_TRANSACTION_ID = 'txn-synthetic-1';
export const DEFAULT_CORRELATION_ID = 'corr-synthetic-1';

/** A terminal transaction record (`transactionStatus` 1=approved, 2=declined, 3=error). */
export function transaction(
    transactionStatus: number,
    merchantTransactionId: string = DEFAULT_MERCHANT_TRANSACTION_ID,
): string {
    return JSON.stringify({
        transactionId: DEFAULT_TRANSACTION_ID,
        transactionDate: '2026-01-01T00:00:00Z',
        transactionStatus,
        message: 'synthetic outcome',
        responseCode: '00',
        transactionType: 'charge',
        merchantTransactionId,
        currency: 'USD',
        amount: 1999,
    });
}

/** A pending intent record (post-P-2 shape; `state` is the discriminator). */
export function pending(merchantTransactionId: string = DEFAULT_MERCHANT_TRANSACTION_ID): string {
    return JSON.stringify({
        state: 'pending',
        merchantTransactionId,
        receivedAt: '2026-01-01T00:00:00Z',
    });
}

/** A grouped envelope (`includeAllTransactions` shape). */
export function transactionGroup(merchantTransactionId: string = DEFAULT_MERCHANT_TRANSACTION_ID): string {
    return JSON.stringify({
        transactions: [JSON.parse(transaction(1, merchantTransactionId))],
    });
}

/** An ErrorResponse body; `code` is omitted when absent (matching the wire contract). */
export function errorBody(error: string, code?: string): string {
    return JSON.stringify(code === undefined ? { error } : { error, code });
}
