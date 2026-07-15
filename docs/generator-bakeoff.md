# OQ-1 Generator Bake-off — Evidence & Recommendation

**Date:** 2026-07-14 · **Prepared for:** SC Eng (OQ-1 owner) · **Status:** Ratified 2026-07-14
→ **ADR-SDK-023** (OQ-1 closed; this document remains the evidence record — the ADR is the
decision).
**Question (RFC-046 §11 / `open-items.md` OQ-1):** openapi-generator vs commercial
(Speakeasy / Fern / Stainless; Kiota for .NET) — quality-per-language vs license cost.
**Acceptance criterion:** the DX contract §a idiomatic bar; a generator that cannot meet it
*with template customization* is disqualified (`dx-contract.md` §a, ADR-SDK-001).

**Inputs.** Gated spec artifact `spec/v2.1.1+f5f9576` (sha256 `c9254a82…72df6` verified against
`.sha256` + `provenance.json`, all platform gates pass). Hands-on runs: openapi-generator
**v7.23.0** (Docker `openapitools/openapi-generator-cli:v7.23.0`, manifest digest
`sha256:5ffccd3b0d4ac57eac443e1c9b3e2f2bb7f0a21ffe6c6701f3690d7edc78bf2d`, verified locally —
identical to `latest-release` at research date), Kiota **1.34.1**. Desk research on all five candidates verified against July-2026 sources
(vendor docs/pricing pages, repos, registries). Hands-on evidence in the appendix; every claim
about *our* spec below was reproduced locally, not taken from marketing.

## 1. One-page comparison

