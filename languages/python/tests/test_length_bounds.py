"""ADR-SDK-034 (OQ-18, SC-886): the SDK never refuses a request because a model field is
longer than the spec's maxLength; the platform decides (it truncates a description over
256 characters, and records or refuses other bounds). The amendment of 2026-11-26 (SC-1018,
OQ-19) adds the rtnData block: there the SDK never refuses a value because it breaks a
documented pattern, minimum or minLength either (test_rtn_data_values.py). Every other
generated check stays: required fields, types, the patterns, minimums and minLengths
outside rtnData, and the path-parameter bounds the API layer enforces.

The python generator emits max_length, ge= and min_length= inside each field's precomputed
declaration, so pipeline/generate.sh strips them after generation (max_length from models/,
the rtnData checks from models/rtn_data*.py only); these tests pin what must stay.
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from revaly_sdk_core.models.capture_request import CaptureRequest
from revaly_sdk_core.models.payment_method import PaymentMethod
from revaly_sdk_core.models.payment_request import PaymentRequest
from revaly_sdk_core.models.pending_transaction_response import PendingTransactionResponse
from revaly_sdk_core.models.refund_cancel_request import RefundCancelRequest

from conftest import SYNTHETIC_MTX, make_client, payment_request

LONG_DESCRIPTION = "d" * 300  # spec maxLength 256; the platform truncates, never blocks
LONG_CUSTOMER_IP = "i" * 50  # spec maxLength 45; the direct path accepts up to 50


def _sent_body(mock_transport) -> dict:
    return json.loads(mock_transport.recorded_requests[-1].body)


def test_description_over_the_bound_is_sent_whole(mock_transport):
    # AC1: built with the long value, sent through the client, carried in full.
    mock_transport.charge().returns_approved()
    request = PaymentRequest(
        amount=1, merchant_transaction_id=SYNTHETIC_MTX, description=LONG_DESCRIPTION
    )

    make_client(mock_transport).charge(request)

    assert _sent_body(mock_transport)["description"] == LONG_DESCRIPTION


def test_assigning_an_over_long_value_does_not_raise(mock_transport):
    # AC1: validate_assignment is on, so assignment is the other place the bound fired.
    mock_transport.charge().returns_approved()
    request = payment_request()
    request.description = LONG_DESCRIPTION
    request.customer_ip = LONG_CUSTOMER_IP

    make_client(mock_transport).charge(request)

    body = _sent_body(mock_transport)
    assert body["description"] == LONG_DESCRIPTION
    assert body["customerIp"] == LONG_CUSTOMER_IP


def test_response_with_an_over_long_field_still_binds():
    # A processed payment must never surface as a parse error over a length bound.
    body = json.dumps({"state": "pending", "merchantTransactionId": "m" * 150})

    parsed = PendingTransactionResponse.from_json(body)

    assert parsed.merchant_transaction_id == "m" * 150


def test_missing_required_field_is_still_refused():
    # AC3
    with pytest.raises(ValidationError):
        PaymentRequest(amount=1)


def test_pattern_outside_rtn_data_is_still_refused():
    # SC-1018 (D5): the kept pattern check, on a field outside rtnData (^[A-Z]{3}$). A step
    # that strips patterns beyond models/rtn_data*.py fails here. The rtnData pattern case
    # this test held before moved to test_rtn_data_values.py, where it is sent as given.
    with pytest.raises(ValidationError) as refused:
        PaymentRequest(amount=1, merchant_transaction_id=SYNTHETIC_MTX, currency="usd")

    errors = refused.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("currency",)
    assert errors[0]["type"] == "value_error"


def test_minimum_outside_rtn_data_is_still_refused():
    # SC-1018 (X1): the kept minimum check outside rtnData (amount, minimum 0).
    with pytest.raises(ValidationError) as refused:
        PaymentRequest(amount=-1, merchant_transaction_id=SYNTHETIC_MTX)

    errors = refused.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("amount",)
    assert errors[0]["type"] == "greater_than_equal"


@pytest.mark.parametrize(
    ("model", "fields"),
    [
        (RefundCancelRequest, {"merchant_transaction_id": SYNTHETIC_MTX, "customer_id": ""}),
        (PaymentMethod, {"payment_method_id": ""}),
    ],
    ids=["RefundCancelRequest.customerId", "PaymentMethod.paymentMethodId"],
)
def test_min_length_outside_rtn_data_is_still_refused(model, fields):
    # SC-1018 (X1): the kept minLength checks outside rtnData (minLength 1).
    with pytest.raises(ValidationError) as refused:
        model(**fields)

    errors = refused.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "string_too_short"


def test_over_long_path_parameter_is_still_refused_before_sending(mock_transport):
    # AC3: the API layer's path-parameter bound (transactionId at 50) is unchanged.
    mock_transport.capture().returns_approved()
    capture = CaptureRequest(merchant_transaction_id=SYNTHETIC_MTX, amount=1)

    with pytest.raises(ValidationError) as refused:
        make_client(mock_transport).capture("t" * 51, capture)

    assert refused.value.errors()[0]["type"] == "string_too_long"
    assert mock_transport.recorded_requests == []
