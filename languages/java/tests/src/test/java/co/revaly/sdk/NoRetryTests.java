package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import co.revaly.sdk.errors.OutcomeUnknownException;
import co.revaly.sdk.errors.RapCoreException;
import co.revaly.sdk.reconcile.ReconcilePolicy;
import co.revaly.sdk.testing.RapMockTransport;
import java.time.Duration;
import org.junit.jupiter.api.Test;

/**
 * ADR-SDK-004 / failover-contract §5: no hidden retries anywhere, single-shot semantics — the
 * explicit caller-bounded reconcile re-poll is the ONLY loop this SDK owns.
 */
class NoRetryTests {

    @Test
    void aFailedChargeSendsExactlyOneRequest() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsServerError();
        RapClient client = TestClient.client(mock);

        assertThrows(RapCoreException.class, () -> client.charge(TestClient.paymentRequest()));

        assertEquals(1, mock.getRequests().size());
    }

    @Test
    void aTransientFailureIsNotRetriedTheCallerFailsOver() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        RapClient client = TestClient.client(mock);

        assertThrows(RapCoreException.class, () -> client.charge(TestClient.paymentRequest()));

        assertEquals(1, mock.getRequests().size());
    }

    @Test
    void aDeadlineExpiryIsNotRetriedResubmissionIsForbidden() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().throwsTimeoutAfterSend();
        RapClient client = TestClient.client(mock);

        assertThrows(
                OutcomeUnknownException.class, () -> client.charge(TestClient.paymentRequest()));

        assertEquals(
                1, mock.getRequests().size(), "resubmitting an unknown outcome can double-charge");
    }

    @Test
    void reconcileIsCallerBoundedAndStopsAtMaxAttempts() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).notFoundYet();
        RapClient client = TestClient.client(mock);

        client.reconcile(
                TestClient.MTX,
                new ReconcilePolicy(3, Duration.ofSeconds(10), Duration.ofMillis(1)));

        assertEquals(3, mock.getRequests().size());
    }
}
