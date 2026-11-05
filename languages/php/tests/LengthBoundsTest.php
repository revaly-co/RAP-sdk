<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Core\Model\CaptureRequest;
use Revaly\Sdk\Core\Model\PendingTransactionResponse;
use Revaly\Sdk\Core\Model\RtnDataAdditionalTransactionData;
use Revaly\Sdk\Core\ObjectSerializer;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * ADR-SDK-034 (OQ-18, SC-886): the SDK never refuses a request because a model field is
 * longer than the spec's maxLength; the platform decides (it truncates a description over
 * 256 characters, and records or refuses other bounds). The forked model_generic.mustache
 * drops the stock maxLength checks from the setters and listInvalidProperties(). Every
 * other check stays: required fields, patterns, and the API layer's path-parameter bounds.
 */
final class LengthBoundsTest extends TestCase
{
    private const LONG_DESCRIPTION_LENGTH = 300; // spec maxLength 256
    private const LONG_CUSTOMER_IP_LENGTH = 50;  // spec maxLength 45; the direct path accepts 50

    public function testOverLongFieldsAreSentWhole(): void
    {
        // AC2: setDescription() was where the bound fired.
        $description = str_repeat('d', self::LONG_DESCRIPTION_LENGTH);
        $customerIp = str_repeat('i', self::LONG_CUSTOMER_IP_LENGTH);
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        $request = TestClients::chargeRequest();
        $request->setDescription($description);
        $request->setCustomerIp($customerIp);

        TestClients::withMock($mock)->charge($request);

        $body = json_decode($mock->getRequests()[0]->body, true, 512, JSON_THROW_ON_ERROR);
        self::assertSame($description, $body['description']);
        self::assertSame($customerIp, $body['customerIp']);
        self::assertSame([], $request->listInvalidProperties());
    }

    public function testResponseWithAnOverLongFieldStillBinds(): void
    {
        // A processed payment must never surface as a parse error over a length bound.
        $long = str_repeat('m', 150);
        $parsed = ObjectSerializer::deserialize(
            json_decode(json_encode(['state' => 'pending', 'merchantTransactionId' => $long])),
            PendingTransactionResponse::class,
        );

        self::assertSame($long, $parsed->getMerchantTransactionId());
    }

    public function testExplicitNullOnARequiredFieldIsStillRefused(): void
    {
        // AC3: the setter's non-null guard on a required field is kept. A required field that
        // is never set was not refused before this change either (nothing calls valid()); the
        // platform answers that one, unchanged.
        $this->expectException(\InvalidArgumentException::class);
        TestClients::chargeRequest()->setMerchantTransactionId(null);
    }

    public function testPatternViolationIsStillRefused(): void
    {
        // AC3: the pattern check is kept (this pattern also caps the value at 128).
        $this->expectException(\InvalidArgumentException::class);
        (new RtnDataAdditionalTransactionData())->setFraudPreventionPlatform('not allowed!');
    }

    public function testOverLongPathParameterIsStillRefusedBeforeSending(): void
    {
        // AC3: the API layer's path-parameter bound (transactionId at 50) is unchanged.
        $mock = new RapMockTransport();
        $refused = null;
        try {
            TestClients::withMock($mock)->capture(str_repeat('t', 51), new CaptureRequest());
        } catch (\Throwable $e) {
            $refused = $e;
        }

        self::assertNotNull($refused, 'an over-long path parameter must be refused');
        self::assertSame([], $mock->getRequests());
    }
}
