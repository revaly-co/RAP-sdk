// The OutcomeUnknown reconciliation procedure (failover-contract §3).
//
// GET-only, side-effect-free, caller-bounded — the only loop the runtime owns
// (ADR-SDK-004). Verdicts are read from the RAW response body, never the
// core's typed union wrapper (repo rule 5): reconciliation is the safety path,
// so it must not depend on generated discrimination logic — server-newer-than-
// spec shapes still count as sightings here. (The wrapper discrimination
// itself works since the model_oneof template fork, but the safety path stays
// raw BY DESIGN, exactly like the other language runtimes.)
package runtime

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log/slog"
	"math/rand"
	"net/http"
	"net/url"
	"strings"
	"time"

	core "github.com/revaly-co/rap-sdk/languages/go/core"
)

const (
	backoffMultiplier = 2.0
	jitterRatio       = 0.2
	reconcilePath     = "/transactions/merchant/{merchantTransactionId}"
)

// TransactionOutcome is the terminal outcome of a found transaction, mapped
// from the record's transactionStatus (1=Approved, 2=Declined, 3=Error).
// Pending is the post-P-2 intent state; Unknown covers unmapped statuses and
// record shapes this SDK version cannot read — found-but-unmapped is still
// FOUND. The string values match the other language runtimes' tokens so
// cross-language log lines join cleanly.
type TransactionOutcome string

const (
	TransactionOutcomeApproved TransactionOutcome = "Approved"
	TransactionOutcomeDeclined TransactionOutcome = "Declined"
	TransactionOutcomeError    TransactionOutcome = "Error"
	TransactionOutcomePending  TransactionOutcome = "Pending"
	TransactionOutcomeUnknown  TransactionOutcome = "Unknown"
)

// ReconcileVerdict is the reconcile result — V1 returns *Found or *NotFoundYet
// only, and the set is OPEN FOR EXTENSION by design (ADR-SDK-009):
// SafeToFailover arrives with platform P-2 as a **minor** release. ALWAYS
// dispatch with a type switch carrying a default branch — the quickstart shows
// it.
type ReconcileVerdict interface{ reconcileVerdict() }

// Found: a record for the merchantTransactionId IS visible at RAP-core (§3).
// Found with Outcome Approved means the money moved — failing over now would
// double-charge.
type Found struct {
	Outcome TransactionOutcome
	// Transaction is the terminal record, when the sighting was a terminal
	// transaction this SDK version could bind (a sighting it cannot bind
	// still returns Found).
	Transaction *core.TransactionResponse
	// Pending is the pending intent, when the sighting was a post-P-2 pending
	// state.
	Pending       *core.PendingTransactionResponse
	CorrelationID string
}

func (*Found) reconcileVerdict() {}

// NotFoundYet: no record is visible YET (§3): platform visibility is
// asynchronous and unbounded — absence is NOT provable in V1. Hold and
// re-poll; on sustained NotFoundYet, escalate per merchant policy.
type NotFoundYet struct {
	Attempts int
	// Elapsed is wall-clock time spent across all attempts and waits.
	Elapsed           time.Duration
	LastCorrelationID string
	// LastHTTPStatus is the last observed HTTP status (0 when no attempt
	// produced a response).
	LastHTTPStatus int
}

func (*NotFoundYet) reconcileVerdict() {}

// ReconcilePolicy is the caller-bounded polling policy — the ONLY loop this
// SDK owns (ADR-SDK-004). All bounds are explicit: the SDK ships no default
// attempt counts, budgets, or delays until the OQ-6 telemetry-derived
// recommendations land (docs/open-items.md — deliberately not invented here).
// The backoff shape is exponential with jitter ([Proposed]: multiplier 2.0,
// full jitter ±20%).
//
// Choose bounds per your risk policy: reconciliation is how an OutcomeUnknown
// payment is resolved, so the budget bounds how long your checkout holds
// before escalating.
type ReconcilePolicy struct {
	// MaxAttempts is the maximum number of GET attempts (≥ 1).
	MaxAttempts int
	// OverallBudget is the total wall-clock budget across all attempts and
	// waits (> 0).
	OverallBudget time.Duration
	// InitialDelay is the delay before the second attempt; it doubles each
	// attempt (with jitter). Zero polls back-to-back within the budget.
	InitialDelay time.Duration
	// MaxDelay optionally caps the per-wait delay; zero leaves growth
	// uncapped within the budget.
	MaxDelay time.Duration
}

