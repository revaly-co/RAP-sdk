// Failure-class taxonomy over the mock transport — every failover-contract §2
// row, the version-pin narrowing, and the transport header contract
// (ADR-SDK-005, runtime-tdd §5).
package tests

import (
	"context"
	"errors"
	"net"
	"regexp"
	"testing"

	revaly "github.com/revaly-co/rap-sdk/languages/go"
	core "github.com/revaly-co/rap-sdk/languages/go/core"
	"github.com/revaly-co/rap-sdk/languages/go/raptest"
)

const syntheticKey = "sk_synthetic_test_key_123"

func newMockClient(t *testing.T, mutate func(*revaly.Config)) (*revaly.Client, *raptest.MockTransport) {
	t.Helper()
	mock := raptest.NewMockTransport()
	cfg := revaly.Config{APIKey: syntheticKey, Transport: mock}
	if mutate != nil {
		mutate(&cfg)
	}
	client, err := revaly.NewClient(cfg)
	if err != nil {
		t.Fatalf("NewClient: %v", err)
	}
	return client, mock
}

func chargeRequest(merchantTransactionID string) *core.PaymentRequest {
	return core.NewPaymentRequest(1099, merchantTransactionID)
}

// A nil request is a plain programming error (ADR-SDK-028 G1) — never one of
// the three typed failure classes: nothing was attempted, so nothing gets
// classified, and no request reaches the wire.
func TestNilRequestIsAPlainError(t *testing.T) {
	client, mock := newMockClient(t, nil)
	_, err := client.Charge(context.Background(), nil)
	if err == nil {
		t.Fatal("Charge(nil) succeeded, want a plain error")
	}
	var rejection *revaly.PermanentRejection
	var transient *revaly.TransientFailure
	var unknown *revaly.OutcomeUnknown
	if errors.As(err, &rejection) || errors.As(err, &transient) || errors.As(err, &unknown) {
		t.Fatalf("Charge(nil) returned a typed failure class (%T) — want a plain error", err)
	}
	if got := len(mock.Requests()); got != 0 {
		t.Fatalf("nil request reached the wire (%d requests recorded)", got)
	}
}

func TestPermanentRejectionStatuses(t *testing.T) {
	for _, status := range []int{400, 401, 403, 404, 422} {
		client, mock := newMockClient(t, nil)
		mock.Charge().ReturnsPermanentRejection(status)
		_, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
		var rejection *revaly.PermanentRejection
		if !errors.As(err, &rejection) {
			t.Fatalf("status %d: got %T (%v), want *PermanentRejection", status, err, err)
		}
		if rejection.Status != status {
			t.Fatalf("status field = %d, want %d", rejection.Status, status)
		}
		if rejection.CorrelationID == "" {
			t.Fatalf("status %d: correlation id missing on the typed error", status)
		}
	}
}

func TestNotProcessed503IsTransientFailure(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Charge().ReturnsNotProcessed503()
	_, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
	var transient *revaly.TransientFailure
	if !errors.As(err, &transient) {
		t.Fatalf("got %T (%v), want *TransientFailure", err, err)
	}
	if transient.Code != "not_processed" || transient.Status != 503 {
		t.Fatalf("code=%q status=%d, want not_processed/503", transient.Code, transient.Status)
	}
}

func TestOutcomeUnknownStatuses(t *testing.T) {
	cases := map[string]func(*raptest.MockOperation) *raptest.MockOperation{
		"bare 503":         func(o *raptest.MockOperation) *raptest.MockOperation { return o.ReturnsBare503() },
		"500":              func(o *raptest.MockOperation) *raptest.MockOperation { return o.Returns500() },
		"502 edge":         func(o *raptest.MockOperation) *raptest.MockOperation { return o.Returns502() },
		"504 edge":         func(o *raptest.MockOperation) *raptest.MockOperation { return o.Returns504() },
		"307 not followed": func(o *raptest.MockOperation) *raptest.MockOperation { return o.ReturnsStatus(307, "") },
		"429 outside the table": func(o *raptest.MockOperation) *raptest.MockOperation {
			return o.ReturnsStatus(429, raptest.SyntheticError("slow down", ""))
		},
	}
	for name, script := range cases {
		client, mock := newMockClient(t, nil)
		script(mock.Charge())
		_, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
		var unknown *revaly.OutcomeUnknown
		if !errors.As(err, &unknown) {
			t.Fatalf("%s: got %T (%v), want *OutcomeUnknown", name, err, err)
		}
	}
}

