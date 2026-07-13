# ADR-SDK-007 — V1 Fast-Failover Signal: `ErrorResponse.code` (`not_processed` | `outcome_unknown`)

**Status:** Accepted — decided 2026-07-09 (D-7, promoting review finding to V1 prerequisite P-1); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §5.4 (P-1), decision D-7 · 2026-07-07 architecture review (footer thread)
**Owner:** SC Eng (API owners) — platform-side implementation: platform repo ADR 013
**Blocks:** SDK V1 release

## Context

The 2026-07-07 architecture review verified in platform code that **a bare 503 is ambiguous on the
wire**: the platform maps upstream 502/504/503 (returned after gateway attempts, which its
resilience layer retries on 5xx) and the circuit-breaker-open case to the **same 503 with the same
`ErrorResponse` shape**. "Never reached a gateway" and "outcome unknown" are indistinguishable to
any client.

That breaks the PRD's first-layer failover promise at its most important point: the breaker-open
case is the dominant "RAP-core is down" mode, and it is exactly the case where the merchant should
fail over *immediately* — but without a signal, the SDK must treat every 503 as OutcomeUnknown and
force a reconcile (ADR-SDK-002/003), adding latency exactly when the merchant most needs speed.

## Problem

Give the SDK a **provable** "this payment was definitively not processed" signal on 5xx responses,
with the smallest possible API change and no behavioural change for existing callers.

## Decision

SDK V1 **blocks on** the platform shipping P-1:

- `ErrorResponse` gains an **additive** field `code` with exactly two values in V1:
  `not_processed` | `outcome_unknown`, emitted **on every 5xx response**.
- **Emission is conservative and provable:** only circuit-open (request never dispatched) and
  pre-dispatch rejections emit `not_processed`. Anything after dispatch — upstream 502/503/504,
  timeouts — emits `outcome_unknown`. When in doubt, `outcome_unknown`.
- The field is response-only, additive, requires no migration, and is documented under
  `X-Api-Version: 2.1` (the SDK's default pin).
- SDK classification (normative): `503 + code=not_processed` → **TransientFailure** (immediate
  failover); any 5xx otherwise (including `code` absent or unrecognized) → **OutcomeUnknown**.

The *full* machine-readable error-code taxonomy remains deferred (OQ-2, before Wave 2); this ADR
covers only the two-value safety binary.

## Rationale

- **Provability over completeness.** The two-value code is the smallest change that restores the
  immediate-failover path where the platform can actually prove non-processing. A rich taxonomy
  (OQ-2) is a contract-design negotiation; the safety binary is not.
- **Conservative emission protects the cardholder.** A false `not_processed` is the only dangerous
  error (it licenses failover on a possibly-approved charge), so the emission rule is anchored to
  dispatch: no dispatch happened ⇒ and only then ⇒ `not_processed`.
- Riding the existing `ErrorResponse` body (not a header) keeps the signal inside the versioned,
  spec-described error contract that generators and typed clients already model.

## Alternatives considered

- **Status-only classification (no server change):** rejected — leaves every 503 as
  OutcomeUnknown, permanently degrading the headline failover scenario to reconcile-first.
- **A response header (e.g., `X-Payment-State`):** rejected — outside the spec-described error
  model, easier for intermediaries to strip, invisible to generated clients.
- **Full error-code taxonomy now (OQ-2):** rejected — much larger surface negotiation; would delay
  V1 for information the failover decision doesn't need.
- **SDK heuristics (e.g., latency-based inference of breaker state):** rejected — guesses, not
  proofs; violates "only promise what the platform can prove".

## Consequences

- The SDK pins `X-Api-Version: 2.1` by default (configurable down to `2.0`, where the `code`
  field is not part of the documented contract and the SDK's fast-failover class narrows to
  client-provable never-sent failures only — document this behavioural difference prominently).
- V1 release order is fixed: platform P-1 deployed → contract-smoke verifies `code` emission →
  SDK V1 can GA.
- The mock transport must simulate `503 + not_processed` (fast-failover path) and 5xx with
  `outcome_unknown`/absent code (reconcile path) — DX contract §d.
- P-2 (ADR-SDK-008) reuses this signal: a failed intent-reservation write rejects fast **as**
  `not_processed`, keeping the degraded-mode contract coherent.

## Implementation guidance

- Parse `code` as an open string field (OQ-2 will add values); map exactly the two known values;
  treat anything else as absent → OutcomeUnknown.
- Never derive the class from `error` message text; `details` stays opaque (ADR-SDK-002).
- Expose `code` verbatim on the typed error object (merchants may log/alert on it), alongside the
  derived class.
- Contract-smoke (pipeline stage 4) must include one forced-`not_processed` scenario against
  Sandbox once the platform exposes a deterministic trigger for it; until then, assert emission
  shape on 5xx via the platform's contract suite evidence (platform repo ADR 017).
