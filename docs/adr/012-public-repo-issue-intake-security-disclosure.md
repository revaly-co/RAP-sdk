# ADR-SDK-012 — Public Repository; GitHub Issues Intake; SECURITY.md + Private Disclosure Channel

**Status:** Accepted — decided 2026-07-09 (D-12); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §7.1, decision D-12 · footer review thread 2026-07-08 (consumer-interaction surface)
**Owner:** SC Eng + Leadership

## Context

Public distribution creates a consumer-interaction surface that binds consumers and is hard to
change later. Review (2026-07-08) required explicit decisions on repo visibility, issue intake, and
vulnerability disclosure before approval. Distribution mechanics also impose constraints:
**pkg.go.dev pulls modules from a public repo**, and **npm provenance links to public source**.

## Problem

Decide, before the repo exists: is `rap-sdk` public or private; where do merchants report
problems; and how are vulnerabilities disclosed privately for packages that run inside merchant
payment systems?

## Decision

1. **Repo visibility: public** — forced by distribution mechanics (Go modules, npm provenance).
   Development discipline compensates: protected branches, PR-only merges, protected publish
   environment (ADR-SDK-013).
2. **Issue intake: GitHub Issues** for SDK bugs and developer-experience problems. Issue templates
   **route anything account- or payment-specific to Enablement/support** — sensitive context never
   lands publicly. The SC squad triage rotation owns first response; the first-response SLA is a
   measured DX KPI (DX contract §f, RFC-046 §8).
3. **Vulnerability disclosure:** `SECURITY.md` in the repo + GitHub private vulnerability
   reporting + a leadership-owned **`security@` group email** (provisioned with the registry
   accounts, ADR-SDK-011/OQ-3).

## Rationale

- Fighting the ecosystem (private repo + public packages) breaks Go distribution and npm
  provenance outright; public-with-discipline is the industry-standard corporate-SDK posture.
- Merchant-reported problems and platform-detected bad releases are different channels: GitHub
  Issues covers the former; the §8 on-call story (deprecate/yank + patch release) covers the
  latter. Both existed as gaps until this decision.
- A private disclosure channel is non-negotiable given the supply-chain threat framing (RFC-046
  §9): six public packages running inside payment systems.

## Alternatives considered

- **Private repo, public packages:** rejected — breaks pkg.go.dev and npm provenance.
- **Enablement-only intake (no public issues):** rejected — hides DX problems from the community
  surface merchants expect, and buries the SLA signal the DX KPIs measure.
- **Disclosure via personal maintainer contact:** rejected — churn risk; group email constraint
  (ADR-SDK-011) applies.

## Consequences

- Everything in the repo is externally visible: the RAP-core vocabulary rule (ADR-SDK-010) applies
  to all committed content, and internal provenance is scrubbed before the repo goes public.
- Issue templates are a launch deliverable (repo bootstrap), not an afterthought: bug report
  (routes sensitive data away), DX feedback, and a hard redirect template for account/payment
  issues.
- Triage rotation + SLA measurement must exist at Wave-1 GA (the KPI is measured from launch).
- SECURITY.md names supported versions (upgrade/support policy per DX contract §e) and the
  `security@` address; GitHub private vulnerability reporting is enabled at repo creation.

## Implementation guidance

- Repo bootstrap checklist: branch protection (PR-only, required checks), CODEOWNERS (SC squad),
  issue templates as above, SECURITY.md, LICENSE (ADR-SDK-019), publish environment (ADR-SDK-013).
- Never accept reproduction data containing PAN/CVV/API keys in issues: templates state it, triage
  macro enforces it, and the values-free logging default (ADR-SDK-020) keeps SDK logs shareable by
  construction.
