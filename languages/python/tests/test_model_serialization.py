"""Empirical pins on generated-core behavior the runtime depends on.

anyOf wrappers (spec v2.4.0, SC-408 B4: the lookup unions switched
oneOf -> anyOf with branches ordered most-specific first): discrimination is
the STOCK anyOf template — ``from_json`` tries branches in declaration order
and pydantic enforces each branch's required members while ignoring unknown
fields, so binding is names-only and additive server-side schema evolution
keeps binding. No python template fork is needed for anyOf.

oneOf wrapper (spec v2.19.0, SC-409: each ``listTransactions`` item is a
flat ``TransactionListItem`` or a ``TransactionListPaymentMethodItem``): the
forked ``model_oneof.mustache`` discriminates it — strict names-and-aliases
pass first, then the recognized-field coverage tiebreak, so additive
server-side fields keep binding. The runtime keeps reading raw bodies
everywhere (repo rule 5) — these pins serve merchants calling the generated
lookups and list directly.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from revaly_sdk_core.models.error_response import ErrorResponse
from revaly_sdk_core.models.get_transaction_by_id200_response import (
    GetTransactionById200Response,
)
from revaly_sdk_core.models.get_transaction_by_merchant_transaction_id200_response import (
    GetTransactionByMerchantTransactionId200Response,
)
from revaly_sdk_core.models.list_transactions200_response_inner import (
    ListTransactions200ResponseInner,
)
from revaly_sdk_core.models.payment_request import PaymentRequest
from revaly_sdk_core.models.pending_transaction_response import PendingTransactionResponse
from revaly_sdk_core.models.stored_credential import StoredCredential
from revaly_sdk_core.models.transaction_group_response import TransactionGroupResponse
from revaly_sdk_core.models.transaction_list_item import TransactionListItem
from revaly_sdk_core.models.transaction_list_payment_method_item import (
    TransactionListPaymentMethodItem,
)
from revaly_sdk_core.models.transaction_response import TransactionResponse
from revaly_sdk.testing import synthetic_data

TERMINAL_BODY = synthetic_data.transaction(1)
GROUP_BODY = synthetic_data.transaction_group()
PENDING_BODY = synthetic_data.pending()

LIST_FLAT_ROW = {
    "transactionId": "t-1",
    "transactionDate": "2025-09-13T03:19:54.86Z",
    "transactionStatus": 1,
    "responseCode": "10000",
    "transactionType": "Charge",
    "amount": 2500,
    "currencyCode": "USD",
}
LIST_PAYMENT_METHOD_ROW = {
    "transaction": {
        "transactionId": "t-2",
        "transactionDate": "2025-12-02T14:44:42.209Z",
        "transactionStatus": 1,
        "message": "Succeeded!",
        "responseCode": "10000",
        "transactionType": "CreateCreditCard",
        "paymentMethod": {
            "paymentMethodId": "pm-1",
            "lastFourDigits": "1111",
            "firstSixDigits": "411111",
            "cardType": "VISA",
            "storageState": "Cached",
            "issuerIdentificationNumber": "41111111",
        },
    }
}


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


# ---- oneOf list-row wrapper (spec v2.19.0: forked model_oneof template) ------


def test_list_row_wrapper_binds_flat_item():
    wrapper = ListTransactions200ResponseInner.from_json(json.dumps(LIST_FLAT_ROW))
    assert isinstance(wrapper.actual_instance, TransactionListItem)
    row = wrapper.actual_instance
    assert row.transaction_id == "t-1"
    assert row.transaction_date == datetime(2025, 9, 13, 3, 19, 54, 860000, tzinfo=timezone.utc)
    assert row.transaction_status == 1
    assert row.response_code == "10000"
    assert row.transaction_type == "Charge"
    assert row.amount == 2500
    assert row.currency_code == "USD"


def test_list_row_wrapper_binds_payment_method_item():
    # The flat branch lenient-matches this body too (its one required member,
    # transactionId, is nullable and from_dict passes it as None); the strict
    # names pass picks the branch that recognizes `transaction`.
    wrapper = ListTransactions200ResponseInner.from_json(json.dumps(LIST_PAYMENT_METHOD_ROW))
    assert isinstance(wrapper.actual_instance, TransactionListPaymentMethodItem)
    transaction = wrapper.actual_instance.transaction
    assert transaction.transaction_id == "t-2"
    assert transaction.transaction_type == "CreateCreditCard"
    assert transaction.payment_method is not None
    assert transaction.payment_method.last_four_digits == "1111"


@pytest.mark.parametrize(
    ("row", "branch_cls"),
    [
        (LIST_FLAT_ROW, TransactionListItem),
        (LIST_PAYMENT_METHOD_ROW, TransactionListPaymentMethodItem),
    ],
    ids=["flat", "payment_method"],
)
def test_list_row_wrapper_binds_additive_row(row, branch_cls):
    # A server newer than the pinned spec (additive top-level field) must keep
    # binding. A flat row binds by elimination (the payment-method branch requires
    # `transaction`); a payment-method row lenient-matches both branches, neither
    # strict-matches the unknown name, and the coverage tiebreak decides (names only).
    body = json.dumps({**row, "futureAdditiveField": "x"})
    wrapper = ListTransactions200ResponseInner.from_json(body)
    assert isinstance(wrapper.actual_instance, branch_cls)


def test_list_transactions_call_decodes_each_row_branch(mock_transport, client):
    mock_transport.list_transactions().returns(
        200, json.dumps([LIST_FLAT_ROW, LIST_PAYMENT_METHOD_ROW])
    )
    rows = client.transactions.list_transactions()
    assert [type(row.actual_instance) for row in rows] == [
        TransactionListItem,
        TransactionListPaymentMethodItem,
    ]


def test_list_row_wrapper_binds_malformed_payment_method_row_as_empty_flat_item():
    # KNOWN EDGE, pinned so a fork revision flips it deliberately (precedent:
    # ADR-SDK-034 §3). A payment-method row whose card digits break their
    # pattern fails the payment-method branch; the flat branch lenient-matches
    # any object (its one required member is nullable), and the fork binds a
    # single lenient match without the strict/coverage pass — so the row comes
    # back as an EMPTY TransactionListItem, not an error. PHP raises here
    # instead; .NET, Go, Java and TypeScript return the payment-method row
    # with the value as sent. Backbone normalizes the digits before it stores a
    # row (ADR 021, SC-879), so only a row stored before 2026-11-05 can do this.
    row = json.loads(json.dumps(LIST_PAYMENT_METHOD_ROW))
    row["transaction"]["paymentMethod"]["lastFourDigits"] = ""
    wrapper = ListTransactions200ResponseInner.from_json(json.dumps(row))
    assert isinstance(wrapper.actual_instance, TransactionListItem)
    assert wrapper.actual_instance.transaction_id is None


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


def test_merchant_transaction_id_over_100_is_left_to_the_platform():
    # ADR-SDK-034 (SC-886): the spec bound (100) is the platform's to enforce; the model
    # no longer refuses a longer value before sending.
    request = PaymentRequest(amount=1, merchant_transaction_id="x" * 101)
    assert json.loads(request.to_json())["merchantTransactionId"] == "x" * 101
