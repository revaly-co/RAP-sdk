"""ADR-SDK-034 amendment of 2026-11-26 (SC-1018, OQ-19): for the rtnData block (RtnData and
its ten nested models, the only schemas the platform exempts) the SDK never refuses a value
because it breaks a documented pattern, minimum or minLength; the platform's own rule
decides. Each table below breaks every such rule the spec documents in the family, so a step
that misses one field, shape or file fails here.

Every value is built through the public constructor, PaymentRequest.from_dict or attribute
assignment (validate_assignment is on), sent through the client, and read back from the mock
transport's recorded request. Value lists already pass through (the open-vocabulary enum
fork), and types and the purchaseDate date-time stay checked (decision 1: the typed model is
the SDK's interface). The checks kept outside rtnData are pinned in test_length_bounds.py.

All values are synthetic (ADR-SDK-020); none is card data.
"""

from __future__ import annotations

import json
import re

import pytest
from pydantic import ValidationError

from revaly_sdk_core.models.authorize_request import AuthorizeRequest
from revaly_sdk_core.models.payment_request import PaymentRequest
from revaly_sdk_core.models.rtn_data import RtnData
from revaly_sdk_core.models.rtn_data_additional_transaction_data import (
    RtnDataAdditionalTransactionData,
)
from revaly_sdk_core.models.rtn_data_billing_data import RtnDataBillingData
from revaly_sdk_core.models.rtn_data_customer_data import RtnDataCustomerData
from revaly_sdk_core.models.rtn_data_device_data import RtnDataDeviceData
from revaly_sdk_core.models.rtn_data_merchant_data import RtnDataMerchantData
from revaly_sdk_core.models.rtn_data_order_data import RtnDataOrderData
from revaly_sdk_core.models.rtn_data_seller_data import RtnDataSellerData
from revaly_sdk_core.models.rtn_data_shipping_data import RtnDataShippingData

from conftest import SYNTHETIC_MTX, make_client

DASHED_DATE = "2024-01-15"  # every rtnData date field documents ^\d{8}$ (YYYYMMDD)
UNLISTED = "unlisted_synthetic_value"

# rtnData block -> {wire key: a value that breaks the field's documented rule}.
PATTERN_BREAKS = {
    "additionalTransactionData": {
        "fraudPreventionPlatform": "not allowed!",  # ^[A-Za-z0-9._:-]{1,128}$
        "fullPan": "1234-5678-9012",  # ^\d{13,19}$, and long enough for minLength 13
    },
    "customerData": {
        "accountOpenedDate": DASHED_DATE,
        "accountLastChangedDate": DASHED_DATE,
        "passwordLastChangedDate": DASHED_DATE,
        "paymentMethodAddedDate": DASHED_DATE,
    },
    "merchantData": {"merchantAccountOpenedDate": DASHED_DATE},
    "orderData": {"preOrderDate": DASHED_DATE, "recurringEndDate": DASHED_DATE},
    "shippingData": {"addressFirstUsedDate": DASHED_DATE},
}
MINIMUM_BREAKS = {
    "customerData": {
        "transactionSuccessfulCountLastSixMonths": -1,
        "transactionAttemptedCountLast24Hours": -1,
        "transactionAttemptedCountLastYear": -1,
        "paymentMethodAddAttemptCountLast24Hours": -1,
        "registeredAccountTenure": -1,
        "daysSinceNameChange": -1,
        "daysSinceEmailChange": -1,
        "daysSincePasswordChange": -1,
        "daysSincePostalCodeChange": -1,
        "daysSinceAddressChange": -1,
        "daysSincePhoneChange": -1,
        "daysSinceShipToNameChange": -1,
    },
    "orderData": {
        "itemCount": -1,
        "highestPriceItemPrice": -1,
        "installmentPaymentCount": -1,
        "recurringIntervalDays": 0,  # the one minimum of 1
        "giftCardCount": -1,
        "giftCardAmount": -1,
    },
    "shippingData": {"shippingAddressCount": -1, "daysSinceShipToAddressChange": -1},
}
MIN_LENGTH_BREAKS = {
    "additionalTransactionData": {"fullPan": "1234"},  # minLength 13
    "billingData": {"country": "U"},  # minLength 2
    "deviceData": {"country": "U"},
    "shippingData": {"country": "U"},
}
UNLISTED_VALUES = {
    "additionalTransactionData": {
        "providerAuthDecision": UNLISTED,
        "paymentRail": UNLISTED,
        "posEntryMode": UNLISTED,
        "merchantTrustLevel": UNLISTED,
        "cardBrand": UNLISTED,
        "messageCategory": UNLISTED,
    },
    "customerData": {
        "accountAgeIndicator": "05",  # documented values 01 to 04
        "accountChangeIndicator": UNLISTED,
        "passwordChangeIndicator": UNLISTED,
        "paymentMethodAgeIndicator": UNLISTED,
        "accountAuthenticationMethod": UNLISTED,
        "isRegisteredCustomer": UNLISTED,
        "isRegistrationUpdated": UNLISTED,
    },
    "deviceData": {"channel": UNLISTED, "deviceType": UNLISTED},
    "merchantData": {"merchantAccountAgeIndicator": UNLISTED},
    "orderData": {"alternatePaymentIndicator": UNLISTED, "isCouponUsed": UNLISTED},
    "sellerData": {"sellerRegion": UNLISTED, "transactionTypeIndicator": UNLISTED},
    "shippingData": {
        "shippingIndicator": UNLISTED,
        "addressFirstUsedIndicator": UNLISTED,
        "deliveryTimeframeIndicator": UNLISTED,
    },
}
RULES = {"pattern": PATTERN_BREAKS, "minimum": MINIMUM_BREAKS, "min_length": MIN_LENGTH_BREAKS}

