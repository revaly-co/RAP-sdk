# ADR-SDK-006 — Spec Accuracy Is a Release Gate: the Pipeline Consumes Only Gated Spec Artifacts

**Status:** Accepted — decided 2026-07-06 (D-6); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §3.2 ("100% validated, or nothing ships"), decision D-6
**Owner:** SC Eng

## Context

The canonical OpenAPI spec for the RAP V2 API is **hand-maintained** in the platform repository —
it is not generated from code, so nothing structurally guarantees it matches the implementation.
Two real spec-accuracy defects were found during this RFC's review and had passed every gate that
existed at the time:

1. `amount` lacked `format: int64` — the runtime type is a 64-bit integer; an unformatted `integer`
   generates **int32** clients in typed languages, overflowing above ~$21.4M in cents;
2. the create call documented `merchantTransactionId` max length 100 while the reconcile lookup and
   refund-cancel routes enforced 50 — a spec-legal id could 400 exactly on the recovery call.

Hand-written merchant integrations absorb such errors quietly. **Generated SDKs do not**: once six
SDKs are generated from the spec, any spec error ships to every merchant as a compile-visible bug,
×6, in the same release.

## Problem

Make it structurally impossible for spec inaccuracy to reach a published SDK.

## Decision

Spec accuracy is a **hard release gate**, enforced as a four-part chain:

1. **Lint/bundle gate** in platform CI (`redocly lint` + `bundle`, PR-blocking, no bypass) —
   *shipped 2026-07-08*.
2. **Breaking-change gate** in platform CI (`oasdiff breaking` vs the main branch, per-finding
   allowlist) — *shipped 2026-07-08*. Also feeds semver classification for SDK releases
   (`../pipeline-and-release.md`).
3. **Spec-vs-implementation contract suite** in platform CI: every operation, response status, and
   schema exercised against the running API, **100% operation coverage required** — *to build*
   (platform repo ADR 017). The two defects above passed gates 1–2; this is the gate that would
   have caught them.
4. **The SDK pipeline consumes only spec artifacts that passed all gates** — it never reads the
   spec from an arbitrary branch or unreviewed ref (artifact publication: platform repo ADR 016).

## Rationale

- The generated core (ADR-SDK-001) inherits spec accuracy verbatim; gating generation on validated
  artifacts is the only place the ×6 blast radius can be cut off.
- A "touched the docs" check (the platform's historical protection) verifies effort, not truth.
  Items 1–2 verify structure and compatibility; item 3 verifies truth; item 4 makes the SDK build
  unable to bypass any of it.

## Alternatives considered

- **Generate the spec from code instead:** rejected — inverts a settled platform convention (the
  hand-maintained multi-file spec is the canonical contract) and would churn the entire existing
  consumer surface; accuracy enforcement achieves the goal without the migration.
- **Trust review to catch spec drift:** rejected — both known defects survived review; this is the
  live evidence a mechanical gate is needed.
- **Validate inside the SDK pipeline only:** rejected — validation must block the *platform* PR
  that introduces drift, not fail the SDK build days later; the SDK pipeline still re-validates as
  defense in depth.

## Consequences

- SDK releases are traceable: every package version maps to a spec commit SHA recorded in release
  notes.
- A platform release with a red contract suite blocks SDK releases (release-gate SLO, RFC-046 §8);
  "nothing ships" is meant literally.
- The SDK pipeline's stage 1 re-runs lint/bundle on the consumed artifact (defense in depth,
  `../pipeline-and-release.md`) even though the artifact is already gated.
- Until gate 3 exists, generation proceeds on artifacts gated by 1–2 plus the pre-generator spec
  corrections (platform repo ADR 015) — gate 3 is a **prerequisite for Wave-1 GA discipline**, and
  its absence is a known, accepted risk only during the pre-GA build phase.

## Implementation guidance

- The pipeline's artifact-consumption step must verify artifact integrity (checksum) and record the
  spec SHA + gate evidence into the build metadata that ends up in release notes.
- Treat "spec artifact version" as an explicit, pinned input of the SDK repo (a committed reference
  updated by PR), not an implicit "latest" — regeneration diffs then review like any dependency
  bump.
- Never point the generator at a spec file from a branch checkout, a URL, or a local edit. If a
  spec change is needed, it lands in the platform repo first and arrives as a new gated artifact.
