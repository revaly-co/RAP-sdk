package co.revaly.sdk.reconcile;

import co.revaly.sdk.core.model.PendingTransactionResponse;
import co.revaly.sdk.core.model.TransactionResponse;
import co.revaly.sdk.errors.FailureClassifier;
import co.revaly.sdk.errors.RapCoreException;
import co.revaly.sdk.errors.RapFailureClass;
import co.revaly.sdk.logging.RapScrubber;
import co.revaly.sdk.logging.RapWireTrace;
import co.revaly.sdk.transport.RapHeaders;
import co.revaly.sdk.transport.RapRequestDecorator;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.function.Consumer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The OutcomeUnknown reconciliation procedure (failover-contract §3): GET-only, side-effect-free,
 * caller-bounded — the only loop the runtime owns (ADR-SDK-004).
 *
 * <p>This helper issues the merchant-transaction GET at the raw HTTP level (through the same shared
 * {@link HttpClient} and header decoration as every other SDK request) instead of the generated
 * core binding, for a safety reason: the core's generated oneOf wrapper for this endpoint requires
 * exactly one schema match, but the response schemas are all-optional under Jackson's lenient
 * binding, so valid 200 bodies can multi-match and fail deserialization inside the core (defect
 * flagged for an upstream/template fix — see the PR notes). Classification here therefore works
 * from the RAW body: the required {@code state} field discriminates a pending intent (it exists
 * only on the pending schema), and terminal records bind directly to {@link TransactionResponse} —
 * classify from raw bodies, never core wrappers (repo rule 5).
 */
public final class RapReconciler {

    private static final Logger LOG = LoggerFactory.getLogger(RapReconciler.class);

    private final HttpClient httpClient;
    private final String baseUri;
    private final RapRequestDecorator decorator;
    private final Duration overallDeadline;
    private final String apiVersion;
    private final ObjectMapper coreMapper;
    private final Consumer<RapWireTrace> wireTraceHook;

    public RapReconciler(
            HttpClient httpClient,
            String baseUri,
            RapRequestDecorator decorator,
            Duration overallDeadline,
            String apiVersion,
            ObjectMapper coreMapper,
            Consumer<RapWireTrace> wireTraceHook) {
        this.httpClient = httpClient;
        this.baseUri = baseUri.endsWith("/") ? baseUri.substring(0, baseUri.length() - 1) : baseUri;
        this.decorator = decorator;
        this.overallDeadline = overallDeadline;
        this.apiVersion = apiVersion;
        this.coreMapper = coreMapper;
        this.wireTraceHook = wireTraceHook;
    }

    /**
     * Runs the reconcile loop until a record is visible or the policy bounds are spent.
     *
     * @throws RapCoreException only for a rejected READ that polling can never fix
     *     (PermanentRejection other than 404 — bad credentials, malformed id); 404 is the
     *     NotFoundYet signal, and degraded reads (5xx/timeouts/transport) keep polling within the
     *     budget.
     * @throws InterruptedException when the calling thread is interrupted — the java cancellation
     *     idiom for a blocking helper; no verdict is implied.
     */
    public RapReconcileVerdict reconcile(String merchantTransactionId, ReconcilePolicy policy)
            throws RapCoreException, InterruptedException {
        if (merchantTransactionId == null || merchantTransactionId.trim().isEmpty()) {
            throw new IllegalArgumentException("merchantTransactionId is required");
        }
        if (policy == null) {
            throw new IllegalArgumentException("policy is required");
        }

        String path = "/transactions/merchant/" + urlEncode(merchantTransactionId);
        long startNanos = System.nanoTime();
        int attempts = 0;
        String lastCorrelationId = null;
        Integer lastHttpStatus = null;

        while (true) {
            attempts++;

            HttpResponse<String> response = null;
            try {
                response = send(path);
            } catch (IOException e) {
                // Transport failure on the READ: never-sent proof or not, the WRITE's
                // status is still unknown — keep polling within the caller's budget.
                RapCoreException classified = FailureClassifier.classifyTransportFailure(e);
                LOG.warn(
                        "rap.reconcile attempt {} transport failure ({}); continuing within policy",
                        attempts,
                        classified.getFailureClass());
                trace(path, null, null, null);
            }

            if (response != null) {
                lastHttpStatus = response.statusCode();
                String correlationId =
                        response.headers().firstValue(RapHeaders.CORRELATION_ID).orElse(null);
                if (correlationId != null) {
                    lastCorrelationId = correlationId;
                }
                String body = response.body();
                trace(path, response.statusCode(), correlationId, body);

                if (response.statusCode() / 100 == 2) {
                    RapReconcileVerdict found = readFound(body, lastCorrelationId, attempts);
                    if (found != null) {
                        return found;
                    }
                    // 2xx that did not parse: ambiguous read — poll again within budget.
                } else if (response.statusCode() == 404) {
                    // Not yet visible — the NotFoundYet signal, not an error (§3).
                    LOG.debug("rap.reconcile attempt {} not visible yet (404)", attempts);
                } else {
                    RapCoreException classified =
                            FailureClassifier.classifyResponse(
                                    response.statusCode(), body, apiVersion, correlationId);
                    if (classified.getFailureClass() == RapFailureClass.PERMANENT_REJECTION) {
                        // 400/401/403/422 escape: polling will never fix a rejected read
                        // (bad credentials, malformed id) — the caller must see it.
                        throw classified;
                    }
                    // Degraded read path (5xx/timeout on the GET) — exactly the window
                    // where visibility is widest; keep polling within the budget.
                    LOG.warn(
                            "rap.reconcile attempt {} degraded read [status={} class={}]; continuing within policy",
                            attempts,
                            response.statusCode(),
                            classified.getFailureClass());
                }
            }

            if (attempts >= policy.getMaxAttempts()) {
                break;
            }

            Duration elapsed = Duration.ofNanos(System.nanoTime() - startNanos);
            Duration delay = policy.delayForAttempt(attempts);
            if (elapsed.plus(delay).compareTo(policy.getOverallBudget()) >= 0) {
                break;
            }

            if (!delay.isZero()) {
                Thread.sleep(delay.toMillis());
            }
        }

        Duration elapsed = Duration.ofNanos(System.nanoTime() - startNanos);
        LOG.info(
                "rap.reconcile verdict=NotFoundYet attempts={} elapsedMs={} lastStatus={} correlation={}",
                attempts,
                elapsed.toMillis(),
                lastHttpStatus,
                lastCorrelationId);
        return new RapReconcileVerdict.NotFoundYet(
                attempts, elapsed, lastCorrelationId, lastHttpStatus);
    }

