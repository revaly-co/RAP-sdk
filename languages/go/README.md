# Revaly SDK for Go

Server-side Go SDK for the RAP V2 payment API (`api.revaly.co`). One module:
the hand-written runtime (this package) wraps a generated core, and every
failure you can see is one of **three typed classes** that tell you exactly
what is safe to do next — the merchant-facing failover contract this SDK
exists to implement.

```
github.com/revaly-co/rap-sdk/languages/go          ← import this (package revaly)
github.com/revaly-co/rap-sdk/languages/go/core     ← generated core (full V2 surface)
github.com/revaly-co/rap-sdk/languages/go/raptest  ← mock transport for your tests
```

> **Install:**
>
> ```bash
> go get github.com/revaly-co/rap-sdk/languages/go@latest
> ```
>
> Module-form releases are `languages/go/vX.Y.Z` tags, served via the Go module
> proxy / pkg.go.dev. The source tree between releases carries the placeholder
> version `0.0.0-dev`; per-language GitHub release artifacts (module zip +
> `.sha256` + `provenance.json`) remain the provenance anchor and fallback
> channel. The supported Go floor is **go 1.21** (the `go.mod` directive).

## Why this SDK is different: the failover contract

A failed `POST /payments` does **not** mean the payment didn't happen. If your
code blind-fails-over to your own gateway on an ambiguous failure, the
cardholder can be charged twice. Every operation therefore returns either a
result or exactly one of:

| Class | Meaning | Your action |
| --- | --- | --- |
| `*revaly.PermanentRejection` | Received and rejected (HTTP 400/401/403/404/422) | Fix or decline — failing over reproduces the same rejection anywhere. |
| `*revaly.TransientFailure` | **Definitively not processed** (provably never sent, or 503 with `code: not_processed`) | Route to your own gateway immediately. |
| `*revaly.OutcomeUnknown` | **May have been processed** (deadline after send, reset mid-flight, other 5xx) | **Reconcile before acting** (below). |

Classification rests on the error **type** and HTTP status alone — message text
and latency are reported to you and excluded from the verdict. Dispatch with
`errors.As`; the class is the whole contract.

## Quickstart (sandbox key → first charge)

Sandbox and live share `https://api.revaly.co` — the environment is selected
by your API key's scope, not by a URL. With your Enablement-issued sandbox key
in hand:

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"time"

	revaly "github.com/revaly-co/rap-sdk/languages/go"
)

func main() {
	client, err := revaly.NewClient(revaly.Config{
		APIKey: "YOUR_SANDBOX_API_KEY",
		// Timeouts are deliberately not set: unset (zero) applies the ratified
		// defaults — the 75 s overall deadline (ADR-SDK-027) and the 10 s
		// connect timeout (ADR-SDK-029; a connect-phase expiry is provably
		// never-sent → TransientFailure). revaly.NoOverallDeadline /
		// revaly.NoConnectTimeout disable them.
	})
	if err != nil {
		log.Fatal(err)
	}

	// merchantTransactionId is required — it is YOUR reconcile key. Use your
	// order/attempt id; you will look the payment up by it if the outcome is
	// ever unknown.
	request := revaly.NewPaymentRequest(1099, "order-0001-attempt-1")
	// orderId + email: the sandbox simulator requires both for an approval.
	request.SetOrderId("order-0001")
	card := revaly.NewCreditCard("4111111111111111", "12", "2030") // sandbox test card
	card.SetCardVerificationCode("123")
	method := revaly.NewPaymentMethod()
	method.SetFullName("Ada Lovelace") // creditCard requires a cardholder name
	method.SetEmail("ada@example.com")
	method.SetCreditCard(*card)
	// paymentMethodType is omitted — inferred from the one populated method object.
	request.SetPaymentMethod(*method)

	transaction, err := client.Charge(context.Background(), request)
	if err == nil {
		fmt.Println("approved:", transaction.GetTransactionId())
		return
	}

	// Handle ALL THREE classes — this switch IS the failover contract.
	var rejection *revaly.PermanentRejection
	var transient *revaly.TransientFailure
	var unknown *revaly.OutcomeUnknown
	switch {
	case errors.As(err, &rejection):
		// Received and rejected. Fix the request or decline the order.
		fmt.Println("rejected:", rejection.APIError, "correlation:", rejection.CorrelationID)

	case errors.As(err, &transient):
		// Provably not processed — this is your fast-failover signal.
		fmt.Println("not processed — safe to route to your own gateway now")

	case errors.As(err, &unknown):
		// The payment MAY exist. Reconcile before doing anything else.
		reconcileBeforeActing(client, "order-0001-attempt-1")

	default:
		// Programming errors (validation, nil contexts) — not wire outcomes.
		log.Fatal(err)
	}
}

