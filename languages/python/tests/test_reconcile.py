"""The reconcile loop (failover-contract §3 · runtime-tdd §4): raw-body reads,
caller-bounded polling, verdicts open for extension."""

from __future__ import annotations

import json

import pytest

from conftest import make_client
from revaly_sdk import (
    Found,
    NotFoundYet,
    RapPermanentRejection,
    RapReconcileVerdict,
    RapTransactionOutcome,
    ReconcilePolicy,
)
from revaly_sdk.reconcile import delay_for_attempt
from revaly_sdk.testing import RapMockTransport, synthetic_data

FAST_POLICY = ReconcilePolicy(max_attempts=5, overall_budget=30.0, initial_delay=0.0)


def _reconcile(mock, policy=FAST_POLICY, mtx="mtx_synthetic_0001", **client_kwargs):
    return make_client(mock, **client_kwargs).reconcile(mtx, policy)


def test_not_found_then_approved():
    mock = RapMockTransport()
    mock.reconcile().not_found_yet(2).then_found_approved()
    verdict = _reconcile(mock)
    assert isinstance(verdict, Found)
    assert verdict.outcome is RapTransactionOutcome.APPROVED
    assert verdict.transaction is not None
    assert verdict.transaction.transaction_status == 1
    assert verdict.correlation_id == synthetic_data.DEFAULT_CORRELATION_ID
    assert len(mock.recorded_requests) == 3


def test_found_declined_and_error_outcomes():
    for scenario, outcome in [
        ("returns_declined", RapTransactionOutcome.DECLINED),
        ("returns_error_outcome", RapTransactionOutcome.ERROR),
    ]:
        mock = RapMockTransport()
        getattr(mock.reconcile(), scenario)()
        verdict = _reconcile(mock)
        assert isinstance(verdict, Found)
        assert verdict.outcome is outcome


def test_unmapped_transaction_status_is_found_unknown():
    # Found-but-unmapped is still FOUND: it licenses no failover either way.
    mock = RapMockTransport()
    mock.reconcile().returns_unmapped_status(9)
    verdict = _reconcile(mock)
    assert isinstance(verdict, Found)
    assert verdict.outcome is RapTransactionOutcome.UNKNOWN
    assert verdict.transaction is not None  # the record still bound


def test_group_envelope_is_found_unknown_sighting():
    mock = RapMockTransport()
    mock.reconcile().returns_transaction_group()
    verdict = _reconcile(mock)
    assert isinstance(verdict, Found)
    assert verdict.outcome is RapTransactionOutcome.UNKNOWN


def test_pending_intent_is_found_pending():
    mock = RapMockTransport()
    mock.reconcile().pending()
    verdict = _reconcile(mock)
    assert isinstance(verdict, Found)
    assert verdict.outcome is RapTransactionOutcome.PENDING
    assert verdict.pending is not None
    assert verdict.pending.state == "pending"


def test_pending_shape_this_sdk_cannot_bind_is_still_a_sighting():
    # `state` present but the pending model cannot bind (missing required id):
    # conservative Found(UNKNOWN), never poll-on.
    mock = RapMockTransport()
    mock.reconcile().returns(200, json.dumps({"state": "reserved_v2"}))
    verdict = _reconcile(mock)
    assert isinstance(verdict, Found)
    assert verdict.outcome is RapTransactionOutcome.UNKNOWN


def test_terminal_record_with_unbindable_enum_is_still_a_sighting():
    # The §A3 edge on the reconcile read: outcome maps from the RAW dict.
    mock = RapMockTransport()
    body = dict(json.loads(synthetic_data.transaction(1)))
    body["storedCredential"] = {"reasonType": "future_reason_v9"}
    mock.reconcile().returns(200, json.dumps(body))
    verdict = _reconcile(mock)
    assert isinstance(verdict, Found)
    assert verdict.outcome is RapTransactionOutcome.APPROVED
    assert verdict.transaction is None  # the typed bind failed; the sighting stands


def test_unreadable_2xx_body_keeps_polling():
    mock = RapMockTransport()
    mock.reconcile().returns(200, "<html>not json</html>").then_found_approved()
    verdict = _reconcile(mock)
    assert isinstance(verdict, Found)
    assert verdict.outcome is RapTransactionOutcome.APPROVED


