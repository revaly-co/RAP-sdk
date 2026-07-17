# ADR-SDK-022 — GitHub Namespace: Create `rap-sdk` Under the Existing `revaly-co` Org; Park `FlexPay-io` Permanently

**Status:** Accepted — decided 2026-07-10 (OQ-15); ratified with RFC-046 approval 2026-07-10;
**namespace landed 2026-07-17** (see Implementation status below)
**Source:** RFC-046 §7 (namespace sequencing) / §11 OQ-15 / dependency map · blocking footer review thread 2026-07-08 + reply 2026-07-09
**Owner:** DevOps (SC squad, per ADR-SDK-018) + Leadership

## Context

The org's GitHub namespace migration (FlexPay-io → Revaly-co) was pending when review flagged it as
an unstated **blocking dependency**: several irreversible surfaces bind to the GitHub org name.
Analysis confirmed per binding:

1. **Go module path — the hardest binding.** The module path embeds the org
   (`github.com/<org>/rap-sdk/...`) and becomes a permanent identifier in merchant `go.mod` files;
   the Go module proxy **caches every published version forever, pre-1.0 betas included**. GitHub
   redirects do not apply to module identity. An abandoned org namespace is a **repo-jacking
   target** (namespace retirement protects only popular repos).
2. **OIDC trusted publishing / npm provenance — redirects do NOT satisfy them.** The OIDC token's
   `repository` claim carries the *current* owner; every trusted-publisher registration (npm,
   PyPI, NuGet) breaks on a rename until re-registered. Package ids themselves (`revaly-sdk-*`,
   group id `co.revaly`) do not embed the GitHub org — merchants other than Go are unaffected.
3. **Spec-artifact references** (platform repo) — internal and git-redirect-tolerant; not
   blocking.
4. **Release-note URLs** — redirect-tolerant as long as the old org is never deleted; not
   blocking.

## Problem

Sequence repo creation and publishing so that no irreversible surface ever bakes in a
namespace that is about to change — without coupling the SDK schedule to the full org migration.

## Decision

- **Create `rap-sdk` under the existing `revaly-co` GitHub org directly** (org created 2026-06-09,
  verified). **No dependency on the full FlexPay-io → Revaly-co migration** — the SDK is decoupled
  from it entirely.
- **`FlexPay-io` is parked permanently after any rename — never deleted**: parking keeps redirects
  alive for everything else and blocks namespace squatting/repo-jacking.
- **Publish order is fixed:** namespace final (satisfied by creating under `revaly-co`) →
  protected publish environment + trusted-publisher registration (OQ-3, ADR-SDK-013) → **any
  publish, pre-1.0 betas included**.
- The namespace gates **the first publish, not approval or build** — build, CI, and contract
  testing proceed regardless of org state.

## Rationale

- Creating under `revaly-co` directly is the cleanest path: it satisfies "namespace final" on day
  one, removes the SDK from the org-migration critical path, and means the Go module path
  (`github.com/revaly-co/rap-sdk/...`) is correct from the first tag.
- Trusted publishers are registered only after the namespace is final because re-registration is
  the *only* remedy when the `repository` claim changes — sequencing, not tolerance.

## Alternatives considered

- **Create under FlexPay-io now, rename later:** rejected — any Go publish (even a beta) bakes the
  old org into merchant imports permanently; every trusted-publisher config breaks at rename.
- **Wait for the full org migration:** rejected — couples the SDK to an org-wide program with its
  own timeline; the decision explicitly severs that dependency.
- **Treat GitHub redirects as sufficient:** rejected — confirmed insufficient for both OIDC claims
  and Go module identity (the two bindings that matter).

## Consequences

- OQ-3 (Week 1) executes against `revaly-co`: publish environment, tag protection,
  trusted-publisher registrations, registry orgs (ADR-SDK-011).
- The platform repo's location is irrelevant to SDK correctness (binding 3) — spec artifacts are
  consumed by reference and updated whenever the platform repo moves.
- The SC squad confirms the redirect findings as part of execution (ADR-SDK-018 item 3) — the
  findings above are recorded as review-confirmed 2026-07-09.
- Go's position last in GA order (ADR-SDK-015) adds slack on the highest-permanence surface.

## Implementation guidance

- Repo creation checklist: `revaly-co/rap-sdk` (public per ADR-SDK-012), bootstrap protections
  (ADR-SDK-012/013), then OQ-3 provisioning.
- Verify org ownership/custody of `revaly-co` sits with leadership (same custody standard as
  ADR-SDK-011) before repo creation.
- If the wider org migration later consolidates other repos into `revaly-co`, nothing here
  changes — that was the point of decoupling.

## Implementation status (dated addendum, 2026-07-17)

The wider org migration landed 2026-07-17: the fleet — this repo included — was **transferred**
into `revaly-co`, and `FlexPay-io` is parked with redirects alive, exactly the consequence the
decision anticipated. "Namespace final" is therefore satisfied via the transfer route rather
than a fresh create; OQ-3 executes against `revaly-co` as planned. Two operational notes:

- **Repo slug casing:** the transfer preserved the `RAP-sdk` slug; this ADR's checklist named
  lowercase `rap-sdk`. GitHub treats owner/repo slugs case-insensitively, so the Go module path
  `github.com/revaly-co/rap-sdk/languages/go` (declared in `languages/go/go.mod`) resolves
  regardless. Whether to rename the slug to lowercase is a cosmetic call to make **with OQ-3
  execution, before any Go publish** — module identity is the one surface where the canonical
  string is forever.
- **Spec-read token:** fine-grained PATs are resource-owner-scoped and do not follow a repo
  across orgs — `SPEC_ARTIFACT_READ_TOKEN` must be re-provisioned under `revaly-co`
  (`pipeline/README.md` prescribed exactly this replacement at rename time).
