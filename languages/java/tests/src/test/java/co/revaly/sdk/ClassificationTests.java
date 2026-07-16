package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import co.revaly.sdk.errors.OutcomeUnknownException;
import co.revaly.sdk.errors.PermanentRejectionException;
import co.revaly.sdk.errors.RapCoreException;
import co.revaly.sdk.errors.RapFailureClass;
import co.revaly.sdk.errors.TransientFailureException;
import co.revaly.sdk.testing.RapMockTransport;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/**
 * The failover-contract §2 classification table, row by row, through the full client stack (mock
 * transport → generated core → runtime classifier).
 */
class ClassificationTests {

    @ParameterizedTest
    @ValueSource(ints = {400, 401, 403, 404, 422})
    void rejectionStatusesClassifyPermanentRejection(int status) {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsPermanentRejection(status);
        RapClient client = TestClient.client(mock);

        PermanentRejectionException e =
                assertThrows(
                        PermanentRejectionException.class,
                        () -> client.charge(TestClient.paymentRequest()));
        assertEquals(RapFailureClass.PERMANENT_REJECTION, e.getFailureClass());
        assertEquals(status, e.getStatusCode());
        assertNotNull(e.getCorrelationId(), "every typed error carries the correlation id");
    }

    @Test
    void notProcessed503ClassifiesTransientFailure() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        RapClient client = TestClient.client(mock);

        TransientFailureException e =
                assertThrows(
                        TransientFailureException.class,
                        () -> client.charge(TestClient.paymentRequest()));
        assertEquals(503, e.getStatusCode());
        assertEquals("not_processed", e.getCode());
        assertNotNull(e.getCorrelationId());
    }

    @Test
    void bare503ClassifiesOutcomeUnknown() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsBare503();
        RapClient client = TestClient.client(mock);

        OutcomeUnknownException e =
                assertThrows(
                        OutcomeUnknownException.class,
                        () -> client.charge(TestClient.paymentRequest()));
        assertEquals(503, e.getStatusCode());
        assertNull(e.getCode());
    }

    @Test
    void unrecognizedCodeIsOpenStringAndTreatedAsAbsent() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsUnknownCode503("totally_new_oq2_code");
        RapClient client = TestClient.client(mock);

        OutcomeUnknownException e =
                assertThrows(
                        OutcomeUnknownException.class,
                        () -> client.charge(TestClient.paymentRequest()));
        // Carried verbatim for the merchant, but never trusted for classification.
        assertEquals("totally_new_oq2_code", e.getCode());
    }

    @ParameterizedTest
    @ValueSource(ints = {500, 502, 504})
    void serverErrorsClassifyOutcomeUnknown(int status) {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returns(status, "{\"error\":\"synthetic\"}", null);
        RapClient client = TestClient.client(mock);

        RapCoreException e =
                assertThrows(
                        OutcomeUnknownException.class,
                        () -> client.charge(TestClient.paymentRequest()));
        assertEquals(status, e.getStatusCode());
    }

    @Test
    void statusOutsideTheTableClassifiesOutcomeUnknown() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returns(409, "{\"error\":\"synthetic conflict\"}", null);
        RapClient client = TestClient.client(mock);

        assertThrows(
                OutcomeUnknownException.class, () -> client.charge(TestClient.paymentRequest()));
    }

    @Test
    void connectionRefusedIsProvablyNeverSent() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().throwsConnectionRefused();
        RapClient client = TestClient.client(mock);

        TransientFailureException e =
                assertThrows(
                        TransientFailureException.class,
                        () -> client.charge(TestClient.paymentRequest()));
        assertNull(e.getStatusCode(), "no response was received");
    }

    @Test
    void connectPhaseTimeoutIsProvablyNeverSent() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().throwsConnectTimeout();
        RapClient client = TestClient.client(mock);

        assertThrows(
                TransientFailureException.class, () -> client.charge(TestClient.paymentRequest()));
    }

    @Test
    void tlsHandshakeFailureIsProvablyNeverSent() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().throwsSslHandshakeFailure();
        RapClient client = TestClient.client(mock);

        assertThrows(
                TransientFailureException.class, () -> client.charge(TestClient.paymentRequest()));
    }

    @Test
    void deadlineAfterSendClassifiesOutcomeUnknownNeverTransient() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().throwsTimeoutAfterSend();
        RapClient client = TestClient.client(mock);

        OutcomeUnknownException e =
                assertThrows(
                        OutcomeUnknownException.class,
                        () -> client.charge(TestClient.paymentRequest()));
        assertTrue(e.getMessage().contains("reconcile"), "teaches the reconcile procedure");
    }

    @Test
    void connectionResetMidFlightClassifiesOutcomeUnknown() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().throwsConnectionReset();
        RapClient client = TestClient.client(mock);

        assertThrows(
                OutcomeUnknownException.class, () -> client.charge(TestClient.paymentRequest()));
    }

    @Test
    void version20PinNarrowsFastFailoverTo503NotProcessed() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        RapClient client = TestClient.client(mock, "2.0");

        // On the 2.0 contract the `code` field is undocumented, so provable non-dispatch
        // narrows to client-side never-sent proof only (runtime-tdd §1 [Decided]).
        assertThrows(
                OutcomeUnknownException.class, () -> client.charge(TestClient.paymentRequest()));
    }

    @Test
    void typedErrorMessagesAreValuesFree() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        RapClient client = TestClient.client(mock);

        RapCoreException e =
                assertThrows(
                        RapCoreException.class, () -> client.charge(TestClient.paymentRequest()));
        assertFalse(e.getMessage().contains(TestClient.API_KEY), "no API key in messages");
        assertFalse(
                e.getMessage().contains("platform breaker open"),
                "no response body text in messages");
        assertTrue(e.getMessage().contains("correlation=mock-corr-1"));
        assertNotNull(e.getRawErrorBody(), "raw body stays available programmatically");
    }

    @Test
    void errorBodyFieldsAreCarriedVerbatim() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsPermanentRejection(422);
        RapClient client = TestClient.client(mock);

        PermanentRejectionException e =
                assertThrows(
                        PermanentRejectionException.class,
                        () -> client.charge(TestClient.paymentRequest()));
        assertEquals("synthetic rejection", e.getErrorMessage());
        assertNull(e.getCode());
    }
}
