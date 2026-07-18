package runtime

import "log/slog"

// WireTraceEvent is one request/response observation delivered to the
// wire-trace hook (runtime-tdd §6, DX contract §c). Payload fields are ALWAYS
// scrubbed by the runtime's central scrubber before the hook sees them —
// scrubbing lives here, not in the hook consumer (ADR-SDK-020).
type WireTraceEvent struct {
	// Operation is the runtime operation name (e.g. "charge", "reconcile").
	Operation string
	Method    string
	// Path is the request path template or path — never the full URL.
	Path   string
	Status int
	// CorrelationID is the response's X-Correlation-ID (empty when the request
	// never produced a response).
	CorrelationID string
	// ScrubbedRequestBody / ScrubbedResponseBody carry allowlist-scrubbed JSON;
	// empty when the side had no body or it was not observed.
	ScrubbedRequestBody  string
	ScrubbedResponseBody string
}

// WireTraceHook observes scrubbed request/response events, for Enablement
// escalations. Off by default.
type WireTraceHook func(WireTraceEvent)

// emitTrace delivers an event to the hook. Observer panics are swallowed
// (runtime-tdd §6) — tracing must never change payment control flow.
func emitTrace(logger *slog.Logger, hook WireTraceHook, event WireTraceEvent) {
	if hook == nil {
		return
	}
	defer func() {
		if recovered := recover(); recovered != nil {
			logger.Debug("rap.wiretrace hook panicked; ignored")
		}
	}()
	hook(event)
}
