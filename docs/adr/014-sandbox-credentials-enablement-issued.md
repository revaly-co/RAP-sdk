# ADR-SDK-014 — Sandbox Test Credentials Are Enablement-Issued in V1; Self-Serve Deferred

**Status:** Accepted — decided 2026-07-10 (OQ-4); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §7 / §11 OQ-4
**Owner:** Eng + Enablement

## Context

The Sandbox environment serves two consumers: the SDK pipeline's **contract-smoke gate** (stage 4 —
live smoke of all six SDKs against Sandbox on every release) and **merchant onboarding** (the DX
contract's ≤15-minute quickstart journey starts from "sandbox API key in hand"). Both need test API
keys; the open question was whether merchants get them self-serve or through Enablement.

## Problem

Fix the V1 credential path so CI can be built and the quickstart can be honestly worded — without
blocking on a self-serve provisioning product that doesn't exist.

## Decision

- **V1 test keys are Enablement-issued.** Self-serve issuance is **deferred** (not rejected — a
  candidate post-GA improvement).
- **Environment parity confirmation remains a pre-GA task**: Sandbox must behave like production
  for everything the taxonomy and quickstart exercise (error classes, `ErrorResponse.code`
  emission once P-1 ships, BIN-routing test cards for E2E).
- CI's test key is a pipeline secret (Key Vault), provisioned once via Enablement like any
  merchant key.

## Rationale

- Enablement issuance reuses the existing merchant-onboarding relationship — zero new product
  surface for V1, and the design-partner beta (DX contract §f) is Enablement-mediated anyway.
- The quickstart's ≤15-minute commitment is measured **from key in hand**; issuance latency is an
  Enablement SLA, not SDK time — the wording stays honest under this decision.

## Alternatives considered

- **Self-serve portal issuance for V1:** rejected for scope — a provisioning product gating an SDK
  release; revisit post-GA when volume justifies it.
- **Shared/public demo key:** rejected — uncontrolled load on Sandbox, no per-merchant telemetry,
  and an anti-pattern for payment credentials even in test.

## Consequences

- The time-to-first-sandbox-charge DX KPI (server-measurable: key issuance → first sandbox 2xx)
  starts its clock at issuance — measurement design already accounts for this decision.
- Design-partner beta onboarding includes key issuance in its runbook.
- If Enablement issuance latency turns out to dominate the merchant journey, that is the data that
  reopens self-serve — the KPI captures it.

## Implementation guidance

- Pipeline: store the CI sandbox key in Key Vault; inject via the environment-scoped publish/test
  jobs only; never echo in logs (values-free logging applies to CI too).
- Quickstarts: first line states how to get a key ("contact Enablement / your onboarding contact")
  with the ≤15-minute journey starting after that.
- Environment parity checklist (pre-GA, with OQ-11's edge verification): error taxonomy rows
  reproducible in Sandbox, P-1 `code` emission, test card BIN-routing coverage.
