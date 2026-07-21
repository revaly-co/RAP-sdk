// The reconcile loop (failover-contract §3, runtime-tdd §4) over the mock
// transport: verdict mapping from RAW bodies, degraded-read polling, the
// PermanentRejection escape, policy bounds, and context cancellation.
package tests

import (
	"context"
	"errors"
	"testing"
	"time"

	revaly "github.com/revaly-co/rap-sdk/languages/go"
	"github.com/revaly-co/rap-sdk/languages/go/raptest"
)

func policy(attempts int) revaly.ReconcilePolicy {
	return revaly.ReconcilePolicy{
		MaxAttempts:   attempts,
		OverallBudget: 30 * time.Second,
		InitialDelay:  0, // back-to-back in tests; jitter/backoff has its own test
	}
}

func TestReconcileFindsTerminalOutcomes(t *testing.T) {
	for name, expect := range map[string]struct {
		script  func(*raptest.MockOperation) *raptest.MockOperation
		outcome revaly.TransactionOutcome
	}{
		"approved": {func(o *raptest.MockOperation) *raptest.MockOperation { return o.ReturnsFoundApproved() }, revaly.TransactionOutcomeApproved},
		"declined": {func(o *raptest.MockOperation) *raptest.MockOperation { return o.ReturnsFoundDeclined() }, revaly.TransactionOutcomeDeclined},
	} {
		client, mock := newMockClient(t, nil)
		expect.script(mock.Reconcile("mock-mtx-0001"))
		verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", policy(3))
		if err != nil {
			t.Fatalf("%s: %v", name, err)
		}
		found, ok := verdict.(*revaly.Found)
		if !ok {
			t.Fatalf("%s: verdict %T, want *Found", name, verdict)
		}
		if found.Outcome != expect.outcome {
			t.Fatalf("%s: outcome %q, want %q", name, found.Outcome, expect.outcome)
		}
		if found.Transaction == nil || found.CorrelationID == "" {
			t.Fatalf("%s: expected an enriched sighting with correlation, got %+v", name, found)
		}
	}
}

func TestReconcileFindsPendingIntent(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0001").ReturnsPending()
	verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", policy(2))
	if err != nil {
		t.Fatal(err)
	}
	found, ok := verdict.(*revaly.Found)
	if !ok || found.Outcome != revaly.TransactionOutcomePending || found.Pending == nil {
		t.Fatalf("verdict %#v, want *Found pending with the bound intent", verdict)
	}
}

func TestReconcileNotFoundYetCarriesLoopState(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0001").ReturnsNotFound()
	verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", policy(3))
	if err != nil {
		t.Fatal(err)
	}
	notFound, ok := verdict.(*revaly.NotFoundYet)
	if !ok {
		t.Fatalf("verdict %T, want *NotFoundYet", verdict)
	}
	if notFound.Attempts != 3 || notFound.LastHTTPStatus != 404 || notFound.LastCorrelationID == "" {
		t.Fatalf("loop state %+v, want 3 attempts / 404 / correlation", notFound)
	}
}

// Degraded reads (5xx and wire failures on the GET) keep polling within the
// budget — exactly the window where visibility is widest.
func TestReconcileKeepsPollingThroughDegradedReads(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0001").Returns500().FailsBeforeSend().ReturnsFoundApproved()
	verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", policy(5))
	if err != nil {
		t.Fatal(err)
	}
	if found, ok := verdict.(*revaly.Found); !ok || found.Outcome != revaly.TransactionOutcomeApproved {
		t.Fatalf("verdict %#v, want *Found approved after degraded reads", verdict)
	}
	if len(mock.Requests()) != 3 {
		t.Fatalf("made %d attempts, want 3", len(mock.Requests()))
	}
}

func TestReconcile404ThenFound(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0001").ReturnsNotFound().ReturnsFoundApproved()
	verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", policy(3))
	if err != nil {
		t.Fatal(err)
	}
	if found, ok := verdict.(*revaly.Found); !ok || found.Outcome != revaly.TransactionOutcomeApproved {
		t.Fatalf("verdict %#v, want *Found approved on the second poll", verdict)
	}
}

// A rejected READ that polling can never fix (non-404 PermanentRejection)
// escapes as the typed error.
func TestReconcileRejectedReadEscapes(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0001").ReturnsPermanentRejection(401)
	verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", policy(5))
	var rejection *revaly.PermanentRejection
	if !errors.As(err, &rejection) || verdict != nil {
		t.Fatalf("got verdict=%v err=%v, want the 401 PermanentRejection escape", verdict, err)
	}
	if len(mock.Requests()) != 1 {
		t.Fatalf("made %d attempts, want 1 (no polling on rejected reads)", len(mock.Requests()))
	}
}

