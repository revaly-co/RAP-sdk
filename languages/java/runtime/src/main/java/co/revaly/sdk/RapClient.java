package co.revaly.sdk;

import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.api.NotifyApi;
import co.revaly.sdk.core.api.PaymentMethodsApi;
import co.revaly.sdk.core.api.PaymentsApi;
import co.revaly.sdk.core.api.TransactionsApi;
import co.revaly.sdk.core.model.AuthorizeRequest;
import co.revaly.sdk.core.model.CaptureRequest;
import co.revaly.sdk.core.model.PaymentRequest;
import co.revaly.sdk.core.model.RefundCancelRequest;
import co.revaly.sdk.core.model.RefundRequest;
import co.revaly.sdk.core.model.TransactionResponse;
import co.revaly.sdk.core.model.VoidRequest;
import co.revaly.sdk.errors.FailureClassifier;
import co.revaly.sdk.errors.RapCoreException;
import co.revaly.sdk.logging.RapScrubber;
import co.revaly.sdk.logging.RapWireTrace;
import co.revaly.sdk.reconcile.RapReconcileVerdict;
import co.revaly.sdk.reconcile.RapReconciler;
import co.revaly.sdk.reconcile.ReconcilePolicy;
import co.revaly.sdk.transport.RapHeaders;
import co.revaly.sdk.transport.RapRequestDecorator;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.net.Authenticator;
import java.net.CookieHandler;
import java.net.ProxySelector;
import java.net.http.HttpClient;
import java.net.http.HttpHeaders;
import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Executor;
import java.util.function.Consumer;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLParameters;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The RAP Java SDK client (runtime-tdd §§1-2): one client object per configuration, immutable and
 * thread-safe — create it once and reuse it (no global singletons).
 *
 * <p>Payment operations return the core's {@link TransactionResponse} on success and throw exactly
 * one of the three typed failure classes on failure (docs/failover-contract.md §2):
 *
 * <ul>
 *   <li>{@link co.revaly.sdk.errors.PermanentRejectionException} — fix or decline; never fail over.
 *   <li>{@link co.revaly.sdk.errors.TransientFailureException} — definitively not processed; safe
 *       to fail over immediately.
 *   <li>{@link co.revaly.sdk.errors.OutcomeUnknownException} — may have been processed; {@link
 *       #reconcile reconcile} before acting.
 * </ul>
 *
 * The full generated V2 surface stays available through {@link #payments()}, {@link
 * #transactions()}, {@link #paymentMethods()} and {@link #notify()} — one dependency, one package
 * to import.
 */
public final class RapClient {

    private static final Logger LOG = LoggerFactory.getLogger(RapClient.class);

    private final String apiVersion;
    private final HttpClient httpClient;
    private final ObjectMapper coreMapper;
    private final Consumer<RapWireTrace> wireTraceHook;
    private final PaymentsApi payments;
    private final TransactionsApi transactions;
    private final PaymentMethodsApi paymentMethods;
    private final NotifyApi notify;
    private final RapReconciler reconciler;

    private RapClient(Builder builder) {
        this.apiVersion = builder.apiVersion;
        this.wireTraceHook = builder.wireTraceHook;

        if (builder.transport != null) {
            this.httpClient = builder.transport;
        } else {
            HttpClient.Builder httpBuilder = HttpClient.newBuilder();
            if (builder.connectTimeout != null) {
                httpBuilder.connectTimeout(builder.connectTimeout);
            }
            this.httpClient = httpBuilder.build();
        }

        RapRequestDecorator decorator =
                new RapRequestDecorator(
                        builder.apiKey, builder.apiVersion, builder.userAgentSuffix);

        // One shared HttpClient for the whole client (core apis + reconciler): the fixed
        // builder hands the same instance to every generated api class.
        ApiClient apiClient =
                new ApiClient(
                        new FixedHttpClientBuilder(httpClient),
                        ApiClient.createDefaultObjectMapper(),
                        builder.baseUrl);
        // Overall per-request deadline; expiry after send classifies OutcomeUnknown
        // (runtime-tdd §1). No SDK-invented default — OQ-6 (docs/open-items.md).
        if (builder.overallDeadline != null) {
            apiClient.setReadTimeout(builder.overallDeadline);
        }
        apiClient.setRequestInterceptor(decorator);

        this.coreMapper = apiClient.getObjectMapper();
        this.payments = new PaymentsApi(apiClient);
        this.transactions = new TransactionsApi(apiClient);
        this.paymentMethods = new PaymentMethodsApi(apiClient);
        this.notify = new NotifyApi(apiClient);
        this.reconciler =
                new RapReconciler(
                        httpClient,
                        apiClient.getBaseUri(),
                        decorator,
                        builder.overallDeadline,
                        builder.apiVersion,
                        coreMapper,
                        builder.wireTraceHook);
    }

    public static Builder builder() {
        return new Builder();
    }

    /** Charges a payment ({@code POST /payments}). */
    public TransactionResponse charge(PaymentRequest request) throws RapCoreException {
        return execute(
                "charge",
                "POST",
                "/payments",
                request,
                () -> payments.chargePaymentWithHttpInfo(request, null));
    }

    /** Authorizes a payment for later capture ({@code POST /payments/authorize}). */
    public TransactionResponse authorize(AuthorizeRequest request) throws RapCoreException {
        return execute(
                "authorize",
                "POST",
                "/payments/authorize",
                request,
                () -> payments.authorizePaymentWithHttpInfo(request, null));
    }

    /** Captures a previously authorized payment. */
    public TransactionResponse capture(String transactionId, CaptureRequest request)
            throws RapCoreException {
        return execute(
                "capture",
                "POST",
                "/payments/{transactionId}/capture",
                request,
                () -> payments.capturePaymentWithHttpInfo(transactionId, request, null));
    }

    /** Voids a previously authorized payment. */
    public TransactionResponse voidPayment(String transactionId, VoidRequest request)
            throws RapCoreException {
        return execute(
                "void",
                "POST",
                "/payments/{transactionId}/void",
                request,
                () -> payments.voidPaymentWithHttpInfo(transactionId, request, null));
    }

    /** Refunds a settled payment. */
    public TransactionResponse refund(String transactionId, RefundRequest request)
            throws RapCoreException {
        return execute(
                "refund",
                "POST",
                "/payments/{transactionId}/refund",
                request,
                () -> payments.refundPaymentWithHttpInfo(transactionId, request, null));
    }

    /** Cancels a refund by merchant transaction id. */
    public TransactionResponse refundCancel(
            String merchantTransactionId, RefundCancelRequest request) throws RapCoreException {
        return execute(
                "refundCancel",
                "POST",
                "/payments/merchant/{merchantTransactionId}/refund-cancel",
                request,
                () ->
                        payments.refundCancelPaymentByMerchantTransactionIdWithHttpInfo(
                                merchantTransactionId, request, null));
    }

    /**
     * The OutcomeUnknown reconciliation procedure (failover-contract §3): polls the
     * merchant-transaction lookup within the caller-bounded {@link ReconcilePolicy} and returns
     * {@link RapReconcileVerdict.Found} or {@link RapReconcileVerdict.NotFoundYet}. ALWAYS branch
     * with a default — verdicts are open for extension (SafeToFailover arrives with platform P-2 as
     * a minor release).
     */
    public RapReconcileVerdict reconcile(String merchantTransactionId, ReconcilePolicy policy)
            throws RapCoreException, InterruptedException {
        return reconciler.reconcile(merchantTransactionId, policy);
    }

    /** The generated payments api, sharing this client's transport and headers. */
    public PaymentsApi payments() {
        return payments;
    }

    /** The generated transactions api, sharing this client's transport and headers. */
    public TransactionsApi transactions() {
        return transactions;
    }

    /** The generated payment-methods api, sharing this client's transport and headers. */
    public PaymentMethodsApi paymentMethods() {
        return paymentMethods;
    }

    /**
     * The generated notify api, sharing this client's transport and headers. (Named {@code
     * notifyApi} because {@code Object.notify()} is final.)
     */
    public NotifyApi notifyApi() {
        return notify;
    }

    private TransactionResponse execute(
            String operation, String method, String path, Object requestModel, CoreCall call)
            throws RapCoreException {
        try {
            ApiResponse<TransactionResponse> response = call.invoke();
            String correlationId = correlationFrom(response.getHeaders());
            LOG.info(
                    "rap.request operation={} status={} correlation={}",
                    operation,
                    response.getStatusCode(),
                    correlationId);
            trace(
                    operation,
                    method,
                    path,
                    response.getStatusCode(),
                    correlationId,
                    requestModel,
                    response.getData());
            return response.getData();
        } catch (ApiException e) {
            throw translate(operation, method, path, requestModel, e);
        }
    }

    private RapCoreException translate(
            String operation, String method, String path, Object requestModel, ApiException e) {
        RapCoreException classified;
        String correlationId = null;
        if (e.getCause() instanceof InterruptedException) {
            Thread.currentThread().interrupt();
            classified = FailureClassifier.classifyInterruption(e.getCause());
        } else if (e.getCode() == 0) {
            // No response was received — transport-level failure; the cause chain
            // carries the never-sent proof, when the stack can give one.
            classified =
                    FailureClassifier.classifyTransportFailure(
                            e.getCause() != null ? e.getCause() : e);
        } else {
            HttpHeaders headers = e.getResponseHeaders();
            correlationId =
                    headers == null
                            ? null
                            : headers.firstValue(RapHeaders.CORRELATION_ID).orElse(null);
            classified =
                    FailureClassifier.classifyResponse(
                            e.getCode(), e.getResponseBody(), apiVersion, correlationId);
        }

        LOG.warn(
                "rap.request failed operation={} class={} status={} code={} correlation={}",
                operation,
                classified.getFailureClass(),
                classified.getStatusCode(),
                classified.getCode(),
                classified.getCorrelationId());
        trace(
                operation,
                method,
                path,
                classified.getStatusCode(),
                classified.getCorrelationId(),
                requestModel,
                null);
        return classified;
    }

    private void trace(
            String operation,
            String method,
            String path,
            Integer status,
            String correlationId,
            Object requestModel,
            Object responseModel) {
        boolean debugPayloads = LOG.isDebugEnabled();
        if (wireTraceHook == null && !debugPayloads) {
            return;
        }
        String scrubbedRequest = scrubModel(requestModel);
        String scrubbedResponse = scrubModel(responseModel);
        if (debugPayloads) {
            // Debug level carries allowlist-scrubbed payloads only (ADR-SDK-020).
            LOG.debug(
                    "rap.request payload operation={} request={} response={}",
                    operation,
                    scrubbedRequest,
                    scrubbedResponse);
        }
        if (wireTraceHook != null) {
            try {
                wireTraceHook.accept(
                        new RapWireTrace(
                                operation,
                                method,
                                path,
                                status,
                                correlationId,
                                null,
                                scrubbedRequest,
                                null,
                                scrubbedResponse));
            } catch (RuntimeException ex) {
                // Observer exceptions are swallowed (runtime-tdd §6).
                LOG.debug("rap.wiretrace hook threw; ignored", ex);
            }
        }
    }

    private String scrubModel(Object model) {
        if (model == null) {
            return null;
        }
        try {
            return RapScrubber.scrubJson(coreMapper.writeValueAsString(model));
        } catch (JsonProcessingException e) {
            return RapScrubber.SCRUBBED;
        }
    }

    private static String correlationFrom(Map<String, List<String>> headers) {
        if (headers == null) {
            return null;
        }
        for (Map.Entry<String, List<String>> entry : headers.entrySet()) {
            if (RapHeaders.CORRELATION_ID.equalsIgnoreCase(entry.getKey())
                    && entry.getValue() != null
                    && !entry.getValue().isEmpty()) {
                return entry.getValue().get(0);
            }
        }
        return null;
    }

    @FunctionalInterface
    private interface CoreCall {
        ApiResponse<TransactionResponse> invoke() throws ApiException;
    }

    /** Hands one fixed HttpClient instance to every generated api class. */
    private static final class FixedHttpClientBuilder implements HttpClient.Builder {

        private final HttpClient client;

        FixedHttpClientBuilder(HttpClient client) {
            this.client = client;
        }

        @Override
        public HttpClient.Builder cookieHandler(CookieHandler cookieHandler) {
            return this;
        }

        @Override
        public HttpClient.Builder connectTimeout(Duration duration) {
            return this;
        }

        @Override
        public HttpClient.Builder sslContext(SSLContext sslContext) {
            return this;
        }

        @Override
        public HttpClient.Builder sslParameters(SSLParameters sslParameters) {
            return this;
        }

        @Override
        public HttpClient.Builder executor(Executor executor) {
            return this;
        }

        @Override
        public HttpClient.Builder followRedirects(HttpClient.Redirect policy) {
            return this;
        }

        @Override
        public HttpClient.Builder version(HttpClient.Version version) {
            return this;
        }

        @Override
        public HttpClient.Builder priority(int priority) {
            return this;
        }

        @Override
        public HttpClient.Builder proxy(ProxySelector proxySelector) {
            return this;
        }

        @Override
        public HttpClient.Builder authenticator(Authenticator authenticator) {
            return this;
        }

        @Override
        public HttpClient build() {
            return client;
        }
    }

    /** Configures and creates one immutable {@link RapClient} (runtime-tdd §1). */
    public static final class Builder {

        private String apiKey;
        private String baseUrl = "https://api.revaly.co";
        private String apiVersion = "2.1";
        private Duration connectTimeout;
        private Duration overallDeadline;
        private String userAgentSuffix;
        private Consumer<RapWireTrace> wireTraceHook;
        private HttpClient transport;

        private Builder() {}

        /**
         * The merchant API key (required). Sent as {@code Authorization: ApiKey <key>} on every
         * request; never persisted, never logged, never present in exception messages
         * (ADR-SDK-020).
         */
        public Builder apiKey(String apiKey) {
            this.apiKey = apiKey;
            return this;
        }

        /**
         * The API base URL. Defaults to production ({@code https://api.revaly.co}); point it at the
         * Sandbox URL for testing.
         */
        public Builder baseUrl(String baseUrl) {
            this.baseUrl = baseUrl;
            return this;
        }

        /**
         * The API contract version, pinned via {@code X-Api-Version} on every request. Default
         * {@code "2.1"}; {@code "2.0"} is selectable. <b>Behavioural difference on "2.0":</b> the
         * {@code ErrorResponse.code} field is not part of the 2.0 documented contract, so the
         * fast-failover class narrows to client-provable never-sent failures only — a 503 with
         * {@code code: not_processed} classifies as OutcomeUnknown (reconcile) instead of
         * TransientFailure (immediate failover). Pin 2.1 unless you have a frozen 2.0 integration.
         */
        public Builder apiVersion(String apiVersion) {
            this.apiVersion = apiVersion;
            return this;
        }

        /**
         * TCP/TLS connection-establishment timeout. Default: none set by this SDK — the transport's
         * own default applies. The telemetry-derived recommended default is OQ-6
         * (docs/open-items.md) and lands before Wave-1 GA; this SDK deliberately does not invent
         * one.
         */
        public Builder connectTimeout(Duration connectTimeout) {
            this.connectTimeout = connectTimeout;
            return this;
        }

        /**
         * Overall per-request deadline. Expiry after the request was sent classifies as
         * <b>OutcomeUnknown</b> (reconcile before acting) — never TransientFailure. Default: none
         * set by this SDK — {@code java.net.http} waits indefinitely for a response when no timeout
         * is set. The telemetry-derived recommended default is OQ-6 (docs/open-items.md); this SDK
         * deliberately does not invent one.
         */
        public Builder overallDeadline(Duration overallDeadline) {
            this.overallDeadline = overallDeadline;
            return this;
        }

        /**
         * Optional merchant product token APPENDED after the SDK's User-Agent token (ADR-SDK-005:
         * the SDK prefix stays first and intact; it can never be replaced or suppressed).
         */
        public Builder userAgentSuffix(String userAgentSuffix) {
            this.userAgentSuffix = userAgentSuffix;
            return this;
        }

        /**
         * Optional request/response observer for Enablement escalations. Receives payloads already
         * scrubbed by the runtime's central allowlist scrubber — never raw material. Observer
         * exceptions are swallowed.
         */
        public Builder wireTraceHook(Consumer<RapWireTrace> wireTraceHook) {
            this.wireTraceHook = wireTraceHook;
            return this;
        }

        /**
         * Replacement wire transport. Intended for the mock transport ({@code
         * co.revaly.sdk.testing.RapMockTransport}) in merchant tests; null uses the real HTTP
         * transport.
         */
        public Builder transport(HttpClient transport) {
            this.transport = transport;
            return this;
        }

        public RapClient build() {
            if (apiKey == null || apiKey.trim().isEmpty()) {
                throw new IllegalArgumentException("apiKey is required");
            }
            if (baseUrl == null || baseUrl.trim().isEmpty()) {
                throw new IllegalArgumentException("baseUrl is required");
            }
            if (apiVersion == null || apiVersion.trim().isEmpty()) {
                throw new IllegalArgumentException("apiVersion is required");
            }
            return new RapClient(this);
        }
    }
}
