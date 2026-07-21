"""Header injection and timeout mapping at the transport (runtime-tdd §5,
ADR-SDK-005/020/024)."""

from __future__ import annotations

import re

import pytest
import urllib3

from conftest import SYNTHETIC_API_KEY, make_client, payment_request
from revaly_sdk import (
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_OVERALL_DEADLINE,
    SDK_VERSION,
    user_agent_value,
)
from revaly_sdk.testing import RapMockTransport

UA_GRAMMAR = re.compile(r"^revaly-sdk-python/\S+ \(python \d+\.\d+; (windows|linux|darwin|other)\)")


def _charge(mock, **client_kwargs):
    mock.charge().returns_approved()
    make_client(mock, **client_kwargs).charge(payment_request())
    return mock.recorded_requests[-1]


def test_user_agent_matches_adr_sdk_005_grammar():
    recorded = _charge(RapMockTransport())
    assert UA_GRAMMAR.match(recorded.headers["User-Agent"])
    assert SDK_VERSION in recorded.headers["User-Agent"]


def test_merchant_suffix_appends_never_replaces():
    recorded = _charge(RapMockTransport(), user_agent_suffix="merchant-app/9.9")
    user_agent = recorded.headers["User-Agent"]
    assert user_agent.startswith("revaly-sdk-python/")
    assert user_agent.endswith(" merchant-app/9.9")
    assert user_agent == user_agent_value("merchant-app/9.9")


def test_authorization_is_apikey_prefixed_and_lives_nowhere_else():
    recorded = _charge(RapMockTransport())
    assert recorded.headers["Authorization"] == f"ApiKey {SYNTHETIC_API_KEY}"
    for name, value in recorded.headers.items():
        if name != "Authorization":
            assert SYNTHETIC_API_KEY not in str(value)
    assert SYNTHETIC_API_KEY not in recorded.url
    assert SYNTHETIC_API_KEY not in (recorded.body or "")


def test_api_version_pinned_by_default():
    recorded = _charge(RapMockTransport())
    assert recorded.headers["X-Api-Version"] == "2.1"


def test_api_version_config_override():
    recorded = _charge(RapMockTransport(), api_version="2.0")
    assert recorded.headers["X-Api-Version"] == "2.0"


def test_per_call_api_version_wins_over_config():
    mock = RapMockTransport()
    mock.reconcile().returns_approved()
    client = make_client(mock)
    # The without_preload_content variant skips response deserialization —
    # this test only observes the outbound header.
    client.transactions.get_transaction_by_merchant_transaction_id_without_preload_content(
        "mtx_synthetic_0001", x_api_version="2.0"
    )
    assert mock.recorded_requests[-1].headers["X-Api-Version"] == "2.0"


def test_correlation_id_header_sent_back_on_error(client, mock_transport):
    from revaly_sdk import RapOutcomeUnknown
    from revaly_sdk.testing import synthetic_data

    mock_transport.charge().returns_bare_503()
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        client.charge(payment_request())
    assert exc_info.value.correlation_id == synthetic_data.DEFAULT_CORRELATION_ID


def test_base_url_joins_paths():
    recorded = _charge(RapMockTransport(), base_url="https://internal.example/")
    assert recorded.url == "https://internal.example/payments"


# ---- timeout mapping ---------------------------------------------------------


class _TimeoutCapturingWire(RapMockTransport):
    def __init__(self) -> None:
        super().__init__()
        self.timeouts: list = []

    def send(self, request):
        self.timeouts.append(request.timeout)
        return super().send(request)


def test_config_timeouts_map_to_total_and_connect():
    wire = _TimeoutCapturingWire()
    wire.charge().returns_approved()
    make_client(wire, connect_timeout=1.5, overall_deadline=7.0).charge(payment_request())
    timeout = wire.timeouts[-1]
    assert isinstance(timeout, urllib3.Timeout)
    assert timeout.total == 7.0
    assert timeout._connect == 1.5


