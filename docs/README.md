# RAP Integration SDK — Design Documentation

Design documentation for the **RAP Integration SDK** (`revaly-co/rap-sdk`): six server-side client
SDKs (Python, TypeScript, Go, .NET, PHP, Java) for the RAP V2 API, per **RFC-046** (SC-215, Epic
SC-234) — **Approved 2026-07-10** (v10, Charles Weiss).

> **Provenance:** relocated here 2026-07-13 from the platform repository (`FlexPay-io/Backbone`,
> `docs/sdk/` on branch SC-215) as one self-contained unit — this folder is now the canonical
> home. Everything here is written to be self-contained — implementable without access to the
> platform repository. Platform-side obligations have their own ADRs in the platform repo
> (`docs/adr/013…018`).
>
> **Pre-publication scrub — done 2026-07-30:** the rap-sdk repo goes public (ADR-SDK-012) and
> merchant-facing surfaces use the RAP-core vocabulary (ADR-SDK-010). The internal provenance
> formerly quarantined in `decision-log.md`'s appendix has been relocated to the internal
> RFC-046 record.

## Documents

| Document | Purpose |
| --- | --- |
| [`adr/`](adr/README.md) | **32 ADRs** — one per finalized RFC decision (D-1…D-13, decided OQs) + post-RFC records (024+, status per ADR) |
| [`architecture.md`](architecture.md) | System architecture: components, data flow, trust boundary, repo shape |
| [`failover-contract.md`](failover-contract.md) | The merchant-facing failover & reconciliation contract, with sequence diagrams — the safety core of the product. Appendix A carries the normative prohibitions verbatim |
| [`failover-cookbook.md`](failover-cookbook.md) | Task-oriented recipes for integrators: handling each outcome, choosing a reconcile policy, testing offline, debugging with correlation ids |
| [`runtime-tdd.md`](runtime-tdd.md) | Technical design of the hand-written runtime layer (per-language surface) |
| [`pipeline-and-release.md`](pipeline-and-release.md) | CI/CD pipeline stages, publish mechanics per registry, versioning & release policy |
| [`registry-provisioning.md`](registry-provisioning.md) | OQ-3 runbook: final names (ADR-SDK-030), the per-registry what-is-left board, ownership/custody, how publishing will work, and the tracked Packagist placeholder deviation |
| [`maven-signing-key.md`](maven-signing-key.md) | The Maven Central signing key: fingerprint/expiry, what is in the publish vault, what still blocks the java publish path, incident + custody notes, and the recorded early-provisioning deviation |
| [`dx-contract.md`](dx-contract.md) | Developer Experience contract (RFC §6 a–f) with acceptance criteria |
| [`open-items.md`](open-items.md) | Open questions (OQ-1/2/3/6/11 from the RFC; post-RFC OQ-16+) and tracked follow-ups — the implementation gates |
| [`decision-log.md`](decision-log.md) | Traceability: every decision → ADR → RFC anchor → provenance |
| [`generator-bakeoff.md`](generator-bakeoff.md) | OQ-1 evidence record: hands-on six-language generation + verified market comparison (basis of ADR-SDK-023) |
| [`prod-sandbox-validation.md`](prod-sandbox-validation.md) | OQ-16 evidence record: the released v0.4.1 SDKs ×6 exercised against the merchant sandbox key-scope on the production URL (ADR-SDK-024 §Decision 4 retarget + the ADR-SDK-014 parity checklist) |

## Reading order for a new implementer

1. `architecture.md` — what we're building and why it's shaped this way.
2. `failover-contract.md` — the safety contract everything serves. Read before writing any code.
3. `adr/README.md` → ADRs 001–009 (architecture + error/reconcile semantics).
4. `runtime-tdd.md` + `dx-contract.md` — the surface you're implementing and the bar it must meet.
5. `pipeline-and-release.md` + ADRs 010–023 — how it ships and the governance around it.
6. `open-items.md` — what is *not* yet decided; don't guess at these, they have owners.

## Reading order for an integrator

Building *on* the SDK rather than *in* it? The path is shorter:

1. `../README.md` — what the SDK gives you, and the contract in thirty seconds.
2. `languages/<language>/README.md` — sandbox key to first classified charge, ≤ 15 minutes.
3. `failover-cookbook.md` — recipes for each outcome, reconcile policy, offline tests.
4. `failover-contract.md` — the normative contract, when a boundary question comes up.
5. `../AGENTS.md` — the whole contract on one page, for AI coding agents (and fast skimmers).

## Status snapshot (2026-08-27)

- **Spec re-pinned v2.3.0 → v2.4.0+4ce73e2 (sixth pin, SC-478)** — the skipped intermediate
  v2.3.1 is superseded. Additive delta: `vaultToken` on charge/authorize response payment
  methods (SC-461), the transaction-lookup unions switched **oneOf → anyOf** with documented
  most-specific-first discriminators and `TransactionGroupResponse` now requiring
  `transactions` (SC-408 B4), and a documented 404 on charge/authorize from the
  fallback-processor path (SC-408 B5). The anyOf switch retired every oneOf in the spec:
  the six oneOf template forks are dormant (retained), stock anyOf output proved
  names-correct and additive-evolution-safe in dotnet/php/python, and **three languages
  needed anyOf-side forks** recorded in their `pipeline/<lang>/config.yaml` — java
  (`anyof_model.mustache`: stock bound the first lenient Jackson match, mis-binding every
  terminal body as pending), typescript (`models.mustache` routing + `modelAnyOf.mustache`:
  stock merged anyOf branches into one interface and threw on bodies without the group's
  required member), and go (`model_anyof.mustache`: stock first-match decode plus
  DisallowUnknownFields in required-member branch models broke additive evolution). Go is
  stdlib-only again (validator.v2 dropped — no oneOf models import it). Quickstart READMEs
  ×6 gained the `vaultToken` note. Scorecard remediation landed the same day (PR #21:
  nanoid ≥ 3.3.18, Dependabot, CodeQL, hash-pinned pip sites; stale-review dismissal
  enabled; non-remediable alerts dismissed with justification on SC-478).

## Status snapshot (2026-08-07)

- **REGISTRY PUBLISH IS LIVE — the ADR-SDK-031 flip runbook executed 2026-08-07 in one
  sitting**: repository public (secret scanning, push protection, private-vulnerability
  reporting, fork-PR approval all enabled), guard-removal PR merged, `REGISTRY_PUBLISH_MODE=live`,
  and **v0.5.1 released ×6 from one commit as the first registry release**: NuGet
  (`Revaly.Sdk`/`Revaly.Sdk.Core`), Maven Central (`co.revaly` — Portal validation 2/2, GPG
  `packages@revaly.co`), npm (`@revaly/sdk`), PyPI (`revaly-sdk`), Packagist (`revaly/sdk`,
  placeholder deleted), and the `languages/go/v0.5.1` tag ceremony (`BlockGoModuleFormTags`
  retired; `ReleaseTagsAdminOnly` still governs). Every registry was client-verified same-day
  (install + mock-transport quickstart; npm/PyPI bytes identical to the release anchors; Maven
  signature verified). Two recorded execution deviations (npm manual first publish; php
  registry-job re-run) and the remaining custody closures live in
  `registry-provisioning.md` § The flip / § Open items. GitHub releases continue as the
  provenance anchor and fallback channel (ADR-SDK-031).

