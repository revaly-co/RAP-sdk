# ADR-SDK-027 — Overall-deadline default ratified from production telemetry (OQ-6)

**Status:** Accepted (2026-07-20) · closes OQ-6 (`docs/open-items.md`)
**Drives:** `runtime-tdd.md` §1 config defaults · SC-278 R3 · all six runtimes

## Context

OQ-6 ("default connect/total deadlines — derive from RAP-core latency telemetry, don't
invent") was the last R3 clause open in SC-278. All six runtimes shipped v0.1.0 accepting
optional connect/overall deadlines and applying them per request, with **no SDK-invented
default** and an explicit OQ-6 marker at every site — an unset overall deadline rode each
ecosystem's own behaviour (.NET `HttpClient` 100 s, `java.net.http` indefinite, Guzzle
none, fetch/undici none, urllib3 none, Go none).

Production telemetry now exists, from two independent sources (pulled 2026-07-20; full
evidence — including workspace names and reproducible queries — in the internal OQ-6
record on SC-278):

- **RAP path** (platform production telemetry, 5 days): per-gateway charge percentiles —
  one high-volume gateway class at P50 1.32 s / P95 3.08 s / P99 4.29 s,
  max 26.5 s with a 32-event 20–26.5 s stall cluster.
- **Gateway fleet** (14 days, unsampled): platform charge envelope P50 1.60 s /
  P95 3.31 s / P99 4.67 s; per-gateway P95 spread ~6× across the routed gateways; the
  slowest shows a 20–40 s stall band; the platform's own ceiling is ≈100 s (tail clusters
  at 100,000 ms — the .NET default `HttpClient.Timeout`).
- **Clip ladder** for a client-side overall deadline (each clipped charge classifies
  OutcomeUnknown → reconcile): 5 s → 0.73 % · 10 s → 0.037 % · 15 s → 0.021 % ·
  **30 s → 0.011 % (~1 in 9,500)** · 60 s → 0.007 %.

Structural facts that shape the decision:

1. RAP routes to the gateway **server-side** — the SDK cannot know the gateway type
   pre-request, so a default must cover the slowest common class; per-gateway tightening
   can only ever be a merchant override.
2. SDK-observed latency = server-side numbers + RAP-core overhead (~0.4–0.7 s
   backbone-side) + client→edge network delta.
3. The dataset is **server-side**: it cannot observe the client→AFD/WAF connect phase,
   so no connect-timeout default is derivable from it (that is OQ-11's territory).

## Decision

1. **Default `overallDeadline` = 75 seconds**, applied by every runtime when the merchant
   does not set one. The telemetry floor is 30 s (clips ~1 in 9,500 charges and clears
   the 20–26.5 s stall band); the OQ-6 owner ratified **75 s as a deliberate safety
   margin above that floor**: it clears every observed non-ceiling gateway tail in the
   14-day fleet data (worst non-ceiling tail: 64 s — only genuine hangs and the ceiling
   cluster sit beyond it), clips ≲0.007 % of charges (the >60 s bound; empirically ~5 per
   million exceeded 90 s), and still sits 25 s under the platform's ≈100 s ceiling — so
   expiry is classified deterministically by the SDK (OutcomeUnknown → reconcile,
   `failover-contract.md` §2) instead of racing whatever the ecosystem's transport
   default happens to be. The default optimises for not clipping real charges (fewer
   OutcomeUnknown reconciles); checkout responsiveness is the merchant's knob — tighten
   per budget, uniform across operations (reads finish far below it).
2. **Unset vs disabled, per language** (explicit opt-out restores the pre-027 unset
   behaviour — the transport's own defaults):

   | Language | Unset → 75 s | Explicit opt-out |
   | --- | --- | --- |
   | .NET | `OverallDeadline = null` | `OverallDeadline = Timeout.InfiniteTimeSpan` |
   | Java | builder omits `overallDeadline(...)` | `noOverallDeadline()` (or explicit `overallDeadline(null)`) |
   | PHP | parameter omitted (default `RapClient::DEFAULT_OVERALL_DEADLINE_SECONDS`) | `overallDeadline: null` |
   | TypeScript | `overallDeadlineMs` omitted | `overallDeadlineMs: null` |
   | Python | parameter omitted (default `DEFAULT_OVERALL_DEADLINE`) | `overall_deadline=None` |
   | Go | `OverallDeadline: 0` (zero value) | `OverallDeadline: revaly.NoOverallDeadline` |

   Zero/negative values remain invalid everywhere (except the documented sentinels).
3. **No connect-timeout default is ratified.** Server-side telemetry cannot see the
   client connect phase; inventing a number would violate the OQ-6 rule itself. The
   transport's own connect defaults continue to apply, documented per language. OQ-11
   (already a hard pre-GA gate) supplies the client/edge data; when it closes, a connect
   default ships as a config-default change in a **minor** release under an amendment to
   this ADR. *(Amended 2026-07-21: OQ-11 closed — **ADR-SDK-029** ratifies the 10 s connect
   default from the edge verification evidence; ships in v0.4.0 ×6.)*
4. **Reconcile-policy defaults are not ratified here** (the other OQ-6 feed,
   `runtime-tdd.md` §4). They need post-charge *visibility-lag* telemetry — when a
   charged transaction becomes observable via `GET /transactions/merchant/{id}` — which
   is a different measurement than charge latency. The reconcile helper keeps requiring
   an explicit policy; this residual moves to the SC-261 follow-up line and rides the
   P-2 `SafeToFailover` work.

## Consequences

- Behaviour change for configs that never set a deadline: requests that previously hung
  toward the ecosystem default (up to ~100 s or indefinite) now classify OutcomeUnknown
  at 75 s with the reconcile path — ≲0.007 % of charges at current production tails
  (empirically ~5 per million beyond 90 s).
  Ships in the next minor release (v0.2.0); pre-1.0 and the Go module path is not yet
  activated, so no published consumer sees a break.
- Every "OQ-6 lands before GA, deliberately not invented" marker (code docs, READMEs,
  `runtime-tdd.md` §1, `docs/README.md` language sections) is replaced by the ratified
  default + opt-out wording referencing this ADR.
- OQ-6 closes in `open-items.md`. Residuals move to their proper owners: connect default
  → OQ-11; reconcile-policy defaults → SC-261 follow-up. The platform ADR-018 §8
  dashboard/alert follow-up ("gated on OQ-6") is unblocked.
- CI gains per-language tests: default applied when unset, opt-out honoured, invalid
  values still rejected.
