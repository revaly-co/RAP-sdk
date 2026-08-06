# RAP Integration SDK — Architecture Decision Records

This directory is the complete ADR set for the **RAP Integration SDK** (`revaly-co/rap-sdk`),
capturing every decision finalized by **RFC-046 "RAP Integration SDK"** (internal Confluence
record; SC-215, Epic SC-234), **Approved 2026-07-10** (v10, Charles Weiss).

> **Provenance:** relocated here 2026-07-13 from the platform repository (`FlexPay-io/Backbone`,
> `docs/sdk/adr/` on branch SC-215) — this is now the canonical home. All ADRs are written to be
> self-contained — implementable without access to the platform repository. Companion design
> docs live one level up (`../`).
>
> **Pre-publication scrub (ADR-SDK-010) — done 2026-07-30:** `../decision-log.md`'s internal
> provenance appendix, formerly the one place internal repo names/paths were kept, has been
> scrubbed; the file-level citations live in the internal RFC-046 record.

## Numbering

`ADR-SDK-001…013` map 1:1 to RFC decisions **D-1…D-13**; `ADR-SDK-014…023` capture the **decided
open questions** (OQ-1, 4, 5, 7, 8, 9, 12, 13, 14, 15). Still-open items (OQ-2, 3, 11) are
implementation gates, tracked in `../open-items.md` — they get ADRs when decided.
`ADR-SDK-024+` are **post-RFC** records; each carries its own status line, and while Proposed
they are tracked as post-RFC open items (OQ-16+) in `../open-items.md`.

## Index

