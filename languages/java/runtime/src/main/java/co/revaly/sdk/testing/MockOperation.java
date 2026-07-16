package co.revaly.sdk.testing;

import java.io.IOException;
import java.net.ConnectException;
import java.net.http.HttpConnectTimeoutException;
import java.net.http.HttpTimeoutException;
import java.util.ArrayDeque;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import javax.net.ssl.SSLHandshakeException;

/**
 * Scripts consecutive outcomes for one mocked route, with builders named after the
 * failover-contract taxonomy so merchant test code reads as the contract (runtime-tdd §8): {@code
 * mock.charge().returnsNotProcessed503()}, {@code
 * mock.reconcile("id").notFoundYet().thenFoundApproved()}.
 *
 * <p>Outcomes are consumed in order; the LAST scripted outcome repeats for any further requests (so
 * a single {@code returnsApproved()} serves a whole test, and a scripted sequence ends in a stable
 * state).
 */
public final class MockOperation {

    private final ArrayDeque<MockResult> script = new ArrayDeque<>();
    private final String merchantTransactionId;
    private int correlationCounter;

    MockOperation(String merchantTransactionId) {
        this.merchantTransactionId =
                merchantTransactionId == null
                        ? SyntheticData.DEFAULT_MERCHANT_TRANSACTION_ID
                        : merchantTransactionId;
    }

    // ---- Success outcomes -------------------------------------------------------

    /** 200 with a synthetic approved transaction ({@code transactionStatus: 1}). */
    public MockOperation returnsApproved() {
        return enqueueBody(200, SyntheticData.transaction(1, merchantTransactionId));
    }

    /** 200 with a synthetic declined transaction ({@code transactionStatus: 2}). */
    public MockOperation returnsDeclined() {
        return enqueueBody(200, SyntheticData.transaction(2, merchantTransactionId));
    }

    /** 200 with a synthetic terminal-error transaction ({@code transactionStatus: 3}). */
    public MockOperation returnsErrorOutcome() {
        return enqueueBody(200, SyntheticData.transaction(3, merchantTransactionId));
    }

    /** 200 with an unmapped {@code transactionStatus} — exercises the UNKNOWN default branch. */
    public MockOperation returnsUnmappedStatus(int transactionStatus) {
        return enqueueBody(
                200, SyntheticData.transaction(transactionStatus, merchantTransactionId));
    }

    // ---- PermanentRejection rows (failover-contract §2) -------------------------

    /** One of 400/401/403/404/422 with a synthetic {@code ErrorResponse} body. */
    public MockOperation returnsPermanentRejection(int status) {
        return enqueueBody(status, SyntheticData.errorBody("synthetic rejection", null));
    }

    // ---- TransientFailure rows ---------------------------------------------------

    /** 503 with {@code code: not_processed} — provable non-dispatch, immediate failover. */
    public MockOperation returnsNotProcessed503() {
        return enqueueBody(503, SyntheticData.errorBody("platform breaker open", "not_processed"));
    }

    /** Connection refused before the request was sent (never-sent proof). */
    public MockOperation throwsConnectionRefused() {
        return enqueueThrow(new ConnectException("connection refused (synthetic)"));
    }

    /** Connect-phase timeout — the connection was never established (never-sent proof). */
    public MockOperation throwsConnectTimeout() {
        return enqueueThrow(new HttpConnectTimeoutException("connect timed out (synthetic)"));
    }

    /** TLS handshake failure before the request was accepted (never-sent proof). */
    public MockOperation throwsSslHandshakeFailure() {
        return enqueueThrow(new SSLHandshakeException("tls handshake failed (synthetic)"));
    }

    // ---- OutcomeUnknown rows -----------------------------------------------------

    /** Bare 503 — no {@code not_processed} proof: reconcile, never fast-failover. */
    public MockOperation returnsBare503() {
        return enqueueBody(503, SyntheticData.errorBody("upstream unavailable", null));
    }

    /** 503 with an unrecognized {@code code} — treated as absent (open string, OQ-2). */
    public MockOperation returnsUnknownCode503(String code) {
        return enqueueBody(503, SyntheticData.errorBody("upstream unavailable", code));
    }

