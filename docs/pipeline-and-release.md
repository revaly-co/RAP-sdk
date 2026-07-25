# RAP Integration SDK — Pipeline & Release Design

**Source:** RFC-046 §3.1 ("the pipeline is the product"), §5.7, §7, §8 · ADR-SDK-006 (gated spec),
013 (publish gate), 015 (GA order), 016 (monorepo), 019 (license), 022 (namespace),
023 (generator)

## 1. Principles

- **Every SDK release is produced by one deterministic CI/CD pipeline, traceable to a platform
  spec commit SHA.**
- **No hand edits to generated code, ever** — the runtime layer is the only hand-written code;
  a CI regeneration-diff check enforces it.
- **A release that fails any stage does not publish.** A tag may exist without artifacts;
  publishing resumes only via a new tag after the fix — never a manual re-run against edited
  state.
- The pipeline consumes **only gated spec artifacts** (ADR-SDK-006) — never a branch checkout,
  URL, or local edit.

## 2. Stages

| # | Stage | What it does | Failure means |
| --- | --- | --- | --- |
| 1 | **validate** | Re-lint + re-bundle the consumed spec artifact (defense in depth on top of platform gates); verify artifact checksum + provenance metadata | Bad/tampered input — nothing downstream runs |
| 2 | **generate** | Generate all six language cores from the artifact (generator pinned per ADR-SDK-023 — `pipeline/generator-pin.yaml`); regeneration-diff check proves no hand edits | Generator/toolchain drift |
| 3 | **build + test** | Compile all six; unit tests (runtime + core); ecosystem linters (DX contract §a); log-capture scrub tests (ADR-SDK-020) | Any language red blocks the release for all |
| 4 | **contract smoke** | Live smoke of all six SDKs against the stage-4 environment (ADR-SDK-024: Backbone staging via the environment-scoped `staging` secrets interim; merchant sandbox key-scope with the Enablement-issued Key Vault key at GA, ADR-SDK-014): charge approved + declined, validation/auth rejections, the injected `503+not_processed` fast-failover row, reconcile both verdicts | Release blocked — the taxonomy is unproven against reality |
| 5 | **package** | Version stamp (semver, §4), license + SCM metadata (Apache-2.0, ADR-SDK-019), SBOM per package, release notes with spec SHA | Metadata incomplete (Maven hard-fails without license/SCM) |
| 6 | **publish** | Signed publish to npm · PyPI · NuGet · Packagist · Maven Central · pkg.go.dev, from the protected environment only (ADR-SDK-013) | — |

Stages 1–3 run on every PR. Stage 4 runs on release tags (**blocking**: any language red
blocks the release for all six), on the nightly schedule (advisory), and on manual dispatch —
never on plain PRs (network and secrets stay out of the PR path; ADR-SDK-024). Stages 5–6 run
only from a release tag on `main` (machine gates below).

## 3. Publish mechanics (ADR-SDK-013 machine gates)

- **One human act: cutting the release tag.** Environment deployment policy restricts the publish
  job to release tags on `main`; tag creation is maintainer-only (tag protection); no required
  reviewers on the environment.
- Per registry: npm / PyPI / NuGet — **OIDC trusted publishing** (no stored tokens; registered
  only after the namespace is final — ADR-SDK-022); Maven Central — **GPG signing**, keys in Key
  Vault, fetched inside the environment-scoped job; Packagist — webhook from the public repo;
  pkg.go.dev — pull-based, the tag *is* the release.
- Monorepo tag scheme (ADR-SDK-016): per-language release tags (e.g. `dotnet/v1.0.0`) drive the
  publish matrix; the environment tag policy covers the whole pattern set.
- A scheduled drift check asserts the gates themselves (environment policy, tag protection,
  trusted-publisher bindings) still match ADR-SDK-013.

## 4. Versioning (RFC §5.7)

- **Semver per package; the SDK major tracks the RAP V2 API major.** Minor/patch follow API
  changes within the major.
- **Pre-1.0 versions publish publicly during the beta phase; 1.0 GA per language** in GA order
  (ADR-SDK-015). Pre-1.0 still counts as publishing for every gate (namespace, license, publish
  protection) — Go module proxies cache betas forever.
- **Every package version maps to a spec commit SHA in release notes** (stage 5 stamps it from the
  artifact provenance).
- Semver classification of spec changes is informed by the platform's breaking-change gate
  (oasdiff): breaking spec change ⇒ major consideration; additive ⇒ minor; fixes ⇒ patch. The
  release-cut checklist records the classification rationale.
- Runtime-only changes version independently within the same scheme (they are package changes,
  not API changes).

## 5. Bad-release response (RFC §8 on-call story)

A runbook is a **GA-gating deliverable** (written in Epic SC-234, not TBD). Outline fixed by the
RFC:

1. Detect: server-side dashboards keyed on `User-Agent` version (error rate by SDK
   language/version) — a bad release is visible without merchant reports.
2. Contain: registry **deprecation/yank per ecosystem** (never delete where deletion is even
   possible; Go: retract directive).
3. Fix: **immediate patch release from the last good spec artifact** through the same pipeline —
   no expedited side channel.
4. Announce: yanked release announced **together with its patched replacement in the same
   notice**; channels per DX contract §e (release notes + registry deprecation metadata).

## 6. Inputs & secrets

| Input | Source | Notes |
| --- | --- | --- |
| Gated spec artifact | Platform repo publication (platform ADR 016) | Pinned by committed reference; bumped by PR |
| Generator toolchain | ADR-SDK-023 pin (`pipeline/generator-pin.yaml`) | Digest-pinned Docker image — checksum-pinned like any release tooling |
| Stage-4 smoke secrets (interim) | GitHub environment **`staging`**: `RAP_SMOKE_BASE_URL`, `RAP_SMOKE_API_KEY`, `RAP_SMOKE_GATEWAY_ROUTING_ID` | ADR-SDK-024 implementation record. Keys borrowed from the platform's staging E2E pool (scope lives on the key — prefer sandbox-scoped for GA parity); never logged. `RAP_SMOKE_FAULT_INJECT=pre-dispatch` is plain workflow env (staging-only fault seam), removed at the GA retarget. **At retarget** (`../docs/prod-sandbox-validation.md`, 2026-07-25): the injector is **inert on the production path** — verified, the injected charge simply approves — so removing the var also removes live coverage of the `503 + not_processed` row (moves to mock-only, accept in writing per ADR-SDK-024); and `RAP_SMOKE_GATEWAY_ROUTING_ID` becomes **required, not optional** — without it prod-sandbox charges land in the `flexpay_declined` sink (responseCode 50130) |
| Sandbox CI key (GA) | Key Vault | Enablement-issued (ADR-SDK-014); replaces the interim staging secrets at the ADR-SDK-024 GA retarget; never logged |
| GPG keys (Maven) | Key Vault | Environment-scoped job access only |
| Registry identities | OIDC trusted publishing | No long-lived registry tokens anywhere |
