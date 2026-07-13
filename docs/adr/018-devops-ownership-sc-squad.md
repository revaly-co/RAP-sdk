# ADR-SDK-018 — DevOps Contribution Is Owned Collectively by the SC Squad

**Status:** Accepted — decided 2026-07-10 (OQ-9, Charles); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 header table / §7 ownership note / §11 OQ-9
**Owner:** SC lead (accountability); SC squad (execution)

## Context

The RFC's infrastructure section (§7 — CI/CD, publish protection, registry mechanics, namespace
sequencing) and its NFR self-audit (§10) required a named DevOps contributor to sign off and to
confirm the namespace redirect findings (OQ-15). The review process asked repeatedly who that
person is.

## Problem

Name the accountable owner for the SDK's DevOps surface — pipeline, publish environment, registry
mechanics, namespace execution — in an organization without a dedicated DevOps individual attached
to this initiative.

## Decision

**The SC squad assumes DevOps ownership collectively** (decided by Charles, 2026-07-10) — squad,
not a named individual. Concretely, the squad:

1. signs off the infrastructure design (§7 — the sign-off is recorded by the RFC approval);
2. walks the NFR self-audit (§10) — explicitly accepted at approval as a **tracked follow-up**
   (see §12 approval notes and `../open-items.md`);
3. confirms the OQ-15 redirect findings (redirects satisfy neither OIDC claims nor Go module
   paths — ADR-SDK-022) as part of executing the namespace decision;
4. owns OQ-3 execution (registry provisioning + publish environment, Week 1) with accounts
   leadership-owned per ADR-SDK-011.

## Rationale

- The squad already owns the pipeline code, the publish workflows, and the repo — separating
  "DevOps" from that ownership would create a handoff seam inside a one-squad product.
- Collective ownership with a named accountable lead (SC lead) avoids both the bus factor of one
  individual and the diffusion of "everyone owns it".

## Alternatives considered

- **Named individual DevOps contributor:** not available; would also concentrate publish-mechanics
  knowledge in one head for a six-registry surface.
- **External/platform DevOps team ownership:** rejected — cross-team dependency on the Week-1
  critical path.

## Consequences

- The §10 NFR walk is a **squad obligation with a deadline** (tracked follow-up from approval),
  not an unowned wish — it sizes the P-2 hot-path write before GA (platform repo ADR 014).
- Registry/namespace execution steps in ADR-SDK-011/013/022 all read "SC squad" as the actor.
- Squad onboarding docs must cover publish mechanics (OIDC trusted publishing, tag protection,
  GPG/Key Vault) so the collective ownership is real, not nominal.

## Implementation guidance

- Track items 2–4 as Jira stories under Epic SC-234 with the SC lead as accountable.
- The scheduled machine-gate drift check (ADR-SDK-013 guidance) is the squad's standing tool for
  keeping the DevOps surface verifiably in the decided state.
