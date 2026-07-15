# ADR-SDK-023 — Generator Selection: OpenAPI Generator v7.23.0, Digest-Pinned, All Six Cores

**Status:** Accepted — decided 2026-07-14 (OQ-1 closure); ratification = SC Eng review + merge
of this ADR's PR
**Source:** RFC-046 §11 OQ-1 (build gate confirmed at the approval walk); evidence:
[`../generator-bakeoff.md`](../generator-bakeoff.md) (2026-07-14 — hands-on generation of all
six cores + July-2026 market research verified against primary sources)
**Owner:** SC Eng

## Context

OQ-1 left the generator choice open: openapi-generator vs commercial (Speakeasy / Fern /
Stainless; Kiota for the .NET role), judged as quality-per-language vs license cost. The
acceptance criterion is the DX contract §a idiomatic bar — a generator that cannot meet §a
*with template customization* is disqualified (`../dx-contract.md` §a, ADR-SDK-001).

Market facts at decision time (verified 2026-07-14, unlikely to be in anyone's training data):
**Stainless exited the market** (acquired by Anthropic 2026-05-18; hosted generator closed to
new customers). **Fern was acquired by Postman** (2026-01-08) and ships default-on retry
machinery that is not excludable from any generated core. **Speakeasy** remains viable at
≈$43–52k/yr with an Elastic-2.0, license-key-gated CLI.

## Decision

**Adopt OpenAPI Generator v7.23.0 for all six language cores, digest-pinned. No Kiota split for
.NET.**

- **Toolchain pin** — committed at
  [`../../pipeline/generator-pin.yaml`](../../pipeline/generator-pin.yaml): Docker image
  `openapitools/openapi-generator-cli:v7.23.0`, manifest digest
  `sha256:5ffccd3b0d4ac57eac443e1c9b3e2f2bb7f0a21ffe6c6701f3690d7edc78bf2d`. Generation is
  zero-egress and account-free — "checksum-pinned like any release tooling"
  (`../pipeline-and-release.md` §6).
- **Pinned per-language generation configs** (all mitigations are generator-flag or
  template-partial level — the spec artifact is never edited, ADR-SDK-006):

| Language | Generator / library | Required flags & overrides |
| --- | --- | --- |
| .NET | `csharp` / `generichost` (default; `httpclient` lib is officially Experimental) | `enumUnknownDefaultCase=true`, `packageGuid=<fixed>`, `hideGenerationTimestamp=true`; ignore-list: Polly `IHttpClientBuilderExtensions` + test scaffolding; banner partial |
| Java | `java` / `native` (JDK 11+ HttpClient + Jackson — leaner than default okhttp-gson) | `enumUnknownDefaultCase=true`, `hideGenerationTimestamp=true` (java default is **false**), `licenseName=Apache-2.0` (pom defaults to Unlicense); banner partial |
| PHP | `php` / `guzzle` (psr-18 lib still beta) | `enumUnknownDefaultCase=true` (setter-level; deserializer edge tracked in bake-off §A3); banner partial |
| TypeScript | `typescript-fetch` (zero runtime deps) | strict tsc verified; unknown enum values pass through at runtime (verbatim preserved); banner partial |
| Python | `python` (pydantic ≥2.11) | **one-partial override of the emitted enum `field_validator`** (no `enumUnknownDefaultCase` for python; stock validator throws on unknown wire values — unacceptable on success-path models); banner partial |
| Go | `go` (stdlib-only for our spec) | `enumUnknownDefaultCase=true` for named enums; inline property enums (incl. `ErrorResponse.code`) already emit as plain `*string`; banner partial |

- **Uniform safety rule** regardless of generator (restates `../runtime-tdd.md` §3): the runtime
  classifies failures from the raw response it already holds — **never from a core model enum**
  — so typed errors carry `code` verbatim even where a core enum collapses or nulls unknowns.

## Rationale

1. The only live candidate that clears **every hard gate simultaneously**: six STABLE client
   generators; zero-egress, digest-pinned generation (pipeline hermeticity); explicit user
   ownership of output (Apache-2.0-licensable, ADR-SDK-019); no repo/registry coupling
   (publish embargo, ADR-SDK-022); $0 license.
2. The idiomatic gap — openapi-generator's real historical weakness, and why ADR-SDK-001
   Option B (raw codegen *as the product*) was rejected — is closed by the architecture already
   decided: the hand-written runtime is the merchant-facing surface; the core is hidden behind
   it except re-exported models, which the hands-on runs show are plain idiomatic DTOs in all
   six languages. §a enforcement stays where the DX contract puts it: the per-language GA
   checklist signed by an experienced developer in that language.
3. Open-string safety on the actual artifact (`ErrorResponse.code` ships as a closed inline
   `enum:`) is achievable in every language via `enumUnknownDefaultCase` / runtime pass-through
   / the one python partial — see the table; the uniform safety rule removes the core enums from
   the failover-classification path entirely (ADR-SDK-007 open-string invariant).
4. The commercial field self-eliminated on our constraints: Stainless is not procurable; Fern's
   non-excludable default-on retries conflict directly with `../failover-contract.md` §5 (an
   auto-retried ambiguous `POST /payments` is the §1 double-charge hazard) and its hermetic
   local generation is Enterprise-gated with an org-verification phone-home; Speakeasy — the
   closest runner-up — costs ≈$43–52k/yr against a $0 alternative whose gap our architecture
   closes, leaves PHP without open-enum support on safety-relevant behavior, and its
   Elastic-licensed key-gated CLI reintroduces the vendor-continuity risk the pipeline design
   exists to avoid.

## Alternatives considered

- **Speakeasy (runner-up):** rejected on cost vs closed gap, PHP open-enum hole, ELv2 key-gated
  CLI (regeneration continuity risk if the contract or vendor ends), and a baked
  `speakeasy-sdk/…` User-Agent that fights ADR-SDK-005. Revisit only if a per-language §a
  checklist fails in a way template work cannot close.
- **Fern:** best enum-openness defaults of any candidate, but blocked by two hard gates as
  shipped: default-on, non-excludable retry machinery in every core (failover-contract §5), and
  Enterprise-gated phone-home local generation (pipeline §6 hermeticity).
- **Stainless:** not procurable — exited the market 2026-05 (Anthropic acquisition).
- **Kiota for .NET (split role):** no template system by design ("code readability is a
  non-goal") — fails the §a customization clause; TypeScript still Preview; and the split adds a
  second toolchain, Graph-style verb builders, and Microsoft-versioned abstractions in the
  re-exported surface for no advantage over the selected option. Rejected on uniformity.

## Consequences

- **OQ-1 is closed**; with the spec input already pinned (`../../spec/pin.yaml`,
  `spec/v2.1.2+9af661b`), pipeline stage 2 (generate ×6) has no remaining decision gates.
- Upstream cadence is ~8–9 minors/yr and every minor is flagged "breaking changes (with
  fallback)": the pin is exact version + image digest; **upgrades ride PRs where the stage-2
  regeneration diff makes the blast radius reviewable** — never a floating tag.
- The maintained template surface per language is deliberately minimal: the generated-code
  banner partial ×6 (ADR-SDK-016 rule) plus the required python enum `field_validator` partial.
  Every additional forked template is a standing liability — prefer flags; record any new
  partial in the language's generation config.
- §a watch-item, recorded honestly: C# generichost models expose an `Option<T>` set/unset
  pattern on non-required properties (defensible — distinguishes unset from null — but unusual).
  The .NET GA checklist reviewer decides (ADR-SDK-015 dogfooding); fallbacks exist (model
  template partial, or `restsharp` library at the cost of a Newtonsoft dependency).
- A generator *change* (version bump or vendor switch) is an ADR-SDK-023 revision — never a
  quiet pipeline edit (repo rule: [Decided] items reverse only by ADR revision).
