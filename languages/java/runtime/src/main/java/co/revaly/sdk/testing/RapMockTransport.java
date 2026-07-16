package co.revaly.sdk.testing;

import co.revaly.sdk.transport.RapUserAgent;
import java.io.IOException;
import java.net.Authenticator;
import java.net.CookieHandler;
import java.net.ProxySelector;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpHeaders;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.Executor;
import java.util.concurrent.Flow;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLParameters;
import javax.net.ssl.SSLSession;

/**
 * The first-class no-network test double (DX contract §d): plug it into {@code
 * RapClient.builder().transport(mock)} and script outcomes with the taxonomy-named builders on
 * {@link MockOperation}. Simulates every row of the failover-contract §2 table, both reconcile
 * verdicts and the post-P-2 pending state, and supports scripting consecutive outcomes so merchants
 * can unit-test their failover handler with no network. Asserts on every request that the
 * ADR-SDK-005 User-Agent leads the header. Synthetic data only (ADR-SDK-020).
 *
 * <p>Because the runtime routes ALL its traffic — the generated core's calls and the reconcile
 * helper's raw GETs — through one shared {@link HttpClient}, this single mock intercepts
 * everything.
 */
public final class RapMockTransport extends HttpClient {

    private final List<Route> routes = new ArrayList<>();
    private final ConcurrentLinkedQueue<RecordedRequest> requests = new ConcurrentLinkedQueue<>();
    private final Object gate = new Object();
    private boolean assertUserAgent = true;

    /**
     * Disables the per-request User-Agent assertion (on by default — the UA is part of the contract
     * with platform dashboards, so leave it on unless the test is about it).
     */
    public RapMockTransport withoutUserAgentAssertion() {
        this.assertUserAgent = false;
        return this;
    }

    /** Every request observed by the mock, in order. */
    public List<RecordedRequest> getRequests() {
        return new ArrayList<>(requests);
    }

    /** Scripts {@code POST /payments} (charge). */
    public MockOperation charge() {
        return stub("POST", "/payments", null);
    }

    /** Scripts {@code POST /payments/authorize}. */
    public MockOperation authorize() {
        return stub("POST", "/payments/authorize", null);
    }

    /** Scripts the reconcile GET for one merchant transaction id. */
    public MockOperation reconcile(String merchantTransactionId) {
        return stub(
                "GET",
                "/transactions/merchant/" + urlEncode(merchantTransactionId),
                merchantTransactionId);
    }

    /** Scripts an arbitrary (method, path-prefix) route; the longest matching prefix wins. */
    public MockOperation stub(String method, String pathPrefix) {
        return stub(method, pathPrefix, null);
    }

    private MockOperation stub(String method, String pathPrefix, String merchantTransactionId) {
        synchronized (gate) {
            for (Route route : routes) {
                if (route.method.equals(method) && route.pathPrefix.equals(pathPrefix)) {
                    return route.operation;
                }
            }
            MockOperation operation = new MockOperation(merchantTransactionId);
            routes.add(new Route(method, pathPrefix, operation));
            return operation;
        }
    }

    @Override
    public <T> HttpResponse<T> send(HttpRequest request, HttpResponse.BodyHandler<T> handler)
            throws IOException {
        String path = request.uri().getPath() == null ? "" : request.uri().getPath();
        String body = readRequestBody(request);

        Map<String, String> flatHeaders = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);
        for (Map.Entry<String, List<String>> entry : request.headers().map().entrySet()) {
            // User-Agent is a space-separated product-token list on the wire; other
            // multi-valued headers join with commas per RFC 9110.
            String separator = "User-Agent".equalsIgnoreCase(entry.getKey()) ? " " : ", ";
            flatHeaders.put(entry.getKey(), String.join(separator, entry.getValue()));
        }
        requests.add(new RecordedRequest(request.method(), path, flatHeaders, body));

        if (assertUserAgent) {
            String userAgent = request.headers().firstValue("User-Agent").orElse("");
            if (!userAgent.startsWith(RapUserAgent.PRODUCT_NAME + "/")) {
                throw new IllegalStateException(
                        "The SDK User-Agent product token must lead every request"
                                + " (ADR-SDK-005); saw '"
                                + userAgent
                                + "'.");
            }
        }

        MockOperation.MockResult result;
        synchronized (gate) {
            Route match = null;
            for (Route route : routes) {
                if (route.method.equals(request.method())
                        && path.startsWith(route.pathPrefix)
                        && (match == null
                                || route.pathPrefix.length() > match.pathPrefix.length())) {
                    match = route;
                }
            }
            if (match == null) {
                throw new IllegalStateException(
                        "Unscripted request: "
                                + request.method()
                                + " "
                                + path
                                + ". Script it with stub()/charge()/reconcile().");
            }
            result = match.operation.next();
        }