func (p ReconcilePolicy) validate() error {
	if p.MaxAttempts < 1 {
		return errors.New("revaly: ReconcilePolicy.MaxAttempts: at least one attempt is required")
	}
	if p.OverallBudget <= 0 {
		return errors.New("revaly: ReconcilePolicy.OverallBudget: the overall budget must be positive")
	}
	if p.InitialDelay < 0 || p.MaxDelay < 0 {
		return errors.New("revaly: ReconcilePolicy: delays cannot be negative")
	}
	return nil
}

// delayForAttempt is the jittered wait after the given number of completed
// attempts.
func delayForAttempt(policy ReconcilePolicy, completedAttempts int) time.Duration {
	if policy.InitialDelay <= 0 {
		return 0
	}
	raw := float64(policy.InitialDelay)
	for i := 1; i < completedAttempts; i++ {
		raw *= backoffMultiplier
	}
	if policy.MaxDelay > 0 && raw > float64(policy.MaxDelay) {
		raw = float64(policy.MaxDelay)
	}
	jitterSpan := raw * jitterRatio
	jittered := raw + (rand.Float64()*2-1)*jitterSpan
	if jittered < 0 {
		return 0
	}
	return time.Duration(jittered)
}

// reconciler runs the reconcile loop until a record is visible or the policy
// bounds are spent.
//
// It returns a typed failure only for a rejected READ that polling can never
// fix (PermanentRejection other than 404 — bad credentials, malformed id);
// 404 is the NotFoundYet signal, and degraded reads (5xx/timeouts/transport
// failures) keep polling within the budget — exactly the window where
// visibility is widest. Context cancellation returns ctx.Err(): a cancelled
// reconcile proves nothing about the payment.
type reconciler struct {
	httpClient *http.Client
	baseURL    string
	apiVersion string
	logger     *slog.Logger
	trace      WireTraceHook
}

func (r *reconciler) reconcile(ctx context.Context, merchantTransactionID string, policy ReconcilePolicy) (ReconcileVerdict, error) {
	if strings.TrimSpace(merchantTransactionID) == "" {
		return nil, errors.New("revaly: merchantTransactionID is required")
	}
	if err := policy.validate(); err != nil {
		return nil, err
	}
	if ctx == nil {
		ctx = context.Background()
	}

	requestURL := r.baseURL + "/transactions/merchant/" + url.PathEscape(merchantTransactionID)
	start := time.Now()
	attempts := 0
	lastCorrelationID := ""
	lastHTTPStatus := 0

	for {
		if err := ctx.Err(); err != nil {
			return nil, err
		}
		attempts++

		verdict, status, correlationID, failure := r.attempt(ctx, requestURL)
		if status != 0 {
			lastHTTPStatus = status
		}
		if correlationID != "" {
			lastCorrelationID = correlationID
		}
		if failure != nil {
			var rejection *PermanentRejection
			if errors.As(failure, &rejection) && rejection.Status != 404 {
				// 400/401/403/422 escape: polling will never fix a rejected
				// read (bad credentials, malformed id) — the caller must see it.
				return nil, failure
			}
			if errors.Is(failure, context.Canceled) || errors.Is(failure, context.DeadlineExceeded) {
				if ctx.Err() != nil {
					return nil, ctx.Err()
				}
			}
			if lastHTTPStatus == 404 {
				r.logger.Debug("rap.reconcile not visible yet (404)", "attempt", attempts)
			} else {
				// Degraded read (5xx/timeout/transport failure on the GET):
				// the WRITE's status is still unknown — keep polling within
				// the caller's budget.
				r.logger.Warn("rap.reconcile degraded read; continuing within policy",
					"attempt", attempts, "status", lastHTTPStatus)
			}
		}
		if verdict != nil {
			return verdict, nil
		}

		if attempts >= policy.MaxAttempts {
			break
		}
		elapsed := time.Since(start)
		delay := delayForAttempt(policy, attempts)
		if elapsed+delay >= policy.OverallBudget {
			break
		}
		if delay > 0 {
			timer := time.NewTimer(delay)
			select {
			case <-ctx.Done():
				timer.Stop()
				return nil, ctx.Err()
			case <-timer.C:
			}
		}
	}

	elapsed := time.Since(start)
	r.logger.Info("rap.reconcile verdict=NotFoundYet",
		"attempts", attempts, "elapsed", elapsed, "last_status", lastHTTPStatus, "correlation", lastCorrelationID)
	return &NotFoundYet{
		Attempts:          attempts,
		Elapsed:           elapsed,
		LastCorrelationID: lastCorrelationID,
		LastHTTPStatus:    lastHTTPStatus,
	}, nil
}

