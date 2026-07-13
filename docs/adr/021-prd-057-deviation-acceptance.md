# ADR-SDK-021 — PRD-057 "Typed Errors" and "Transient = 503, Timeout" Musts Are Resolved via Formal Deviation Acceptance

**Status:** Accepted — decided 2026-07-10 (OQ-14, Charles): resolve via formal deviation acceptance recorded on PRD-057; the RFC approval was given ahead of that recording by explicit approver decision, with the acceptance a tracked Product follow-up
**Source:** RFC-046 §11 OQ-14 / §12 sequencing note · inline review thread (PRD gate rule, 2026-07-08)
**Owner:** Product (recording); SC Eng (contract)

## Context

Two PRD-057 Musts are deviated from by the approved design:

1. **"Surface HTTP errors as typed errors"** — assumed a machine-readable error code existed on
   `ErrorResponse`. Verification showed none did. The deviation is now *narrowed* by D-7: the
   scoped two-value `ErrorResponse.code` (ADR-SDK-007) restores a machine-readable **safety**
   signal in V1; the full taxonomy remains deferred to OQ-2 (before Wave 2).
2. **"Surface a transient failure immediately", defining transient as "503, timeout"** —
   **superseded** by the §5.2 taxonomy (ADR-SDK-002): timeout-after-send is OutcomeUnknown
   (reconcile before acting), and even a bare 503 is not uniformly safe (the platform's 503
   conflation). Implementing the PRD's literal definition would ship a double-charge hazard.

The pipeline's RFC-gate rule says: when an RFC surfaces a gap or contradiction in the PRD, the PRD
is updated before the RFC is adopted.

## Problem

Reconcile an approved RFC with a PRD whose literal Musts it deliberately — and for safety reasons —
does not implement, without leaving implementers two contradictory sources of truth.

## Decision

- The deviations are resolved by **formal deviation acceptance recorded on PRD-057** by Product
  (not by silently rewording the Musts).
- The 2026-07-10 RFC approval was **explicitly given ahead of that recording** by approver
  decision; the recording is a **tracked follow-up** (see §12 notes, RFC header, and
  `../open-items.md`).
- **For implementers, the RFC taxonomy is authoritative.** Do not implement PRD-057's literal
  "transient = 503, timeout" trigger under any circumstance — it is superseded as unsafe.

## Rationale

- The double-charge analysis is the stronger contract, and the review itself judged it so; the
  deviation path exists precisely for the case where design verification proves a PRD assumption
  wrong.
- Recording acceptance on the PRD (rather than editing history) preserves the audit trail of *why*
  the product requirement changed.

## Alternatives considered

- **Amend the PRD Musts textually before approval:** the original ask; the approver chose the
  deviation-acceptance route with approval proceeding first — same end state, explicit ownership.
- **Implement the PRD as written:** rejected — ships a known double-charge hazard.
- **Leave the contradiction undocumented:** rejected — guarantees a future implementer or auditor
  "fixes" the SDK back to the unsafe behaviour.

## Consequences

- Until Product records the acceptance, PRD-057 read alone **misstates the failover contract** —
  anyone onboarding from the PRD must be routed to the RFC/this ADR set (the PRD page carries the
  RFC link; the acceptance recording closes the loop).
- OQ-2's future full taxonomy further shrinks deviation 1; it does not reopen deviation 2.
- The DX contract's quickstart examples are the practical enforcement: they demonstrate the safe
  taxonomy, and merchants copy examples, not PRDs.

## Implementation guidance

- Track the recording as a Product-owned item with a deadline in `../open-items.md`; verify
  it before Wave-1 GA announcements reference the PRD.
- Any future PRD-057 edits touching error semantics must cross-check ADR-SDK-002/007/009 — add
  that note to the acceptance recording itself.
