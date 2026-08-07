# RAP Integration SDK — Maven Central Signing Key

**Status:** signing keypair **generated and vaulted 2026-08-06**. Nothing was published, no
registry was contacted, and no registry token exists. Publish remains embargoed (CLAUDE.md rule 3).
**Owner:** Leadership (custody, ADR-SDK-011) + SC squad (execution)
**Source of truth for policy:** ADR-SDK-011 (accounts leadership-owned), ADR-SDK-013 (the pipeline
is the publisher), ADR-SDK-019 (license gate). This document records execution state.

Maven Central is the only one of the six registries that requires artifact signing rather than a
trusted-publisher relationship, so its signing material has to exist before flip day rather than
being created during it. This is the record of that key: what it is, where it lives, what still
has to happen before the java publish path can run, and what an incident responder needs to know.

**Infrastructure identifiers are deliberately absent.** The Key Vault name, resource group,
subscription, and tenant are not recorded here — they live in the corporate secret store, and the
pipeline reads the vault through the `PUBLISH_KEYVAULT_NAME` variable rather than a literal
(`.github/workflows/pipeline.yml`). Keep it that way; this repository goes public (ADR-SDK-012).

## The key

| Property | Value |
| --- | --- |
| Fingerprint | `07E856878E77A944169F56683ED2EB632E4EAAE7` |
| Algorithm | RSA-4096, sign-capable primary (`[SC]`) |
| Identity | `Revaly SDK Maven signing <packages@revaly.co>` — the group mailbox, never a personal address (ADR-SDK-011) |
| Created | 2026-08-06 |
| Expires | **2028-08-05** |

Generated in an isolated, short-path keyring on a leadership workstation, exported, vaulted, and
scrubbed locally in a single scripted ceremony. After the scrub the private key exists **only** in
the publish Key Vault. Rehearsed end-to-end against the staging vault on 2026-08-05 before the
production run.

## What is in the vault

Four secrets, all tagged `purpose=maven-central-signing custody=leadership`, created
2026-08-06 12:47 UTC:

| Secret | Read by the pipeline? | Notes |
| --- | --- | --- |
| `maven-gpg-private-key` | **yes** — stage 6, java live only | ASCII-armored secret key |
| `maven-gpg-passphrase` | **yes** — stage 6, java live only | |
| `maven-gpg-public-key` | no | custody copy; also what goes to the keyserver |
| `maven-gpg-revocation-cert` | no | custody copy — see the incident notes below |
| `maven-central-token` | **yes**, when it exists | **not created** — registry credential, embargoed |

Nobody needs the private key or the passphrase on a workstation. The pipeline fetches them in-job
inside the protected `publish` environment (ADR-SDK-013), and local signing work should use a
throwaway key. Requesting a copy of either is a custody violation, not a convenience.

## Still outstanding before the java publish path can run

The key alone does not make stage 6 work. In dependency order:

1. **Azure workload identity + scoped read access.** The publish job authenticates with
   `azure/login` over OIDC and then reads the vault. That needs a dedicated user-assigned managed
   identity, a federated credential for this repository's `publish` environment, and
   `Key Vault Secrets User` scoped **to the individual secrets** rather than the whole vault — it
   is a shared vault holding unrelated production secrets. Then set `PUBLISH_AZURE_CLIENT_ID`,
   `PUBLISH_AZURE_TENANT_ID`, `PUBLISH_AZURE_SUBSCRIPTION_ID`, and `PUBLISH_KEYVAULT_NAME` on the
   `publish` environment. Requires production access; assign accordingly.
   - The federated credential's subject uses the **immutable-ID** form
     (`repo:<owner>@<owner_id>/<repo>@<repo_id>:environment:publish`), not the path form. Derive it
     rather than hand-typing it:
     `gh api /repos/revaly-co/RAP-sdk/actions/oidc/customization/sub --jq .sub_claim_prefix`, then
     append `:environment:publish`. A wrong subject fails at login with
     `AADSTS70021: No matching federated identity record found`.
   - The repository ID is **stable from here**: the ADR-SDK-032 cutover already executed
     (2026-08-05), so this repo is the final one and the remaining public flip does not change its
     ID. The credential does not need recreating later.
   - Give the SDK/DevOps group `Managed Identity Contributor` scoped to that one identity so the
     binding can be maintained without going back to leadership each time.
