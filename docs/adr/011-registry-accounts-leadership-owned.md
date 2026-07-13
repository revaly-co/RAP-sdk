# ADR-SDK-011 — Registry Accounts Are Leadership-Owned, Under a Group Email

**Status:** Accepted — decided 2026-07-09 (D-11, per review constraint); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §7 / §7.1, decision D-11 · inline review thread 2026-07-08
**Owner:** Leadership (provisioning executed via OQ-3, Week 1)

## Context

Distribution requires organization/namespace ownership on six registries: **npm, PyPI, NuGet,
Packagist, Maven Central (Sonatype), pkg.go.dev** (the last is pull-based off git tags — no
account, but the module path binds to the GitHub namespace, ADR-SDK-022). Registry publishes are
**irreversible**; account loss or hijack is a supply-chain incident affecting merchant payment
systems. PRD-057 rates registry provisioning a High risk and it sits on the Week-1 critical path
(OQ-3).

## Problem

Who owns the registry accounts, and under what identity, such that personnel churn, credential
loss, or a compromised individual cannot orphan or hijack public payment-SDK packages?

## Decision

- All registry organizations/accounts are **leadership-owned**.
- Accounts are registered under a **group email** (not any individual's mailbox) — the explicit
  review constraint.
- The `security@` vulnerability-disclosure mailbox (ADR-SDK-012) is provisioned under the same
  group-email constraint, together with the registry accounts (OQ-3).
- Squad engineers get scoped publish rights via the pipeline's trusted-publishing configuration
  (ADR-SDK-013), never via personal ownership of the org.

## Rationale

- **Bus factor and custody:** individual-owned registry orgs are lost with the individual; group
  email + leadership custody survives personnel changes.
- **Blast radius:** ownership is the recovery path of last resort for hijacked or bad releases;
  it must sit with the accountable owners of an irreversible public surface.

## Alternatives considered

- **Squad-engineer-owned accounts:** rejected — churn risk on an irreversible surface.
- **Individual leadership mailbox:** rejected — same single-point failure with a nicer title;
  the review constraint specifically requires a group email.

## Consequences

- OQ-3 (Week 1) executes provisioning: org/namespace creation on all six registries + the
  protected publish environment, sequenced **after** the GitHub namespace decision (ADR-SDK-022).
- 2FA and recovery policy on every registry org is part of provisioning acceptance.
- Publishing day-to-day never uses these owner credentials — OIDC trusted publishing binds the
  pipeline instead (ADR-SDK-013); owner credentials are break-glass only.

## Implementation guidance

Provisioning checklist (executed under OQ-3):

1. Group email created and access-controlled by leadership.
2. Orgs/namespaces registered: npm org, PyPI org, NuGet org, Packagist vendor, Sonatype namespace
   (`co.revaly` — requires DNS or GitHub proof of namespace control).
3. 2FA enforced; recovery codes stored in the corporate secret store.
4. Trusted-publisher / OIDC registration deferred until the GitHub namespace is final
   (ADR-SDK-022 publish-order rule).
5. Maven GPG signing keys generated and stored in Key Vault (pipeline-only access).
6. `security@` group mailbox live and referenced by SECURITY.md before first publish.