| ADR | Decision | RFC source |
| --- | --- | --- |
| [001](001-hybrid-generated-core-handwritten-runtime.md) | Hybrid architecture: generated core + hand-written runtime per language | D-1, §3 |
| [002](002-typed-error-taxonomy.md) | Typed error taxonomy: HTTP status + transport condition + scoped safety signal | D-2 (+D-7), §5.2 |
| [003](003-outcomeunknown-reconciliation-contract.md) | OutcomeUnknown first-class; reconciliation via `merchantTransactionId` | D-3, §5.3 |
| [004](004-no-circuit-breaker-stateless-sdk.md) | No circuit breaker in V1; stateless, deterministic SDK | D-4, §5.1–5.2 |
| [005](005-user-agent-adoption-telemetry.md) | Adoption telemetry via `User-Agent` | D-5, §5.7/§8 |
| [006](006-spec-accuracy-release-gate.md) | Spec accuracy is a release gate; only gated spec artifacts | D-6, §3.2 |
| [007](007-errorresponse-code-v1-failover-signal.md) | `ErrorResponse.code` safety signal is the V1 fast-failover trigger (P-1) | D-7, §5.4 |
| [008](008-synchronous-intent-reservation-ga-gate.md) | Synchronous intent reservation + idempotency is the GA gate (P-2) | D-8, §5.4 |
| [009](009-v1-reconcile-hold-and-repoll.md) | V1 reconcile verdict: hold-and-re-poll; `SafeToFailover` only with P-2 | D-9, §5.3 |
| [010](010-external-vocabulary-rap-core.md) | External vocabulary: RAP-core | D-10, §1 |
| [011](011-registry-accounts-leadership-owned.md) | Registry accounts leadership-owned, group email | D-11, §7.1 |
| [012](012-public-repo-issue-intake-security-disclosure.md) | Public repo; GitHub Issues intake; SECURITY.md + `security@` | D-12, §7.1 |
| [013](013-single-human-publish-gate.md) | Single human publish gate: the release cut; machine gates elsewhere | D-13, §3.1/§7 |
| [014](014-sandbox-credentials-enablement-issued.md) | Sandbox test credentials Enablement-issued in V1 | OQ-4 |
| [015](015-ga-language-order.md) | GA order: .NET → Java → PHP → TypeScript → Python → Go | OQ-5, §3.3 |
| [016](016-monorepo-layout.md) | Monorepo `revaly-co/rap-sdk`; read-only mirrors only if demanded | OQ-7 |
| [017](017-rtn-sdk-decoupled.md) | Decoupled from the RTN SDK (PRD-049); no pipeline reuse commitment | OQ-8 |
| [018](018-devops-ownership-sc-squad.md) | DevOps ownership: SC squad collectively | OQ-9 |
| [019](019-license-apache-2.0.md) | License: Apache-2.0; **Legal-ratified in writing — recorded 2026-08-06** (publish gate closed) | OQ-12, §7.1 |
| [020](020-pci-scope-values-free-logging.md) | PCI scope merchant-side; values-free logging obligation | OQ-13, §9 |
| [021](021-prd-057-deviation-acceptance.md) | PRD-057 Musts resolved via formal deviation acceptance | OQ-14 |
| [022](022-github-namespace-revaly-co.md) | Create under `revaly-co`; park `FlexPay-io` permanently | OQ-15, §7 |
| [023](023-generator-openapi-generator-pinned.md) | Generator: OpenAPI Generator v7.23.0, digest-pinned, all six cores; no Kiota split | OQ-1, §3.3/§11 |
| [024](024-stage4-contract-smoke-environment.md) | **Accepted 2026-07-18:** stage-4 smoke = thin per-language runtime suites vs Backbone staging ACA (interim; built — 8 scenarios ×6 languages, environment-scoped secrets, staging-only fault-inject row); merchant sandbox is key-scoped, not URL-scoped — GA retarget follows ADR-SDK-014 parity + OQ-11 | post-RFC (OQ-16, closed) |
| [025](025-spec-repin-automation.md) | **Accepted 2026-07-19:** spec re-pin automation — tier 1 nightly freshness watchdog (implemented: idempotent `spec-repin` checklist issue, self-closing/superseding, fail-closed) + tier 2 platform-dispatched draft re-pin PR (pending the cross-repo credential) | post-RFC (OQ-17 tracks tier 2) |
| [026](026-interim-github-release-artifacts.md) | **Accepted 2026-07-20:** interim distribution = per-language GitHub release artifacts (stage 5 `package.sh` + interim stage 6; asset + `.sha256` + `provenance.json` on the spec-release model); tags `<lang>/vX.Y.Z` on `main`, go as `go/v*` (module form reserved), plain versions only (no alpha/beta/rc), tag = version source (ephemeral stamping), first cut `v0.1.0` ×6; registry publish stays embargoed | post-RFC (registry stage 6 waits on OQ-3) |
| [027](027-deadline-defaults-from-telemetry.md) | **Accepted 2026-07-20:** overall-deadline default **75 s** in all six runtimes, ratified from production telemetry (owner safety margin above the 30 s floor — clears every observed non-ceiling tail, clips ≲0.007 %; per-language opt-out sentinels); connect default deliberately not set — awaits OQ-11 edge data; reconcile-policy defaults stay explicit (SC-261 follow-up) | post-RFC (closes OQ-6) |
| [028](028-pre-ga-idiom-ratifications.md) | **Accepted 2026-07-21:** pre-GA idiom review closed (dx-contract §a) — four per-language reviews + adversarial coherence pass; all flagged `[Proposed]` idiom choices ratified or corrected (java checked exceptions/interruption, go layout fence `internal/runtime/`+`raptest/` **amending ADR-SDK-016**, pointer params, `Transport` key, TS PascalCase verdict discriminants, python cancellation/TLS conservatism); §a linter clause closed ×4 (Error Prone 2.50.0, eslint+typescript-eslint, ruff, staticcheck — pinned, hand-written surfaces only); breaking subset batched as one v0.3.0 break; OQ-3/SC-261/OQ-11 explicitly untouched | post-RFC (dx-contract §a; amends ADR-SDK-016) |
| [029](029-edge-behaviour-verified-connect-default.md) | **Accepted 2026-07-21:** AFD/WAF edge behaviour verified against the live production edge — §2 edge rows ratified unchanged (30-day census: one connect-phase 504, zero 502/AFD-503; origin error bodies pass through so the P-1 `not_processed` signal survives; WAF blocks are HTML 403s and bot rules are log-only for server-side clients); **connect-timeout default 10 s ×6** (TS documentation-level per ADR-SDK-028 §4); timeout ordering 75 s < ≈100 s < 120 s + ops guardrail; ships v0.4.0 | post-RFC (closes OQ-11; amends ADR-SDK-027 Decision 3) |
| [030](030-registry-package-names.md) | **Accepted 2026-07-30:** final registry package names ×6 — npm **`@revaly/sdk`** (scoped), PyPI `revaly-sdk`, NuGet `Revaly.Sdk` + `Revaly.Sdk.Core`, Packagist `revaly/sdk`, Maven `co.revaly:revaly-sdk`, Go path unchanged; committed metadata already final except the npm rename (stage-6 prep); publish embargo unchanged | post-RFC (closes OQ-3 naming; residuals per `../registry-provisioning.md`) |
| [031](031-registry-publish-dark-mode.md) | **Proposed 2026-08-03:** stage-6 registry publish ships **DARK** on every release tag (rehearsal + flip-readiness report in the `publish` environment, no registry contact); **double-keyed flip** (`REGISTRY_PUBLISH_MODE=live` + the guard-removal PR — a half-flip hard-fails); Packagist via a generated mirror built from the verified stage-5 artifact tree (`rap-sdk-php`), amending ADR-SDK-013's webhook wording; npm renamed to `@revaly/sdk`; **GitHub releases stay after registry GA** as provenance anchor + fallback channel | post-RFC (concretizes ADR-SDK-013; flip runbook in `../registry-provisioning.md`) |
| [032](032-public-repo-fresh-cutover.md) | **Accepted 2026-08-03 (Dimitri):** the public repo ships via **fresh-repo cutover** — the current repo becomes the private `RAP-sdk-archive` (true history, PR threads, pre-cutover releases); a **new** `revaly-co/RAP-sdk` reclaims the name (Go module path unchanged) carrying a **sanitized-history transplant** (`git filter-repo`: smoke.exe blob, pre-redaction doc versions, `c584d69` message, `@flexpay.io → @revaly.co` author emails; commit map kept in the archive); plumbing recreated, old tags/releases not ported, versions continue, cutover release ×6 proves the new repo before it flips public | post-RFC (closes the history sanitize-vs-accept decision; executes as flip-runbook gate 3) |

## Companion documents (`../`)

- `architecture.md` — system architecture and component model
- `failover-contract.md` — the merchant-facing failover & reconciliation contract (sequence diagrams)
- `runtime-tdd.md` — technical design of the hand-written runtime layer
- `pipeline-and-release.md` — CI/CD pipeline, publish mechanics, versioning
- `dx-contract.md` — the Developer Experience contract (§6 a–f, expanded)
- `open-items.md` — open questions & tracked follow-ups (implementation gates)
- `decision-log.md` — full traceability: decision → ADR → RFC anchor → provenance
