// Stage-4 contract smoke (ADR-SDK-024, pipeline stage 4): a thin, live
// runtime-contract check of THIS SDK against the environment named by
// RAP_SMOKE_BASE_URL / RAP_SMOKE_API_KEY (interim: Backbone staging;
// at GA: the merchant sandbox key-scope). Its single purpose is proving the
// SDK's classification against reality — it deliberately does not replicate
// platform test coverage.
//
// Environment contract (same across all six languages):
//
//	RAP_SMOKE_BASE_URL            required — target base URL
//	RAP_SMOKE_API_KEY             required — staging/sandbox-scoped key
//	RAP_SMOKE_GATEWAY_ROUTING_ID  optional — included in charge payloads when set
//	                              (staging routes by it; drop at GA retarget)
//	RAP_SMOKE_FAULT_INJECT        optional — value ("pre-dispatch") sent as the
//	                              platform's X-Backbone-Fault-Inject header to
//	                              trigger the 503+not_processed row; the scenario
//	                              SKIPs when unset (the injector is structurally
//	                              inert outside staging/testing)
//
// Scenarios mirror the quickstart shape (README). Output is values-free
// (ADR-SDK-020): identifiers, statuses, classes and correlation ids only —
// never payload values, never the key, never the target host.
//
// Exit codes: 0 all scenarios pass (skips allowed) · 1 at least one failed ·
// 2 not configured.
package main

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"net/http"
	"os"
	"time"

	revaly "github.com/revaly-co/rap-sdk/languages/go"
)

// faultInjectHeader is the platform's executor fault seam (Backbone ADR 014
// test affordance): value "pre-dispatch" makes the charge fail between intent
// reservation and gateway dispatch — the only deterministic live trigger for
// the 503 + code=not_processed fast-failover row.
const faultInjectHeader = "X-Backbone-Fault-Inject"

// errSkip marks a scenario that cannot run in this environment (reported as
// SKIP, never silently dropped, never a failure).
type errSkip struct{ reason string }

func (e errSkip) Error() string { return e.reason }

// headerInjectingWire is a real-HTTP wire that stamps one extra header on
// every request. It sits at the Config.Wire seam, INSIDE the runtime's own
// header injection, so auth/UA/version behaviour is unchanged.
type headerInjectingWire struct {
	name  string
	value string
}

func (w *headerInjectingWire) RoundTrip(req *http.Request) (*http.Response, error) {
	cloned := req.Clone(req.Context())
	cloned.Header.Set(w.name, w.value)
	return http.DefaultTransport.RoundTrip(cloned)
}