def test_exhausted_attempts_yield_not_found_yet():
    mock = RapMockTransport()
    mock.reconcile().not_found_yet()
    verdict = _reconcile(mock, ReconcilePolicy(max_attempts=3, overall_budget=30, initial_delay=0))
    assert isinstance(verdict, NotFoundYet)
    assert verdict.attempts == 3
    assert verdict.last_http_status == 404
    assert verdict.last_correlation_id == synthetic_data.DEFAULT_CORRELATION_ID
    assert verdict.elapsed >= 0


def test_budget_bounds_the_loop_before_max_attempts():
    mock = RapMockTransport()
    mock.reconcile().not_found_yet()
    # The next wait (≥ 8s even with full negative jitter) exceeds the budget.
    verdict = _reconcile(
        mock, ReconcilePolicy(max_attempts=50, overall_budget=1.0, initial_delay=10.0)
    )
    assert isinstance(verdict, NotFoundYet)
    assert verdict.attempts == 1


def test_degraded_reads_keep_polling_within_budget():
    mock = RapMockTransport()
    mock.reconcile().returns_bare_503().throws_connect_timeout().then_found_approved()
    verdict = _reconcile(mock)
    assert isinstance(verdict, Found)
    assert verdict.outcome is RapTransactionOutcome.APPROVED
    assert len(mock.recorded_requests) == 3


def test_degraded_reads_carry_last_status_into_not_found_yet():
    mock = RapMockTransport()
    mock.reconcile().returns_bare_503()
    verdict = _reconcile(mock, ReconcilePolicy(max_attempts=2, overall_budget=30, initial_delay=0))
    assert isinstance(verdict, NotFoundYet)
    assert verdict.last_http_status == 503


def test_non_404_permanent_rejection_escapes():
    # Polling never fixes a rejected read (bad credentials, malformed id).
    mock = RapMockTransport()
    mock.reconcile().returns_permanent_rejection(401)
    with pytest.raises(RapPermanentRejection):
        _reconcile(mock)


def test_merchant_transaction_id_required():
    mock = RapMockTransport()
    with pytest.raises(ValueError):
        _reconcile(mock, mtx="   ")


def test_verdicts_are_open_for_extension():
    # The dispatch idiom every example teaches: isinstance checks with a
    # mandatory trailing else — SafeToFailover arrives with P-2 as a minor.
    mock = RapMockTransport()
    mock.reconcile().returns_approved()
    verdict = _reconcile(mock)
    assert isinstance(verdict, RapReconcileVerdict)
    if isinstance(verdict, Found):
        handled = "found"
    elif isinstance(verdict, NotFoundYet):
        handled = "notFoundYet"
    else:
        handled = "unrecognized-verdict-hold"
    assert handled == "found"


# ---- policy ------------------------------------------------------------------


def test_policy_validation():
    with pytest.raises(ValueError):
        ReconcilePolicy(max_attempts=0, overall_budget=1, initial_delay=0)
    with pytest.raises(ValueError):
        ReconcilePolicy(max_attempts=1, overall_budget=0, initial_delay=0)
    with pytest.raises(ValueError):
        ReconcilePolicy(max_attempts=1, overall_budget=1, initial_delay=-1)


def test_delay_growth_doubles_with_bounded_jitter():
    policy = ReconcilePolicy(max_attempts=10, overall_budget=600, initial_delay=1.0)
    for completed, base in [(1, 1.0), (2, 2.0), (3, 4.0), (4, 8.0)]:
        for _ in range(50):
            delay = delay_for_attempt(policy, completed)
            assert base * 0.8 <= delay <= base * 1.2


def test_delay_cap_applies_before_jitter():
    policy = ReconcilePolicy(
        max_attempts=10, overall_budget=600, initial_delay=1.0, max_delay=3.0
    )
    for _ in range(50):
        assert delay_for_attempt(policy, 6) <= 3.0 * 1.2


def test_zero_initial_delay_stays_zero():
    policy = ReconcilePolicy(max_attempts=10, overall_budget=600, initial_delay=0.0)
    assert delay_for_attempt(policy, 5) == 0.0