    private HttpResponse<String> send(String path) throws IOException, InterruptedException {
        HttpRequest.Builder builder =
                HttpRequest.newBuilder()
                        .uri(URI.create(baseUri + path))
                        .header("Accept", "application/json")
                        .GET();
        if (overallDeadline != null) {
            builder.timeout(overallDeadline);
        }
        decorator.accept(builder);
        return httpClient.send(builder.build(), HttpResponse.BodyHandlers.ofString());
    }

    /**
     * Maps a 2xx body to a Found verdict from the RAW json. Returns null for a body this SDK cannot
     * read at all (→ poll-continue: an ambiguous read is not a sighting).
     */
    private RapReconcileVerdict readFound(String body, String correlationId, int attempt) {
        JsonNode root;
        try {
            root = coreMapper.readTree(body == null ? "" : body);
        } catch (IOException e) {
            root = null;
        }
        if (root == null || !root.isObject()) {
            LOG.warn(
                    "rap.reconcile attempt {} returned 2xx with an unreadable body; continuing within policy",
                    attempt);
            return null;
        }

        // `state` exists only on the pending schema — its presence is authoritative
        // (the spec marks it the discriminator).
        JsonNode state = root.get("state");
        if (state != null && state.isTextual()) {
            PendingTransactionResponse pending = null;
            try {
                pending = coreMapper.treeToValue(root, PendingTransactionResponse.class);
            } catch (IOException e) {
                // A pending-shaped record this SDK version cannot bind is still a
                // sighting — surface it conservatively rather than polling on.
            }
            if (pending != null) {
                LOG.info(
                        "rap.reconcile verdict=Found outcome=PENDING correlation={}",
                        correlationId);
                return new RapReconcileVerdict.Found(
                        RapTransactionOutcome.PENDING, null, pending, correlationId);
            }
            return new RapReconcileVerdict.Found(
                    RapTransactionOutcome.UNKNOWN, null, null, correlationId);
        }

        // Terminal records bind DIRECTLY to TransactionResponse — never through the
        // core's oneOf wrapper (see the class doc).
        try {
            TransactionResponse transaction =
                    coreMapper.treeToValue(root, TransactionResponse.class);
            RapTransactionOutcome outcome = mapOutcome(transaction.getTransactionStatus());
            LOG.info(
                    "rap.reconcile verdict=Found outcome={} correlation={}",
                    outcome,
                    correlationId);
            return new RapReconcileVerdict.Found(outcome, transaction, null, correlationId);
        } catch (IOException e) {
            // A response shape this SDK version does not recognize (e.g. a grouped
            // envelope, or a post-P-2 variant). Found-but-unmapped is still FOUND.
            return new RapReconcileVerdict.Found(
                    RapTransactionOutcome.UNKNOWN, null, null, correlationId);
        }
    }

    private static RapTransactionOutcome mapOutcome(Integer transactionStatus) {
        if (transactionStatus == null) {
            return RapTransactionOutcome.UNKNOWN;
        }
        switch (transactionStatus) {
            case 1:
                return RapTransactionOutcome.APPROVED;
            case 2:
                return RapTransactionOutcome.DECLINED;
            case 3:
                return RapTransactionOutcome.ERROR;
            default:
                return RapTransactionOutcome.UNKNOWN;
        }
    }

    private void trace(String path, Integer status, String correlationId, String rawResponseBody) {
        if (wireTraceHook == null) {
            return;
        }
        try {
            wireTraceHook.accept(
                    new RapWireTrace(
                            "reconcile",
                            "GET",
                            path,
                            status,
                            correlationId,
                            null,
                            null,
                            null,
                            rawResponseBody == null
                                    ? null
                                    : RapScrubber.scrubJson(rawResponseBody)));
        } catch (RuntimeException e) {
            // Observer exceptions are swallowed (runtime-tdd §6) — tracing must never
            // change payment control flow.
            LOG.debug("rap.wiretrace hook threw; ignored", e);
        }
    }

    private static String urlEncode(String value) {
        return URLEncoder.encode(value, StandardCharsets.UTF_8).replace("+", "%20");
    }
}
