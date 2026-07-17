"""ADR-SDK-020 CI log-capture obligations (DX contract §c): no payload values at
default verbosity, full scrubbing at debug, keys never anywhere, correlation id
present on error paths."""

from __future__ import annotations

import logging

import pytest

from conftest import (
    SYNTHETIC_API_KEY,
    SYNTHETIC_CVV,
    SYNTHETIC_MTX,
    SYNTHETIC_PAN,
    make_client,
    payment_request,
)
from revaly_sdk import RapOutcomeUnknown, RapTransientFailure, ReconcilePolicy
from revaly_sdk.testing import RapMockTransport, synthetic_data

SENSITIVE = (SYNTHETIC_PAN, SYNTHETIC_CVV, SYNTHETIC_API_KEY, "Cardholder", "Synthetic")


def _assert_values_free(text: str) -> None:
    for sentinel in SENSITIVE:
        assert sentinel not in text


def test_default_level_success_is_values_free(caplog):
    caplog.set_level(logging.INFO, logger="revaly_sdk")
    mock = RapMockTransport()
    mock.charge().returns_approved()
    make_client(mock).charge(payment_request(with_card=True))
    assert "rap.request" in caplog.text
    assert synthetic_data.DEFAULT_CORRELATION_ID in caplog.text
    _assert_values_free(caplog.text)
    # Amounts are payload values too — never at default verbosity.
    assert "2500" not in caplog.text


def test_default_level_failure_carries_class_status_code_correlation(caplog):
    caplog.set_level(logging.INFO, logger="revaly_sdk")
    mock = RapMockTransport()
    mock.charge().returns_not_processed_503()
    with pytest.raises(RapTransientFailure):
        make_client(mock).charge(payment_request(with_card=True))
    assert "class=TransientFailure" in caplog.text
    assert "status=503" in caplog.text
    assert "code=not_processed" in caplog.text
    assert synthetic_data.DEFAULT_CORRELATION_ID in caplog.text
    _assert_values_free(caplog.text)


def test_debug_level_payloads_are_scrubbed(caplog):
    caplog.set_level(logging.DEBUG, logger="revaly_sdk")
    mock = RapMockTransport()
    mock.charge().returns_approved()
    make_client(mock).charge(payment_request(with_card=True))
    assert "rap.request payload" in caplog.text
    assert "[scrubbed]" in caplog.text
    # Allowlisted identifiers pass; payload values never do.
    assert SYNTHETIC_MTX in caplog.text
    _assert_values_free(caplog.text)


def test_reconcile_logs_are_values_free(caplog):
    caplog.set_level(logging.DEBUG, logger="revaly_sdk")
    mock = RapMockTransport()
    mock.reconcile().not_found_yet(1).then_found_approved()
    make_client(mock).reconcile(
        SYNTHETIC_MTX, ReconcilePolicy(max_attempts=3, overall_budget=30, initial_delay=0)
    )
    assert "rap.reconcile" in caplog.text
    _assert_values_free(caplog.text)


def test_unreadable_2xx_containment_logs_values_free(caplog):
    caplog.set_level(logging.INFO, logger="revaly_sdk")
    mock = RapMockTransport()
    mock.charge().returns(
        200, '{"transactionStatus": 1, "storedCredential": {"reasonType": "future_v9"}}'
    )
    with pytest.raises(RapOutcomeUnknown):
        make_client(mock).charge(payment_request(with_card=True))
    assert "reason=unreadable-2xx" in caplog.text
    _assert_values_free(caplog.text)


def test_exception_messages_never_carry_key_or_payload():
    mock = RapMockTransport()
    mock.charge().returns_bare_503()
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        make_client(mock).charge(payment_request(with_card=True))
    _assert_values_free(str(exc_info.value))
    _assert_values_free(repr(exc_info.value))


def test_wire_trace_hook_receives_scrubbed_payloads_only():
    events = []
    mock = RapMockTransport()
    mock.charge().returns_approved()
    make_client(mock, wire_trace_hook=events.append).charge(payment_request(with_card=True))
    assert len(events) == 1
    event = events[0]
    assert event.operation == "charge"
    assert event.correlation_id == synthetic_data.DEFAULT_CORRELATION_ID
    _assert_values_free(event.scrubbed_request_body or "")
    _assert_values_free(event.scrubbed_response_body or "")
    assert SYNTHETIC_MTX in (event.scrubbed_request_body or "")


def test_wire_trace_hook_exceptions_are_swallowed():
    def exploding_hook(event):
        raise RuntimeError("observer bug")

    mock = RapMockTransport()
    mock.charge().returns_approved()
    transaction = make_client(mock, wire_trace_hook=exploding_hook).charge(payment_request())
    assert transaction.transaction_status == 1


def test_wire_trace_hook_fires_on_failures_too():
    events = []
    mock = RapMockTransport()
    mock.charge().returns_not_processed_503()
    with pytest.raises(RapTransientFailure):
        make_client(mock, wire_trace_hook=events.append).charge(payment_request(with_card=True))
    assert len(events) == 1
    assert events[0].status == 503
    _assert_values_free(events[0].scrubbed_request_body or "")


def test_reconcile_trace_hook_receives_scrubbed_bodies():
    events = []
    mock = RapMockTransport()
    mock.reconcile().returns_approved()
    make_client(mock, wire_trace_hook=events.append).reconcile(
        SYNTHETIC_MTX, ReconcilePolicy(max_attempts=1, overall_budget=30, initial_delay=0)
    )
    assert events and events[0].operation == "reconcile"
    body = events[0].scrubbed_response_body or ""
    assert "[scrubbed]" in body
    assert SYNTHETIC_MTX in body  # allowlisted identifier passes


def test_silent_by_default_without_app_configuration(caplog):
    # Library etiquette: the revaly_sdk logger has only a NullHandler; nothing
    # propagates unless the application opts in. caplog captures at WARNING by
    # default here — an INFO-level success must produce no records.
    mock = RapMockTransport()
    mock.charge().returns_approved()
    with caplog.at_level(logging.WARNING, logger="revaly_sdk"):
        make_client(mock).charge(payment_request())
    assert caplog.records == []
