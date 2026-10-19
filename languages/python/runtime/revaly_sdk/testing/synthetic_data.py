"""Synthetic response bodies for the mock transport (DX contract §d).

SYNTHETIC DATA ONLY (ADR-SDK-020): every identifier below is a fabricated token —
no real PAN, customer, or merchant material may ever appear here.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

DEFAULT_CORRELATION_ID = "corr-synthetic-0001"
DEFAULT_MERCHANT_TRANSACTION_ID = "mtx_synthetic_0001"
DEFAULT_TRANSACTION_ID = "06SYNTHETIC00000000000000001"
# The synthetic edge-firewall tracking reference carried by the edge-rejection row
# (``details.reference``, the shape of the ``x-azure-ref`` header — ADR-SDK-033).
EDGE_REFERENCE = "20261016T181449Z-synthetic0000000000000000000000"


def transaction_dict(transaction_status: int) -> Dict[str, Any]:
    """A terminal transaction record with the given ``transactionStatus``."""
    return {
        "transactionId": DEFAULT_TRANSACTION_ID,
        "transactionDate": "2026-01-01T00:00:00Z",
        "transactionStatus": transaction_status,
        "transactionType": "Charge",
        "merchantTransactionId": DEFAULT_MERCHANT_TRANSACTION_ID,
        "message": "synthetic outcome",
        "responseCode": "00",
        "currency": "USD",
        "amount": 2500,
        "gatewayType": "synthetic-gateway",
        "gatewayTransactionId": "gw_synthetic_0001",
    }


def transaction(transaction_status: int) -> str:
    return json.dumps(transaction_dict(transaction_status))


def transaction_group() -> str:
    """The grouped envelope shape (`transactions` list)."""
    return json.dumps({"transactions": [transaction_dict(1)]})


def pending() -> str:
    """The post-P-2 pending intent shape (`state` discriminator)."""
    return json.dumps(
        {
            "state": "pending",
            "merchantTransactionId": DEFAULT_MERCHANT_TRANSACTION_ID,
            "transactionType": "Charge",
            "receivedAt": "2026-01-01T00:00:00Z",
        }
    )


def error_body(message: str, code: Optional[str] = None) -> str:
    body: Dict[str, Any] = {"error": message}
    if code is not None:
        body["code"] = code
    return json.dumps(body)


def edge_rejection_body(reference: str = EDGE_REFERENCE) -> str:
    """The edge firewall's block body (ADR-SDK-033): ``details.edgeRejection: true``
    plus the tracking reference; the production edge serves it as ``text/html``."""
    return json.dumps(
        {
            "details": {"edgeRejection": True, "reference": reference},
            "error": "synthetic: blocked by the edge firewall; did not reach the payment platform",
        }
    )


def html_block_page() -> str:
    """The legacy edge HTML block page — not JSON, so no marker can be read."""
    return (
        "<html><head><title>403 Forbidden</title></head>"
        "<body>synthetic edge block page</body></html>"
    )
