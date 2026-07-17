<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Errors\OutcomeUnknownException;
use Revaly\Sdk\Errors\RapCoreException;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * ADR-SDK-004: no hidden retries anywhere; single-shot semantics except the explicit
 * caller-bounded reconcile loop. A payment operation issues EXACTLY ONE request no
 * matter how it fails — resubmission is the double-charge hazard this SDK exists to
 * prevent.
 */
final class NoRetryTest extends TestCase
{
    /** @return iterable<string, array{string}> */
    public static function failureScenarios(): iterable
    {
        yield 'permanent rejection 422' => ['permanentRejection'];
        yield '503 + not_processed' => ['notProcessed'];
        yield 'bare 503' => ['bare503'];
        yield '500' => ['serverError'];
        yield 'connection refused' => ['connectionRefused'];
        yield 'timeout' => ['timeout'];
    }

    #[DataProvider('failureScenarios')]
    public function testEveryFailureClassGetsExactlyOneRequest(string $scenario): void
    {
        $mock = new RapMockTransport();
        match ($scenario) {
            'permanentRejection' => $mock->charge()->returnsPermanentRejection(422),
            'notProcessed' => $mock->charge()->returnsNotProcessed503(),
            'bare503' => $mock->charge()->returnsBare503(),
            'serverError' => $mock->charge()->returnsServerError(),
            'connectionRefused' => $mock->charge()->throwsConnectionRefused(),
            'timeout' => $mock->charge()->throwsTimeoutAfterSend(),
        };
        $client = TestClients::withMock($mock);

        try {
            $client->charge(TestClients::chargeRequest());
            self::fail('expected a typed failure');
        } catch (RapCoreException $expected) {
        }

        self::assertCount(1, $mock->getRequests());
    }

    public function testSuccessIsAlsoSingleShot(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();

        TestClients::withMock($mock)->charge(TestClients::chargeRequest());

        self::assertCount(1, $mock->getRequests());
    }

    public function testRedirectsAreNeverFollowed(): void
    {
        // A followed 307/308 would RE-SEND the payment body — a hidden resubmission.
        // The runtime never follows; an off-contract 3xx classifies OutcomeUnknown.
        $mock = new RapMockTransport();
        $mock->charge()->returns(307, '', ['Location' => 'https://elsewhere.synthetic.test/payments']);
        $client = TestClients::withMock($mock);

        try {
            $client->charge(TestClients::chargeRequest());
            self::fail('expected OutcomeUnknownException');
        } catch (OutcomeUnknownException $e) {
            self::assertSame(307, $e->getStatusCode());
        }

        self::assertCount(1, $mock->getRequests());
    }

    public function testOutcomeUnknownDoesNotAutoReconcile(): void
    {
        // Reconciliation is the CALLER's explicit decision (§3) — the client never
        // issues a GET on its own after a failed POST.
        $mock = new RapMockTransport();
        $mock->charge()->throwsTimeoutAfterSend();
        $client = TestClients::withMock($mock);

        try {
            $client->charge(TestClients::chargeRequest());
            self::fail('expected OutcomeUnknownException');
        } catch (OutcomeUnknownException $expected) {
        }

        self::assertCount(1, $mock->getRequests());
        self::assertSame('POST', $mock->getRequests()[0]->method);
    }
}
