# ADR-SDK-005 — Adoption Telemetry via `User-Agent`

**Status:** Accepted — decided 2026-07-06 (D-5); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §5.7 / §8, decision D-5 · answers PRD-057 Open Question 2
**Owner:** SC Eng + Product

## Context

Product's adoption KPI is "full traffic through RAP" — which requires distinguishing SDK-originated
requests from bespoke merchant integrations in platform telemetry. PRD-057 Open Question 2 asks how
adoption will be measured. The SDK has **no phone-home** in V1 (RFC-046 §8): all observability is
server-side.

## Problem

Identify SDK traffic (per language, per version) with zero merchant configuration, no new API
surface, and no trust implications.

## Decision

Every request sends:

```
User-Agent: revaly-sdk-<language>/<semver> (<runtime-version>; <os>)
```

Examples: `revaly-sdk-dotnet/1.2.0 (.NET 10.0.3; linux)`, `revaly-sdk-python/1.0.1 (CPython 3.13.2; darwin)`.

- Platform telemetry segments SDK vs custom traffic on this header — this is how Product measures
  the adoption KPI, so the identifier ships in the **first GA wave**, not later (platform-side
  capture: platform repo ADR 018).
- The identifier is **telemetry only** — never an auth or trust signal, never used server-side for
  authorization or behavioural branching (trust boundary, ADR-SDK-004).

## Rationale

Chosen over a custom header because `User-Agent` is:

- **zero-config** — merchants do nothing, adoption measurement starts on first request;
- **proxy-safe** — survives standard intermediaries without allowlisting;
- **already captured** by standard HTTP logging on the platform, so no request-schema change, no
  new retention, no data-store work (RFC-046 §4).

## Alternatives considered

- **Custom header (e.g., `X-Revaly-Sdk`):** rejected — needs allowlisting through edge layers, is
  easier to strip, and adds a header contract for zero gain over UA.
- **SDK phone-home metrics:** rejected for V1 — new data flows from merchant infrastructure carry
  privacy/PCI review weight the KPI doesn't need; explicitly "no SDK phone-home in V1".
- **Registry download counts:** rejected as KPI source — measures downloads, not traffic.

## Consequences

- Dashboards keyed on the UA dimension (platform-side): SDK traffic share vs custom integrations;
  error rate by SDK language/version; 503 + timeout rates (= failover triggers fired);
  OutcomeUnknown-class rate (spike ⇒ edge/platform problem, not merchant bugs).
- The `<semver>` token makes version-specific regressions visible server-side — a bad SDK release
  is detectable without merchant reports (§8 on-call story).
- The UA string must never contain merchant-identifying or host-identifying detail beyond the
  coarse tokens below.

## Implementation guidance

- Token grammar (normative):
  - `<language>` ∈ `python | typescript | go | dotnet | php | java` (fixed lowercase tokens);
  - `<semver>` — the package's exact version, no `v` prefix;
  - `<runtime-version>` — coarse runtime identifier (e.g., `.NET 10.0.3`, `CPython 3.13.2`,
    `go1.24`, `PHP 8.4`, `OpenJDK 21`, `node 22.11`);
  - `<os>` — coarse platform token only (`linux` / `windows` / `darwin` / other); **no hostnames,
    no distro fingerprints, no architecture unless ecosystem-standard**.
- Follow HTTP UA convention: merchant frameworks may *append* their own product token after the
  SDK's; the SDK prefix must stay first and intact so platform segmentation keeps working. The SDK
  must not offer a way to replace or suppress its own token.
- Set the header at the transport layer of the runtime so the generated core cannot bypass it.
- Unit-test the exact string per language (it is a contract with platform dashboards); the mock
  transport asserts its presence.
