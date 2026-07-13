# ADR-SDK-017 — Explicitly Decoupled from the RTN SDK Initiative (PRD-049)

**Status:** Accepted — decided 2026-07-10 (OQ-8, Charles); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §3 dependency map / §11 OQ-8
**Owner:** SC Eng + RTN squad

## Context

A second SDK initiative exists: the RTN SDK (PRD-049), for the RTN Relay API — a separate product
surface owned by a different effort. The open question was whether the two SDK products should
share one generation pipeline ("one pipeline, two SDK products"), which the RFC's dependency map
listed as a peer opportunity, explicitly *not* a blocker.

## Problem

Decide now whether rap-sdk's pipeline is designed as shared infrastructure (multi-product inputs,
two release cadences, two owners) or as a single-product pipeline — the two shapes diverge
immediately in CI design, versioning, and configuration.

## Decision

**Explicitly decoupled** (Charles, 2026-07-10): separate pipelines, **no reuse commitment** in
either direction. The rap-sdk pipeline is designed for exactly one product: the RAP V2 SDK.

## Rationale

- A shared pipeline couples two products' release cadences, spec conventions, gate policies, and
  failure modes under two different owners — coordination cost with no merchant-visible benefit.
- The rap-sdk pipeline's hard parts (failover contract, publish gates, spec gating) are
  product-specific anyway; the genuinely reusable part (generator invocation) is the cheap part.

## Alternatives considered

- **One pipeline, two SDK products:** rejected — coupling across squads on the critical path of
  both products.
- **Defer the decision:** rejected — pipeline design starts Week 1; ambiguity here shapes CI
  wrongly from the first commit.

## Consequences

- No rap-sdk design decision needs RTN review, and vice versa — removed from both critical paths.
- The RTN initiative may **copy** anything useful (configs, templates, this ADR set's patterns) —
  copying is explicitly fine; a shared dependency is what's ruled out.
- If convergence ever becomes attractive post-GA, it is a new decision with its own RFC — this ADR
  records that it was considered and deliberately not taken now.

## Implementation guidance

- Keep pipeline code free of speculative multi-product abstraction (no "product" parameter,
  no second spec input) — single-product simplicity is the decided design.
