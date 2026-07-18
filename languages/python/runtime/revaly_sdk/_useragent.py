"""Adoption-telemetry User-Agent per the ADR-SDK-005 normative grammar:
``revaly-sdk-python/<semver> (python <major.minor>; <os>)``.

The exact string is a contract with platform dashboards; it carries only the
coarse tokens below — no hostnames, no distro fingerprints. A merchant token may
be APPENDED after the SDK token; the SDK prefix stays first and intact — it can
never be replaced or suppressed (enforced at transport level, where the core
cannot bypass it).
"""

from __future__ import annotations

import sys
from typing import Optional

from ._version import SDK_VERSION

PRODUCT_NAME = "revaly-sdk-python"
"""The fixed lowercase language token (ADR-SDK-005 grammar)."""


def user_agent_value(merchant_suffix: Optional[str] = None) -> str:
    """The full header value, e.g. ``revaly-sdk-python/1.2.0 (python 3.12; linux)``."""
    value = f"{PRODUCT_NAME}/{SDK_VERSION} ({runtime_token()}; {os_token()})"
    suffix = merchant_suffix.strip() if merchant_suffix else ""
    if suffix:
        value += f" {suffix}"
    return value


def runtime_token() -> str:
    """Coarse runtime token: ``python <major.minor>``."""
    return f"python {sys.version_info.major}.{sys.version_info.minor}"


def os_token() -> str:
    """Coarse platform token: ``linux`` / ``windows`` / ``darwin`` / ``other``."""
    platform = sys.platform
    if platform.startswith("win"):
        return "windows"
    if platform.startswith("linux"):
        return "linux"
    if platform == "darwin":
        return "darwin"
    return "other"
