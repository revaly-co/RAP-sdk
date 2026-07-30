# RAP Integration SDK — Decision Log & Traceability

Every finalized decision from **RFC-046 "RAP Integration SDK"** (internal Confluence record,
**Approved 2026-07-10**, v10, Charles Weiss), mapped to its ADR and RFC anchor. Open items live in
`open-items.md`.

## Decisions (D-series)

| ID | Decision | Date | Owner | RFC anchor | ADR |
| --- | --- | --- | --- | --- | --- |
| D-1 | Hybrid architecture: generated core + hand-written runtime per language | 2026-07-06 | SC Eng | §3 | ADR-SDK-001 |
| D-2 | V1 typed errors key off HTTP status + transport condition (amended by D-7) | 2026-07-06 | SC Eng | §5.2 | ADR-SDK-002 |
| D-3 | OutcomeUnknown distinct class; reconciliation via required `merchantTransactionId` + existing GET; SDK never auto-resubmits | 2026-07-06 | SC Eng | §5.3 | ADR-SDK-003 |
| D-4 | No circuit breaker in V1 — SDK stateless; suppression/routing merchant-side | 2026-07-06 | SC Eng | §5.1–5.2 | ADR-SDK-004 |
| D-5 | Adoption telemetry via `User-Agent: revaly-sdk-<lang>/<semver>` (answers PRD OQ 2) | 2026-07-06 | SC Eng + Product | §5.7/§8 | ADR-SDK-005 |
| D-6 | Spec accuracy is a release gate; SDK pipeline consumes gated artifacts only | 2026-07-06 | SC Eng | §3.2 | ADR-SDK-006 |
| D-7 | Scoped `ErrorResponse.code` (`not_processed` \| `outcome_unknown` on 5xx) is a V1 prerequisite (P-1); 503 reclassified OutcomeUnknown unless the code proves otherwise | 2026-07-09 | SC Eng (API owners) | §5.4 P-1 | ADR-SDK-007 · platform ADR 013 |
| D-8 | OQ-10 promoted: per-account uniqueness + idempotency via synchronous intent reservation is a GA blocker (P-2), incl. inline-retry provenance fix | 2026-07-09 | SC Eng | §5.4 P-2 | ADR-SDK-008 · platform ADR 014 |
| D-9 | V1 reconcile verdict is hold-and-re-poll; `SafeToFailover` enters the API only when P-2 makes it provable | 2026-07-09 | SC Eng | §5.3 | ADR-SDK-009 |
| D-10 | External vocabulary: RAP-core; internal repo name never merchant-facing | 2026-07-09 | SC Eng + Product | §1 | ADR-SDK-010 |
| D-11 | Registry accounts leadership-owned, under a group email | 2026-07-09 | Leadership | §7.1 | ADR-SDK-011 |
| D-12 | rap-sdk repo public; GitHub Issues intake w/ routing templates; SECURITY.md + `security@` private disclosure | 2026-07-09 | SC Eng + Leadership | §7.1 | ADR-SDK-012 |
| D-13 | Publish protection collapsed to ONE human gate (the release cut); machine gates: tag-restricted env policy, maintainer-only tag protection, OIDC trusted publishing; env required-reviewer dropped | 2026-07-10 | SC squad | §3.1/§7 | ADR-SDK-013 |

## Decided open questions

| ID | Decision | Date | Owner | ADR |
| --- | --- | --- | --- | --- |
| OQ-1 | Generator: OpenAPI Generator v7.23.0, digest-pinned, all six cores; no Kiota .NET split; upgrades ride PRs with regen-diff review (evidence: `generator-bakeoff.md`) | 2026-07-14 | SC Eng | ADR-SDK-023 |
| OQ-4 | V1 test keys Enablement-issued; self-serve deferred; environment parity = pre-GA task | 2026-07-10 | Eng + Enablement | ADR-SDK-014 |
| OQ-5 | GA order .NET → Java → PHP → TypeScript → Python → Go (Charles); supersedes Wave-1 composition + pipeline-data validation | 2026-07-10 | Product + Enablement | ADR-SDK-015 |
| OQ-6 | Overall-deadline default **75 s** across all six runtimes (production telemetry ×2 sources; owner safety margin above the 30 s floor — clears every observed non-ceiling gateway tail, clips ≲0.007 %; evidence in the internal OQ-6 record on SC-278); connect default deliberately deferred to OQ-11 edge data; reconcile-policy defaults stay explicit pending visibility-lag telemetry (SC-261 follow-up) | 2026-07-20 | SC Eng | ADR-SDK-027 |
| OQ-7 | Monorepo `revaly-co/rap-sdk`; per-language read-only mirrors only if an ecosystem demands | 2026-07-10 | SC Eng | ADR-SDK-016 |
| OQ-8 | RTN SDK (PRD-049) explicitly decoupled; separate pipelines, no reuse commitment (Charles) | 2026-07-10 | SC Eng + RTN squad | ADR-SDK-017 |
| OQ-9 | DevOps contribution owned collectively by the SC squad (Charles); squad signs §7, walks §10 NFR audit, confirms OQ-15 findings | 2026-07-10 | SC lead | ADR-SDK-018 |
| OQ-10 | *Promoted to D-8 (GA blocker)* — see D-series | 2026-07-09 | — | ADR-SDK-008 |
| OQ-12 | Apache-2.0 (Charles); Legal ratifies before first publish; copyright Revaly | 2026-07-10 | Leadership + Legal | ADR-SDK-019 |
| OQ-13 | Approval explicitly covers the PCI scope determination + values-free logging obligation (Charles); QSA link = follow-up | 2026-07-10 | Leadership + Compliance | ADR-SDK-020 |
| OQ-14 | PRD-057 Musts resolved via formal deviation acceptance recorded on the PRD (Charles); approval given ahead as tracked follow-up | 2026-07-10 | Product | ADR-SDK-021 |
| OQ-15 | Create `rap-sdk` under existing `revaly-co` org (created 2026-06-09, verified); decoupled from org rename; `FlexPay-io` parked permanently | 2026-07-10 | DevOps + Leadership | ADR-SDK-022 |

Still open: **OQ-2, OQ-3, OQ-11** → `open-items.md`.

## Review-thread provenance

The RFC review threads that produced or shaped these decisions — architecture review (the four
platform facts; P-1/P-2 promotion; hold-and-re-poll), consumer-interaction surface (§7.1 policy →
D-11, D-12, OQ-12), namespace (OQ-15), consumer-side contract (§6 DX a–f), human-gate
justification (D-13), PCI authority (OQ-13), PRD gate rule (OQ-14), external vocabulary (D-10),
registry ownership (D-11), NFR self-audit (§10), and claims verification (§2 panel) — are
preserved with their comment ids in the internal RFC-046 Confluence record.

## Provenance appendix

The four load-bearing platform facts behind D-7/D-8/D-9 — the 5xx conflation, async unbounded
visibility, inline-retry re-keying, and the id-length mismatch — were verified directly against
the platform codebase at RFC approval (2026-07-09) and re-verified 2026-07-11 while drafting this
document set. Facts 1 and 4 were subsequently addressed by platform ADRs 013/015 (merged
2026-07-14: `ErrorResponse.code` + id-length/format corrections); facts 2 and 3 stand until
platform ADR 014 (P-2, Epic SC-234) lands. The file-level citations and environment
verifications grounding this appendix live in the internal RFC record, not in this public
repository.