| Criterion (hard gates first) | openapi-generator v7.23.0 | Speakeasy | Fern | Stainless | Kiota 1.34.1 (.NET role) |
| --- | --- | --- | --- | --- | --- |
| **Available to us at all** | ✅ Apache-2.0 OSS | ✅ commercial | ✅ commercial — **acquired by Postman 2026-01-08** ("roadmap unchanged") | ❌ **acquired by Anthropic 2026-05-18; hosted generator closed to new customers** | ✅ MIT OSS |
| **Six languages at GA grade** | ✅ all six client generators STABLE tier | ✅ all six GA | ✅ all six GA (PHP youngest; 9 languages total) | (moot) | ❌ 5/6 stable; **TypeScript still Preview** (multi-year, preview-numbered runtime packages) |
| **Pinned, offline, deterministic generation** (pipeline stage 2 regen-diff; toolchain checksum-pinned) | ✅ digest-pinned Docker, no account, no egress; hands-on: byte-identical except self-generated GUIDs (pinnable via `packageGuid`) | ⚠️ CLI runs locally **but requires `SPEAKEASY_API_KEY` + phones home run metadata** (no documented off switch); CLI is Elastic-2.0 with license-key clause → regeneration continuity risk if contract/vendor ends | ⚠️ default = **remote cloud generation**; supported local mode is **Enterprise-gated** (`FERN_TOKEN` + org-verification network call — spec data stays local); generator images Docker-pinned; Replay merge must be off for hermetic regen; generators are Apache-2.0 (forkable if vendor exits) | (moot) | ✅ local CLI; hands-on: deterministic except `.kiota.log`; needs `--clean-output --clear-cache`, `KIOTA_OFFLINE_ENABLED=true`, telemetry opt-out |
| **DX §a reachable via template customization** | ✅ mustache partial overrides per language (only forked files maintained) | ⚠️ no templates; overlays + `x-speakeasy-*` + hooks; custom-code regions Java/Py/TS only, Enterprise-gated | ⚠️ no templates; per-generator config keys + `x-fern-*` overrides overlay + `.fernignore`/Replay; deeper change = fork the OSS generators | (moot) | ❌ **no template system by design; "code readability is a non-goal"** — fails the §a customization clause |
| **Runtime fully wraps/hides core; forced `User-Agent`** (ADR-SDK-001/005) | ✅ verified all six: injected HttpClient/OkHttp-or-JDK/Guzzle/fetch/httpx-or-subclass/RoundTripper | ✅ hooks + injected clients (PHP = Guzzle-coupled); must override baked `speakeasy-sdk/…` UA that conflicts with ADR-SDK-005 | ✅ injected clients all six (PHP = PSR-18); must strip `X-Fern-*` + own UA (`omitFernHeaders` per language) and force UA at transport level (header-level config is caller-overridable) | (moot) | ✅ RequestAdapter architecture; but `Microsoft.Kiota.*` types sit in generated public signatures (C#-only `Internal` modifier mitigates) |
| **Open-string safety on our actual spec** (`ErrorResponse.code` ships as a closed `enum:` in the artifact — §A3) | ✅ achievable everywhere: `enumUnknownDefaultCase` (java/go/php; honored for csharp in 7.23.0 output) + TS runtime pass-through + **one-partial python override (required — pydantic validator throws)** | ⚠️ enums closed by default (TS/Zod throws on unknown); `x-speakeasy-unknown-values` covers 5/6 — **no PHP support** | ✅ **best default posture of all candidates**: C# forward-compatible by default, Java always-open (`visitUnknown`), TS/Python/Go/PHP pass through unknowns | (moot) | ⚠️ unknown enum → silently null (contradicts own docs; open issue); verbatim value lost |
| **No retries / breakers in shipped core** (failover-contract §5) | ✅ none in any of the six cores; csharp emits *opt-in* Polly extension file → excluded via `.openapi-generator-ignore` | ✅ retries strictly opt-in (`x-speakeasy-retries` absent → none); verify no dormant retry utils ship | ❌ **retries default-on in every language** (2 retries, backoff, 408/429/5xx) and the **machinery is not excludable** — generator default can be set to 0 but `maxRetries` stays reachable on core client/request surfaces | ❌ (reference point: shipped default-on retries incl. 409) | ⚠️ default `KiotaClientFactory` pipeline includes RetryHandler — runtime must construct adapter with explicit middleware chain |
| **Output licensable Apache-2.0, our copyright** (ADR-SDK-019) | ✅ README §3.4: generated code "owned by the user … licensing terms that you deem appropriate" | ✅ customer-owned, MIT default, relicensable | ⚠️ license configurable (SPDX or custom file, Apache-2.0 fine); **no output-ownership clause found in public ToS** — contractual ownership unverified | (moot) | ✅ no claim on output (MIT tool) |
| **Publish-embargo / monorepo fit** (no repo or registry coupling) | ✅ emits code only | ✅ code-only into subdirs supported; their GitHub Action optional | ✅ `local-file-system` output mode into an arbitrary path | ❌ (managed per-SDK repos was the model) | ✅ code only |
| **License cost (six languages)** | $0 — cost is template-maintenance time across pinned upgrades | **≈ $43–52k/yr** (Business $600–720/mo/language) | **≈ $18–43k/yr** list (Basic $250 / Pro $600 per SDK/mo, annual); hermetic local generation = Enterprise (custom $) | (moot) | $0 |
| **Vendor/vocabulary risk** | ~8–9 minors/yr, every minor "breaking changes (with fallback)" → pin exact + regen-diff; 26.5k★, active daily | pivoting to MCP/agents platform; SDK gen still shipped; $26M raised, no Series B | Postman acquisition 4 months old; press framing docs-weighted; SDK generators still shipping daily; OSS generators de-risk a wind-down | exited the market | Microsoft-backed; monthly cadence; but OTel is a hard transitive dep of its runtime in 5/6 languages — heavy for a PCI-scoped payments core |

**Disqualifications under the OQ-1 criteria:** **Stainless** (not procurable — market exit).
**Kiota** for the six-language role (no customization path to §a; TS Preview); for the
.NET-only split role it *works* but offers no advantage over the selected option while adding a
second toolchain, Graph-style verb builders (`PostAsync`, not payments idiom), and
Microsoft-versioned abstractions in the re-exported surface — rejected on uniformity.
**Fern** is blocked by two hard gates as shipped: non-excludable default-on retry machinery in
every core (failover-contract §5), and Enterprise-gated, phone-home local generation (pipeline
§6 hermeticity) — despite the best open-enum defaults in the field.

## 2. Recommendation (for SC Eng to ratify or reject)

**Adopt OpenAPI Generator v7.23.0, digest-pinned, for all six cores. Do not split .NET to
Kiota.** Rationale, in the RFC's own terms:

1. It is the only live candidate that clears **every hard gate simultaneously** — six STABLE
   generators, zero-egress digest-pinned generation compatible with `pipeline-and-release.md` §6
   ("checksum-pinned like any release tooling"), explicit user ownership of output, no publish
   coupling, $0 license.
2. The idiomatic gap — the real historical weakness of openapi-generator, and why ADR-SDK-001
   Option B (raw codegen *as the product*) was rejected — is closed by the architecture we
   already decided: the hand-written runtime is the merchant-facing surface; the core is hidden
   behind it except **re-exported models**, which hands-on runs show are plain idiomatic DTOs
   (pydantic v2 models, POJOs+builders, TS interfaces, Go structs, PHP models, C# classes).
   §a enforcement stays where the DX contract puts it: per-language GA checklist signed by an
   experienced developer in that language.
3. Known §a watch-item, recorded honestly: the C# generichost models expose an `Option<T>`
   set/unset pattern on non-required properties (defensible — distinguishes unset from null —
   but unusual). The .NET checklist reviewer decides; fallbacks exist (model template partial,
   or `restsharp` library at the cost of a Newtonsoft dependency).
4. The commercial field self-eliminated on our constraints. **Stainless** exited the market.
   **Fern** — the best enum-openness defaults of any candidate — ships default-on retry
   machinery that cannot be removed from the core (a direct failover-contract §5 conflict: an
   auto-retried ambiguous `POST /payments` is precisely the double-charge hazard of
   failover-contract §1) and gates hermetic local generation behind Enterprise with an
   org-verification phone-home. **Speakeasy** is the
   closest runner-up: retries are genuinely opt-in and the monorepo/hooks story is good, but it
   costs ≈$43–52k/yr against a $0 alternative whose gap our architecture already closes, its PHP
   open-enum hole lands on safety-relevant behavior, its Elastic-licensed key-gated CLI
   reintroduces the vendor-continuity risk the pipeline design exists to avoid, and its baked
   `speakeasy-sdk/…` User-Agent fights ADR-SDK-005. Revisit a commercial generator only if a
   per-language §a checklist fails in a way template work cannot close.

**Pinned per-language generation configs** (all mitigations are generator-flag or
template-partial level — the spec artifact is never edited, per ADR-SDK-006):

| Language | Generator / library | Required flags & overrides |
| --- | --- | --- |
| .NET | `csharp` / `generichost` (default; `httpclient` lib is officially Experimental) | `enumUnknownDefaultCase=true`, `packageGuid=<fixed>`, `hideGenerationTimestamp=true`; ignore-list: Polly `IHttpClientBuilderExtensions` + test scaffolding; banner partial |
| Java | `java` / `native` (JDK 11+ HttpClient + Jackson — leaner than default okhttp-gson) | `enumUnknownDefaultCase=true`, `hideGenerationTimestamp=true` (java default is **false**), `licenseName=Apache-2.0` (pom defaults to Unlicense); banner partial |
| PHP | `php` / `guzzle` (psr-18 lib still beta) | `enumUnknownDefaultCase=true` (setter-level; deserializer edge tracked in §A3); banner partial |
| TypeScript | `typescript-fetch` (zero runtime deps) | strict tsc verified; unknown enum values pass through at runtime (verbatim preserved); banner partial |
| Python | `python` (pydantic ≥2.11) | **one-partial override of the emitted enum `field_validator`** (no `enumUnknownDefaultCase` for python; stock validator throws on unknown wire values — unacceptable on success-path models); banner partial |
| Go | `go` (stdlib-only for our spec) | `enumUnknownDefaultCase=true` for named enums; inline property enums (incl. `ErrorResponse.code`) already emit as plain `*string`; banner partial |

Uniform safety rule regardless of generator (restates `runtime-tdd.md` §3): **the runtime
classifies failures from the raw response it already holds — never from a core model enum** —
so typed errors carry `code` verbatim even where a core enum collapses or nulls unknowns.

**Closure executed 2026-07-14:** ADR-SDK-023 records this table + the pin (tag `v7.23.0` +
image digest committed at `../pipeline/generator-pin.yaml`);
`open-items.md` OQ-1 row → Decided; upgrades of the pin ride PRs where the regen-diff makes the
blast radius reviewable.

## 3. Findings that leave this repo (platform follow-ups)

1. **Spec defect (blocks .NET core compile):** the five amount fields carry
   `maximum: 9223372036854776000` — that is 2^63 rounded through an IEEE-754 double and
   **exceeds int64 max (9223372036854775807)**, i.e. unrepresentable in the field's own
   `format: int64`. openapi-generator faithfully emits it as a C# `long` constant → `CS0221`
   compile error ×5 (fails closed — the only candidate that surfaced the defect; Go/TS/Kiota
   silently drop the constraint). Diagnostic regeneration from a corrected copy compiles
   0 warnings / 0 errors, isolating the defect as the sole blocker. Root cause is upstream of
   the source file: the schema source holds the *exact* int64 max, but the Node-based redocly
   bundler parses YAML integers as IEEE-754 doubles and rounds anything past 2^53 — no literal
   near 2^63 can survive bundling, so the constraint (vacuous for `format: int64`) is removed
   rather than the value adjusted. **Fix merged: FlexPay-io/Backbone#241** (2026-07-14) — drops
   `maximum` ×5, bumps spec to 2.1.2; published as `spec/v2.1.2+9af661b` (all four gates pass)
   and pinned as the SDK's spec input (`../spec/pin.yaml`) the same day — since superseded by
   `spec/v2.1.3+e75c71a` (§3.3).
2. **Vocabulary hygiene (next spec minor, non-blocking):** response-side *inline closed enums*
   remain in the artifact (`ErrorResponse.code`, `cardType`, `providerAuthDecision`, …) even
   after `transactionType` was widened (platform PR #240). Any new wire value breaks python
   deserialization (and java without our flag) on **success paths**. The SDK mitigations above
   contain it; recommend the platform apply the ADR-SDK-010 open-vocabulary stance to these
   fields at the next spec minor.
3. **Orphan schema (fixed):** `components/schemas/PaymentMethodRequest` was defined but
   referenced by no operation — the superseded ancestor of `CreatePaymentMethodRequest`
   (same `paymentMethodType` enum and `PaymentMethod` `$ref`; Create added `customerId` and
   relaxed `required`). Surfaced by `redocly lint` (`no-unused-components`) during pipeline
   stage-1 bring-up, 2026-07-15. It matters because openapi-generator emits a model for **every**
   `components/schemas` entry regardless of reachability, and `core/` is never hand-edited
   (repo rule 1) — so it would have shipped as a public type in all six SDKs that no operation
   accepts, with a shorter and more intuitive name than the one merchants actually need. Removing
   a public type after 1.0 is a semver-major break, so this was pre-GA or never. **Fix merged:
   FlexPay-io/Backbone#242** (2026-07-15) → `spec/v2.1.3+e75c71a`, pinned the same day; bundle
   diff is exactly `info.version` + the 41-line schema removal. The remaining `redocly lint`
   warning is `info-license`, which is **deliberately not fixed in the spec** — the API
   description's license is not the SDK's license (ADR-SDK-019); instead set the license fields
   explicitly per language in the stage-2 generator config (§2) rather than letting the generator
   default them into published package metadata.

## Appendix A — hands-on evidence (2026-07-14, spec/v2.1.1+f5f9576)

### A1. Generation & compile matrix

| Run | Generator config | Generate | Compile/check |
| --- | --- | --- | --- |
| cs-runA/B | csharp generichost, `hideGenerationTimestamp` | ✅ 220 files ×2 | ❌ `CS0221` ×5 — **sole cause: spec `maximum` defect (§3.1)** |
| cs-runG (diagnostic) | same + corrected `maximum` in a scratch copy — *not* pipeline input | ✅ | ✅ **0 warnings / 0 errors** |
| cs-runC/F | + `enumUnknownDefaultCase`; `library=httpclient` variant | ✅ | (same defect; httpclient lib also Experimental — not selected) |
| ts-runD | typescript-fetch | ✅ | ✅ `tsc --strict` clean |
| go-runE | go | ✅ | ✅ `go build ./...` clean |
| java-runH | java `library=native` | ✅ 211 files | not compile-tested (no JDK build attempted) |
| php-runI | php | ✅ 196 files | not compile-tested |
| py-runJ | python | ✅ 205 files | not compile-tested |
| kiota cs-run1/2 | Kiota 1.34.1 C# ×2 | ✅ 134 files | ✅ compiles vs `Microsoft.Kiota.Bundle` 2.x |

### A2. Determinism (two identical runs, SHA-256 per file)

- openapi-generator csharp: **218/220 byte-identical**; only diffs = freshly generated solution
  GUIDs (`.sln`, README `packageGuid`) — eliminated by pinning `packageGuid` and/or excluding
  scaffolding from `core/` via ignore-list. Code files: zero diffs.
- Kiota: all code byte-identical; only `.kiota.log` differs. Regen-diff CI would need
  `--clean-output --clear-cache` (unchanged-hash runs are otherwise skipped).

### A3. `ErrorResponse.code` (spec ships `enum: [not_processed, outcome_unknown]`) — observed behavior on unknown wire values

| Output | Emitted shape | Unknown value at deserialization | Verbatim string recoverable from model? |
| --- | --- | --- | --- |
| csharp generichost | closed `CodeEnum` (+`UnknownDefaultOpenApi` with flag — honored in 7.23.0 output despite absent docs) | deserializer uses `…FromStringOrDefault` → **null** (no throw); public `CodeEnumFromString` helper throws (footgun, hidden by runtime wrap) | no → runtime reads raw body (uniform rule) |
| java native | closed enum, `fromValue` throws `IllegalArgumentException` | **throws without flag**; returns `UNKNOWN_DEFAULT_OPEN_API` with flag | no → raw body |
| php | class constants + allowable-values check | setter throws without flag; coerces with flag (standalone-enum deserialize path stays strict — tracked) | partially |
| typescript-fetch | literal-union type; `FromJSON` is a cast | **passes through untouched** | **yes** |
| python | `StrictStr` + emitted `@field_validator` | **`ValueError` — throws; no flag exists** → template-partial override required | after override: yes |
| go | **plain `*string`** (inline property enums not projected) | passes through | **yes** |
| Kiota C# | closed enum `ErrorResponse_code` | `GetEnumValue<>` → silently null (contradicts Kiota docs; upstream issue open) | no |

### A4. Wrap/hide & forced User-Agent (ADR-SDK-001 "verify the runtime can fully wrap the generated layer")

Verified injection points — .NET: DI `AddHttpClient` + DelegatingHandler (runtime-owned);
Java native: injected JDK `HttpClient`; PHP: injected `GuzzleHttp\ClientInterface`
(handler-stack middleware); TS: `fetchApi` override + pre/post middleware + per-request headers;
Python: `user_agent`/`default_headers` (header-level) or `RESTClientObject` subclass
(transport-level — weakest of the six, adequate); Go: `NewAPIClient` *requires* a UA string and
stamps it on every request (`client.go:422`), transport override via `http.RoundTripper`.
No generated core sets its own competing User-Agent (default `OpenAPI-Generator/{version}/{lang}`
replaced at generation via `httpUserAgent`, enforced at transport by the runtime per ADR-SDK-005).

### A5. Retry surface audit

Grep of all six openapi-generator cores: zero retry/breaker logic in request paths. Sole hit =
csharp `IHttpClientBuilderExtensions.cs`, *opt-in* Polly retry/timeout/circuit-breaker helper
extensions (never invoked by generated code) → excluded from `core/` via ignore-list so the
public surface cannot even offer them (failover-contract §5). Comparison points: Stainless
shipped default-on retries (2 retries incl. HTTP 409 — a double-charge hazard on payment POSTs);
Speakeasy is opt-in-by-extension (acceptable); Kiota's default client factory installs a
RetryHandler (must be assembled without it).

### A6. Sources

Candidate fact sheets compiled 2026-07-14 from: OpenAPITools/openapi-generator v7.23.0 tag
(docs + templates + release/milestone API), Docker Hub digests; microsoft/kiota +
learn.microsoft.com Kiota docs + msgraph SDK repos + kiota-dotnet/-typescript releases;
speakeasy.com docs/pricing/legal/product-security + speakeasy-api repos (CLI ELv2 license text)
+ Mistral production SDK inspection; stainless.com blog ("Stainless is joining Anthropic",
2026-05-18) + TechCrunch 2026-05-18 + pricing/docs pages; buildwithfern.com docs
(generators-yml reference, self-hosted deep-dive, retries deep-dive, custom-code/Replay) +
fern-api/fern `seed/` generated-output fixtures (enum behavior verified per language against
committed snapshots) + Docker Hub generator-image tags + blog.postman.com acquisition
announcement (2026-01-08) + Series-A coverage. Competitor-authored comparisons treated as
marketing-adjacent and used only where directionally corroborated.
