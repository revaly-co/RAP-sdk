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
| 6 | **publish** | GitHub release (interim channel + permanent provenance anchor, ADR-SDK-026/031), then the registry job: npm · PyPI · NuGet · Packagist · Maven Central · pkg.go.dev from the protected environment only (ADR-SDK-013). **Dark until the rule-3 gates close** (ADR-SDK-031): rehearsal + flip-readiness report on every tag, no registry contact | — |

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
- **Dark until flip (ADR-SDK-031):** the registry job runs on every release tag in the
  `publish` environment but contacts no registry until the **double-keyed** flip —
  `REGISTRY_PUBLISH_MODE=live` (repo variable, fail-closed) **and** the flip-day
  guard-removal PR (npm `"private"`, python `Private :: Do Not Upload`); a half-flip
  hard-fails. `pipeline/registry-publish.sh` is the single entry point; the flip runbook is
  in `registry-provisioning.md`.
- **Packagist mechanics:** packagist.org needs `composer.json` at the repo root, so
  `revaly/sdk` publishes from a generated read-only mirror (`revaly-co/rap-sdk-php`) that
  the registry job builds **from the verified stage-5 artifact tree** (version-stamped,
  LICENSE/NOTICE included — never a raw subtree split of the unstamped committed tree);
  the webhook lives on the mirror (ADR-SDK-031, amending the earlier "webhook from the
  monorepo" wording).
- **GitHub releases stay after registry GA** as the provenance anchor and
  registry-outage/air-gap fallback; registries are the primary install path from flip
  (ADR-SDK-031).
- A scheduled drift check asserts the gates themselves (environment policy, tag protection,
  trusted-publisher bindings) still match ADR-SDK-013.

### 3.1 Per-registry push mechanics — what lives in the workflow vs `registry-publish.sh`

One design rule decides where every step lives: **`pipeline/registry-publish.sh` owns
everything that runs identically on a laptop and in CI** (all checks, all CLI-based
pushes); **the workflow owns only what requires GitHub Actions machinery** (OIDC token
exchanges, action-based uploads). That is why some languages have visible per-language
workflow steps and others none — npm's push lives *inside the script*, and Go has *no push
anywhere, by design*.

| Language | Dark rehearsal (script, every tag) | Live push — where + command | Credential (provisioned at flip) |
| --- | --- | --- | --- |
| dotnet | nuspec ids/versions vs ADR-SDK-030 | **script**: `dotnet nuget push`, `Revaly.Sdk.Core` before `Revaly.Sdk` (consumers must never resolve the runtime before its core exists) | workflow `NuGet/login` exchanges OIDC for a temp key → script env `NUGET_API_KEY` |
| java | bundle layout, POM completeness (name/description/url/licenses/scm/developers), sources + javadoc jars | **script**: GPG-sign every bundle file + md5/sha1 → zip the `co/` tree → `curl POST` to the Central Portal API. Never rebuilds — signs exactly the stage-5 bytes | workflow `azure/login` + Key Vault fetch → script env `MAVEN_GPG_KEY_FILE`, `MAVEN_CENTRAL_TOKEN` |
| php | builds the mirror tree **from the stage-5 zip** (stamped SEMVER, LICENSE/NOTICE present, injected `version` field removed) and validates it | **script**: `git push` the tree as a fresh commit + `v<version>` tag to the `rap-sdk-php` mirror. Packagist's API is never called — its webhook on the mirror ingests the release | `PACKAGIST_MIRROR_PUSH_TOKEN` environment secret |
| typescript | packed name `@revaly/sdk`, version, `"private"` guard state | **script**: `npm publish <tgz> --access public --provenance`. No workflow push step exists: npm ≥ 11.5 performs the OIDC exchange itself (job `id-token: write` + the trusted publisher registered at flip); the only workflow step is live-only `setup-node` | none (OIDC via npm CLI) |
| python | wheel METADATA, classifier guard, stages `dist/python/.pypi-upload/` with **PyPI-canonical filenames** (the GitHub asset name is not a valid sdist name), `twine check` | **workflow**: `pypa/gh-action-pypi-publish` uploads the staged dir — the one push outside the script, because that action *is* PyPI's official OIDC implementation (token mint + upload); `publish_python` in the script is just a pointer to it | none (OIDC via the pypa action) |
| go | asserts the module path inside the zip | **nowhere — no push operation exists.** pkg.go.dev is pull-based: publishing = public repo + a `languages/go/v*` tag; proxy.golang.org fetches from GitHub on first request. The interim `go/v*` tags are inert to Go tooling; the real release is the ADR-SDK-026 ceremony (lift the tag ruleset, tag, verify), deliberately **last** — module proxies cache every version forever | none |

**What is and is not tested before flip:** dark mode proves everything *up to* the push —
artifact integrity, names, filenames, guards, credential plumbing, refusal paths (the live
negative tests). The pushes themselves cannot run without contacting a registry, which is
exactly what rule 3 embargoes, so they execute for the first time on flip day. That
residual is accepted in ADR-SDK-031 and deliberately minimized: every live path is one
well-known command (`dotnet nuget push` / `npm publish` / `git push` / one `curl`), with
all inputs pre-proven by the readiness lint.

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
| Stage-4 smoke secrets (interim) | GitHub environment **`staging`**: `RAP_SMOKE_BASE_URL`, `RAP_SMOKE_API_KEY`, `RAP_SMOKE_GATEWAY_ROUTING_ID` | ADR-SDK-024 implementation record. Keys borrowed from the platform's staging E2E pool (scope lives on the key — prefer sandbox-scoped for GA parity); never logged. **Two-target since 2026-07-25** (ADR-SDK-024 §Decision 4): each job runs its suite twice — step 1 against the prod sandbox key-scope (`RAP_SANDBOX_BASE_URL` / `RAP_SANDBOX_API_KEY` / `RAP_SANDBOX_GATEWAY_ROUTING_ID`, injector not passed → the `not_processed` row SKIPs), step 2 against Backbone staging (`RAP_SMOKE_BASE_URL` / `RAP_SMOKE_API_KEY` / `RAP_SMOKE_GATEWAY_ROUTING_ID` + the `RAP_SMOKE_FAULT_INJECT=pre-dispatch` **variable**), which is the only place the injector exists. Together they keep the full §2 taxonomy covered. All six secrets + the variable are **fail-closed at job start** — an unset injector variable is an error, not a skip, because it would silently drop the only immediate-failover row. `RAP_SMOKE_*` now denotes the step-2 (staging) target specifically. **Staging traps:** the base URL must be the HOST ROOT (a `/payments` suffix makes the SDK append its own path and every call 404s — the tell is 7/8 failing while `reconcile-not-found-yet` passes), and the routing token must point at a gateway where expiry drives the outcome (12/2020 must DECLINE, or `reconcile-found-declined` fails). The injector is **inert on the production path** (`../docs/prod-sandbox-validation.md`), which is exactly why step 2 exists; the routing id is **required, not optional** in both steps — without it charges land in the `flexpay_declined` sink (responseCode 50130) |
| Sandbox CI key (GA) | Key Vault | Enablement-issued (ADR-SDK-014); replaces the interim staging secrets at the ADR-SDK-024 GA retarget; never logged |
| GPG keys (Maven) | Key Vault | Environment-scoped job access only |
| Registry identities | OIDC trusted publishing | No long-lived registry tokens anywhere |
