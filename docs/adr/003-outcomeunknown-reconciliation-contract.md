# ADR-SDK-003 — OutcomeUnknown as a First-Class State; Reconciliation via `merchantTransactionId`

**Status:** Accepted — decided 2026-07-06 (D-3); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §5.2–5.3, decision D-3 (V1 verdict semantics: D-9 / ADR-SDK-009)
**Owner:** SC Eng
**Safety-critical:** yes — governs the only path that prevents double charges

## Context

A failed `POST /payments` call does not mean the payment didn't happen. Between the merchant's
timeout and RAP-core's internals, a charge may have been approved after the merchant stopped
waiting. If the merchant then routes the same payment to their own gateway, the cardholder is
charged twice.

Existing API surface the contract stands on (no new endpoints needed):

- `merchantTransactionId` is **already required** on every payment request — it is the merchant's
  correlation handle (documented max length 100 on create).
- `GET /transactions/merchant/{merchantTransactionId}` exists and returns the transaction state.

Verified platform facts that shape the V1 semantics (provenance: `../decision-log.md`):

1. **Transaction visibility is asynchronous and unbounded.** Persistence is fire-and-forget after
   the API response (event → service bus → consumer → database); read-your-write lag has no bound
   and is widest exactly when RAP-core is degraded.
2. **Inline retry re-keys attempts.** Platform-side retry attempts > 0 are submitted under a fresh
   ULID, so a payment that succeeded on a retry is *not findable* under the merchant's original
   `merchantTransactionId` (the grouped lookup is not available on the public read path).
3. The create call documents `merchantTransactionId` max length 100, while the reconcile lookup and
   refund-cancel routes historically enforced max 50 — a spec-legal id could 400 exactly on the
   recovery call. Fixed platform-side toward 100 (platform repo ADR 015); the fix rides V1.

## Problem

The SDK must give merchants a deterministic, safe procedure for the OutcomeUnknown class — one that
never turns "I can't see the transaction yet" into "it doesn't exist, fail over".

## Decision

1. **OutcomeUnknown is a first-class state** in the taxonomy (ADR-SDK-002) — not an exception
   detail, not a retry hint. It has its own documented handling procedure.
2. **Reconciliation is the procedure**, standing entirely on existing API surface:
   on OutcomeUnknown, the caller (or the SDK's provided `reconcile` helper) queries
   `GET /transactions/merchant/{merchantTransactionId}`.
   - **Found** → the outcome is known; act on the real transaction state. **No failover if
     approved.**
   - **Not found** → V1: **hold and re-poll** with backoff (ADR-SDK-009). Absence is not yet
     provable (facts 1 and 2). After P-2 lands (ADR-SDK-008), not-found once the reservation window
     closes ⇒ provably never accepted ⇒ safe to fail over.
3. **The SDK never auto-resubmits** a payment and never invokes `bypassPlatform` — second-layer
   recovery stays inside RAP-core; the routing decision belongs to the merchant's system above the
   SDK (trust boundary, ADR-SDK-004).
4. The `reconcile` helper ships as a **first-class, documented pattern** — helper + worked example
   in all six languages, part of the quickstart (DX contract §b), simulated by the mock transport
   (DX contract §d).

## Rationale

- Reconciliation on existing surface means V1 needs **zero new endpoints** — the merchant's
  correlation handle already exists and is mandatory.
- Auto-resubmission inside the SDK would move the double-charge decision into code the merchant
  can't see, against the trust boundary; and until P-2, the platform has no idempotency to make
  resubmission safe.
- Naming OutcomeUnknown as a class (rather than burying it under "transient") is what makes the
  double-charge hazard visible and testable in merchant code.

## Alternatives considered

- **SDK-side auto-resubmit with client-generated idempotency keys:** rejected — no server-side
  idempotency until P-2; violates the SDK's never-resubmit rule; hides a money-moving decision.
- **"Not found after a bounded wait ⇒ safe to fail over" in V1:** rejected — the visibility window
  is unbounded (fact 1) and retry re-keying (fact 2) makes absence unprovable; this is exactly the
  false promise the 2026-07-07 architecture review caught.
- **A new dedicated reconcile endpoint:** rejected for V1 — existing surface suffices; P-2 upgrades
  the *semantics* of the existing GET (pending-state visibility) rather than adding surface.

## Consequences

- The helper's verdict vocabulary in V1 is deliberately `Found(outcome)` / `NotFoundYet` — never a
  "safe to fail over" value (ADR-SDK-009 fixes this as a type-level decision).
- Merchants must implement a hold/escalate policy for sustained NotFoundYet; the SDK documents the
  pattern and its escalation hooks but does not decide it.
- GA (post-P-2) upgrades the same helper with a `SafeToFailover` verdict — designed now for
  forward-compatible extension (see ADR-SDK-009 implementation guidance).
- The id-length spec correction (fact 3) must be live before merchants rely on reconcile with ids
  longer than 50 characters.

## Implementation guidance

- Helper shape (per-language idiom in `../runtime-tdd.md`):
  `reconcile(merchantTransactionId, policy) → Found(transaction) | NotFoundYet`
  where `policy` covers backoff schedule, per-attempt deadline, and overall budget; sensible
  defaults derive from RAP-core latency telemetry (OQ-6, pre-GA).
- The helper re-polls the GET — this is the **only** loop the runtime is allowed to own, and it is
  explicit, bounded by the caller's policy, and side-effect-free (GET only).
- Surface the last-seen HTTP status/correlation id on `NotFoundYet` so merchant escalation tickets
  are actionable.
- The worked example in every quickstart must show: OutcomeUnknown caught → reconcile → all three
  outcomes handled (`Found(approved)` → done; `Found(declined)` → merchant decision; `NotFoundYet`
  sustained → hold + escalate). Failover on `NotFoundYet` must appear **only** in the post-P-2
  (GA) variant of the example.
