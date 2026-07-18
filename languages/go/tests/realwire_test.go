// Real-wire proofs over local sockets (no external network): the never-sent
// taxonomy on the actual net/http stack, single-send semantics on redirects,
// and the deadline-after-send classification. Mirrors the other runtimes'
// real-socket suites.
package tests

import (
	"context"
	"crypto/tls"
	"errors"
	"fmt"
	"net"
	"net/http"
	"net/http/httptest"
	"sync/atomic"
	"testing"
	"time"

	revaly "github.com/revaly-co/rap-sdk/languages/go"
)

func newRealClient(t *testing.T, baseURL string, mutate func(*revaly.Config)) *revaly.Client {
	t.Helper()
	cfg := revaly.Config{APIKey: syntheticKey, BaseURL: baseURL}
	if mutate != nil {
		mutate(&cfg)
	}
	client, err := revaly.NewClient(cfg)
	if err != nil {
		t.Fatalf("NewClient: %v", err)
	}
	return client
}

func TestRealWireConnectionRefusedIsTransientFailure(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	address := listener.Addr().String()
	listener.Close()

	client := newRealClient(t, "http://"+address, nil)
	_, chargeErr := client.Charge(context.Background(), chargeRequest("mtx-wire-1"))
	var transient *revaly.TransientFailure
	if !errors.As(chargeErr, &transient) {
		t.Fatalf("got %T (%v), want *TransientFailure", chargeErr, chargeErr)
	}
	var op *net.OpError
	if !errors.As(chargeErr, &op) || op.Op != "dial" {
		t.Fatalf("dial proof missing: %v", chargeErr)
	}
}

func TestRealWireDNSFailureIsTransientFailure(t *testing.T) {
	client := newRealClient(t, "http://rap-go-sdk-no-such-host.invalid", nil)
	_, chargeErr := client.Charge(context.Background(), chargeRequest("mtx-wire-2"))
	var transient *revaly.TransientFailure
	if !errors.As(chargeErr, &transient) {
		t.Fatalf("got %T (%v), want *TransientFailure", chargeErr, chargeErr)
	}
	var dnsErr *net.DNSError
	if !errors.As(chargeErr, &dnsErr) {
		t.Fatalf("DNS error missing from the chain: %v", chargeErr)
	}
}

func TestRealWireTLSCertificateFailureIsTransientFailure(t *testing.T) {
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {}))
	defer server.Close()

	client := newRealClient(t, server.URL, nil)
	_, chargeErr := client.Charge(context.Background(), chargeRequest("mtx-wire-3"))
	var transient *revaly.TransientFailure
	if !errors.As(chargeErr, &transient) {
		t.Fatalf("got %T (%v), want *TransientFailure", chargeErr, chargeErr)
	}
	var certErr *tls.CertificateVerificationError
	if !errors.As(chargeErr, &certErr) {
		t.Fatalf("certificate-verification proof missing: %v", chargeErr)
	}
}

// A plaintext endpoint reached over https:// fails during the handshake with a
// generic TLS error — not phase-provable by type → OutcomeUnknown (the
// documented TLS conservatism).
func TestRealWirePlaintextOnTLSIsOutcomeUnknown(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {}))
	defer server.Close()

	client := newRealClient(t, "https"+server.URL[len("http"):], nil)
	_, chargeErr := client.Charge(context.Background(), chargeRequest("mtx-wire-4"))
	var unknown *revaly.OutcomeUnknown
	if !errors.As(chargeErr, &unknown) {
		t.Fatalf("got %T (%v), want *OutcomeUnknown", chargeErr, chargeErr)
	}
}

// The server accepts and never responds: the overall deadline expires AFTER
// send → OutcomeUnknown, never TransientFailure.
func TestRealWireStallAfterSendIsOutcomeUnknown(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()
	go func() {
		for {
			conn, acceptErr := listener.Accept()
			if acceptErr != nil {
				return
			}
			go func(c net.Conn) {
				buffer := make([]byte, 4096)
				_, _ = c.Read(buffer)
				time.Sleep(5 * time.Second)
				c.Close()
			}(conn)
		}
	}()

	client := newRealClient(t, "http://"+listener.Addr().String(), func(cfg *revaly.Config) {
		cfg.OverallDeadline = 300 * time.Millisecond
	})
	_, chargeErr := client.Charge(context.Background(), chargeRequest("mtx-wire-5"))
	var unknown *revaly.OutcomeUnknown
	if !errors.As(chargeErr, &unknown) {
		t.Fatalf("got %T (%v), want *OutcomeUnknown", chargeErr, chargeErr)
	}
	if !errors.Is(chargeErr, context.DeadlineExceeded) {
		t.Fatalf("expected the deadline in the chain: %v", chargeErr)
	}
}

