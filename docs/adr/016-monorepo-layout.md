# ADR-SDK-016 — Repository Layout: Monorepo `revaly-co/rap-sdk`

**Status:** Accepted — decided 2026-07-10 (OQ-7); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §11 OQ-7 (visibility decided separately as D-12 / ADR-SDK-012; namespace as OQ-15 / ADR-SDK-022)
**Owner:** SC Eng

## Context

Six languages, one deterministic pipeline (ADR-SDK-001/006), one spec input, one squad. The layout
question traded publishing ergonomics (some ecosystems prefer repo-per-package) against pipeline
coherence (one spec bump should regenerate and release all six coherently).

## Problem

Choose between a monorepo and per-language repos before the repo is created — the choice shapes
CI, versioning, tagging, and how a spec-artifact bump propagates.

## Decision

- **Monorepo:** `revaly-co/rap-sdk` holds all six languages, the pipeline, the vendored gated spec
  artifact reference, and the SDK documentation set.
- **Per-language read-only mirrors are created only if an ecosystem demands it** — mirror, never
  fork: generated one-way from the monorepo by the pipeline, no direct pushes, no divergent
  history. (Packagist is the known likely candidate — Composer installs expect a repo per package.
  Go supports subdirectory module paths, so a mirror is not automatically required.)

## Rationale

- **One spec bump = one atomic change set** across all six cores — cross-language consistency is
  reviewable in a single PR, which is the entire point of the shared pipeline.
- One CI/CD definition, one release process, one place for the machine gates (ADR-SDK-013) instead
  of six drifting copies.
- A single squad cannot shepherd six repos' branch protection, secrets, environments, and issue
  trackers without drift — the exact failure mode the org's ungated-environments finding
  illustrates.

## Alternatives considered

- **Repo per language:** rejected — six copies of pipeline/gates/config; spec bumps become six
  PRs; cross-language releases lose atomicity.
- **Monorepo + mirrors for all six from day one:** rejected — mirrors only where an ecosystem
  *requires* them; every mirror is surface to protect and explain.

## Consequences

- Tagging scheme must support both repo-wide and per-language releases (languages GA at different
  times, ADR-SDK-015): per-language release tags (e.g., `dotnet/v1.0.0`) drive the publish matrix;
  the environment tag policy (ADR-SDK-013) covers the pattern set.
- GitHub Issues intake (ADR-SDK-012) is one tracker with language labels — matching the one-squad
  triage rotation.
- If a Packagist mirror is needed, it is pipeline-generated, read-only, carries the same LICENSE/
  SECURITY.md, and its README points back to the monorepo for issues.

## Implementation guidance

Proposed layout (finalize in the repo-bootstrap story):

```
rap-sdk/
  spec/                  # pinned gated spec artifact reference + checksums (ADR-SDK-006)
  languages/
    dotnet/   { core/ (generated), runtime/, tests/ }
    java/     { core/, runtime/, tests/ }
    php/      { core/, runtime/, tests/ }
    typescript/ { core/, runtime/, tests/ }
    python/   { core/, runtime/, tests/ }
    go/       { core/, runtime/, tests/ }   # module path: github.com/revaly-co/rap-sdk/languages/go (subdir module)
  pipeline/              # generation configs, templates, publish workflows
  docs/                  # this ADR set + design docs (relocated from the platform repo)
```

- Each `core/` carries a generated-code banner and is protected by the CI regeneration-diff check
  (ADR-SDK-001).
- Confirm the Go module path shape (root vs subdir module) during the OQ-1 bake-off — if a root
  module is required for pkg.go.dev ergonomics, that is the one layout question revisited before
  first Go publish (Go is last in GA order, ADR-SDK-015, so the window is long).
