<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Core\Model\CaptureRequest;
use Revaly\Sdk\Core\Model\PaymentRequest;
use Revaly\Sdk\Core\Model\PendingTransactionResponse;
use Revaly\Sdk\Core\Model\RefundCancelRequest;
use Revaly\Sdk\Core\ObjectSerializer;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Testing\SyntheticData;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * ADR-SDK-034 (OQ-18, SC-886): the SDK never refuses a request because a model field is
 * longer than the spec's maxLength; the platform decides (it truncates a description over
 * 256 characters, and records or refuses other bounds). The forked model_generic.mustache
 * drops the stock maxLength checks from the setters and listInvalidProperties(). The
 * amendment of 2026-11-26 (SC-1018, OQ-19) adds the rtnData block: there the setters
 * neither refuse a value that breaks a documented pattern, minimum or minLength nor replace
 * an unlisted value (RtnDataValuesTest). Every other check stays: required fields and
 * non-null guards, the patterns, minimums, minLengths and value-list coercions outside
 * rtnData, and the API layer's path-parameter bounds.
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

    public function testPatternOutsideRtnDataIsStillRefused(): void
    {
        // SC-1018 (D5): the kept pattern check, on a field outside rtnData (^[A-Z]{3}$). A
        // change that removes checks beyond lib/Model/RtnData*.php fails here. The rtnData
        // pattern case this test held before moved to RtnDataValuesTest, where it is sent.
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('must conform to the pattern');
        TestClients::chargeRequest()->setCurrency('usd');
    }

    public function testMinimumOutsideRtnDataIsStillRefused(): void
    {
        // SC-1018 (X1): the kept minimum check outside rtnData (amount, minimum 0).
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('must be bigger than or equal to 0');
        TestClients::chargeRequest()->setAmount(-1);
    }

    public function testMinLengthOutsideRtnDataIsStillRefused(): void
    {
        // SC-1018 (X1): the kept minLength check outside rtnData (customerId, minLength 1).
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('must be bigger than or equal to 1');
        (new RefundCancelRequest())->setCustomerId('');
    }

    public function testListInvalidPropertiesOutsideRtnDataStillReportsTheRules(): void
    {
        // SC-1018 (X1): the array constructor runs no check, so listInvalidProperties() is
        // where these rules read a model built that way; outside rtnData they all stay.
        $payment = new PaymentRequest([
            'amount' => -1,
            'merchant_transaction_id' => SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID,
            'currency' => 'usd',
            'payment_method_type' => 'unlisted_synthetic_value',
        ]);
        $refundCancel = new RefundCancelRequest([
            'merchant_transaction_id' => SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID,
            'customer_id' => '',
        ]);

        $invalid = $payment->listInvalidProperties();
        self::assertContains('invalid value for \'amount\', must be bigger than or equal to 0.', $invalid);
        self::assertContains('invalid value for \'currency\', must be conform to the pattern /^[A-Z]{3}$/.', $invalid);
        self::assertCount(1, preg_grep('/^invalid value \'unlisted_synthetic_value\' for \'payment_method_type\', must be one of /', $invalid));
        self::assertFalse($payment->valid());
        self::assertContains(
            'invalid value for \'customer_id\', the character length must be bigger than or equal to 1.',
            $refundCancel->listInvalidProperties(),
        );
    }

    public function testUnlistedValueOutsideRtnDataStillReadsBackTheSentinel(): void
    {
        // SC-1018 (X1): the open-vocabulary coercion stays outside rtnData (bake-off §A3), the
        // request-side twin of ModelSerializationTest's ErrorResponse code pin.
        $request = TestClients::chargeRequest();
        $request->setPaymentMethodType('unlisted_synthetic_value');

        self::assertSame(PaymentRequest::PAYMENT_METHOD_TYPE_UNKNOWN_DEFAULT_OPEN_API, $request->getPaymentMethodType());
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
