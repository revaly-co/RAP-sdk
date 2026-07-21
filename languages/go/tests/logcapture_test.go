// ADR-SDK-020 log-capture suite (DX contract §c acceptance): run a charge, a
// failure, and a reconcile against the mock transport with logging at debug
// level and a wire-trace hook attached, then assert no PAN/CVV/key material
// anywhere — logs, trace events, or error messages — and correlation ids on
// every error path. Plus direct units for the central scrubber.
package tests

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"net/http"
	"strings"
	"sync"
	"testing"

	revaly "github.com/revaly-co/rap-sdk/languages/go"
	core "github.com/revaly-co/rap-sdk/languages/go/core"
	"github.com/revaly-co/rap-sdk/languages/go/internal/runtime"
)

const (
	syntheticPAN = "4111111111111111"
	syntheticCVV = "9876"
)

// capturingHandler renders every record (message + attrs) into a string list.
type capturingHandler struct {
	mu    sync.Mutex
	lines *[]string
	attrs []slog.Attr
}

func (h *capturingHandler) Enabled(context.Context, slog.Level) bool { return true }

func (h *capturingHandler) Handle(_ context.Context, record slog.Record) error {
	var b strings.Builder
	b.WriteString(record.Message)
	for _, attr := range h.attrs {
		fmt.Fprintf(&b, " %s=%v", attr.Key, attr.Value)
	}
	record.Attrs(func(attr slog.Attr) bool {
		fmt.Fprintf(&b, " %s=%v", attr.Key, attr.Value)
		return true
	})
	h.mu.Lock()
	*h.lines = append(*h.lines, b.String())
	h.mu.Unlock()
	return nil
}

func (h *capturingHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	return &capturingHandler{lines: h.lines, attrs: append(append([]slog.Attr{}, h.attrs...), attrs...)}
}

func (h *capturingHandler) WithGroup(string) slog.Handler { return h }

func cardChargeRequest() *core.PaymentRequest {
	card := core.NewCreditCard(syntheticPAN, "12", "2030")
	card.SetCardVerificationCode(syntheticCVV)
	method := core.NewPaymentMethod()
	method.SetCreditCard(*card)
	request := core.NewPaymentRequest(1099, "mock-mtx-log-1")
	request.SetPaymentMethod(*method)
	return request
}

func TestValuesFreeLoggingAndScrubbedTraces(t *testing.T) {
	var lines []string
	var events []revaly.WireTraceEvent
	var eventsMu sync.Mutex

	client, mock := newMockClient(t, func(cfg *revaly.Config) {
		cfg.Logger = slog.New(&capturingHandler{lines: &lines})
		cfg.WireTrace = func(event revaly.WireTraceEvent) {
			eventsMu.Lock()
			events = append(events, event)
			eventsMu.Unlock()
		}
	})

	// charge (success) + charge (failure) + reconcile — the §c acceptance flow.
	mock.Charge().ReturnsApproved().ReturnsNotProcessed503()
	mock.Reconcile("mock-mtx-log-1").ReturnsNotFound().ReturnsFoundApproved()

	if _, err := client.Charge(context.Background(), cardChargeRequest()); err != nil {
		t.Fatalf("charge 1: %v", err)
	}
	_, chargeErr := client.Charge(context.Background(), cardChargeRequest())
	var transient *revaly.TransientFailure
	if !errors.As(chargeErr, &transient) {
		t.Fatalf("charge 2: got %v, want *TransientFailure", chargeErr)
	}
	if _, err := client.Reconcile(context.Background(), "mock-mtx-log-1", policy(3)); err != nil {
		t.Fatalf("reconcile: %v", err)
	}

	joinedLogs := strings.Join(lines, "\n")
	var traceBodies strings.Builder
	eventsMu.Lock()
	for _, event := range events {
		traceBodies.WriteString(event.ScrubbedRequestBody)
		traceBodies.WriteString(event.ScrubbedResponseBody)
	}
	eventsMu.Unlock()

	for name, corpus := range map[string]string{
		"logs":          joinedLogs,
		"trace bodies":  traceBodies.String(),
		"error message": chargeErr.Error(),
	} {
		for _, secret := range []string{syntheticPAN, syntheticCVV, syntheticKey} {
			if strings.Contains(corpus, secret) {
				t.Fatalf("%s contain sensitive material %q:\n%s", name, secret, corpus)
			}
		}
	}

	if len(lines) == 0 {
		t.Fatal("expected values-free log lines")
	}
	if !strings.Contains(joinedLogs, "correlation=mock-corr-") {
		t.Fatalf("error-path logs missing the correlation id:\n%s", joinedLogs)
	}
	if transient.CorrelationID == "" {
		t.Fatal("typed error missing the correlation id")
	}

	// The trace hook saw scrubbed material: allowlisted identifiers pass,
	// payload values do not.
	eventsMu.Lock()
	defer eventsMu.Unlock()
	if len(events) == 0 {
		t.Fatal("expected wire-trace events")
	}
	sawChargeRequest := false
	for _, event := range events {
		if event.Operation == "charge" && strings.Contains(event.ScrubbedRequestBody, "mock-mtx-log-1") {
			sawChargeRequest = true
		}
	}
	if !sawChargeRequest {
		t.Fatal("trace events missing the allowlisted merchantTransactionId")
	}
}