## Status snapshot (2026-08-06)

- **ADR-SDK-019 Apache-2.0 Legal-ratified IN WRITING — recorded 2026-08-06**: the written
  ratification landed; per the ratification runbook the signed record is held in the internal
  RFC-046 record (not committed here) and supersedes the 2026-07-29 verbal approval.
  Flip-runbook **gate 1 is closed** — with the ADR-SDK-032 cutover already executed through
  step 7 and **gate 2 closed 2026-08-07** (PyPI pending-publisher deviation accepted for
  launch — `registry-provisioning.md` § PyPI deviation), the step-8 public flip and the
  registry flip now wait **only on the flip acts themselves**. Nothing publishes yet: the embargo
  guards, the dark stage-6 job, and `REGISTRY_PUBLISH_MODE` are unchanged — going live remains
  the runbook ceremony (`registry-provisioning.md` § Flip to LIVE). The dated record lives in
  ADR-SDK-019 § Ratification record. Its item-2 check resolved same-day: the exact legal
  entity is **Revaly Technologies Inc.** — `NOTICE`, the dotnet runtime csproj, and the
  stage-5 nuspec stamp corrected from the incorrect "Revaly, Inc." form (no registry ever
  received it); the item-5 third-party-review status remains to record.
- **Maven Central Portal custody deviation RECORDED + ACCEPTED, 2026-08-06**
  (`registry-provisioning.md` § Known deviation: Maven Central Portal account custody):
  `co.revaly` is owned by a leadership Portal account anchored to an individual corporate
  mailbox (GitHub-SSO), not the `packages@` group mailbox — **accepted by Charles**, the
  accountable owner, on the Packagist-placeholder basis, with a post-flip closure plan
  (group-mailbox Portal account → support-add/transfer → token rotation → individual
  accounts to break-glass). A support request is in flight to add a second squad publisher
  on an individual personal mailbox; **that grant is not covered by the acceptance** — the
  review recommendation is to land the group-mailbox registration first. Account identities
  stay out of this repo (public per ADR-SDK-012).
- **Maven signing key GENERATED + VAULTED, 2026-08-06** (`maven-signing-key.md`): RSA-4096
  `07E856878E77A944169F56683ED2EB632E4EAAE7`, identity `packages@revaly.co`, expires
  2028-08-05; `maven-gpg-private-key` / `-passphrase` / `-public-key` / `-revocation-cert` in
  the publish Key Vault under leadership custody. **No registry contact, no Central Portal
  token, nothing public** — the keyserver upload is deliberately deferred and the embargo
  guards are untouched. This pulled one flip-act-6 item ahead of the ADR-SDK-019 written gate;
  accepted and recorded as a deviation (Charles, 2026-08-06) alongside the Packagist
  placeholder precedent. The java publish path is still blocked on the workload-identity +
  scoped Key Vault bindings, the Central Portal token, and the keyserver upload — the
  javadoc-jar gap closed 2026-08-07 (stage 5 ships sources + javadoc jars for both
  artifacts).

- **ADR-SDK-032 cutover EXECUTED through runbook step 7 (private phase), 2026-08-05**: this
  repository at `revaly-co/RAP-sdk` is the **new** repository carrying the sanitized-history
  transplant (153 commits; HEAD tree byte-identical to the archive's final `main`; zero
  sanitization residue — verification record in SC-263). The prior repository is
  **`RAP-sdk-archive`** (private permanently; Actions disabled; archive banner +
  `cutover-commit-map.txt` at its root; PRs #1–#55 and pre-cutover releases v0.1.0–v0.4.1
  with their provenance resolve only there). Plumbing recreated in full (three rulesets,
  `staging`/`publish` environments with the six tag policies, re-issued
  `SPEC_ARTIFACT_READ_TOKEN`); stages 1–4 proof dispatch green; **cutover release v0.5.0 ×6
  green** — restoring the interim GitHub-release artifact feed and rehearsing the dark
  stage-6 registry job on the new plumbing. dotnet and go were re-cut solo after a
  staging-load flake on the `reconcile-found-*` smoke rows (six concurrent release runs;
  `Found(Pending)` before settlement); the settle-poll hardening rides this repo's first
  PR. The repository **stays private**: step 8 (public flip) is now unblocked —
  gate 2 closed 2026-08-07 via the accepted PyPI pending-publisher deviation (the
  ADR-SDK-019 written ack was recorded 2026-08-06) — and executes with the flip sitting.
- **NuGet `Revaly.*` ID-prefix RESERVED, 2026-08-03** — NuGet.org admin confirmed "reserved
  the prefix 'Revaly' for account 'revaly'" to the owner mailbox, one business day after the
  2026-07-31 owner-mailbox resubmission. **PyPI org approval is now the only provisioning act
  still in an external queue**; everything else outstanding is publish-day (OIDC/webhook +
  the Maven bindings), Legal-unblocked since the ADR-SDK-019 written ack (recorded 2026-08-06)
  but executed only via the flip runbook — per-registry board in
  `registry-provisioning.md`.
- **History decision DECIDED: fresh-repo cutover, 2026-08-03** (ADR-SDK-032 Accepted —
  Dimitri): the public repo will be a **new** `revaly-co/RAP-sdk` carrying a
  `git filter-repo`-sanitized transplant of the full history (smoke.exe blob, pre-redaction
  doc versions, the `c584d69` message, and `@flexpay.io` author emails rewritten); the
  current repo becomes the private **`RAP-sdk-archive`** (true history, all PR threads,
  pre-cutover releases + provenance). No GitHub Support ticket, no `refs/pull/*` residue,
  PR conversations never go public. Execution rides flip-runbook gate 3: rename → transplant
  → recreate plumbing (envs, ruleset, re-issued `SPEC_ARTIFACT_READ_TOKEN`) → green
  dispatch run → cutover release ×6 → public.
- **Stage-6 registry publish built, ships DARK — 2026-08-03** (ADR-SDK-031 Proposed): the
  registry job now runs on every release tag in the protected `publish` environment —
  checksum re-verify, ADR-SDK-030 name assertions, embargo-guard integrity, per-registry
  flip-readiness report — and contacts **no registry** until the double-keyed flip
  (`REGISTRY_PUBLISH_MODE=live` + the guard-removal PR). The npm rename to **`@revaly/sdk`**
  shipped with it (committed metadata now final ×6). Flip day is a runbook
  (`registry-provisioning.md` § Flip to LIVE), not a build: written ADR-SDK-019 ack → PyPI
  org → history decision + repo public → bindings → flip → tags in GA order.
