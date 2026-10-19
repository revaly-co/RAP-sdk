/**
 * Synthetic wire bodies for the mock transport. SYNTHETIC DATA ONLY (ADR-SDK-020):
 * every identifier is an obvious placeholder and no real PAN/CVV/PII ever appears here.
 */

export const DEFAULT_MERCHANT_TRANSACTION_ID = 'mtx-synthetic-1';
export const DEFAULT_TRANSACTION_ID = 'txn-synthetic-1';
export const DEFAULT_CORRELATION_ID = 'corr-synthetic-1';
/**
 * The synthetic edge-firewall tracking reference carried by the edge-rejection row
 * (`details.reference`, the shape of the `x-azure-ref` header — ADR-SDK-033).
 */
export const EDGE_REFERENCE = '20261016T181449Z-synthetic0000000000000000000000';

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

/**
 * The edge firewall's block body (ADR-SDK-033): `details.edgeRejection: true` plus the
 * tracking reference; the production edge serves it as `text/html`.
 */
export function edgeRejectionBody(reference: string = EDGE_REFERENCE): string {
    return JSON.stringify({
        details: { edgeRejection: true, reference },
        error: 'synthetic: blocked by the edge firewall; did not reach the payment platform',
    });
}

/** The legacy edge HTML block page — not JSON, so no marker can be read. */
export function htmlBlockPage(): string {
    return '<html><head><title>403 Forbidden</title></head><body>synthetic edge block page</body></html>';
}
