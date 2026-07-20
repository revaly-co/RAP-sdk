# ADR-SDK-026 — Interim Distribution: Per-Language GitHub Release Artifacts (Pipeline Stage 5 + Interim Stage 6)

**Status:** Accepted — 2026-07-20 (build-sequencing decision of 2026-07-18: release artifacts
before idiom flags, registry publish last; first-cut version + no-pre-release decision: Dimitri,
2026-07-20). Built the same day (`../../pipeline/package.sh`, `pipeline.yml` `package` +
`github-release` jobs).
**Source:** repo rule 3 (interim-distribution clause) · `../pipeline-and-release.md` §2 rows 5–6,
§3–4 · ADR-SDK-006 (artifact model) · ADR-SDK-013 (release-cut human gate) · ADR-SDK-015 (GA
order) · ADR-SDK-016 (tag scheme) · ADR-SDK-019 (license) · ADR-SDK-022 (namespace)
**Owner:** SC squad (per ADR-SDK-018)

## Context

All six hand-written runtimes are built and green (stage 3), and the live contract-smoke suites
prove the taxonomy against reality on every release tag and nightly (stage 4, ADR-SDK-024). The
registry publish surface remains embargoed behind OQ-3 (registry accounts, protected `publish`
environment, OIDC/GPG bindings), the ADR-SDK-013 machine gates, and ADR-SDK-019 Legal
ratification — none of which this repo can close unilaterally. Meanwhile the platform's E2E
dogfood (.NET, ADR-SDK-015) and Enablement pilots need consumable, verifiable SDK artifacts
*now*, with real version identities and provenance.

The platform's `spec/v*` releases already established the house artifact model: **asset +
`.sha256` + `provenance.json`** on a GitHub release, verified by consumers before use. Repo
rule 3 names per-language GitHub release artifacts from this repo, on that model, as the
sanctioned interim distribution channel.

## Decision

1. **Channel.** Pipeline stage 5 (package) and an **interim stage 6** (GitHub release on this
   repo) ship per-language release artifacts. No registry surface is touched: no OIDC
   trusted-publisher registrations, no registry tokens, no protected `publish` environment yet —
   those remain OQ-3/ADR-SDK-013 deliverables for the real stage 6.
2. **Tag scheme.** A release is cut by pushing `<language>/vX.Y.Z` (`dotnet/v0.1.0`,
   `java/v0.1.0`, `php/v0.1.0`, `typescript/v0.1.0`, `python/v0.1.0`) on `main` — the
   ADR-SDK-016 monorepo scheme, one language per tag. **Go tags as `go/vX.Y.Z`**, deliberately
   *not* the module-activating `languages/go/vX.Y.Z` form: a tag matching the subdir module path
   becomes a live, proxy-cached-forever Go publish the moment the repo goes public
   (ADR-SDK-012), which would jump the embargo and the publish-last ordering (ADR-SDK-015).
   `languages/go/v*` is **reserved** for the real, gated Go registry publish; the stage-5 job
   refuses it explicitly.
3. **Versions are plain `X.Y.Z` — no pre-release identifiers on this channel.** No
   `-alpha`/`-beta`/`-rc` (decided 2026-07-20): a "beta" version string is exactly what the
   embargoed pre-1.0 registry beta phase (`../pipeline-and-release.md` §4) will look like, and
   the two must not be confusable. The **first cut is `v0.1.0` across all six languages**;
   `1.0.0` stays reserved for registry GA per language (ADR-SDK-015 order). `package.sh` and the
   stage-5 job both refuse non-plain versions (fail-closed, not convention).
4. **The tag is the version source.** Committed manifests keep their `0.0.0-dev`-family
   placeholders (csproj `0.0.0-dev`, poms `0.0.0-SNAPSHOT`, package.json/version.ts `0.0.0`,
   pyproject/_version.py `0.0.0.dev0`, go `0.0.0-dev`, php SEMVER `0.0.0`); stage 5 stamps the
   tag version into the **ephemeral packaging copy only** (`pipeline/package.sh`, every stamp
   verified — a no-op sed fails the run). No version-bump commits, no drift between tag and
   artifact, and the committed tree never claims a released identity.