// attempt performs one GET. It returns a verdict when the body proved a
// sighting, the observed status/correlation, and the classified failure for
// non-2xx or wire errors (nil on a readable 2xx).
func (r *reconciler) attempt(ctx context.Context, requestURL string) (ReconcileVerdict, int, string, error) {
	request, err := http.NewRequestWithContext(ctx, http.MethodGet, requestURL, nil)
	if err != nil {
		return nil, 0, "", fmt.Errorf("revaly: building reconcile request: %w", err)
	}
	response, err := r.httpClient.Do(request)
	if err != nil {
		return nil, 0, "", ClassifyTransportError(err)
	}
	defer response.Body.Close()

	status := response.StatusCode
	correlationID := response.Header.Get(CorrelationIDHeader)
	bodyBytes, readErr := io.ReadAll(response.Body)
	if readErr != nil {
		return nil, status, correlationID, ClassifyTransportError(readErr)
	}
	rawBody := string(bodyBytes)
	r.emitReconcileTrace(status, correlationID, rawBody)

	if classified := ClassifyResponse(status, rawBody, correlationID, r.apiVersion); classified != nil {
		return nil, status, correlationID, classified
	}
	return r.readFound(rawBody, correlationID), status, correlationID, nil
}

// readFound maps a 2xx body to a Found verdict from the RAW json. Returns nil
// for a body this SDK cannot read at all (→ poll-continue: an ambiguous read
// is not a sighting).
func (r *reconciler) readFound(rawBody string, correlationID string) ReconcileVerdict {
	var root map[string]json.RawMessage
	if err := json.Unmarshal([]byte(rawBody), &root); err != nil || root == nil {
		r.logger.Warn("rap.reconcile 2xx with an unreadable body; continuing within policy")
		return nil
	}

	// `state` exists only on the pending schema — its presence is
	// authoritative (the spec marks it the discriminator).
	if stateRaw, ok := root["state"]; ok {
		var state string
		if json.Unmarshal(stateRaw, &state) == nil {
			var pending core.PendingTransactionResponse
			if err := json.Unmarshal([]byte(rawBody), &pending); err == nil {
				r.logger.Info("rap.reconcile verdict=Found", "outcome", TransactionOutcomePending, "correlation", correlationID)
				return &Found{Outcome: TransactionOutcomePending, Pending: &pending, CorrelationID: correlationID}
			}
			// A pending-shaped record this SDK version cannot bind is still a
			// sighting — surface it conservatively rather than polling on.
			return &Found{Outcome: TransactionOutcomeUnknown, CorrelationID: correlationID}
		}
	}

	// Terminal records: the outcome maps from the RAW json; the typed model
	// bind only enriches the verdict. A record the model cannot bind (e.g. a
	// grouped envelope, or a shape newer than this SDK) is still FOUND —
	// found-but-unmapped licenses no failover either way.
	outcome := mapOutcome(root["transactionStatus"])
	var transaction *core.TransactionResponse
	var bound core.TransactionResponse
	if err := json.Unmarshal([]byte(rawBody), &bound); err == nil {
		transaction = &bound
	}
	r.logger.Info("rap.reconcile verdict=Found", "outcome", outcome, "correlation", correlationID)
	return &Found{Outcome: outcome, Transaction: transaction, CorrelationID: correlationID}
}

func (r *reconciler) emitReconcileTrace(status int, correlationID string, rawBody string) {
	if r.trace == nil {
		return
	}
	emitTrace(r.logger, r.trace, WireTraceEvent{
		Operation:            "reconcile",
		Method:               http.MethodGet,
		Path:                 reconcilePath,
		Status:               status,
		CorrelationID:        correlationID,
		ScrubbedResponseBody: ScrubJSON(rawBody),
	})
}

func mapOutcome(raw json.RawMessage) TransactionOutcome {
	if raw == nil {
		return TransactionOutcomeUnknown
	}
	var status int
	if err := json.Unmarshal(raw, &status); err != nil {
		return TransactionOutcomeUnknown
	}
	switch status {
	case 1:
		return TransactionOutcomeApproved
	case 2:
		return TransactionOutcomeDeclined
	case 3:
		return TransactionOutcomeError
	default:
		return TransactionOutcomeUnknown
	}
}
