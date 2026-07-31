# ADR-SDK-010 — External Vocabulary: the Platform Service Is "RAP-core"

**Status:** Accepted — decided 2026-07-09 (D-10); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §1 (external vocabulary block), decision D-10 · internal repo naming guide
**Owner:** SC Eng + Product

## Context

The platform service behind the RAP V2 API carries an internal repository name that predates the
Revaly branding. The SDK creates the first large **merchant-facing** documentation and metadata
surface that describes the platform in prose: package readmes, registry listings, release notes,
error-handling guides, SECURITY.md, issue templates.

## Problem

Without a fixed vocabulary, internal service names leak into public surfaces — confusing merchants
(two names for one thing), weakening the brand, and exposing internal topology.

## Decision

- Merchant-facing surfaces — SDK docs, package metadata, release notes, error messages, issue
  templates, support macros — say **RAP-core** for the platform service.
- The internal repository name **never appears externally** (per the repo naming guide).
- Product/brand tokens: packages and the `User-Agent` product token use the **Revaly** brand
  (`revaly-sdk-<language>`, group id `co.revaly`); the API host is `api.revaly.co`; the platform
  *service* is RAP-core.

## Rationale

- One external name per system; the naming guide is the single source of truth.
- The SDK repo is **public** (ADR-SDK-012), so "repo-internal" documentation is externally visible
  documentation — the rule applies to nearly everything in the rap-sdk repo, not just registry
  listings.

## Alternatives considered

- **Use the internal name externally "because the spec repo does":** rejected — the spec's title
  is already "Revaly" and the naming guide forbids it.
- **No rule, fix in review:** rejected — vocabulary drift is exactly the class of error review
  misses piecemeal.

## Consequences

- This ADR set and the companion design docs already use RAP-core; internal provenance (platform
  file paths, internal repo names) was quarantined in `../decision-log.md`'s provenance appendix
  and **relocated to the internal RFC record ahead of the public flip** (done 2026-07-30).
- Public error messages emitted by SDK runtimes must not name internal services; they reference
  RAP-core and carry the correlation id.

## Implementation guidance

- Add a CI vocabulary check in rap-sdk that scans publishable surfaces (docs/, readmes, package
  metadata, release-note templates) for forbidden internal names. Keep the denylist pattern in a
  repository **secret/variable**, not in a committed file — a committed denylist in a public repo
  would itself disclose the internal names it polices.
- Registry metadata review (per publish, part of the release-cut checklist in ADR-SDK-013) includes
  a vocabulary pass.
