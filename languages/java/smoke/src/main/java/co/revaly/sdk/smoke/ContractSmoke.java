package co.revaly.sdk.smoke;

import co.revaly.sdk.RapClient;
import co.revaly.sdk.core.model.CreditCard;
import co.revaly.sdk.core.model.PaymentMethod;
import co.revaly.sdk.core.model.PaymentRequest;
import co.revaly.sdk.core.model.Recovery;
import co.revaly.sdk.core.model.TransactionResponse;
import co.revaly.sdk.errors.PermanentRejectionException;
import co.revaly.sdk.errors.RapCoreException;
import co.revaly.sdk.errors.TransientFailureException;
import co.revaly.sdk.reconcile.RapReconcileVerdict;
import co.revaly.sdk.reconcile.RapTransactionOutcome;
import co.revaly.sdk.reconcile.ReconcilePolicy;
import java.security.SecureRandom;
import java.time.Duration;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Stage-4 contract smoke (ADR-SDK-024, pipeline stage 4): a thin, live runtime-contract check of
 * THIS SDK against the environment named by RAP_SMOKE_BASE_URL / RAP_SMOKE_API_KEY (interim:
 * Backbone staging; at GA: the merchant sandbox key-scope). Its single purpose is proving the SDK's
 * classification against reality — it deliberately does not replicate platform test coverage.
 *
 * <p>Environment contract (same across all six languages): RAP_SMOKE_BASE_URL (required),
 * RAP_SMOKE_API_KEY (required), RAP_SMOKE_GATEWAY_ROUTING_ID (optional — included in charge
 * payloads when set), RAP_SMOKE_FAULT_INJECT (optional — sent as the platform's
 * X-Backbone-Fault-Inject header to trigger the 503+not_processed row; the scenario SKIPs when
 * unset).
 *
 * <p>Scenarios mirror the quickstart shape (README). Output is values-free (ADR-SDK-020):
 * identifiers, statuses, classes and correlation ids only — never payload values, never the key,
 * never the target host.
 *
 * <p>Exit codes: 0 all pass (skips allowed) · 1 at least one failed · 2 not configured.
 */
public final class ContractSmoke {

    /**
     * The platform's executor fault seam (Backbone ADR 014 test affordance): value "pre-dispatch"
     * makes the charge fail between intent reservation and gateway dispatch — the only
     * deterministic live trigger for the 503 + code=not_processed fast-failover row.
     */
    private static final String FAULT_INJECT_HEADER = "X-Backbone-Fault-Inject";

    // The fault-injected charge must not present as a first attempt — the route it takes
    // depends on it. See charge-not-processed-503.
    private static final int FAULT_RETRY_COUNT = 1;

    // One synthetic test PAN; the EXPIRY drives the outcome (staging-verified
    // matrix 2026-07-18: 12/2027 approves, 12/2020 declines).
    private static final String TEST_PAN = "4111111111111111";

    private static final SecureRandom RANDOM = new SecureRandom();

    private ContractSmoke() {}

    /** One smoke scenario: returns the PASS detail suffix, or throws. */
    private interface Scenario {
        String run() throws Exception;
    }

    /** A scenario assertion failure (values-free message). */
    private static final class SmokeFailure extends RuntimeException {
        SmokeFailure(String message) {
            super(message);
        }
    }

    /** A scenario that cannot run in this environment (reported, never silent). */
    private static final class SmokeSkip extends RuntimeException {
        SmokeSkip(String reason) {
            super(reason);
        }
    }

