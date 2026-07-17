<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Logging\RapScrubber;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * The central allowlist scrubber (ADR-SDK-020): only known-safe fields pass; everything
 * else — including every field the schema might grow tomorrow — fails safe to
 * `[scrubbed]`.
 */
final class ScrubberTest extends TestCase
{
    public function testPanAndCvvNeverSurvive(): void
    {
        $payload = json_encode([
            'amount' => 1999,
            'currency' => 'USD',
            'merchantTransactionId' => 'mtx-synthetic-1',
            'paymentMethod' => [
                'creditCard' => [
                    'cardNumber' => TestClients::SYNTHETIC_PAN,
                    'cvv' => TestClients::SYNTHETIC_CVV,
                    'cardholderName' => 'SYNTHETIC CARDHOLDER',
                ],
            ],
        ]);

        $scrubbed = RapScrubber::scrubJson($payload);

        self::assertStringNotContainsString(TestClients::SYNTHETIC_PAN, $scrubbed);
        self::assertStringNotContainsString(TestClients::SYNTHETIC_CVV, $scrubbed);
        self::assertStringNotContainsString('SYNTHETIC CARDHOLDER', $scrubbed);
        // Allowlisted identifiers pass verbatim; structure is preserved.
        self::assertStringContainsString('"merchantTransactionId":"mtx-synthetic-1"', $scrubbed);
        self::assertStringContainsString('"currency":"USD"', $scrubbed);
        self::assertStringContainsString('"cardNumber":"[scrubbed]"', $scrubbed);
        // Amounts are NOT on the allowlist.
        self::assertStringNotContainsString('1999', $scrubbed);
    }

    public function testUnknownFieldsFailSafe(): void
    {
        // Schema evolution: a field added tomorrow is scrubbed by default.
        $scrubbed = RapScrubber::scrubJson('{"fieldAddedTomorrow":"sensitive-value","status":"ok"}');

        self::assertStringNotContainsString('sensitive-value', $scrubbed);
        self::assertStringContainsString('"status":"ok"', $scrubbed);
    }

    public function testArraysInheritTheirParentKeyStatus(): void
    {
        $scrubbed = RapScrubber::scrubJson(json_encode([
            'transactions' => [
                ['transactionId' => 'txn-synthetic-1', 'amount' => 5],
            ],
            'notes' => ['a secret note'],
        ]));

        self::assertStringContainsString('"transactionId":"txn-synthetic-1"', $scrubbed);
        self::assertStringNotContainsString('a secret note', $scrubbed);
        self::assertStringNotContainsString(':5', $scrubbed);
    }

    public function testNonJsonInputNeverLeaksRawText(): void
    {
        self::assertSame('[unparseable:scrubbed]', RapScrubber::scrubJson('PAN 4111111111111111 inline'));
        self::assertSame('', RapScrubber::scrubJson(''));
        self::assertSame('', RapScrubber::scrubJson(null));
    }

    public function testHeaderScrubRedactsEverythingOffTheAllowlist(): void
    {
        $scrubbed = RapScrubber::scrubHeaders([
            'Authorization' => ['ApiKey ' . TestClients::API_KEY],
            'Content-Type' => ['application/json'],
            'X-Correlation-ID' => ['corr-synthetic-1'],
            'X-Internal-Routing' => ['secret-target'],
            'User-Agent' => ['revaly-sdk-php/0.0.0 (php 8.3; linux)', 'merchant-app/2.0'],
        ]);

        self::assertSame(RapScrubber::REDACTED, $scrubbed['Authorization']);
        self::assertStringNotContainsString(TestClients::API_KEY, json_encode($scrubbed) ?: '');
        self::assertSame('application/json', $scrubbed['Content-Type']);
        self::assertSame('corr-synthetic-1', $scrubbed['X-Correlation-ID']);
        self::assertSame(RapScrubber::REDACTED, $scrubbed['X-Internal-Routing']);
        // User-Agent joins with spaces (product-token list), not commas.
        self::assertSame(
            'revaly-sdk-php/0.0.0 (php 8.3; linux) merchant-app/2.0',
            $scrubbed['User-Agent'],
        );
    }

    public function testFieldAllowlistIsCaseInsensitive(): void
    {
        $scrubbed = RapScrubber::scrubJson('{"MerchantTransactionID":"mtx-1","AMOUNT":9}');

        self::assertStringContainsString('"MerchantTransactionID":"mtx-1"', $scrubbed);
        self::assertStringNotContainsString('9', $scrubbed);
    }
}
