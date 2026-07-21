// Package raptest is the first-class mock transport (runtime-tdd §8, DX
// contract §d): a no-network test double for merchant failover-handler tests.
//
// MockTransport replaces ONLY the transport (Config.Transport) — the runtime's
// header injection and classification still run, so a merchant test exercises
// the same safety-relevant code paths as production. It simulates every row of the
// failover-contract §2 table (PermanentRejection statuses, TransientFailure
// including 503+not_processed, the OutcomeUnknown family) and both reconcile
// outcomes, supports scripting consecutive outcomes, records every request,
// and asserts the User-Agent contract. Synthetic data only (ADR-SDK-020).
package raptest

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"strings"
	"sync"
)

// RecordedRequest is one request the mock observed, after the runtime's header
// injection.
type RecordedRequest struct {
	Operation string
	Method    string
	Path      string
	Header    http.Header
	Body      []byte
}

type outcome struct {
	status int
	body   string
	err    error
}

// MockTransport is an http.RoundTripper scripted per operation. Zero value is
// not usable — construct with NewMockTransport. Safe for concurrent use.
type MockTransport struct {
	mu          sync.Mutex
	scripts     map[string][]outcome
	recorded    []RecordedRequest
	correlation int
}

// NewMockTransport builds an empty mock. Unscripted operations return a
// synthetic 501 with a marker body, so a test that hits an unexpected
// operation fails loudly rather than silently.
func NewMockTransport() *MockTransport {
	return &MockTransport{scripts: map[string][]outcome{}}
}

// MockOperation scripts outcomes for one operation. Each Returns*/Fails*
// call APPENDS one outcome; consecutive calls script consecutive responses
// (the last scripted outcome repeats once the script is exhausted), so
// suppression/escalation logic is testable.
type MockOperation struct {
	transport *MockTransport
	key       string
}

// Charge scripts POST /payments.
func (m *MockTransport) Charge() *MockOperation { return &MockOperation{m, "charge"} }

// Authorize scripts POST /payments/authorize.
func (m *MockTransport) Authorize() *MockOperation { return &MockOperation{m, "authorize"} }

// Capture scripts POST /payments/{transactionId}/capture.
func (m *MockTransport) Capture() *MockOperation { return &MockOperation{m, "capture"} }

// Void scripts POST /payments/{transactionId}/void.
func (m *MockTransport) Void() *MockOperation { return &MockOperation{m, "void"} }

// Refund scripts POST /payments/{transactionId}/refund.
func (m *MockTransport) Refund() *MockOperation { return &MockOperation{m, "refund"} }

// RefundCancel scripts POST /payments/merchant/{id}/refund-cancel.
func (m *MockTransport) RefundCancel() *MockOperation { return &MockOperation{m, "refund_cancel"} }

// Reconcile scripts GET /transactions/merchant/{merchantTransactionID}.
func (m *MockTransport) Reconcile(merchantTransactionID string) *MockOperation {
	return &MockOperation{m, "reconcile:" + merchantTransactionID}
}

// --- §2 table rows -----------------------------------------------------------

// ReturnsApproved scripts a 200 with a synthetic approved terminal
// transaction.
func (o *MockOperation) ReturnsApproved() *MockOperation {
	return o.append(outcome{status: 200, body: SyntheticTransaction(1)})
}

// ReturnsDeclined scripts a 200 with a synthetic declined terminal
// transaction.
func (o *MockOperation) ReturnsDeclined() *MockOperation {
	return o.append(outcome{status: 200, body: SyntheticTransaction(2)})
}

// ReturnsPermanentRejection scripts one of the §2 PermanentRejection statuses
// (400/401/403/404/422) with a synthetic ErrorResponse body.
func (o *MockOperation) ReturnsPermanentRejection(status int) *MockOperation {
	return o.append(outcome{status: status, body: SyntheticError("synthetic rejection", "")})
}

// ReturnsNotProcessed503 scripts the fast-failover row: 503 with
// code=not_processed (provable non-dispatch → TransientFailure).
func (o *MockOperation) ReturnsNotProcessed503() *MockOperation {
	return o.append(outcome{status: 503, body: SyntheticError("service unavailable", "not_processed")})
}

// ReturnsBare503 scripts a 503 WITHOUT the not_processed code → OutcomeUnknown.
func (o *MockOperation) ReturnsBare503() *MockOperation {
	return o.append(outcome{status: 503, body: SyntheticError("service unavailable", "outcome_unknown")})
}

// Returns500 scripts a 500 → OutcomeUnknown.
func (o *MockOperation) Returns500() *MockOperation {
	return o.append(outcome{status: 500, body: SyntheticError("internal error", "outcome_unknown")})
}

// Returns502 scripts an edge 502 → OutcomeUnknown.
func (o *MockOperation) Returns502() *MockOperation {
	return o.append(outcome{status: 502, body: ""})
}

// Returns504 scripts an edge 504 → OutcomeUnknown.
func (o *MockOperation) Returns504() *MockOperation {
	return o.append(outcome{status: 504, body: ""})
}

// FailsBeforeSend scripts a dial-phase failure (a real *net.OpError with
// Op="dial", the provable never-sent signal) → TransientFailure.
func (o *MockOperation) FailsBeforeSend() *MockOperation {
	return o.append(outcome{err: &net.OpError{Op: "dial", Net: "tcp", Err: errors.New("connection refused (synthetic)")}})
}

