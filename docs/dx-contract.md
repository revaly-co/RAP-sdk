# RAP Integration SDK — Developer Experience Contract

**Source:** RFC-046 §6 (Approved 2026-07-10, v10). Added in review (2026-07-09/10) in response to
the "consumer-side contract is undesigned" finding — the runtime is the product, so its
merchant-facing surface is a **designed artifact**. This document fixes principles and
commitments; the per-language API reference lives in `runtime-tdd.md` and the code.

## (a) Idiomatic bar

**Commitment:** each SDK reads as native to its ecosystem — naming, error idiom (exceptions vs
result types vs `err` returns), async model, package layout — with the ecosystem's standard
linters enforced in CI.

**Acceptance:** a per-language GA checklist signed off by an **experienced developer in that
language** before that language ships GA (in GA order, ADR-SDK-015). This same bar is the
acceptance criterion for the OQ-1 generator bake-off: a generator that cannot meet it with
template customization is **disqualified**.

## (b) Developer journey

**Commitment:** from sandbox API key in hand to **first successful sandbox charge in ≤ 15
minutes**, using only the quickstart.

**Acceptance:** each language ships a copy-paste quickstart covering install → init → charge →
**handling all three error classes**; the failover + reconcile worked example is **part of the
quickstart, not an appendix** (it is the safety-critical path merchants copy). Test keys are
Enablement-issued in V1 (ADR-SDK-014) — the 15-minute clock starts at key-in-hand.

## (c) Debuggability

**Commitment:** pluggable logging via each ecosystem's native abstraction; **default output is
values-free**; debug level scrubs PAN/CVV/PII (ADR-SDK-020). Every response and every typed error
carries the **request correlation id**, so a merchant support ticket joins directly to RAP-core
telemetry. A **wire-trace hook** (request/response observer with scrubbed payloads) supports
Enablement escalations.

**Acceptance:** CI log-capture tests per language assert no payload values at default level and
full scrubbing at debug level; correlation id presence asserted on every error path.

## (d) Merchant-side testability

**Commitment:** every language ships a **first-class mock transport** simulating the full
taxonomy — PermanentRejection, TransientFailure (**including 503 + `not_processed`**),
OutcomeUnknown, and both reconcile outcomes — so a merchant can unit-test their failover handler
**with no network**. Testing the failover handler is a documented first-class scenario; sandbox
BIN-routing test cards cover E2E. Mock mode uses **only synthetic data**.

**Acceptance:** the mock ships in the same package (or companion test package per ecosystem norm),
is used by our own quickstart tests, and covers every row of the failover-contract §2 table plus
(post-P-2) pending-state scenarios.

## (e) Upgrade & support policy

**Commitment, per package:**
- **current + previous minor** supported;
- deprecations announced in release notes **and registry deprecation metadata**;
- a **published migration guide per major**;
- a yanked release is announced **together with its patched replacement in the same notice**;
- security patches go to the **latest GA of every supported major**;
- `X-Api-Version: 2.0` pinning support follows the platform's API deprecation policy.

**Acceptance:** SECURITY.md + support table in each package readme; the §5 bad-release runbook
(`pipeline-and-release.md`) implements the announcement mechanics.

## (f) Consumer voice

**Commitment:** Wave-1 GA is preceded by a **design-partner beta** (2–3 merchants from the
Enablement pipeline). DX KPIs are measured alongside the adoption KPI:

| KPI | Measurement |
| --- | --- |
| Time-to-first-sandbox-charge | Server-measurable: key issuance → first sandbox 2xx |
| SDK-attributed Enablement ticket rate | Ticket tagging by Enablement |
| GitHub issue first-response SLA | Issue tracker metrics; SC triage rotation owns response (ADR-SDK-012) |

**.NET dogfooding (ADR-SDK-015) validates our ergonomics, not merchants' — it does not substitute
for the beta.**

## Traceability

The six commitments map (a)–(f) one-to-one to the 2026-07-09 review finding's asks; the mapping
was confirmed point-by-point in the review thread on 2026-07-10. Changes to any commitment require
an RFC revision (per the RFC's change-control note), not a quiet doc edit.
