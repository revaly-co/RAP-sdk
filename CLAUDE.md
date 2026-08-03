# rap-sdk — Global Rules for AI Sessions

Six server-side SDKs (**.NET, Java, PHP, TypeScript, Python, Go**) for the **RAP V2 API**
(RAP-core, `api.revaly.co`), per **RFC-046** (Approved 2026-07-10 v10; SC-215, Epic SC-234).
One monorepo, one deterministic pipeline consuming only gated spec artifacts, one merchant-facing
failover contract. `docs/` is the complete, self-contained design set (30 ADRs + 10 design docs) —
**docs are the source of truth; this file is the enforcement summary.**

**Namespace:** the repo lives at **`revaly-co/RAP-sdk`** — the org migration landed 2026-07-17
(fleet-wide transfer; `FlexPay-io` is parked with redirects alive, per ADR-SDK-022). The
namespace publish-gate is satisfied, the `publish` environment exists (2026-07-29), and names
are final (ADR-SDK-030); the remaining publish gates (OQ-3 provisioning residuals, publish-day
OIDC bindings, ADR-SDK-019 **written** Legal ratification) still stand — **publish remains
embargoed** (rule 3).

**Current phase:** see `docs/README.md` § Status snapshot (dated facts live there, not here).
Standing build sequencing: global rules → repo bootstrap → pipeline stages 1–4 → per-language
**GitHub release artifacts** as interim distribution → registry publish **last**, only after its
gates close.

## Read before writing code

`docs/README.md` has the full reading order. Minimum for any code-touching session:
`docs/failover-contract.md` (safety contract — normative classification algorithm),
`docs/runtime-tdd.md` (the runtime surface), `docs/dx-contract.md` (the acceptance bar), plus the
ADRs the task touches. Items marked **[Decided]** are fixed by RFC/ADR — reversing one requires an
ADR revision, never a quiet code choice. Items marked **[Proposed]** are finalized in Epic SC-234
build stories.

## Hard rules — never violate

1. **Never hand-edit generated code.** `languages/*/core/` is generator output only (ADR-SDK-001);
   it changes exclusively by regeneration against a newly pinned spec artifact, and CI enforces
   this with a regeneration-diff check. The hand-written runtime (`languages/*/runtime/`; go:
   `languages/go/{revaly.go, internal/runtime/, raptest/}` per ADR-SDK-028) is the only product
   code.
2. **Spec input = pinned gated artifact only** (ADR-SDK-006): a `spec/v*` release tag from the
   platform repo, verified against its `.sha256` and `provenance.json` (pin lives in `spec/`).
   Never generate from a branch checkout, a URL, or a locally edited spec.
3. **Publish is embargoed.** No registry publish (npm / PyPI / NuGet / Packagist /
   Maven Central / pkg.go.dev), no OIDC trusted-publisher registration, no registry tokens —
   until the `revaly-co` namespace is final (ADR-SDK-022), registry accounts + the protected
   publish environment exist (OQ-3, ADR-SDK-011/013), and Apache-2.0 is Legal-ratified
   (ADR-SDK-019). Pre-1.0 betas count as publishing. Interim distribution = per-language
   **GitHub release artifacts** from this repo (model: the platform's `spec/v*` releases —
   asset + `.sha256` + `provenance.json`). The stage-6 registry job exists but runs **DARK**
   (ADR-SDK-031): rehearsal only, double-keyed flip — editing it is fine; setting
   `REGISTRY_PUBLISH_MODE=live`, provisioning any registry binding/secret, or removing the
   embargo guards (npm `"private"`, python `Private :: Do Not Upload`) IS the embargoed act
   and happens only via the flip runbook in `docs/registry-provisioning.md`.
4. **Do not decide open items.** OQ-2 (full error-code taxonomy) and the OQ-3 provisioning
   residuals (NuGet prefix, PyPI org, publish-day OIDC/GPG) have owners and gates in
   `docs/open-items.md`. Where code needs the answer, leave an explicit marker referencing the
   OQ. (OQ-1 is decided — ADR-SDK-023; generator changes are ADR revisions, never quiet
   pipeline edits. OQ-6 is decided — ADR-SDK-027: overall-deadline default 75 s ×6,
   telemetry-ratified. OQ-11 is decided — ADR-SDK-029: connect default 10 s ×6, edge rows
   ratified. OQ-3 naming is decided — ADR-SDK-030: names final, npm scoped `@revaly/sdk`.
   Reconcile-policy defaults still ride SC-261 — do not invent them.)
