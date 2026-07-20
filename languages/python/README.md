# Revaly RAP SDK for Python

Server-side Python SDK for the RAP V2 API: payments, payment methods, transactions and
notify — with a **merchant-facing failover contract** built in. Every failed payment
call raises exactly one of three typed classes that tell you what you may safely do
next.

> **Package status:** the PyPI name `revaly-sdk` is **[Proposed]** until registry
> provisioning (OQ-3), and registry publish is embargoed — install from the
> per-language GitHub release artifact until then. Requires Python ≥ 3.9.

## Why the error classes matter (read this first)

A failed `charge(...)` does **not** mean the payment didn't happen. If you
blind-fail-over to your own gateway on an ambiguous failure, the cardholder can be
charged **twice**. The SDK classifies every failure so you never have to guess:

| Class | Meaning | What you do |
| --- | --- | --- |
| `RapPermanentRejection` | Received and rejected (400/401/403/404/422) | Fix or decline. **Never fail over** — the same request fails anywhere. |
| `RapTransientFailure` | **Definitively not processed** (provably never sent, or `503` + `code: not_processed`) | Route to your own gateway immediately. |
| `RapOutcomeUnknown` | **May have been processed** (timeout after send, reset, 5xx) | **Reconcile before acting** — see below. |

## Quickstart (sandbox key → first charge, ≤ 15 minutes)

Your API key's scope selects the environment: sandbox and live share the same URL —
there is no separate sandbox host. Use the sandbox-scoped key issued by Enablement.

```bash
# Download revaly-sdk-python.tar.gz from the release, verify its .sha256, then:
pip install ./revaly-sdk-python.tar.gz
```

```python
import os

from revaly_sdk import (
    CreditCard,
    Found,
    NotFoundYet,
    PaymentMethod,
    PaymentRequest,
    RapClient,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransactionOutcome,
    RapTransientFailure,
    ReconcilePolicy,
)

client = RapClient(os.environ["RAP_API_KEY"])

request = PaymentRequest(
    amount=1999,
    currency="USD",
    merchant_transaction_id="order-1042",  # required on every payment — it is your reconcile handle
    # paymentMethodType is omitted — inferred from the one populated method object
    payment_method=PaymentMethod(
        full_name="Ada Lovelace",  # creditCard requires a cardholder name
        credit_card=CreditCard(
            number="4111111111111111",  # sandbox test PAN
            card_verification_code="999",
            expiry_month="12",
            expiry_year="2030",
        )
    ),
)

try:
    transaction = client.charge(request)
    print("approved", transaction.transaction_id)
except RapPermanentRejection as failure:
    # Fix or decline. Never fail over — the same request fails anywhere.
    print("rejected", failure.status, failure.api_error, failure.correlation_id)
except RapTransientFailure:
    # Definitively not processed — route to your own gateway immediately.
    route_to_own_gateway()
except RapOutcomeUnknown:
    # May have been processed — reconcile BEFORE acting (double-charge hazard).
    verdict = client.reconcile(
        "order-1042",
        ReconcilePolicy(max_attempts=5, overall_budget=30.0, initial_delay=0.5),
    )
    if isinstance(verdict, Found):
        # The record IS visible. Found(APPROVED) means the money moved —
        # failing over now would double-charge.
        print("resolved", verdict.outcome, verdict.correlation_id)
    elif isinstance(verdict, NotFoundYet):
        # Not visible YET — absence is not provable in V1. Hold and escalate
        # per your risk policy; do not treat this as "safe to fail over".
        print("hold", verdict.attempts, verdict.last_correlation_id)
    else:
        # Verdicts are open for extension (SafeToFailover arrives with
        # platform P-2 as a minor release). Always keep this branch.
        escalate_to_operator(verdict)
```

### Timeouts

