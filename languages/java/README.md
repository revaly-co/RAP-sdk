# Revaly RAP SDK for Java

Server-side Java SDK for the RAP V2 API (`api.revaly.co`): the full payments / payment
methods / transactions / notify surface, plus the pieces that make failover **safe** —
three typed failure classes, a bounded reconcile helper, values-free logging, and a
first-class mock transport.

**Requires:** JDK 11+. **Depends on:** the generated core (`revaly-sdk-core`, built in
this repo), Jackson, SLF4J (bring your own binding).

> **Install:** from Maven Central —
>
> ```xml
> <dependency>
>     <groupId>co.revaly</groupId>
>     <artifactId>revaly-sdk</artifactId>
>     <version>0.5.1</version><!-- or newer -->
> </dependency>
> ```
>
> Artifacts are GPG-signed (`packages@revaly.co`). GitHub release artifacts remain the
> provenance anchor and fallback channel.

## Why the error classes matter (read this first)

A failed `POST /payments` does **not** mean the payment didn't happen. If you blind-fail-over
to your own gateway on an ambiguous failure, the cardholder can be charged **twice**. Every
SDK failure is therefore classified into exactly one of three classes, and each class has
one correct reaction:

| You caught | What it means | What you do |
| --- | --- | --- |
| `PermanentRejectionException` | Received and rejected (400/401/403/404/422) | Fix or decline — failing over reproduces the same rejection anywhere. |
| `TransientFailureException` | **Definitively not processed** (provably never sent, or 503 + `code: not_processed`) | Route to your own gateway immediately. |
| `OutcomeUnknownException` | **May have been processed** (deadline after send, 5xx, ambiguous) | **Reconcile before acting** (below). |

## Quickstart (sandbox key → first charge, ≤ 15 minutes)

