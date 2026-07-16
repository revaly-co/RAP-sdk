package co.revaly.sdk.testing;

import java.util.Collections;
import java.util.Map;

/** One request observed by {@link RapMockTransport}, for merchant test assertions. */
public final class RecordedRequest {

    private final String method;
    private final String path;
    private final Map<String, String> headers;
    private final String body;

    RecordedRequest(String method, String path, Map<String, String> headers, String body) {
        this.method = method;
        this.path = path;
        this.headers = Collections.unmodifiableMap(headers);
        this.body = body;
    }

    public String getMethod() {
        return method;
    }

    public String getPath() {
        return path;
    }

    /**
     * Request headers, case-insensitive lookup. User-Agent is joined with spaces (it is a
     * product-token list on the wire); other multi-valued headers join with commas.
     */
    public Map<String, String> getHeaders() {
        return headers;
    }

    /** The request body, or null when the request had none. */
    public String getBody() {
        return body;
    }
}
