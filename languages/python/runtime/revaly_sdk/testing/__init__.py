"""Merchant-side testability surface (DX contract §d): the mock transport and
its synthetic data. No network, synthetic data only (ADR-SDK-020)."""

from . import synthetic_data
from .mock_transport import MockOperation, RapMockTransport, RecordedRequest

__all__ = [
    "MockOperation",
    "RapMockTransport",
    "RecordedRequest",
    "synthetic_data",
]
