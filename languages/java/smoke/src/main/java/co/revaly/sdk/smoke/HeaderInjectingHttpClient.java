package co.revaly.sdk.smoke;

import java.io.IOException;
import java.net.Authenticator;
import java.net.CookieHandler;
import java.net.ProxySelector;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLParameters;

/**
 * A real-HTTP transport that stamps one extra header on every request. It sits at the RapClient
 * builder's transport seam, INSIDE the runtime's own header injection, so auth/UA/version behaviour
 * is unchanged. Used to send the platform's fault-inject header (Backbone ADR 014 test affordance).
 *
 * <p>Requests are rebuilt field-by-field (the copying {@code HttpRequest.newBuilder(request)} is
 * JDK 16+; this module compiles at the repo's Java 11 floor). Redirects stay disabled — same
 * posture as the runtime's own default transport (a 307 re-POST would resubmit a payment).
 */
final class HeaderInjectingHttpClient extends HttpClient {

    private final HttpClient delegate;
    private final String name;
    private final String value;

    HeaderInjectingHttpClient(String name, String value) {
        this.delegate =
                HttpClient.newBuilder()
                        .connectTimeout(Duration.ofSeconds(5))
                        .followRedirects(Redirect.NEVER)
                        .build();
        this.name = name;
        this.value = value;
    }

    private HttpRequest withHeader(HttpRequest original) {
        HttpRequest.Builder builder =
                HttpRequest.newBuilder(original.uri())
                        .method(
                                original.method(),
                                original.bodyPublisher()
                                        .orElse(HttpRequest.BodyPublishers.noBody()));
        original.timeout().ifPresent(builder::timeout);
        original.version().ifPresent(builder::version);
        original.headers()
                .map()
                .forEach((header, values) -> values.forEach(v -> builder.header(header, v)));
        builder.header(name, value);
        return builder.build();
    }

    @Override
    public <T> HttpResponse<T> send(HttpRequest request, HttpResponse.BodyHandler<T> handler)
            throws IOException, InterruptedException {
        return delegate.send(withHeader(request), handler);
    }

    @Override
    public <T> CompletableFuture<HttpResponse<T>> sendAsync(
            HttpRequest request, HttpResponse.BodyHandler<T> handler) {
        return delegate.sendAsync(withHeader(request), handler);
    }

    @Override
    public <T> CompletableFuture<HttpResponse<T>> sendAsync(
            HttpRequest request,
            HttpResponse.BodyHandler<T> handler,
            HttpResponse.PushPromiseHandler<T> pushPromiseHandler) {
        return delegate.sendAsync(withHeader(request), handler, pushPromiseHandler);
    }

    @Override
    public Optional<CookieHandler> cookieHandler() {
        return delegate.cookieHandler();
    }

    @Override
    public Optional<Duration> connectTimeout() {
        return delegate.connectTimeout();
    }

    @Override
    public Redirect followRedirects() {
        return delegate.followRedirects();
    }

    @Override
    public Optional<ProxySelector> proxy() {
        return delegate.proxy();
    }

    @Override
    public SSLContext sslContext() {
        return delegate.sslContext();
    }

    @Override
    public SSLParameters sslParameters() {
        return delegate.sslParameters();
    }

    @Override
    public Optional<Authenticator> authenticator() {
        return delegate.authenticator();
    }

    @Override
    public Version version() {
        return delegate.version();
    }

    @Override
    public Optional<Executor> executor() {
        return delegate.executor();
    }
}
