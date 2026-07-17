"""Shared fixtures for the python runtime suite.

All card/customer material below is SYNTHETIC (ADR-SDK-020): the PAN is the
documentation test number, the key is a fabricated token. The log-capture tests
assert these exact sentinels never reach any log or exception message.
"""

from __future__ import annotations

import pytest

from revaly_sdk import RapClient
from revaly_sdk.testing import RapMockTransport

SYNTHETIC_API_KEY = "sk_synthetic_secret_0123456789"
SYNTHETIC_PAN = "4111111111111111"
SYNTHETIC_CVV = "123"
SYNTHETIC_MTX = "mtx_synthetic_0001"


@pytest.fixture
def mock_transport() -> RapMockTransport:
    return RapMockTransport()


@pytest.fixture
def client(mock_transport: RapMockTransport) -> RapClient:
    return RapClient(SYNTHETIC_API_KEY, transport=mock_transport)


def make_client(mock_transport: RapMockTransport, **kwargs) -> RapClient:
    return RapClient(SYNTHETIC_API_KEY, transport=mock_transport, **kwargs)


def payment_request(with_card: bool = False):
    from revaly_sdk_core.models.credit_card import CreditCard
    from revaly_sdk_core.models.payment_method import PaymentMethod
    from revaly_sdk_core.models.payment_request import PaymentRequest

    payment_method = None
    if with_card:
        payment_method = PaymentMethod(
            first_name="Synthetic",
            last_name="Cardholder",
            credit_card=CreditCard(
                number=SYNTHETIC_PAN,
                card_verification_code=SYNTHETIC_CVV,
                expiry_month="12",
                expiry_year="2030",
            ),
        )
    return PaymentRequest(
        amount=2500,
        merchant_transaction_id=SYNTHETIC_MTX,
        currency="USD",
        payment_method=payment_method,
    )
