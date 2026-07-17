<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests\Support;

use Psr\Log\LoggerInterface;
use Revaly\Sdk\Core\Model\PaymentRequest;
use Revaly\Sdk\RapClient;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Testing\SyntheticData;

/** Shared fixtures. Synthetic values only (ADR-SDK-020). */
final class TestClients
{
    public const API_KEY = 'sk-synthetic-test-key';

    /** A PAN that must never appear in any log or trace. */
    public const SYNTHETIC_PAN = '4111111111111111';
    public const SYNTHETIC_CVV = '9987';

    private function __construct()
    {
    }

    public static function withMock(
        RapMockTransport $mock,
        ?LoggerInterface $logger = null,
        ?callable $wireTraceHook = null,
        string $apiVersion = '2.1',
        ?string $userAgentSuffix = null,
    ): RapClient {
        return new RapClient(
            apiKey: self::API_KEY,
            baseUrl: 'https://sandbox.synthetic.test',
            apiVersion: $apiVersion,
            logger: $logger,
            wireTraceHook: $wireTraceHook,
            transport: $mock,
            userAgentSuffix: $userAgentSuffix,
        );
    }

    /** A minimal charge request (required fields only). */
    public static function chargeRequest(): PaymentRequest
    {
        $request = new PaymentRequest();
        $request->setAmount(1999);
        $request->setMerchantTransactionId(SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID);
        $request->setCurrency('USD');

        return $request;
    }
}
