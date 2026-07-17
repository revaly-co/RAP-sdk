<?php

declare(strict_types=1);

namespace Revaly\Sdk\Testing;

/**
 * Synthetic wire bodies for the mock transport. SYNTHETIC DATA ONLY (ADR-SDK-020):
 * every identifier is an obvious placeholder and no real PAN/CVV/PII ever appears here.
 */
final class SyntheticData
{
    public const DEFAULT_MERCHANT_TRANSACTION_ID = 'mtx-synthetic-1';
    public const DEFAULT_TRANSACTION_ID = 'txn-synthetic-1';
    public const DEFAULT_CORRELATION_ID = 'corr-synthetic-1';

    private function __construct()
    {
    }

    /** A terminal transaction record (`transactionStatus` 1=approved, 2=declined, 3=error). */
    public static function transaction(
        int $transactionStatus,
        string $merchantTransactionId = self::DEFAULT_MERCHANT_TRANSACTION_ID,
    ): string {
        return json_encode([
            'transactionId' => self::DEFAULT_TRANSACTION_ID,
            'transactionDate' => '2026-01-01T00:00:00Z',
            'transactionStatus' => $transactionStatus,
            'message' => 'synthetic outcome',
            'responseCode' => '00',
            'transactionType' => 'charge',
            'merchantTransactionId' => $merchantTransactionId,
            'currency' => 'USD',
            'amount' => 1999,
        ], JSON_THROW_ON_ERROR);
    }

    /** A pending intent record (post-P-2 shape; `state` is the discriminator). */
    public static function pending(
        string $merchantTransactionId = self::DEFAULT_MERCHANT_TRANSACTION_ID,
    ): string {
        return json_encode([
            'state' => 'pending',
            'merchantTransactionId' => $merchantTransactionId,
            'receivedAt' => '2026-01-01T00:00:00Z',
        ], JSON_THROW_ON_ERROR);
    }

    /** A grouped envelope (`include_all_transactions` shape). */
    public static function transactionGroup(
        string $merchantTransactionId = self::DEFAULT_MERCHANT_TRANSACTION_ID,
    ): string {
        return json_encode([
            'transactions' => [
                json_decode(self::transaction(1, $merchantTransactionId), true),
            ],
        ], JSON_THROW_ON_ERROR);
    }

    /** An ErrorResponse body; `code` is omitted when null (matching the wire contract). */
    public static function errorBody(string $error, ?string $code = null): string
    {
        $body = ['error' => $error];
        if ($code !== null) {
            $body['code'] = $code;
        }

        return json_encode($body, JSON_THROW_ON_ERROR);
    }
}
