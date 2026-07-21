// ADR-SDK-029 connect-timeout-default semantics: a zero-value Config resolves
// to the 10 s edge-ratified default, NoConnectTimeout opts out entirely, and
// negative values are still rejected. The dial-phase mapping itself (dialer
// bound → dial-phase *net.OpError → TransientFailure) is proven against a real
// wire in realwire_test.go.
package tests

import (
	"testing"
	"time"

	revaly "github.com/revaly-co/rap-sdk/languages/go"
)

func TestConnectDefaultConstantIsTheRatifiedValue(t *testing.T) {
	if revaly.DefaultConnectTimeout != 10*time.Second {
		t.Fatalf("DefaultConnectTimeout = %v, want 10s (ADR-SDK-029)", revaly.DefaultConnectTimeout)
	}
}

func TestNoConnectTimeoutIsAcceptedAsOptOut(t *testing.T) {
	cfg := revaly.Config{APIKey: syntheticKey, ConnectTimeout: revaly.NoConnectTimeout}
	if _, err := revaly.NewClient(cfg); err != nil {
		t.Fatalf("NewClient rejected NoConnectTimeout: %v", err)
	}
}

func TestNegativeConnectTimeoutIsStillRejected(t *testing.T) {
	cfg := revaly.Config{APIKey: syntheticKey, ConnectTimeout: -2 * time.Second}
	if _, err := revaly.NewClient(cfg); err == nil {
		t.Fatal("NewClient accepted a negative ConnectTimeout")
	}
}
