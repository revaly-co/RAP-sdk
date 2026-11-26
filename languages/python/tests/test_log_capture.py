"""ADR-SDK-020 CI log-capture obligations (DX contract §c): no payload values at
default verbosity, full scrubbing at debug, keys never anywhere, correlation id
present on error paths."""

from __future__ import annotations

import json
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
from revaly_sdk_core.models.authorize_request import AuthorizeRequest
from revaly_sdk_core.models.payment_request import PaymentRequest
from revaly_sdk_core.models.rtn_data import RtnData
from revaly_sdk_core.models.rtn_data_additional_transaction_data import (
    RtnDataAdditionalTransactionData,
)
from revaly_sdk_core.models.rtn_data_customer_data import RtnDataCustomerData

SENSITIVE = (SYNTHETIC_PAN, SYNTHETIC_CVV, SYNTHETIC_API_KEY, "Cardholder", "Synthetic")
# The documentation test number in the spaced form a merchant might store (it breaks the
# documented fullPan pattern), and a synthetic customer email.
SPACED_PAN = " ".join(SYNTHETIC_PAN[i : i + 4] for i in range(0, len(SYNTHETIC_PAN), 4))
SYNTHETIC_EMAIL = "customer@synthetic.test"


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


@pytest.mark.parametrize("operation", ["charge", "authorize"])
def test_rtn_data_card_material_is_sent_but_never_logged_or_traced(caplog, operation):
    # SC-1018 (AppSec M1): once the core sends rtnData values as given, a malformed fullPan
    # built through the public constructor reaches the runtime, and the key-based scrubber
    # is the only control on that path. Built through the constructor (never
    # model_construct), so the request reaches the wire only when the core sends the value.
    caplog.set_level(logging.DEBUG, logger="revaly_sdk")
    events = []
    mock = RapMockTransport()
    getattr(mock, operation)().returns_approved()
    request_type = PaymentRequest if operation == "charge" else AuthorizeRequest
    request = request_type(
        amount=2500,
        merchant_transaction_id=SYNTHETIC_MTX,
        currency="USD",
        rtn_data=RtnData(
            additional_transaction_data=RtnDataAdditionalTransactionData(full_pan=SPACED_PAN),
            customer_data=RtnDataCustomerData(email=SYNTHETIC_EMAIL),
        ),
    )

    getattr(make_client(mock, wire_trace_hook=events.append), operation)(request)

    # The wire carries the value as given ...
    sent = json.loads(mock.recorded_requests[-1].body)["rtnData"]
    assert sent["additionalTransactionData"]["fullPan"] == SPACED_PAN
    assert sent["customerData"]["email"] == SYNTHETIC_EMAIL
    # ... the trace carries it only as [scrubbed] ...
    assert "rap.request payload" in caplog.text
    assert len(events) == 1
    scrubbed = json.loads(events[0].scrubbed_request_body)["rtnData"]
    assert scrubbed["additionalTransactionData"]["fullPan"] == "[scrubbed]"
    assert scrubbed["customerData"]["email"] == "[scrubbed]"
    # ... and no record or event holds the value, its digit run or its 15-character prefix.
    surfaces = [caplog.text] + [record.getMessage() for record in caplog.records]
    surfaces += [events[0].scrubbed_request_body or "", events[0].scrubbed_response_body or ""]
    for text in surfaces:
        for needle in (SPACED_PAN, SPACED_PAN[:15], SYNTHETIC_PAN, SYNTHETIC_EMAIL):
            assert needle not in text
        _assert_values_free(text)


def test_silent_by_default_without_app_configuration(caplog):
    # Library etiquette: the revaly_sdk logger has only a NullHandler; nothing
    # propagates unless the application opts in. caplog captures at WARNING by
    # default here — an INFO-level success must produce no records.
    mock = RapMockTransport()
    mock.charge().returns_approved()
    with caplog.at_level(logging.WARNING, logger="revaly_sdk"):
        make_client(mock).charge(payment_request())
    assert caplog.records == []
