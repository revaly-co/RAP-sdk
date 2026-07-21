"""The first-class mock transport (runtime-tdd §8 · DX contract §d).

``RapMockTransport`` replaces only the WIRE: it is passed as ``transport=`` to
:class:`revaly_sdk.RapClient`, so header injection and failure classification —
the safety-relevant runtime code — run identically in merchant tests. Transport
failures are simulated with REAL urllib3 exception instances (never message
strings), so classification exercises the exact production code path; scripted
responses cover every row of the failover-contract §2 table and both §3 reconcile
verdicts. No network is ever touched; all bodies are synthetic (ADR-SDK-020).

The mock asserts ``User-Agent`` presence on every request (§8).
"""

from __future__ import annotations

import socket
import ssl
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Tuple
from urllib.parse import urlsplit

import urllib3.exceptions

from . import synthetic_data
from .._useragent import PRODUCT_NAME
from ..transport import RapWireRequest, RapWireResponse

_ScriptedOutcome = Tuple[str, Any]  # ("body", (status, body, headers)) | ("raise", exc)


@dataclass(frozen=True)
class RecordedRequest:
    """One request the mock received, exactly as the transport prepared it."""

    method: str
    url: str
    headers: Mapping[str, str]
    body: Optional[str]


class MockOperation:
    """A scripted outcome queue for one stubbed operation.

    The scenario methods read as the failover-contract taxonomy: every §2 row has
    a method, and consecutive outcomes can be scripted so merchants can test
    their suppression/escalation logic. When the queue runs dry the LAST scripted
    outcome repeats.
    """

    def __init__(self) -> None:
        self._queue: List[_ScriptedOutcome] = []

    def _next(self) -> _ScriptedOutcome:
        if not self._queue:
            raise AssertionError("mock: operation stubbed but no outcome scripted")
        if len(self._queue) > 1:
            return self._queue.pop(0)
        return self._queue[0]

    # ---- success outcomes ---------------------------------------------------

    def returns_approved(self) -> "MockOperation":
        """200 with a synthetic approved transaction (``transactionStatus`` 1)."""
        return self._push_body(200, synthetic_data.transaction(1))

    def returns_declined(self) -> "MockOperation":
        """200 with a synthetic declined transaction (``transactionStatus`` 2)."""
        return self._push_body(200, synthetic_data.transaction(2))

    def returns_error_outcome(self) -> "MockOperation":
        """200 with a synthetic terminal-error transaction (``transactionStatus`` 3)."""
        return self._push_body(200, synthetic_data.transaction(3))

    def returns_unmapped_status(self, transaction_status: int) -> "MockOperation":
        """200 with an unmapped ``transactionStatus`` (forward-compat drills)."""
        return self._push_body(200, synthetic_data.transaction(transaction_status))

    def returns_transaction_group(self) -> "MockOperation":
        """200 with the grouped envelope shape."""
        return self._push_body(200, synthetic_data.transaction_group())

    # ---- PermanentRejection rows (§2) ---------------------------------------

    def returns_permanent_rejection(self, status: int) -> "MockOperation":
        """One of the §2 PermanentRejection statuses (400/401/403/404/422)."""
        return self._push_body(status, synthetic_data.error_body("synthetic rejection"))

    # ---- TransientFailure rows (§2) -----------------------------------------

    def returns_not_processed_503(self) -> "MockOperation":
        """503 + ``code: not_processed`` — the provable non-dispatch signal
        (immediate failover)."""
        return self._push_body(
            503, synthetic_data.error_body("temporarily unable to process", "not_processed")
        )

    def throws_connection_refused(self) -> "MockOperation":
        """Connection refused — provably never sent (``NewConnectionError``)."""
        return self._push_raise(
            urllib3.exceptions.NewConnectionError(
                None,
                "synthetic: failed to establish a new connection",  # type: ignore[arg-type]
            )
        )

    def throws_dns_failure(self) -> "MockOperation":
        """DNS resolution failure — provably never sent (``NameResolutionError``)."""
        return self._push_raise(
            urllib3.exceptions.NameResolutionError(
                "api.synthetic.invalid",
                None,  # type: ignore[arg-type]
                socket.gaierror(-2, "synthetic: name resolution failure"),
            )
        )

    def throws_ssl_handshake_failure(self) -> "MockOperation":
        """TLS certificate verification failure — the phase-provable TLS case
        (``ssl.SSLCertVerificationError`` in the chain) — provably never sent."""
        return self._push_raise(
            urllib3.exceptions.SSLError(
                ssl.SSLCertVerificationError(1, "synthetic: certificate verify failed")
            )
        )

    def throws_connect_timeout(self) -> "MockOperation":
        """Connect-phase timeout (``ConnectTimeoutError``). urllib3 types this
        distinctly from after-send timeouts — even under a total-only timeout —
        so it carries never-sent proof and classifies TransientFailure (unlike
        the PHP runtime, whose curl errno 28 covers both phases)."""
        return self._push_raise(
            urllib3.exceptions.ConnectTimeoutError("synthetic: connect timeout")
        )

    # ---- OutcomeUnknown rows (§2) -------------------------------------------

    def returns_bare_503(self) -> "MockOperation":
        """Bare 503 (no ``code``) — may have been dispatched: OutcomeUnknown."""
        return self._push_body(503, synthetic_data.error_body("service unavailable"))

    def returns_unknown_code_503(self, code: str) -> "MockOperation":
        """503 with an unrecognized ``code`` — treated as absent: OutcomeUnknown."""
        return self._push_body(503, synthetic_data.error_body("service unavailable", code))

    def returns_server_error(self) -> "MockOperation":
        """500 internal error — OutcomeUnknown."""
        return self._push_body(500, synthetic_data.error_body("internal error", "outcome_unknown"))

    def returns_bad_gateway(self) -> "MockOperation":
        """502 (edge) — OutcomeUnknown."""
        return self._push_body(502, synthetic_data.error_body("bad gateway"))

    def returns_gateway_timeout(self) -> "MockOperation":
        """504 (edge) — OutcomeUnknown."""
        return self._push_body(504, synthetic_data.error_body("gateway timeout"))

    def throws_timeout_after_send(self) -> "MockOperation":
        """Deadline expiry after the request was sent (``ReadTimeoutError``) —
        no never-sent proof: OutcomeUnknown."""
        return self._push_raise(
            urllib3.exceptions.ReadTimeoutError(
                None,
                "/payments",
                "synthetic: read timed out",  # type: ignore[arg-type]
            )
        )

    def throws_connection_reset(self) -> "MockOperation":
        """Connection reset mid-flight (``ProtocolError``) — OutcomeUnknown."""
        return self._push_raise(
            urllib3.exceptions.ProtocolError(
                "Connection aborted.", ConnectionResetError(104, "synthetic: connection reset")
            )
        )

    def throws_ssl_after_handshake(self) -> "MockOperation":
        """A TLS failure WITHOUT certificate-verification proof — urllib3 cannot
        prove the phase, so it classifies OutcomeUnknown (python-specific
        conservatism; see the classifier)."""
        return self._push_raise(
            urllib3.exceptions.SSLError(ssl.SSLError(1, "synthetic: tls record failure"))
        )

    # ---- reconcile scripting (§3) -------------------------------------------

    def not_found_yet(self, times: int = 1) -> "MockOperation":
        """404 not-visible-yet, ``times`` in a row (then the next scripted outcome)."""
        for _ in range(times):
            self._push_body(404, synthetic_data.error_body("transaction not found"))
        return self

    def pending(self) -> "MockOperation":
        """200 pending intent (post-P-2 shape)."""
        return self._push_body(200, synthetic_data.pending())

    def then_found_approved(self) -> "MockOperation":
        """Then a 200 approved terminal record (chain after not_found_yet()/pending())."""
        return self.returns_approved()

    def then_found_declined(self) -> "MockOperation":
        """Then a 200 declined terminal record (chain after not_found_yet()/pending())."""
        return self.returns_declined()

    # ---- raw escapes --------------------------------------------------------

    def returns(
        self, status: int, body: str, headers: Optional[Dict[str, str]] = None
    ) -> "MockOperation":
        """A raw scripted response. The synthetic correlation id and JSON content
        type are always present unless overridden."""
        return self._push_body(status, body, headers or {})

    def throws_io(self, failure: BaseException) -> "MockOperation":
        """A raw scripted transport failure (raised without a response)."""
        return self._push_raise(failure)

    def _push_body(
        self, status: int, body: str, extra_headers: Optional[Dict[str, str]] = None
    ) -> "MockOperation":
        headers = {
            "Content-Type": "application/json",
            "X-Correlation-ID": synthetic_data.DEFAULT_CORRELATION_ID,
            "api-supported-versions": "2.0, 2.1",
        }
        headers.update(extra_headers or {})
        self._queue.append(("body", (status, body, headers)))
        return self

    def _push_raise(self, failure: BaseException) -> "MockOperation":
        self._queue.append(("raise", failure))
        return self