    public static void main(String[] args) {
        String baseUrl = System.getenv("RAP_SMOKE_BASE_URL");
        String apiKey = System.getenv("RAP_SMOKE_API_KEY");
        String routingId = System.getenv("RAP_SMOKE_GATEWAY_ROUTING_ID");
        String faultValue = System.getenv("RAP_SMOKE_FAULT_INJECT");
        if (isBlank(baseUrl) || isBlank(apiKey)) {
            System.err.println(
                    "smoke: RAP_SMOKE_BASE_URL and RAP_SMOKE_API_KEY must be set (ADR-SDK-024)"
                            + " — refusing to run.");
            System.exit(2);
        }

        // One client per configuration, quickstart-shaped. The wire-trace hook
        // is the designed observer for correlation ids on the success path
        // (DX §c); events arrive already scrubbed by the runtime.
        AtomicReference<String> lastCorrelation = new AtomicReference<>();
        RapClient client =
                RapClient.builder()
                        .apiKey(apiKey)
                        .baseUrl(baseUrl)
                        .connectTimeout(Duration.ofSeconds(5))
                        .overallDeadline(Duration.ofSeconds(15))
                        .wireTraceHook(trace -> lastCorrelation.set(trace.getCorrelationId()))
                        .build();

        // A separately configured client whose key is a synthetic invalid
        // value — the auth-rejection row.
        RapClient badKeyClient =
                RapClient.builder()
                        .apiKey("sk_smoke_synthetic_invalid")
                        .baseUrl(baseUrl)
                        .connectTimeout(Duration.ofSeconds(5))
                        .overallDeadline(Duration.ofSeconds(15))
                        .build();

        // A client whose transport stamps the platform's fault-inject header —
        // every charge through it deterministically fails pre-dispatch
        // (503 + code=not_processed). Only built when the scenario is enabled.
        RapClient faultClient =
                isBlank(faultValue)
                        ? null
                        : RapClient.builder()
                                .apiKey(apiKey)
                                .baseUrl(baseUrl)
                                .overallDeadline(Duration.ofSeconds(15))
                                .transport(
                                        new HeaderInjectingHttpClient(
                                                FAULT_INJECT_HEADER, faultValue))
                                .build();

        // Charged ids feed the reconcile scenarios: the verdicts — through the
        // runtime's own outcome mapping — are the proof the charge outcomes
        // were what the smoke claims.
        String chargedId = freshId("charge");
        String declinedId = freshId("decline");

        Map<String, Scenario> scenarios = new LinkedHashMap<>();

        scenarios.put(
                "charge-approved",
                () -> {
                    TransactionResponse transaction =
                            client.charge(
                                    buildCharge(chargedId, TEST_PAN, "2027", routingId, true));
                    if (isBlank(transaction.getTransactionId())) {
                        throw new SmokeFailure("transactionId is empty on the success surface");
                    }
                    // Assert the OUTCOME, not just that a transaction bound: a
                    // decline arrives on this same success surface.
                    if (!Integer.valueOf(1).equals(transaction.getTransactionStatus())) {
                        throw new SmokeFailure(
                                "expected transactionStatus=1 (approved), got "
                                        + transaction.getTransactionStatus());
                    }
                    if (isBlank(lastCorrelation.get())) {
                        throw new SmokeFailure(
                                "no X-Correlation-ID observed on the success path (DX §c)");
                    }
                    return String.format(
                            " (txn=%s correlation=%s)",
                            transaction.getTransactionId(), lastCorrelation.get());
                });

        scenarios.put(
                "charge-declined",
                () -> {
                    // An expired expiry declines deterministically (same PAN). A decline is
                    // a business outcome on the SUCCESS surface — not a
                    // failure class; reconcile-found-declined proves the
                    // mapping below.
                    TransactionResponse transaction =
                            client.charge(
                                    buildCharge(declinedId, TEST_PAN, "2020", routingId, true));
                    if (isBlank(transaction.getTransactionId())) {
                        throw new SmokeFailure(
                                "transactionId is empty on the declined-charge surface");
                    }
                    // Assert the decline actually happened — a gateway that approves
                    // the expired card would otherwise slip through to
                    // reconcile-found-declined.
                    if (!Integer.valueOf(2).equals(transaction.getTransactionStatus())) {
                        throw new SmokeFailure(
                                "expected transactionStatus=2 (declined), got "
                                        + transaction.getTransactionStatus()
                                        + " — the staging gateway must be one where"
                                        + " expiry drives the outcome");
                    }
                    if (isBlank(lastCorrelation.get())) {
                        throw new SmokeFailure(
                                "no X-Correlation-ID observed on the declined-charge path"
                                        + " (DX §c)");
                    }
                    return String.format(
                            " (txn=%s correlation=%s)",
                            transaction.getTransactionId(), lastCorrelation.get());
                });

        scenarios.put(
                "charge-validation-rejected",
                () -> {
                    // An empty card number passes every client-side model but
                    // fails the server's required-field validation — the
                    // rejection is proven to come from reality (HTTP 400; 4xx
                    // carries no code).
                    try {
                        client.charge(
                                buildCharge(
                                        freshId("validation"), TEST_PAN, "2027", routingId, false));
                    } catch (PermanentRejectionException rejection) {
                        Integer status = rejection.getStatusCode();
                        if (status == null || (status != 400 && status != 422)) {
                            throw new SmokeFailure("expected HTTP 400/422, got " + status);
                        }
                        if (isBlank(rejection.getCorrelationId())) {
                            throw new SmokeFailure("no X-Correlation-ID on the rejection (DX §c)");
                        }
                        return String.format(
                                " (status=%d correlation=%s)",
                                status, rejection.getCorrelationId());
                    }
                    throw new SmokeFailure(
                            "server accepted a nameless charge — expected"
                                    + " PermanentRejectionException");
                });

        scenarios.put(
                "charge-auth-rejected",
                () -> {
                    try {
                        badKeyClient.charge(
                                buildCharge(freshId("auth"), TEST_PAN, "2027", routingId, true));
                    } catch (PermanentRejectionException rejection) {
                        Integer status = rejection.getStatusCode();
                        if (status == null || (status != 401 && status != 403)) {
                            throw new SmokeFailure("expected HTTP 401/403, got " + status);
                        }
                        if (isBlank(rejection.getCorrelationId())) {
                            throw new SmokeFailure(
                                    "no X-Correlation-ID on the auth rejection (DX §c)");
                        }
                        return String.format(
                                " (status=%d correlation=%s)",
                                status, rejection.getCorrelationId());
                    }
                    throw new SmokeFailure(
                            "server accepted a synthetic invalid key — expected"
                                    + " PermanentRejectionException");
                });

        scenarios.put(
                "charge-not-processed-503",
                () -> {
                    // The fast-failover row (503 + code=not_processed): valid
                    // input cannot reach it deterministically, so the
                    // platform's fault injector fails the charge pre-dispatch.
                    // TransientFailureException is the ONLY acceptable class
                    // here — it is the row that licenses immediate failover.
                    if (faultClient == null) {
                        throw new SmokeSkip(
                                "RAP_SMOKE_FAULT_INJECT not set (injector is staging-only)");
                    }
                    // retryCount > 0 keeps this charge on the route that carries the seam.
                    // Backbone admits only FIRST attempts to the direct path
                    // (DirectPathAttemptEligibility.IsFirstAttempt == "recovery.retryCount is
                    // not > 0"), and the pre-dispatch injector exists only on the TransactionApi
                    // dispatch path — so on a direct-path-enrolled account a first-attempt charge
                    // takes the direct-send fork, never reaches the injector, and approves
                    // (nightly 30983100997: red 6/6, 2026-08-05).
                    PaymentRequest faultCharge =
                            buildCharge(freshId("fault"), TEST_PAN, "2027", routingId, true);
                    faultCharge.recovery(new Recovery().retryCount(FAULT_RETRY_COUNT));
                    try {
                        faultClient.charge(faultCharge);
                    } catch (TransientFailureException transientFailure) {
                        Integer status = transientFailure.getStatusCode();
                        if (status == null || status != 503) {
                            throw new SmokeFailure("expected HTTP 503, got " + status);
                        }
                        if (!"not_processed".equals(transientFailure.getCode())) {
                            throw new SmokeFailure(
                                    "expected code=not_processed, got \""
                                            + transientFailure.getCode()
                                            + "\"");
                        }
                        if (isBlank(transientFailure.getCorrelationId())) {
                            throw new SmokeFailure(
                                    "no X-Correlation-ID on the not-processed failure (DX §c)");
                        }
                        return String.format(
                                " (status=503 code=%s correlation=%s)",
                                transientFailure.getCode(), transientFailure.getCorrelationId());
                    }
                    throw new SmokeFailure(
                            "fault-injected charge succeeded — expected"
                                    + " TransientFailureException");
                });

        scenarios.put(
                "reconcile-found-approved",
                () -> {
                    // Found(APPROVED) through the runtime's own outcome
                    // mapping is the approval proof for the first charge;
                    // visibility is asynchronous, hence the budget.
                    RapReconcileVerdict verdict =
                            client.reconcile(
                                    chargedId,
                                    new ReconcilePolicy(
                                            5, Duration.ofSeconds(30), Duration.ofSeconds(1)));
                    return expectFound(verdict, RapTransactionOutcome.APPROVED);
                });

        scenarios.put(
                "reconcile-found-declined",
                () -> {
                    // The declined charge must reconcile as Found(DECLINED) —
                    // the outcome branch that tells a merchant their own
                    // gateway is safe.
                    RapReconcileVerdict verdict =
                            client.reconcile(
                                    declinedId,
                                    new ReconcilePolicy(
                                            5, Duration.ofSeconds(30), Duration.ofSeconds(1)));
                    return expectFound(verdict, RapTransactionOutcome.DECLINED);
                });

        scenarios.put(
                "reconcile-not-found-yet",
                () -> {
                    // A fresh, never-used merchantTransactionId (ADR-SDK-024):
                    // the only correct verdict is NotFoundYet, and it must
                    // come from real 404s — not from a transport that never
                    // reached the API.
                    RapReconcileVerdict verdict =
                            client.reconcile(
                                    freshId("absent"),
                                    new ReconcilePolicy(
                                            2, Duration.ofSeconds(10), Duration.ofMillis(500)));
                    if (verdict instanceof RapReconcileVerdict.NotFoundYet) {
                        RapReconcileVerdict.NotFoundYet notFound =
                                (RapReconcileVerdict.NotFoundYet) verdict;
                        Integer lastStatus = notFound.getLastHttpStatus();
                        if (lastStatus == null || lastStatus != 404) {
                            throw new SmokeFailure(
                                    "expected last HTTP status 404, got " + lastStatus);
                        }
                        if (isBlank(notFound.getCorrelationId())) {
                            throw new SmokeFailure(
                                    "no X-Correlation-ID on the NotFoundYet verdict (DX §c)");
                        }
                        return String.format(
                                " (attempts=%d correlation=%s)",
                                notFound.getAttempts(), notFound.getCorrelationId());
                    }
                    if (verdict instanceof RapReconcileVerdict.Found) {
                        throw new SmokeFailure("a never-used id reconciled as Found");
                    }
                    throw new SmokeFailure(
                            "unrecognized verdict " + verdict.getClass().getSimpleName());
                });

        System.out.printf("RAP contract smoke (java): %d scenarios%n", scenarios.size());
        int failures = 0;
        int skips = 0;
        for (Map.Entry<String, Scenario> entry : scenarios.entrySet()) {
            String name = entry.getKey();
            try {
                String detail = entry.getValue().run();
                System.out.printf("PASS %s%s%n", name, detail);
            } catch (SmokeSkip skip) {
                skips++;
                System.out.printf("SKIP %s (%s)%n", name, skip.getMessage());
            } catch (SmokeFailure failure) {
                failures++;
                System.out.printf("FAIL %s: %s%n", name, failure.getMessage());
            } catch (RapCoreException rapFailure) {
                // Typed-class messages are values-free by construction
                // (class, status, code, correlation only).
                failures++;
                System.out.printf("FAIL %s: unexpected %s%n", name, rapFailure.getMessage());
            } catch (Exception unexpected) {
                // Never print raw exception messages — transport error chains
                // can carry endpoint details into CI logs.
                failures++;
                System.out.printf(
                        "FAIL %s: unexpected %s%n", name, unexpected.getClass().getSimpleName());
            }
        }

        int passed = scenarios.size() - failures - skips;
        if (failures > 0) {
            System.out.printf(
                    "RESULT: FAIL (%d/%d passed, %d skipped)%n", passed, scenarios.size(), skips);
            System.exit(1);
        }
        System.out.printf(
                "RESULT: PASS (%d/%d passed, %d skipped)%n", passed, scenarios.size(), skips);
    }

