# `pipeline/` — Generation & Release Pipeline

One deterministic pipeline (`../docs/pipeline-and-release.md`): **validate → generate ×6 →
build+test → contract smoke → package → publish**. Stages 1–4 run on every PR
(`../.github/workflows/pipeline.yml`); 5–6 only from release tags on `main` — and **publish is
embargoed** until its gates close (repo rule 3; ADR-SDK-011/013/019/022).

## What exists today

| Piece | Purpose |
| --- | --- |
| `../.github/workflows/pipeline.yml` | **Stage 1 — validate**: re-verifies the pinned gated spec artifact (`../spec/pin.yaml`, ADR-SDK-006): download from the pinned release, bundle checksum vs pin + release assets, byte-identity of the committed evidence copies, provenance gates (lint / bundle / breaking / contractSuite), tag ↔ sourceCommit ↔ specVersion consistency, then redocly re-lint + re-bundle as defense in depth |
| `spec-tooling/` | Lockfile-pinned `@redocly/cli` — `npm ci` verifies the pinned tarball's integrity hash; the workflow cross-checks the installed version against `REDOCLY_VERSION` and refuses drift |
| `generator-pin.yaml` | Generator toolchain pin (ADR-SDK-023) — stage 2's input; upgrades are ADR revisions riding PRs where the regeneration diff makes the blast radius reviewable |

## One-time CI provisioning: `SPEC_ARTIFACT_READ_TOKEN`

The platform repo is **private**, and a workflow's default `GITHUB_TOKEN` is scoped to this
repo only — it cannot read the platform repo's releases. Stage 1 therefore needs one repo
secret:

- **Name:** `SPEC_ARTIFACT_READ_TOKEN`
- **Value:** a fine-grained PAT — resource: the platform repo (`repo:` in `../spec/pin.yaml`)
  **only**; permissions: **Contents: read-only** (+ implicit Metadata). Nothing else.
- **Set:** `gh secret set SPEC_ARTIFACT_READ_TOKEN -R FlexPay-io/RAP-sdk`
  (or repo Settings → Secrets and variables → Actions).
- Until it exists, stage 1 **fails closed** with a provisioning message — deliberately: a
  silently skipped verification would conflate "gate passed" with "gate never ran".
- Rotate on expiry; replace when the platform repo changes org (ADR-SDK-022 rename).

## Stage roadmap (build order)

Stage 2 (generate ×6, per-language configs under `pipeline/<language>/`) → stage 3
(build + test, any language red blocks all) → stage 4 (contract smoke vs Sandbox,
Enablement-issued key, ADR-SDK-014) → stages 5–6 (package / publish — embargoed; per-language
release tags drive the matrix). Each stage appends a job to `pipeline.yml` chained with
`needs:`.
