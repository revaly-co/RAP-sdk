# RAP Integration SDK — Registry Provisioning Runbook

**Status:** OQ-3 **naming closed** (ADR-SDK-030, 2026-07-30); namespaces reserved on all six
registries; **exactly two provisioning acts outstanding** (NuGet ID-prefix reservation, PyPI
org approval). Publish still embargoed.
**Last updated:** 2026-07-30
**Owner:** Leadership (custody) + SC squad (execution), per ADR-SDK-011 / OQ-3
**Source of truth:** ADR-SDK-011 (accounts leadership-owned), ADR-SDK-013 (publish gate),
ADR-SDK-019 (license), ADR-SDK-022 (GitHub namespace), ADR-SDK-030 (final names). This runbook
records execution state; the ADRs decide policy.

This is the human-readable record of where the SDK's six package-registry namespaces stand,
who owns them, and how publishing will work. It is a status + how-it-works doc, not a
decision doc.

## The one rule that governs everything here

**Publishing is embargoed** (CLAUDE.md rule 3). No registry publish, no OIDC
trusted-publisher registration, and no registry tokens until all three gates close:

1. GitHub namespace is final (ADR-SDK-022) — **satisfied** (repo at `revaly-co/RAP-sdk`
   since 2026-07-17).
2. Registry accounts + the protected publish environment exist (OQ-3, ADR-SDK-011/013) —
   **nearly satisfied**: namespaces reserved ×6, the `publish` GitHub environment created
   2026-07-29 (per-language tag-pattern deployment policies; `languages/go/v*` deliberately
   excluded until the Go publish ceremony). Two acts remain — see the table below.
3. Apache-2.0 is Legal-ratified (ADR-SDK-019) — **pending in writing** (approval exists
   verbally as of 2026-07-29; the embargo holds until the written record lands).

**Pre-1.0 betas count as publishing.** Until the gates close, distribution is per-language
**GitHub release artifacts** from this repo, not registry packages (ADR-SDK-026).

## Current state — what is left, per registry

Names are final (ADR-SDK-030). "Publish-day" items are embargoed behind gate 3 and executed
only from the gated pipeline's protected environment (ADR-SDK-013).

| Registry | Final name | Namespace held | Outstanding **now** | Publish-day (embargoed) |
| --- | --- | --- | --- | --- |
| npm | `@revaly/sdk` | ✅ org `revaly` (2026-07-17; owns the `@revaly` scope) | — | OIDC trusted publisher · `package.json` rename to `@revaly/sdk` + quickstart install-line sweep (stage-6 prep, ADR-SDK-030) |
| PyPI | `revaly-sdk` | ⏳ org application **pending PyPI approval** | **Org approval** — in PyPI's queue; the only namespace still not held. Interim custody: pending-publisher under a user account, transferred to the org later (recorded deviation) | OIDC trusted publisher |
| NuGet | `Revaly.Sdk` + `Revaly.Sdk.Core` | ✅ org (2026-07-17; access confirmed 2026-07-30) | **`Revaly.*` ID-prefix reservation** — email request to account@nuget.org (owner display name + prefix); days-to-weeks turnaround — the live long-lead act | Trusted-publishing policy — created close to publish day (policies on private repos auto-expire after 7 unused days), by a leadership account that is an org member |
| Packagist | `revaly/sdk` | ✅ vendor `revaly` held via placeholder `revaly/rap-sdk` v0.0.1 (2026-07-17; verified live 2026-07-30) | — | Delete the placeholder; publish `revaly/sdk` from the public monorepo via webhook (see the deviation record below) |
| Maven Central | `co.revaly:revaly-sdk` | ✅ namespace `co.revaly` reserved + DNS-verified (2026-07-17; no publish needed to hold it) | — | GPG signing keys in Key Vault, fetched inside the environment-scoped job; publisher token |
| Go (pkg.go.dev) | `github.com/revaly-co/rap-sdk/languages/go` | ✅ n/a — the path binds to the GitHub org (ADR-SDK-022) | — | Repo public + a `languages/go/v*` tag; the tag ruleset currently **blocks** go-module-form tags, and lifting it is the deliberate admin ceremony (ADR-SDK-026). Go publishes **last** |

Namespace URLs and the owning group-email address live in the corporate secret store, not in
this repo (the repo is public per ADR-SDK-012).

## Ownership and custody (ADR-SDK-011)

- **Leadership-owned, under a group email**, never an individual's mailbox. Registry account
  loss or hijack is a supply-chain incident on merchant payment systems, so custody sits with
  the accountable owners.
