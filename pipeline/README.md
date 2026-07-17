# `pipeline/` — Generation & Release Pipeline

One deterministic pipeline (`../docs/pipeline-and-release.md`): **validate → generate ×6 →
build+test → contract smoke → package → publish**. Stages 1–4 run on every PR
(`../.github/workflows/pipeline.yml`); 5–6 only from release tags on `main` — and **publish is
embargoed** until its gates close (repo rule 3; ADR-SDK-011/013/019/022).

## What exists today

| Piece | Purpose |
| --- | --- |
| `../.github/workflows/pipeline.yml` | **Stage 1 — validate**: re-verifies the pinned gated spec artifact (`../spec/pin.yaml`, ADR-SDK-006): download from the pinned release, bundle checksum vs pin + release assets, byte-identity of the committed evidence copies, provenance gates (lint / bundle / breaking / contractSuite), tag ↔ sourceCommit ↔ specVersion consistency, then redocly re-lint + re-bundle as defense in depth. **Stage 2 — generate + regen-diff**: reruns `generate.sh` for all six languages and fails unless `../languages/*/core/` is byte-identical (ADR-SDK-001 enforcement). **Stage 3 — build + test ×6**: one `Stage 3 - Build + Test (<language>)` job per language compiles the committed core — `dotnet build` (Release) / `mvn compile` / composer validate + install + `php -l` + strict-PSR-4 dump / strict no-emit `tsc` (via `typescript/compile-check/`) / `pip install` + package import + compileall / `go build` + `go vet`. Toolchains are minor-pinned, patch-floating (they emit no committed bytes — only the spec artifact and generator image are hard-pinned). First increment is compile-only: unit tests, dx-contract §a ecosystem linters, and ADR-SDK-020 log-capture scrub tests attach to these jobs when `../languages/*/runtime/` lands |
| `spec-tooling/` | Lockfile-pinned `@redocly/cli` — `npm ci` verifies the pinned tarball's integrity hash; the workflow cross-checks the installed version against `REDOCLY_VERSION` and refuses drift |
| `generator-pin.yaml` | Generator toolchain pin (ADR-SDK-023) — stage 2's input; upgrades are ADR revisions riding PRs where the regeneration diff makes the blast radius reviewable |
| `generate.sh` | The only generation entry point (local and CI): downloads the pinned artifact (or takes `--spec`), **sha256-verifies it against `../spec/pin.yaml` before generating** (ADR-SDK-006), wipes each `core/` and regenerates it with the digest-pinned image — never a floating tag, never a local install |
| `typescript/compile-check/` | Stage-3 compile harness for the TS core: lockfile-pinned `typescript` (`npm ci`, same trust posture as `spec-tooling/`), strict no-emit `tsc` over `../languages/typescript/core/`. Exists because the core is generated **bare** (no `npmName` → no package scaffolding, see `typescript/config.yaml`): the core ships inside the runtime's package (runtime-tdd.md §2), so the harness never becomes a publishable package — the npm identity is [Proposed] until OQ-3 and belongs to the runtime |
| `<language>/` (×6: `dotnet` `java` `php` `typescript` `python` `go`) | Per-language generation config (ADR-SDK-023 flag table): `config.yaml` (flags, [Proposed] OQ-3 package identities, explicit Apache-2.0 license fields per ADR-SDK-019), `.openapi-generator-ignore` (exclusions — note: patterns need a `**/` prefix, this matcher is narrower than gitignore), `templates/` (generated-code banner partial per ADR-SDK-016; python additionally forks `model_generic.mustache` to make enum validators open-vocabulary; all six fork their auth-example templates so every generated README/api-doc shows the RAP scheme — an API key in the `Authorization` header with the **required `ApiKey` prefix**, `Authorization: ApiKey <key>` — instead of the stock Bearer-style or prefix-less samples (java native's stock samples didn't even compile); dotnet additionally forks the generichost `JsonConverter.mustache` (2026-07-16) to guard optional inner-enum serialization with `Option.IsSet` — the stock template dereferences the unset Option, crashing any request that omits e.g. `paymentMethodType`/`cardType`; each `config.yaml` header lists its exact fork set — re-diff forks against the embedded originals on any generator upgrade) |

## One-time CI provisioning: `SPEC_ARTIFACT_READ_TOKEN`

The platform repo is **private**, and a workflow's default `GITHUB_TOKEN` is scoped to this
repo only — it cannot read the platform repo's releases. Stage 1 therefore needs one repo
secret:

- **Name:** `SPEC_ARTIFACT_READ_TOKEN`
- **Value:** a fine-grained PAT — resource: the platform repo (`repo:` in `../spec/pin.yaml`)
  **only**; permissions: **Contents: read-only** (+ implicit Metadata). Nothing else.
- **Set:** `gh secret set SPEC_ARTIFACT_READ_TOKEN -R revaly-co/RAP-sdk`
  (or repo Settings → Secrets and variables → Actions).
- Until it exists, stage 1 **fails closed** with a provisioning message — deliberately: a
  silently skipped verification would conflate "gate passed" with "gate never ran".
- Rotate on expiry; replace when the platform repo changes org (ADR-SDK-022 rename).
  **The 2026-07-17 org migration is exactly this event**: fine-grained PATs are
  resource-owner-scoped and do not follow a repo across orgs, so the token must be
  re-provisioned under `revaly-co` (resource: `revaly-co/Backbone` only, Contents:
  read-only). Until then, downloads may ride the old grant + redirect — working today is
  not proof it survives the old org's parking.

## Dependency hygiene for generated manifests

The generated cores carry dependency manifests (pom.xml, pyproject.toml/setup.py/
requirements.txt, composer.json, csproj, go.mod ranges) whose versions come from the pinned
generator's templates. **Dependabot alerts are the detector; the fix vehicle is always the
generation config** — bump the floor in a template fork (or flag) under `pipeline/<language>/`
and regenerate. A Dependabot (or human) PR that edits `languages/*/core/` directly can never
merge: stage 2 regenerates and rejects any byte drift (ADR-SDK-001). For that reason
Dependabot's *automated security-fix PRs* are disabled repo-wide while *alerts stay enabled*;
`languages/go/go.mod`/`go.sum` are the one hand-maintained manifest pair (bump directly).
First applied 2026-07-15: jackson-databind 2.21.5 (java pom fork), urllib3 ≥ 2.7.0 + dev-group
pytest ≥ 9.0.3 (python manifest forks) — 11 of 12 launch alerts cleared, the 12th (filelock,
dev-scope transitive) tracked for dismissal.

## Stage roadmap (build order)

Stage 2 (generate ×6 — **built 2026-07-15**, cores committed from `spec/v2.1.3+e75c71a`) →
stage 3 (build + test, any language red blocks all — **first increment built 2026-07-16**:
compile ×6 on every PR; tests/linters/scrub tests attach when the runtime lands) → stage 4
(contract smoke vs Sandbox, Enablement-issued key, ADR-SDK-014) → stages 5–6 (package /
publish — embargoed; per-language release tags drive the matrix). Each stage appends a job
to `pipeline.yml` chained with `needs:`.
