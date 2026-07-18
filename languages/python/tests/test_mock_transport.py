"""The mock transport's own contract (runtime-tdd §8): request recording,
User-Agent assertion, routing, queue semantics, synthetic headers."""

from __future__ import annotations

import pytest
import urllib3

from conftest import make_client, payment_request
from revaly_sdk.testing import RapMockTransport, synthetic_data
from revaly_sdk.transport import RapWireRequest


def test_records_requests_with_final_headers():
    mock = RapMockTransport()
    mock.charge().returns_approved()
    make_client(mock).charge(payment_request())
    assert len(mock.recorded_requests) == 1
    recorded = mock.recorded_requests[0]
    assert recorded.method == "POST"
    assert recorded.url.endswith("/payments")
    assert recorded.body is not None and synthetic_data.DEFAULT_MERCHANT_TRANSACTION_ID.split("_")[0] in recorded.body


def test_missing_user_agent_is_asserted():
    mock = RapMockTransport()
    mock.charge().returns_approved()
    request = RapWireRequest(
        method="POST",
        url="https://api.revaly.co/payments",
        headers={"Authorization": "ApiKey synthetic"},
        body="{}",
        timeout=urllib3.Timeout(),
    )
    with pytest.raises(AssertionError, match="User-Agent"):
        mock.send(request)


def test_unstubbed_operation_raises():
    mock = RapMockTransport()
    from revaly_sdk import RapClient
    from conftest import SYNTHETIC_API_KEY

    client = RapClient(SYNTHETIC_API_KEY, transport=mock)
    with pytest.raises(AssertionError, match="no outcome scripted"):
        client.charge(payment_request())


def test_stubbed_without_outcome_raises():
    mock = RapMockTransport()
    mock.charge()  # stubbed, nothing scripted
    from revaly_sdk import RapClient
    from conftest import SYNTHETIC_API_KEY

    client = RapClient(SYNTHETIC_API_KEY, transport=mock)
    with pytest.raises(AssertionError, match="no outcome scripted"):
        client.charge(payment_request())


def test_queue_last_outcome_repeats():
    mock = RapMockTransport()
    mock.charge().returns_approved()
    client = make_client(mock)
    for _ in range(3):
        assert client.charge(payment_request()).transaction_status == 1


def test_routing_separates_payment_operations():
    from revaly_sdk_core.models.capture_request import CaptureRequest
    from revaly_sdk_core.models.refund_cancel_request import RefundCancelRequest
    from revaly_sdk_core.models.refund_request import RefundRequest
    from revaly_sdk_core.models.void_request import VoidRequest
    from revaly_sdk_core.models.authorize_request import AuthorizeRequest

    mock = RapMockTransport()
    mock.charge().returns_approved()
    mock.authorize().returns_approved()
    mock.capture().returns_approved()
    mock.void_payment().returns_approved()
    mock.refund().returns_approved()
    mock.refund_cancel().returns_approved()
    client = make_client(mock)

    client.charge(payment_request())
    client.authorize(
        AuthorizeRequest(amount=2500, merchant_transaction_id="mtx_synthetic_0002")
    )
    client.capture(
        "06SYNTHETIC00000000000000001",
        CaptureRequest(merchant_transaction_id="mtx_synthetic_0003"),
    )
    client.void_payment(
        "06SYNTHETIC00000000000000001",
        VoidRequest(merchant_transaction_id="mtx_synthetic_0004"),
    )
    client.refund(
        "06SYNTHETIC00000000000000001",
        RefundRequest(merchant_transaction_id="mtx_synthetic_0005"),
    )
    client.refund_cancel(
        "mtx_synthetic_0001",
        RefundCancelRequest(
            merchant_transaction_id="mtx_synthetic_0006", customer_id="cust_synthetic_0001"
        ),
    )

    paths = [request.url.split("api.revaly.co", 1)[1] for request in mock.recorded_requests]
    assert paths == [
        "/payments",
        "/payments/authorize",
        "/payments/capture/06SYNTHETIC00000000000000001",
        "/payments/void/06SYNTHETIC00000000000000001",
        "/payments/refund/06SYNTHETIC00000000000000001",
        "/payments/refund-cancel/merchant/mtx_synthetic_0001",
    ]


def test_synthetic_headers_present_by_default():
    mock = RapMockTransport()
    mock.charge().returns_approved()
    events = []
    make_client(mock, wire_trace_hook=events.append).charge(payment_request())
    # correlation id flowed from the mock's synthetic response headers
    assert events[0].correlation_id == synthetic_data.DEFAULT_CORRELATION_ID


def test_api_supported_versions_header_advertised():
    mock = RapMockTransport()
    mock.charge().returns_approved()

    captured = {}
    original_send = mock.send

    def spying_send(request):
        response = original_send(request)
        captured["headers"] = response.headers
        return response

    mock.send = spying_send  # type: ignore[method-assign]
    make_client(mock).charge(payment_request())
    assert captured["headers"]["api-supported-versions"] == "2.0, 2.1"
