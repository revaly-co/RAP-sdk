"""revaly-sdk — the RAP V2 server-side SDK for Python.

One package, one import (runtime-tdd §2): the hand-written runtime (client,
typed failure classes, reconcile, mock transport under ``revaly_sdk.testing``)
plus the full generated core surface re-exported — request/response models here,
generated api classes via the client's ``payments`` / ``transactions`` /
``payment_methods`` / ``notify`` attributes.

Quickstart: see the package README — install → init → charge → handle all three
failure classes → reconcile.
"""

import logging as _logging

# The generated core's full model surface, re-exported (§2 one-package).
from revaly_sdk_core.models import *  # noqa: F401,F403
from revaly_sdk_core.api.notify_api import NotifyApi
from revaly_sdk_core.api.payment_methods_api import PaymentMethodsApi
from revaly_sdk_core.api.payments_api import PaymentsApi
from revaly_sdk_core.api.transactions_api import TransactionsApi
from revaly_sdk_core.api_response import ApiResponse

from ._scrub import REDACTED, SCRUBBED, scrub_headers, scrub_json, scrub_value
from ._useragent import user_agent_value
from ._version import SDK_VERSION
from ._wire_trace import RapWireTraceEvent, RapWireTraceHook
from .client import (
    DEFAULT_API_VERSION,
    DEFAULT_BASE_URL,
    DEFAULT_OVERALL_DEADLINE,
    RapClient,
)
from .errors import (
    RapError,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransientFailure,
)
from .reconcile import (
    Found,
    NotFoundYet,
    RapReconciler,
    RapReconcileVerdict,
    RapTransactionOutcome,
    ReconcilePolicy,
)
from .transport import RapTransport, RapWireRequest, RapWireResponse

# Library logging etiquette: silent unless the application configures handlers.
_logging.getLogger("revaly_sdk").addHandler(_logging.NullHandler())
