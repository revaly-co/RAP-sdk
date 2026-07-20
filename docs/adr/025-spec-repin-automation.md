# ADR-SDK-025 — Spec Re-Pin Automation: Consumer Watchdog Now, Producer Dispatch When Credentialed

**Status:** Accepted — 2026-07-19 (design approved by Dimitri in the build session; **tier 1
implemented same day** — `.github/workflows/spec-freshness.yml`; **tier 2 pending** the
cross-repo credential, tracked as OQ-17 in `../open-items.md`)
**Source:** post-RFC. ADR-SDK-006 makes the pinned gated artifact the only spec input and
`../pipeline-and-release.md` §2 defines the re-pin flow, but nothing *initiates* it — the
platform publishes `spec/v*` releases and the SDK repo finds out only when a human remembers.
First live exposure: the platform's spec-reality alignment (Backbone PR #251 → `spec/v2.3.0`).
**Owner:** SC Eng + DevOps (ADR-SDK-018)

## Context

Backbone publishes gated spec artifacts (`spec/v<version>+<shortsha>` GitHub Releases, platform
ADR 016) whenever `Docs/**` changes land on its main. The SDK consumes exactly one of them via
`spec/pin.yaml` (ADR-SDK-006), bumped by PR only. Between those two facts sits an unmanaged
hand-off: nothing tells this repo a newer artifact exists. The failure mode is silent staleness —
SDKs generated from a superseded contract, quickstarts drifting from reality, and release notes
mapping package versions to an old spec commit.

Constraints that shaped the design:

- Both repos are private; the default `GITHUB_TOKEN` is repo-scoped, so **any** cross-repo
  signal (producer→consumer dispatch) needs a provisioned credential — the same fine-grained-PAT
  family as `SPEC_ARTIFACT_READ_TOKEN`, whose post-migration re-provisioning is already parked
  under OQ-3. That credential does not exist yet; the reminder problem does.
- The platform's `spec-artifact.yml` creates releases with `GITHUB_TOKEN`, so release-triggered
  workflows are suppressed even inside the platform repo — notification cannot ride the release
  event; it must be an explicit dispatch step or a consumer-side poll.
- Renovate's `github-releases` datasource could watch the tags but cannot perform the gated
  re-pin (checksum + provenance verification, regen ×6) — a custom workflow is needed either
  way, so a dependency bot adds a system without removing one. Rejected.
- Chat notification (Teams) is the weakest "don't forget" primitive and is deliberately not
  wired for spec releases platform-side. Rejected as a mechanism (fine as garnish later).

## Decision

Two tiers, shipped in reverse order of value because tier 1 has no credential dependency:

1. **Tier 1 — consumer-side watchdog (implemented).** `spec-freshness.yml`, nightly 06:15 UTC
   + manual dispatch: list the platform's `spec/v*` releases with `SPEC_ARTIFACT_READ_TOKEN`
   (Contents: read — the secret pipeline stage 1 already holds), resolve the highest semver
   (platform ADR 019 guarantees one tag per version), and compare against `spec/pin.yaml`:
   - **Pin current** → close any open `spec-repin` issues (the pin caught up); green.
   - **Pin behind** → close issues for superseded versions, then ensure **exactly one** open
     issue titled `chore(spec): re-pin to <tag>` (label `spec-repin`) carrying the full re-pin
     checklist — pin fields + committed checksum/provenance copies, regen ×6, stages 1–3,
     quickstart sweep, open-string/verdict review, spec-gap marker resolution, release-notes
     SHA mapping. The trigger solves "forgot to start"; the template solves "forgot a step."
   - **Suppression:** an open PR on branch `repin/spec-v<version>` (or naming the tag) mutes
     issue creation — the PR *is* the reminder. This branch convention is load-bearing and is
     what tier 2's auto-PR will use.
   - **Pin ahead of visible releases** → fail: that state is impossible under append-only spec
     history and means the token lost scope or the listing broke.
   - **Fail-closed throughout** (platform ADR 012 lesson): missing token or empty listing turns
     the run red after three attempts — "detector fired" and "detector never ran" are never
     conflated. Empirical note: the releases endpoint reproducibly 503s at `per_page=100` on
     the platform repo (found in the 2026-07-19 dry run) — the workflow walks default-sized
     pages instead.

2. **Tier 2 — producer-side dispatch → draft re-pin PR (pending OQ-17).** When the cross-repo
   credential lands: the platform's `spec-artifact.yml` gains a final `repository_dispatch`
   step to this repo carrying `{tag, specVersion, sha256, sourceCommit}`; a receiving workflow
   here opens a **draft re-pin PR** on `repin/spec-v<version>` — download + verify the artifact
   (checksums, provenance), rewrite `spec/pin.yaml` and the committed copies, run
   `pipeline/generate.sh` ×6, commit the regen diff — so the reminder arrives as a red-or-green
   PR with stages 1–3 already executed against the new spec. Merging stays human (branch
   protection; ADR-SDK-006's "pin bumped by PR only" is satisfied — review is the gate, not
   authorship). Tier 1 then demotes to the backstop that only speaks when the push path
   silently broke (failed dispatch step, expired credential, manually-created release).

## Consequences

- Staleness is now bounded at 24 h (tier 1) and drops to minutes at tier 2 — including for the
  P-2 `SafeToFailover` minor release, which rides this same rail when it ships.
- One idempotent issue per artifact version; no duplicate nagging, self-closing, self-superseding.
  Issue titles carry the release tag — retitling breaks idempotency; don't.
- The `repin/spec-v<version>` branch convention is contract: tier 1 uses it to stand down,
  tier 2 creates it. Manual re-pins should adopt it too.
- A red `Spec Freshness` run is a real signal by design (token health, API breakage, or the
  impossible pin-ahead state) — it must not be ignored or made advisory.
- Tier 2 adds a credential with **write** reach into this repo from the platform workflow
  (dispatch) and PR-creation rights here; scope it minimally (org GitHub App preferred over a
  long-lived PAT if provisioning allows) — decided at OQ-17 execution.
- New label `spec-repin`; the workflow (re)creates it idempotently.