// TimesOutAfterSend scripts a deadline expiry after the request was written
// (a timeout without dial-phase proof) → OutcomeUnknown.
func (o *MockOperation) TimesOutAfterSend() *MockOperation {
	return o.append(outcome{err: fmt.Errorf("awaiting response headers (synthetic): %w", os.ErrDeadlineExceeded)})
}

// ResetsMidFlight scripts a connection reset after send (a real *net.OpError
// with Op="read") → OutcomeUnknown.
func (o *MockOperation) ResetsMidFlight() *MockOperation {
	return o.append(outcome{err: &net.OpError{Op: "read", Net: "tcp", Err: errors.New("connection reset by peer (synthetic)")}})
}

// --- reconcile outcomes ------------------------------------------------------

// ReturnsFoundApproved scripts a 200 terminal approved record.
func (o *MockOperation) ReturnsFoundApproved() *MockOperation { return o.ReturnsApproved() }

// ReturnsFoundDeclined scripts a 200 terminal declined record.
func (o *MockOperation) ReturnsFoundDeclined() *MockOperation { return o.ReturnsDeclined() }

// ReturnsPending scripts a 200 post-P-2 pending intent record.
func (o *MockOperation) ReturnsPending() *MockOperation {
	return o.append(outcome{status: 200, body: SyntheticPending()})
}

// ReturnsNotFound scripts the 404 NotFoundYet signal.
func (o *MockOperation) ReturnsNotFound() *MockOperation {
	return o.append(outcome{status: 404, body: SyntheticError("transaction not found", "")})
}

// ReturnsStatus scripts an arbitrary status with a raw body — the escape
// hatch for shapes the named rows do not cover (keep bodies synthetic).
func (o *MockOperation) ReturnsStatus(status int, body string) *MockOperation {
	return o.append(outcome{status: status, body: body})
}

// FailsWith scripts an arbitrary wire error instance.
func (o *MockOperation) FailsWith(err error) *MockOperation {
	return o.append(outcome{err: err})
}

func (o *MockOperation) append(out outcome) *MockOperation {
	o.transport.mu.Lock()
	defer o.transport.mu.Unlock()
	o.transport.scripts[o.key] = append(o.transport.scripts[o.key], out)
	return o
}

// --- RoundTripper ------------------------------------------------------------

// RoundTrip matches the request to an operation, records it, and plays the
// next scripted outcome.
func (m *MockTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	op := operationFor(req)

	var body []byte
	if req.Body != nil {
		body, _ = io.ReadAll(req.Body)
		req.Body.Close()
	}

	m.mu.Lock()
	m.recorded = append(m.recorded, RecordedRequest{
		Operation: op,
		Method:    req.Method,
		Path:      req.URL.Path,
		Header:    req.Header.Clone(),
		Body:      body,
	})
	script := m.scripts[op]
	var next outcome
	switch {
	case len(script) > 1:
		next, m.scripts[op] = script[0], script[1:]
	case len(script) == 1:
		next = script[0] // the last scripted outcome repeats
	default:
		next = outcome{status: 501, body: SyntheticError("raptest: no script for operation "+op, "")}
	}
	m.correlation++
	correlationID := fmt.Sprintf("mock-corr-%04d", m.correlation)
	m.mu.Unlock()

	if next.err != nil {
		return nil, next.err
	}

	header := http.Header{}
	header.Set("Content-Type", "application/json")
	header.Set("X-Correlation-ID", correlationID)
	return &http.Response{
		StatusCode: next.status,
		Status:     fmt.Sprintf("%d %s", next.status, http.StatusText(next.status)),
		Header:     header,
		Body:       io.NopCloser(bytes.NewReader([]byte(next.body))),
		Request:    req,
		ProtoMajor: 1,
		ProtoMinor: 1,
	}, nil
}

// Requests returns a copy of every recorded request, in order.
func (m *MockTransport) Requests() []RecordedRequest {
	m.mu.Lock()
	defer m.mu.Unlock()
	out := make([]RecordedRequest, len(m.recorded))
	copy(out, m.recorded)
	return out
}

// RequireUserAgent verifies every recorded request carried the ADR-SDK-005
// User-Agent product token (the mock's §8 obligation).
func (m *MockTransport) RequireUserAgent() error {
	for _, r := range m.Requests() {
		ua := r.Header.Get("User-Agent")
		if !strings.HasPrefix(ua, "revaly-sdk-go/") {
			return fmt.Errorf("raptest: request %s %s missing the revaly-sdk-go User-Agent (got %q)", r.Method, r.Path, ua)
		}
	}
	return nil
}

// operationFor maps a request to the scripting key.
func operationFor(req *http.Request) string {
	path := req.URL.Path
	switch {
	case req.Method == http.MethodPost && path == "/payments":
		return "charge"
	case req.Method == http.MethodPost && path == "/payments/authorize":
		return "authorize"
	case req.Method == http.MethodPost && strings.HasSuffix(path, "/capture"):
		return "capture"
	case req.Method == http.MethodPost && strings.HasSuffix(path, "/void"):
		return "void"
	case req.Method == http.MethodPost && strings.HasSuffix(path, "/refund-cancel"):
		return "refund_cancel"
	case req.Method == http.MethodPost && strings.HasSuffix(path, "/refund"):
		return "refund"
	case req.Method == http.MethodGet && strings.HasPrefix(path, "/transactions/merchant/"):
		return "reconcile:" + strings.TrimPrefix(path, "/transactions/merchant/")
	default:
		return req.Method + " " + path
	}
}
