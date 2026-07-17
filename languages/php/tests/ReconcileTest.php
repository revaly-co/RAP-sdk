<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Errors\PermanentRejectionException;
use Revaly\Sdk\Reconcile\Found;
use Revaly\Sdk\Reconcile\NotFoundYet;
use Revaly\Sdk\Reconcile\RapTransactionOutcome;
use Revaly\Sdk\Reconcile\ReconcilePolicy;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Testing\SyntheticData;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * The reconcile helper (failover-contract §3; runtime-tdd §4): the only loop the SDK
 * owns, caller-bounded, GET-only, classifying from RAW bodies.
 */
final class ReconcileTest extends TestCase
{
    private const MTX = SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID;

    /** A no-delay policy so tests never sleep. */
    private static function policy(int $maxAttempts = 5, float $budgetSeconds = 30.0): ReconcilePolicy
    {
        return new ReconcilePolicy($maxAttempts, $budgetSeconds, 0.0);
    }

    public function testFoundApprovedImmediately(): void
    {
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->returnsApproved();

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

        self::assertInstanceOf(Found::class, $verdict);
        self::assertSame(RapTransactionOutcome::Approved, $verdict->getOutcome());
        self::assertNotNull($verdict->getTransaction());
        self::assertSame(self::MTX, $verdict->getTransaction()->getMerchantTransactionId());
        self::assertNull($verdict->getPending());
        self::assertSame(SyntheticData::DEFAULT_CORRELATION_ID, $verdict->getCorrelationId());
    }

    public function testFoundDeclinedAndErrorMapTerminalOutcomes(): void
    {
        foreach ([2 => RapTransactionOutcome::Declined, 3 => RapTransactionOutcome::Error] as $status => $expected) {
            $mock = new RapMockTransport();
            $mock->reconcile(self::MTX)->returnsUnmappedStatus($status);

            $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

            self::assertInstanceOf(Found::class, $verdict);
            self::assertSame($expected, $verdict->getOutcome());
        }
    }

    public function testUnmappedStatusIsFoundUnknown(): void
    {
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->returnsUnmappedStatus(42);

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

        self::assertInstanceOf(Found::class, $verdict);
        // A sighting is still a sighting: never fail over on Unknown.
        self::assertSame(RapTransactionOutcome::Unknown, $verdict->getOutcome());
        self::assertNotNull($verdict->getTransaction());
    }

    public function testPendingStateDiscriminatesFromTheRawBody(): void
    {
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->pending();

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

        self::assertInstanceOf(Found::class, $verdict);
        self::assertSame(RapTransactionOutcome::Pending, $verdict->getOutcome());
        self::assertNotNull($verdict->getPending());
        self::assertSame('pending', $verdict->getPending()->getState());
        self::assertNull($verdict->getTransaction());
    }

    public function testNotFoundYetThenFound(): void
    {
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->notFoundYet(2)->thenFoundApproved();

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

        self::assertInstanceOf(Found::class, $verdict);
        self::assertCount(3, $mock->getRequests());
    }

    public function testSustainedNotFoundYetReportsAttemptsAndStatus(): void
    {
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->notFoundYet();

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy(maxAttempts: 3));

        self::assertInstanceOf(NotFoundYet::class, $verdict);
        self::assertSame(3, $verdict->getAttempts());
        self::assertSame(404, $verdict->getLastHttpStatus());
        self::assertGreaterThanOrEqual(0.0, $verdict->getElapsedSeconds());
        self::assertSame(SyntheticData::DEFAULT_CORRELATION_ID, $verdict->getCorrelationId());
        self::assertCount(3, $mock->getRequests());
    }

    public function testDegradedReadKeepsPollingWithinBudget(): void
    {
        // A 500 on the GET is exactly the window where visibility is widest — poll on.
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->returnsServerError()->thenFoundApproved();

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

        self::assertInstanceOf(Found::class, $verdict);
        self::assertCount(2, $mock->getRequests());
    }

    public function testTransportFailureOnTheReadKeepsPolling(): void
    {
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->throwsConnectionRefused()->thenFoundApproved();

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

        self::assertInstanceOf(Found::class, $verdict);
        self::assertCount(2, $mock->getRequests());
    }

    public function testUnreadable2xxBodyIsNotASighting(): void
    {
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->returns(200, 'not json at all')->thenFoundApproved();

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

        self::assertInstanceOf(Found::class, $verdict);
        self::assertCount(2, $mock->getRequests());
    }

    public function testGroupedEnvelopeIsFoundUnknown(): void
    {
        // A shape this SDK version does not map terminally — found-but-unmapped is
        // still FOUND (treat conservatively; do not fail over).
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->returnsTransactionGroup();

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, self::policy());

        self::assertInstanceOf(Found::class, $verdict);
        self::assertSame(RapTransactionOutcome::Unknown, $verdict->getOutcome());
    }

    public function testRejectedReadEscapesAsPermanentRejection(): void
    {
        // Polling never fixes bad credentials — the caller must see it (§3).
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->returnsPermanentRejection(401);

        $this->expectException(PermanentRejectionException::class);
        TestClients::withMock($mock)->reconcile(self::MTX, self::policy());
    }

    public function testBudgetStopsThePollBeforeTheNextDelay(): void
    {
        // initialDelay 5s against a 0.5s budget: after attempt 1 the loop must stop
        // rather than sleep past the caller's budget.
        $mock = new RapMockTransport();
        $mock->reconcile(self::MTX)->notFoundYet();
        $policy = new ReconcilePolicy(10, 0.5, 5.0);

        $verdict = TestClients::withMock($mock)->reconcile(self::MTX, $policy);

        self::assertInstanceOf(NotFoundYet::class, $verdict);
        self::assertSame(1, $verdict->getAttempts());
    }

    public function testEmptyMerchantTransactionIdIsRejected(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        TestClients::withMock(new RapMockTransport())->reconcile('   ', self::policy());
    }

    public function testPolicyBoundsAreValidated(): void
    {
        // OQ-6: no SDK-invented defaults — all bounds are explicit and validated.
        foreach (
            [
                fn () => new ReconcilePolicy(0, 1.0, 0.0),
                fn () => new ReconcilePolicy(1, 0.0, 0.0),
                fn () => new ReconcilePolicy(1, 1.0, -0.1),
            ] as $invalid
        ) {
            try {
                $invalid();
                self::fail('expected InvalidArgumentException');
            } catch (\InvalidArgumentException $e) {
                self::assertNotSame('', $e->getMessage());
            }
        }
    }

    public function testBackoffDoublesAndRespectsTheCap(): void
    {
        $policy = new ReconcilePolicy(5, 60.0, 1.0, 2.5);

        // Jitter is ±20%, so assert the enclosing envelopes.
        $first = $policy->delayForAttempt(1);
        $second = $policy->delayForAttempt(2);
        $third = $policy->delayForAttempt(3);

        self::assertGreaterThanOrEqual(0.8, $first);
        self::assertLessThanOrEqual(1.2, $first);
        self::assertGreaterThanOrEqual(1.6, $second);
        self::assertLessThanOrEqual(2.4, $second);
        // Raw 4.0 capped to 2.5 before jitter.
        self::assertGreaterThanOrEqual(2.0, $third);
        self::assertLessThanOrEqual(3.0, $third);
    }
}
