package co.revaly.sdk.errors;

import com.fasterxml.jackson.databind.JsonNode;

/**
 * The request was received by RAP-core and rejected (HTTP 400/401/403/404/422). The payment was NOT
 * processed and the same request fails anywhere — fix or decline, <b>never fail over</b>
 * (failover-contract §2).
 */
public final class PermanentRejectionException extends RapCoreException {
    private static final long serialVersionUID = 1L;

    PermanentRejectionException(
            Integer statusCode,
            String code,
            String errorMessage,
            JsonNode details,
            String correlationId,
            String rawErrorBody) {
        super(
                RapFailureClass.PERMANENT_REJECTION,
                buildMessage(
                        RapFailureClass.PERMANENT_REJECTION,
                        statusCode,
                        code,
                        correlationId,
                        "received and rejected; fix or decline — never fail over"),
                statusCode,
                code,
                errorMessage,
                details,
                correlationId,
                rawErrorBody,
                null);
    }
}
