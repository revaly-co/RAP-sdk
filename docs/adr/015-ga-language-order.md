# ADR-SDK-015 — GA Investment Order: .NET → Java → PHP → TypeScript → Python → Go; All Six Cores Generated from Day One

**Status:** Accepted — decided 2026-07-10 (OQ-5, Charles); ratified with RFC-046 approval 2026-07-10. Supersedes the RFC's original Wave-1 composition proposal (TS + PHP + .NET) and the pipeline-data validation step.
**Source:** RFC-046 §3.3 (as amended 2026-07-10) / §11 OQ-5
**Owner:** Product + Enablement (order); SC Eng (execution)

## Context

All six language cores (Python, TypeScript, Go, .NET, PHP, Java) are **generated, compiled, and
contract-tested in CI from day one** — no language ever starts from scratch later. What the order
controls is where the squad invests the hand-written runtime, docs polish, per-language GA
checklist (DX contract §a), and GA hardening. The RFC originally proposed Wave 1 = TypeScript +
PHP + .NET, subject to validation against merchant pipeline data (the original OQ-5).

## Problem

Fix the GA sequencing so beta partner selection, runtime staffing, and per-language sign-offs can
be planned — without re-opening the debate per wave.

## Decision

GA investment order (decided by Charles, 2026-07-10):

1. **.NET** — first, and **dogfooded internally**: the platform organization is a .NET shop, so
   the .NET SDK becomes the client of the platform's own E2E tests, validating ergonomics and the
   failover contract before any merchant sees them.
2. **Java**
3. **PHP**
4. **TypeScript**
5. **Python**
6. **Go**

This order **supersedes** the wave-composition proposal and the merchant-pipeline-data validation
step. The PRD's six-language Must stays satisfied structurally (all six cores exist and are
CI-green from day one).

## Rationale

- .NET-first converts internal E2E infrastructure into the first consumer — the cheapest honest
  ergonomics validation available (with the explicit caveat, kept from the DX contract, that
  dogfooding validates *our* ergonomics, not merchants' — the design-partner beta still precedes
  each GA).
- The decided order front-loads the enterprise server stacks and defers Go, whose distribution
  binding (module path permanence, ADR-SDK-022) also makes it the language that most benefits from
  a settled namespace and mature pipeline.

## Alternatives considered

- **Original proposal (TS + PHP + .NET wave, then data-validated):** superseded by the approver's
  direct call — the decision replaces the data-gathering step entirely.
- **All six GA simultaneously:** rejected from the start — PRD itself rates six-language scope
  High risk; GA requires a per-language idiomatic sign-off that doesn't parallelize across one
  squad.

## Consequences

- Design-partner beta merchants (DX contract §f) are recruited to match the earliest GA languages
  (.NET/Java/PHP first).
- The per-language GA checklist sign-offs happen in this order; an experienced developer in each
  language signs before that language ships (DX contract §a).
- Go's late position means its module path is published only after the namespace and pipeline are
  fully settled — reducing the highest-permanence risk (ADR-SDK-022).
- Docs/quickstart polish follows the same order; all six quickstarts exist from the start (they are
  CI-tested), but DX-bar polish lands in GA order.

## Implementation guidance

- CI treats all six languages identically at every stage (generate/build/test/contract-smoke) —
  "GA order" gates only the publish stage's 1.0 designation and the DX sign-off checklist.
- Pre-1.0 betas may publish for languages ahead of their GA slot (per ADR-SDK-013 mechanics and
  ADR-SDK-022 namespace gate) to feed the design-partner beta.
