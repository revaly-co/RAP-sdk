package co.revaly.sdk.errors;

import com.fasterxml.jackson.databind.JsonNode;

/**
 * The payment was definitively NOT processed at RAP-core: either the transport can prove the
 * request was never sent (connection refused, DNS or TLS failure before acceptance), the platform
 * answered 503 with {@code code: not_processed} (provable non-dispatch), or the edge firewall
 * blocked the request with a 403 carrying {@code details.edgeRejection: true} ({@link
 * #isEdgeRejection()}, ADR-SDK-033). <b>Safe to fail over</b> — route the payment to your own
 * gateway immediately (failover-contract §2, the PRD's first-layer failover path).
 */
public final class TransientFailureException extends RapCoreException {
    private static final long serialVersionUID = 1L;

    TransientFailureException(
            Integer statusCode,
            String code,
            String errorMessage,
            JsonNode details,
            String correlationId,
            String rawErrorBody,
            boolean edgeRejection,
            String edgeReference) {
        super(
                RapFailureClass.TRANSIENT_FAILURE,
                buildMessage(
                        RapFailureClass.TRANSIENT_FAILURE,
                        statusCode,
                        code,
                        correlationId,
                        edgeRejection
                                ? "blocked at the edge firewall; never reached the platform — safe"
                                        + " to fail over"
                                : "definitively not processed; safe to fail over"),
                statusCode,
                code,
                errorMessage,
                details,
                correlationId,
                rawErrorBody,
                null,
                edgeRejection,
                edgeReference);
    }

    TransientFailureException(String detail, Throwable cause) {
        super(
                RapFailureClass.TRANSIENT_FAILURE,
                buildMessage(RapFailureClass.TRANSIENT_FAILURE, null, null, null, detail),
                null,
                null,
                null,
                null,
                null,
                null,
                cause,
                false,
                null);
    }
}
