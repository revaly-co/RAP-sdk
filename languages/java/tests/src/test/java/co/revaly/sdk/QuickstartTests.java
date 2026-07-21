package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import co.revaly.sdk.core.model.TransactionResponse;
import co.revaly.sdk.errors.OutcomeUnknownException;
import co.revaly.sdk.errors.PermanentRejectionException;
import co.revaly.sdk.errors.TransientFailureException;
import co.revaly.sdk.reconcile.RapReconcileVerdict;
import co.revaly.sdk.reconcile.RapTransactionOutcome;
import co.revaly.sdk.reconcile.ReconcilePolicy;
import co.revaly.sdk.testing.RapMockTransport;
import java.time.Duration;
import org.junit.jupiter.api.Test;

/**
 * The README quickstart, executed: install → init → charge → handle all three error classes →
 * reconcile with every verdict branch including the default (DX contract §b — these tests keep the
 * copy-paste example honest).
 */
class QuickstartTests {

    @Test
    void quickstartHappyPathChargesSuccessfully() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsApproved();

        RapClient client =
                RapClient.builder()
                        .apiKey(TestClient.API_KEY)
                        .baseUrl("https://sandbox.synthetic.test")
                        .transport(mock)
                        .build();

        TransactionResponse response = client.charge(TestClient.paymentRequest());
        assertEquals(1, response.getTransactionStatus());
    }

    @Test
    void quickstartBranchesOnAllThreeErrorClasses() {
        boolean permanentHandled = false;
        boolean transientHandled = false;
        boolean unknownHandled = false;

        // PermanentRejection: fix or decline — never fail over.
        RapMockTransport rejected = new RapMockTransport();
        rejected.charge().returnsPermanentRejection(422);
        try {
            TestClient.client(rejected).charge(TestClient.paymentRequest());
            fail("expected a typed failure");
        } catch (PermanentRejectionException e) {
            permanentHandled = true;
        } catch (Exception e) {
            fail("wrong class: " + e);
        }

        // TransientFailure: definitively not processed — fail over immediately.
        RapMockTransport breakerOpen = new RapMockTransport();
        breakerOpen.charge().returnsNotProcessed503();
        try {
            TestClient.client(breakerOpen).charge(TestClient.paymentRequest());
            fail("expected a typed failure");
        } catch (TransientFailureException e) {
            transientHandled = true;
        } catch (Exception e) {
            fail("wrong class: " + e);
        }

        // OutcomeUnknown: may have been processed — reconcile before acting.
        RapMockTransport ambiguous = new RapMockTransport();
        ambiguous.charge().throwsTimeoutAfterSend();
        try {
            TestClient.client(ambiguous).charge(TestClient.paymentRequest());
            fail("expected a typed failure");
        } catch (OutcomeUnknownException e) {
            unknownHandled = true;
        } catch (Exception e) {
            fail("wrong class: " + e);
        }

        assertTrue(permanentHandled && transientHandled && unknownHandled);
    }

    @Test
    void quickstartReconcileWorkedExampleAvoidsTheDoubleCharge() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().throwsTimeoutAfterSend();
        mock.reconcile(TestClient.MTX).notFoundYet(1).thenFoundApproved();
        RapClient client = TestClient.client(mock);

        boolean failedOver = false;
        try {
            client.charge(TestClient.paymentRequest());
            fail("expected a typed failure");
        } catch (OutcomeUnknownException e) {
            RapReconcileVerdict verdict =
                    client.reconcile(
                            TestClient.MTX,
                            ReconcilePolicy.builder()
                                    .maxAttempts(5)
                                    .overallBudget(Duration.ofSeconds(10))
                                    .initialDelay(Duration.ofMillis(1))
                                    .build());

            if (verdict instanceof RapReconcileVerdict.Found) {
                RapReconcileVerdict.Found found = (RapReconcileVerdict.Found) verdict;
                if (found.getOutcome() == RapTransactionOutcome.APPROVED) {
                    // The payment already succeeded at RAP-core: failing over here
                    // would charge the cardholder twice.
                    failedOver = false;
                } else {
                    fail("scripted approved");
                }
            } else if (verdict instanceof RapReconcileVerdict.NotFoundYet) {
                fail("scripted found on the second poll");
            } else {
                // Default branch — REQUIRED: verdicts are open for extension.
                fail("future verdict type reached the example");
            }
        }

        assertFalse(failedOver);
    }
}
