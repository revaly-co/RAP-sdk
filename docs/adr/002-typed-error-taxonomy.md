# ADR-SDK-002 — Typed Error Taxonomy: HTTP Status + Transport Condition + Scoped Safety Signal

**Status:** Accepted — decided 2026-07-06 (D-2); amended 2026-07-09 by D-7 (ADR-SDK-007); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §5.2, decisions D-2 and D-7 · resolves PRD-057 Open Question 1
**Owner:** SC Eng
**Safety-critical:** yes — this taxonomy is the merchant's failover trigger contract

## Context

The RAP-core `ErrorResponse` body is `{ error: string, details?: <any> }`. There is historically
**no machine-readable error code** — callers can only key off HTTP status. (`details` is
deliberately typeless: the runtime truth is any JSON kind or a raw string; the SDK must treat it as
opaque and must never re-type it.)

Verified platform facts the taxonomy must respect (validated against the platform service's main
branch on 2026-07-09; provenance appendix in `../decision-log.md`):

1. **A bare 503 is ambiguous.** The platform maps upstream 502/504/503 (returned *after* gateway
   attempts, which its resilience layer retries on 5xx) and the circuit-breaker-open case to the
   same 503 with the same `ErrorResponse` shape. "Never reached a gateway" and "outcome unknown"
   are indistinguishable on the wire without the P-1 safety signal.
2. **502/504 can also originate at the edge** (Front Door / WAF), before or after the request
   reached the platform — their classification is assumed until OQ-11 verifies edge behaviour
   (hard pre-GA gate).

## Problem

The merchant's failover decision needs a reliable classification of every failure: *can I route
this payment to my own gateway right now, or might RAP-core already have charged the cardholder?*
PRD-057's own framing ("transient = 503, timeout") is unsafe: a timeout after send, and a bare 503,
may both wrap an approved charge. Blind failover on those risks a **double charge**.

## Decision

V1 typed errors key off **HTTP status + transport condition + one scoped safety signal**
(`ErrorResponse.code`, ADR-SDK-007). Three classes:

| Error class | Trigger | Payment state at RAP-core | Caller action |
| --- | --- | --- | --- |
| **PermanentRejection** | HTTP 400 / 401 / 403 / 404 / 422 | Request received and rejected | Fix or decline. **Never fail over** — the same request will fail anywhere. |
| **TransientFailure** *(safe to fail over)* | Connection refused, DNS/TLS failure **before the request was accepted** (client-provable never-sent); **503 carrying `code: not_processed`** (circuit-open fast-fail, P-1) | **Definitively not processed** | Route to own gateway immediately — the PRD's first-layer failover path. |
| **OutcomeUnknown** | Deadline exceeded after send; connection reset mid-flight; 500; 502/504 (edge); **503 without** `code: not_processed` | **May have been processed** | Reconcile before acting (ADR-SDK-003/009). |

Supporting rules:

- `ErrorResponse.error` is carried as the human-readable message — **never parsed or matched on**;
  message strings are not contract.
- `ErrorResponse.details` is passed through untouched as an opaque value.
- The *full* machine-readable error-code taxonomy is deferred (OQ-2, lands before Wave 2 as a 2.1
  contract refinement); when it lands, SDKs expose it in a **minor** release.
- Unknown/future `code` values must be handled forward-compatibly: an unrecognized code is treated
  as absent (i.e., the 5xx falls into OutcomeUnknown, the conservative class).

## Rationale

- **Only promise what the platform can prove.** "Timeout" is not uniformly safe to fail over — only
  failures where the request provably never reached RAP-core are. A bare 503 is not safe either
  (fact 1 above); the fast-failover class therefore rides on the P-1 `code`, not on status alone.
- The circuit-open case is the dominant "RAP-core is down" mode. With P-1 it fails instantly and
  provably unprocessed — restoring the PRD's immediate-failover promise exactly where merchants
  need it.
- The double-charge analysis is the stronger contract, and was recognized as such in review; the
  PRD deviation is formally accepted on PRD-057 (OQ-14, ADR-SDK-021).

## Alternatives considered

- **PRD-057 literal taxonomy ("transient = 503, timeout" → fail over):** rejected — double-charge
  hazard; both triggers can wrap an approved charge.
- **Wait for the full error-code taxonomy (OQ-2) before shipping:** rejected — blocks V1 on a much
  larger API negotiation; the scoped two-value code is sufficient for the safety decision.
- **Classify on `error` message strings:** rejected — messages are not versioned contract and
  differ per failure path.
- **Client-side heuristics (e.g., retry-then-classify):** rejected — the SDK never resubmits
  (trust boundary, ADR-SDK-004); heuristics cannot prove non-processing.

## Consequences

- V1 ships **only after** the platform emits `ErrorResponse.code` on 5xx (P-1 — ADR-SDK-007;
  platform-side implementation is platform repo ADR 013).
- OQ-11 (verify Front Door / WAF edge behaviour for 502/504/resets against this classification) is
  a **hard pre-GA gate** — until then the edge rows of the table are design assumptions.
- Every typed error carries the request correlation id (DX contract §c) so merchant tickets join
  RAP-core telemetry.
- The mock transport must simulate **all** rows of this table, including 503 + `not_processed` and
  both reconcile outcomes (DX contract §d) — testing a merchant's failover handler is a first-class
  scenario.

## Implementation guidance

Classification algorithm (normative pseudocode; implement idiomatically per language):

```
classify(outcome):
  if transport error and request provably never sent        → TransientFailure
     (connection refused; DNS resolution failure; TLS handshake failure)
  if HTTP status in {400, 401, 403, 404, 422}               → PermanentRejection
  if HTTP status == 503 and body.code == "not_processed"    → TransientFailure
  if HTTP status >= 500                                     → OutcomeUnknown
  if deadline exceeded after send, or connection reset,
     or response unreadable/ambiguous                       → OutcomeUnknown
```

- "Provably never sent" must be established from the transport layer's own error semantics per
  language (e.g., connect-phase vs response-phase errors). When a language's HTTP stack cannot
  distinguish the phase, classify as OutcomeUnknown — never guess toward "safe".
- Deserialize `code` as a plain string and map known values; do not bind it to a closed enum that
  fails on future values (OQ-2 will extend it).
- Expose the three classes as the ecosystem's native error idiom (exceptions / result types / `err`
  returns) per `../runtime-tdd.md`; each error object carries: class, HTTP status (if any),
  `code` (if any), message, opaque `details`, correlation id, and the raw response for escalation.
