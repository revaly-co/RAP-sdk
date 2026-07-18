"""Empirical pins on generated-core behavior the runtime depends on.

KNOWN CORE LIMITATION (oneOf wrappers): the generated union wrappers raise
``ValueError("Multiple matches found...")`` for EVERY valid response shape —
the branch models are all-optional, so every body matches more than one branch.
The runtime reads raw bodies everywhere (repo rule 5) and is unaffected; these
probes pin the defect until the python oneOf template fork lands (java PR #18 /
typescript PR #25 pattern), at which point they FLIP to assert correct binding.
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
from revaly_sdk_core.models.stored_credential import StoredCredential
from revaly_sdk_core.models.transaction_response import TransactionResponse
from revaly_sdk.testing import synthetic_data

TERMINAL_BODY = synthetic_data.transaction(1)
GROUP_BODY = synthetic_data.transaction_group()
PENDING_BODY = synthetic_data.pending()


# ---- KNOWN CORE LIMITATION: oneOf wrapper discrimination ---------------------


@pytest.mark.parametrize("body", [TERMINAL_BODY, GROUP_BODY], ids=["terminal", "group"])
def test_by_id_wrapper_throws_multiple_matches_on_valid_shapes(body):
    with pytest.raises(ValueError, match="Multiple matches found"):
        GetTransactionById200Response.from_json(body)


@pytest.mark.parametrize(
    "body", [TERMINAL_BODY, GROUP_BODY, PENDING_BODY], ids=["terminal", "group", "pending"]
)
def test_by_merchant_wrapper_throws_multiple_matches_on_valid_shapes(body):
    with pytest.raises(ValueError, match="Multiple matches found"):
        GetTransactionByMerchantTransactionId200Response.from_json(body)


def test_branch_models_bind_directly_from_raw():
    # The raw-read path the runtime actually uses is unaffected by the wrapper.
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
