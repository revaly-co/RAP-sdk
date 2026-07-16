package co.revaly.sdk.errors;

import com.fasterxml.jackson.databind.JsonNode;

/**
 * The payment MAY have been processed at RAP-core (deadline exceeded after send, connection reset
 * mid-flight, 500/502/504, bare 503, or any transport failure without never-sent proof).
 * <b>Reconcile before acting</b> (failover-contract §3) — failing over blind risks charging the
 * cardholder twice.
 */
public final class OutcomeUnknownException extends RapCoreException {
    private static final long serialVersionUID = 1L;

    OutcomeUnknownException(
            Integer statusCode,
            String code,
            String errorMessage,
            JsonNode details,
            String correlationId,
            String rawErrorBody) {
        super(
                RapFailureClass.OUTCOME_UNKNOWN,
                buildMessage(
                        RapFailureClass.OUTCOME_UNKNOWN,
                        statusCode,
                        code,
                        correlationId,
                        "may have been processed; reconcile before acting"),
                statusCode,
                code,
                errorMessage,
                details,
                correlationId,
                rawErrorBody,
                null);
    }

    OutcomeUnknownException(String detail, Throwable cause) {
        super(
                RapFailureClass.OUTCOME_UNKNOWN,
                buildMessage(RapFailureClass.OUTCOME_UNKNOWN, null, null, null, detail),
                null,
                null,
                null,
                null,
                null,
                null,
                cause);
    }
}
