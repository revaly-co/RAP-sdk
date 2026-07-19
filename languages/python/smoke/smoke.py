"""Stage-4 contract smoke (ADR-SDK-024, pipeline stage 4).

A thin, live runtime-contract check of THIS SDK against the environment named
by RAP_SMOKE_BASE_URL / RAP_SMOKE_API_KEY (interim: Backbone staging; at GA:
the merchant sandbox key-scope). Its single purpose is proving the SDK's
classification against reality — it deliberately does not replicate platform
test coverage.

Environment contract (same across all six languages):

    RAP_SMOKE_BASE_URL            required — target base URL
    RAP_SMOKE_API_KEY             required — staging/sandbox-scoped key
    RAP_SMOKE_GATEWAY_ROUTING_ID  optional — included in charge payloads when set
    RAP_SMOKE_FAULT_INJECT        optional — sent as the platform's
                                  X-Backbone-Fault-Inject header to trigger the
                                  503+not_processed row; SKIPs when unset

Scenarios mirror the quickstart shape (README). Output is values-free
(ADR-SDK-020): identifiers, statuses, classes and correlation ids only — never
payload values, never the key, never the target host.

Exit codes: 0 all pass (skips allowed) / 1 at least one failed / 2 not
configured.
"""

from __future__ import annotations

import dataclasses
import os
import secrets
import sys
import time
from typing import Callable, List, Optional, Tuple

from revaly_sdk import (
    CreditCard,
    Found,
    NotFoundYet,
    PaymentMethod,
    PaymentRequest,
    RapClient,
    RapPermanentRejection,
    RapTransactionOutcome,
    RapTransientFailure,
    ReconcilePolicy,
)
from revaly_sdk.errors import RapError
from revaly_sdk.transport import _Urllib3Wire

# The platform's executor fault seam (Backbone ADR 014 test affordance):
# value "pre-dispatch" makes the charge fail between intent reservation and
# gateway dispatch — the only deterministic live trigger for the
# 503 + code=not_processed fast-failover row.
FAULT_INJECT_HEADER = "X-Backbone-Fault-Inject"

# One synthetic test PAN; the EXPIRY drives the outcome (staging-verified
# matrix 2026-07-18: 12/2027 approves, 12/2020 declines).
TEST_PAN = "4111111111111111"


class SmokeFailure(Exception):
    """A scenario assertion failure (values-free message)."""


class SmokeSkip(Exception):
    """A scenario that cannot run in this environment (reported, never silent)."""


class _FaultInjectingWire(_Urllib3Wire):
    """A real-HTTP wire that stamps one extra header on every request.

    Sits at the transport seam INSIDE the runtime's own header injection, so
    auth/UA/version behaviour is unchanged. (The wire class is runtime-internal;
    this smoke is in-repo tooling, not merchant guidance.)
    """

    def __init__(self, name: str, value: str) -> None:
        super().__init__()
        self._name = name
        self._value = value

    def send(self, request):  # noqa: ANN001 — runtime-internal request type
        headers = {**dict(request.headers), self._name: self._value}
        return super().send(dataclasses.replace(request, headers=headers))


def fresh_id(label: str) -> str:
    """Unique merchantTransactionId (<= 100 chars) — every reconcile scenario
    uses a fresh one (ADR-SDK-024)."""
    return f"smoke-python-{label}-{int(time.time() * 1000)}-{secrets.token_hex(4)}"


def build_charge(mtid: str, pan: str, expiry_year: str, routing_id: Optional[str]) -> PaymentRequest:
    """Charge request with the minimal live-approving field set (staging-verified
    2026-07-18): paymentMethodType + a cardholder name are SERVER-required
    (business validation; the spec marks them optional — ADR-SDK-024), and
    orderId + email are additionally required by the staging simulator for an
    approval. Synthetic test cards only."""
    kwargs = {}
    if routing_id:
        kwargs["gateway_routing_id"] = routing_id
    return PaymentRequest(
        amount=1999,
        currency="USD",
        merchant_transaction_id=mtid,
        payment_method_type="creditCard",
        order_id=mtid,
        payment_method=PaymentMethod(
            full_name="Smoke Test",
            email="smoke@example.com",
            credit_card=CreditCard(
                number=pan,
                card_verification_code="123",
                expiry_month="12",
                expiry_year=expiry_year,
            ),
        ),
        **kwargs,
    )


def classified(context: str, err: Exception) -> SmokeFailure:
    """Values-free rendering of an unexpected failure: typed classes print
    their runtime-crafted message (status, code, correlation — never payloads,
    never the target host); anything else prints its type only."""
    if isinstance(err, RapError):
        return SmokeFailure(f"{context}, got: {err}")
    return SmokeFailure(f"{context}, got {type(err).__name__}")


