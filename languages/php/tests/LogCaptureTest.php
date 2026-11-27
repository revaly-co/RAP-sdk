<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Core\Model\CreditCard;
use Revaly\Sdk\Core\Model\PaymentMethod;
use Revaly\Sdk\Core\Model\PaymentRequest;
use Revaly\Sdk\Core\Model\RtnData;
use Revaly\Sdk\Core\Model\RtnDataAdditionalTransactionData;
use Revaly\Sdk\Core\Model\RtnDataCustomerData;
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
    private const SYNTHETIC_EMAIL = 'customer@synthetic.test';

    /**
     * PCI DSS lets a PAN be shown with at most its first six and last four digits, so seven
     * digits of the test number in a row (space or dash separators dropped) show more than any
     * permitted rendering. It catches a value cut below the 15 characters the prefix needle
     * covers; six would flag the six-digit BIN that PCI permits.
     */
    private const PAN_DIGIT_WINDOW = 7;

    /** How many digit runs in $haystack hold PAN_DIGIT_WINDOW digits of the test number in a row. */
    private static function panDigitRuns(string $haystack): int
    {
        $pan = TestClients::SYNTHETIC_PAN;
        $windows = [];
        for ($i = 0; $i + self::PAN_DIGIT_WINDOW <= strlen($pan); $i++) {
            $windows[] = substr($pan, $i, self::PAN_DIGIT_WINDOW);
        }
        $windows = array_values(array_unique($windows));
        preg_match_all('/\d(?:[ -]?\d)*/', $haystack, $runs);
        $hits = 0;
        foreach ($runs[0] as $run) {
            $digits = str_replace([' ', '-'], '', $run);
            foreach ($windows as $window) {
                if (str_contains($digits, $window)) {
                    $hits++;
                    break;
                }
            }
        }

        return $hits;
    }

    /** @return array<string, array{string}> */
    public static function rtnDataOperations(): array
    {
        return ['charge' => ['charge'], 'authorize' => ['authorize']];
    }

    #[DataProvider('rtnDataOperations')]
    public function testRtnDataCardMaterialIsSentButNeverLoggedOrTraced(string $operation): void
    {
        // SC-1018 (AppSec M1): once the setters send rtnData values as given, a malformed
        // fullPan set through the public setter reaches the runtime, and the key-based
        // scrubber is the only control on that path. Set through the setter (never the array
        // constructor), so the request reaches the wire only when the core sends the value.
        // The documentation test number, in the spaced form that breaks the fullPan pattern.
        $spacedPan = implode(' ', str_split(TestClients::SYNTHETIC_PAN, 4));
        $transaction = new RtnDataAdditionalTransactionData();
        $transaction->setFullPan($spacedPan);
        $customer = new RtnDataCustomerData();
        $customer->setEmail(self::SYNTHETIC_EMAIL);
        $rtnData = new RtnData();
        $rtnData->setAdditionalTransactionData($transaction);
        $rtnData->setCustomerData($customer);

        $logger = new CollectingLogger();
        /** @var list<RapWireTrace> $traces */
        $traces = [];
        $mock = new RapMockTransport();
        $client = TestClients::withMock(
            $mock,
            logger: $logger,
            wireTraceHook: function (RapWireTrace $trace) use (&$traces): void {
                $traces[] = $trace;
            },
        );
        if ($operation === 'charge') {
            $mock->charge()->returnsApproved();
            $request = TestClients::chargeRequest();
            $request->setRtnData($rtnData);
            $client->charge($request);
        } else {
            $mock->authorize()->returnsApproved();
            $request = TestClients::authorizeRequest();
            $request->setRtnData($rtnData);
            $client->authorize($request);
        }

        // The wire carries the value as given ...
        $sent = json_decode($mock->getRequests()[0]->body, true, 512, JSON_THROW_ON_ERROR)['rtnData'];
        self::assertSame($spacedPan, $sent['additionalTransactionData']['fullPan']);
        self::assertSame(self::SYNTHETIC_EMAIL, $sent['customerData']['email']);

        // ... the debug payload and the trace carry it only as [scrubbed] ...
        $debug = $logger->atLevel('debug');
        self::assertNotEmpty($debug);
        self::assertCount(1, $traces);
        foreach ([(string) $debug[0]['context']['request'], (string) $traces[0]->scrubbedRequestBody] as $scrubbed) {
            $scrubbedRtnData = json_decode($scrubbed, true, 512, JSON_THROW_ON_ERROR)['rtnData'];
            self::assertSame('[scrubbed]', $scrubbedRtnData['additionalTransactionData']['fullPan']);
            self::assertSame('[scrubbed]', $scrubbedRtnData['customerData']['email']);
        }

        // ... and no record or trace holds the value, its digit run or its 15-character prefix.
        $haystack = implode("\n", [
            $logger->flattened(),
            (string) $traces[0]->scrubbedRequestBody,
            (string) $traces[0]->scrubbedResponseBody,
        ]);
        foreach ([$spacedPan, substr($spacedPan, 0, 15), TestClients::SYNTHETIC_PAN, self::SYNTHETIC_EMAIL, TestClients::API_KEY] as $needle) {
            self::assertStringNotContainsString($needle, $haystack);
        }
        // The haystack renders each Throwable in log context in full (CollectingLogger), and no
        // part of it holds seven digits of the test number in a row, the shape a value cut
        // below 15 characters leaves.
        self::assertSame(0, self::panDigitRuns($haystack), 'seven digits of the test number in a row were logged');
    }

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
