# RAP Integration SDK (`rap-sdk`)

Six server-side client SDKs — **.NET, Java, PHP, TypeScript, Python, Go** — for the **RAP V2
API** (RAP-core), built per **RFC-046** (Approved 2026-07-10, v10): one monorepo, one
deterministic generation + release pipeline consuming only gated spec artifacts, and one
merchant-facing failover & reconciliation contract.

**Status: build phase (Epic SC-234).** The design documentation set is complete (23 ADRs +
8 design docs); the spec input is pinned (`spec/`, ADR-SDK-006) and the generator is decided
(ADR-SDK-023: OpenAPI Generator v7.23.0, digest-pinned). Language cores and runtimes are not
yet scaffolded.

## Start here

- [`docs/README.md`](docs/README.md) — documentation index and reading order
- [`docs/adr/README.md`](docs/adr/README.md) — the full ADR set (D-1…D-13 + decided OQs)
- [`docs/failover-contract.md`](docs/failover-contract.md) — the safety contract everything
  serves; read before writing any code
- [`docs/open-items.md`](docs/open-items.md) — what is *not* decided (OQ-1/2/3/6/11) and the
  platform-side gates

## Target layout (ADR-SDK-016)

```
rap-sdk/
  spec/                  # pinned gated spec artifact reference + checksums
  languages/<lang>/      # { core/ (generated), runtime/, tests/ } × 6
  pipeline/              # generation configs, templates, publish workflows
  docs/                  # design docs + ADRs
```

Finalized in the repo-bootstrap story; `docs/` and `spec/` (pinned to `spec/v2.1.3+e75c71a`)
exist today.

## Namespace note (ADR-SDK-022)

This repository lives at **`revaly-co/RAP-sdk`** — the org migration landed 2026-07-17
(fleet-wide transfer; `FlexPay-io` is parked with redirects alive, exactly as the ADR
prescribed). The namespace publish-gate is satisfied. The first publish — pre-1.0 betas
included — remains gated on the protected publish environment and trusted-publisher
registrations (OQ-3, ADR-SDK-013) and Apache-2.0 Legal ratification (ADR-SDK-019). The
pre-publication scrub of the internal provenance appendix in `docs/decision-log.md` landed
2026-07-30 (ADR-SDK-012).
