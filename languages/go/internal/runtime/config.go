package runtime

import (
	"errors"
	"log/slog"
	"net/http"
	"strings"
	"time"
)

// DefaultBaseURL is the production API endpoint. Sandbox and live share this
// URL — the environment is selected by the API key's scope, not the URL
// (ADR-SDK-024); override only for internal/pre-release targets.
const DefaultBaseURL = "https://api.revaly.co"

// DefaultAPIVersion is the X-Api-Version pin sent when a call does not select
// one explicitly. New integrations pin "2.1" — it is where the
// ErrorResponse.code fast-failover signal is documented (failover-contract §2).
const DefaultAPIVersion = "2.1"

// DefaultOverallDeadline is applied when Config.OverallDeadline is zero:
// 75 seconds, ratified from production latency telemetry (ADR-SDK-027) — it
// clears every observed gateway tail cluster and clips ≲0.007% of charges.
// Set NoOverallDeadline to disable the client deadline entirely.
const DefaultOverallDeadline = 75 * time.Second

// NoOverallDeadline disables the client-imposed overall deadline — the
// pre-ADR-SDK-027 zero-value behaviour. Callers can still bound calls with
// their own context.
const NoOverallDeadline time.Duration = -1

// Config is the client configuration (runtime-tdd §1). One client per
// configuration; the client is safe for concurrent use and there are no global
// singletons.
type Config struct {
	// APIKey is the merchant API key — required. It is injected per request at
	// the transport layer and never persisted, logged, or placed in error
	// messages (ADR-SDK-020).
	APIKey string

	// BaseURL defaults to DefaultBaseURL.
	BaseURL string

	// APIVersion defaults to DefaultAPIVersion ("2.1"); "2.0" is selectable.
	// On "2.0" the ErrorResponse.code field is not part of the documented
	// contract, so the fast-failover class narrows to client-provable
	// never-sent failures only — a 503 with code=not_processed classifies
	// OutcomeUnknown under that pin.
	APIVersion string

	// ConnectTimeout bounds the dial phase (TCP connect). Zero leaves the
	// stdlib defaults. Setting it is what makes a connect-phase expiry
	// PROVABLY never-sent (a dial-phase *net.OpError → TransientFailure); a
	// context deadline expiring during the dial is not phase-provable and
	// classifies OutcomeUnknown. A client-side connect default cannot be
	// derived from server-side telemetry; it awaits the OQ-11 edge
	// verification (ADR-SDK-027) and is deliberately not invented here.
	ConnectTimeout time.Duration

	// OverallDeadline bounds each client operation end to end, applied as a
	// context timeout per call (callers can also bound calls with their own
	// context). Expiry AFTER send classifies OutcomeUnknown, never
	// TransientFailure. Zero applies DefaultOverallDeadline (75 s, ratified
	// from production latency telemetry — ADR-SDK-027); NoOverallDeadline
	// disables the client deadline entirely.
	OverallDeadline time.Duration

	// Logger receives values-free structured logs (runtime-tdd §6). Nil
	// discards. Default output is values-free at every level — payload values
	// never appear; debug adds only scrubbed material.
	Logger *slog.Logger

	// WireTrace, when set, observes scrubbed request/response events
	// (Enablement escalations). Scrubbing happens in the runtime before the
	// hook sees data.
	WireTrace WireTraceHook

	// Transport replaces the HTTP transport itself (the runtime-tdd §1
	// cross-language "transport" key, named for http.Client.Transport) — the
	// mock transport injection point (DX contract §d): header injection and
	// classification still run. Nil uses the real transport.
	Transport http.RoundTripper

	// HTTPClient supplies a base client whose Transport is used (ignored when
	// Config.Transport is set). The client is never mutated: its transport is
	// wrapped and its other fields are not carried over — redirect following
	// in particular is always disabled by the runtime (a 307 re-POST would
	// resubmit a payment).
	HTTPClient *http.Client
}

// withDefaults validates the configuration and fills defaults.
func (c Config) withDefaults() (Config, error) {
	if strings.TrimSpace(c.APIKey) == "" {
		return c, errors.New("revaly: Config.APIKey is required")
	}
	if c.BaseURL == "" {
		c.BaseURL = DefaultBaseURL
	}
	c.BaseURL = strings.TrimRight(c.BaseURL, "/")
	if c.APIVersion == "" {
		c.APIVersion = DefaultAPIVersion
	}
	if strings.TrimSpace(c.APIVersion) == "" {
		return c, errors.New("revaly: Config.APIVersion cannot be blank")
	}
	if c.ConnectTimeout < 0 {
		return c, errors.New("revaly: Config.ConnectTimeout cannot be negative")
	}
	switch {
	case c.OverallDeadline == 0:
		c.OverallDeadline = DefaultOverallDeadline
	case c.OverallDeadline == NoOverallDeadline:
		// Explicit opt-out: the client applies no context deadline.
	case c.OverallDeadline < 0:
		return c, errors.New(
			"revaly: Config.OverallDeadline must be positive, or NoOverallDeadline to disable")
	}
	if c.Logger == nil {
		c.Logger = slog.New(discardHandler{})
	}
	return c, nil
}