def expect_found(verdict, want: RapTransactionOutcome) -> str:
    """Asserts Found(want) with a correlation id. The verdict set is open — an
    unrecognized verdict is a real finding here, not a pass."""
    if isinstance(verdict, Found):
        if verdict.outcome is not want:
            raise SmokeFailure(f"expected outcome {want.value}, got {verdict.outcome.value}")
        if not verdict.correlation_id:
            raise SmokeFailure("no X-Correlation-ID on the Found verdict (DX §c)")
        return f" (outcome={verdict.outcome.value} correlation={verdict.correlation_id})"
    if isinstance(verdict, NotFoundYet):
        raise SmokeFailure(
            f"charge not visible after {verdict.attempts} attempts ({verdict.elapsed:.1f}s) — expected Found"
        )
    raise SmokeFailure(f"unrecognized verdict {type(verdict).__name__}")


def main() -> int:
    base_url = os.environ.get("RAP_SMOKE_BASE_URL", "")
    api_key = os.environ.get("RAP_SMOKE_API_KEY", "")
    routing_id = os.environ.get("RAP_SMOKE_GATEWAY_ROUTING_ID") or None
    fault_value = os.environ.get("RAP_SMOKE_FAULT_INJECT") or None
    if not base_url or not api_key:
        print(
            "smoke: RAP_SMOKE_BASE_URL and RAP_SMOKE_API_KEY must be set (ADR-SDK-024) — refusing to run.",
            file=sys.stderr,
        )
        return 2

    # One client per configuration, quickstart-shaped. The wire-trace hook is
    # the designed observer for correlation ids on the success path (DX §c);
    # events arrive already scrubbed by the runtime.
    last_correlation: List[Optional[str]] = [None]

    def trace_hook(event) -> None:  # noqa: ANN001 — RapWireTraceEvent
        last_correlation[0] = event.correlation_id

    client = RapClient(
        api_key,
        base_url=base_url,
        connect_timeout=5.0,
        overall_deadline=15.0,
        wire_trace_hook=trace_hook,
    )

    # A separately configured client whose key is a synthetic invalid value —
    # the auth-rejection row.
    bad_key_client = RapClient(
        "sk_smoke_synthetic_invalid",
        base_url=base_url,
        connect_timeout=5.0,
        overall_deadline=15.0,
    )

    # A client whose wire stamps the platform's fault-inject header — every
    # charge through it deterministically fails pre-dispatch
    # (503 + code=not_processed). Only built when the scenario is enabled.
    fault_client = (
        RapClient(
            api_key,
            base_url=base_url,
            overall_deadline=15.0,
            transport=_FaultInjectingWire(FAULT_INJECT_HEADER, fault_value),
        )
        if fault_value
        else None
    )

    # Charged ids feed the reconcile scenarios: the verdicts — through the
    # runtime's own outcome mapping — are the proof the charge outcomes were
    # what the smoke claims.
    charged_id = fresh_id("charge")
    declined_id = fresh_id("decline")

    def charge_approved() -> str:
        transaction = client.charge(build_charge(charged_id, TEST_PAN, "2027", routing_id))
        if not transaction.transaction_id:
            raise SmokeFailure("transactionId is empty on the success surface")
        if not last_correlation[0]:
            raise SmokeFailure("no X-Correlation-ID observed on the success path (DX §c)")
        return f" (txn={transaction.transaction_id} correlation={last_correlation[0]})"

    def charge_declined() -> str:
        # An expired expiry declines deterministically (same PAN). A decline is a business
        # outcome on the SUCCESS surface — not a failure class;
        # reconcile-found-declined proves the mapping below.
        transaction = client.charge(build_charge(declined_id, TEST_PAN, "2020", routing_id))
        if not transaction.transaction_id:
            raise SmokeFailure("transactionId is empty on the declined-charge surface")
        if not last_correlation[0]:
            raise SmokeFailure("no X-Correlation-ID observed on the declined-charge path (DX §c)")
        return f" (txn={transaction.transaction_id} correlation={last_correlation[0]})"

    def charge_validation_rejected() -> str:
        # An empty card number passes every client-side model but fails the
        # server's required-field validation — the rejection is proven to come
        # from reality (HTTP 400; 4xx carries no code).
        try:
            client.charge(build_charge(fresh_id("validation"), "", "2027", routing_id))
        except RapPermanentRejection as rejection:
            if rejection.status not in (400, 422):
                raise SmokeFailure(f"expected HTTP 400/422, got {rejection.status}") from None
            if not rejection.correlation_id:
                raise SmokeFailure("no X-Correlation-ID on the rejection (DX §c)") from None
            return f" (status={rejection.status} correlation={rejection.correlation_id})"
        except Exception as err:  # noqa: BLE001 — classified below
            raise classified("expected RapPermanentRejection", err) from None
        raise SmokeFailure("server accepted an empty card number — expected RapPermanentRejection")

    def charge_auth_rejected() -> str:
        try:
            bad_key_client.charge(build_charge(fresh_id("auth"), TEST_PAN, "2027", routing_id))
        except RapPermanentRejection as rejection:
            if rejection.status not in (401, 403):
                raise SmokeFailure(f"expected HTTP 401/403, got {rejection.status}") from None
            if not rejection.correlation_id:
                raise SmokeFailure("no X-Correlation-ID on the auth rejection (DX §c)") from None
            return f" (status={rejection.status} correlation={rejection.correlation_id})"
        except Exception as err:  # noqa: BLE001
            raise classified("expected RapPermanentRejection", err) from None
        raise SmokeFailure("server accepted a synthetic invalid key — expected RapPermanentRejection")

    def charge_not_processed_503() -> str:
        # The fast-failover row (503 + code=not_processed): valid input cannot
        # reach it deterministically, so the platform's fault injector fails
        # the charge pre-dispatch. RapTransientFailure is the ONLY acceptable
        # class here — it is the row that licenses immediate failover.
        if fault_client is None:
            raise SmokeSkip("RAP_SMOKE_FAULT_INJECT not set (injector is staging-only)")
        try:
            fault_client.charge(build_charge(fresh_id("fault"), TEST_PAN, "2027", routing_id))
        except RapTransientFailure as transient:
            if transient.status != 503:
                raise SmokeFailure(f"expected HTTP 503, got {transient.status}") from None
            if transient.code != "not_processed":
                raise SmokeFailure(f'expected code=not_processed, got "{transient.code}"') from None
            if not transient.correlation_id:
                raise SmokeFailure("no X-Correlation-ID on the not-processed failure (DX §c)") from None
            return f" (status=503 code={transient.code} correlation={transient.correlation_id})"
        except Exception as err:  # noqa: BLE001
            raise classified("expected RapTransientFailure", err) from None
        raise SmokeFailure("fault-injected charge succeeded — expected RapTransientFailure")

    def reconcile_found_approved() -> str:
        # Found(APPROVED) through the runtime's own outcome mapping is the
        # approval proof for the first charge; visibility is asynchronous,
        # hence the budget.
        verdict = client.reconcile(
            charged_id,
            ReconcilePolicy(max_attempts=5, overall_budget=30.0, initial_delay=1.0),
        )
        return expect_found(verdict, RapTransactionOutcome.APPROVED)

    def reconcile_found_declined() -> str:
        # The declined charge must reconcile as Found(DECLINED) — the outcome
        # branch that tells a merchant their own gateway is safe.
        verdict = client.reconcile(
            declined_id,
            ReconcilePolicy(max_attempts=5, overall_budget=30.0, initial_delay=1.0),
        )
        return expect_found(verdict, RapTransactionOutcome.DECLINED)

    def reconcile_not_found_yet() -> str:
        # A fresh, never-used merchantTransactionId (ADR-SDK-024): the only
        # correct verdict is NotFoundYet, and it must come from real 404s —
        # not from a transport that never reached the API.
        verdict = client.reconcile(
            fresh_id("absent"),
            ReconcilePolicy(max_attempts=2, overall_budget=10.0, initial_delay=0.5),
        )
        if isinstance(verdict, NotFoundYet):
            if verdict.last_http_status != 404:
                raise SmokeFailure(f"expected last HTTP status 404, got {verdict.last_http_status}")
            if not verdict.last_correlation_id:
                raise SmokeFailure("no X-Correlation-ID on the NotFoundYet verdict (DX §c)")
            return f" (attempts={verdict.attempts} correlation={verdict.last_correlation_id})"
        if isinstance(verdict, Found):
            raise SmokeFailure("a never-used id reconciled as Found")
        raise SmokeFailure(f"unrecognized verdict {type(verdict).__name__}")

    scenarios: List[Tuple[str, Callable[[], str]]] = [
        ("charge-approved", charge_approved),
        ("charge-declined", charge_declined),
        ("charge-validation-rejected", charge_validation_rejected),
        ("charge-auth-rejected", charge_auth_rejected),
        ("charge-not-processed-503", charge_not_processed_503),
        ("reconcile-found-approved", reconcile_found_approved),
        ("reconcile-found-declined", reconcile_found_declined),
        ("reconcile-not-found-yet", reconcile_not_found_yet),
    ]

    print(f"RAP contract smoke (python): {len(scenarios)} scenarios")
    failures = 0
    skips = 0
    for name, run in scenarios:
        try:
            detail = run()
        except SmokeSkip as skip:
            skips += 1
            print(f"SKIP {name} ({skip})")
        except SmokeFailure as failure:
            failures += 1
            print(f"FAIL {name}: {failure}")
        except RapError as err:
            # Typed-class messages are values-free by construction.
            failures += 1
            print(f"FAIL {name}: unexpected {err}")
        except Exception as err:  # noqa: BLE001 — never print raw messages (host leak)
            failures += 1
            print(f"FAIL {name}: unexpected {type(err).__name__}")
        else:
            print(f"PASS {name}{detail}")

    passed = len(scenarios) - failures - skips
    verdict = "FAIL" if failures else "PASS"
    print(f"RESULT: {verdict} ({passed}/{len(scenarios)} passed, {skips} skipped)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