        if (result.failure != null) {
            throw result.failure;
        }
        return buildResponse(request, handler, result);
    }

    @Override
    public <T> CompletableFuture<HttpResponse<T>> sendAsync(
            HttpRequest request, HttpResponse.BodyHandler<T> handler) {
        try {
            return CompletableFuture.completedFuture(send(request, handler));
        } catch (Exception e) {
            CompletableFuture<HttpResponse<T>> failed = new CompletableFuture<>();
            failed.completeExceptionally(e);
            return failed;
        }
    }

    @Override
    public <T> CompletableFuture<HttpResponse<T>> sendAsync(
            HttpRequest request,
            HttpResponse.BodyHandler<T> handler,
            HttpResponse.PushPromiseHandler<T> pushPromiseHandler) {
        return sendAsync(request, handler);
    }

    private <T> HttpResponse<T> buildResponse(
            HttpRequest request,
            HttpResponse.BodyHandler<T> handler,
            MockOperation.MockResult result) {
        Map<String, List<String>> headerMap =
                result.headers.entrySet().stream()
                        .collect(
                                Collectors.toMap(
                                        Map.Entry::getKey,
                                        e -> Collections.singletonList(e.getValue())));
        HttpHeaders responseHeaders = HttpHeaders.of(headerMap, (a, b) -> true);
        byte[] bytes =
                result.body == null ? new byte[0] : result.body.getBytes(StandardCharsets.UTF_8);

        HttpResponse.BodySubscriber<T> subscriber =
                handler.apply(new MockResponseInfo(result.status, responseHeaders));
        subscriber.onSubscribe(NoopSubscription.INSTANCE);
        if (bytes.length > 0) {
            subscriber.onNext(List.of(ByteBuffer.wrap(bytes)));
        }
        subscriber.onComplete();
        T responseBody;
        try {
            responseBody = subscriber.getBody().toCompletableFuture().get(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted assembling the mock response", e);
        } catch (Exception e) {
            throw new IllegalStateException("could not assemble the mock response body", e);
        }

        return new MockHttpResponse<>(request, result.status, responseHeaders, responseBody);
    }

    private static String readRequestBody(HttpRequest request) {
        Optional<HttpRequest.BodyPublisher> publisher = request.bodyPublisher();
        if (!publisher.isPresent() || publisher.get().contentLength() == 0) {
            return null;
        }
        ByteCollector collector = new ByteCollector();
        publisher.get().subscribe(collector);
        return collector.awaitUtf8();
    }

    private static String urlEncode(String value) {
        return URLEncoder.encode(value, StandardCharsets.UTF_8).replace("+", "%20");
    }

    // ---- HttpClient plumbing ---------------------------------------------------------

    @Override
    public Optional<CookieHandler> cookieHandler() {
        return Optional.empty();
    }

    @Override
    public Optional<Duration> connectTimeout() {
        return Optional.empty();
    }

    @Override
    public Redirect followRedirects() {
        return Redirect.NEVER;
    }

    @Override
    public Optional<ProxySelector> proxy() {
        return Optional.empty();
    }

    @Override
    public SSLContext sslContext() {
        try {
            return SSLContext.getDefault();
        } catch (java.security.NoSuchAlgorithmException e) {
            throw new IllegalStateException(e);
        }
    }

    @Override
    public SSLParameters sslParameters() {
        return new SSLParameters();
    }

    @Override
    public Optional<Authenticator> authenticator() {
        return Optional.empty();
    }

    @Override
    public Version version() {
        return Version.HTTP_1_1;
    }

    @Override
    public Optional<Executor> executor() {
        return Optional.empty();
    }

    private static final class Route {
        final String method;
        final String pathPrefix;
        final MockOperation operation;

        Route(String method, String pathPrefix, MockOperation operation) {
            this.method = method;
            this.pathPrefix = pathPrefix;
            this.operation = operation;
        }
    }

    private enum NoopSubscription implements Flow.Subscription {
        INSTANCE;

        @Override
        public void request(long n) {}

        @Override
        public void cancel() {}
    }

    private static final class ByteCollector implements Flow.Subscriber<ByteBuffer> {
        private final CompletableFuture<byte[]> done = new CompletableFuture<>();
        private final List<ByteBuffer> buffers = new ArrayList<>();

        @Override
        public void onSubscribe(Flow.Subscription subscription) {
            subscription.request(Long.MAX_VALUE);
        }

        @Override
        public void onNext(ByteBuffer item) {
            buffers.add(item);
        }

        @Override
        public void onError(Throwable throwable) {
            done.completeExceptionally(throwable);
        }

        @Override
        public void onComplete() {
            int total = 0;
            for (ByteBuffer buffer : buffers) {
                total += buffer.remaining();
            }
            byte[] all = new byte[total];
            int offset = 0;
            for (ByteBuffer buffer : buffers) {
                int length = buffer.remaining();
                buffer.get(all, offset, length);
                offset += length;
            }
            done.complete(all);
        }

        String awaitUtf8() {
            try {
                return new String(done.get(5, TimeUnit.SECONDS), StandardCharsets.UTF_8);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new IllegalStateException("interrupted reading the mock request body", e);
            } catch (Exception e) {
                throw new IllegalStateException("could not read the mock request body", e);
            }
        }
    }

    private static final class MockHttpResponse<T> implements HttpResponse<T> {
        private final HttpRequest request;
        private final int status;
        private final HttpHeaders headers;
        private final T body;

        MockHttpResponse(HttpRequest request, int status, HttpHeaders headers, T body) {
            this.request = request;
            this.status = status;
            this.headers = headers;
            this.body = body;
        }

        @Override
        public int statusCode() {
            return status;
        }

        @Override
        public HttpRequest request() {
            return request;
        }

        @Override
        public Optional<HttpResponse<T>> previousResponse() {
            return Optional.empty();
        }

        @Override
        public HttpHeaders headers() {
            return headers;
        }

        @Override
        public T body() {
            return body;
        }

        @Override
        public Optional<SSLSession> sslSession() {
            return Optional.empty();
        }

        @Override
        public java.net.URI uri() {
            return request.uri();
        }

        @Override
        public Version version() {
            return Version.HTTP_1_1;
        }
    }

    private static final class MockResponseInfo implements HttpResponse.ResponseInfo {
        private final int status;
        private final HttpHeaders headers;

        MockResponseInfo(int status, HttpHeaders headers) {
            this.status = status;
            this.headers = headers;
        }

        @Override
        public int statusCode() {
            return status;
        }

        @Override
        public HttpHeaders headers() {
            return headers;
        }

        @Override
        public Version version() {
            return Version.HTTP_1_1;
        }
    }
}
