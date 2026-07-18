"""The OutcomeUnknown reconciliation procedure (failover-contract §3).

GET-only, side-effect-free, caller-bounded — the only loop the runtime owns
(ADR-SDK-004). Verdicts are read from the RAW response body, never the core's
typed union wrapper (repo rule 5): reconciliation is the safety path, so it must
not depend on generated discrimination logic — server-newer-than-spec shapes
still count as sightings here. (The generated wrapper is unusable regardless: it
raises "Multiple matches found" for every valid body shape — pinned in tests
until the template fork lands.)

All time values are seconds (Python convention), as floats.
"""

from __future__ import annotations

import json
import logging
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from revaly_sdk_core.api.transactions_api import TransactionsApi
from revaly_sdk_core.models.pending_transaction_response import PendingTransactionResponse
from revaly_sdk_core.models.transaction_response import TransactionResponse

from ._scrub import scrub_json
from ._wire_trace import RapWireTraceEvent, RapWireTraceHook
from .errors import RapError, RapPermanentRejection
from .transport import CORRELATION_ID_HEADER, get_header

__all__ = [
    "RapTransactionOutcome",
    "RapReconcileVerdict",
    "Found",
    "NotFoundYet",
    "ReconcilePolicy",
    "RapReconciler",
]

_MULTIPLIER = 2.0
_JITTER_RATIO = 0.2

_RECONCILE_PATH = "/transactions/merchant/{merchantTransactionId}"


class RapTransactionOutcome(str, Enum):
    """Terminal outcome of a found transaction, mapped from the record's
    ``transactionStatus`` (1=Approved, 2=Declined, 3=Error).

    ``PENDING`` is the post-P-2 intent state; ``UNKNOWN`` covers unmapped
    statuses and record shapes this SDK version cannot read — found-but-unmapped
    is still FOUND. Values match the other language runtimes' tokens so
    cross-language log lines join cleanly.
    """

    APPROVED = "Approved"
    DECLINED = "Declined"
    ERROR = "Error"
    PENDING = "Pending"
    UNKNOWN = "Unknown"


class RapReconcileVerdict:
    """Base of the reconcile verdicts — V1 returns :class:`Found` or
    :class:`NotFoundYet` only, and the set is OPEN FOR EXTENSION by design
    (ADR-SDK-009): ``SafeToFailover`` arrives with platform P-2 as a **minor**
    release. ALWAYS branch with a trailing ``else`` when dispatching on verdict
    type — the quickstart shows it."""


@dataclass(frozen=True)
class Found(RapReconcileVerdict):
    """A record for the merchantTransactionId IS visible at RAP-core (§3).

    ``Found(APPROVED)`` means the money moved — failing over now would
    double-charge.
    """

    outcome: RapTransactionOutcome
    transaction: Optional[TransactionResponse] = None
    """The terminal record, when the sighting was a terminal transaction this
    SDK version could bind (a sighting it cannot bind still returns Found)."""
    pending: Optional[PendingTransactionResponse] = None
    """The pending intent, when the sighting was a post-P-2 pending state."""
    correlation_id: Optional[str] = None


@dataclass(frozen=True)
class NotFoundYet(RapReconcileVerdict):
    """No record is visible YET (§3): platform visibility is asynchronous and
    unbounded — absence is NOT provable in V1. Hold and re-poll; on sustained
    NotFoundYet, escalate per merchant policy."""

    attempts: int
    elapsed: float
    """Wall-clock seconds spent across all attempts and waits."""
    last_correlation_id: Optional[str] = None
    last_http_status: Optional[int] = None