`overall_deadline` defaults to **30 seconds** (`DEFAULT_OVERALL_DEADLINE`) — ratified
from production latency telemetry (ADR-SDK-027): it clips ~1 in 9,500 charges at the
platform's observed tail while staying above the real slow-gateway stall band. Tighten
it per your checkout budget (RAP routes gateways server-side, so the default must
cover the slowest common class), or pass an explicit `overall_deadline=None` to
disable the SDK deadline. `connect_timeout` still ships **no SDK default** — a
client-side value needs edge telemetry (OQ-11). All timeouts are seconds:

```python
client = RapClient(api_key, connect_timeout=3.0, overall_deadline=10.0)
# or per call:
client.charge(request, overall_deadline=5.0)
```

- `overall_deadline` expiry **after send** classifies `RapOutcomeUnknown` (reconcile),
  never TransientFailure.
- `connect_timeout` expiry proves the request never left the client and classifies
  `RapTransientFailure` — urllib3 reports the connect phase distinctly even when only
  an overall deadline is set.

Python has no ambient cancellation token: bound calls with these timeout arguments and
bound reconciliation with the `ReconcilePolicy` budget — that is this SDK's
cancellation idiom.

### API versioning

Requests pin `X-Api-Version: 2.1` by default. `"2.0"` is selectable
(`api_version="2.0"`) but narrows the contract: `ErrorResponse.code` is not part of
the 2.0 documented surface, so a `503` + `not_processed` classifies
`RapOutcomeUnknown` (reconcile) instead of `RapTransientFailure` (immediate failover).
Pin 2.1 unless you have a frozen 2.0 integration.

## Testing your failover handler — no network

The mock transport scripts every row of the failure taxonomy and both reconcile
verdicts, and asserts your requests carry the SDK User-Agent. It replaces only the
wire: header injection and classification run exactly as in production.

```python
from revaly_sdk import RapClient
from revaly_sdk.testing import RapMockTransport

mock = RapMockTransport()
mock.charge().returns_not_processed_503()  # → RapTransientFailure
mock.reconcile().not_found_yet(2).then_found_approved()

client = RapClient("sk-synthetic", transport=mock)
# exercise YOUR suppression/escalation logic against scripted consecutive outcomes:
mock.charge().returns_bare_503().throws_connection_refused().returns_approved()
```

Scenario methods mirror the contract: `returns_permanent_rejection(status)`,
`returns_not_processed_503()`, `throws_connection_refused()`, `throws_dns_failure()`,
`throws_ssl_handshake_failure()`, `throws_connect_timeout()`,
`throws_timeout_after_send()`, `throws_connection_reset()`, `returns_bare_503()`,
`returns_server_error()`, `pending()`, and raw escapes `returns(...)` /
`throws_io(...)`. Transport failures are simulated with real urllib3 exception
instances, so classification in your tests exercises the production code path.
Synthetic data only — no real PAN/CVV/PII ever appears in the mock.

## Logging & debugging

- Logging uses the stdlib `logging` module (logger name `revaly_sdk`; silent until
  your application configures handlers, or pass `logger=`). Default output is
  **values-free** — operation, status, class, correlation id. `DEBUG` level carries
  **allowlist-scrubbed** payloads only; PAN/CVV/PII and the API key can never appear
  (the API key is also absent from every error message).
- `wire_trace_hook`: a request/response observer for Enablement escalations —
  payloads arrive already scrubbed by the runtime's central allowlist scrubber.
- Every response and every typed error carries the `X-Correlation-ID`; quote it in
  support tickets to join RAP-core telemetry directly.

## What this SDK never does

No hidden retries, no resubmission, no circuit breaker, no cross-request state, no
`bypassPlatform`. The explicit, caller-bounded reconcile re-poll is the only loop the
SDK owns. Classification never derives from message text, latency, or wait
heuristics. (Concretely: urllib3's default connect retries and redirect-following are
disabled on every request — a `307` on `POST /payments` comes back as a response and
classifies `RapOutcomeUnknown` instead of being silently re-sent.)

## Beyond payments

The full generated V2 surface ships in the same package and flows through the same
transport, headers and classification:

```python
methods = client.payment_methods.list_payment_methods()
raw = client.transactions.get_transaction_by_id_without_preload_content("txn-1")
```