class RapMockTransport:
    """The wire double. Pass as ``RapClient(..., transport=mock)``.

    Stub operations through the accessors, then drive the client::

        mock = RapMockTransport()
        mock.charge().returns_not_processed_503()
        mock.reconcile().not_found_yet(2).then_found_approved()
        client = RapClient("sk_synthetic", transport=mock)
    """

    def __init__(self) -> None:
        self._operations: Dict[str, MockOperation] = {}
        self.recorded_requests: List[RecordedRequest] = []

    # ---- operation accessors ------------------------------------------------

    def charge(self) -> MockOperation:
        return self._operation("charge")

    def authorize(self) -> MockOperation:
        return self._operation("authorize")

    def capture(self) -> MockOperation:
        return self._operation("capture")

    def void_payment(self) -> MockOperation:
        return self._operation("void")

    def refund(self) -> MockOperation:
        return self._operation("refund")

    def refund_cancel(self) -> MockOperation:
        return self._operation("refundCancel")

    def reconcile(self) -> MockOperation:
        """The reconcile lookup (``GET /transactions/merchant/{id}``)."""
        return self._operation("reconcile")

    def get_transaction(self) -> MockOperation:
        return self._operation("getTransaction")

    def list_transactions(self) -> MockOperation:
        return self._operation("listTransactions")

    def notify(self) -> MockOperation:
        return self._operation("notify")

    # ---- the wire surface (called by RapTransport) --------------------------

    def send(self, request: RapWireRequest) -> RapWireResponse:
        from ..transport import get_header  # local import avoids a cycle at import time

        user_agent = get_header(request.headers, "User-Agent")
        if user_agent is None or not user_agent.startswith(f"{PRODUCT_NAME}/"):
            raise AssertionError(
                "mock: every request must carry the SDK User-Agent (runtime-tdd §8)"
            )

        body = request.body
        if isinstance(body, bytes):
            body = body.decode("utf-8", errors="replace")
        self.recorded_requests.append(
            RecordedRequest(
                method=request.method,
                url=request.url,
                headers=dict(request.headers),
                body=body,
            )
        )

        operation = self._route(request.method, urlsplit(request.url).path)
        if operation not in self._operations:
            raise AssertionError(f"mock: no outcome scripted for operation '{operation}'")

        kind, payload = self._operations[operation]._next()
        if kind == "raise":
            raise payload
        status, response_body, headers = payload
        return RapWireResponse(
            status=status,
            headers=headers,
            data=response_body.encode("utf-8"),
            reason="",
        )

    def _operation(self, name: str) -> MockOperation:
        if name not in self._operations:
            self._operations[name] = MockOperation()
        return self._operations[name]

    @staticmethod
    def _route(method: str, path: str) -> str:
        if path == "/payments":
            return "charge"
        if path == "/payments/authorize":
            return "authorize"
        if path.startswith("/payments/capture/"):
            return "capture"
        if path.startswith("/payments/void/"):
            return "void"
        if path.startswith("/payments/refund-cancel/merchant/"):
            return "refundCancel"
        if path.startswith("/payments/refund/"):
            return "refund"
        if path.startswith("/transactions/merchant/"):
            return "reconcile"
        if path == "/transactions":
            return "listTransactions"
        if path.startswith("/transactions/"):
            return "getTransaction"
        if path == "/notify":
            return "notify"
        return f"unmapped:{method} {path}"
