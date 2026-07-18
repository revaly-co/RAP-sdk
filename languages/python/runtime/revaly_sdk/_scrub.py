"""The single central scrub function of this runtime (ADR-SDK-020).

Applied to debug logs, wire traces, and any payload surface the SDK emits.
Scrubbing is by ALLOWLIST — only known-safe identifier/status fields are emitted
verbatim; every other scalar is replaced with ``[scrubbed]``, so schema evolution
fails safe. PAN/CVV/PII can never appear because card and customer fields are
simply not on the list. API keys are additionally redacted at the header layer.

The allowlists are a verbatim port of the other runtimes' lists — extending them
is a reviewed change to the runtime's PCI posture; never add payload value fields.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Mapping, Optional

SCRUBBED = "[scrubbed]"
"""The replacement token for scrubbed scalar values."""

REDACTED = "[redacted]"
"""The replacement token for redacted header values."""

_FIELD_ALLOWLIST = frozenset(
    {
        "transactionid",
        "merchanttransactionid",
        "transactiontype",
        "transactionstatus",
        "transactiondate",
        "responsecode",
        "code",
        "error",
        "currency",
        "gatewaytype",
        "gatewaytransactionid",
        "gatewayroutingid",
        "correlationid",
        "status",
        "state",
        "attempts",
    }
)

# Authorization is never emitted, even redacted-by-length — the merchant API key
# must not leak shape or presence into logs (ADR-SDK-020).
_HEADER_ALLOWLIST = frozenset(
    {
        "content-type",
        "content-length",
        "user-agent",
        "x-api-version",
        "x-correlation-id",
        "api-supported-versions",
    }
)


def scrub_json(payload: Optional[str]) -> str:
    """Scrubs a JSON payload string.

    Allowlisted scalar fields pass through verbatim, all other scalars are
    replaced with :data:`SCRUBBED`; object/array structure is preserved. Non-JSON
    input returns a fixed placeholder (never the raw text).
    """
    if payload is None or payload.strip() == "":
        return ""
    try:
        root = json.loads(payload)
    except ValueError:
        return "[unparseable:scrubbed]"
    return json.dumps(_scrub_node(root, False))


def scrub_value(value: Any) -> str:
    """Scrubs an in-memory payload (a generated model or plain data), returning
    the scrubbed JSON string. Values that cannot serialize scrub to the fixed
    token."""
    try:
        if hasattr(value, "to_json") and callable(value.to_json):
            return scrub_json(value.to_json())
        if isinstance(value, (str, bytes)):
            text = value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value
            return scrub_json(text)
        return scrub_json(json.dumps(value))
    except Exception:
        return SCRUBBED


def scrub_headers(headers: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    """Scrubs an HTTP header mapping for tracing.

    Allowlisted headers pass through; everything else (including Authorization)
    becomes :data:`REDACTED`. Multi-valued headers join with commas per RFC 9110
    (User-Agent is a space-separated product-token list on the wire).
    """
    result: Dict[str, str] = {}
    if headers is None:
        return result

    for name, values in headers.items():
        if isinstance(values, (list, tuple)):
            separator = " " if name.lower() == "user-agent" else ", "
            value = separator.join(str(v) for v in values)
        else:
            value = str(values)
        result[name] = value if name.lower() in _HEADER_ALLOWLIST else REDACTED

    return dict(sorted(result.items(), key=lambda item: item[0].lower()))


def _scrub_node(node: Any, parent_key_allowlisted: bool) -> Any:
    if isinstance(node, list):
        # Scalars inside arrays keep only their parent key's status.
        return [
            _scrub_node(element, parent_key_allowlisted)
            if isinstance(element, (dict, list))
            else (element if parent_key_allowlisted else SCRUBBED)
            for element in node
        ]

    if isinstance(node, dict):
        scrubbed: Dict[str, Any] = {}
        for key, child in node.items():
            allowlisted = str(key).lower() in _FIELD_ALLOWLIST
            if isinstance(child, (dict, list)):
                scrubbed[key] = _scrub_node(child, allowlisted)
            else:
                scrubbed[key] = child if allowlisted else SCRUBBED
        return scrubbed

    # Bare scalar root.
    return node if parent_key_allowlisted else SCRUBBED
