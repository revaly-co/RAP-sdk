"""The README quickstart flow, executed end to end against the mock transport
(DX contract §b/§d: our own quickstart is tested, no network). The handler shape
below is the copy-paste example: all three failure classes plus the reconcile
default branch."""

from __future__ import annotations

import pytest

from conftest import SYNTHETIC_MTX, make_client, payment_request
from revaly_sdk import (
    Found,
    NotFoundYet,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransactionOutcome,
    RapTransientFailure,
    ReconcilePolicy,
)
from revaly_sdk.testing import RapMockTransport

POLICY = ReconcilePolicy(max_attempts=5, overall_budget=30.0, initial_delay=0.0)


def charge_with_failover(client, request):
    """The quickstart's failover handler: returns (outcome, detail)."""
    try:
        transaction = client.charge(request)
        return "processed", transaction
    except RapPermanentRejection as failure:
        return "declined", failure  # fix or decline; never fail over
    except RapTransientFailure as failure:
        return "failover", failure  # provably not processed: own gateway now
    except RapOutcomeUnknown:
        verdict = client.reconcile(request.merchant_transaction_id, POLICY)
        if isinstance(verdict, Found):
            if verdict.outcome is RapTransactionOutcome.APPROVED:
                return "processed-late", verdict  # money moved: NO failover
            return "found-terminal", verdict
        elif isinstance(verdict, NotFoundYet):
            return "hold-and-escalate", verdict  # absence is NOT provable in V1
        else:
            # Verdicts are open for extension (SafeToFailover arrives with P-2):
            # the default branch is mandatory in every example.
            return "unrecognized-verdict-hold", verdict


def test_success_path():
    mock = RapMockTransport()
    mock.charge().returns_approved()
    outcome, transaction = charge_with_failover(make_client(mock), payment_request())
    assert outcome == "processed"
    assert transaction.transaction_status == 1


def test_permanent_rejection_path_never_fails_over():
    mock = RapMockTransport()
    mock.charge().returns_permanent_rejection(422)
    outcome, failure = charge_with_failover(make_client(mock), payment_request())
    assert outcome == "declined"
    assert failure.status == 422


def test_fast_failover_path():
    mock = RapMockTransport()
    mock.charge().returns_not_processed_503()
    outcome, failure = charge_with_failover(make_client(mock), payment_request())
    assert outcome == "failover"
    assert failure.code == "not_processed"


def test_outcome_unknown_reconciles_to_found_approved():
    # The double-charge guard: the timeout LOOKED like a failure, but the
    # payment succeeded — reconcile finds it and no failover happens.
    mock = RapMockTransport()
    mock.charge().throws_timeout_after_send()
    mock.reconcile().not_found_yet(1).then_found_approved()
    outcome, verdict = charge_with_failover(make_client(mock), payment_request())
    assert outcome == "processed-late"
    assert verdict.outcome is RapTransactionOutcome.APPROVED


def test_outcome_unknown_reconciles_to_not_found_yet_holds():
    mock = RapMockTransport()
    mock.charge().returns_bare_503()
    mock.reconcile().not_found_yet()
    outcome, verdict = charge_with_failover(make_client(mock), payment_request())
    assert outcome == "hold-and-escalate"
    assert verdict.attempts == 5


def test_declined_after_reconcile_is_a_merchant_decision():
    mock = RapMockTransport()
    mock.charge().throws_connection_reset()
    mock.reconcile().then_found_declined()
    outcome, verdict = charge_with_failover(make_client(mock), payment_request())
    assert outcome == "found-terminal"
    assert verdict.outcome is RapTransactionOutcome.DECLINED


def test_scripted_consecutive_outcomes_for_suppression_logic():
    # Merchants can script consecutive outcomes to test their escalation logic.
    mock = RapMockTransport()
    mock.charge().returns_not_processed_503().returns_not_processed_503().returns_approved()
    client = make_client(mock)
    results = []
    for _ in range(3):
        outcome, _detail = charge_with_failover(client, payment_request())
        results.append(outcome)
    assert results == ["failover", "failover", "processed"]


def test_full_api_surface_raises_the_same_classes():
    # Non-payment operations flow through the same transport and classification.
    mock = RapMockTransport()
    mock.get_transaction().returns_bare_503()
    client = make_client(mock)
    with pytest.raises(RapOutcomeUnknown):
        client.transactions.get_transaction_by_id("06SYNTHETIC00000000000000001")