func reconcileBeforeActing(client *revaly.Client, merchantTransactionID string) {
	verdict, err := client.Reconcile(context.Background(), merchantTransactionID,
		revaly.ReconcilePolicy{
			MaxAttempts:   5,
			OverallBudget: 30 * time.Second, // bound by YOUR checkout's risk policy
			InitialDelay:  1 * time.Second,  // doubles each attempt, ±20% jitter
		})
	if err != nil {
		// A rejected read (bad key, malformed id) or a cancelled context —
		// escalate; polling cannot fix these.
		log.Fatal(err)
	}

	// The verdict set is OPEN by design: SafeToFailover arrives with a minor
	// release once the platform can prove absence. ALWAYS keep the default
	// branch.
	switch v := verdict.(type) {
	case *revaly.Found:
		switch v.Outcome {
		case revaly.TransactionOutcomeApproved:
			fmt.Println("payment already succeeded — failing over would double-charge")
		case revaly.TransactionOutcomeDeclined, revaly.TransactionOutcomeError:
			fmt.Println("terminal failure at RAP — your own gateway is now safe")
		case revaly.TransactionOutcomePending:
			fmt.Println("platform holds a pending intent — keep polling")
		default:
			fmt.Println("record sighted but not readable by this SDK version — treat as found; do not fail over")
		}
	case *revaly.NotFoundYet:
		// Absence is NOT provable in V1 — hold and escalate per your policy.
		fmt.Printf("not visible yet after %d attempts (%s) — hold, do not fail over blind\n",
			v.Attempts, v.Elapsed)
	default:
		// Future verdicts (e.g. SafeToFailover) land here on older SDKs.
		fmt.Println("unrecognized verdict — treat conservatively; upgrade the SDK")
	}
}
```

## Configuration

| Field | Default | Notes |
| --- | --- | --- |
| `APIKey` | — required | Injected per request at the transport; never logged, never in errors |
| `BaseURL` | `https://api.revaly.co` | Sandbox and live share it (key-scoped); override only for internal targets |
| `APIVersion` | `"2.1"` | Pinned via `X-Api-Version` on every request. On `"2.0"` the `code` field is not part of the documented contract, so 503 + `not_processed` classifies **OutcomeUnknown** — fast failover narrows to provable never-sent failures |
| `ConnectTimeout` | 10 s (ADR-SDK-029) | Maps to `net.Dialer.Timeout`; the bound makes connect-phase expiries **provably never-sent** (`TransientFailure`). Zero applies the edge-ratified default; `revaly.NoConnectTimeout` disables it (stdlib dial defaults) |
| `OverallDeadline` | 75 s (ADR-SDK-027) | Per-call context timeout; expiry **after send** is `OutcomeUnknown`, never `TransientFailure`. Zero applies the telemetry-ratified default; `revaly.NoOverallDeadline` disables it |
| `Logger` | discard | `*slog.Logger`; output is values-free at every level |
| `WireTrace` | off | Scrubbed request/response observer for support escalations |
| `Transport` | real HTTP | The mock-transport injection point (named for `http.Client.Transport` — the cross-language `transport` key) |
| `HTTPClient` | — | Advanced: its `Transport` is used (ignored when `Transport` is set); redirects are always disabled by the runtime |

Cancellation is idiomatic Go: every operation takes a `context.Context`, and
`Reconcile` additionally enforces its caller-bounded policy budget.

### Design guarantees

- **Each charge is sent exactly once.** Redirects stay off (the runtime overrides the
  stdlib default), so a `307` on `POST /payments` arrives as a response to classify
  rather than a re-POST that resubmits a payment.
- **Every call stands alone** — no cross-request state, no circuit breaker, so
  behaviour under load is the behaviour you tested.
