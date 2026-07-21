// The runtime transport (runtime-tdd §5 · ADR-SDK-004/005/020).
//
// A single http.RoundTripper wraps the wire and is installed on the http.Client
// handed to the generated core, so EVERY request the core makes flows through
// here — the single place where:
//
//   - User-Agent is force-set (the core cannot bypass or replace it,
//     ADR-SDK-005);
//   - `Authorization: ApiKey <key>` is injected — the key lives ONLY in this
//     object, never on the core Configuration, never in a context value, never
//     in logs or messages (ADR-SDK-020);
//   - X-Api-Version is pinned to the configured default when the call did not
//     set it (the core sends the header only when the per-call parameter is
//     used; an absent header binds the server to 2.0);
//   - redirects are never followed: the http.Client is built with
//     CheckRedirect returning ErrUseLastResponse — the stdlib default re-sends
//     a POST body on 307 (probed), which would silently resubmit a payment. A
//     3xx therefore comes back as a plain response and classifies
//     OutcomeUnknown; no hidden retries anywhere (ADR-SDK-004 — the stdlib
//     transport only ever re-dials a request whose bytes were never written,
//     which preserves single-send semantics).
//
// The transport itself is replaceable (Config.Transport): the mock transport
// substitutes the wire only, so header injection — the safety-relevant code —
// runs identically in merchant tests (DX contract §d).
package runtime

import (
	"net"
	"net/http"
	"time"
)

// CorrelationIDHeader is the response header joining every request to RAP-core
// telemetry. It is echoed on success and error alike.
const CorrelationIDHeader = "X-Correlation-ID"

const (
	authorizationHeader = "Authorization"
	userAgentHeader     = "User-Agent"
	apiVersionHeader    = "X-Api-Version"
)

// roundTripper injects the RAP headers and delegates to the transport.
type roundTripper struct {
	apiKey     string
	apiVersion string
	userAgent  string
	transport  http.RoundTripper
}

func (t *roundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	injected := req.Clone(req.Context())
	injected.Header.Set(userAgentHeader, t.userAgent)
	injected.Header.Set(authorizationHeader, "ApiKey "+t.apiKey)
	if injected.Header.Get(apiVersionHeader) == "" {
		injected.Header.Set(apiVersionHeader, t.apiVersion)
	}
	return t.transport.RoundTrip(injected)
}

// newBaseTransport builds the real HTTP transport. It starts from a clone of
// the stdlib default transport (keeping proxy/HTTP2/pool behaviour) and maps
// ConnectTimeout onto net.Dialer.Timeout — the mapping that makes a
// connect-phase expiry surface as a dial-phase *net.OpError, i.e. the provable
// never-sent signal (see ClassifyTransportError). Config resolution applies
// DefaultConnectTimeout (10 s — ADR-SDK-029) when the field is zero; with
// NoConnectTimeout the value arrives negative, no dialer bound is set, and the
// stdlib defaults apply.
func newBaseTransport(connectTimeout time.Duration) http.RoundTripper {
	base, ok := http.DefaultTransport.(*http.Transport)
	if !ok {
		return http.DefaultTransport
	}
	transport := base.Clone()
	if connectTimeout > 0 {
		dialer := &net.Dialer{Timeout: connectTimeout}
		transport.DialContext = dialer.DialContext
	}
	return transport
}
