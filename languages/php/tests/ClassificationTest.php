<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Errors\OutcomeUnknownException;
use Revaly\Sdk\Errors\PermanentRejectionException;
use Revaly\Sdk\Errors\RapCoreException;
use Revaly\Sdk\Errors\RapFailureClass;
use Revaly\Sdk\Errors\TransientFailureException;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Testing\SyntheticData;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * Every row of the failover-contract §2 table, end to end through the client, the
 * generated core, and the classification middleware — the normative algorithm, pinned.
 */
final class ClassificationTest extends TestCase
{
    /** @return iterable<string, array{int}> */
    public static function permanentRejectionStatuses(): iterable
    {
        yield '400' => [400];
        yield '401' => [401];
        yield '403' => [403];
        yield '404' => [404];
        yield '422' => [422];
    }

    #[DataProvider('permanentRejectionStatuses')]
    public function testPermanentRejectionStatuses(int $status): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsPermanentRejection($status);
        $client = TestClients::withMock($mock);

        try {
            $client->charge(TestClients::chargeRequest());
            self::fail('expected PermanentRejectionException');
        } catch (PermanentRejectionException $e) {
            self::assertSame(RapFailureClass::PermanentRejection, $e->getFailureClass());
            self::assertSame($status, $e->getStatusCode());
            self::assertSame(SyntheticData::DEFAULT_CORRELATION_ID, $e->getCorrelationId());
            self::assertSame('synthetic rejection', $e->getApiError());
            self::assertNotNull($e->getRawBody());
        }
    }

    public function testNotProcessed503IsTransientFailure(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsNotProcessed503();
        $client = TestClients::withMock($mock);

        try {
            $client->charge(TestClients::chargeRequest());
            self::fail('expected TransientFailureException');
        } catch (TransientFailureException $e) {
            self::assertSame(RapFailureClass::TransientFailure, $e->getFailureClass());
            self::assertSame(503, $e->getStatusCode());
            self::assertSame('not_processed', $e->getErrorCode());
            self::assertSame(SyntheticData::DEFAULT_CORRELATION_ID, $e->getCorrelationId());
        }
    }

    public function testBare503IsOutcomeUnknown(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsBare503();
        $client = TestClients::withMock($mock);

        $this->expectException(OutcomeUnknownException::class);
        $client->charge(TestClients::chargeRequest());
    }

    public function testUnknownCode503IsTreatedAsAbsentButCarriedVerbatim(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsUnknownCode503('brand_new_code_from_oq2');
        $client = TestClients::withMock($mock);

        try {
            $client->charge(TestClients::chargeRequest());
            self::fail('expected OutcomeUnknownException');
        } catch (OutcomeUnknownException $e) {
            // Unrecognized code = absent for CLASSIFICATION, but carried verbatim on
            // the typed error (open string — repo rule 5).
            self::assertSame('brand_new_code_from_oq2', $e->getErrorCode());
        }
    }

    /** @return iterable<string, array{string}> */
    public static function outcomeUnknownResponseScenarios(): iterable
    {
        yield '500' => ['returnsServerError'];
        yield '502' => ['returnsBadGateway'];
        yield '504' => ['returnsGatewayTimeout'];
    }

    #[DataProvider('outcomeUnknownResponseScenarios')]
    public function testServerErrorStatusesAreOutcomeUnknown(string $scenario): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->{$scenario}();
        $client = TestClients::withMock($mock);

        $this->expectException(OutcomeUnknownException::class);
        $client->charge(TestClients::chargeRequest());
    }

    public function testStatusOutsideTheTableIsOutcomeUnknown(): void
    {
        // 409 is not in the §2 table — ambiguous statuses classify conservatively.
        $mock = new RapMockTransport();
        $mock->charge()->returns(409, SyntheticData::errorBody('conflict'));
        $client = TestClients::withMock($mock);

        $this->expectException(OutcomeUnknownException::class);
        $client->charge(TestClients::chargeRequest());
    }

    /** @return iterable<string, array{string}> */
    public static function neverSentScenarios(): iterable
    {
        yield 'connection refused (errno 7)' => ['throwsConnectionRefused'];
        yield 'dns failure (errno 6)' => ['throwsDnsFailure'];
        yield 'tls handshake (errno 35)' => ['throwsSslHandshakeFailure'];
    }

    #[DataProvider('neverSentScenarios')]
    public function testProvablyNeverSentIsTransientFailure(string $scenario): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->{$scenario}();
        $client = TestClients::withMock($mock);

        try {
            $client->charge(TestClients::chargeRequest());
            self::fail('expected TransientFailureException');
        } catch (TransientFailureException $e) {
            self::assertNull($e->getStatusCode());
            self::assertStringContainsString('never sent', $e->getMessage());
        }
    }

    /** @return iterable<string, array{string}> */
    public static function ambiguousTransportScenarios(): iterable
    {
        // errno 28 covers connect-phase AND after-send timeouts — curl cannot prove
        // never-sent on a timeout, so BOTH are conservative (unlike runtimes whose
        // stack types the connect timeout distinctly).
        yield 'timeout after send (errno 28)' => ['throwsTimeoutAfterSend'];
        yield 'connect timeout (errno 28)' => ['throwsConnectTimeout'];
        yield 'reset mid-flight (errno 56)' => ['throwsConnectionReset'];
    }

    #[DataProvider('ambiguousTransportScenarios')]
    public function testAmbiguousTransportFailuresAreOutcomeUnknown(string $scenario): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->{$scenario}();
        $client = TestClients::withMock($mock);

        $this->expectException(OutcomeUnknownException::class);
        $client->charge(TestClients::chargeRequest());
    }

    public function testTransportFailureWithoutErrnoIsOutcomeUnknown(): void
    {
        // A rejection with no structured errno carries no never-sent proof.
        $mock = new RapMockTransport();
        $mock->charge()->throwsIo(new \RuntimeException('synthetic: ambiguous transport failure'));
        $client = TestClients::withMock($mock);

        $this->expectException(OutcomeUnknownException::class);
        $client->charge(TestClients::chargeRequest());
    }

    public function testVersion20PinDoesNotHonorNotProcessed(): void
    {
        // On "2.0" the code field is not part of the documented contract: 503 +
        // not_processed falls through to OutcomeUnknown (runtime-tdd §1 [Decided]).
        $mock = new RapMockTransport();
        $mock->charge()->returnsNotProcessed503();
        $client = TestClients::withMock($mock, apiVersion: '2.0');

        $this->expectException(OutcomeUnknownException::class);
        $client->charge(TestClients::chargeRequest());
    }

    public function testUnreadable200ClassifiesOutcomeUnknown(): void
    {
        // The core's standalone-enum deserialize edge (generator-bakeoff §A3): a valid
        // 200 whose storedCredential.reasonType carries a server-newer-than-spec value
        // throws inside the generated deserializer. The response was received, so the
        // outcome is unknowable locally — OutcomeUnknown; reconcile resolves it.
        $body = json_decode(SyntheticData::transaction(1), true);
        $body['storedCredential'] = ['reasonType' => 'brand_new_reason_from_a_newer_spec'];

        $mock = new RapMockTransport();
        $mock->charge()->returns(200, json_encode($body, JSON_THROW_ON_ERROR));
        $client = TestClients::withMock($mock);

        try {
            $client->charge(TestClients::chargeRequest());
            self::fail('expected OutcomeUnknownException');
        } catch (OutcomeUnknownException $e) {
            self::assertStringContainsString('unreadable by this SDK version', $e->getMessage());
            self::assertCount(1, $mock->getRequests());
        }
    }

    public function testPreSendValidationFailureIsACallerErrorNotAnOutcome(): void
    {
        // The core rejects an over-long transactionId BEFORE dispatch — that must stay
        // an InvalidArgumentException (fix your code), never a payment outcome.
        $mock = new RapMockTransport();
        $client = TestClients::withMock($mock);

        try {
            $client->capture(str_repeat('x', 51), new \Revaly\Sdk\Core\Model\CaptureRequest());
            self::fail('expected InvalidArgumentException');
        } catch (\InvalidArgumentException $e) {
            self::assertNotInstanceOf(RapCoreException::class, $e);
            self::assertCount(0, $mock->getRequests());
        }
    }

    public function testSuccessReturnsTransactionResponse(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        $client = TestClients::withMock($mock);

        $transaction = $client->charge(TestClients::chargeRequest());

        self::assertSame(SyntheticData::DEFAULT_TRANSACTION_ID, $transaction->getTransactionId());
        self::assertSame(1, $transaction->getTransactionStatus());
        self::assertSame(SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID, $transaction->getMerchantTransactionId());
    }

    public function testApiKeyNeverAppearsInExceptionMessages(): void
    {
        $scenarios = [
            static function (RapMockTransport $mock): void {
                $mock->charge()->returnsPermanentRejection(401);
            },
            static function (RapMockTransport $mock): void {
                $mock->charge()->returnsNotProcessed503();
            },
            static function (RapMockTransport $mock): void {
                $mock->charge()->throwsConnectionRefused();
            },
            static function (RapMockTransport $mock): void {
                $mock->charge()->returnsServerError();
            },
        ];

        foreach ($scenarios as $script) {
            $mock = new RapMockTransport();
            $script($mock);
            $client = TestClients::withMock($mock);
            try {
                $client->charge(TestClients::chargeRequest());
                self::fail('expected a typed failure');
            } catch (RapCoreException $e) {
                // ADR-SDK-020: API keys never appear in exception messages.
                self::assertStringNotContainsString(TestClients::API_KEY, $e->getMessage());
            }
        }
    }
}