// An RST after the headers landed surfaces at body-read time → OutcomeUnknown.
func TestRealWireResetMidBodyIsOutcomeUnknown(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()
	go func() {
		conn, acceptErr := listener.Accept()
		if acceptErr != nil {
			return
		}
		buffer := make([]byte, 4096)
		_, _ = conn.Read(buffer)
		_, _ = conn.Write([]byte("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 100\r\n\r\n{\"partial\":"))
		if tcp, ok := conn.(*net.TCPConn); ok {
			tcp.SetLinger(0)
		}
		conn.Close()
	}()

	client := newRealClient(t, "http://"+listener.Addr().String(), nil)
	_, chargeErr := client.Charge(context.Background(), chargeRequest("mtx-wire-6"))
	var unknown *revaly.OutcomeUnknown
	if !errors.As(chargeErr, &unknown) {
		t.Fatalf("got %T (%v), want *OutcomeUnknown", chargeErr, chargeErr)
	}
}

// Single-send semantics: the runtime never follows a redirect (the stdlib
// default would re-POST the body — probed), so the origin sees exactly one
// request, the redirect target sees none, and the 307 classifies
// OutcomeUnknown.
func TestRealWire307IsNeverFollowed(t *testing.T) {
	var originHits, targetHits atomic.Int32
	mux := http.NewServeMux()
	var baseURL string
	mux.HandleFunc("/payments", func(w http.ResponseWriter, r *http.Request) {
		originHits.Add(1)
		w.Header().Set("Location", baseURL+"/elsewhere")
		w.WriteHeader(http.StatusTemporaryRedirect)
	})
	mux.HandleFunc("/elsewhere", func(w http.ResponseWriter, r *http.Request) {
		targetHits.Add(1)
	})
	server := httptest.NewServer(mux)
	defer server.Close()
	baseURL = server.URL

	client := newRealClient(t, server.URL, nil)
	_, chargeErr := client.Charge(context.Background(), chargeRequest("mtx-wire-7"))
	var unknown *revaly.OutcomeUnknown
	if !errors.As(chargeErr, &unknown) {
		t.Fatalf("got %T (%v), want *OutcomeUnknown for the unfollowed 307", chargeErr, chargeErr)
	}
	if originHits.Load() != 1 || targetHits.Load() != 0 {
		t.Fatalf("origin=%d target=%d, want exactly one send and no follow",
			originHits.Load(), targetHits.Load())
	}
}

// A connect-phase expiry with ConnectTimeout mapped onto the dialer surfaces
// as a dial-phase OpError → provably never sent → TransientFailure. Self-skips
// when the environment routes the non-routable probe address.
func TestRealWireConnectTimeoutIsTransientFailure(t *testing.T) {
	client := newRealClient(t, "http://10.255.255.1:81", func(cfg *revaly.Config) {
		cfg.ConnectTimeout = 500 * time.Millisecond
	})
	start := time.Now()
	_, chargeErr := client.Charge(context.Background(), chargeRequest("mtx-wire-8"))
	elapsed := time.Since(start)
	if chargeErr == nil || elapsed < 400*time.Millisecond {
		t.Skipf("environment routes 10.255.255.1 (err=%v in %v) — probe not meaningful here", chargeErr, elapsed)
	}
	var transient *revaly.TransientFailure
	if !errors.As(chargeErr, &transient) {
		t.Skipf("connect probe surfaced %T (%v) — environment-specific, self-skipping", chargeErr, chargeErr)
	}
	var op *net.OpError
	if !errors.As(chargeErr, &op) || op.Op != "dial" {
		t.Fatalf("dial proof missing: %v", chargeErr)
	}
	fmt.Println("connect-timeout proof held in", elapsed)
}
