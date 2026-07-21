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

import revaly_sdk_core.models as _core_models

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
from .transport import RapTransport, RapWire, RapWireRequest, RapWireResponse

__version__ = SDK_VERSION
"""The installed SDK version (the conventional dunder; equals :data:`SDK_VERSION`)."""

# The explicit runtime surface (runtime-tdd §§1-6): client + constants, the three
# typed failure classes, reconcile verdicts + policy, transport seam types, hooks,
# scrub helpers, and the generated api classes re-exported above.
__all__ = [
    "ApiResponse",
    "DEFAULT_API_VERSION",
    "DEFAULT_BASE_URL",
    "DEFAULT_OVERALL_DEADLINE",
    "Found",
    "NotFoundYet",
    "NotifyApi",
    "PaymentMethodsApi",
    "PaymentsApi",
    "REDACTED",
    "RapClient",
    "RapError",
    "RapOutcomeUnknown",
    "RapPermanentRejection",
    "RapReconcileVerdict",
    "RapReconciler",
    "RapTransactionOutcome",
    "RapTransientFailure",
    "RapTransport",
    "RapWire",
    "RapWireRequest",
    "RapWireResponse",
    "RapWireTraceEvent",
    "RapWireTraceHook",
    "ReconcilePolicy",
    "SCRUBBED",
    "SDK_VERSION",
    "TransactionsApi",
    "__version__",
    "scrub_headers",
    "scrub_json",
    "scrub_value",
    "user_agent_value",
]

# Extend DYNAMICALLY with the generated core models' public names so the §2
# one-package surface tracks regeneration and never silently shrinks behind a
# static list: the core's own __all__ when it defines one, otherwise every
# non-underscore name — exactly what the star re-export above surfaces.
__all__ += [
    name
    for name in (getattr(_core_models, "__all__", None) or dir(_core_models))
    if not name.startswith("_") and name not in __all__
]

# Library logging etiquette: silent unless the application configures handlers.
_logging.getLogger("revaly_sdk").addHandler(_logging.NullHandler())