    /** 500 internal error. */
    public MockOperation returnsServerError() {
        return enqueueBody(500, SyntheticData.errorBody("internal error", null));
    }

    /** 502 from the edge. */
    public MockOperation returnsBadGateway() {
        return enqueueBody(502, SyntheticData.errorBody("bad gateway", null));
    }

    /** 504 from the edge. */
    public MockOperation returnsGatewayTimeout() {
        return enqueueBody(504, SyntheticData.errorBody("gateway timeout", null));
    }

    /** Overall deadline expiry AFTER the request was sent. */
    public MockOperation throwsTimeoutAfterSend() {
        return enqueueThrow(new HttpTimeoutException("request timed out (synthetic)"));
    }

    /** Connection reset mid-flight — ambiguous, no never-sent proof. */
    public MockOperation throwsConnectionReset() {
        return enqueueThrow(new IOException("connection reset (synthetic)"));
    }

    // ---- Reconcile verdicts (failover-contract §3) -------------------------------

    /** 404 — the NotFoundYet signal ("not yet visible", never "doesn't exist"). */
    public MockOperation notFoundYet() {
        return enqueueBody(404, SyntheticData.errorBody("transaction not found", null));
    }

    /** {@code times} consecutive 404s. */
    public MockOperation notFoundYet(int times) {
        for (int i = 0; i < times; i++) {
            notFoundYet();
        }
        return this;
    }

    /** 200 with the pending-intent shape ({@code state: pending}) — post-P-2 scenario. */
    public MockOperation pending() {
        return enqueueBody(200, SyntheticData.pending(merchantTransactionId));
    }

    /** 200 approved — reconcile finds the payment succeeded (no failover!). */
    public MockOperation thenFoundApproved() {
        return returnsApproved();
    }

    /** 200 declined — reconcile finds a terminal decline (merchant decision). */
    public MockOperation thenFoundDeclined() {
        return returnsDeclined();
    }

    /** 200 with a grouped envelope — exercises the found-but-unmapped (UNKNOWN) branch. */
    public MockOperation returnsTransactionGroup() {
        return enqueueBody(200, SyntheticData.transactionGroup(merchantTransactionId));
    }

    // ---- Escape hatch --------------------------------------------------------------

    /** An arbitrary scripted response — synthetic data only (ADR-SDK-020). */
    public MockOperation returns(int status, String body, Map<String, String> headers) {
        Map<String, String> h = headers == null ? Collections.emptyMap() : headers;
        script.addLast(MockResult.response(status, body, new LinkedHashMap<>(h)));
        return this;
    }

    /** An arbitrary scripted transport failure. */
    public MockOperation throwsIo(IOException failure) {
        return enqueueThrow(failure);
    }

    // ---- Internals ------------------------------------------------------------------

    private MockOperation enqueueBody(int status, String body) {
        Map<String, String> headers = new LinkedHashMap<>();
        headers.put("Content-Type", "application/json");
        headers.put("X-Correlation-ID", "mock-corr-" + (++correlationCounter));
        script.addLast(MockResult.response(status, body, headers));
        return this;
    }

    private MockOperation enqueueThrow(IOException failure) {
        script.addLast(MockResult.failure(failure));
        return this;
    }

    MockResult next() {
        if (script.isEmpty()) {
            throw new IllegalStateException(
                    "This route is stubbed but has no scripted outcome; add one with the"
                            + " returns*/throws* builders.");
        }
        return script.size() == 1 ? script.peekFirst() : script.pollFirst();
    }

    static final class MockResult {
        final int status;
        final String body;
        final Map<String, String> headers;
        final IOException failure;

        private MockResult(
                int status, String body, Map<String, String> headers, IOException failure) {
            this.status = status;
            this.body = body;
            this.headers = headers;
            this.failure = failure;
        }

        static MockResult response(int status, String body, Map<String, String> headers) {
            return new MockResult(status, body, headers, null);
        }

        static MockResult failure(IOException failure) {
            return new MockResult(0, null, Collections.emptyMap(), failure);
        }
    }
}