```java
import co.revaly.sdk.RapClient;
import co.revaly.sdk.core.model.CreditCard;
import co.revaly.sdk.core.model.PaymentMethod;
import co.revaly.sdk.core.model.PaymentRequest;
import co.revaly.sdk.core.model.TransactionResponse;
import co.revaly.sdk.errors.OutcomeUnknownException;
import co.revaly.sdk.errors.PermanentRejectionException;
import co.revaly.sdk.errors.RapCoreException;
import co.revaly.sdk.errors.TransientFailureException;
import co.revaly.sdk.reconcile.RapReconcileVerdict;
import co.revaly.sdk.reconcile.RapTransactionOutcome;
import co.revaly.sdk.reconcile.ReconcilePolicy;
import java.time.Duration;

public class Quickstart {
    public static void main(String[] args) throws RapCoreException, InterruptedException {
        RapClient client = RapClient.builder()
                // Enablement-issued sandbox-scoped key. Sandbox and live share the same
                // URL — your key's scope selects the environment (no separate sandbox host).
                .apiKey(System.getenv("REVALY_API_KEY"))
                .connectTimeout(Duration.ofSeconds(2))      // no SDK default — see timeout note below
                // overallDeadline not set — the 75 s ADR-SDK-027 default applies; tune it to your
                // checkout budget with .overallDeadline(...) (see the Timeouts note below)
                .build();

        // merchantTransactionId is required on every payment request — it is also the
        // key the reconcile procedure looks the payment up by. Make it unique and durable.
        String merchantTransactionId = "order-1042-attempt-1";
        PaymentRequest request = new PaymentRequest()
                .merchantTransactionId(merchantTransactionId)
                .amount(1999L)
                .currency("USD")
                // orderId + email: the sandbox simulator requires both for an approval.
                .orderId(merchantTransactionId)
                // paymentMethodType is omitted — inferred from the one populated
                // method object. creditCard requires a cardholder name.
                .paymentMethod(new PaymentMethod()
                        .fullName("Ada Lovelace")
                        .email("ada@example.com")
                        .creditCard(new CreditCard()
                                .number("4111111111111111") // sandbox test card
                                .expiryMonth("12")
                                .expiryYear("2030")
                                .cardVerificationCode("123")));

        try {
            TransactionResponse response = client.charge(request);
            System.out.println("charged, status=" + response.getTransactionStatus());
            // response.getPaymentMethod().getVaultToken() (spec >= 2.4.0) ties this charge
            // back to the stored credential it ran against — set only when a vault credential
            // was used, and it may reflect an Account Updater roll. Treat it as optional;
            // absence proves nothing.

        } catch (PermanentRejectionException e) {
            // Received and rejected — fix the request or decline the order.
            // Failing over reproduces the same rejection at any gateway.
            System.err.println("rejected [" + e.getStatusCode() + "] " + e.getErrorMessage());

        } catch (TransientFailureException e) {
            // Definitively NOT processed at RAP-core — safe to fail over immediately.
            routeToOwnGateway(request);

        } catch (OutcomeUnknownException e) {
            // May have been processed — reconcile BEFORE acting (double-charge hazard).
            RapReconcileVerdict verdict = client.reconcile(
                    merchantTransactionId,
                    ReconcilePolicy.builder()
                            .maxAttempts(6)
                            .overallBudget(Duration.ofSeconds(30))
                            .initialDelay(Duration.ofSeconds(1))
                            .build());

            if (verdict instanceof RapReconcileVerdict.Found) {
                RapReconcileVerdict.Found found = (RapReconcileVerdict.Found) verdict;
                switch (found.getOutcome()) {
                    case APPROVED:
                        // The payment already succeeded at RAP-core.
                        // Failing over here would charge the cardholder twice.
                        break;
                    case DECLINED:
                    case ERROR:
                        // Terminal at RAP-core — your own gateway is now safe,
                        // per your risk policy.
                        routeToOwnGateway(request);
                        break;
                    case PENDING:
                        // Accepted, not yet visible as a transaction — hold and
                        // re-poll (call reconcile again).
                        break;
                    default:
                        // REQUIRED default: outcomes are open for extension.
                        escalateToSupport(merchantTransactionId, verdict.getCorrelationId());
                        break;
                }
            } else if (verdict instanceof RapReconcileVerdict.NotFoundYet) {
                // NOT proof of absence — visibility is asynchronous and unbounded.
                // Hold and escalate per YOUR policy; quote the correlation id.
                RapReconcileVerdict.NotFoundYet nf = (RapReconcileVerdict.NotFoundYet) verdict;
                escalateToSupport(merchantTransactionId, nf.getCorrelationId());
            } else {
                // REQUIRED default: verdict types are open for extension —
                // SafeToFailover arrives with platform P-2 as a minor release.
                escalateToSupport(merchantTransactionId, verdict.getCorrelationId());
            }
        }
    }

    static void routeToOwnGateway(PaymentRequest request) { /* your failover path */ }
    static void escalateToSupport(String id, String correlationId) { /* your escalation */ }
}
```

### Timeouts

The overall deadline defaults to **75 seconds**, ratified from production latency
telemetry (ADR-SDK-027): it clears every observed gateway tail cluster (the worst
non-hung tail seen in 14 fleet days was 64 s), clips ≲0.007% of charges, and still
classifies well before the platform's own ≈100 s ceiling. Tighten it per your checkout
budget (RAP routes gateways server-side, so the default must cover the slowest common
class — per-gateway tuning is your override), or disable it with `noOverallDeadline()`.
The connect timeout defaults to **10 seconds**, ratified from the OQ-11 edge
verification (ADR-SDK-029): roughly 25× the observed cold client→edge TLS envelope, and
65 s below the overall deadline so the connect bound always fires first during connect.
Expiry surfaces as `HttpConnectTimeoutException` — provably never-sent — and classifies
as `TransientFailure` (safe to fail over immediately); disable with `noConnectTimeout()`.
The one rule that is not yours to choose: an overall deadline that expires **after the
request was sent** classifies as `OutcomeUnknown` — reconcile, never resubmit.

One semantic caveat: the deadline bounds **time-to-response**, per `java.net.http`'s
`HttpRequest.timeout()` semantics — the wait through the response status and headers. A
response body that stalls *after* headers arrive is not bounded by it; such a stall
surfaces as `OutcomeUnknown` through a transport failure when the connection dies. If you
need a hard wall-clock bound on the whole call, enforce it in your own execution layer —
and treat expiry there exactly like any `OutcomeUnknown`: reconcile, never resubmit.

### API versioning

The client pins `X-Api-Version: 2.1` by default (recommended). If you pin `"2.0"`, the
`ErrorResponse.code` field is not part of that contract, so the fast-failover class
narrows to client-provable never-sent failures only — a 503 with `code: not_processed`
classifies as `OutcomeUnknown` (reconcile) instead of `TransientFailure`.

