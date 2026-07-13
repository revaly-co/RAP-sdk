# ADR-SDK-004 — No Circuit Breaker in V1: the SDK Is Stateless and Deterministic

**Status:** Accepted — decided 2026-07-06 (D-4); ratified with RFC-046 approval 2026-07-10
**Source:** RFC-046 §5.1–5.2, decision D-4 · PRD-057 non-goals
**Owner:** SC Eng

## Context

The SDK executes **inside merchant infrastructure**. The trust boundary (RFC-046 §5.1) fixes the
division of responsibility:

- RAP-core's responsibility ends at the HTTP response.
- The SDK's responsibility ends at **classifying the failure and surfacing it as a typed error**
  (ADR-SDK-002).
- The routing decision — where the payment goes next, whether to suppress traffic to RAP-core for a
  while, when to resume — belongs to the merchant's system, **above** the SDK. Traffic splitting
  and A/B routing are explicit PRD non-goals.
- The SDK is an untrusted client from RAP-core's perspective; the `User-Agent` identifier
  (ADR-SDK-005) is telemetry, never an auth or trust signal.
- The merchant API key is merchant-held: supplied at init, attached per request, never persisted or
  logged by the SDK.
- The SDK never resubmits and never invokes `bypassPlatform`.

## Problem

When RAP-core degrades, should the SDK itself stop sending (open a circuit) and fail fast locally?
A client-side breaker is the conventional reflex — and six different ecosystems have six different
breaker idioms, state models, and surprise factors.

## Decision

**No circuit breaker in V1.** The SDK is stateless and deterministic: no cross-request shared
state, no background threads/timers, no adaptive behaviour. Suppression windows and routing policy
live merchant-side. The SDK's contribution to the "RAP-core is down" scenario is a *fast, provable
signal* — the platform's circuit-open case returns 503 + `code: not_processed` immediately
(ADR-SDK-007), which the SDK surfaces as TransientFailure (safe to fail over).

## Rationale

- **The platform already has the breaker.** RAP-core's own circuit breaker is the authoritative
  degradation detector; with P-1 its opening becomes visible and provable on the wire. A second,
  client-side breaker adds a state machine without adding information.
- **Statelessness keeps six runtimes honest.** Deterministic request → typed-result behaviour is
  testable with the mock transport (DX contract §d) and identical across languages; breaker state
  would diverge per ecosystem and per process model (serverless vs long-lived).
- **Routing is the merchant's decision.** A breaker inside the SDK silently makes a
  business-routing choice (stop using RAP-core) that PRD-057 explicitly leaves with the merchant.

## Alternatives considered

- **Per-instance client breaker:** rejected — hidden state; behaviour differs across worker models;
  surprises merchants running many short-lived processes (breaker never trips) or few long-lived
  ones (breaker trips globally for unrelated traffic).
- **Optional breaker module (off by default):** rejected for V1 — real design surface (six
  ecosystems) for a behaviour the merchant's own infrastructure (service mesh, gateway, feature
  flag) already covers; may be revisited post-GA as a documented merchant-side pattern, not as SDK
  internals.

## Consequences

- Fast-failover latency for the "RAP-core is down" case comes from the platform's breaker-open
  fast-fail (+ P-1 code), not from client-side suppression. Merchants who want suppression build it
  above the SDK; the docs show the pattern.
- Deadlines are the SDK's only latency control: connect and overall deadlines are configurable per
  client instance, with defaults derived from RAP-core latency telemetry (OQ-6 — set before Wave 1
  GA, not invented).
- The runtime owns exactly one loop — the explicit reconcile re-poll (ADR-SDK-003); everything else
  is single-shot. No hidden retries anywhere in the runtime.
- Serverless and multi-process merchant deployments get identical semantics to long-lived servers.

## Implementation guidance

- Client construction takes `connectTimeout` and `overallDeadline` (names per language idiom);
  document that the overall deadline is the OutcomeUnknown boundary — expiry after send classifies
  as OutcomeUnknown, never TransientFailure.
- Do not add jittered auto-retry on idempotent GETs in V1 either — keep the behaviour model "one
  call, one result" everywhere except the explicit reconcile helper.
- The mock transport must allow scripting consecutive outcomes so merchants can unit-test their own
  suppression logic above the SDK.