- **The reconcile re-poll you bound is the only loop the runtime owns.**
- **Classification rests on evidence only**: HTTP status and `ErrorResponse.code`.
  Message text and latency are reported to you and excluded from the verdict.
- **Recovery beyond this boundary belongs to RAP-core** — resubmission and
  `bypassPlatform` are platform-internal, so a payment's outcome stays unambiguous.

Normative form: [`docs/failover-contract.md`](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-contract.md) §5 and
Appendix A.

## Testing your failover handler (no network)

The mock transport replaces only the transport — header injection and
classification still run, so your tests exercise the same safety code as
production. It ships in the companion package
`github.com/revaly-co/rap-sdk/languages/go/raptest`:

```go
mock := raptest.NewMockTransport()
client, _ := revaly.NewClient(revaly.Config{APIKey: "sk_test_synthetic", Transport: mock})

// Script the §2 taxonomy — consecutive calls script consecutive outcomes:
mock.Charge().ReturnsNotProcessed503()          // → *TransientFailure (fast failover)
mock.Reconcile("order-1").ReturnsNotFound().ReturnsFoundApproved()

// ... drive your handler and assert its decisions ...

if err := mock.RequireUserAgent(); err != nil { t.Fatal(err) } // UA contract held
```

Scriptable rows: `ReturnsApproved`, `ReturnsDeclined`,
`ReturnsPermanentRejection(status)`, `ReturnsNotProcessed503`,
`ReturnsBare503`, `Returns500/502/504`, `FailsBeforeSend` (dial-phase error
instance), `TimesOutAfterSend`, `ResetsMidFlight`, and for reconcile:
`ReturnsFoundApproved/Declined`, `ReturnsPending`, `ReturnsNotFound`. Mock
data is synthetic only.

## Debuggability

- Every response and every typed error carries the `X-Correlation-ID` —
  quote it to support and it joins platform telemetry directly.
- Logs are **values-free at every level** (a PCI obligation, enforced by CI
  log-capture tests): identifiers and statuses only, payload values never.
- The wire-trace hook receives request/response events scrubbed by a central
  allowlist before your code sees them.
- Calls made directly against the generated core (`…/languages/go/core`)
  return the generator's `GenericOpenAPIError`, whose `Error()` string can
  embed response-body content (and `.Body()` returns it raw). Response bodies
  can contain PII (names, emails, masked card data) — never log raw core
  errors or bodies; log the correlation id and the typed `revaly.*` errors
  (values-free by design) instead.

## Support policy

- **Supported:** current + previous minor, per package.
- Deprecations are announced in release notes and registry deprecation
  metadata; every major ships a published migration guide.
- A yanked release is announced together with its patched replacement.
- Security patches go to the latest GA of every supported major.
- `X-Api-Version: 2.0` pinning support follows the platform's API deprecation
  policy.

Vulnerability reports: see `SECURITY.md` at the repository root (added before
the repository goes public).

## Idiom notes (pre-GA review — ADR-SDK-028)

Reviewed and ratified by the experienced-Go pre-GA review (dx-contract §a;
ADR-SDK-028): the root-package re-export (`package revaly` at the module root,
internals fenced under `internal/runtime/`), pointer request parameters on the
payment operations, `time.Duration` for all bounds, pointer-typed error
classes dispatched via `errors.As`, the sealed-interface verdict pattern with
a mandatory default branch, and the `raptest` companion-package name (now at
the module root, outside the internal fence).

## Where to go next

- [Failover cookbook](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-cookbook.md) — recipes for each outcome, choosing a
  reconcile policy, testing offline, debugging with correlation ids.
- [Failover contract](https://github.com/revaly-co/RAP-sdk/blob/main/docs/failover-contract.md) — the normative specification, with
  sequence diagrams and the verbatim prohibitions in Appendix A.
- [AGENTS.md](https://github.com/revaly-co/RAP-sdk/blob/main/AGENTS.md) — the whole contract on one page, for AI coding agents.
- [Support](https://github.com/revaly-co/RAP-sdk/blob/main/SUPPORT.md) · [Contributing](https://github.com/revaly-co/RAP-sdk/blob/main/CONTRIBUTING.md) · [Security](https://github.com/revaly-co/RAP-sdk/blob/main/SECURITY.md)
