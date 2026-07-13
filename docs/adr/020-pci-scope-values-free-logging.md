# ADR-SDK-020 — PCI Scope: Merchant-Side; SDK Obligation Is Values-Free Logging

**Status:** Accepted — decided 2026-07-10 (OQ-13, Charles): the RFC approval explicitly covers the scope determination and the logging obligation; QSA/policy link is a tracked follow-up
**Source:** RFC-046 §9 / §11 OQ-13 / §12 approval notes · inline review thread (PCI authority, 2026-07-08)
**Owner:** Leadership + Compliance (authority); SC Eng (obligations)

## Context

The SDK assembles payment payloads: **PAN/CVV pass through it in memory, merchant-side.** Review
flagged that "merchant's PCI scope" is a compliance determination stated as fact and required a
named authority: either a linked compliance policy / QSA assessment, or the leadership approval
explicitly covering the determination.

## Problem

Establish, with an accountable authority, where PCI DSS scope sits for six public packages that
handle cardholder data inside merchant payment systems — and what obligations the SDK carries
regardless.

## Decision

1. **Scope determination:** the SDK executes inside merchant infrastructure; PAN/CVV handled in
   memory there is the **merchant's PCI scope**. RAP-core's scope is unchanged by the SDK's
   existence (the API contract is unchanged).
2. **Authority:** per the §12 approval note, the 2026-07-10 approval (Charles) **explicitly covers
   this scope determination together with the values-free logging obligation**. Linking the QSA
   assessment / compliance policy when available remains a tracked follow-up
   (`../open-items.md`).
3. **SDK obligations (binding, all languages):**
   - **default logging is values-free** — no payload values at default verbosity, ever;
   - debug-level logging **scrubs PAN/CVV/PII**;
   - **mock mode uses only synthetic data** (never recorded live payloads);
   - merchant API keys are redacted from all logs and exception messages (trust boundary,
     ADR-SDK-004).

## Rationale

- The trust boundary already places execution, credentials, and routing merchant-side; scope
  follows execution. What the SDK *can* control — and therefore must — is that it never becomes an
  accidental cardholder-data sink via logs, traces, or test fixtures.
- An explicit approver statement was the review's named alternative to a policy link; it makes the
  determination owned rather than assumed.

## Alternatives considered

- **Block approval on the QSA/policy link:** rejected by the approver — the explicit approval
  statement covers it; the link remains a follow-up so the paper trail completes.
- **Treat the SDK as in-scope vendor software (PA-DSS-style validation):** not applicable to a
  merchant-embedded open-source library; obligations are carried as engineering controls instead.

## Consequences

- The values-free default is a **DX-contract commitment** (§c) and a GA checklist item per
  language — verified, not assumed: tests assert that default-level logs of full request/response
  cycles contain no payload values.
- The wire-trace hook (DX contract §c) emits **scrubbed** payloads only; scrubbing lives in the
  runtime, not in the hook consumer.
- Issue templates (ADR-SDK-012) instruct merchants never to attach PAN/CVV/keys; values-free logs
  make compliant bug reports the default output.
- If the QSA assessment, once linked, narrows or adjusts the determination, this ADR is amended —
  the obligations above are a floor either way.

## Implementation guidance

- Centralize scrubbing per language runtime (single scrub function applied to logs, exceptions,
  wire traces, and mock recordings); test it against the full payload schema, not a field list
  that can drift.
- Scrub by **allowlist** (emit only known-safe fields) rather than denylist where feasible —
  schema evolution then fails safe.
- CI includes a log-capture test per language: run a charge + failure + reconcile against the mock
  transport at default and debug levels; assert no PAN/CVV/key material in output.
