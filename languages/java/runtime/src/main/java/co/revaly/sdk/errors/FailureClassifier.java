package co.revaly.sdk.errors;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.net.ConnectException;
import java.net.http.HttpConnectTimeoutException;
import java.net.http.HttpTimeoutException;
import java.nio.channels.UnresolvedAddressException;
import javax.net.ssl.SSLHandshakeException;

/**
 * The normative failure-classification algorithm of failover-contract.md §2. Every rule here is
 * contract, not heuristic:
 *
 * <pre>
 * if transport error and request provably never sent          → TransientFailure
 * if HTTP status in {400, 401, 403, 404, 422}                 → PermanentRejection
 * if HTTP status == 503 and body.code == "not_processed"      → TransientFailure
 * if HTTP status &gt;= 500                                        → OutcomeUnknown
 * if deadline exceeded after send / reset / ambiguous          → OutcomeUnknown
 * </pre>
 *
 * Never classify from {@code error} message text; treat {@code details} as opaque; unrecognized
 * {@code code} values are treated as absent; when the stack cannot prove the request was never
 * sent, classify OutcomeUnknown — never guess toward "safe".
 */
public final class FailureClassifier {

    /** The provable-non-dispatch safety signal (platform P-1, ADR-SDK-007). */
    public static final String NOT_PROCESSED = "not_processed";

    // Plain mapper for raw-body reads only (open strings — repo rule 5); reads are
    // thread-safe and no core modules are needed.
    private static final ObjectMapper RAW = new ObjectMapper();

    private static final int MAX_CAUSE_DEPTH = 8;

    private FailureClassifier() {}

    /**
     * Classifies a received non-success HTTP response. Statuses outside the §2 table (e.g. 409,
     * 3xx) are ambiguous and classify as OutcomeUnknown — reconcile reveals the true state.
     *
     * @param statusCode the received HTTP status code
     * @param rawBody the raw response body (may be null/empty)
     * @param apiVersion the pinned {@code X-Api-Version}. On {@code "2.0"} the {@code
     *     ErrorResponse.code} field is not part of the documented contract, so the fast-failover
     *     class narrows to client-provable never-sent failures only: 503 + {@code not_processed} is
     *     NOT honored and falls through to OutcomeUnknown (runtime-tdd §1 [Decided]).
     * @param correlationId the response correlation id, if present
     */
    public static RapCoreException classifyResponse(
            int statusCode, String rawBody, String apiVersion, String correlationId) {
        ParsedError parsed = parseErrorBody(rawBody);

        if (statusCode == 400
                || statusCode == 401
                || statusCode == 403
                || statusCode == 404
                || statusCode == 422) {
            return new PermanentRejectionException(
                    statusCode, parsed.code, parsed.error, parsed.details, correlationId, rawBody);
        }

        if (statusCode == 503 && NOT_PROCESSED.equals(parsed.code) && !"2.0".equals(apiVersion)) {
            return new TransientFailureException(
                    statusCode, parsed.code, parsed.error, parsed.details, correlationId, rawBody);
        }

        return new OutcomeUnknownException(
                statusCode, parsed.code, parsed.error, parsed.details, correlationId, rawBody);
    }

    /**
     * Classifies a transport-level failure by the cause chain. Provably-never-sent detection uses
     * {@code java.net.http}'s own phase semantics: connection establishment ({@link
     * ConnectException}, {@link HttpConnectTimeoutException}), name resolution ({@link
     * UnresolvedAddressException}), and TLS handshake ({@link SSLHandshakeException}) failures all
     * occur before the request was accepted, so they are {@link TransientFailureException}. A
     * non-connect {@link HttpTimeoutException} is the overall deadline expiring after send —
     * OutcomeUnknown by contract, never TransientFailure (runtime-tdd §1). Every other transport
     * failure (reset mid-flight, ambiguous IO) is OutcomeUnknown.
     */
    public static RapCoreException classifyTransportFailure(Throwable failure) {
        Throwable cause = failure;
        for (int depth = 0; cause != null && depth < MAX_CAUSE_DEPTH; depth++) {
            // Connect-phase timeout is a subclass of HttpTimeoutException — check first.
            if (cause instanceof HttpConnectTimeoutException
                    || cause instanceof ConnectException
                    || cause instanceof UnresolvedAddressException
                    || cause instanceof SSLHandshakeException) {
                return new TransientFailureException(
                        "request provably never sent (" + cause.getClass().getSimpleName() + ")",
                        rootException(failure));
            }
            if (cause instanceof HttpTimeoutException) {
                return new OutcomeUnknownException(
                        "deadline exceeded after send; reconcile before acting",
                        rootException(failure));
            }
            cause = cause.getCause();
        }

        return new OutcomeUnknownException(
                "transport failure without never-sent proof ("
                        + failure.getClass().getSimpleName()
                        + ")",
                rootException(failure));
    }

    /**
     * Classifies caller interruption observed mid-request (java's cancellation idiom). Interruption
     * cannot prove the request was never sent, so it lands on the conservative branch:
     * OutcomeUnknown — reconcile before acting. Callers restore the thread's interrupt status
     * before throwing this.
     */
    public static RapCoreException classifyInterruption(Throwable cause) {
        return new OutcomeUnknownException(
                "interrupted mid-request; outcome unknown — reconcile before acting", cause);
    }

    /**
     * Parses {@code code}, {@code error}, and {@code details} from the raw error body. {@code code}
     * is read as an OPEN STRING from the wire — deliberately not via the generated core's {@code
     * ErrorResponse.CodeEnum} (ADR-SDK-023 uniform safety rule; repo rule 5): new values arrive
     * with OQ-2 and must never break classification. Anything unparseable is treated as absent (→
     * the conservative branch).
     */
    static ParsedError parseErrorBody(String rawBody) {
        if (rawBody == null || rawBody.trim().isEmpty()) {
            return ParsedError.EMPTY;
        }
        try {
            JsonNode root = RAW.readTree(rawBody);
            if (root == null || !root.isObject()) {
                return ParsedError.EMPTY;
            }
            String code = null;
            JsonNode codeNode = root.get("code");
            if (codeNode != null && codeNode.isTextual()) {
                code = codeNode.asText();
            }
            String error = null;
            JsonNode errorNode = root.get("error");
            if (errorNode != null && errorNode.isTextual()) {
                error = errorNode.asText();
            }
            JsonNode details = root.get("details");
            return new ParsedError(code, error, details);
        } catch (IOException e) {
            return ParsedError.EMPTY;
        }
    }

    // The transport failures the generated core wraps keep their original exception as
    // the cause; keep only exception causes on the typed error (never response bodies).
    private static Throwable rootException(Throwable failure) {
        return failure;
    }

    static final class ParsedError {
        static final ParsedError EMPTY = new ParsedError(null, null, null);

        final String code;
        final String error;
        final JsonNode details;

        ParsedError(String code, String error, JsonNode details) {
            this.code = code;
            this.error = error;
            this.details = details;
        }
    }
}
