package co.revaly.sdk.errors;

import com.fasterxml.jackson.databind.JsonNode;

/**
 * Base type for the three typed failure classes of the RAP failover contract
 * (docs/failover-contract.md §2; runtime-tdd.md §3). Catch the subclasses — {@link
 * PermanentRejectionException}, {@link TransientFailureException}, {@link OutcomeUnknownException}
 * — to branch failover logic.
 *
 * <p>Checked-vs-unchecked note: these are CHECKED exceptions, [Proposed] pending the DX-contract §a
 * idiomatic-reviewer sign-off (runtime-tdd §3 leaves the java idiom to the bake-off). Checked
 * mirrors the generated core's {@code ApiException} convention and forces the merchant to face the
 * three-way failover decision at compile time — the safety-critical branch this SDK exists to
 * teach.
 *
 * <p>The exception message is values-free by construction (class, HTTP status, code, correlation id
 * only — ADR-SDK-020): it never embeds request payloads, API keys, or the raw response body. The
 * raw error body remains available on {@link #getRawErrorBody()} for programmatic use — scrub
 * before logging (see {@code RapScrubber}).
 */
public abstract class RapCoreException extends Exception {
    private static final long serialVersionUID = 1L;

    private final RapFailureClass failureClass;
    private final Integer statusCode;
    private final String code;
    private final String errorMessage;
    private final transient JsonNode details;
    private final String correlationId;
    private final String rawErrorBody;

    RapCoreException(
            RapFailureClass failureClass,
            String message,
            Integer statusCode,
            String code,
            String errorMessage,
            JsonNode details,
            String correlationId,
            String rawErrorBody,
            Throwable cause) {
        super(message, cause);
        this.failureClass = failureClass;
        this.statusCode = statusCode;
        this.code = code;
        this.errorMessage = errorMessage;
        this.details = details;
        this.correlationId = correlationId;
        this.rawErrorBody = rawErrorBody;
    }

    /** The failure class assigned by the normative classification algorithm. */
    public RapFailureClass getFailureClass() {
        return failureClass;
    }

    /** The HTTP status code, when a response was received; otherwise null. */
    public Integer getStatusCode() {
        return statusCode;
    }

    /**
     * The {@code ErrorResponse.code} machine-readable safety signal, verbatim from the wire, when
     * present. This is an open string: values beyond today's {@code not_processed} / {@code
     * outcome_unknown} arrive with OQ-2 (the full error-code taxonomy) and unrecognized values are
     * treated as absent for classification. Never a closed enum (repo rule 5).
     */
    public String getCode() {
        return code;
    }

    /** The human-readable {@code error} message from the response body, if any. */
    public String getErrorMessage() {
        return errorMessage;
    }

    /**
     * The opaque {@code details} member of the error body, if any. The SDK never interprets it
     * (failover-contract §2) and it may contain merchant payload echoes — treat as sensitive when
     * logging (it is excluded from {@link #getMessage()}).
     */
    public JsonNode getDetails() {
        return details;
    }

    /**
     * The request correlation id ({@code X-Correlation-ID} response header), when a response was
     * received. Quote it in support tickets — it joins directly to RAP-core telemetry (DX contract
     * §c).
     */
    public String getCorrelationId() {
        return correlationId;
    }

    /**
     * The raw error response body, when one was received. Kept out of {@link #getMessage()} and
     * {@code toString()}; scrub before logging (see {@code RapScrubber}).
     */
    public String getRawErrorBody() {
        return rawErrorBody;
    }

    static String buildMessage(
            RapFailureClass failureClass,
            Integer statusCode,
            String code,
            String correlationId,
            String detail) {
        return "RAP request failed [class="
                + failureClass
                + " status="
                + (statusCode == null ? "-" : statusCode.toString())
                + " code="
                + (code == null ? "-" : code)
                + " correlation="
                + (correlationId == null ? "-" : correlationId)
                + "]: "
                + detail;
    }
}