## Testing your failover handler — no network

The mock transport is a first-class part of the SDK. It simulates every row of the
failover-contract classification table, both reconcile verdicts, and the pending state —
with taxonomy-named builders and synthetic data only:

```java
import co.revaly.sdk.testing.RapMockTransport;

RapMockTransport mock = new RapMockTransport();
mock.charge().returnsNotProcessed503();               // breaker open: fast-failover row
mock.reconcile("order-1042-attempt-1")
        .notFoundYet(2)                               // two polls: not visible yet
        .thenFoundApproved();                         // third poll: it was approved

RapClient client = RapClient.builder()
        .apiKey("test-key")
        .transport(mock)                              // no network from here on
        .build();

// exercise your handler; assert on mock.getRequests() (method, path, headers, body)
```

Scriptable outcomes include: `returnsApproved/Declined/ErrorOutcome`,
`returnsPermanentRejection(status)`, `returnsNotProcessed503`, `returnsBare503`,
`returnsServerError/BadGateway/GatewayTimeout`, `throwsConnectionRefused/ConnectTimeout/
SslHandshakeFailure` (never-sent proofs), `throwsTimeoutAfterSend/ConnectionReset`
(ambiguous), `notFoundYet(n)`, `pending()`, and a `returns(status, body, headers)` escape
hatch. The mock asserts the SDK User-Agent leads every request.

## Logging & debugging

- The SDK logs through **SLF4J** (`co.revaly.sdk.*` loggers); bind whatever backend you
  use. Default output is **values-free**: operation, status, failure class, correlation
  id — never payloads, never keys.
- `DEBUG` adds payloads that passed the central **allowlist scrubber** — PAN/CVV/PII and
  unknown fields are `[scrubbed]`.
- Every response and every typed error carries the **`X-Correlation-ID`**
  (`getCorrelationId()`); quote it in support tickets — it joins your request directly to
  RAP-core telemetry.
- A `wireTraceHook` receives scrubbed request/response observations for Enablement
  escalations; it never sees raw material.

## Design guarantees

Failures classify; the caller decides.

- **Each charge is sent exactly once.** Retry policy stays yours, with the
  classification that makes it safe to exercise.
- **Every call stands alone** — no cross-request state, no circuit breaker, so behaviour
  under load is the behaviour you tested.
- **The reconcile re-poll you bound is the only loop the SDK owns.**
- **Classification rests on evidence only**: HTTP status and `ErrorResponse.code`. Message
  text and latency are reported to you and excluded from the verdict.
- **Recovery beyond this boundary belongs to RAP-core** — resubmission and
  `bypassPlatform` are platform-internal, so a payment's outcome stays unambiguous.

Normative form: [`docs/failover-contract.md`](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-contract.md) §5 and
Appendix A.

## Beyond payments

The full generated V2 surface is re-exported through the client:
`client.payments()`, `client.transactions()`, `client.paymentMethods()`,
`client.notifyApi()` — same transport, same auth, same User-Agent, same version pin.

One logging caution on this surface: raw core operations throw the generator's
`ApiException`, not the three typed classes — and `ApiException.getMessage()` embeds the
raw HTTP response body verbatim (`"<operation> call failed with: <status> - <body>"`).
Response bodies can contain PII (names, emails, masked card data): never log raw core
exception messages or bodies; log the correlation id and the typed runtime errors
(values-free by design) instead.

## Where to go next

- [Failover cookbook](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-cookbook.md) — recipes for each outcome, choosing a
  reconcile policy, testing offline, debugging with correlation ids.
- [Failover contract](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-contract.md) — the normative specification, with
  sequence diagrams and the verbatim prohibitions in Appendix A.
- [AGENTS.md](https://github.com/revaly-co/RAP-sdk/blob/main/AGENTS.md) — the whole contract on one page, for AI coding agents.
- [Support](https://github.com/revaly-co/RAP-sdk/blob/main/SUPPORT.md) · [Contributing](https://github.com/revaly-co/RAP-sdk/blob/main/CONTRIBUTING.md) · [Security](https://github.com/revaly-co/RAP-sdk/blob/main/SECURITY.md)
