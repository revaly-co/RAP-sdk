"""Wire-trace hook types (runtime-tdd §6 · DX contract §c).

The hook is a request/response observer for Enablement escalations. It receives
payloads ALREADY scrubbed by the runtime's central allowlist scrubber — never raw
material. Observer exceptions are swallowed by the runtime: tracing must never
change payment control flow.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class RapWireTraceEvent:
    """One observed request/response exchange, scrubbed."""

    operation: str
    method: str
    path: str
    status: Optional[int] = None
    correlation_id: Optional[str] = None
    scrubbed_request_body: Optional[str] = None
    scrubbed_response_body: Optional[str] = None


RapWireTraceHook = Callable[[RapWireTraceEvent], None]
