"""The RAP Python SDK client (runtime-tdd §§1-2).

One client object per configuration — create it once and reuse it; the object is
thread-safe and shareable (no global singletons).

Payment operations return the core's :class:`TransactionResponse` on success and
raise exactly one of the three typed failure classes on failure
(docs/failover-contract.md §2):

- :class:`RapPermanentRejection` — fix or decline; never fail over.
- :class:`RapTransientFailure` — definitively not processed; safe to fail over
  immediately.
- :class:`RapOutcomeUnknown` — may have been processed; :meth:`RapClient.reconcile`
  before acting.

The full generated V2 surface stays available through :attr:`RapClient.payments`,
:attr:`RapClient.transactions`, :attr:`RapClient.payment_methods` and
:attr:`RapClient.notify` — every request they make flows through the same
transport, headers and classification, so they raise the same three classes. One
dependency, one package to import.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Optional

from pydantic import ValidationError

from revaly_sdk_core.api.notify_api import NotifyApi
from revaly_sdk_core.api.payment_methods_api import PaymentMethodsApi
from revaly_sdk_core.api.payments_api import PaymentsApi
from revaly_sdk_core.api.transactions_api import TransactionsApi
from revaly_sdk_core.api_client import ApiClient
from revaly_sdk_core.api_response import ApiResponse
from revaly_sdk_core.configuration import Configuration
from revaly_sdk_core.exceptions import OpenApiException
from revaly_sdk_core.models.authorize_request import AuthorizeRequest
from revaly_sdk_core.models.capture_request import CaptureRequest
from revaly_sdk_core.models.payment_request import PaymentRequest
from revaly_sdk_core.models.refund_cancel_request import RefundCancelRequest
from revaly_sdk_core.models.refund_request import RefundRequest
from revaly_sdk_core.models.transaction_response import TransactionResponse
from revaly_sdk_core.models.void_request import VoidRequest

from ._scrub import scrub_json, scrub_value
from ._useragent import user_agent_value
from ._wire_trace import RapWireTraceEvent, RapWireTraceHook
from .errors import RapError, RapOutcomeUnknown
from .reconcile import RapReconciler, RapReconcileVerdict, ReconcilePolicy
from .transport import (
    CORRELATION_ID_HEADER,
    RapTransport,
    _PerCallTimeout,
    get_header,
)

DEFAULT_BASE_URL = "https://api.revaly.co"
DEFAULT_API_VERSION = "2.1"

#: The overall-deadline default (seconds) applied when the argument is omitted:
#: 30 seconds, ratified from production latency telemetry (ADR-SDK-027). Pass an
#: explicit ``overall_deadline=None`` to disable the SDK deadline entirely.
DEFAULT_OVERALL_DEADLINE = 30.0

_LOGGER_NAME = "revaly_sdk"


class RapClient:
    """The RAP client. See the module docstring and the README quickstart.

    :param api_key: The merchant API key (required). Sent as
        ``Authorization: ApiKey <key>`` on every request; never persisted, never
        logged, never present in error messages (ADR-SDK-020). The key also
        selects the environment: sandbox and live are key-scoped, not URL-scoped
        (ADR-SDK-024).
    :param base_url: The API base URL. Defaults to ``https://api.revaly.co`` —
        sandbox and live share this URL; the environment is selected by your API
        key's scope, not the URL. Override only for internal/pre-release targets.
    :param api_version: The API contract version, pinned via ``X-Api-Version`` on
        every request. Default ``"2.1"``; ``"2.0"`` is selectable. Behavioural
        difference on ``"2.0"``: the ``ErrorResponse.code`` field is not part of
        the 2.0 documented contract, so the fast-failover class narrows to
        client-provable never-sent failures only — a 503 with
        ``code: not_processed`` classifies as OutcomeUnknown (reconcile) instead
        of TransientFailure (immediate failover). Pin 2.1 unless you have a
        frozen 2.0 integration.
    :param connect_timeout: Connect-phase timeout in seconds. A connect-phase
        expiry is provably never-sent and classifies TransientFailure. Default:
        none set by this SDK (the OS default applies) — a client-side connect
        default cannot be derived from server-side telemetry; it awaits the
        OQ-11 edge verification (ADR-SDK-027) and this SDK deliberately does not
        invent one.
    :param overall_deadline: Overall per-request deadline in seconds. Expiry
        after the request was sent classifies as OutcomeUnknown (reconcile before
        acting) — never TransientFailure. Default:
        :data:`DEFAULT_OVERALL_DEADLINE` (30 seconds, ratified from production
        latency telemetry — ADR-SDK-027; it clips ~1 in 9,500 charges at the
        platform's observed tail). Pass an explicit ``None`` to disable the SDK
        deadline entirely.
    :param logger: A standard :mod:`logging` logger. Default output is
        VALUES-FREE: operation, status, class, and correlation id only; DEBUG
        level carries allowlist-scrubbed payloads (ADR-SDK-020). Defaults to
        ``logging.getLogger("revaly_sdk")``, which is silent unless your
        application configures handlers.
    :param wire_trace_hook: Optional request/response observer for Enablement
        escalations. Receives payloads already scrubbed by the runtime's central
        allowlist scrubber — never raw material. Observer exceptions are
        swallowed.
    :param transport: Replacement wire (the mock transport,
        :class:`revaly_sdk.testing.RapMockTransport`, in merchant tests). Only
        the wire is replaced — header injection and failure classification run
        identically, so tests exercise the production code path. Omit for real
        HTTP.
    :param user_agent_suffix: Optional merchant product token APPENDED after the
        SDK's User-Agent token (ADR-SDK-005: the SDK prefix stays first and
        intact; it can never be replaced or suppressed).

    Cancellation idiom: Python has no ambient cancellation token — bound calls
    with ``connect_timeout`` / ``overall_deadline`` (per client or per call) and
    bound reconciliation with the :class:`ReconcilePolicy` budget. A deadline
    expiring after send is an OutcomeUnknown payment outcome, not a cancellation.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = DEFAULT_API_VERSION,
        connect_timeout: Optional[float] = None,
        overall_deadline: Optional[float] = DEFAULT_OVERALL_DEADLINE,
        logger: Optional[logging.Logger] = None,
        wire_trace_hook: Optional[RapWireTraceHook] = None,
        transport: Optional[Any] = None,
        user_agent_suffix: Optional[str] = None,
    ) -> None:
        if not isinstance(api_key, str) or api_key.strip() == "":
            raise ValueError("api_key is required")
        base_url = (base_url or "").rstrip("/")
        if base_url == "":
            raise ValueError("base_url is required")
        if not isinstance(api_version, str) or api_version.strip() == "":
            raise ValueError("api_version is required")
        if overall_deadline is not None and not overall_deadline > 0:
            raise ValueError("overall_deadline must be positive when set")
        if connect_timeout is not None and not connect_timeout > 0:
            raise ValueError("connect_timeout must be positive when set")

        self._logger = logger if logger is not None else logging.getLogger(_LOGGER_NAME)
        self._wire_trace_hook = wire_trace_hook

        # The core Configuration deliberately never receives the API key — the
        # transport is the single injection point (ADR-SDK-020), where the core
        # cannot bypass it (ADR-SDK-005), and it classifies every failure before
        # any core code sees it.
        self._transport = RapTransport(
            api_key=api_key,
            api_version=api_version,
            user_agent=user_agent_value(user_agent_suffix),
            connect_timeout=connect_timeout,
            overall_deadline=overall_deadline,
            wire=transport,
        )
        core_config = Configuration(host=base_url)
        api_client = ApiClient(core_config)
        api_client.rest_client = self._transport

        self.payments = PaymentsApi(api_client)
        """The generated payments api, sharing this client's transport and headers."""
        self.transactions = TransactionsApi(api_client)
        """The generated transactions api, sharing this client's transport and headers."""
        self.payment_methods = PaymentMethodsApi(api_client)
        """The generated payment-methods api, sharing this client's transport and headers."""
        self.notify = NotifyApi(api_client)
        """The generated notify api, sharing this client's transport and headers."""

        self._reconciler = RapReconciler(self.transactions, self._logger, wire_trace_hook)

    # -- payment operations -----------------------------------------------------

    def charge(
        self,
        request: PaymentRequest,
        *,
        connect_timeout: Optional[float] = None,
        overall_deadline: Optional[float] = None,
    ) -> TransactionResponse:
        """Charges a payment (``POST /payments``)."""
        return self._execute(
            "charge",
            "POST",
            "/payments",
            request,
            connect_timeout,
            overall_deadline,
            lambda: self.payments.charge_payment_with_http_info(request),
        )

    def authorize(
        self,
        request: AuthorizeRequest,
        *,
        connect_timeout: Optional[float] = None,
        overall_deadline: Optional[float] = None,
    ) -> TransactionResponse:
        """Authorizes a payment for later capture (``POST /payments/authorize``)."""
        return self._execute(
            "authorize",
            "POST",
            "/payments/authorize",
            request,
            connect_timeout,
            overall_deadline,
            lambda: self.payments.authorize_payment_with_http_info(request),
        )

    def capture(
        self,
        transaction_id: str,
        request: CaptureRequest,
        *,
        connect_timeout: Optional[float] = None,
        overall_deadline: Optional[float] = None,
    ) -> TransactionResponse:
        """Captures a previously authorized payment."""
        return self._execute(
            "capture",
            "POST",
            "/payments/capture/{transactionId}",
            request,
            connect_timeout,
            overall_deadline,
            lambda: self.payments.capture_payment_with_http_info(transaction_id, request),
        )

    def void_payment(
        self,
        transaction_id: str,
        request: VoidRequest,
        *,
        connect_timeout: Optional[float] = None,
        overall_deadline: Optional[float] = None,
    ) -> TransactionResponse:
        """Voids a previously authorized payment."""
        return self._execute(
            "void",
            "POST",
            "/payments/void/{transactionId}",
            request,
            connect_timeout,
            overall_deadline,
            lambda: self.payments.void_payment_with_http_info(transaction_id, request),
        )

    def refund(
        self,
        transaction_id: str,
        request: RefundRequest,
        *,
        connect_timeout: Optional[float] = None,
        overall_deadline: Optional[float] = None,
    ) -> TransactionResponse:
        """Refunds a settled payment."""
        return self._execute(
            "refund",
            "POST",
            "/payments/refund/{transactionId}",
            request,
            connect_timeout,
            overall_deadline,
            lambda: self.payments.refund_payment_with_http_info(transaction_id, request),
        )

    def refund_cancel(
        self,
        merchant_transaction_id: str,
        request: RefundCancelRequest,
        *,
        connect_timeout: Optional[float] = None,
        overall_deadline: Optional[float] = None,
    ) -> TransactionResponse:
        """Cancels a refund by merchant transaction id."""
        return self._execute(
            "refundCancel",
            "POST",
            "/payments/refund-cancel/merchant/{merchantTransactionId}",
            request,
            connect_timeout,
            overall_deadline,
            lambda: self.payments.refund_cancel_payment_by_merchant_transaction_id_with_http_info(
                merchant_transaction_id, request
            ),
        )

    def reconcile(
        self, merchant_transaction_id: str, policy: ReconcilePolicy
    ) -> RapReconcileVerdict:
        """The OutcomeUnknown reconciliation procedure (failover-contract §3):
        polls the merchant-transaction lookup within the caller-bounded
        :class:`ReconcilePolicy` and returns a :class:`RapReconcileVerdict`.
        ALWAYS branch with a trailing ``else`` — verdicts are open for extension
        (``SafeToFailover`` arrives with platform P-2 as a minor release)."""
        self._transport.begin_call()
        return self._reconciler.reconcile(merchant_transaction_id, policy)

    # -- internals --------------------------------------------------------------

    def _execute(
        self,
        operation: str,
        method: str,
        path: str,
        request_model: Any,
        connect_timeout: Optional[float],
        overall_deadline: Optional[float],
        call: Callable[[], "ApiResponse[TransactionResponse]"],
    ) -> TransactionResponse:
        per_call = None
        if connect_timeout is not None or overall_deadline is not None:
            per_call = _PerCallTimeout(
                connect_timeout=connect_timeout, overall_deadline=overall_deadline
            )
        self._transport.begin_call(per_call)

        try:
            api_response = call()
        except RapError as failure:
            self._logger.warning(
                "rap.request failed operation=%s class=%s status=%s code=%s correlation=%s",
                operation,
                failure.kind,
                failure.status,
                failure.code,
                failure.correlation_id,
            )
            self._trace(
                operation, method, path, failure.status, failure.correlation_id,
                request_model, failure.raw_body,
            )
            raise
        except (ValidationError, OpenApiException) as failure:
            if not self._transport.dispatched():
                # Pre-send caller error (argument validation, malformed model) —
                # not a payment outcome; it propagates untyped.
                raise
            # The wire exchange returned 2xx but the body cannot be read as the
            # expected model (e.g. an enum value newer than this SDK — §A3).
            # The payment may well have SUCCEEDED: this is OutcomeUnknown, and
            # reconcile resolves it from the raw record.
            meta = self._transport.last_response_meta()
            self._logger.warning(
                "rap.request failed operation=%s class=OutcomeUnknown status=%s correlation=%s "
                "reason=unreadable-2xx",
                operation,
                meta.status,
                meta.correlation_id,
            )
            self._trace(
                operation, method, path, meta.status, meta.correlation_id,
                request_model, meta.raw_body,
            )
            raise RapOutcomeUnknown(
                "OutcomeUnknown: the 2xx response body could not be read as the expected "
                "model — the payment may have been processed; reconcile before acting",
                status=meta.status,
                correlation_id=meta.correlation_id,
                raw_body=meta.raw_body,
            ) from failure

        status = api_response.status_code
        correlation_id = get_header(api_response.headers, CORRELATION_ID_HEADER)
        self._logger.info(
            "rap.request operation=%s status=%s correlation=%s", operation, status, correlation_id
        )
        raw_body = (
            api_response.raw_data.decode("utf-8", errors="replace")
            if api_response.raw_data is not None
            else None
        )
        self._trace(operation, method, path, status, correlation_id, request_model, raw_body)
        return api_response.data

    def _trace(
        self,
        operation: str,
        method: str,
        path: str,
        status: Optional[int],
        correlation_id: Optional[str],
        request_model: Any,
        raw_response_body: Optional[str],
    ) -> None:
        emit_debug = self._logger.isEnabledFor(logging.DEBUG)
        if not emit_debug and self._wire_trace_hook is None:
            return

        scrubbed_request = None if request_model is None else scrub_value(request_model)
        scrubbed_response = None if raw_response_body is None else scrub_json(raw_response_body)

        if emit_debug:
            # Debug level carries allowlist-scrubbed payloads only (ADR-SDK-020).
            self._logger.debug(
                "rap.request payload operation=%s request=%s response=%s",
                operation,
                scrubbed_request,
                scrubbed_response,
            )

        if self._wire_trace_hook is not None:
            try:
                self._wire_trace_hook(
                    RapWireTraceEvent(
                        operation=operation,
                        method=method,
                        path=path,
                        status=status,
                        correlation_id=correlation_id,
                        scrubbed_request_body=scrubbed_request,
                        scrubbed_response_body=scrubbed_response,
                    )
                )
            except Exception as hook_failure:
                # Observer exceptions are swallowed (runtime-tdd §6).
                self._logger.debug(
                    "rap.wiretrace hook threw; ignored exception=%s",
                    type(hook_failure).__name__,
                )