- **2FA enforced on every org**, with recovery codes in the corporate secret store. This is
  part of provisioning acceptance, not an afterthought.
- **The `security@` disclosure mailbox is live** (2026-07-29) and referenced by the repo's
  `SECURITY.md` (merged 2026-07-30) — the ADR-SDK-012 precondition for first publish is met.
- **Squad engineers never get personal ownership or membership** of the orgs. Day-to-day
  publish rights come only from the pipeline's trusted-publishing configuration
  (ADR-SDK-013); owner credentials are break-glass.

> Because of the last point, there is no "add engineers as org members" step. If you were
> asked for teammates' registry usernames to add them to an org, that request should be
> dropped — it is contrary to ADR-SDK-011.

## How publishing will work (ADR-SDK-013)

- **One human act: cutting a release tag** on `main`. The publish job is restricted to
  release tags via environment deployment policy; tag creation is maintainer-only.
- **Per registry:**
  - **npm / PyPI / NuGet** — OIDC trusted publishing (no stored tokens), registered only at
    publish day (gate 3).
  - **Maven Central** — GPG signing; keys in Key Vault, fetched inside the
    environment-scoped job. Access is by publisher token, not by adding member usernames
    (Maven Central has no member model).
  - **Packagist** — webhook from the public repo; the tag drives it.
  - **pkg.go.dev** — pull-based; the tag is the release.
- Per-language tags (for example `dotnet/v1.0.0`) drive the publish matrix. Every published
  version maps to a spec commit SHA in its release notes.

## Final package names (ADR-SDK-030)

Finalized 2026-07-30 — `runtime-tdd.md` §7 is the normative surface; this table mirrors it.

| Registry | Final name |
| --- | --- |
| npm | `@revaly/sdk` (scoped) |
| PyPI | `revaly-sdk` |
| NuGet | `Revaly.Sdk` + `Revaly.Sdk.Core` |
| Packagist | `revaly/sdk` |
| Maven Central | `co.revaly:revaly-sdk` |
| Go | `github.com/revaly-co/rap-sdk/languages/go` (subdir module) |

## Known deviation: the temporary Packagist placeholder

Packagist is the only one of the six that **cannot reserve a vendor namespace without
publishing an actual package**. To hold `revaly/` during Week 1, a placeholder was published:

- **Package:** `revaly/rap-sdk` v0.0.1, sourced from a standalone repo `revaly-co/rap-sdk-php`
  with a hand-written `composer.json`.
- **What it deviates from:**
  - **ADR-SDK-019** — it is licensed **MIT**, but the SDK license is **Apache-2.0**, and no
    publish of any kind is meant to happen before Legal ratifies.
  - **CLAUDE.md rule 3 / ADR-SDK-013** — it is a manual publish outside the gated pipeline
    and protected environment. Pre-1.0 counts as publishing.
  - **ADR-SDK-016 / ADR-SDK-012** — the SDK is one monorepo with generated cores; a
    standalone hand-written PHP repo is off-architecture, and Packagist is meant to be fed by
    webhook from the monorepo.
  - **Naming** — it uses `revaly/rap-sdk`; the final name is `revaly/sdk` (ADR-SDK-030).
- **Decision (Charles, 2026-07-17):** keep the placeholder as a deliberate temporary
  namespace-hold; **delete it and publish `revaly/sdk` through the gated pipeline**
  (Apache-2.0, from the public monorepo) when the publish gates close.
- **Owner:** SC squad (execution) — remove the placeholder as part of the first real
  Packagist publish.

## Open items

Done and dated: ✅ names final (ADR-SDK-030, 2026-07-30) · ✅ `security@` mailbox live +
`SECURITY.md` merged (2026-07-29/30) · ✅ `publish` environment with tag-pattern policies
(2026-07-29) · ✅ npm / NuGet / Maven / Packagist namespaces held (2026-07-17).

| Item | Owner | Gate |
| --- | --- | --- |
| **PyPI org approval** (application pending in PyPI's queue) | SC squad | Before first PyPI publish |
| **NuGet ID-prefix (`Revaly.*`) reservation** — email act, days-to-weeks | SC squad | Before first NuGet publish; start immediately |
| Apache-2.0 Legal ratification **in writing** (verbal 2026-07-29) | Leadership + Legal | Before first publish (ADR-SDK-019); also gates every OIDC registration |
| OIDC / GPG / webhook bindings + npm `@revaly/sdk` metadata rename (stage-6 prep) | SC squad + DevOps | Publish day, after the written ratification (ADR-SDK-013/030) |
| Delete the Packagist placeholder; publish `revaly/sdk` via pipeline | SC squad | First gated Packagist publish |
