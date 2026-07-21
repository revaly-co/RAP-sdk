"""Every row of the failover-contract §2 table, classified through the full
client → transport → classifier stack (the mock replaces only the wire)."""

from __future__ import annotations

import pytest
import urllib3.exceptions

from conftest import SYNTHETIC_API_KEY, make_client, payment_request
from revaly_sdk import (
    RapError,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransientFailure,
)
from revaly_sdk.errors import classify_transport_exception
from revaly_sdk.testing import RapMockTransport, synthetic_data


@pytest.mark.parametrize("status", [400, 401, 403, 404, 422])
def test_permanent_rejection_statuses(status):
    mock = RapMockTransport()
    mock.charge().returns_permanent_rejection(status)
    with pytest.raises(RapPermanentRejection) as exc_info:
        make_client(mock).charge(payment_request())
    assert exc_info.value.status == status
    assert exc_info.value.kind == "PermanentRejection"
    assert exc_info.value.correlation_id == synthetic_data.DEFAULT_CORRELATION_ID


def test_503_not_processed_is_transient_failure():
    mock = RapMockTransport()
    mock.charge().returns_not_processed_503()
    with pytest.raises(RapTransientFailure) as exc_info:
        make_client(mock).charge(payment_request())
    assert exc_info.value.status == 503
    assert exc_info.value.code == "not_processed"


def test_503_not_processed_narrows_to_outcome_unknown_on_api_version_20():
    # Version-pin behaviour (runtime-tdd §1): code is not part of the 2.0 contract.
    mock = RapMockTransport()
    mock.charge().returns_not_processed_503()
    with pytest.raises(RapOutcomeUnknown):
        make_client(mock, api_version="2.0").charge(payment_request())


def test_bare_503_is_outcome_unknown():
    mock = RapMockTransport()
    mock.charge().returns_bare_503()
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        make_client(mock).charge(payment_request())
    assert exc_info.value.status == 503
    assert exc_info.value.code is None


def test_unrecognized_503_code_treated_as_absent():
    mock = RapMockTransport()
    mock.charge().returns_unknown_code_503("shiny_future_code")
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        make_client(mock).charge(payment_request())
    # The code is carried VERBATIM (open string) even though it did not classify.
    assert exc_info.value.code == "shiny_future_code"


@pytest.mark.parametrize(
    "scenario",
    ["returns_server_error", "returns_bad_gateway", "returns_gateway_timeout"],
)
def test_5xx_statuses_are_outcome_unknown(scenario):
    mock = RapMockTransport()
    getattr(mock.charge(), scenario)()
    with pytest.raises(RapOutcomeUnknown):
        make_client(mock).charge(payment_request())


@pytest.mark.parametrize("status", [301, 307, 308, 409, 418, 429])
def test_statuses_outside_the_normative_table_are_outcome_unknown(status):
    mock = RapMockTransport()
    mock.charge().returns(status, synthetic_data.error_body("synthetic"))
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        make_client(mock).charge(payment_request())
    assert exc_info.value.status == status


@pytest.mark.parametrize(
    ("scenario", "expected"),
    [
        ("throws_connection_refused", RapTransientFailure),
        ("throws_dns_failure", RapTransientFailure),
        ("throws_connect_timeout", RapTransientFailure),
        ("throws_ssl_handshake_failure", RapTransientFailure),
        ("throws_timeout_after_send", RapOutcomeUnknown),
        ("throws_connection_reset", RapOutcomeUnknown),
        ("throws_ssl_after_handshake", RapOutcomeUnknown),
    ],
)
def test_transport_failures_classify_by_exception_type(scenario, expected):
    mock = RapMockTransport()
    getattr(mock.charge(), scenario)()
    with pytest.raises(expected) as exc_info:
        make_client(mock).charge(payment_request())
    assert isinstance(exc_info.value, RapError)
    # The transport failure is chained for diagnostics.
    assert exc_info.value.__cause__ is not None