    /**
     * Charge request with the minimal live-approving field set (staging-verified 2026-07-18): a
     * cardholder name is SERVER-required for creditCard (per-type rule, spec-documented since
     * 2.3.0); paymentMethodType is optional since spec 2.3.0 (Backbone #251 inference) — sent
     * explicitly here to keep the wire shape deterministic across the six languages. orderId +
     * email are additionally required by the staging simulator for an approval. Synthetic test
     * cards only.
     */
    private static PaymentRequest buildCharge(
            String merchantTransactionId,
            String pan,
            String expiryYear,
            String routingId,
            boolean withName) {
        PaymentRequest request =
                new PaymentRequest()
                        .amount(1999L)
                        .merchantTransactionId(merchantTransactionId)
                        .paymentMethodType(PaymentRequest.PaymentMethodTypeEnum.CREDIT_CARD)
                        .currency("USD")
                        .orderId(merchantTransactionId)
                        .paymentMethod(
                                new PaymentMethod()
                                        .fullName(withName ? "Smoke Test" : null)
                                        .email("smoke@example.com")
                                        .creditCard(
                                                new CreditCard()
                                                        .number(pan)
                                                        .expiryMonth("12")
                                                        .expiryYear(expiryYear)
                                                        .cardVerificationCode("123")));
        if (!isBlank(routingId)) {
            request.gatewayRoutingId(routingId);
        }
        return request;
    }