@dataclass(frozen=True)
class ReconcilePolicy:
    """The caller-bounded polling policy — the ONLY loop this SDK owns
    (ADR-SDK-004). All bounds are explicit: the SDK ships no default attempt
    counts, budgets, or delays until the OQ-6 telemetry-derived recommendations
    land (docs/open-items.md — deliberately not invented here). The backoff shape
    is exponential with jitter ([Proposed]: multiplier 2.0, full jitter ±20%).

    Choose bounds per your risk policy: reconciliation is how an OutcomeUnknown
    payment is resolved, so the budget bounds how long your checkout holds before
    escalating. All values are seconds.
    """

    max_attempts: int
    """Maximum GET attempts (≥ 1)."""
    overall_budget: float
    """Total wall-clock budget across all attempts and waits, in seconds."""
    initial_delay: float
    """Delay before the second attempt, in seconds; doubles each attempt (with jitter)."""
    max_delay: Optional[float] = None
    """Optional cap on the per-wait delay; omit to leave growth uncapped within the budget."""

    def __post_init__(self) -> None:
        if not isinstance(self.max_attempts, int) or self.max_attempts < 1:
            raise ValueError("max_attempts: at least one attempt is required")
        if not self.overall_budget > 0:
            raise ValueError("overall_budget: the overall budget must be positive")
        if self.initial_delay < 0:
            raise ValueError("initial_delay: the initial delay cannot be negative")


def delay_for_attempt(policy: ReconcilePolicy, completed_attempts: int) -> float:
    """The jittered wait after the given number of completed attempts, in seconds."""
    if policy.initial_delay <= 0:
        return 0.0
    raw = policy.initial_delay * _MULTIPLIER ** (completed_attempts - 1)
    if policy.max_delay is not None and raw > policy.max_delay:
        raw = policy.max_delay
    jitter_span = raw * _JITTER_RATIO
    jittered = raw + (random.random() * 2 - 1) * jitter_span
    return max(0.0, jittered)