def test_classification_never_reads_message_text():
    # A 500 whose error text CLAIMS a never-sent failure still classifies by
    # status: OutcomeUnknown (§2 rules: never classify from `error` text).
    mock = RapMockTransport()
    mock.charge().returns(
        500, synthetic_data.error_body("connection refused before send; not processed")
    )
    with pytest.raises(RapOutcomeUnknown):
        make_client(mock).charge(payment_request())


def test_error_carries_contract_fields():
    mock = RapMockTransport()
    mock.charge().returns(
        503, '{"error": "synthetic outage", "code": "not_processed", "details": {"zone": "syn"}}'
    )
    with pytest.raises(RapTransientFailure) as exc_info:
        make_client(mock).charge(payment_request())
    failure = exc_info.value
    assert failure.api_error == "synthetic outage"
    assert failure.details == {"zone": "syn"}
    assert failure.raw_body is not None and "synthetic outage" in failure.raw_body
    assert failure.correlation_id == synthetic_data.DEFAULT_CORRELATION_ID


def test_non_json_error_body_still_classifies():
    mock = RapMockTransport()
    mock.charge().returns(503, "<html>gateway said no</html>")
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        make_client(mock).charge(payment_request())
    assert exc_info.value.code is None


def test_api_key_never_in_exception_message():
    mock = RapMockTransport()
    mock.charge().returns_permanent_rejection(401)
    with pytest.raises(RapPermanentRejection) as exc_info:
        make_client(mock).charge(payment_request())
    assert SYNTHETIC_API_KEY not in str(exc_info.value)
    assert SYNTHETIC_API_KEY not in repr(exc_info.value)


def test_unreadable_2xx_is_contained_as_outcome_unknown():
    # The §A3 closed-enum edge: a 2xx whose body cannot bind (enum value newer
    # than this SDK) is a POST-DISPATCH failure — the payment may have succeeded.
    mock = RapMockTransport()
    mock.charge().returns(
        200,
        '{"transactionId": "06SYNTHETIC00000000000000001", "transactionStatus": 1,'
        ' "storedCredential": {"reasonType": "future_reason_v9"}}',
    )
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        make_client(mock).charge(payment_request())
    failure = exc_info.value
    assert failure.status == 200
    assert failure.correlation_id == synthetic_data.DEFAULT_CORRELATION_ID
    assert failure.raw_body is not None
    assert failure.__cause__ is not None


def test_caller_side_validation_error_stays_untyped():
    # Pre-send argument validation is NOT a payment outcome (no dispatch happened).
    import pydantic

    mock = RapMockTransport()
    mock.charge().returns_approved()
    client = make_client(mock)
    with pytest.raises(pydantic.ValidationError):
        client.payments.charge_payment("not a model")  # type: ignore[arg-type]
    assert mock.recorded_requests == []


# ---- classifier unit surface -------------------------------------------------


def test_max_retry_error_unwraps_to_underlying_reason():
    wrapped = urllib3.exceptions.MaxRetryError(
        None, "/payments", reason=urllib3.exceptions.ConnectTimeoutError("synthetic")
    )
    assert isinstance(classify_transport_exception(wrapped), RapTransientFailure)


def test_max_retry_error_without_reason_is_outcome_unknown():
    wrapped = urllib3.exceptions.MaxRetryError(None, "/payments", reason=None)
    assert isinstance(classify_transport_exception(wrapped), RapOutcomeUnknown)


def test_unknown_transport_exception_is_outcome_unknown():
    assert isinstance(classify_transport_exception(OSError("synthetic")), RapOutcomeUnknown)


def test_connect_family_single_check_covers_subclasses():
    # urllib3 hierarchy fact the classifier relies on (probed): the never-sent
    # family shares ConnectTimeoutError as base.
    assert issubclass(urllib3.exceptions.NewConnectionError, urllib3.exceptions.ConnectTimeoutError)
    assert issubclass(urllib3.exceptions.NameResolutionError, urllib3.exceptions.NewConnectionError)
    assert not issubclass(
        urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.ConnectTimeoutError
    )