5. **Artifact set per release** (the ADR-SDK-006 spec-release model): the distributable
   asset(s) + one `.sha256` per asset + `provenance.json` (spec pin: release tag / spec version /
   source commit / bundle sha256; generator pin: name / version / image digest; gate trail;
   CI run id + URL; per-asset checksums) + release notes mapping the package version to the
   pinned spec commit SHA (`../pipeline-and-release.md` §4). Stable asset names match the
   committed quickstart READMEs: `Revaly.Sdk[.Core].<version>.nupkg` (both nupkgs — the local
   NuGet-feed pair), `revaly-sdk-java.zip` (Maven repository bundle: `co.revaly` subtree),
   `revaly-sdk-php.zip` (Composer artifact-repository zip, version injected into the zipped
   manifest), `revaly-sdk-typescript.tgz` (npm tarball with compiled CommonJS `dist/` — the
   generated core's extensionless imports rule out plain-Node ESM emit), `revaly-sdk-python.tar.gz`
   (+ canonically named wheel), `revaly-sdk-go.zip` (source-module zip consumed via `replace`).
6. **Gate mechanics.** The stage-5 `package` job runs only on a release tag and `needs:` all six
   stage-4 smoke jobs from the same run — any language red blocks every language's release
   (`../pipeline-and-release.md` §2). The job proves the tagged commit is an ancestor of `main`
   (GitHub cannot express "tag on main" declaratively; ADR-SDK-013 requires it). Stage 6 interim
   re-verifies checksums after the artifact transfer and creates the release with
   `--verify-tag --latest=false`; it **fails if the release already exists** — a failed release
   never resumes by re-run, the fix ships under a new tag (§1). Cutting the tag remains the one
   human act (ADR-SDK-013).
7. **Embargo guards stay in the artifacts:** npm `"private": true` (blocks `npm publish`, not
   `npm pack`), the PyPI `Private :: Do Not Upload` classifier, the version-free committed
   `composer.json` (Packagist derives versions from tags only once publish opens). `LICENSE`
   (Apache-2.0) + `NOTICE` land at the repo root with this ADR (the ADR-SDK-019 bootstrap
   deliverables; Legal ratification continues to gate **registry** publish, not source or the
   interim channel).
8. **Deliberately deferred to the real stage 5/6** (registry publish): SBOM per package, artifact
   signing, the third-party license scan, the protected `publish` environment, tag-protection
   rulesets, and OIDC/GPG bindings (all OQ-3/ADR-SDK-013/019 scope). The interim channel carries
   the spec-release trio only.

## Rationale

- **Same trust model as the spec input we consume:** merchants and internal consumers verify
  `sha256` + provenance exactly the way stage 1 verifies the platform's spec artifact — one
  verification idiom across the whole system (ADR-SDK-006).
- **Version identity without publishing:** per-language tags give real semver + traceability
  (version → spec SHA) while every registry gate stays closed; nothing about the interim channel
  has to be undone later — the same tags, versions, and provenance carry into registry publish
  history.
- **Tag-as-version-source** eliminates the classic monorepo failure of manifest/tag drift and
  keeps release mechanics out of the committed tree (no bump commits to review, no placeholder
  churn in PRs).
- **Go's inert tag form** is the only way to have an interim Go release at all without queueing
  an irreversible implicit publish for repo-public day.

## Alternatives considered

- **Publish pre-1.0 betas to registries now:** rejected — repo rule 3 is explicit that pre-1.0
  betas count as publishing; Go proxies cache forever; ADR-SDK-013/019/022 gates are open.
- **Consume from git (branch/commit URLs, git-based composer/npm/go installs):** rejected — no
  checksums, no provenance, no version identity, and it trains consumers onto moving refs that
  bypass the gated pipeline.
- **One combined release tag for all six languages:** rejected — semver is per package
  (RFC §5.7); languages move independently (runtime-only patches); ADR-SDK-016 already fixes the
  per-language tag matrix.
- **`languages/go/v*` for the interim Go release:** rejected — module-activating (see Decision 2).
- **Stamping versions into committed manifests per release:** rejected — bump-commit churn,
  tag/manifest drift risk, and the committed tree would claim released identities it doesn't have.

## Consequences

- Cutting `v0.1.0` ×6 is now a tag-push per language. **Cut sequentially in GA order
  (ADR-SDK-015: dotnet → java → php → typescript → python → go), waiting for green:** each tag
  runs the full pipeline including live smoke ×6 — six simultaneous tags would fire ~36
  concurrent live smoke scenarios at staging for no benefit.
- Every release re-proves stages 1–4 at its exact commit — a release can be blocked by a spec,
  generator, build, or live-contract regression, which is the point (§2 "any language red").
- The interim install paths documented in the language READMEs (local NuGet feed / file
  repository / composer artifact repo / tarball installs / `replace` directive) become the
  supported merchant path until registry publish; registry package names stay **[Proposed]**
  (OQ-3) and release notes say so.
- **Follow-up (repo-admin, Dimitri):** a tag ruleset protecting `*/v*` creation (maintainer-only)
  and blocking `languages/go/v*` outright — the workflow refuses the latter, but the tag itself
  should never exist. Tracked with the OQ-3 environment work (ADR-SDK-013 implementation
  guidance). ✅ **Done 2026-07-20:** `ReleaseTagsAdminOnly` (`refs/tags/**/v*`, admin bypass
  only) + `BlockGoModuleFormTags` (`refs/tags/languages/go/**`, no bypass — proven live against
  an admin push). Lifting the go-form block is a deliberate admin ceremony at the real Go
  registry publish.
- At registry-publish time, stage 6 interim is superseded, not removed: GitHub releases remain
  as the provenance record, and the registry publish job appends after it (`needs:`), gated on
  the `publish` environment.