class RapReconciler:
    """Runs the reconcile loop until a record is visible or the policy bounds are
    spent.

    Raises a typed failure only for a rejected READ that polling can never fix
    (PermanentRejection other than 404 — bad credentials, malformed id); 404 is
    the NotFoundYet signal, and degraded reads (5xx/timeouts/transport failures)
    keep polling within the budget — exactly the window where visibility is
    widest.
    """

    def __init__(
        self,
        transactions: TransactionsApi,
        logger: logging.Logger,
        wire_trace_hook: Optional[RapWireTraceHook] = None,
    ) -> None:
        self._transactions = transactions
        self._logger = logger
        self._wire_trace_hook = wire_trace_hook

    def reconcile(self, merchant_transaction_id: str, policy: ReconcilePolicy) -> RapReconcileVerdict:
        if not merchant_transaction_id or merchant_transaction_id.strip() == "":
            raise ValueError("merchant_transaction_id is required")

        start = time.monotonic()
        attempts = 0
        last_correlation_id: Optional[str] = None
        last_http_status: Optional[int] = None

        while True:
            attempts += 1
            outcome: Optional[Found] = None
            try:
                response = self._transactions.get_transaction_by_merchant_transaction_id_without_preload_content(
                    merchant_transaction_id
                )
                last_http_status = response.status
                correlation_id = get_header(response.headers, CORRELATION_ID_HEADER)
                if correlation_id is not None:
                    last_correlation_id = correlation_id
                raw_body = response.read().decode("utf-8", errors="replace")
                self._trace(response.status, correlation_id, raw_body)
                outcome = self._read_found(raw_body, last_correlation_id, attempts)
            except RapPermanentRejection as failure:
                if failure.status == 404:
                    # Not yet visible — the NotFoundYet signal, not an error (§3).
                    last_http_status = 404
                    if failure.correlation_id is not None:
                        last_correlation_id = failure.correlation_id
                    self._trace(404, failure.correlation_id, failure.raw_body)
                    self._logger.debug("rap.reconcile not visible yet (404) attempt=%d", attempts)
                else:
                    # 400/401/403/422 escape: polling will never fix a rejected
                    # read (bad credentials, malformed id) — the caller must see it.
                    raise
            except RapError as failure:
                # Degraded read path (5xx/timeout/transport failure on the GET):
                # the WRITE's status is still unknown — keep polling within the
                # caller's budget.
                if failure.status is not None:
                    last_http_status = failure.status
                if failure.correlation_id is not None:
                    last_correlation_id = failure.correlation_id
                self._trace(failure.status, failure.correlation_id, failure.raw_body)
                self._logger.warning(
                    "rap.reconcile degraded read; continuing within policy attempt=%d status=%s class=%s",
                    attempts,
                    failure.status,
                    failure.kind,
                )
            # Anything else (argument validation, programming errors) is not a
            # wire outcome — it propagates.

            if outcome is not None:
                return outcome

            if attempts >= policy.max_attempts:
                break
            elapsed = time.monotonic() - start
            delay = delay_for_attempt(policy, attempts)
            if elapsed + delay >= policy.overall_budget:
                break
            if delay > 0:
                time.sleep(delay)

        elapsed = time.monotonic() - start
        self._logger.info(
            "rap.reconcile verdict=NotFoundYet attempts=%d elapsed=%.3f last_status=%s correlation=%s",
            attempts,
            elapsed,
            last_http_status,
            last_correlation_id,
        )
        return NotFoundYet(
            attempts=attempts,
            elapsed=elapsed,
            last_correlation_id=last_correlation_id,
            last_http_status=last_http_status,
        )

    def _read_found(
        self, raw_body: str, correlation_id: Optional[str], attempt: int
    ) -> Optional[Found]:
        """Maps a 2xx body to a Found verdict from the RAW json. Returns ``None``
        for a body this SDK cannot read at all (→ poll-continue: an ambiguous
        read is not a sighting)."""
        root: Any = None
        try:
            root = json.loads(raw_body)
        except ValueError:
            root = None
        if not isinstance(root, dict):
            self._logger.warning(
                "rap.reconcile 2xx with an unreadable body; continuing within policy attempt=%d",
                attempt,
            )
            return None

        # `state` exists only on the pending schema — its presence is
        # authoritative (the spec marks it the discriminator).
        if isinstance(root.get("state"), str):
            try:
                pending = PendingTransactionResponse.from_json(raw_body)
                self._logger.info(
                    "rap.reconcile verdict=Found outcome=Pending correlation=%s", correlation_id
                )
                return Found(
                    outcome=RapTransactionOutcome.PENDING,
                    pending=pending,
                    correlation_id=correlation_id,
                )
            except Exception:
                # A pending-shaped record this SDK version cannot bind is still
                # a sighting — surface it conservatively rather than polling on.
                return Found(outcome=RapTransactionOutcome.UNKNOWN, correlation_id=correlation_id)

        # Terminal records: the outcome maps from the RAW dict; the typed model
        # bind only enriches the verdict. A record the model cannot bind (e.g.
        # an enum value newer than this SDK, or a grouped envelope) is still
        # FOUND — found-but-unmapped licenses no failover either way.
        outcome = _map_outcome(root.get("transactionStatus"))
        transaction: Optional[TransactionResponse] = None
        try:
            transaction = TransactionResponse.from_json(raw_body)
        except Exception:
            transaction = None
        self._logger.info(
            "rap.reconcile verdict=Found outcome=%s correlation=%s", outcome.value, correlation_id
        )
        return Found(outcome=outcome, transaction=transaction, correlation_id=correlation_id)

    def _trace(
        self,
        status: Optional[int],
        correlation_id: Optional[str],
        raw_response_body: Optional[str],
    ) -> None:
        if self._wire_trace_hook is None:
            return
        try:
            self._wire_trace_hook(
                RapWireTraceEvent(
                    operation="reconcile",
                    method="GET",
                    path=_RECONCILE_PATH,
                    status=status,
                    correlation_id=correlation_id,
                    scrubbed_response_body=None
                    if raw_response_body is None
                    else scrub_json(raw_response_body),
                )
            )
        except Exception as hook_failure:
            # Observer exceptions are swallowed (runtime-tdd §6) — tracing must
            # never change payment control flow.
            self._logger.debug(
                "rap.wiretrace hook threw; ignored exception=%s", type(hook_failure).__name__
            )


def _map_outcome(transaction_status: Any) -> RapTransactionOutcome:
    if transaction_status == 1:
        return RapTransactionOutcome.APPROVED
    if transaction_status == 2:
        return RapTransactionOutcome.DECLINED
    if transaction_status == 3:
        return RapTransactionOutcome.ERROR
    return RapTransactionOutcome.UNKNOWN
