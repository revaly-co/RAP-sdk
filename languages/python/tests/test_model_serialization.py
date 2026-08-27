"""Empirical pins on generated-core behavior the runtime depends on.

anyOf wrappers (spec v2.4.0, SC-408 B4: the lookup unions switched
oneOf -> anyOf with branches ordered most-specific first): discrimination is
the STOCK anyOf template — ``from_json`` tries branches in declaration order
and pydantic enforces each branch's required members while ignoring unknown
fields, so binding is names-only and additive server-side schema evolution
keeps binding. No python template fork is needed for anyOf (the forked
``model_oneof.mustache`` stays for any future oneOf; the v2.4.0 spec has
none). The runtime keeps reading raw bodies everywhere (repo rule 5) — these
pins serve merchants calling the generated lookups directly.
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from revaly_sdk_core.models.error_response import ErrorResponse
from revaly_sdk_core.models.get_transaction_by_id200_response import (
    GetTransactionById200Response,
)
from revaly_sdk_core.models.get_transaction_by_merchant_transaction_id200_response import (
    GetTransactionByMerchantTransactionId200Response,
)
from revaly_sdk_core.models.payment_request import PaymentRequest
from revaly_sdk_core.models.pending_transaction_response import PendingTransactionResponse
from revaly_sdk_core.models.stored_credential import StoredCredential
from revaly_sdk_core.models.transaction_group_response import TransactionGroupResponse
from revaly_sdk_core.models.transaction_response import TransactionResponse
from revaly_sdk.testing import synthetic_data

TERMINAL_BODY = synthetic_data.transaction(1)
GROUP_BODY = synthetic_data.transaction_group()
PENDING_BODY = synthetic_data.pending()


# ---- anyOf wrapper discrimination (stock template, ordered branches) ---------


def test_by_id_wrapper_binds_terminal():
    wrapper = GetTransactionById200Response.from_json(TERMINAL_BODY)
    assert isinstance(wrapper.actual_instance, TransactionResponse)
    assert wrapper.actual_instance.transaction_status == 1


def test_by_id_wrapper_binds_group():
    wrapper = GetTransactionById200Response.from_json(GROUP_BODY)
    assert isinstance(wrapper.actual_instance, TransactionGroupResponse)
    assert wrapper.actual_instance.transactions[0].transaction_status == 1


def test_by_merchant_wrapper_binds_terminal():
    wrapper = GetTransactionByMerchantTransactionId200Response.from_json(TERMINAL_BODY)
    assert isinstance(wrapper.actual_instance, TransactionResponse)


def test_by_merchant_wrapper_binds_group():
    wrapper = GetTransactionByMerchantTransactionId200Response.from_json(GROUP_BODY)
    assert isinstance(wrapper.actual_instance, TransactionGroupResponse)


def test_by_merchant_wrapper_binds_pending():
    wrapper = GetTransactionByMerchantTransactionId200Response.from_json(PENDING_BODY)
    assert isinstance(wrapper.actual_instance, PendingTransactionResponse)
    assert wrapper.actual_instance.state == "pending"


@pytest.mark.parametrize(
    "wrapper_cls",
    [GetTransactionById200Response, GetTransactionByMerchantTransactionId200Response],
    ids=["by_id", "by_merchant"],
)
def test_wrappers_bind_additive_terminal(wrapper_cls):
    # A server newer than the pinned spec (additive top-level field) must keep
    # binding: pydantic ignores unknown fields, and the narrower branches still
    # reject the body by their missing required members (names only).
    body = json.dumps(
        {**synthetic_data.transaction_dict(1), "settlementBatchId": "batch_synthetic_01"}
    )
    wrapper = wrapper_cls.from_json(body)
    assert isinstance(wrapper.actual_instance, TransactionResponse)


def test_additive_field_still_binds_pending():
    # The additive-evolution hazard on the pending branch (one new platform
    # field re-binding a pending body as a terminal transaction) cannot occur:
    # pydantic ignores the unknown field and pending still matches first.
    body = json.dumps({**json.loads(PENDING_BODY), "reservationExpiresAt": "2026-08-01T00:00:00Z"})
    wrapper = GetTransactionByMerchantTransactionId200Response.from_json(body)
    assert isinstance(wrapper.actual_instance, PendingTransactionResponse)


def test_nested_additive_field_still_binds_group():
    body = json.loads(GROUP_BODY)
    body["transactions"][0]["settlementBatchId"] = "batch_synthetic_01"
    wrapper = GetTransactionByMerchantTransactionId200Response.from_json(json.dumps(body))
    assert isinstance(wrapper.actual_instance, TransactionGroupResponse)


@pytest.mark.parametrize(
    "wrapper_cls",
    [GetTransactionById200Response, GetTransactionByMerchantTransactionId200Response],
    ids=["by_id", "by_merchant"],
)
def test_empty_object_binds_terminal_branch(wrapper_cls):
    # Pinned stock-anyOf behavior (changed from the oneOf-fork era, which
    # raised): an empty object carries neither `transactions` nor `state`, so
    # per the documented discriminators it IS a single TransactionResponse —
    # the all-optional terminal branch binds. Does not occur on the wire.
    wrapper = wrapper_cls.from_json("{}")
    assert isinstance(wrapper.actual_instance, TransactionResponse)


def test_wrapper_discriminates_raw_dict_via_from_dict():
    # The wire path (from_json / from_dict) discriminates raw payloads; direct
    # actual_instance assignment accepts constructed model instances only
    # (pinned below) — that is the stock anyOf construction surface.
    terminal = GetTransactionById200Response.from_dict(json.loads(TERMINAL_BODY))
    assert isinstance(terminal.actual_instance, TransactionResponse)
    group = GetTransactionById200Response.from_dict(json.loads(GROUP_BODY))
    assert isinstance(group.actual_instance, TransactionGroupResponse)
    pending = GetTransactionByMerchantTransactionId200Response.from_dict(json.loads(PENDING_BODY))
    assert isinstance(pending.actual_instance, PendingTransactionResponse)


def test_wrapper_rejects_raw_dict_on_direct_assignment():
    # Pinned stock-anyOf behavior (changed from the oneOf-fork era, which
    # discriminated dicts on assignment): actual_instance takes model
    # instances; a raw dict raises instead of silently union-coercing.
    with pytest.raises(ValidationError):
        GetTransactionById200Response(actual_instance=json.loads(TERMINAL_BODY))


def test_wrapper_validator_instance_passthrough():
    transaction = TransactionResponse.from_json(TERMINAL_BODY)
    wrapper = GetTransactionById200Response(actual_instance=transaction)
    assert wrapper.actual_instance is transaction


def test_branch_models_bind_directly_from_raw():
    # The raw-read path the runtime actually uses (repo rule 5) stays valid.
    transaction = TransactionResponse.from_json(TERMINAL_BODY)
    assert transaction.transaction_status == 1
    assert transaction.merchant_transaction_id == synthetic_data.DEFAULT_MERCHANT_TRANSACTION_ID


# ---- §A3: closed standalone enums on response models -------------------------


def test_unknown_reason_type_on_response_raises_validation_error():
    # Pinned: pydantic rejects unknown wire values for the closed
    # StoredCredentialReasonType enum on a RESPONSE model. The runtime contains
    # this as OutcomeUnknown post-dispatch (see test_classification).
    with pytest.raises(ValidationError):
        TransactionResponse.from_json('{"storedCredential": {"reasonType": "future_reason_v9"}}')


def test_known_reason_type_binds():
    transaction = TransactionResponse.from_json('{"storedCredential": {"reasonType": "recurring"}}')
    assert transaction.stored_credential is not None
    assert transaction.stored_credential.reason_type == "recurring"


# ---- ErrorResponse.code: open vocabulary (ADR-SDK-023 generation override) ---


def test_unknown_error_code_passes_through_verbatim():
    error = ErrorResponse.from_json('{"error": "boom", "code": "totally_new_code_v9"}')
    assert error.code == "totally_new_code_v9"


def test_not_processed_code_accessible():
    error = ErrorResponse.from_json('{"error": "breaker open", "code": "not_processed"}')
    assert error.code == "not_processed"


def test_absent_code_is_none():
    assert ErrorResponse.from_json('{"error": "plain 4xx"}').code is None


# ---- serialization of unset optionals ----------------------------------------


def test_unset_optionals_are_omitted():
    # The dotnet optional-enum serialization trap is ABSENT in the python core.
    assert json.loads(StoredCredential().to_json()) == {}


def test_explicit_none_on_nullable_field_is_kept():
    assert json.loads(StoredCredential(reason_type=None).to_json()) == {"reasonType": None}


def test_payment_request_requires_amount_and_merchant_transaction_id():
    required = {name for name, field in PaymentRequest.model_fields.items() if field.is_required()}
    assert required == {"amount", "merchant_transaction_id"}


def test_merchant_transaction_id_max_length_100():
    with pytest.raises(ValidationError):
        PaymentRequest(amount=1, merchant_transaction_id="x" * 101)
    PaymentRequest(amount=1, merchant_transaction_id="x" * 100)
