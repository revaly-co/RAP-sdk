package co.revaly.sdk.transport;

/** Wire-header names and tokens the runtime owns (runtime-tdd §5). */
public final class RapHeaders {

    public static final String AUTHORIZATION = "Authorization";

    /**
     * The RAP auth scheme prefix — {@code Authorization: ApiKey <key>}. The prefix is mandatory;
     * this is NOT a Bearer scheme. The {@code native} core generates no auth helpers, so the
     * runtime owns the full header (pipeline/java/config.yaml).
     */
    public static final String AUTH_SCHEME_PREFIX = "ApiKey ";

    /** Selects the RAP API contract version on every request (runtime-tdd §1). */
    public static final String API_VERSION = "X-Api-Version";

    /**
     * Present on every response, success and error alike (gated spec ≥ 2.2.1). Joins a merchant
     * support ticket directly to RAP-core telemetry (DX contract §c).
     */
    public static final String CORRELATION_ID = "X-Correlation-ID";

    public static final String USER_AGENT = "User-Agent";

    private RapHeaders() {}
}
