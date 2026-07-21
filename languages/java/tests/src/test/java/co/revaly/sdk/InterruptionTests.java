package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import co.revaly.sdk.errors.OutcomeUnknownException;
import java.io.IOException;
import java.net.Authenticator;
import java.net.CookieHandler;
import java.net.ProxySelector;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.security.NoSuchAlgorithmException;
import java.time.Duration;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLParameters;
import org.junit.jupiter.api.Test;

/**
 * Java's cancellation idiom through the classification pipe ({@code
 * FailureClassifier.classifyInterruption}): interruption mid-request can never prove the request
 * was not sent, so it classifies OutcomeUnknown — and the thread's interrupt status is restored
 * before the typed error reaches the caller (never swallowed).
 */
class InterruptionTests {

    @Test
    void interruptionClassifiesOutcomeUnknownAndRestoresInterruptStatus() {
        RapClient client =
                RapClient.builder()
                        .apiKey(TestClient.API_KEY)
                        .baseUrl("https://sandbox.synthetic.test")
                        .transport(new InterruptingTransport())
                        .build();

        OutcomeUnknownException e =
                assertThrows(
                        OutcomeUnknownException.class,
                        () -> client.charge(TestClient.paymentRequest()));

        // Thread.interrupted() also CLEARS the flag, leaving the test thread clean.
        assertTrue(Thread.interrupted(), "the interrupt status must be restored to the caller");
        assertTrue(
                e.getCause() instanceof InterruptedException,
                "the typed error keeps the InterruptedException cause");
        assertNull(e.getStatusCode(), "no response was received");
        assertTrue(e.getMessage().contains("reconcile"), "teaches the reconcile procedure");
    }

    /**
     * A transport whose {@code send} is interrupted mid-request: the generated core catches the
     * {@link InterruptedException}, restores the interrupt status, and wraps it in the {@code
     * ApiException} whose cause the runtime classifies.
     */
    private static final class InterruptingTransport extends HttpClient {

        @Override
        public <T> HttpResponse<T> send(HttpRequest request, HttpResponse.BodyHandler<T> handler)
                throws IOException, InterruptedException {
            throw new InterruptedException("interrupted mid-request (synthetic)");
        }

        @Override
        public <T> CompletableFuture<HttpResponse<T>> sendAsync(
                HttpRequest request, HttpResponse.BodyHandler<T> handler) {
            CompletableFuture<HttpResponse<T>> failed = new CompletableFuture<>();
            failed.completeExceptionally(
                    new InterruptedException("interrupted mid-request (synthetic)"));
            return failed;
        }

        @Override
        public <T> CompletableFuture<HttpResponse<T>> sendAsync(
                HttpRequest request,
                HttpResponse.BodyHandler<T> handler,
                HttpResponse.PushPromiseHandler<T> pushPromiseHandler) {
            return sendAsync(request, handler);
        }

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
            } catch (NoSuchAlgorithmException e) {
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
    }
}