BLOCK_MODELS = {
    "additionalTransactionData": RtnDataAdditionalTransactionData,
    "billingData": RtnDataBillingData,
    "customerData": RtnDataCustomerData,
    "deviceData": RtnDataDeviceData,
    "merchantData": RtnDataMerchantData,
    "orderData": RtnDataOrderData,
    "sellerData": RtnDataSellerData,
    "shippingData": RtnDataShippingData,
}


def _attr(wire_key: str) -> str:
    """The model attribute for a wire key (the generator's snake_case form)."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", wire_key).lower()


def _fields(block: str, values: dict) -> dict:
    model = BLOCK_MODELS[block]
    fields = {_attr(key): value for key, value in values.items()}
    unknown = sorted(set(fields) - set(model.model_fields))
    assert not unknown, f"the test table names no field of {model.__name__}: {unknown}"
    return fields


def _constructed(values: dict) -> RtnData:
    return RtnData(
        **{
            _attr(block): BLOCK_MODELS[block](**_fields(block, fields))
            for block, fields in values.items()
        }
    )


def _sent_rtn_data(mock_transport) -> dict:
    assert len(mock_transport.recorded_requests) == 1
    return json.loads(mock_transport.recorded_requests[-1].body)["rtnData"]


def _charge(mock_transport, request: PaymentRequest) -> dict:
    mock_transport.charge().returns_approved()
    make_client(mock_transport).charge(request)
    return _sent_rtn_data(mock_transport)


def _payment_request(rtn_data: RtnData) -> PaymentRequest:
    return PaymentRequest(
        amount=1, merchant_transaction_id=SYNTHETIC_MTX, currency="USD", rtn_data=rtn_data
    )


@pytest.mark.parametrize("rule", sorted(RULES))
def test_constructed_value_breaking_a_rule_is_sent_as_given(mock_transport, rule):
    # AC3, D2: construction is where a pattern, minimum or minLength refused the value.
    values = RULES[rule]

    assert _charge(mock_transport, _payment_request(_constructed(values))) == values


@pytest.mark.parametrize("rule", sorted(RULES))
def test_from_dict_value_breaking_a_rule_is_sent_as_given(mock_transport, rule):
    # AC3: the dict path (the nested PaymentRequest.from_dict) ran the same validators.
    values = RULES[rule]
    request = PaymentRequest.from_dict(
        {"amount": 1, "merchantTransactionId": SYNTHETIC_MTX, "currency": "USD", "rtnData": values}
    )

    assert _charge(mock_transport, request) == values


@pytest.mark.parametrize("rule", sorted(RULES))
def test_assigned_value_breaking_a_rule_is_sent_as_given(mock_transport, rule):
    # X6: validate_assignment=True made assignment a third place the rule fired.
    values = RULES[rule]
    request = _payment_request(RtnData(**{_attr(block): BLOCK_MODELS[block]() for block in values}))
    for block, fields in values.items():
        model = getattr(request.rtn_data, _attr(block))
        for attr, value in _fields(block, fields).items():
            setattr(model, attr, value)

    assert _charge(mock_transport, request) == values


@pytest.mark.parametrize("rule", sorted(RULES))
def test_authorize_sends_a_value_breaking_a_rule_as_given(mock_transport, rule):
    # AC3: rtnData rides AuthorizeRequest too.
    values = RULES[rule]
    mock_transport.authorize().returns_approved()
    request = AuthorizeRequest(
        amount=1,
        merchant_transaction_id=SYNTHETIC_MTX,
        currency="USD",
        rtn_data=_constructed(values),
    )

    make_client(mock_transport).authorize(request)

    assert _sent_rtn_data(mock_transport) == values


def test_unlisted_value_list_entry_is_sent_as_given(mock_transport):
    # D1 "value list", D2 "the enum validators ... are untouched": the open-vocabulary fork
    # already passes every unlisted value through; the change must keep that.
    request = _payment_request(_constructed(UNLISTED_VALUES))

    assert _charge(mock_transport, request) == UNLISTED_VALUES


@pytest.mark.parametrize(
    ("block", "values", "error_type"),
    [
        ("orderData", {"itemCount": "3"}, "int_type"),
        ("orderData", {"purchaseDate": "not a date"}, "datetime_from_date_parsing"),
        ("additionalTransactionData", {"fullPan": 1234}, "string_type"),
        ("customerData", {"isFreeAccount": "yes"}, "bool_type"),
    ],
    ids=["int", "date-time", "string", "bool"],
)
def test_wrong_type_is_still_refused(block, values, error_type):
    # D1: types and formats stay in every SDK; the typed model is the SDK's interface.
    with pytest.raises(ValidationError) as refused:
        BLOCK_MODELS[block](**_fields(block, values))

    errors = refused.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == error_type
