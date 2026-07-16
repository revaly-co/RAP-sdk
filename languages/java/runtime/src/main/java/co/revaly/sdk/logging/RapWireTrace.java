package co.revaly.sdk.logging;

import java.util.Collections;
import java.util.Map;

/**
 * One scrubbed request/response observation for the wire-trace hook (runtime-tdd §6; DX contract §c
 * — Enablement escalations). Every payload and header set on this object has already passed the
 * central allowlist scrubber ({@link RapScrubber}) — the hook never receives raw material, so a
 * merchant cannot accidentally log PAN/CVV/PII or API keys through it.
 */
public final class RapWireTrace {

    private final String operation;
    private final String method;
    private final String path;
    private final Integer statusCode;
    private final String correlationId;
    private final Map<String, String> requestHeaders;
    private final String requestBody;
    private final Map<String, String> responseHeaders;
    private final String responseBody;

    public RapWireTrace(
            String operation,
            String method,
            String path,
            Integer statusCode,
            String correlationId,
            Map<String, String> requestHeaders,
            String requestBody,
            Map<String, String> responseHeaders,
            String responseBody) {
        this.operation = operation;
        this.method = method;
        this.path = path;
        this.statusCode = statusCode;
        this.correlationId = correlationId;
        this.requestHeaders =
                requestHeaders == null
                        ? Collections.emptyMap()
                        : Collections.unmodifiableMap(requestHeaders);
        this.requestBody = requestBody;
        this.responseHeaders =
                responseHeaders == null
                        ? Collections.emptyMap()
                        : Collections.unmodifiableMap(responseHeaders);
        this.responseBody = responseBody;
    }

    /** SDK operation name, e.g. {@code charge} or {@code reconcile}. */
    public String getOperation() {
        return operation;
    }

    public String getMethod() {
        return method;
    }

    /** Request path only — never the full URI with query values. */
    public String getPath() {
        return path;
    }

    /** HTTP status, or null when no response was received (transport failure). */
    public Integer getStatusCode() {
        return statusCode;
    }

    public String getCorrelationId() {
        return correlationId;
    }

    /** Scrubbed request headers (Authorization is always {@code [redacted]}). */
    public Map<String, String> getRequestHeaders() {
        return requestHeaders;
    }

    /** Allowlist-scrubbed request payload, or null when the request had no body. */
    public String getRequestBody() {
        return requestBody;
    }

    /** Scrubbed response headers. */
    public Map<String, String> getResponseHeaders() {
        return responseHeaders;
    }

    /** Allowlist-scrubbed response payload, or null when none was received. */
    public String getResponseBody() {
        return responseBody;
    }
}