2. **`maven-central-token`.** A Central Portal token — a registry credential, so it stays a
   flip-runbook act under rule 3 (the ADR-SDK-019 written ratification was recorded 2026-08-06,
   so Legal no longer blocks it). Two minutes on flip day — but note the fetch step reads it
   **unconditionally**, so the java live path fails without it. Do not meet that failure for the
   first time on flip day.
3. **Public key on a keyserver.** Central will not accept a signed bundle until the public key is
   published: `gpg --keyserver keyserver.ubuntu.com --send-keys 07E856878E77A944169F56683ED2EB632E4EAAE7`.
   This is public and permanent — keyservers never delete — so it is deliberately deferred, but do
   it a few days before flip so propagation is not on the critical path.
4. **The javadoc-jar gap — closed 2026-08-07.** Stage 5 now builds sources + javadoc jars for
   both artifacts (core pom template doclint fork + runtime pom source/javadoc plugins); the
   stage-6 flip-readiness lint enforces their presence.

## Incident and custody notes

- **The revocation certificate has a colon in front of the armor header.** GnuPG deliberately
  inserts `:` before `-----BEGIN PGP PUBLIC KEY BLOCK-----` so the certificate cannot be imported
  by accident. Strip it before use. Finding this out mid-incident wastes the time you have least
  of.
- **The vaulted key is the primary, not a subkey.** Revoking it revokes the signing identity
  outright. The conventional split — a certify-only primary kept offline and a signing subkey in
  CI — was deliberately not used, because the production run intentionally did not vary from the
  ceremony rehearsed in staging. Revisit it at rotation, when there is time to rehearse the
  change.
- **Keep a copy of the revocation certificate in the corporate secret store**, alongside the org
  recovery codes. Vault plus corporate store is the ADR-SDK-011 custody pattern; a revocation
  certificate that only exists inside the vault it protects is not a recovery plan.
- **Rotation is due before 2028-08-05** and is the same ceremony re-run. Rotation is a feature of
  the two-year expiry, not an incident.

## Governance — recorded deviation

`docs/registry-provisioning.md` § Flip to LIVE places "GPG keypair → Key Vault" inside flip act 6,
behind all three gates, and `docs/open-items.md` OQ-3 lists Maven GPG keys in Key Vault as
publish-day work embargoed until the ADR-SDK-019 **written** ratification. Generating and vaulting
the key on 2026-08-06 pulled that act forward, ahead of gate 1.

Accepted by Charles (2026-08-06) on the same basis as the Packagist placeholder deviation, and
recorded here rather than left implicit. What makes it narrow:

- A GPG keypair is **signing** material, not a registry credential. It cannot publish anything.
- **No registry was contacted**, no Central Portal token was created, and nothing was made public
  — the keyserver upload, which is the irreversible public act, was explicitly deferred.
- The embargo guards are untouched: `REGISTRY_PUBLISH_MODE` is unchanged, and the npm `"private"`
  and PyPI `Private :: Do Not Upload` guards remain in place. Stage 6 still runs DARK
  (ADR-SDK-031).

Net effect on the runbook: flip act 6 reduces to the Central Portal token, the workload-identity
bindings, and the keyserver upload.

**Postscript (2026-08-06):** the ADR-SDK-019 written ratification was recorded later the same
day (ADR-SDK-019 § Ratification record) — gate 1 of the flip runbook is closed and this
deviation's head start shrank to hours. The token, the keyserver upload, and the bindings
remain flip-runbook acts.