- **Registry names finalized ×6 + repo-public prep merged, 2026-07-30** (ADR-SDK-030; PRs
  #46/#47): npm **`@revaly/sdk`** (scoped) · PyPI `revaly-sdk` · NuGet
  `Revaly.Sdk`+`Revaly.Sdk.Core` · Packagist `revaly/sdk` · Maven `co.revaly:revaly-sdk` ·
  Go path unchanged — `runtime-tdd.md` §7 is now **[Decided]**, and committed metadata is
  already final everywhere except the npm rename (stage-6 prep). All six namespaces are
  reserved; the exact remaining registry acts (PyPI org approval; publish-day OIDC/GPG,
  embargoed until the ADR-SDK-019 **written** ack — NuGet `Revaly.*` prefix **reserved
  2026-08-03**) are tabulated per registry in
  `registry-provisioning.md`. The public-flip
  prep also landed: internal-infrastructure evidence relocated out of the docs at HEAD,
  SECURITY.md + CODEOWNERS + issue/PR templates added, the one open Dependabot alert fixed.
  The git-history question is now **decided → ADR-SDK-032** (2026-08-03, next bullet).
- **Prod sandbox key-scope validated ×6, 2026-07-25** (`prod-sandbox-validation.md`): the released
  **v0.4.1** artifacts — installed as a merchant installs them, from the GitHub release assets —
  were exercised against the merchant sandbox key-scope on the shared production URL through the
  real AFD/WAF edge: **6/6 languages green, 39 passed / 0 failed / 8 skipped**. Every
  failover-contract §2 row reachable there is proven ×6 (approved, success-surface decline, 4xx →
  `PermanentRejection`, reconcile `Found`/`NotFoundYet`, generated-core secondary surface). The
  harness is a separate repo — **`revaly-co/RAP-sdk-integration-tests`** — deliberately consuming
  only released artifacts, never `languages/*/` source. This is OQ-16 / ADR-SDK-024 §Decision 4
  evidence. **Key finding:** the fault injector is **inert on the production path**, so the
  `503 + not_processed` fast-failover row cannot be a live-sandbox assertion — which is precisely
  why stage 4 became two-target (next bullet) rather than demoting that row to mock coverage. Byproduct: the Backbone `firstSixDigits`/`bin` deserialization crash
  (empty value → now null) is **verified fixed** live in py+php.
- **Decision-4 retargeted to a TWO-TARGET stage 4, 2026-07-25** (ADR-SDK-024 §"Decision-4 retarget:
  two-target smoke"): each language job runs its suite **twice** — step 1 against the merchant
  sandbox key-scope on the production URL (the GA target; the injector is inert there so the
  `503+not_processed` row SKIPs) and step 2 against Backbone staging with the injector, the only
  place that row can be produced. Neither target proves the whole taxonomy alone, so running both
  keeps §2 fully covered and **nothing is demoted to mock-only** — this supersedes the
  single-target coverage-delta acceptance recorded earlier the same day. Secrets split into
  `RAP_SANDBOX_*` (step 1) and `RAP_SMOKE_*` (step 2), with the injector variable **fail-closed** (unset is an
  error, not a silent skip, precisely because the suites would otherwise SKIP the row quietly).
  **Validated green ×6** ([run 30178436668](https://github.com/revaly-co/RAP-sdk/actions/runs/30178436668)):
  step 1 `PASS (7/8, 1 skipped)`, step 2 `PASS (8/8)` with `charge-not-processed-503` passing —
  the full §2 taxonomy is proven against real servers in every language. **Decision 4 is complete.**
  Earlier the same day, the single-target form was prepared and executed — `RAP_SMOKE_FAULT_INJECT` moved to a `staging` environment
  variable (still `pre-dispatch`, so staging is unchanged) and the fail-closed guard now requires
  `RAP_SMOKE_GATEWAY_ROUTING_ID` too. Correction to earlier records: the `staging` environment and
  all three secrets **already exist** and point at Backbone staging — what is left is the repoint
  (with an **Enablement-issued** sandbox key per ADR-SDK-014) plus deleting the variable, in one
  ordered window. Decision 3 (platform reverse-dogfood) is additionally gated on a cross-repo read
  credential, the same family as OQ-17.

- RFC-046 **Approved** (v10, 2026-07-10, Charles Weiss). Jerome's approval row remains open
  (not blocking).
- Platform prerequisites: **P-1** (`ErrorResponse.code`, platform ADR 013) **merged + deployed
  to production 2026-07-14** (platform PR #238, release 29.6), together with the spec
  corrections (ADR 015), the gated spec artifact pipeline (ADR 016), the spec contract suite
  (ADR 017), and UA telemetry segmentation (ADR 018) — **SDK V1 is unblocked**. Gated spec
  artifacts are live: first release `spec/v2.1.1+f5f9576` (2026-07-14); current
  `spec/v2.3.0+80cc897` (spec-vs-reality alignment — `paymentMethodType` inference documented,
  per-type required fields, `error`-only 400 bodies documented as valid `ErrorResponse`,
  ≤48-char reference-id guidance; Backbone ADR 020 / PR #251, merged 2026-07-20; prior:
  `v2.2.1+c4000e9`, `X-Correlation-ID` header, PR #247) — **pinned as the SDK's spec input in
  `../spec/pin.yaml` 2026-07-20**, checksum + provenance verified, all six cores regenerated. **P-2** (intent reservation, platform ADR 014) remains the GA gate — the
  hot-path reservation write + duplicate suppression (409) shipped to production with 29.6
  (verified in telemetry 2026-07-14); 5-day production-load evidence recorded 2026-07-20
  (zero reservation write failures, pg P99 7.1 ms — internal R13 record on SC-278); the
  pg_cron registration rollout gate and the platform ADR-014 NFR walk remain open (Epic
  SC-234).
- Spec re-pin automation (ADR-SDK-025, 2026-07-19): the nightly **spec-freshness watchdog**
  (`.github/workflows/spec-freshness.yml`, 06:15 UTC) compares `spec/pin.yaml` against the
  platform's latest `spec/v*` release and keeps one idempotent `spec-repin` checklist issue
  alive while the pin is behind; tier 2 (platform-dispatched draft re-pin PRs) is gated on the
  cross-repo credential (OQ-17). Platform-side: the spec-reality alignment PR (Backbone #251,
  ADR 020 — paymentMethodType inference, ErrorResponse-everywhere error shapes, vaultToken
  `customerId`, reference-length caveat) **merged 2026-07-20**, publishing `spec/v2.3.0+80cc897`;
  the watchdog detected the stale pin ~30 minutes later and filed the first live `spec-repin`
  issue (#32), driving the re-pin (regen ×6 + quickstart sweep + ADR-SDK-024 corrections) —
  both watchdog live paths (pin-current, pin-behind) are now proven.
- Repository: created 2026-07-13; **transferred to `revaly-co/RAP-sdk` 2026-07-17** with the
  fleet-wide org migration (`FlexPay-io` parked, redirects alive — ADR-SDK-022 implementation
  note). The ADR-SDK-022 namespace gate is now satisfied; OQ-3 (registry accounts + protected
  publish environment, executing against `revaly-co`) remains the publish gate. Namespace
  reservation is underway on all six registries (`docs/registry-provisioning.md`): npm, NuGet,
  and Maven Central (`co.revaly`, DNS-verified) reserved org/namespace only; PyPI org pending
  approval; Go binds to the GitHub namespace. One deviation: the Packagist vendor `revaly` was
  claimed via a temporary placeholder publish (`revaly/rap-sdk` v0.0.1, MIT, standalone
  `rap-sdk-php` repo), which crosses the CLAUDE.md rule-3 embargo and ADR-SDK-019; accepted as a
  temporary hold (Charles, 2026-07-17) to be deleted and republished through the gated pipeline
  at first real publish. The `publish` environment was created 2026-07-29 (per-language
  tag-pattern policies; `languages/go/v*` excluded until the Go ceremony); OIDC/GPG bindings
  stay unregistered until the flip runbook (the ADR-SDK-019 written ack was recorded
  2026-08-06). Names finalized 2026-07-30 → ADR-SDK-030.
- **OQ-1 decided 2026-07-14 → ADR-SDK-023**: OpenAPI Generator v7.23.0, digest-pinned, all six
  cores; no Kiota split (toolchain pin: `../pipeline/generator-pin.yaml`). Evidence:
  `generator-bakeoff.md` — all six cores generated hands-on; Stainless exited the market
  (2026-05 Anthropic acquisition). Byproduct findings for the platform, both **fixed**: the five
  amount fields' `maximum: 9223372036854776000` exceeds int64 max and blocks the .NET core
  compile (Backbone PR #241 merged 2026-07-14 → `spec/v2.1.2+9af661b`; doc §3); and the orphan
  `components/schemas/PaymentMethodRequest` — unreferenced, but openapi-generator emits a model
  per schema regardless, so it would have shipped as an unusable public type shadowing
  `CreatePaymentMethodRequest` in all six SDKs (Backbone PR #242 merged 2026-07-15 →
  `spec/v2.1.3+e75c71a`). With spec pinned + generator decided, **pipeline stage 2 has no
  remaining decision gates**.
- **Pipeline stage 2 built 2026-07-15**: per-language generation configs under
  `../pipeline/<language>/` (the ADR-SDK-023 flag table, incl. the python enum
  `field_validator` template fork and the generated-code banner partial ×6),
  `../pipeline/generate.sh` (sha256-verifies the pinned artifact before generating; runs the
  generator by image digest only), and the first generated cores for **all six languages**
  under `../languages/*/core/` from `spec/v2.1.3+e75c71a` — byte-deterministic across a double
  run; the CI stage-2 job now enforces the ADR-SDK-001 regeneration diff on every PR. Package
  identities in the configs follow the `runtime-tdd.md` §7 working scheme (**[Proposed] until
  OQ-3**); license metadata is set explicitly to Apache-2.0 per ADR-SDK-019 (Legal ratification
  still gates publish, not build).
- **Pipeline stage 3 first increment built 2026-07-16**: six `Stage 3 - Build + Test
  (<language>)` CI jobs — chained after stage 2, one per language, any red blocks all —
  compile every committed core on each PR (toolchains minor-pinned/patch-floating; the TS
  core is deliberately bare, so `../pipeline/typescript/compile-check/` supplies a
  lockfile-pinned strict-tsc harness). All six v2.2.0 cores compile clean, including the
  **first-ever compile proof for the java/php/python cores** (the bake-off compile matrix
  §A1 covered only .NET/TS/Go). Unit tests, `dx-contract.md` §a ecosystem linters, and the
  ADR-SDK-020 log-capture scrub tests attach to these same jobs when `../languages/*/runtime/`
  lands. Stage-4 keys are two-phase per ADR-SDK-024: an environment-scoped staging key interim,
  the Enablement-issued sandbox key (ADR-SDK-014) at GA.
- **.NET runtime first increment built 2026-07-16** (`../languages/dotnet/{runtime,tests}/`,
  first in the ADR-SDK-015 order): the full `runtime-tdd.md` §§1–9 surface — client config
  (§1; OQ-6 timeout defaults deliberately not invented, ecosystem defaults documented), core
  re-export (§2), the three typed exceptions with **transport-level classification** per the
  failover-contract §2 normative algorithm (§3; `code` parsed as an open string from the raw
  body, never the core `CodeEnum`; the 2.0-pin narrowing honored), caller-bounded
  `ReconcileAsync` with the open verdict hierarchy incl. the P-2 pending variant (§4,
  ADR-SDK-009), `ApiKey`-prefix auth + the ADR-SDK-005 UA + `X-Api-Version` pin injected at
  transport level (§5), values-free `ILogger` output + one central allowlist scrubber +
  scrubbed wire-trace hook (§6, ADR-SDK-020), `RapMockTransport` covering every §2 row with
  consecutive-outcome scripting and the UA assert (§8), and the quickstart README teaching
  all three error classes + reconcile with the mandatory default branch (§9). 56 tests green
  including the ADR-SDK-020 CI log-capture suite; the stage-3 dotnet job now builds the
  solution, runs the tests, and enforces `dotnet format` on the hand-written projects only.
  **Byproduct findings**: (1) the generated core serializes optional enums without an IsSet
  guard (`PaymentRequest.paymentMethodType`, `CreditCard.cardType` crash when omitted) —
  **fixed 2026-07-16** via the `JsonConverter.mustache` template fork (next bullet);
  (2) the `X-Correlation-ID` response header the platform echoes (and the SDK surfaces,
  DX §c) was platform middleware behaviour not documented in the gated spec —
  **resolved 2026-07-16**: Backbone PR #247 documents it on every response (spec 2.2.1,
  contract-protected by the platform's `CorrelationIdContractTests`), re-pinned here the
  same day.
- **Optional-enum serializer defect fixed 2026-07-16** via template fork
  `../pipeline/dotnet/templates/libraries/generichost/JsonConverter.mustache` + dotnet core
  regeneration (12 model files): optional inner enums are now guarded with `Option.IsSet`
  (omitted → off the wire; set-null → JSON null; set-value → wire value), required-property
  output byte-identical to stock, double-run regeneration verified deterministic.
  Regression-tested in `ModelSerializationTests`; quickstart workaround removed. This is an
  upstream openapi-generator defect — raise it upstream at the next ADR-SDK-023 revision.
- **Java runtime first increment built 2026-07-16** (`../languages/java/{runtime,tests}/` +
  hand-written reactor aggregator `../languages/java/pom.xml`, second in the ADR-SDK-015
  order): the full `runtime-tdd.md` §§1–9 surface mirroring the dotnet shape — builder-config
  client (§1; OQ-6 timeout defaults deliberately not invented), core re-export (§2), the three
  typed **checked** exceptions ([Proposed] pending the DX §a idiomatic-reviewer sign-off) with
  the §2 normative classifier over raw bodies and the `java.net.http` never-sent taxonomy
  (`ConnectException`/`UnresolvedAddressException`/`HttpConnectTimeoutException`/
  `SSLHandshakeException` ⇒ TransientFailure; non-connect `HttpTimeoutException` ⇒
  OutcomeUnknown; 2.0-pin narrowing honored) (§3), caller-bounded `reconcile` with the open
  verdict hierarchy incl. pending (§4), runtime-owned `Authorization: ApiKey` + ADR-SDK-005 UA
  + version pin via the core request interceptor with one shared `HttpClient` (§5),
  values-free SLF4J output + the central allowlist scrubber + scrubbed wire-trace hook (§6,
  ADR-SDK-020), `RapMockTransport` (an `HttpClient` double) covering every §2 row with
  consecutive-outcome scripting and the UA assert (§8), quickstart README (§9). **67 tests
  green** incl. the ADR-SDK-020 log-capture suite; the stage-3 java job now runs the reactor
  build + tests + `spotless:check` on the hand-written modules only ([Proposed] linter choice).
  **Byproduct findings**: (1) the dotnet optional-enum serializer defect does NOT reproduce in
  the java `native` core (Jackson/JsonNullable mechanism — pinned by test); (2) **core defect,
  found and fixed same day** (next bullet): the generated oneOf wrappers on the two transaction
  GETs (`GetTransactionByMerchantTransactionId200Response`, `GetTransactionById200Response`)
  demand exactly one schema match while their all-optional branch models multi-match under
  lenient Jackson binding, so **valid 200 bodies threw inside the core**; the runtime's
  reconcile was never affected (it reads the raw body by design, repo rule 5). The four
  java-idiom **[Proposed]** choices (checked exceptions, spotless linter, interruption →
  OutcomeUnknown on payment ops, body-read timeout note) stay open for the pre-GA DX §a
  idiomatic-reviewer sign-off — decided 2026-07-16 to defer exactly those, nothing else.
- **Java oneOf discrimination defect fixed 2026-07-16** via template fork
  `../pipeline/java/templates/libraries/native/oneof_model.mustache` + java core regeneration
  (2 wrapper models, jackson2 legs only): a strict fail-on-unknown-properties first pass binds
  spec-aligned bodies uniquely; a recognized-top-level-field coverage tiebreak keeps a server
  newer than the pinned spec (additive fields — the `statementDescriptor` precedent) binding
  instead of throwing; genuinely ambiguous bodies still error (stock behaviour). Double-run
  regeneration verified deterministic; pinned in `ModelSerializationTests` (terminal / pending
  / group / additive-field / by-id wrapper); README known-limitation warning removed. This is
  an upstream openapi-generator defect — raise it upstream at the next ADR-SDK-023 revision
  together with the dotnet optional-enum fork.
- **PHP runtime built 2026-07-17** (`../languages/php/{composer.json,runtime,tests}/`, third in
  the ADR-SDK-015 order): the full `runtime-tdd.md` §§1–9 surface — named-argument constructor
  config (§1; OQ-6 timeout defaults deliberately not invented), ONE composer package
  (`revaly/sdk`, §7 **[Proposed]**) autoloading the runtime AND the re-exported core (§2), the
  three typed unchecked exceptions with the §2 normative classifier over raw bodies (§3), the
  curl never-sent taxonomy read as STRUCTURED errnos from Guzzle's handler context
  (DNS/TCP-connect/TLS-handshake errnos ⇒ TransientFailure; errno 28 is deliberately
  OutcomeUnknown — curl reports connect-phase and after-send timeouts identically, so PHP never
  claims never-sent on a timeout; 2.0-pin narrowing honored), caller-bounded `reconcile` with
  the open verdict hierarchy incl. pending (§4), runtime-owned `Authorization: ApiKey` +
  ADR-SDK-005 UA + version pin via Guzzle middleware the core cannot bypass, redirects
  hard-disabled (a followed 307/308 would resubmit a payment) (§5), values-free PSR-3 output +
  the central allowlist scrubber + scrubbed wire-trace hook (§6, ADR-SDK-020),
  `RapMockTransport` (a Guzzle handler double) covering every §2 row with consecutive-outcome
  scripting and the UA assert (§8), quickstart README (§9). **81 tests green** incl. the
  ADR-SDK-020 log-capture suite; the stage-3 php job now adds runtime manifest/lint/strict-PSR-4
  checks plus the PHPUnit suite. **Byproduct findings (all pinned by test; no template fork
  needed)**: (1) the php core's oneOf wrappers MERGE all branches into one flattened class with
  no discrimination — nothing throws (unlike pre-fork java) and nothing mis-binds to a wrong
  branch type (unlike dotnet); the runtime classifies from raw bodies (repo rule 5) and the
  README documents the merged shape; (2) the dotnet optional-enum serializer defect does NOT
  reproduce (unset optionals are omitted from serialization); (3) the bake-off §A3
  standalone-enum deserialize edge is REAL on response paths (`storedCredential.reasonType`): a
  server-newer-than-spec enum value throws inside the core on a valid 200 — the runtime contains
  it by classifying a dispatched-but-unreadable 2xx as OutcomeUnknown (dispatch-counted so
  pre-send caller errors stay `InvalidArgumentException`); reconcile then resolves it from the
  raw record.
- **TypeScript runtime built 2026-07-17** (`../languages/typescript/{package.json,runtime,tests}/`,
  fourth in the ADR-SDK-015 order; PR #22): the full `runtime-tdd.md` §§1–9 surface — object-config
  client (§1; OQ-6 defaults deliberately not invented), ONE npm package (`revaly-sdk`, §7
  **[Proposed]**, `private: true` under the embargo) compiling the core inside the runtime
  package (§2), the three typed error classes plus a discriminated-union result option (§3),
  the undici never-sent taxonomy read as STRUCTURED error codes off the cause chain
  (DNS/TCP/TLS-verify/`ERR_TLS_*` and `UND_ERR_CONNECT_TIMEOUT` ⇒ TransientFailure — the
  connect phase is distinctly typed, unlike php's errno 28; `UND_ERR_HEADERS_TIMEOUT`/
  `ECONNRESET`/unknown ⇒ OutcomeUnknown; 2.0-pin narrowing honored), caller-bounded
  `reconcile` reading raw bodies with the open verdict union (§4, a never-constructed
  sentinel member forces the default branch at compile time), one fetchApi wrapper the core
  cannot bypass injecting `Authorization: ApiKey` + the ADR-SDK-005 UA + the `X-Api-Version`
  pin (the core sends the header only when the per-call arg is set; absent would bind 2.0) +
  `redirect: 'manual'` (§5), values-free console-compatible logging + the central allowlist
  scrubber + scrubbed wire-trace hook (§6, ADR-SDK-020), `RapMockTransport` (a fetch double
  that rejects pre-dispatch on aborted signals, like real fetch) covering every §2 row (§8),
  quickstart README (§9). **111 tests green** incl. the ADR-SDK-020 log-capture suite; zero
  runtime dependencies; engines node ≥ 20.3. One §1 deviation flagged **[Proposed]** for the
  DX §a reviewer: no `connectTimeout` key (WHATWG fetch cannot bound the connect phase) — a
  `dispatcher` passthrough + README undici-Agent recipe instead. **Byproduct finding**: the TS
  core's oneOf wrappers EMPTIED terminal bodies (the all-optional `TransactionGroupResponse`
  stub `instanceOf` always matched first → every typed lookup returned an empty object —
  silent total data loss, unlike dotnet's mis-bind, java's throw, php's merge).
- **TypeScript oneOf discrimination defect fixed 2026-07-17** via template fork
  `../pipeline/typescript/templates/modelGeneric.mustache` + typescript core regeneration
  (36 all-optional models; PR #25): `instanceOf` now requires at least one declared key for
  all-optional models (required-carrying models byte-identical to stock); double-run
  regeneration verified deterministic; probes in `model-serialization.test.ts` flipped from
  pinning the defect to asserting correct binding; README known-limitation note removed.
  Upstream report due at the next ADR-SDK-023 revision together with the dotnet and java forks.
- **Python runtime built 2026-07-17** (`../languages/python/{pyproject.toml,runtime,tests}/`,
  fifth in the ADR-SDK-015 order): the full `runtime-tdd.md` §§1–9 surface — keyword-argument
  client config in seconds (§1; OQ-6 defaults deliberately not invented; per-call timeout
  overrides are the documented cancellation idiom — python has no ambient cancellation token),
  ONE distribution (`revaly-sdk`, §7 **[Proposed]**, `Private :: Do Not Upload` under the
  embargo) packaging the runtime AND the generated core in a single wheel (§2), the three
  typed exceptions with the §2 normative classifier over raw bodies (§3), the urllib3
  never-sent taxonomy read by exception TYPE (`ConnectTimeoutError` and its
  `NewConnectionError`/`NameResolutionError` subclasses ⇒ TransientFailure — one isinstance
  covers the family, and the connect phase stays distinctly typed even under a total-only
  timeout; `ReadTimeoutError`/`ProtocolError` ⇒ OutcomeUnknown; TLS: only
  `ssl.SSLCertVerificationError` is phase-provable ⇒ TransientFailure, any other `SSLError`
  ⇒ OutcomeUnknown — php-style conservatism where the stack cannot prove the phase; 2.0-pin
  narrowing honored), caller-bounded `reconcile` reading raw bodies with the open verdict
  classes (§4), the transport installed as the core's `rest_client` — the single point the
  core cannot bypass — injecting `Authorization: ApiKey` + the ADR-SDK-005 UA + the
  `X-Api-Version` pin (absent would bind 2.0), with **urllib3 `retries=False` on every
  request** (the urllib3 DEFAULT silently retries the connect phase ×3 AND follows a 307 on
  POST re-sending the payment body — a hidden resubmission, verified against a local socket
  server) and bodies materialized in-request so mid-body failures classify (§5), values-free
  stdlib-`logging` output + the central allowlist scrubber + scrubbed wire-trace hook (§6,
  ADR-SDK-020), `RapMockTransport` replacing only the wire — injection and classification run
  identically in merchant tests, transport failures simulated with real urllib3 exception
  instances — covering every §2 row with the UA assert (§8), quickstart README (§9). **129
  tests green** incl. the ADR-SDK-020 log-capture suite and real-socket single-shot proofs;
  the stage-3 python job now byte-compiles the runtime, proves the combined package
  self-contained, and runs pytest. **Byproduct findings (all pinned by test)**: (1) the python
  core's oneOf wrappers raise `Multiple matches found` for EVERY valid response shape —
  terminal, group, AND pending, both wrappers — the worst materialization across the five
  languages so far (runtime unaffected: raw reads per repo rule 5; **fixed 2026-07-17** via
  the `model_oneof.mustache` template fork, next bullet);
  (2) `ErrorResponse.code` is already OPEN in the python core — the stage-2 enum
  `field_validator` fork covers it, unknown codes pass through verbatim (no php-style
  coercion); (3) the §A3 standalone-enum edge is REAL on response paths
  (`storedCredential.reasonType` raises pydantic `ValidationError` on unknown wire values) —
  contained as dispatched-but-unreadable-2xx ⇒ OutcomeUnknown, pre-send caller errors rethrown
  untyped; (4) the dotnet optional-enum serializer defect does NOT reproduce (unset optionals
  are omitted).
- **Python oneOf discrimination defect fixed 2026-07-17** via template fork
  `../pipeline/python/templates/model_oneof.mustache` + python core regeneration (the 2 wrapper
  models only): a strict top-level-key pass binds spec-aligned bodies uniquely; a
  recognized-field coverage tiebreak keeps a server newer than the pinned spec (additive
  fields) binding; genuinely ambiguous payloads still raise the stock error. Both defective
  sites are forked — `from_json` AND the `actual_instance` validator, the latter moved to
  pydantic `mode='before'` so raw dicts are discriminated instead of silently union-coercing
  into the first all-optional branch (field names only, never values). Double-run regeneration
  verified deterministic; pins in `test_model_serialization.py` flipped from the defect to
  correct binding (terminal / group / pending / additive-field / ambiguous / both validator
  paths); README known-limitation section removed; runtime raw reads unchanged (repo rule 5).
  Upstream report due at the next ADR-SDK-023 revision together with the dotnet, java, and
  typescript forks.
- **Go oneOf discrimination defect found and fixed 2026-07-18** (pre-runtime probes for the
  sixth language) via template fork `../pipeline/go/templates/model_oneof.mustache` + go core
  regeneration (the 2 wrapper models only). Sixth and final materialization of the
  cross-language wrapper defect, in a new failure family: **zero-match instead of
  multi-match** — the stock template's per-branch `gopkg.in/validator.v2` value pass
  eliminated valid branches unconditionally on this spec (regexp validators on `Nullable*`
  struct FIELDS report "unsupported type"; `{m,n}` regexp quantifiers split on validator.v2's
  tag comma into "unknown tag"), so every terminal `TransactionResponse` /
  `TransactionGroupResponse` payload returned "data failed to match schemas" on BOTH wrappers
  (pending still bound) — the reconcile lookup and `GET /transactions/{id}` were unparseable.
  Additionally the stock strict pass made additive platform fields (minor releases) a hard
  parse failure. Fork = fleet-standard names-only algorithm (failover-contract §2: never
  values): strict unknown-fields pass, then a recognized-field-coverage pass on zero strict
  matches (required keys = json tags without `omitempty`; unique max coverage wins; bind from
  the payload filtered to known keys, lenient so nested additive fields survive); ambiguous
  payloads keep the stock errors verbatim. validator.v2 stays in `go.mod` only because the
  generator force-imports it into oneOf models (referenced, never invoked). Double-run
  regeneration deterministic; pinned by `languages/go/tests/oneof_discrimination_test.go`
  (stage-3 build-go job now runs `go test`). Joins the dotnet/java/typescript/python forks in
  the upstream report due at the next ADR-SDK-023 revision. PHP remains the only language
  needing no fork (merged-blob wrappers).
- **Go runtime built 2026-07-18** (`../languages/go/`) — the **sixth and final language**: every
  language now has its hand-written runtime. Root one-package surface `package revaly` at the
  module root (runtime-tdd §2; internals in `runtime/`, mock in `runtime/raptest` — merchants
  never import those paths for the happy path), config with `time.Duration` bounds and OQ-6
  markers (§1), typed classes `PermanentRejection` / `TransientFailure` / `OutcomeUnknown` as
  sentinel-wrapped errors dispatched via `errors.As` (§3), raw-body reconcile helper with open
  verdict interface + mandatory default branch (§4, rule-5 raw reads like python), single
  RoundTripper injecting `Authorization: ApiKey`, the exact ADR-SDK-005 UA, and the
  `X-Api-Version: 2.1` set-if-absent pin (§5 — the key lives only in the transport, never in a
  context value), values-free slog + central allowlist scrubber + scrubbed wire-trace hook
  (§6, ADR-SDK-020), `raptest.MockTransport` replacing only the wire with every §2 row
  scriptable (§8), quickstart README with all three classes + reconcile default branch (§9).
  **Runtime findings (all pinned by test):** stdlib `http.Client` re-POSTs a 307 redirect body
  (probed — double-charge hazard) → redirects always disabled, 3xx classifies OutcomeUnknown;
  the never-sent proof is `*net.OpError{Op:"dial"}` (covers refused/DNS/dialer connect-timeout)
  plus `*tls.CertificateVerificationError` — a context deadline expiring during the dial is NOT
  phase-provable → OutcomeUnknown (documented: set `ConnectTimeout` to get the dial-phase
  proof); generic TLS failures → OutcomeUnknown (php/python conservatism); core `ErrorResponse`
  is strict-parse so the classifier reads raw bodies leniently itself; the §A3 enum edge does
  NOT exist in Go (`enumUnknownDefaultCase` maps unknown wire values to the UNKNOWN member
  without a parse error — no containment needed). Stage-3 build-go job extended with a gofmt
  format check over the hand-written packages (`go test ./...` landed with the fork PR);
  `.gitattributes` pins hand-written `*.go` to LF.
- **Pipeline stage 4 built + ADR-SDK-024 Accepted 2026-07-18** (OQ-16 closed): six
  `Stage 4 - Contract Smoke (<language>)` CI jobs chained after stage 3, gated to release tags
  (blocking) + the nightly schedule (advisory) + manual dispatch — never plain PRs. Each runs
  the thin live suite `../languages/<lang>/smoke/` (quickstart-shaped, values-free output,
  identical 8-scenario matrix): charge approved and deterministically declined (expired card),
  server-side validation rejection (**empty PAN** → 400 — negative amounts would fail
  pydantic client-side in python and never reach the wire), auth rejection (synthetic bad key
  → 401), the injected `503 + code=not_processed` fast-failover row via the platform's
  staging-only `X-Backbone-Fault-Inject: pre-dispatch` executor seam (platform ADR 014;
  SKIPs where unset — structurally inert in production), and reconcile `Found(Approved)` /
  `Found(Declined)` / `NotFoundYet` (fresh ids; last-status-404 asserted), with correlation-id
  presence asserted on every path (DX §c; wire-trace hooks observe the success surfaces).
  Secrets are environment-scoped (GitHub environment **`staging`** — names in
  `pipeline-and-release.md` §6, borrowed from the platform's staging E2E key pool; scope lives
  on the key; staging always simulates); jobs fail closed when
  unprovisioned. **Provisioning the environment + three secrets is the one open act.**
  Byproduct finding: the Go quickstart's `revaly.NewPaymentRequest(...)` did not exist —
  the root package re-exported model *types* but not their constructors (runtime-tdd §2 gap;
  the published quickstart didn't compile) — fixed in `../languages/go/revaly.go`; the smoke
  suites now double as stage-3 compile-guards over every quickstart surface. The platform-repo
  reverse-dogfood job and the GA sandbox retarget remain (ADR-SDK-024 §Decisions 3–4);
  **OQ-11 stays undischarged** (staging bypasses the AFD/WAF edge).
- **Pipeline stage 5 + interim stage 6 built + ADR-SDK-026 Accepted 2026-07-20**: per-language
  **GitHub release artifacts** as the sanctioned interim distribution (repo rule 3) —
  `../pipeline/package.sh` (stage-5 entry point: packages the committed tree at HEAD via
  `git archive`, stamps the tag version into the ephemeral copy only — committed manifests keep
  their `0.0.0-dev` placeholders — and emits asset + `.sha256` + `provenance.json` +
  release notes mapping version → spec SHA, the platform `spec/v*` model) and two new
  `pipeline.yml` jobs (`package`, `github-release`) chained after all six stage-4 smoke jobs,
  release-tag-only, with an in-job tag-on-`main` ancestry proof (ADR-SDK-013). Tag scheme
  `<lang>/vX.Y.Z`; **go tags `go/v*`** (the module-activating `languages/go/v*` form is refused
  and reserved for the gated Go registry publish); versions are plain `X.Y.Z` — the interim
  channel ships **no pre-release identifiers** (decided 2026-07-20). `LICENSE` (Apache-2.0) +
  `NOTICE` landed at the repo root (ADR-SDK-019 bootstrap; Legal ratification still gates
  registry publish only). **First cut: `v0.1.0` across all six languages, tags cut sequentially
  in GA order after this lands on `main`.** Registry publish (real stage 6) remains embargoed
  behind OQ-3 + ADR-SDK-013 machine gates + ADR-SDK-019 ratification. Follow-up (repo-admin):
  tag ruleset for `*/v*` creation + a hard block on `languages/go/v*` (ADR-SDK-026
  §Consequences) — ✅ done 2026-07-20: rulesets `ReleaseTagsAdminOnly` (admin bypass only) and
  `BlockGoModuleFormTags` (no bypass, proven live against an admin push) are active; lifting
  the go-form block is a deliberate admin ceremony at the real Go registry publish.
- **OQ-6 decided 2026-07-20 → ADR-SDK-027 Accepted** (with the R13 evidence run): the
  overall-deadline default is **75 seconds** across all six runtimes, ratified from production
  telemetry (two independent sources — RAP-path 5-day per-gateway percentiles + a 14-day
  unsampled gateway-fleet window; the 30 s telemetry floor clips ~1 in 9,500 — ratified at 75 s
  as an owner safety margin clearing every observed non-ceiling tail (worst 64 s), clipping
  ≲0.007 %, 25 s under the platform's ≈100 s ceiling; full evidence in the internal OQ-6
  record on SC-278).
  Implemented as config defaults with per-language opt-out sentinels
  (`Timeout.InfiniteTimeSpan` / `noOverallDeadline()` / `overallDeadline: null` /
  `overallDeadlineMs: null` / `overall_deadline=None` / `revaly.NoOverallDeadline`) and
  default/opt-out/validation tests ×6 — superseding every earlier "OQ-6 defaults deliberately
  not invented" marker in the per-language bullets above. Deliberate residuals: **no connect
  default** (not derivable from server-side data → OQ-11, already the hard pre-GA edge gate)
  and **no reconcile-policy defaults** (need post-charge visibility-lag telemetry → SC-261
  follow-up). The same evidence pull recorded the R13 intent-reservation production-load
  results (5 days: zero reservation write failures, pg P99 7.1 ms, zero 5xx) — the SC-278
  R13 "sized and load-tested" clause is signed off at story level;
  the platform ADR-014 NFR walk stays open. The new defaults ship in the next release cut
  (v0.2.0 ×6).
- **v0.1.0 + v0.2.0 released ×6 2026-07-20** through the ADR-SDK-026 interim channel (tags
  `<lang>/vX.Y.Z`, go as `go/v0.2.0`; asset + `.sha256` + `provenance.json` per release):
  all six v0.2.0 artifacts built from one commit with identical spec provenance
  (`spec/v2.3.0+80cc897`) and all four quality gates green — v0.2.0 carries the ADR-SDK-027
  75 s deadline defaults. Tag rulesets (ADR-SDK-026 follow-up) proven live in the same run.
- **Pre-GA idiom review closed 2026-07-21 → ADR-SDK-028 Accepted**: four per-language
  dx-contract §a idiomatic reviews (java/go/python/typescript) + an adversarial cross-language
  coherence pass, every verdict verified against the tree. All flagged **[Proposed]** idiom
  choices are now **[Decided]** — this bullet supersedes the earlier "pending the DX §a
  idiomatic-reviewer sign-off" phrasing in the per-language bullets above. Ratified as built:
  java checked exceptions + interruption→OutcomeUnknown (now pinned by test), go
  Duration/`errors.As`/sealed-open-verdict/`raptest` designs, python cancellation idiom + TLS
  conservatism, TS no-`connectTimeout` (dispatcher passthrough; OQ-11 default absorbed at
  documentation level when it lands). Corrected: go layout fence — internals to
  `internal/runtime/`, mock lifted to `languages/go/raptest/` (**amends ADR-SDK-016**;
  supersedes the "internals in `runtime/`, mock in `runtime/raptest`" paths in the go bullet
  above), go pointer request params + `Config.Wire`→`Transport` (runtime-tdd §1 key now 6-of-6),
  TS verdict discriminants → PascalCase (matches the cross-language log vocabulary; log output
  byte-identical), java `ReconcilePolicy.builder()` (shape only — SC-261 defaults untouched),
  java deadline-semantics caveat (headers-bounded; stall → OutcomeUnknown → reconcile), python
  `py.typed` ×2 + `__all__` + `__version__` + `RapWire` Protocol, copy-block deadline hygiene
  (TS 10 s + go 30 s overrides dropped — quickstarts never silently undercut the ratified 75 s).
  dx-contract §a "standard linters in CI" closed ×4, pinned, hand-written surfaces only:
  **Error Prone 2.50.0** (java, forked-jvmArgs wiring), **eslint 10.7.0 + typescript-eslint
  8.65.0** (TS, lockfile-isolated lint toolchain), **ruff 0.15.22** (python), **staticcheck
  v0.7.0** (go). Breaking subset ships as ONE coordinated pre-GA break in the next cut
  (v0.3.0 ×6; migration notes in release notes). Verified green at adoption: java 79 / python
  138 / TS 115 tests, go full gate set. dotnet/php had no flagged items — the full §a GA
  checklist per language (all six) remains a GA-gate activity. OQ-2/OQ-3/OQ-11/SC-261
  explicitly untouched.
- **v0.3.0 + v0.3.1 released ×6 2026-07-21**: v0.3.0 carries the ADR-SDK-028 coordinated
  pre-GA breaking batch (migration notes on every release); v0.3.1 is a patch re-cut off the
  CI warning cleanup (node24 artifact-action pins, javadoc-skip on generated cores,
  EnumOrdinal suppression) plus the stage-6 download-artifact v8 layout fix — all six
  pipelines green with **zero warning annotations**, identical spec provenance
  (`spec/v2.3.0+80cc897`, source commit fc36ad4).
- **OQ-11 closed 2026-07-21 → ADR-SDK-029 Accepted** (the hard pre-GA edge gate): AFD/WAF
  edge behaviour verified against the live production edge — 30-day census of
  `api.revaly.co`: **one** edge 5xx total (a 504/OriginTimeout on a synthetic health
  probe, connect-phase at ~4 s, origin provably never received it), zero 502s, zero
  AFD-generated 503s; the WAF blocks only scanner/hostile traffic, and its bot-management
  rules — where server-side SDK clients land — are Log-only;
  origin error bodies pass through unmodified, so the P-1 `503 {code: "not_processed"}`
  signal survives the edge. `failover-contract.md` §2 edge rows ratified unchanged, with two
  documented nuances: an edge 504 can fire at ~4 s (never implies the deadline elapsed), and
  edge bodies are HTML — the open-string `code` fallthrough is load-bearing.
  **Connect-timeout default ratified: 10 s ×6** (undici precedent; ~25× the observed cold
  client→edge TLS envelope; honours the ADR-SDK-028 §4 constraint, 10 < 75) with
  per-language opt-out sentinels — TypeScript at documentation level. Timeout ordering
  ratified: SDK 75 s < platform ≈100 s < AFD 120 s, with an ops guardrail on lowering the
  edge timeout or hardening Bot Manager. Ships v0.4.0 ×6. The ADR-SDK-024 GA sandbox
  retarget now waits only on its ADR-SDK-014 parity leg.
- **External SDK-tester audit (Jarvis) verified + fixes landed 2026-07-23**: eight findings
  against the v0.4.0 artifacts — six confirmed, two refuted, every verdict evidence-checked
  against the shipped release assets. Confirmed + fixed: the dotnet `Revaly.Sdk.Core` nupkg
  shipped generator placeholder metadata (authors "OpenAPI", `GIT_USER_ID/GIT_REPO_ID` repo
  URL, "No Copyright") and an unused `Microsoft.Extensions.Http.Polly` dependency — both now
  corrected at stage-5 by staged-copy transforms with fail-closed nuspec verification (the
  `package_java` versions:set precedent; the generator-config-level fix is a pre-GA follow-up
  under ADR-SDK-023); the TS package failed strict Node-only compiles (`skipLibCheck: false`,
  no DOM lib — TS2304 on `RequestCredentials`/`RequestInfo`) — hand-written runtime typings
  are now Node-clean (`string | URL | Request`), and the generated core's DOM aliases are
  README-documented and deferred to the pre-GA template review; quickstarts ×6 now carry
  `orderId` + `paymentMethod.email` (staging-simulator approval requirement — the §9 ≤15-min
  bar was unmeetable without them); the go README is release-agnostic with zip-consumption
  instructions (was frozen at "v0.2.0 shipped"); READMEs ×6 gained a raw-core-exception
  logging caution (generator exception messages/objects can embed response bodies — Java
  verbatim in `getMessage()`, Python in `str()`, Go in `Error()`, PHP via the Guzzle
  summary). Refuted: the python tar.gz-vs-wheel claim (the release ships both; README now
  says so) and the PHP reconcile transport-failure→`NotFoundYet` report (identical,
  contract-conformant degraded-read behavior in all six languages; `runtime-tdd.md` §4
  gained the `lastHttpStatus=null` = API-unreachable explanatory note). Mock payment-methods
  routes remain a deliberate runtime-tdd §8 scope choice (dotnet/TS ship raw `stub()`
  escapes) — logged as a v-next enhancement.
- Accepted-at-approval follow-ups: PRD-057 deviation acceptance (Product), squad NFR walk —
  tracked in `open-items.md`.