func main() {
	baseURL := os.Getenv("RAP_SMOKE_BASE_URL")
	apiKey := os.Getenv("RAP_SMOKE_API_KEY")
	routingID := os.Getenv("RAP_SMOKE_GATEWAY_ROUTING_ID")
	faultValue := os.Getenv("RAP_SMOKE_FAULT_INJECT")
	if baseURL == "" || apiKey == "" {
		fmt.Fprintln(os.Stderr, "smoke: RAP_SMOKE_BASE_URL and RAP_SMOKE_API_KEY must be set (ADR-SDK-024) — refusing to run.")
		os.Exit(2)
	}

	// One client per configuration, quickstart-shaped. The wire-trace hook is
	// the designed observer for correlation ids on the success path (DX §c);
	// events arrive already scrubbed by the runtime.
	var lastTrace revaly.WireTraceEvent
	client := mustClient(revaly.Config{
		APIKey:          apiKey,
		BaseURL:         baseURL,
		ConnectTimeout:  5 * time.Second,
		OverallDeadline: 15 * time.Second,
		WireTrace:       func(ev revaly.WireTraceEvent) { lastTrace = ev },
	})

	// A separately configured client whose key is a synthetic invalid value —
	// the auth-rejection row. Same wire, same headers, wrong credential.
	badKeyClient := mustClient(revaly.Config{
		APIKey:          "sk_smoke_synthetic_invalid",
		BaseURL:         baseURL,
		ConnectTimeout:  5 * time.Second,
		OverallDeadline: 15 * time.Second,
	})

	// A client whose wire stamps the platform's fault-inject header — every
	// charge through it deterministically fails pre-dispatch (503 +
	// code=not_processed). Only built when the scenario is enabled.
	var faultClient *revaly.Client
	if faultValue != "" {
		faultClient = mustClient(revaly.Config{
			APIKey:          apiKey,
			BaseURL:         baseURL,
			OverallDeadline: 15 * time.Second,
			Wire:            &headerInjectingWire{name: faultInjectHeader, value: faultValue},
		})
	}

	// buildCharge assembles a quickstart-shaped charge request. One synthetic
	// test PAN; the EXPIRY drives the outcome (staging-verified matrix
	// 2026-07-18: 12/2027 approves, 12/2020 declines).
	buildCharge := func(mtid, number, month, year string) revaly.PaymentRequest {
		request := *revaly.NewPaymentRequest(1999, mtid)
		request.SetCurrency("USD")
		if routingID != "" {
			request.SetGatewayRoutingId(routingID)
		}
		card := revaly.NewCreditCard(number, month, year)
		card.SetCardVerificationCode("123")
		method := revaly.NewPaymentMethod()
		method.SetCreditCard(*card)
		request.SetPaymentMethod(*method)
		return request
	}

	// Charged ids feed the reconcile scenarios: the verdicts — through the
	// runtime's own outcome mapping — are the proof the charge outcomes were
	// what the smoke claims.
	chargedID := freshID("charge")
	declinedID := freshID("decline")

	scenarios := []struct {
		name string
		run  func(ctx context.Context) (string, error)
	}{
		{"charge-approved", func(ctx context.Context) (string, error) {
			transaction, err := client.Charge(ctx, buildCharge(chargedID, "4111111111111111", "12", "2027"))
			if err != nil {
				return "", classified("expected a successful charge", err)
			}
			if transaction.GetTransactionId() == "" {
				return "", errors.New("transactionId is empty on the success surface")
			}
			if lastTrace.CorrelationID == "" {
				return "", errors.New("no X-Correlation-ID observed on the success path (DX §c)")
			}
			return fmt.Sprintf(" (txn=%s correlation=%s)", transaction.GetTransactionId(), lastTrace.CorrelationID), nil
		}},

		{"charge-declined", func(ctx context.Context) (string, error) {
			// An expired expiry declines deterministically (same PAN — the
			// expiry drives the outcome). A decline is a business outcome on
			// the SUCCESS surface — not a failure class;
			// reconcile-found-declined proves the mapping below.
			transaction, err := client.Charge(ctx, buildCharge(declinedID, "4111111111111111", "12", "2020"))
			if err != nil {
				return "", classified("expected a declined charge on the success surface", err)
			}
			if transaction.GetTransactionId() == "" {
				return "", errors.New("transactionId is empty on the declined-charge surface")
			}
			if lastTrace.CorrelationID == "" {
				return "", errors.New("no X-Correlation-ID observed on the declined-charge path (DX §c)")
			}
			return fmt.Sprintf(" (txn=%s correlation=%s)", transaction.GetTransactionId(), lastTrace.CorrelationID), nil
		}},

		{"charge-validation-rejected", func(ctx context.Context) (string, error) {
			// An empty card number passes every client-side model but fails
			// the server's required-field validation — the rejection is proven
			// to come from reality (HTTP 400, no code on 4xx).
			_, err := client.Charge(ctx, buildCharge(freshID("validation"), "", "12", "2027"))
			if err == nil {
				return "", errors.New("server accepted an empty card number — expected PermanentRejection")
			}
			var rejection *revaly.PermanentRejection
			if !errors.As(err, &rejection) {
				return "", classified("expected PermanentRejection", err)
			}
			if rejection.Status != 400 && rejection.Status != 422 {
				return "", fmt.Errorf("expected HTTP 400/422, got %d", rejection.Status)
			}
			if rejection.CorrelationID == "" {
				return "", errors.New("no X-Correlation-ID on the rejection (DX §c)")
			}
			return fmt.Sprintf(" (status=%d correlation=%s)", rejection.Status, rejection.CorrelationID), nil
		}},

		{"charge-auth-rejected", func(ctx context.Context) (string, error) {
			_, err := badKeyClient.Charge(ctx, buildCharge(freshID("auth"), "4111111111111111", "12", "2027"))
			if err == nil {
				return "", errors.New("server accepted a synthetic invalid key — expected PermanentRejection")
			}
			var rejection *revaly.PermanentRejection
			if !errors.As(err, &rejection) {
				return "", classified("expected PermanentRejection", err)
			}
			if rejection.Status != 401 && rejection.Status != 403 {
				return "", fmt.Errorf("expected HTTP 401/403, got %d", rejection.Status)
			}
			if rejection.CorrelationID == "" {
				return "", errors.New("no X-Correlation-ID on the auth rejection (DX §c)")
			}
			return fmt.Sprintf(" (status=%d correlation=%s)", rejection.Status, rejection.CorrelationID), nil
		}},

		{"charge-not-processed-503", func(ctx context.Context) (string, error) {
			// The fast-failover row (503 + code=not_processed): valid input
			// cannot reach it deterministically, so the platform's fault
			// injector fails the charge pre-dispatch. TransientFailure is the
			// ONLY acceptable class here — it is the row that licenses
			// immediate failover.
			if faultClient == nil {
				return "", errSkip{"RAP_SMOKE_FAULT_INJECT not set (injector is staging-only)"}
			}
			_, err := faultClient.Charge(ctx, buildCharge(freshID("fault"), "4111111111111111", "12", "2027"))
			if err == nil {
				return "", errors.New("fault-injected charge succeeded — expected TransientFailure")
			}
			var transient *revaly.TransientFailure
			if !errors.As(err, &transient) {
				return "", classified("expected TransientFailure", err)
			}
			if transient.Status != 503 {
				return "", fmt.Errorf("expected HTTP 503, got %d", transient.Status)
			}
			if transient.Code != "not_processed" {
				return "", fmt.Errorf("expected code=not_processed, got %q", transient.Code)
			}
			if transient.CorrelationID == "" {
				return "", errors.New("no X-Correlation-ID on the not-processed failure (DX §c)")
			}
			return fmt.Sprintf(" (status=503 code=%s correlation=%s)", transient.Code, transient.CorrelationID), nil
		}},

		{"reconcile-found-approved", func(ctx context.Context) (string, error) {
			// Found(Approved) through the runtime's own outcome mapping is the
			// approval proof for scenario 1; visibility is asynchronous, hence
			// the budget.
			verdict, err := client.Reconcile(ctx, chargedID, revaly.ReconcilePolicy{
				MaxAttempts:   5,
				OverallBudget: 30 * time.Second,
				InitialDelay:  1 * time.Second,
			})
			if err != nil {
				return "", classified("reconcile errored", err)
			}
			return expectFound(verdict, revaly.TransactionOutcomeApproved)
		}},

		{"reconcile-found-declined", func(ctx context.Context) (string, error) {
			// The declined charge must reconcile as Found(Declined) — the
			// outcome branch that tells a merchant their own gateway is safe.
			verdict, err := client.Reconcile(ctx, declinedID, revaly.ReconcilePolicy{
				MaxAttempts:   5,
				OverallBudget: 30 * time.Second,
				InitialDelay:  1 * time.Second,
			})
			if err != nil {
				return "", classified("reconcile errored", err)
			}
			return expectFound(verdict, revaly.TransactionOutcomeDeclined)
		}},

		{"reconcile-not-found-yet", func(ctx context.Context) (string, error) {
			// A fresh, never-used merchantTransactionId (ADR-SDK-024): the
			// only correct verdict is NotFoundYet, and it must come from real
			// 404s — not from a transport that never reached the API.
			verdict, err := client.Reconcile(ctx, freshID("absent"), revaly.ReconcilePolicy{
				MaxAttempts:   2,
				OverallBudget: 10 * time.Second,
				InitialDelay:  500 * time.Millisecond,
			})
			if err != nil {
				return "", classified("reconcile errored", err)
			}
			switch v := verdict.(type) {
			case *revaly.NotFoundYet:
				if v.LastHTTPStatus != 404 {
					return "", fmt.Errorf("expected last HTTP status 404, got %d", v.LastHTTPStatus)
				}
				if v.LastCorrelationID == "" {
					return "", errors.New("no X-Correlation-ID on the NotFoundYet verdict (DX §c)")
				}
				return fmt.Sprintf(" (attempts=%d correlation=%s)", v.Attempts, v.LastCorrelationID), nil
			case *revaly.Found:
				return "", errors.New("a never-used id reconciled as Found")
			default:
				return "", fmt.Errorf("unrecognized verdict %T", verdict)
			}
		}},
	}

	fmt.Printf("RAP contract smoke (go): %d scenarios\n", len(scenarios))
	failures, skips := 0, 0
	for _, s := range scenarios {
		detail, err := s.run(context.Background())
		var skip errSkip
		switch {
		case err == nil:
			fmt.Printf("PASS %s%s\n", s.name, detail)
		case errors.As(err, &skip):
			skips++
			fmt.Printf("SKIP %s (%s)\n", s.name, skip.reason)
		default:
			failures++
			fmt.Printf("FAIL %s: %v\n", s.name, err)
		}
	}
	passed := len(scenarios) - failures - skips
	if failures > 0 {
		fmt.Printf("RESULT: FAIL (%d/%d passed, %d skipped)\n", passed, len(scenarios), skips)
		os.Exit(1)
	}
	fmt.Printf("RESULT: PASS (%d/%d passed, %d skipped)\n", passed, len(scenarios), skips)
}