def test_per_call_override_layers_over_config():
    wire = _TimeoutCapturingWire()
    wire.charge().returns_approved()
    make_client(wire, connect_timeout=1.5, overall_deadline=7.0).charge(
        payment_request(), overall_deadline=2.0
    )
    timeout = wire.timeouts[-1]
    assert timeout.total == 2.0
    assert timeout._connect == 1.5  # unset per-call field falls back to config


def test_core_convention_number_and_tuple_honored():
    wire = _TimeoutCapturingWire()
    wire.reconcile().returns_approved()
    client = make_client(wire)
    client.transactions.get_transaction_by_merchant_transaction_id_without_preload_content(
        "mtx_synthetic_0001", _request_timeout=3.0
    )
    assert wire.timeouts[-1].total == 3.0
    client.transactions.get_transaction_by_merchant_transaction_id_without_preload_content(
        "mtx_synthetic_0001", _request_timeout=(1.0, 4.0)
    )
    assert wire.timeouts[-1]._connect == 1.0
    assert wire.timeouts[-1].read_timeout == 4.0


def test_no_timeouts_configured_applies_the_ratified_defaults():
    # ADR-SDK-027 + ADR-SDK-029: an omitted overall_deadline resolves to the
    # 75 s ratified default; an omitted connect_timeout resolves to the 10 s
    # edge-ratified default.
    wire = _TimeoutCapturingWire()
    wire.charge().returns_approved()
    make_client(wire).charge(payment_request())
    timeout = wire.timeouts[-1]
    assert timeout.total == DEFAULT_OVERALL_DEADLINE
    assert timeout._connect == DEFAULT_CONNECT_TIMEOUT


def test_deadline_default_constant_is_the_ratified_value():
    assert DEFAULT_OVERALL_DEADLINE == 75.0


def test_connect_default_constant_is_the_ratified_value():
    assert DEFAULT_CONNECT_TIMEOUT == 10.0


def test_explicit_none_disables_the_sdk_connect_bound():
    # The pre-ADR-029 unset behaviour, now an explicit opt-out.
    wire = _TimeoutCapturingWire()
    wire.charge().returns_approved()
    make_client(wire, connect_timeout=None).charge(payment_request())
    assert wire.timeouts[-1]._connect in (None, urllib3.Timeout.DEFAULT_TIMEOUT)


def test_zero_and_negative_connect_timeouts_are_rejected():
    with pytest.raises(ValueError):
        make_client(RapMockTransport(), connect_timeout=0.0)
    with pytest.raises(ValueError):
        make_client(RapMockTransport(), connect_timeout=-5.0)


def test_explicit_none_disables_the_sdk_deadline():
    # The pre-ADR-027 unset behaviour, now an explicit opt-out.
    wire = _TimeoutCapturingWire()
    wire.charge().returns_approved()
    make_client(wire, overall_deadline=None).charge(payment_request())
    assert wire.timeouts[-1].total is None


def test_zero_and_negative_deadlines_are_rejected():
    with pytest.raises(ValueError):
        make_client(RapMockTransport(), overall_deadline=0.0)
    with pytest.raises(ValueError):
        make_client(RapMockTransport(), overall_deadline=-5.0)


def test_per_call_timeout_does_not_leak_into_reconcile():
    wire = _TimeoutCapturingWire()
    wire.charge().returns_approved()
    wire.reconcile().returns_approved()
    from revaly_sdk import ReconcilePolicy

    client = make_client(wire)
    client.charge(payment_request(), overall_deadline=2.0)
    client.reconcile(
        "mtx_synthetic_0001",
        ReconcilePolicy(max_attempts=1, overall_budget=30, initial_delay=0),
    )
    # The client-level default applies — not the per-call 2.0 from the charge.
    assert wire.timeouts[-1].total == DEFAULT_OVERALL_DEADLINE
