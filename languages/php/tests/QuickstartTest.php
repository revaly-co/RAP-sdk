<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Core\Model\PaymentRequest;
use Revaly\Sdk\Errors\OutcomeUnknownException;
use Revaly\Sdk\Errors\PermanentRejectionException;
use Revaly\Sdk\Errors\TransientFailureException;
use Revaly\Sdk\RapClient;
use Revaly\Sdk\Reconcile\Found;
use Revaly\Sdk\Reconcile\NotFoundYet;
use Revaly\Sdk\Reconcile\RapTransactionOutcome;
use Revaly\Sdk\Reconcile\ReconcilePolicy;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * Executes the README quickstart (runtime-tdd §9; DX contract §b): install → init →
 * charge → handle ALL THREE error classes → reconcile with every verdict branch
 * including the mandatory default. If this test drifts from the README, the README is
 * wrong.
 */
final class QuickstartTest extends TestCase
{
    /** The quickstart's charge + failure-handling flow, verbatim in shape. */
    private function quickstartChargeFlow(RapClient $client, PaymentRequest $request): string
    {
        try {
            $transaction = $client->charge($request);

            return 'approved:' . $transaction->getTransactionId();
        } catch (PermanentRejectionException $e) {
            // Fix or decline. NEVER fail over — the same request fails anywhere.
            return 'rejected:' . $e->getStatusCode();
        } catch (TransientFailureException $e) {
            // Definitively not processed — route to your own gateway immediately.
            return 'failover';
        } catch (OutcomeUnknownException $e) {
            // May have been processed — reconcile BEFORE acting (double-charge hazard).
            $verdict = $client->reconcile(
                $request->getMerchantTransactionId(),
                new ReconcilePolicy(maxAttempts: 5, overallBudgetSeconds: 30.0, initialDelaySeconds: 0.0),
            );

            if ($verdict instanceof Found) {
                return match ($verdict->getOutcome()) {
                    RapTransactionOutcome::Approved => 'reconciled:approved',
                    RapTransactionOutcome::Declined,
                    RapTransactionOutcome::Error => 'reconciled:terminal-failure',
                    // Pending, Unknown, and future outcomes: hold conservatively.
                    default => 'reconciled:hold',
                };
            }

            if ($verdict instanceof NotFoundYet) {
                // NOT proof of absence — hold and escalate per your policy.
                return 'hold:escalate';
            }

            // Default branch — REQUIRED: future SDK minors add verdicts
            // (e.g. SafeToFailover with platform P-2).
            return 'hold:unknown-verdict';
        }
    }

    public function testHappyPathCharge(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();

        $result = $this->quickstartChargeFlow(TestClients::withMock($mock), TestClients::chargeRequest());

        self::assertSame('approved:txn-synthetic-1', $result);
    }

    public function testPermanentRejectionBranch(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsPermanentRejection(422);

        $result = $this->quickstartChargeFlow(TestClients::withMock($mock), TestClients::chargeRequest());

        self::assertSame('rejected:422', $result);
    }

    public function testTransientFailureBranchIsImmediateFailover(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsNotProcessed503();

        $result = $this->quickstartChargeFlow(TestClients::withMock($mock), TestClients::chargeRequest());

        self::assertSame('failover', $result);
    }

    public function testOutcomeUnknownReconcilesToApproved(): void
    {
        $request = TestClients::chargeRequest();
        $mock = new RapMockTransport();
        $mock->charge()->throwsTimeoutAfterSend();
        $mock->reconcile($request->getMerchantTransactionId())->notFoundYet()->thenFoundApproved();

        $result = $this->quickstartChargeFlow(TestClients::withMock($mock), $request);

        // The payment already succeeded at RAP-core — failing over would double-charge.
        self::assertSame('reconciled:approved', $result);
    }

    public function testOutcomeUnknownWithSustainedAbsenceHolds(): void
    {
        $request = TestClients::chargeRequest();
        $mock = new RapMockTransport();
        $mock->charge()->throwsTimeoutAfterSend();
        $mock->reconcile($request->getMerchantTransactionId())->notFoundYet();

        $result = $this->quickstartChargeFlow(TestClients::withMock($mock), $request);

        // V1 has NO SafeToFailover: sustained NotFoundYet is hold-and-escalate.
        self::assertSame('hold:escalate', $result);
    }

    public function testPendingOutcomeHoldsViaTheDefaultBranch(): void
    {
        $request = TestClients::chargeRequest();
        $mock = new RapMockTransport();
        $mock->charge()->throwsTimeoutAfterSend();
        $mock->reconcile($request->getMerchantTransactionId())->pending();

        $result = $this->quickstartChargeFlow(TestClients::withMock($mock), $request);

        self::assertSame('reconciled:hold', $result);
    }
}
