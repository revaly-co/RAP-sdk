# ADR-SDK-009 — V1 Reconcile Verdict Is "Hold and Re-Poll"; `SafeToFailover` Enters the API Only with P-2

**Status:** Accepted — decided 2026-07-09 (D-9); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §5.3, decision D-9
**Owner:** SC Eng
**Safety-critical:** yes — encodes the double-charge safety analysis into the type system

## Context

ADR-SDK-003 fixes reconciliation as the OutcomeUnknown procedure; ADR-SDK-008 explains why absence
is unprovable until the platform's intent reservation (P-2) ships. Between V1 and GA there is a
window in which the API *could* tempt implementers and merchants into treating "not found" as "safe
to fail over" — the exact false promise the 2026-07-07 architecture review caught in the original
draft.

## Problem

Contract wording is not enough. If the V1 helper exposes any value naming "safe", some merchant
code path will act on it. The safety analysis must be carried by the API shape itself.

## Decision

- The V1 reconcile helper returns exactly two verdicts: **`Found(outcome)`** or **`NotFoundYet`** —
  deliberately **never** a `SafeToFailover` value. That value **enters the API only when P-2 makes
  it true**.
- All V1 documentation, quickstarts, and examples word the not-found path as **hold and re-poll**
  with backoff, escalating per merchant policy. The merchant-facing promise says "safe" only where
  the platform can prove it.
- At GA (post-P-2), `SafeToFailover` is added as a third verdict in a **minor** release, together
  with the pending-state modelling from ADR-SDK-008.

## Rationale

- **The name `NotFoundYet` is the design.** It states the platform's actual knowledge ("not visible
  *yet*") instead of the tempting misreading ("doesn't exist"). Type systems propagate this into
  merchant code better than any doc warning.
- **Absence of the unsafe value is stronger than a caveat on it.** A `SafeToFailover` variant with
  a "don't use before GA" note would still compile, still autocomplete, and still get used.
- The merchant-facing promise is the product; shipping a promise the platform cannot keep converts
  a double-charge hazard into an SDK defect.

## Alternatives considered

- **Return `NotFound` + documentation caveat:** rejected — foot-gun; developers reliably treat
  `NotFound` as absence.
- **Config flag (`assumeSafeAfterSeconds`):** rejected — unsound; no client-side wait length makes
  absence provable (ADR-SDK-008 context).
- **Ship `SafeToFailover` disabled/reserved in V1:** rejected — reserved-but-visible API is the
  caveat problem in different clothes.

## Consequences

- Merchants needing V1 failover on sustained `NotFoundYet` must make that call in **their** code,
  above the SDK, against their own risk policy — the SDK does not bless it. The docs state this
  explicitly and show the escalation hook.
- Adding a verdict at GA must not break existing merchant code — this constrains how the verdict
  type is designed **now** (see guidance).
- Quickstart examples (DX contract §b) branch three ways in V1: `Found(approved)` → done;
  `Found(declined/other terminal)` → merchant decision; `NotFoundYet` sustained → hold + escalate.

## Implementation guidance

- **Design the verdict type as open for extension in every language**, so `SafeToFailover` lands as
  a *minor* release:
  - languages with exhaustive matching (Go, TypeScript discriminated unions, Java sealed
    interfaces, .NET, PHP enums): expose the verdict as a non-exhaustive construct — e.g., a
    sealed/abstract base with documented "future verdicts will be added; always include a default
    branch", or an enum + explicit `Unknown` guidance, per ecosystem norms captured in
    `../runtime-tdd.md`;
  - lint/document the default-branch requirement in every quickstart example (the examples are
    what merchants copy).
- `NotFoundYet` carries: attempts made, elapsed time, last correlation id, last HTTP status — the
  escalation payload.
- `Found` carries the full transaction state (terminal outcome vs — post-P-2 — pending intent, as
  distinct variants per ADR-SDK-008).
- The helper's polling policy (backoff, per-attempt deadline, overall budget) is caller-provided
  with telemetry-derived defaults (OQ-6); the helper must be side-effect-free (GET only) and
  cancellable per language idiom.
