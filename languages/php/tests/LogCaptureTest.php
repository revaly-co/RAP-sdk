<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Core\Model\CreditCard;
use Revaly\Sdk\Core\Model\PaymentMethod;
use Revaly\Sdk\Core\Model\PaymentRequest;
use Revaly\Sdk\Errors\OutcomeUnknownException;
use Revaly\Sdk\Errors\PermanentRejectionException;
use Revaly\Sdk\Logging\RapWireTrace;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Testing\SyntheticData;
use Revaly\Sdk\Tests\Support\CollectingLogger;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * The ADR-SDK-020 log-capture obligations (DX contract §c): default output is
 * values-free; debug level carries allowlist-scrubbed payloads only; the correlation id
 * is on every error path; the wire-trace hook never sees raw material.
 */
final class LogCaptureTest extends TestCase
{
    /** A charge request carrying synthetic card material that must never be logged. */
    private static function cardChargeRequest(): PaymentRequest
    {
        $card = new CreditCard();
        $card->setNumber(TestClients::SYNTHETIC_PAN);
        $card->setCardVerificationCode(TestClients::SYNTHETIC_CVV);

        $method = new PaymentMethod();
        $method->setCreditCard($card);

        $request = TestClients::chargeRequest();
        $request->setPaymentMethodType('creditCard');
        $request->setPaymentMethod($method);

        return $request;
    }

    public function testDefaultOutputIsValuesFreeOnSuccess(): void
    {
        $logger = new CollectingLogger();
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();

        TestClients::withMock($mock, logger: $logger)->charge(self::cardChargeRequest());

        $haystack = $logger->flattened();
        self::assertNotSame('', $haystack);
        self::assertStringNotContainsString(TestClients::SYNTHETIC_PAN, $haystack);
        self::assertStringNotContainsString(TestClients::API_KEY, $haystack);

        $info = $logger->atLevel('info');
        self::assertNotEmpty($info);
        self::assertSame('charge', $info[0]['context']['operation']);
        self::assertSame(200, $info[0]['context']['status']);
        self::assertSame(SyntheticData::DEFAULT_CORRELATION_ID, $info[0]['context']['correlation']);
    }

    public function testFailurePathLogsClassAndCorrelationOnly(): void
    {
        $logger = new CollectingLogger();
        $mock = new RapMockTransport();
        $mock->charge()->returnsPermanentRejection(422);

        try {
            TestClients::withMock($mock, logger: $logger)->charge(self::cardChargeRequest());
            self::fail('expected PermanentRejectionException');
        } catch (PermanentRejectionException $expected) {
        }

        $haystack = $logger->flattened();
        self::assertStringNotContainsString(TestClients::SYNTHETIC_PAN, $haystack);
        self::assertStringNotContainsString(TestClients::API_KEY, $haystack);

        $warnings = $logger->atLevel('warning');
        self::assertNotEmpty($warnings);
        self::assertSame('PermanentRejection', $warnings[0]['context']['class']);
        // Correlation id on every error path (DX contract §c).
        self::assertSame(SyntheticData::DEFAULT_CORRELATION_ID, $warnings[0]['context']['correlation']);
    }

    public function testDebugPayloadsAreScrubbed(): void
    {
        $logger = new CollectingLogger();
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();

        TestClients::withMock($mock, logger: $logger)->charge(self::cardChargeRequest());

        $debug = $logger->atLevel('debug');
        self::assertNotEmpty($debug);
        $request = (string) $debug[0]['context']['request'];
        self::assertStringContainsString('[scrubbed]', $request);
        self::assertStringContainsString('mtx-synthetic-1', $request);
        self::assertStringNotContainsString(TestClients::SYNTHETIC_PAN, $request);
    }

    public function testWireTraceHookReceivesOnlyScrubbedPayloads(): void
    {
        /** @var list<RapWireTrace> $traces */
        $traces = [];
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();

        TestClients::withMock(
            $mock,
            wireTraceHook: function (RapWireTrace $trace) use (&$traces): void {
                $traces[] = $trace;
            },
        )->charge(self::cardChargeRequest());

        self::assertCount(1, $traces);
        $trace = $traces[0];
        self::assertSame('charge', $trace->operation);
        self::assertSame('POST', $trace->method);
        self::assertSame(200, $trace->status);
        self::assertSame(SyntheticData::DEFAULT_CORRELATION_ID, $trace->correlationId);
        self::assertStringNotContainsString(TestClients::SYNTHETIC_PAN, (string) $trace->scrubbedRequestBody);
        self::assertStringContainsString('[scrubbed]', (string) $trace->scrubbedRequestBody);
        self::assertStringContainsString('mtx-synthetic-1', (string) $trace->scrubbedRequestBody);
    }

    public function testWireTraceHookExceptionsAreSwallowed(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();

        $transaction = TestClients::withMock(
            $mock,
            wireTraceHook: static function (): void {
                throw new \RuntimeException('observer bug');
            },
        )->charge(self::cardChargeRequest());

        // Tracing must never change payment control flow (runtime-tdd §6).
        self::assertSame(1, $transaction->getTransactionStatus());
    }

    public function testReconcileTraceCarriesScrubbedResponseOnly(): void
    {
        /** @var list<RapWireTrace> $traces */
        $traces = [];
        $mock = new RapMockTransport();
        $mock->reconcile(SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID)->returnsApproved();

        TestClients::withMock(
            $mock,
            wireTraceHook: function (RapWireTrace $trace) use (&$traces): void {
                $traces[] = $trace;
            },
        )->reconcile(
            SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID,
            new \Revaly\Sdk\Reconcile\ReconcilePolicy(1, 5.0, 0.0),
        );

        self::assertCount(1, $traces);
        self::assertSame('reconcile', $traces[0]->operation);
        self::assertStringContainsString('[scrubbed]', (string) $traces[0]->scrubbedResponseBody);
        self::assertStringContainsString('mtx-synthetic-1', (string) $traces[0]->scrubbedResponseBody);
    }

    public function testTransportFailureLogsNeverContainTheApiKey(): void
    {
        $logger = new CollectingLogger();
        $mock = new RapMockTransport();
        $mock->charge()->throwsTimeoutAfterSend();

        try {
            TestClients::withMock($mock, logger: $logger)->charge(self::cardChargeRequest());
            self::fail('expected OutcomeUnknownException');
        } catch (OutcomeUnknownException $expected) {
        }

        self::assertStringNotContainsString(TestClients::API_KEY, $logger->flattened());
    }
}
