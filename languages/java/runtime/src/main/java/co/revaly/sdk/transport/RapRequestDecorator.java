package co.revaly.sdk.transport;

import java.net.http.HttpRequest;
import java.util.function.Consumer;

/**
 * Decorates every outgoing request — both the generated core's (via the core's request interceptor,
 * which runs last in each request builder) and the runtime's own reconcile GETs — with the headers
 * the runtime owns (runtime-tdd §5):
 *
 * <ul>
 *   <li>{@code Authorization: ApiKey <key>} — the RAP scheme; the core generates no auth machinery,
 *       the runtime is the sole owner.
 *   <li>{@code User-Agent} — the exact ADR-SDK-005 grammar. {@code setHeader} replaces any value
 *       the core or JDK would contribute, so the core cannot bypass it; a merchant token may be
 *       APPENDED after the SDK's (never replacing it).
 *   <li>{@code X-Api-Version} — the pinned contract version on every request.
 * </ul>
 */
public final class RapRequestDecorator implements Consumer<HttpRequest.Builder> {

    private final String apiKey;
    private final String apiVersion;
    private final String userAgent;

    public RapRequestDecorator(String apiKey, String apiVersion, String userAgentSuffix) {
        this.apiKey = apiKey;
        this.apiVersion = apiVersion;
        this.userAgent =
                userAgentSuffix == null || userAgentSuffix.trim().isEmpty()
                        ? RapUserAgent.VALUE
                        : RapUserAgent.VALUE + " " + userAgentSuffix.trim();
    }

    @Override
    public void accept(HttpRequest.Builder builder) {
        builder.setHeader(RapHeaders.AUTHORIZATION, RapHeaders.AUTH_SCHEME_PREFIX + apiKey);
        builder.setHeader(RapHeaders.USER_AGENT, userAgent);
        builder.setHeader(RapHeaders.API_VERSION, apiVersion);
    }

    /** The full User-Agent this decorator stamps (SDK token first, suffix appended). */
    public String getUserAgent() {
        return userAgent;
    }
}
