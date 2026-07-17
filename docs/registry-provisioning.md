# RAP Integration SDK — Registry Provisioning Runbook

**Status:** OQ-3 in progress (Week 1). Namespaces reserved on all six registries; publish still embargoed.
**Last updated:** 2026-07-17
**Owner:** Leadership (custody) + SC squad (execution), per ADR-SDK-011 / OQ-3
**Source of truth:** ADR-SDK-011 (accounts leadership-owned), ADR-SDK-013 (publish gate), ADR-SDK-019 (license), ADR-SDK-022 (GitHub namespace). This runbook records execution state; the ADRs decide policy.

This is the human-readable record of where the SDK's six package-registry namespaces stand, who owns them, and how publishing will work. It is a status + how-it-works doc, not a decision doc.

## The one rule that governs everything here

**Publishing is embargoed** (CLAUDE.md rule 3). No registry publish, no OIDC trusted-publisher registration, and no registry tokens until all three gates close:

1. GitHub namespace is final (ADR-SDK-022) — **satisfied** (repo lives at `revaly-co/RAP-sdk` since 2026-07-17).
2. Registry accounts + the protected publish environment exist (OQ-3, ADR-SDK-011/013) — **in progress**.
3. Apache-2.0 is Legal-ratified (ADR-SDK-019) — **pending**.

**Pre-1.0 betas count as publishing.** Until the gates close, interim distribution is per-language **GitHub release artifacts** from this repo, not registry packages.

## Current state

| **Registry** | **Language** | **Namespace reserved** | **Status** |
| --- | --- | --- | --- |
| npm | TypeScript | org `revaly` | Reserved (org only, no package) |
| PyPI | Python | org `revaly` | Org application **pending PyPI approval**; user account active |
| NuGet | .NET | org `revaly` | Reserved (org only); ID-prefix reservation still to do |
| Packagist | PHP | vendor `revaly` | **Deviation:** claimed via a temporary placeholder publish (see below) |
| Maven Central | Java | namespace `co.revaly` | Reserved + DNS-verified (no publish needed to hold it) |
| Go | Go | `github.com/revaly-co/...` | No registry account; module path binds to the GitHub org (ADR-SDK-022) |

Namespace URLs and the owning group-email address live in the corporate secret store, not in this repo (this repo goes public per ADR-SDK-012).

## Ownership and custody (ADR-SDK-011)

- **Leadership-owned, under a group email**, never an individual's mailbox. Registry account loss or hijack is a supply-chain incident on merchant payment systems, so custody sits with the accountable owners.
- **2FA enforced on every org**, with recovery codes in the corporate secret store. This is part of provisioning acceptance, not an afterthought.
- **A `security@` disclosure mailbox** (ADR-SDK-012) is provisioned under the same group-email constraint and must be live and referenced by `SECURITY.md` before first publish. **Still open.**
- **Squad engineers never get personal ownership or membership** of the orgs. Day-to-day publish rights come only from the pipeline's trusted-publishing configuration (ADR-SDK-013); owner credentials are break-glass.

> Because of the last point, there is no "add engineers as org members" step. If you were asked for teammates' registry usernames to add them to an org, that request should be dropped — it is contrary to ADR-SDK-011.

## How publishing will work (ADR-SDK-013)

- **One human act: cutting a release tag** on `main`. The publish job is restricted to release tags via environment deployment policy; tag creation is maintainer-only.
- **Per registry:**
  - **npm / PyPI / NuGet** — OIDC trusted publishing (no stored tokens), registered only after the namespace is final.
  - **Maven Central** — GPG signing; keys in Key Vault, fetched inside the environment-scoped job. Access is by publisher token, not by adding member usernames (Maven Central has no member model).
  - **Packagist** — webhook from the public repo; the tag drives it.
  - **pkg.go.dev** — pull-based; the tag is the release.
- Per-language tags (for example `dotnet/v1.0.0`) drive the publish matrix. Every published version maps to a spec commit SHA in its release notes.

## Proposed package names (not yet final)

Names are **[Proposed]** until OQ-3 finalizes them (`runtime-tdd.md` §7). Do not hardcode them as final.

| **Registry** | **Proposed name** |
| --- | --- |
| npm | `revaly-sdk` (or `@revaly/sdk` if the org scope is preferred) |
| PyPI | `revaly-sdk` |
| NuGet | `Revaly.Sdk` |
| Packagist | `revaly/sdk` |
| Maven Central | `co.revaly:revaly-sdk` |
| Go | `github.com/revaly-co/rap-sdk/languages/go` (subdir module) |

## Known deviation: the temporary Packagist placeholder

Packagist is the only one of the six that **cannot reserve a vendor namespace without publishing an actual package**. To hold `revaly/` during Week 1, a placeholder was published:

- **Package:** `revaly/rap-sdk` v0.0.1, sourced from a standalone repo `revaly-co/rap-sdk-php` with a hand-written `composer.json`.
- **What it deviates from:**
  - **ADR-SDK-019** — it is licensed **MIT**, but the SDK license is **Apache-2.0**, and no publish of any kind is meant to happen before Legal ratifies.
  - **CLAUDE.md rule 3 / ADR-SDK-013** — it is a manual publish outside the gated pipeline and protected environment. Pre-1.0 counts as publishing.
  - **ADR-SDK-016 / ADR-SDK-012** — the SDK is one monorepo with generated cores; a standalone hand-written PHP repo is off-architecture, and Packagist is meant to be fed by webhook from the (not-yet-public) monorepo.
  - **Naming** — it uses `revaly/rap-sdk`, while the proposed working name is `revaly/sdk`.
- **Decision (Charles, 2026-07-17):** keep the placeholder as a deliberate temporary namespace-hold; **delete it and republish `revaly/...` through the gated pipeline** (Apache-2.0, from the public monorepo) when the publish gates close. Tracked as an OQ-3 follow-up.
- **Owner:** SC squad (execution) — remove the placeholder as part of the first real Packagist publish.

## Open items

| **Item** | **Owner** | **Gate** |
| --- | --- | --- |
| PyPI org approval (application pending) | SC squad | Before first PyPI publish |
| NuGet ID-prefix (`Revaly.*`) reservation | SC squad | Before first NuGet publish |
| `security@` disclosure mailbox live + `SECURITY.md` | Leadership + SC squad | Before first publish (ADR-SDK-012) |
| Finalize package names (resolve `revaly/rap-sdk` vs `revaly/sdk`) | SC Eng | OQ-3 close |
| Delete the Packagist placeholder; republish via pipeline | SC squad | First gated Packagist publish |
| Apache-2.0 Legal ratification | Leadership + Legal | Before first publish (ADR-SDK-019) |
| Protected publish environment + OIDC/GPG bindings | SC squad + DevOps | Before first publish (ADR-SDK-013) |
