# ADR-SDK-001 — Hybrid Architecture: Generated Core + Hand-Written Runtime per Language

**Status:** Accepted — decided 2026-07-06 (D-1); ratified with RFC-046 approval 2026-07-10 (v10, Charles Weiss)
**Source:** RFC-046 "RAP Integration SDK" §3, decision D-1 · PRD-057 · SC-215 / Epic SC-234
**Owner:** SC Eng
**Target repo:** `revaly-co/rap-sdk` (this document set relocates there — see `README.md`)

## Context

PRD-057 requires a server-side client SDK for the RAP V2 API in six languages: Python, TypeScript,
Go, .NET, PHP, Java. The API surface is the full V2 contract — payments (charge, authorize, capture,
void, refund, refund-cancel), payment methods, transactions, and notify — served at `api.revaly.co`
and described by a canonical, **hand-maintained** OpenAPI spec (title "Revaly", currently v2.1.1,
OpenAPI 3.0.3). The spec is *not* generated from code; whatever is generated from it inherits its
accuracy (see ADR-SDK-006).

The real technical challenge is not writing six HTTP clients. It is:

1. keeping six language targets correct and in sync with an evolving API without six times the
   hand-maintenance, and
2. shipping a **failover contract** (ADR-SDK-002/003/009) precise enough that a merchant can route
   full traffic through RAP-core and know exactly what to do when a call fails — including the case
   where the payment outcome is unknown.

PRD-057 itself rates "six-language scope underestimated" as a **High** risk.

## Problem

One squad must deliver and sustain six correct, idiomatic SDKs carrying one safety-critical failover
contract. Any architecture that requires per-language re-implementation of the API surface will
drift — from the API and between languages — and any architecture that leans entirely on raw code
generation produces unidiomatic clients with no failover semantics, increasing the Enablement
support load the SDK exists to reduce.

## Decision

Adopt the **hybrid architecture**: for each of the six languages,

- a **generated core** — models and endpoint bindings generated from the canonical OpenAPI spec
  (only from gated spec artifacts, ADR-SDK-006). The core is the commodity: it churns mechanically
  with the API and is **never hand-edited** (enforced in CI — a regeneration diff check fails the
  build if generated output was touched by hand);
- a **thin, hand-written runtime** — the product. It carries everything PRD-057 actually values:
  authentication (merchant API key injection), API version pinning (`X-Api-Version: 2.1` default,
  `2.0` selectable), connect/overall deadlines, the typed error taxonomy (ADR-SDK-002), the failover
  and reconciliation surface (ADR-SDK-003/009), and the telemetry identifier (ADR-SDK-005). Its
  merchant-facing shape is governed by the Developer Experience contract (`../dx-contract.md`).

The runtime is deliberately small and stable; the generated core absorbs API churn.

## Rationale

- The generated/hand-written split puts the maintenance burden where automation works (models,
  endpoints) and human design where it matters (safety semantics, ergonomics).
- The failover contract is the differentiating value of this SDK. It cannot be generated — it is a
  designed safety analysis (double-charge hazard, provable-absence reasoning) that must be expressed
  idiomatically per language.
- One squad can own six runtimes only if each runtime is thin. Everything that can churn is pushed
  into the regenerable core.

## Alternatives considered

| Option | Verdict | Why rejected |
| --- | --- | --- |
| **A — Hand-crafted SDK per language** | Rejected | Best ergonomics, unsustainable: six codebases drift from the API and from each other; PRD already rates the six-language scope a High risk. |
| **B — Raw codegen (openapi-generator defaults) per language** | Rejected | Fast to first artifact; per-language template quality varies wildly, no failover semantics, unidiomatic surfaces. Likely *increases* Enablement load — defeats the PRD's integration-simplicity goal. |
| **C — Hybrid: generated core + hand-written runtime** | **Selected** | Generated part is the commodity; runtime is the product, small and stable. |

## Consequences

- The generator choice becomes a build gate (OQ-1 bake-off: openapi-generator vs Speakeasy / Fern /
  Stainless; Kiota for .NET). The acceptance criterion is the DX contract's idiomatic bar
  (`../dx-contract.md` §a): a generator that cannot meet the bar with template customization
  is disqualified.
- The CI/CD pipeline becomes the product's manufacturing line (`../pipeline-and-release.md`):
  every release is produced by one deterministic pipeline traceable to a spec commit SHA
  (ADR-SDK-013 governs publish protection).
- Every language ships both layers from day one; the GA investment order is governed by ADR-SDK-015.
- The per-language runtime API reference is TDD material (`../runtime-tdd.md`), not ADR
  material.

## Implementation guidance

- Repository layout per ADR-SDK-016 (monorepo): each language directory separates `core/`
  (generated, marked with a "do not edit" banner and CI-diff-enforced) from `runtime/`
  (hand-written).
- The runtime wraps the generated transport; merchants construct a single client object configured
  with API key, base URL, version pin, and deadlines. The generated types are re-exported through
  the runtime's namespace so merchants import one package.
- Regeneration is a pipeline stage, not a developer chore: a spec-artifact bump PR regenerates all
  six cores in one change set (see `../pipeline-and-release.md`).
- Do not leak generator idiosyncrasies into the public surface: the OQ-1 bake-off must verify that
  the runtime can fully wrap/hide the generated layer in every language.
