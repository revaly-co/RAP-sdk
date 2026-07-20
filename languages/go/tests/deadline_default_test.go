// ADR-SDK-027 deadline-default semantics: a zero-value Config resolves to the
// 30 s ratified default, NoOverallDeadline opts out entirely, explicit values
// pass through, and negative values are still rejected.
package tests

import (
	"context"
	"net/http"
	"testing"
	"time"

	revaly "github.com/revaly-co/rap-sdk/languages/go"
	"github.com/revaly-co/rap-sdk/languages/go/runtime/raptest"
)

// deadlineCapture wraps the mock wire and records the context deadline each
// request carried, exactly as the network would experience it.
type deadlineCapture struct {
	inner     http.RoundTripper
	remaining []time.Duration // 0 = the request carried no deadline
}

func (w *deadlineCapture) RoundTrip(req *http.Request) (*http.Response, error) {
	if deadline, ok := req.Context().Deadline(); ok {
		w.remaining = append(w.remaining, time.Until(deadline))
	} else {
		w.remaining = append(w.remaining, 0)
	}
	return w.inner.RoundTrip(req)
}

func chargeDeadline(t *testing.T, mutate func(*revaly.Config)) time.Duration {
	t.Helper()
	mock := raptest.NewMockTransport()
	mock.Charge().ReturnsApproved()
	capture := &deadlineCapture{inner: mock}
	cfg := revaly.Config{APIKey: syntheticKey, Wire: capture}
	if mutate != nil {
		mutate(&cfg)
	}
	client, err := revaly.NewClient(cfg)
	if err != nil {
		t.Fatalf("NewClient: %v", err)
	}
	if _, err := client.Charge(context.Background(), chargeRequest("mock-mtx-deadline")); err != nil {
		t.Fatalf("Charge: %v", err)
	}
	if len(capture.remaining) != 1 {
		t.Fatalf("recorded %d requests, want 1", len(capture.remaining))
	}
	return capture.remaining[0]
}

func TestZeroValueConfigAppliesTheRatifiedDefault(t *testing.T) {
	if revaly.DefaultOverallDeadline != 30*time.Second {
		t.Fatalf("DefaultOverallDeadline = %v, want 30s", revaly.DefaultOverallDeadline)
	}
	got := chargeDeadline(t, nil)
	if got <= 29*time.Second || got > 30*time.Second {
		t.Fatalf("request context deadline %v away, want ~30s (ADR-SDK-027 default)", got)
	}
}

func TestNoOverallDeadlineDisablesTheClientDeadline(t *testing.T) {
	got := chargeDeadline(t, func(cfg *revaly.Config) { cfg.OverallDeadline = revaly.NoOverallDeadline })
	if got != 0 {
		t.Fatalf("request carried a deadline (%v away), want none", got)
	}
}

func TestExplicitDeadlinePassesThroughUnchanged(t *testing.T) {
	got := chargeDeadline(t, func(cfg *revaly.Config) { cfg.OverallDeadline = 5 * time.Second })
	if got <= 4*time.Second || got > 5*time.Second {
		t.Fatalf("request context deadline %v away, want ~5s", got)
	}
}

func TestNegativeDeadlineIsStillRejected(t *testing.T) {
	_, err := revaly.NewClient(revaly.Config{APIKey: syntheticKey, OverallDeadline: -2 * time.Second})
	if err == nil {
		t.Fatal("NewClient accepted a negative OverallDeadline")
	}
}
