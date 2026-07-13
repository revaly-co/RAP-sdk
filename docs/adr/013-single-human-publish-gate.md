# ADR-SDK-013 — Publish Protection: Exactly One Human Gate (the Release Cut); Everything Else Is a Machine Gate

**Status:** Accepted — decided 2026-07-10 (D-13, superseding the earlier double-gate design); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §3.1 / §7 ("Publish protection prerequisite"), decision D-13 · inline review thread (human-gate justification, 2026-07-09/10)
**Owner:** SC squad (per ADR-SDK-018)

## Context

Registry publishes are **irreversible** — a published version can be deprecated or yanked but never
unpublished-as-if-it-never-existed, and Go module proxies cache every published version forever.
At decision time, FlexPay GitHub environments had **zero protection rules** (verified 2026-06-30),
and several repos could deploy to production from any branch. With LLM-driven development, an
agent-authored branch could otherwise trigger an irreversible public publish.

The first design stacked two human gates: PR review to `main` **plus** a required-reviewer approval
on the publish environment. Review pushback (2026-07-10): agreed on protection in principle,
"frown on a double human gate."

## Problem

Guarantee that publishes happen only from a protected ref, deliberately, exactly once per release —
without stacking redundant human approvals that slow every release and train reviewers to
rubber-stamp.

## Decision

**The only human act in the publish path is cutting the release.** All other protection is
mechanical:

1. **Environment deployment policy:** the publish job runs **solely from a release tag on
   `main`** — the GitHub environment's deployment branch/tag policy enforces this; no user branch
   can ever reach the publish job.
2. **Tag protection:** release-tag creation is restricted to maintainers.
3. **OIDC trusted publishing** binds the registry side to exactly this repository + environment
   (npm, PyPI, NuGet); Maven Central uses GPG signing with keys in Key Vault; pkg.go.dev is
   pull-based off the tag.
4. **The required-reviewer approval on the publish environment is dropped.** PR review to `main`
   is a code gate that exists regardless of publishing — it no longer stacks a second human on the
   publish path.

## Rationale

- **The agent-authored-branch risk is fully handled by the ref policy alone:** such a branch can
  never reach the publish job, because the job only runs from a maintainer-created release tag on
  `main`.
- **One deliberate human decision** (cutting the release) is the meaningful control point; a second
  approval reviewing the same artifact adds latency, not safety, and degrades into ritual.
- Machine gates are deterministic and auditable; each maps to a specific failure mode: ref policy →
  wrong-source publish; tag protection → unauthorized release cut; OIDC binding → stolen-credential
  publish from elsewhere.

## Alternatives considered

- **Double human gate (PR review + environment required reviewer):** rejected by review — redundant
  human control on the same path.
- **No environment gating (rely on registry credentials as secrets):** rejected — long-lived
  secrets are the supply-chain attack surface OIDC trusted publishing exists to remove; and secrets
  don't constrain *which ref* publishes.
- **Publish on every merge to `main` (full CD):** rejected — removes the one deliberate human
  decision for an irreversible, versioned, consumer-facing artifact; release cadence is a product
  decision, not a merge side effect.

## Consequences

- Configuring the environment + tag protection is a **prerequisite of the first publish** (tracked
  under OQ-3, sequenced after the namespace decision, ADR-SDK-022). GitHub environments elsewhere
  in the org remain ungated — this repo must not inherit that default.
- The release cut becomes a checklist moment (versioning per `../pipeline-and-release.md`,
  vocabulary pass per ADR-SDK-010, release notes with spec SHA per ADR-SDK-006).
- A failed pipeline stage after the tag (build, contract smoke) means **no publish** — the tag can
  exist without artifacts; publishing resumes only via a new tag after the fix (never by manual
  re-run against edited state).
- Trusted-publisher registrations must be re-established if the repo identity ever changes — which
  is why they are configured only after the namespace is final (ADR-SDK-022).

## Implementation guidance

- GitHub environment `publish`: deployment policy = tags matching the release pattern (e.g.
  `v*.*.*` and per-language tags per the monorepo scheme, ADR-SDK-016) on `main` only; secrets
  scoped to that environment; no required reviewers.
- Tag protection rule: release-tag pattern creatable by the maintainer team only.
- Per-registry mechanics: npm/PyPI/NuGet — OIDC trusted publishing (no stored tokens); Maven
  Central — GPG keys from Key Vault fetched inside the environment-scoped job; Packagist — webhook
  from the public repo; pkg.go.dev — nothing to push (tag is the release).
- CI asserts the machine gates themselves: a scheduled job fails loudly if the environment policy,
  tag protection, or trusted-publisher bindings drift from this ADR (config-as-code where the
  platform allows; explicit checks where it doesn't).
