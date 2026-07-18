"""Empirical pins on generated-core behavior the runtime depends on.

oneOf wrappers: discrimination comes from the forked
``pipeline/python/templates/model_oneof.mustache`` (java PR #18 / typescript
PR #25 pattern) — a strict top-level-key pass binds spec-aligned bodies
uniquely, a recognized-field coverage tiebreak keeps additive server-side
schema evolution binding, and genuinely ambiguous payloads still raise the
stock error. The runtime keeps reading raw bodies everywhere (repo rule 5) —
the fork serves merchants calling the generated lookups directly.
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


# ---- oneOf wrapper discrimination (forked model_oneof.mustache) --------------


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
def test_wrappers_bind_additive_terminal_via_coverage_tiebreak(wrapper_cls):
    # A server newer than the pinned spec (additive top-level field) fails the
    # strict pass for every branch; the recognized-field coverage tiebreak keeps
    # the terminal shape binding (java fork precedent).
    body = json.dumps(
        {**synthetic_data.transaction_dict(1), "settlementBatchId": "batch_synthetic_01"}
    )
    wrapper = wrapper_cls.from_json(body)
    assert isinstance(wrapper.actual_instance, TransactionResponse)


@pytest.mark.parametrize(
    "wrapper_cls",
    [GetTransactionById200Response, GetTransactionByMerchantTransactionId200Response],
    ids=["by_id", "by_merchant"],
)
def test_wrappers_still_raise_on_genuinely_ambiguous_body(wrapper_cls):
    # An empty object matches every all-optional branch with zero coverage — the
    # fork resolves nothing and the stock error is preserved.
    with pytest.raises(ValueError, match="Multiple matches found"):
        wrapper_cls.from_json("{}")


def test_wrapper_validator_discriminates_raw_dict():
    # Fork site 2: assigning a raw dict binds the right branch instead of
    # silently union-coercing into the first all-optional branch.
    terminal = GetTransactionById200Response(actual_instance=json.loads(TERMINAL_BODY))
    assert isinstance(terminal.actual_instance, TransactionResponse)
    group = GetTransactionById200Response(actual_instance=json.loads(GROUP_BODY))
    assert isinstance(group.actual_instance, TransactionGroupResponse)
    pending = GetTransactionByMerchantTransactionId200Response(
        actual_instance=json.loads(PENDING_BODY)
    )
    assert isinstance(pending.actual_instance, PendingTransactionResponse)


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
        TransactionResponse.from_json(
            '{"storedCredential": {"reasonType": "future_reason_v9"}}'
        )


def test_known_reason_type_binds():
    transaction = TransactionResponse.from_json(
        '{"storedCredential": {"reasonType": "recurring"}}'
    )
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
    required = {
        name for name, field in PaymentRequest.model_fields.items() if field.is_required()
    }
    assert required == {"amount", "merchant_transaction_id"}


def test_merchant_transaction_id_max_length_100():
    with pytest.raises(ValidationError):
        PaymentRequest(amount=1, merchant_transaction_id="x" * 101)
    PaymentRequest(amount=1, merchant_transaction_id="x" * 100)