5. **Safety-contract invariants** (`failover-contract.md` §2/§5; ADR-SDK-002/003/004/007/009):
   classify failures only by the normative algorithm — never from `error` message text, latency,
   or wait heuristics; `ErrorResponse.code` and `transactionType` are **open strings**, never
   closed enums; unrecognized `code` = absent → OutcomeUnknown; if the transport cannot prove the
   request was never sent, classify OutcomeUnknown — never guess toward "safe". No retries, no
   resubmission, no circuit breaker, no cross-request state; the caller-bounded reconcile re-poll
   is the only loop. V1 reconcile verdicts are `Found | NotFoundYet` only; `SafeToFailover`
   arrives with platform P-2 as a **minor** release; verdict types stay open for extension
   (default/else branch mandatory in every language and every example).
6. **Values-free logging is a PCI obligation** (ADR-SDK-020): no payload values at default
   verbosity; debug level scrubs PAN/CVV/PII; API keys never appear in logs **or exception
   messages**; scrub by allowlist in one central function per runtime; every language ships CI
   log-capture tests asserting this. Mock transports use synthetic data only.
7. **DX-contract commitments (`dx-contract.md` a–f) change only via RFC revision** — they are a
   designed artifact, not conventions to drift from.

## Layout (ADR-SDK-016)

```
rap-sdk/
  spec/                    # pinned gated spec artifact reference + checksums
  languages/
    dotnet/     { core/ (generated), runtime/, tests/ }
    java/       { core/, runtime/, tests/ }
    php/        { core/, runtime/, tests/ }
    typescript/ { core/, runtime/, tests/ }
    python/     { core/, runtime/, tests/ }
    go/         { core/, revaly.go + internal/runtime/ + raptest/, tests/ }   # subdir module: github.com/revaly-co/rap-sdk/languages/go (layout per ADR-SDK-028)
  pipeline/                # generation configs, templates, publish workflows
  docs/                    # ADRs + design docs (source of truth)
```

Scaffolding rules:

- GA investment order (ADR-SDK-015): **.NET → Java → PHP → TypeScript → Python → Go** — but all
  six cores are generated, compiled, and contract-tested in CI from day one; no language starts
  later from scratch. .NET is dogfooded via the platform's E2E tests.
- Every `core/` file set carries a generated-code banner.
- Runtime surface per `runtime-tdd.md` §§1–9: config (§1), one-package re-export (§2), typed
  errors in the per-language idiom (§3), reconcile helper (§4), transport with
  `User-Agent: revaly-sdk-<language>/<semver> (<runtime-version>; <os>)` injected where the core
  cannot bypass it (§5, ADR-SDK-005), values-free logging + wire-trace hook (§6), mock transport
  covering every failover-contract §2 row (§8), copy-paste quickstart with all three error
  classes + reconcile (§9, ≤15-minute bar).
- Registry package names (`runtime-tdd.md` §7) are **[Decided]** — ADR-SDK-030 (npm is scoped
  `@revaly/sdk`; the npm metadata rename rides the stage-6 prep). Go publishes last
  (highest-permanence module path).

## Pipeline (docs/pipeline-and-release.md)

validate → generate ×6 → build+test → contract smoke (Sandbox) → package → publish.
Stages 1–3 run on every PR; stage 4 runs on release tags (blocking), the nightly schedule
(advisory), and manual dispatch — never plain PRs (ADR-SDK-024); 5–6 only from release tags on
`main`. Any language red blocks the release for all six. Semver per package; per-language tags (`dotnet/v1.0.0`) drive the publish
matrix; every version maps to a spec commit SHA in release notes. A failed release never resumes
via manual re-run — fix, then cut a new tag.

## Conventions

- Conventional commits (`docs:`, `feat(dotnet):`, `chore(ci):` …); PR-only merges to `main`
  (branch protection on).
- New decisions become numbered ADRs in `docs/adr/` (Title / Status / Context / Decision /
  Consequences); status changes are dated edits to `docs/README.md` § Status snapshot and
  `docs/open-items.md` — keep both current when platform facts change.
- Going public (ADR-SDK-012) happens via the **ADR-SDK-032 fresh-repo cutover** (decided
  2026-08-03): the public repo is a NEW `revaly-co/RAP-sdk` carrying a sanitized history
  transplant; THIS repo becomes the private `RAP-sdk-archive`. Never flip this repo's
  visibility directly. (The HEAD scrub + `SECURITY.md`/`security@` intake landed 2026-07-30.)
- .NET code style: no `#region` / `#endregion` directives.