    /**
     * Asserts a Found verdict carrying the wanted outcome and a correlation id. The verdict set is
     * open — an unrecognized verdict is a real finding here, not a pass.
     */
    private static String expectFound(RapReconcileVerdict verdict, RapTransactionOutcome want) {
        if (verdict instanceof RapReconcileVerdict.Found) {
            RapReconcileVerdict.Found found = (RapReconcileVerdict.Found) verdict;
            if (found.getOutcome() != want) {
                throw new SmokeFailure("expected outcome " + want + ", got " + found.getOutcome());
            }
            if (isBlank(found.getCorrelationId())) {
                throw new SmokeFailure("no X-Correlation-ID on the Found verdict (DX §c)");
            }
            return String.format(
                    " (outcome=%s correlation=%s)", found.getOutcome(), found.getCorrelationId());
        }
        if (verdict instanceof RapReconcileVerdict.NotFoundYet) {
            RapReconcileVerdict.NotFoundYet notFound = (RapReconcileVerdict.NotFoundYet) verdict;
            throw new SmokeFailure(
                    "charge not visible after "
                            + notFound.getAttempts()
                            + " attempts ("
                            + notFound.getElapsed()
                            + ") — expected Found");
        }
        throw new SmokeFailure("unrecognized verdict " + verdict.getClass().getSimpleName());
    }

    /**
     * Unique merchantTransactionId (≤ 100 chars) — every reconcile scenario uses a fresh one
     * (ADR-SDK-024).
     */
    private static String freshId(String label) {
        return String.format(
                "smoke-java-%s-%d-%08x", label, System.currentTimeMillis(), RANDOM.nextInt());
    }

    private static boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
    }
}