// expectFound asserts a Found verdict carrying the wanted outcome and a
// correlation id. The verdict set is open — an unrecognized verdict is a real
// finding here, not a pass.
func expectFound(verdict revaly.ReconcileVerdict, want revaly.TransactionOutcome) (string, error) {
	switch v := verdict.(type) {
	case *revaly.Found:
		if v.Outcome != want {
			return "", fmt.Errorf("expected outcome %q, got %q", want, v.Outcome)
		}
		if v.CorrelationID == "" {
			return "", errors.New("no X-Correlation-ID on the Found verdict (DX §c)")
		}
		return fmt.Sprintf(" (outcome=%s correlation=%s)", v.Outcome, v.CorrelationID), nil
	case *revaly.NotFoundYet:
		return "", fmt.Errorf("charge not visible after %d attempts (%s) — expected Found", v.Attempts, v.Elapsed)
	default:
		return "", fmt.Errorf("unrecognized verdict %T", verdict)
	}
}

// classified renders an unexpected failure values-free: typed classes print
// their runtime-crafted message (status, code, correlation — never payloads,
// never the target host); anything else prints its type only, so transport
// error chains cannot leak endpoint details into CI logs.
func classified(context string, err error) error {
	var pr *revaly.PermanentRejection
	var tf *revaly.TransientFailure
	var ou *revaly.OutcomeUnknown
	if errors.As(err, &pr) || errors.As(err, &tf) || errors.As(err, &ou) {
		return fmt.Errorf("%s, got: %v", context, err)
	}
	return fmt.Errorf("%s, got %T", context, err)
}

func mustClient(cfg revaly.Config) *revaly.Client {
	client, err := revaly.NewClient(cfg)
	if err != nil {
		fmt.Fprintf(os.Stderr, "smoke: client construction failed: %v\n", err)
		os.Exit(2)
	}
	return client
}

// freshID builds a unique merchantTransactionId (≤ 100 chars) — every
// reconcile scenario uses a fresh one (ADR-SDK-024).
func freshID(label string) string {
	b := make([]byte, 4)
	_, _ = rand.Read(b)
	return fmt.Sprintf("smoke-go-%s-%d-%s", label, time.Now().UnixMilli(), hex.EncodeToString(b))
}