// A 2xx body this SDK cannot read at all is NOT a sighting — the loop
// continues (an ambiguous read licenses nothing).
func TestReconcileUnreadable2xxContinues(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0001").ReturnsStatus(200, `[1,2,3]`).ReturnsFoundApproved()
	verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", policy(3))
	if err != nil {
		t.Fatal(err)
	}
	if found, ok := verdict.(*revaly.Found); !ok || found.Outcome != revaly.TransactionOutcomeApproved {
		t.Fatalf("verdict %#v, want *Found approved after the unreadable body", verdict)
	}
}

// Sightings this SDK version cannot bind are still FOUND (conservative:
// found-but-unmapped licenses no failover either way).
func TestReconcileUnmappedSightingsAreFound(t *testing.T) {
	for name, body := range map[string]string{
		"group envelope": `{"transaction":` + raptest.SyntheticTransaction(1) + `,"transactions":[` + raptest.SyntheticTransaction(1) + `]}`,
		"pending newer than the spec": `{"state":"pending","merchantTransactionId":"mock-mtx-0001",` +
			`"reservationExpiresAt":"2026-08-01T00:00:00Z"}`,
	} {
		client, mock := newMockClient(t, nil)
		mock.Reconcile("mock-mtx-0001").ReturnsStatus(200, body)
		verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", policy(2))
		if err != nil {
			t.Fatalf("%s: %v", name, err)
		}
		found, ok := verdict.(*revaly.Found)
		if !ok || found.Outcome != revaly.TransactionOutcomeUnknown {
			t.Fatalf("%s: verdict %#v, want *Found with outcome Unknown", name, verdict)
		}
	}
}

func TestReconcileHonorsContextCancellation(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0001").ReturnsNotFound()
	ctx, cancel := context.WithCancel(context.Background())
	go func() {
		time.Sleep(50 * time.Millisecond)
		cancel()
	}()
	verdict, err := client.Reconcile(ctx, "mock-mtx-0001", revaly.ReconcilePolicy{
		MaxAttempts:   1000,
		OverallBudget: time.Hour,
		InitialDelay:  20 * time.Millisecond,
	})
	if verdict != nil || !errors.Is(err, context.Canceled) {
		t.Fatalf("got verdict=%v err=%v, want the context cancellation", verdict, err)
	}
}

func TestReconcilePolicyValidation(t *testing.T) {
	client, _ := newMockClient(t, nil)
	for name, bad := range map[string]revaly.ReconcilePolicy{
		"zero attempts": {MaxAttempts: 0, OverallBudget: time.Second},
		"zero budget":   {MaxAttempts: 1},
		"negative wait": {MaxAttempts: 1, OverallBudget: time.Second, InitialDelay: -time.Second},
	} {
		if _, err := client.Reconcile(context.Background(), "mock-mtx-0001", bad); err == nil {
			t.Fatalf("%s: expected a validation error", name)
		}
	}
	if _, err := client.Reconcile(context.Background(), "  ", policy(1)); err == nil {
		t.Fatal("blank merchantTransactionID: expected a validation error")
	}
}

// The budget bounds wall-clock spend: with a sticky 404 and a delay schedule
// that exceeds the budget, the loop stops early with NotFoundYet.
func TestReconcileBudgetBoundsTheLoop(t *testing.T) {
	client, mock := newMockClient(t, nil)
	mock.Reconcile("mock-mtx-0001").ReturnsNotFound()
	start := time.Now()
	verdict, err := client.Reconcile(context.Background(), "mock-mtx-0001", revaly.ReconcilePolicy{
		MaxAttempts:   50,
		OverallBudget: 150 * time.Millisecond,
		InitialDelay:  100 * time.Millisecond,
	})
	if err != nil {
		t.Fatal(err)
	}
	notFound, ok := verdict.(*revaly.NotFoundYet)
	if !ok {
		t.Fatalf("verdict %T, want *NotFoundYet", verdict)
	}
	if notFound.Attempts >= 50 {
		t.Fatalf("attempts = %d, want the budget to stop the loop early", notFound.Attempts)
	}
	if elapsed := time.Since(start); elapsed > 2*time.Second {
		t.Fatalf("loop ran %v, want it bounded by the budget", elapsed)
	}
}