// A panicking trace hook must never affect payment control flow.
func TestWireTraceHookPanicsAreSwallowed(t *testing.T) {
	client, mock := newMockClient(t, func(cfg *revaly.Config) {
		cfg.WireTrace = func(revaly.WireTraceEvent) { panic("observer bug") }
	})
	mock.Charge().ReturnsApproved()
	if _, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001")); err != nil {
		t.Fatalf("charge with a panicking hook: %v", err)
	}
}

func TestScrubberAllowlist(t *testing.T) {
	scrubbed := runtime.ScrubJSON(`{"merchantTransactionId":"mtx-1","number":"` + syntheticPAN + `",` +
		`"cardVerificationCode":"` + syntheticCVV + `","transactionStatus":1,` +
		`"nested":{"code":"not_processed","customerName":"Jane Cardholder"}}`)
	for _, keep := range []string{`"merchantTransactionId":"mtx-1"`, `"transactionStatus":1`, `"code":"not_processed"`} {
		if !strings.Contains(scrubbed, keep) {
			t.Fatalf("allowlisted field lost: %s missing from %s", keep, scrubbed)
		}
	}
	for _, gone := range []string{syntheticPAN, syntheticCVV, "Jane Cardholder"} {
		if strings.Contains(scrubbed, gone) {
			t.Fatalf("sensitive value survived the scrub: %s in %s", gone, scrubbed)
		}
	}
	if !strings.Contains(scrubbed, runtime.Scrubbed) {
		t.Fatalf("expected scrub tokens in %s", scrubbed)
	}
}

func TestScrubberNonJSONNeverEchoes(t *testing.T) {
	if got := runtime.ScrubJSON("PAN " + syntheticPAN + " raw text"); strings.Contains(got, syntheticPAN) {
		t.Fatalf("raw text echoed: %s", got)
	}
}

func TestScrubberHeadersRedactAuthorization(t *testing.T) {
	headers := http.Header{}
	headers.Set("Authorization", "ApiKey "+syntheticKey)
	headers.Set("Content-Type", "application/json")
	headers.Set("X-Correlation-ID", "corr-1")
	headers.Set("X-Custom", "value")
	scrubbed := runtime.ScrubHeaders(headers)
	if scrubbed["Authorization"] != runtime.Redacted {
		t.Fatalf("Authorization = %q, want redacted", scrubbed["Authorization"])
	}
	if strings.Contains(fmt.Sprint(scrubbed), syntheticKey) {
		t.Fatal("API key survived header scrubbing")
	}
	// http.Header canonicalizes stored keys (X-Correlation-ID → X-Correlation-Id).
	if scrubbed["Content-Type"] != "application/json" || scrubbed[http.CanonicalHeaderKey("X-Correlation-ID")] != "corr-1" {
		t.Fatalf("allowlisted headers mangled: %v", scrubbed)
	}
	if scrubbed["X-Custom"] != runtime.Redacted {
		t.Fatalf("unknown header not redacted: %v", scrubbed)
	}
}
