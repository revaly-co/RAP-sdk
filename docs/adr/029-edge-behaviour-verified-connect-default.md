# ADR-SDK-029 — AFD/WAF edge behaviour verified; connect-timeout default ratified (OQ-11)

**Status:** Accepted (2026-07-21) · closes OQ-11 (`docs/open-items.md`) · amends ADR-SDK-027
Decision 3 (the connect-default residual assigned there)
**Drives:** `failover-contract.md` §2/§6 verification state · `runtime-tdd.md` §1 config
defaults · all six runtimes · unblocks the OQ-11 leg of the ADR-SDK-024 GA sandbox retarget

## Context

OQ-11 ("verify AFD/WAF edge behaviour — 502/504, resets — and confirm the taxonomy
classification against reality") was a **hard pre-GA gate**: until verified, the edge rows of
the `failover-contract.md` §2 table (502/504 → OutcomeUnknown, reset mid-flight →
OutcomeUnknown) were design assumptions, and no connect-timeout default existed in any runtime
(ADR-SDK-027 Decision 3 deliberately left it here — server-side telemetry cannot observe the
client→edge connect phase). ADR-SDK-028 §4 added the binding constraint: any ratified connect
default must stay **below** the 75 s overall deadline, or the phase-blind overall deadline
fires first during connect and classifies OutcomeUnknown where a connect bound would have
proven TransientFailure.

Verification ran 2026-07-21 against the live production edge: configuration inspection of
the Front Door profile, a 30-day telemetry census of the edge access and WAF logs,
origin-side correlation, and live client probes. Resource names and the query recipes are
held in the internal OQ-11 evidence record, not in this public document.

## Evidence

**Topology (live config, 2026-07-21).** `api.revaly.co` is a custom domain (min TLS 1.2) on
an AFD Premium profile → an HTTPS-only route on `/*` (HTTP→HTTPS redirect enabled) → a
health-probed origin group → the platform origin. The edge's origin-response timeout is
**120 s**. A WAF policy is associated on `/*` (managed rule sets plus a small set of custom
rules); of the custom rules, only a request-body rule has a match that can reach the payment
paths. Block responses use the AFD default (403), and the managed missing-header rules that
plain API clients trip were already tuned to log-only.

**30-day edge census** (edge access log, 2026-06-21 → 2026-07-21, host `api.revaly.co`):

- **5xx from the edge: exactly one row.** A `504` / `OriginTimeout` on a synthetic
  availability-test request — `timeTaken` **≈4 s** with TTFB = total: AFD's fixed (~4–5 s)
  origin-**connect** bound fired, not the 120 s response timeout. Origin-side request logs
  show the platform serving steady 200s through that entire minute — the request **never
  reached the application**. Reality was "not processed", the client cannot prove it, and
  OutcomeUnknown is exactly the conservative classification the contract mandates.
- **Zero 502s. Zero AFD-generated 503s** (health-probe failures for the origin were
  scattered isolated samples across the window — never enough consecutive failures to cross
  the unhealthy threshold at any POP).
- **Origin responses pass through unmodified.** Origin-generated 400/401/404/405/409 bodies
  (tens of thousands of rows) streamed through AFD to clients; AFD substitutes a body only
  for errors it generates itself. A platform `503 {code: "not_processed"}` therefore
  survives the edge intact — the P-1 fast-failover signal is not rewritten. (Zero such 503s
  occurred in the window; the pass-through mechanism is status-agnostic response streaming.)
- A handful of 499s (`ClientDisconnected` — client-side aborts, which is what an SDK
  deadline firing mid-request looks like from the edge) and a steady stream of 307s
  (plain-HTTP redirects — see probes). No `revaly-sdk/*` User-Agent traversed the edge in
  the window (pre-GA, as expected; the evidence base is fleet client traffic).

**WAF census** (same window): every Block was scanner/hostile traffic — sensitive-path
probes, anomaly-threshold detections, bad bots, and a handful of body-rule and geo matches;
block totals reconcile with the access log's edge 403s. **The bot-management rules where
server-side SDK clients from datacenter IPs land only ever Log, never Block**: no bot
false-positive risk for merchant SDK traffic under the current policy. Missing-header rules
logged heavily without blocking (pre-tuned, above).

**Live probes (2026-07-21, client-side).** Five timed requests: TCP connect 29–98 ms,
TLS-complete 85–415 ms (cold worst-case), TTFB 215–558 ms — the probe path passed the WAF
and returned the origin's 404 through the edge. A `/.git` probe returned the real WAF block
shape: `403`, `Content-Type: text/html`, a 1,484-byte XHTML page with `x-azure-ref` and
`Connection: close` — **not** an `ErrorResponse`. A plain-HTTP request returned `307` +
`Location: https://…` from the edge itself.

## Decision

1. **The §2 edge rows are ratified unchanged.** 502/504 → OutcomeUnknown, reset mid-flight →
   OutcomeUnknown, and the plain-4xx rule (403 → PermanentRejection) all held against every
   observed edge behaviour. Two nuances are now documented facts rather than assumptions:
   - **A 504 does not imply the deadline elapsed.** AFD's origin-connect bound can produce a
     504 in ~4 s. Classification stays status-only.
   - **Edge-generated errors whose reality is "never dispatched" (AFD connect-fail 504,
     pool-unhealthy 503, WAF 403) still classify conservatively** (OutcomeUnknown for the
     5xx; PermanentRejection for the WAF 403). The client cannot distinguish them from
     post-dispatch failures by status, and edge bodies are HTML — the open-string `code`
     fallthrough (absent → OutcomeUnknown) is load-bearing and verified. Only the platform's
     own `503 {code: "not_processed"}` licenses fast failover, and it passes through the edge
     unmodified. The edge cannot mint that signal; nothing else may either.
2. **Default `connectTimeout` = 10 seconds** in every runtime that can enforce it
   (.NET, Java, PHP, Python, Go); TypeScript absorbs it at documentation level per
   ADR-SDK-028 §4 (the README dispatcher recipe carries the number; undici's own default is
   already 10 s, which is also the precedent that fixes the value — all six languages teach
   the same number). Rationale: ≈25× the observed cold client→edge TLS envelope (0.415 s),
   wide enough for lossy-link SYN-retransmit ladders and high-latency handshakes, and 65 s
   below the 75 s overall deadline — the ADR-SDK-028 §4 constraint holds with margin. The
   edge is anycast: merchants connect to a nearby POP, not to the origin region, so the
   envelope generalises. A bounded connect phase converts the ecosystems' infinite connect defaults
   into a fast, usually **provable** failover signal.

   | Language | Unset → 10 s | Explicit opt-out | Expiry classifies as |
   | --- | --- | --- | --- |
   | .NET | `ConnectTimeout = null` | `ConnectTimeout = Timeout.InfiniteTimeSpan` | TransientFailure (connect-phase provable) |
   | Java | builder omits `connectTimeout(...)` | `noConnectTimeout()` (or explicit `connectTimeout(null)`) | TransientFailure (`HttpConnectTimeoutException`) |
   | PHP | parameter omitted (default `RapClient::DEFAULT_CONNECT_TIMEOUT_SECONDS`) | `connectTimeout: null` | **OutcomeUnknown** (curl errno-28 is phase-blind — documented divergence, ADR-SDK-028 precedent; refusal errno-7 stays TransientFailure) |
   | TypeScript | documentation-level (undici default 10 s) | dispatcher recipe | TransientFailure (`UND_ERR_CONNECT_TIMEOUT`) |
   | Python | parameter omitted (default `DEFAULT_CONNECT_TIMEOUT`) | `connect_timeout=None` at construction | TransientFailure (`ConnectTimeoutError`) |
   | Go | `ConnectTimeout: 0` (zero value) | `ConnectTimeout: revaly.NoConnectTimeout` | TransientFailure (dial `OpError` provable) |

   Zero/negative values remain invalid everywhere except the documented sentinels. Per-stack
   provability is unchanged: where the stack proves the connect phase, expiry is
   TransientFailure; where it cannot (PHP errno-28), OutcomeUnknown — never guessed toward
   "safe".
3. **The timeout ordering is ratified: SDK 75 s < platform ≈100 s < AFD 120 s.** The
   platform, not the edge, owns the timeout narrative on the payment path; AFD's response
   timeout never fires first. **Ops guardrail:** lowering the edge's origin-response timeout
   below ~100 s (or switching its bot-management rules to Block, or adding WAF custom rules
   whose match reaches the payment paths) changes merchant-visible SDK behaviour and must be
   flagged to the SDK owners before rollout.
4. **No OQ-11 residuals remain.** The ADR-SDK-024 GA sandbox retarget now waits only on its
   ADR-SDK-014 parity leg.

## Consequences

- Behaviour change for configs that never set a connect timeout: a dead/black-holed edge
  path now fails in 10 s (TransientFailure where provable → immediate failover) instead of
  riding infinite ecosystem defaults toward the 75 s overall deadline (OutcomeUnknown →
  reconcile). Strictly better failover latency; no working configuration is affected
  (observed connect envelope is sub-second).
- Ships as a **minor** release ×6 (v0.4.0) per ADR-SDK-027 Decision 3's amendment clause.
- Every "awaits OQ-11" marker (code docs, READMEs, `runtime-tdd.md` §1) is replaced by the
  ratified default + opt-out wording referencing this ADR; `failover-contract.md` §6 flips
  the edge rows from "design assumptions" to "verified (this ADR)".
- CI gains per-language tests: default applied when unset, opt-out honoured, invalid values
  still rejected.
- The quickstart guidance is unchanged: base URLs are HTTPS-only (the edge 307s plain HTTP,
  and a redirect-following client would re-POST — the hazard stays documented), and merchant
  handlers keep the mandatory default branch for unrecognized codes/verdicts.
