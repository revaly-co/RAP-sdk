# ADR-SDK-008 — GA Failover Proof: Synchronous Intent Reservation + `merchantTransactionId` Idempotency (P-2)

**Status:** Accepted — decided 2026-07-09 (D-8, promoting OQ-10 to GA blocker); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §5.4 (P-2), decision D-8 · 2026-07-07 architecture review
**Owner:** SC Eng (API owners) — platform-side implementation: platform repo ADR 014; detailed schema design in Epic SC-234
**Blocks:** SDK GA (the `SafeToFailover` reconcile verdict)

## Context

Two verified platform facts make "not found ⇒ never accepted" **unprovable** in V1
(ADR-SDK-003):

1. transaction visibility is asynchronous with no bound (fire-and-forget persistence pipeline),
   widest exactly when RAP-core is degraded;
2. platform-side inline retry re-keys attempts > 0 under a fresh ULID, so a payment that succeeded
   on a retry is not findable under the merchant's original `merchantTransactionId`.

The GA-level merchant promise — *"not found once the reservation window closes ⇒ provably never
accepted ⇒ safe to fail over"* — therefore requires server-side work. The 2026-07-07 review
promoted this from an open question (OQ-10) to a **GA blocker**.

## Problem

The reconcile contract needs a platform mechanism that (a) makes absence provable, (b) bounds the
reconciliation window, and (c) dedupes replays of the same merchant transaction.

## Decision

SDK GA **blocks on** the platform shipping P-2:

- **Per-account uniqueness + idempotency on `merchantTransactionId`**, implemented as a
  **synchronous intent reservation**: a reservation row is written in the request path **before
  gateway dispatch** (state `received` → terminal states), in the platform's primary database.
- The reservation is **surfaced through the existing** `GET /transactions/merchant/{id}` as a
  pending state — read-your-write becomes immediate for intent, even while full transaction
  visibility remains asynchronous.
- **Inline-retry provenance fix:** platform retry attempts stay anchored to the original
  `merchantTransactionId`; retry ULIDs remain platform/gateway-side only. A payment that succeeds
  on a retry is findable under the merchant's id.
- **Failure semantics (named trade-off):** the reservation write joins the payment hot path. If the
  reservation cannot be written, the platform **rejects fast with `code: not_processed`** — safe by
  construction, handing the merchant an immediate, clean failover signal exactly when RAP-core is
  degraded.
- Platform NFR gates before GA: capacity/latency sizing of the hot-path write plus a load test.

Post-P-2 SDK semantics: reconcile's *not found* after the reservation window closes becomes
**provably never accepted** ⇒ the helper may return `SafeToFailover` (ADR-SDK-009).

## Rationale

- **Reservation at the request path is the only place absence can be proven.** Any read-side
  bounding (wait N seconds, then trust absence) inherits the unbounded pipeline (fact 1) and the
  re-keying hole (fact 2). Writing intent synchronously before dispatch closes both.
- **Reject-fast-on-write-failure inverts the degradation story safely:** the platform being too
  degraded to record intent is exactly when the merchant should fail over — and `not_processed` is
  then *true by construction* (nothing was dispatched).
- Idempotency on the merchant's existing required key adds replay protection without new request
  fields.

## Alternatives considered

- **Bounded-visibility promise without reservation ("not found after X seconds is safe"):**
  rejected — X does not exist; the persistence pipeline has no bound and degrades with the
  platform.
- **Client-generated idempotency-key header (Stripe-style) instead of reusing
  `merchantTransactionId`:** rejected — `merchantTransactionId` is already required, already the
  merchant's correlation handle, and already what the reconcile GET keys on; a second key splits
  the identity the contract depends on.
- **Asynchronous reservation (event-driven):** rejected — reintroduces the visibility gap the
  reservation exists to close.

## Consequences

- GA is sequenced: platform P-2 deployed + NFR/load-test gates passed → `SafeToFailover` verdict
  enabled in SDKs (minor release per ADR-SDK-009's forward-compatible verdict design).
- Until P-2, all SDK documentation and examples must say **hold and re-poll** — never "safe after
  a wait" (ADR-SDK-009).
- Duplicate submissions with the same `merchantTransactionId` on the same account become
  deterministic (idempotent) rather than double-charges — the SDK documents this as a platform
  guarantee **only after** P-2 ships.
- One new platform capability the SDK's GET handling must model: transaction lookups may now return
  a **pending/reservation state** distinct from a completed transaction; the reconcile helper's
  `Found(outcome)` must distinguish terminal outcomes from pending intent.

## Implementation guidance

- Do **not** infer P-2's presence from observed behaviour. The capability arrives as a platform
  release coordinated with an SDK minor release; gate the `SafeToFailover` code path on an explicit
  SDK-side switch tied to the platform rollout (mechanism finalized in Epic SC-234 — e.g., minimum
  platform API version advertised via the existing supported-versions surface).
- Model the pending state as a distinct, explicit variant in the reconcile result (not a synthetic
  "found with null outcome").
- The reservation window's closing rule (when absence becomes provable) is defined by the platform
  epic; the SDK treats it as an opaque platform guarantee surfaced through the GET — do not
  re-implement window math client-side.
- Mock transport: add scripted scenarios for pending-then-terminal and pending-then-absent
  (post-window) so merchants can test both GA paths (DX contract §d).
