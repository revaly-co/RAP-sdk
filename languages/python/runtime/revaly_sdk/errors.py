"""Typed failure classes and the normative outcome classifier.

The three classes of docs/failover-contract.md §2 as a Python exception hierarchy
(runtime-tdd §3). The class — never the message text, never latency — is what
licenses (or forbids) failover. The ``kind`` tokens match the other language
runtimes so cross-language log lines join cleanly.

The merchant API key can never appear in a message: no constructor on this
hierarchy ever receives it (ADR-SDK-020).
"""

from __future__ import annotations

import json
import ssl
from typing import Any, ClassVar, Optional

import urllib3.exceptions

__all__ = [
    "RapError",
    "RapPermanentRejection",
    "RapTransientFailure",
    "RapOutcomeUnknown",
    "classify_response",
    "classify_transport_exception",
]


class RapError(Exception):
    """Base of the three typed failure classes (runtime-tdd §3).

    Every instance carries the class discriminant (``kind``), the HTTP status (if
    any), the verbatim open ``code`` (if any — an open string; OQ-2 adds values
    later), the server's human ``api_error`` message, opaque ``details``, the
    ``X-Correlation-ID`` of the response, and the raw response body.
    """

    kind: ClassVar[str]

    def __init__(
        self,
        message: str,
        *,
        status: Optional[int] = None,
        code: Optional[str] = None,
        api_error: Optional[str] = None,
        details: Any = None,
        correlation_id: Optional[str] = None,
        raw_body: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.api_error = api_error
        self.details = details
        self.correlation_id = correlation_id
        self.raw_body = raw_body


class RapPermanentRejection(RapError):
    """Received and rejected (HTTP 400/401/403/404/422). Fix or decline.

    **Never fail over** — the same request fails anywhere.
    """

    kind = "PermanentRejection"


class RapTransientFailure(RapError):
    """Definitively not processed (client-provable never-sent, or 503 with
    ``code: not_processed``). Safe to route to your own gateway immediately."""

    kind = "TransientFailure"


class RapOutcomeUnknown(RapError):
    """May have been processed (deadline after send, reset mid-flight, 5xx without
    the ``not_processed`` proof). **Reconcile before acting** — failing over blind
    can double-charge (failover-contract §3)."""

    kind = "OutcomeUnknown"


_PERMANENT_REJECTION_STATUSES = frozenset({400, 401, 403, 404, 422})


def classify_response(
    *,
    status: int,
    raw_body: Optional[str],
    correlation_id: Optional[str],
    api_version: str,
) -> Optional[RapError]:
    """Classifies a received HTTP response per the failover-contract §2 algorithm.

    Returns ``None`` for 2xx. ``code`` is read verbatim as an open string;
    ``details`` stays opaque; the ``error`` message is carried but NEVER consulted
    for classification. Statuses outside the normative table (3xx, 409, 429, …)
    are ambiguous → OutcomeUnknown.

    Version-pin behaviour (runtime-tdd §1): on ``"2.0"`` the ``code`` field is not
    part of the documented contract, so a 503 with ``not_processed`` still
    classifies OutcomeUnknown — the fast-failover class narrows to client-provable
    never-sent failures only.
    """
    if 200 <= status <= 299:
        return None

    code, api_error, details = _read_error_body(raw_body)
    correlation_note = f" correlation={correlation_id}" if correlation_id else ""

    if status in _PERMANENT_REJECTION_STATUSES:
        return RapPermanentRejection(
            f"PermanentRejection: HTTP {status}{correlation_note} — fix or decline; never fail over",
            status=status,
            code=code,
            api_error=api_error,
            details=details,
            correlation_id=correlation_id,
            raw_body=raw_body,
        )

    if status == 503 and code == "not_processed" and api_version != "2.0":
        return RapTransientFailure(
            f"TransientFailure: HTTP 503 code=not_processed{correlation_note} — "
            "provably not dispatched; safe to fail over",
            status=status,
            code=code,
            api_error=api_error,
            details=details,
            correlation_id=correlation_id,
            raw_body=raw_body,
        )

    return RapOutcomeUnknown(
        f"OutcomeUnknown: HTTP {status}{correlation_note} — may have been processed; "
        "reconcile before acting",
        status=status,
        code=code,
        api_error=api_error,
        details=details,
        correlation_id=correlation_id,
        raw_body=raw_body,
    )


def classify_transport_exception(exc: BaseException) -> RapError:
    """Classifies a wire-level failure by exception TYPE ONLY — never message text
    (failover-contract §2 rules).

    urllib3's connect-phase family shares one base: ``NewConnectionError`` and
    ``NameResolutionError`` both subclass ``ConnectTimeoutError``, so a single
    isinstance check covers DNS failure, connection refused/unreachable, and the
    connect-phase timeout — all provably never-sent → TransientFailure. urllib3
    raises ``ConnectTimeoutError`` for a connect-phase expiry even under a
    total-only timeout (probed), so the proof holds for both timeout configs.

    TLS: only ``ssl.SSLCertVerificationError`` is phase-provable by type
    (certificate verification happens strictly during the handshake, before any
    HTTP bytes) → TransientFailure. Any other ``SSLError`` is not provably
    pre-send in urllib3 — both handshake and mid-stream record failures funnel to
    the same type — so it classifies OutcomeUnknown (python-specific
    conservatism, like PHP's curl errno 28; java/TS stacks CAN prove the phase).
    """
    if isinstance(exc, RapError):
        return exc

    if isinstance(exc, urllib3.exceptions.MaxRetryError):
        # Defensive: the transport always sends retries=False, so this should not
        # occur; if it does, classify the underlying reason.
        if exc.reason is not None:
            return classify_transport_exception(exc.reason)
        return _outcome_unknown_for(exc)

    if isinstance(exc, urllib3.exceptions.SSLError):
        if _chain_contains(exc, ssl.SSLCertVerificationError):
            return RapTransientFailure(
                "TransientFailure: TLS certificate verification failed during the "
                "handshake — the request was provably never sent",
                raw_body=None,
            )
        return _outcome_unknown_for(exc)

    if isinstance(exc, urllib3.exceptions.ConnectTimeoutError):
        # Covers NewConnectionError and NameResolutionError subclasses too.
        return RapTransientFailure(
            f"TransientFailure: {type(exc).__name__} — connect-phase failure; "
            "the request was provably never sent",
        )

    if isinstance(exc, urllib3.exceptions.ReadTimeoutError):
        return RapOutcomeUnknown(
            "OutcomeUnknown: deadline exceeded after the request was sent — "
            "reconcile before acting",
        )

    if isinstance(exc, urllib3.exceptions.ProtocolError):
        return RapOutcomeUnknown(
            "OutcomeUnknown: connection failed mid-flight — reconcile before acting",
        )

    # Any other urllib3 or socket-level failure: the stack has not proven the
    # request was never sent — never guess toward "safe".
    return _outcome_unknown_for(exc)


def _outcome_unknown_for(exc: BaseException) -> RapOutcomeUnknown:
    return RapOutcomeUnknown(
        f"OutcomeUnknown: {type(exc).__name__} — transport failure without "
        "never-sent proof; reconcile before acting",
    )


def _chain_contains(exc: BaseException, target: type, _depth: int = 8) -> bool:
    """Walks ``__cause__``/``__context__`` and exception args for ``target``.

    urllib3 wraps the underlying ssl error as an argument rather than a formal
    cause, so args are part of the chain here.
    """
    seen: set = set()
    stack: list = [exc]
    while stack and _depth > 0:
        _depth -= 1
        current = stack.pop()
        if id(current) in seen or not isinstance(current, BaseException):
            continue
        seen.add(id(current))
        if isinstance(current, target):
            return True
        stack.extend(a for a in current.args if isinstance(a, BaseException))
        if current.__cause__ is not None:
            stack.append(current.__cause__)
        if current.__context__ is not None:
            stack.append(current.__context__)
    return False


def _read_error_body(raw_body: Optional[str]):
    """Leniently reads ErrorResponse fields from the raw body.

    Classification must survive any body shape: non-JSON or non-object bodies
    yield all-absent fields (unrecognized/absent ``code`` falls to the
    OutcomeUnknown path per §2).
    """
    if not raw_body:
        return None, None, None
    try:
        root = json.loads(raw_body)
    except ValueError:
        return None, None, None
    if not isinstance(root, dict):
        return None, None, None
    code = root.get("code")
    error = root.get("error")
    return (
        code if isinstance(code, str) else None,
        error if isinstance(error, str) else None,
        root.get("details"),
    )
