"""The runtime transport (runtime-tdd §5 · ADR-SDK-004/005/020).

``RapTransport`` duck-types the generated core's ``RESTClientObject`` and is
installed as ``ApiClient.rest_client``, so EVERY request the core makes flows
through here — the single place where:

- ``User-Agent`` is force-set (the core cannot bypass or replace it, ADR-SDK-005);
- ``Authorization: ApiKey <key>`` is injected — the key lives ONLY in this object,
  never on the core ``Configuration``, never in logs or messages (ADR-SDK-020);
- ``X-Api-Version`` is pinned to the configured default when the call did not set
  it (the core sends the header only when the per-call parameter is used; an
  absent header binds the server to 2.0);
- urllib3 is invoked with ``retries=False`` — mandatory: the urllib3 DEFAULT
  performs 3 hidden connect retries AND follows redirects re-sending the body
  (a 307 on POST /payments would silently resubmit the payment — probed). With
  retries disabled a 3xx comes back as a plain response and classifies
  OutcomeUnknown; no hidden retries anywhere (ADR-SDK-004);
- the response body is materialized INSIDE the request so that mid-body failures
  (reset, read timeout, TLS) classify here too — urllib3 surfaces them at
  ``read()`` time, not at request time (probed);
- every failure leaves as exactly one of the three typed classes, raised BEFORE
  any core code can flatten it (the core's rest.py collapses SSL failures into
  ``ApiException(status=0)``; this transport replaces that path entirely).

The wire itself (`RapWire`) is replaceable: the mock transport substitutes the
wire only, so header injection and classification — the safety-relevant code —
run identically in merchant tests (DX contract §d).
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Protocol, Union

import urllib3
import urllib3.exceptions

from .errors import RapError, classify_response, classify_transport_exception

_AUTHORIZATION = "Authorization"
_USER_AGENT = "User-Agent"
_API_VERSION_HEADER = "X-Api-Version"
CORRELATION_ID_HEADER = "X-Correlation-ID"


@dataclass(frozen=True)
class RapWireRequest:
    """One fully prepared outbound request handed to the wire."""

    method: str
    url: str
    headers: Mapping[str, str]
    body: Optional[Union[str, bytes]]
    timeout: urllib3.Timeout


@dataclass(frozen=True)
class RapWireResponse:
    """One fully materialized inbound response returned by the wire."""

    status: int
    headers: Mapping[str, str]
    data: bytes
    reason: str = ""


class RapWire(Protocol):
    """The replaceable wire seam, as a PEP 544 structural protocol.

    ``RapTransport`` calls exactly one method on the injected wire; anything with
    this shape satisfies the seam — the built-in urllib3 wire in production and
    :class:`revaly_sdk.testing.RapMockTransport` in merchant tests (no
    subclassing required; Protocols match structurally). Only the wire is
    replaceable: header injection and failure classification always run in
    ``RapTransport`` above it (DX contract §d).
    """

    def send(self, request: RapWireRequest) -> RapWireResponse:
        """Performs one single-shot exchange: returns the fully materialized
        response, or raises the transport failure exactly as the wire saw it
        (never a classification — classifying is ``RapTransport``'s job)."""
        ...


@dataclass(frozen=True)
class _PerCallTimeout:
    """Internal per-call timeout override from RapClient method kwargs (seconds)."""

    connect_timeout: Optional[float] = None
    overall_deadline: Optional[float] = None


@dataclass
class _ResponseMeta:
    """Values-free response metadata captured for containment and logging."""

    status: Optional[int] = None
    correlation_id: Optional[str] = None
    raw_body: Optional[str] = None


def get_header(headers: Optional[Mapping[str, Any]], name: str) -> Optional[str]:
    """Case-insensitive header lookup over plain dicts and HTTPHeaderDict alike."""
    if headers is None:
        return None
    getter = getattr(headers, "get", None)
    if getter is not None:
        direct = getter(name)
        if direct is not None:
            return str(direct)
    lowered = name.lower()
    for key, value in headers.items():
        if str(key).lower() == lowered:
            return str(value)
    return None


class _Urllib3Wire:
    """The real HTTP wire: one urllib3 pool, single-shot semantics."""

    def __init__(self) -> None:
        self._pool = urllib3.PoolManager()

    def send(self, request: RapWireRequest) -> RapWireResponse:
        response = self._pool.request(
            request.method,
            request.url,
            body=request.body,
            headers=dict(request.headers),
            timeout=request.timeout,
            retries=False,  # no hidden retries, no redirect follow (ADR-SDK-004)
            redirect=False,
            preload_content=False,
        )
        try:
            data = response.read()
        finally:
            response.release_conn()
        return RapWireResponse(
            status=response.status,
            headers=response.headers,
            data=data,
            reason=response.reason or "",
        )


class _RestResponseAdapter:
    """Duck-types the core's ``rest.RESTResponse`` for ``response_deserialize``."""

    def __init__(self, wire_response: RapWireResponse) -> None:
        self.status = wire_response.status
        self.reason = wire_response.reason
        self.data = wire_response.data
        self._headers = wire_response.headers
        # The core's *_without_preload_content methods return `.response` (the
        # underlying stream object on the real RESTResponse). The body is always
        # materialized here, so the adapter serves as its own stream surface.
        self.response = self

    def read(self) -> bytes:
        return self.data

    @property
    def headers(self) -> Mapping[str, str]:
        return self._headers

    def getheaders(self) -> Mapping[str, str]:
        return self._headers

    def getheader(self, name: str, default: Optional[str] = None) -> Optional[str]:
        found = get_header(self._headers, name)
        return default if found is None else found


class RapTransport:
    """The transport installed as the core ``ApiClient.rest_client``."""

    def __init__(
        self,
        *,
        api_key: str,
        api_version: str,
        user_agent: str,
        connect_timeout: Optional[float] = None,
        overall_deadline: Optional[float] = None,
        wire: Optional[RapWire] = None,
    ) -> None:
        self._api_key = api_key
        self._api_version = api_version
        self._user_agent = user_agent
        self._connect_timeout = connect_timeout
        self._overall_deadline = overall_deadline
        self._wire: RapWire = wire if wire is not None else _Urllib3Wire()
        self._local = threading.local()

    # -- call-scope containment surface (used by RapClient) ---------------------

    def begin_call(self, per_call_timeout: Optional[_PerCallTimeout] = None) -> None:
        """Resets the call scope for one logical client call.

        The dispatch marker distinguishes pre-send caller errors (argument
        validation — rethrown untyped) from post-dispatch deserialize failures on
        a 2xx (the §A3 closed-enum edge — contained as OutcomeUnknown by
        RapClient). The per-call timeout override travels here rather than
        through the generated ``_request_timeout`` parameter, whose
        ``@validate_call`` schema only admits the core's number/tuple shapes.
        """
        self._local.dispatched = False
        self._local.meta = _ResponseMeta()
        self._local.call_timeout = per_call_timeout

    def dispatched(self) -> bool:
        return bool(getattr(self._local, "dispatched", False))

    def last_response_meta(self) -> _ResponseMeta:
        meta = getattr(self._local, "meta", None)
        return meta if meta is not None else _ResponseMeta()

    # -- the RESTClientObject duck-type surface ---------------------------------

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]] = None,
        body: Any = None,
        post_params: Any = None,
        _request_timeout: Any = None,
    ) -> _RestResponseAdapter:
        if post_params:
            # The RAP V2 surface is JSON-only; form/multipart bodies never occur.
            raise ValueError("form-encoded requests are not supported by this transport")

        prepared_headers = dict(headers or {})
        prepared_headers[_USER_AGENT] = self._user_agent
        prepared_headers[_AUTHORIZATION] = f"ApiKey {self._api_key}"
        if get_header(prepared_headers, _API_VERSION_HEADER) is None:
            prepared_headers[_API_VERSION_HEADER] = self._api_version

        request = RapWireRequest(
            method=method.upper(),
            url=url,
            headers=prepared_headers,
            body=self._encode_body(body, prepared_headers),
            timeout=self._build_timeout(_request_timeout),
        )

        self._local.dispatched = True
        try:
            wire_response = self._wire.send(request)
        except RapError:
            raise
        except (urllib3.exceptions.HTTPError, OSError) as exc:
            raise classify_transport_exception(exc) from exc

        raw_body = wire_response.data.decode("utf-8", errors="replace")
        correlation_id = get_header(wire_response.headers, CORRELATION_ID_HEADER)
        self._local.meta = _ResponseMeta(
            status=wire_response.status,
            correlation_id=correlation_id,
            raw_body=raw_body,
        )

        failure = classify_response(
            status=wire_response.status,
            raw_body=raw_body,
            correlation_id=correlation_id,
            api_version=self._api_version,
        )
        if failure is not None:
            raise failure

        return _RestResponseAdapter(wire_response)

    # -- helpers ----------------------------------------------------------------

    def _encode_body(self, body: Any, headers: Mapping[str, str]) -> Optional[Union[str, bytes]]:
        if body is None or isinstance(body, (str, bytes)):
            return body
        content_type = get_header(headers, "Content-Type")
        if content_type is None or "json" in content_type.lower():
            return json.dumps(body)
        raise ValueError(f"unsupported request content type: {content_type}")

    def _build_timeout(self, request_timeout: Any) -> urllib3.Timeout:
        """Maps timeout inputs to a urllib3.Timeout.

        - ``None`` → the configured defaults: overall deadline as ``total``,
          connect timeout as ``connect``. The transport itself defaults both to
          None — RapClient resolves the 75 s ratified overall default before
          construction (ADR-SDK-027); connect awaits OQ-11 edge data.
        - ``_PerCallTimeout`` → RapClient per-call overrides layered over config.
        - number / (connect, read) tuple → the core convention, honored verbatim
          for callers using the generated apis directly.

        A total/read expiry AFTER send surfaces as ReadTimeoutError →
        OutcomeUnknown; a connect-phase expiry surfaces as ConnectTimeoutError
        (even under a total-only timeout — probed) → TransientFailure.
        """
        if isinstance(request_timeout, _PerCallTimeout):
            overall = (
                request_timeout.overall_deadline
                if request_timeout.overall_deadline is not None
                else self._overall_deadline
            )
            connect = (
                request_timeout.connect_timeout
                if request_timeout.connect_timeout is not None
                else self._connect_timeout
            )
            return urllib3.Timeout(total=overall, connect=connect)
        if isinstance(request_timeout, (int, float)) and not isinstance(request_timeout, bool):
            return urllib3.Timeout(total=request_timeout)
        if isinstance(request_timeout, tuple) and len(request_timeout) == 2:
            return urllib3.Timeout(connect=request_timeout[0], read=request_timeout[1])
        call_override = getattr(self._local, "call_timeout", None)
        if call_override is not None:
            return self._build_timeout(call_override)
        return urllib3.Timeout(total=self._overall_deadline, connect=self._connect_timeout)
