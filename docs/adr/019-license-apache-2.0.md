# ADR-SDK-019 — License: Apache-2.0 (Legal Ratifies Before First Publish)

**Status:** Accepted — decided 2026-07-10 (OQ-12, Charles); Legal ratification pending (gate on first publish); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §7.1 / §11 OQ-12
**Owner:** Leadership + Legal

## Context

A license binds consumers and is **effectively irreversible once merchants adopt** — relicensing a
public SDK after adoption is a breaking legal event. Maven Central additionally *requires* a
license plus an SCM URL in the POM before it will accept a publish; every registry listing displays
the license. Review (2026-07-08) required the license decision named and owned before approval.

## Problem

Pick the license for six public packages that merchants will run inside payment systems, before the
repo and the first (even pre-1.0) publish exist.

## Decision

- **Apache-2.0** (decided by Charles, 2026-07-10). MIT was the acceptable alternative; Apache-2.0
  selected.
- **Copyright remains with Revaly.**
- **Legal ratifies before the first publish** — the decision is made; ratification is a tracked
  gate on publishing, not on build (see `../open-items.md`).

## Rationale

- **The explicit patent grant** is the differentiator over MIT: merchants embedding the SDK in
  payment systems get patent peace, and the grant's defensive-termination clause protects Revaly.
- It is the corporate-SDK standard — matches Square/AWS practice — so merchant legal teams approve
  it without review friction.

## Alternatives considered

- **MIT:** acceptable fallback; rejected in favor of the patent grant.
- **Proprietary / source-available:** rejected — incompatible with the public-repo distribution
  mechanics (ADR-SDK-012) and with ecosystem expectations for client SDKs.
- **Copyleft (GPL/LGPL/MPL):** never candidates — viral obligations inside merchant codebases are
  a non-starter for adoption.

## Consequences

- `LICENSE` (Apache-2.0 text) and per-file/package license metadata are repo-bootstrap
  deliverables; **no publish of any kind before Legal ratifies** (sequenced with the ADR-SDK-013
  machine gates and ADR-SDK-022 namespace gate).
- Maven POM carries license + SCM URL (pointing at `revaly-co/rap-sdk`); every package manifest
  (package.json, pyproject.toml, csproj/nuspec, composer.json, go.mod's repo LICENSE) declares
  `Apache-2.0` (SPDX identifier).
- `NOTICE` file policy (Apache-2.0 §4d) decided at bootstrap: carry a minimal NOTICE with the
  Revaly copyright line.
- Third-party code pulled in by generators/templates must be Apache-2.0-compatible — add a license
  scan to the pipeline's build stage.

## Implementation guidance

- Use SPDX `Apache-2.0` consistently in all metadata; registry listings render from it.
- The release-cut checklist (ADR-SDK-013) includes "license metadata present and correct per
  package" — Maven Central will hard-fail without it; the others fail softer but must not drift.