// On the "2.0" pin the code field is not part of the documented contract — the
// fast-failover class narrows to client-provable never-sent failures only
// (runtime-tdd §1).
func TestVersion20NarrowsNotProcessedToOutcomeUnknown(t *testing.T) {
	client, mock := newMockClient(t, func(cfg *revaly.Config) { cfg.APIVersion = "2.0" })
	mock.Charge().ReturnsNotProcessed503()
	_, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
	var unknown *revaly.OutcomeUnknown
	if !errors.As(err, &unknown) {
		t.Fatalf("got %T (%v), want *OutcomeUnknown under the 2.0 pin", err, err)
	}
}

func TestWireFailureClasses(t *testing.T) {
	t.Run("dial-phase failure is TransientFailure with the OpError proof", func(t *testing.T) {
		client, mock := newMockClient(t, nil)
		mock.Charge().FailsBeforeSend()
		_, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
		var transient *revaly.TransientFailure
		if !errors.As(err, &transient) {
			t.Fatalf("got %T (%v), want *TransientFailure", err, err)
		}
		var op *net.OpError
		if !errors.As(err, &op) || op.Op != "dial" {
			t.Fatalf("dial OpError proof missing from the chain: %v", err)
		}
	})
	t.Run("timeout after send is OutcomeUnknown", func(t *testing.T) {
		client, mock := newMockClient(t, nil)
		mock.Charge().TimesOutAfterSend()
		_, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
		var unknown *revaly.OutcomeUnknown
		if !errors.As(err, &unknown) {
			t.Fatalf("got %T (%v), want *OutcomeUnknown", err, err)
		}
	})
	t.Run("reset mid-flight is OutcomeUnknown", func(t *testing.T) {
		client, mock := newMockClient(t, nil)
		mock.Charge().ResetsMidFlight()
		_, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
		var unknown *revaly.OutcomeUnknown
		if !errors.As(err, &unknown) {
			t.Fatalf("got %T (%v), want *OutcomeUnknown", err, err)
		}
	})
}

func TestUnreadable2xxIsOutcomeUnknown(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Charge().ReturnsStatus(200, `{not json`)
	_, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
	var unknown *revaly.OutcomeUnknown
	if !errors.As(err, &unknown) {
		t.Fatalf("got %T (%v), want *OutcomeUnknown", err, err)
	}
	if unknown.Status != 200 {
		t.Fatalf("status = %d, want 200", unknown.Status)
	}
}

func TestSuccessfulChargeParses(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Charge().ReturnsApproved()
	tx, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001"))
	if err != nil {
		t.Fatalf("charge: %v", err)
	}
	if tx.GetTransactionStatus() != 1 || tx.GetMerchantTransactionId() != "mock-mtx-0001" {
		t.Fatalf("unexpected transaction: %+v", tx)
	}
}

var userAgentPattern = regexp.MustCompile(`^revaly-sdk-go/0\.0\.0-dev \(go[0-9a-z.]+; (linux|windows|darwin|other)\)$`)

// The transport header contract: exact ADR-SDK-005 User-Agent grammar, the
// ApiKey auth scheme, and the X-Api-Version default pin — all injected where
// the core cannot bypass them.
func TestTransportHeaderContract(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Charge().ReturnsApproved()
	if _, err := client.Charge(context.Background(), chargeRequest("mock-mtx-0001")); err != nil {
		t.Fatalf("charge: %v", err)
	}
	requests := mock.Requests()
	if len(requests) != 1 {
		t.Fatalf("recorded %d requests, want 1", len(requests))
	}
	headers := requests[0].Header
	if got := headers.Get("Authorization"); got != "ApiKey "+syntheticKey {
		t.Fatalf("Authorization = %q, want the ApiKey scheme", got)
	}
	if got := headers.Get("X-Api-Version"); got != "2.1" {
		t.Fatalf("X-Api-Version = %q, want the 2.1 default pin", got)
	}
	if ua := headers.Get("User-Agent"); !userAgentPattern.MatchString(ua) {
		t.Fatalf("User-Agent %q does not match the ADR-SDK-005 grammar", ua)
	}
	if err := mock.RequireUserAgent(); err != nil {
		t.Fatal(err)
	}
}

// A per-call version selected through the core wins over the default pin
// (set-if-absent semantics).
func TestPerCallAPIVersionWins(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0002").ReturnsFoundApproved()
	_, _, err := client.Core().TransactionsAPI.
		GetTransactionByMerchantTransactionId(context.Background(), "mock-mtx-0002").
		XApiVersion("2.0").Execute()
	if err != nil {
		t.Fatalf("core call: %v", err)
	}
	requests := mock.Requests()
	if got := requests[len(requests)-1].Header.Get("X-Api-Version"); got != "2.0" {
		t.Fatalf("X-Api-Version = %q, want the per-call 2.0", got)
	}
}
