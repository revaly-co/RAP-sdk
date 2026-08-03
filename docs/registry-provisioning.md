# RAP Integration SDK — Registry Provisioning Runbook

**Status:** OQ-3 **naming closed** (ADR-SDK-030, 2026-07-30); namespaces reserved on all six
registries; **NuGet `Revaly.*` ID-prefix RESERVED 2026-08-03** (NuGet.org admin confirmation to
the owner mailbox — one business day after the 2026-07-31 resubmission). **One provisioning act
still sits in an external queue** (PyPI org approval). Publish still embargoed.
**Last updated:** 2026-08-03
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
   excluded until the Go publish ceremony), NuGet `Revaly.*` ID-prefix reserved 2026-08-03.
   One act remains — PyPI org approval (see the table below).
3. Apache-2.0 is Legal-ratified (ADR-SDK-019) — **pending in writing** (approval exists
   verbally as of 2026-07-29; the embargo holds until the written record lands).

**Pre-1.0 betas count as publishing.** Until the gates close, distribution is per-language
**GitHub release artifacts** from this repo, not registry packages (ADR-SDK-026).

## Current state — what is left, per registry

Names are final (ADR-SDK-030). "Publish-day" items are embargoed behind gate 3 and executed
only from the gated pipeline's protected environment (ADR-SDK-013).

| Registry | Final name | Namespace held | Outstanding **now** | Publish-day (embargoed) |
| --- | --- | --- | --- | --- |
| npm | `@revaly/sdk` | ✅ org `revaly` (2026-07-17; owns the `@revaly` scope) · ✅ `package.json` renamed to `@revaly/sdk` 2026-08-03 (stage-6 prep, ADR-SDK-030/031) | — | OIDC trusted publisher · quickstart install lines switch to `npm install @revaly/sdk` at flip |
| PyPI | `revaly-sdk` | ⏳ org application **pending PyPI approval** | **Org approval** — in PyPI's queue; the only namespace still not held. Interim custody: pending-publisher under a user account, transferred to the org later (recorded deviation) | OIDC trusted publisher |
| NuGet | `Revaly.Sdk` + `Revaly.Sdk.Core` | ✅ org (2026-07-17; access confirmed 2026-07-30) · ✅ **`Revaly.*` ID-prefix reserved 2026-08-03** — NuGet.org admin: "reserved the prefix 'Revaly' for account 'revaly'", confirmed to the owner mailbox one business day after the 2026-07-31 resubmission (first send had bounced the sender-identity check: registry support requests must originate **from the email registered to the account**) | — | Trusted-publishing policy — created close to publish day (policies on private repos auto-expire after 7 unused days), by a leadership account that is an org member |
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

## Flip to LIVE — runbook (ADR-SDK-031)

The stage-6 registry job ships **dark** on every release tag: full rehearsal in the protected
`publish` environment, a per-release flip-readiness report, **no registry contact**. The flip
is **double-keyed** — the `REGISTRY_PUBLISH_MODE=live` repo variable **and** the guard-removal
PR (steps 4/8 below); either alone hard-fails rather than publishes. Going live is this
runbook, not a build. Per-registry push mechanics (which push lives in the workflow vs in
`pipeline/registry-publish.sh`, and why npm and Go have no visible workflow steps):
`pipeline-and-release.md` §3.1.

**Gates first (nothing below runs until all three close):**

1. **ADR-SDK-019 written ratification recorded.** The fill-and-sign PDF is the artifact;
   the 2026-07-29 verbal approval and Charles's 2026-07-31 Teams confirmation do not close
   the gate.
2. **PyPI org approved** (or the recorded pending-publisher deviation accepted for launch).
3. **Git-history decision executed and repo → public** (leadership; ADR-SDK-012). Public is
   required for npm `--provenance`, the Packagist webhook, and pkg.go.dev.

**Flip acts (one sitting — cut no release tags while between steps 4 and 8):**

4. **Guard-removal PR:** delete `"private": true` from `languages/typescript/package.json`
   and the `Private :: Do Not Upload` classifier from `languages/python/pyproject.toml`.
   (Between this merge and step 8, a release tag would hard-fail the registry job's
   half-flip check — by design. Do 4→8 in one sitting.)
5. **OIDC trusted publishers:** npm (`@revaly/sdk` → this repo + `pipeline.yml` +
   environment `publish`), PyPI (`revaly-sdk`), NuGet trusted-publishing policy (by a
   leadership org-member account; policies expire after 7 unused days — create last) + set
   the `NUGET_TRUSTED_PUBLISHING_USER` variable.
6. **Maven Central:** GPG keypair → Key Vault (`maven-gpg-private-key`,
   `maven-gpg-passphrase`), public key → keyservers, Central Portal token →
   `maven-central-token`; federated credential for the `publish` environment +
   `PUBLISH_AZURE_CLIENT_ID/TENANT_ID/SUBSCRIPTION_ID` + `PUBLISH_KEYVAULT_NAME` variables.
   **Fix the javadoc-jar gap first** (standing flip-readiness finding: stage 5 skips
   javadoc; Central rejects bundles without it).
7. **Packagist:** provision `PACKAGIST_MIRROR_PUSH_TOKEN` (environment secret; prefer an
   org GitHub App scoped to `revaly-co/rap-sdk-php` — same credential family as OQ-17);
   register the Packagist webhook on the mirror; **delete the placeholder `revaly/rap-sdk`**
   immediately before the first real publish (the recorded deviation closes then).
8. **Set `REGISTRY_PUBLISH_MODE=live`** (repository variable).
9. **Cut release tags in GA order** (ADR-SDK-015): dotnet → java → php → typescript →
   python — **one tag per push** (a multi-tag push silently starts zero runs). Each tag:
   GitHub release first (unchanged, stays the provenance anchor per ADR-SDK-031), then the
   registry publish; verify on the registry before the next tag. Go remains the separate,
   last `languages/go/v*` ceremony (ADR-SDK-026: lift the tag ruleset, tag, verify
   pkg.go.dev).
10. **Post-flip sweep:** quickstart install lines ×6 switch to registry installs;
    `revaly-co/RAP-sdk-integration-tests` updates its TypeScript import to `@revaly/sdk`
    (single known external consumer of the old specifier) and gains a registry-install
    variant; arm the ADR-SDK-013 drift check for the new bindings; announce per DX
    contract §e.

## Open items

Done and dated: ✅ names final (ADR-SDK-030, 2026-07-30) · ✅ `security@` mailbox live +
`SECURITY.md` merged (2026-07-29/30) · ✅ `publish` environment with tag-pattern policies
(2026-07-29) · ✅ npm / NuGet / Maven / Packagist namespaces held (2026-07-17) · ✅ NuGet
`Revaly.*` ID-prefix reserved (2026-08-03).

| Item | Owner | Gate |
| --- | --- | --- |
| **PyPI org approval** (application pending in PyPI's queue — the last provisioning act in an external queue) | SC squad | Before first PyPI publish |
| Apache-2.0 Legal ratification **in writing** (verbal 2026-07-29) | Leadership + Legal | Before first publish (ADR-SDK-019); also gates every OIDC registration |
| OIDC / GPG / webhook bindings (the npm `@revaly/sdk` metadata rename shipped 2026-08-03 with the stage-6 prep) | SC squad + DevOps | Publish day, after the written ratification (ADR-SDK-013/030/031) |
| Delete the Packagist placeholder; publish `revaly/sdk` via pipeline | SC squad | First gated Packagist publish |
