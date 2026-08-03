# RAP Integration SDK — Runtime Technical Design (TDD)

**Source:** RFC-046 (Approved 2026-07-10) · ADR-SDK-001/002/003/004/005/007/009 · DX contract
(`dx-contract.md`)
**Scope:** the hand-written runtime layer, per language. The generated core is out of scope here
(it is spec-derived; see `pipeline-and-release.md`).
**Legend:** items marked **[Decided]** are fixed by RFC/ADR; items marked **[Proposed]** are
TDD-level design to finalize in Epic SC-234 build stories without re-opening decided ground.

## 1. Client construction & configuration

**[Decided]** Config surface (names idiomatic per language):

| Setting | Default | Notes |
| --- | --- | --- |
| `apiKey` | — required | Merchant-held; injected per request; never persisted/logged (ADR-SDK-020) |
| `baseUrl` | `https://api.revaly.co` | Sandbox and live share this URL — the environment is selected by the API key's scope, not the URL (ADR-SDK-024); override only for internal/pre-release targets |
| `apiVersion` | `"2.1"` | Pinned via `X-Api-Version` on every request; `"2.0"` selectable |
| `connectTimeout` | **10 s** (ADR-SDK-029) | Edge-verified 2026-07-21; per-language opt-out sentinel documented in the ADR (TypeScript: documentation-level per ADR-SDK-028 §4). Expiry classifies TransientFailure where the stack proves the connect phase; PHP errno-28 stays OutcomeUnknown |
| `overallDeadline` | **75 s** (ADR-SDK-027) | Telemetry-ratified 2026-07-20; per-language opt-out sentinel documented in the ADR. Expiry **after send** classifies as OutcomeUnknown, never TransientFailure |
| `logger` | ecosystem-native | Values-free by default (§6) |
| `wireTraceHook` | off | Scrubbed request/response observer (§6) |
| `transport` | real HTTP | Replaceable by the mock transport (§8) |

**[Decided]** Version-pin behaviour: on `"2.0"`, the `ErrorResponse.code` field is not part of the
documented contract — the fast-failover class narrows to client-provable never-sent failures only.
This behavioural difference is documented prominently wherever `apiVersion` is described.

**[Proposed]** One client object per configuration; thread-safe/shareable per language norms;
no global singletons.

## 2. API surface

**[Decided]** Full V2 surface via the generated core, re-exported through the runtime namespace:
payments (charge, authorize, capture, void, refund, refund-cancel), payment methods, transactions,
notify. Merchants import **one package** per language.

**[Decided]** `merchantTransactionId` is required on every payment request (max length 100 —
platform-aligned end to end after the platform's id-length correction).

## 3. Typed errors

**[Decided]** Three classes + classification algorithm per `failover-contract.md` §2. Every typed
error carries: class, HTTP status (if any), `code` (verbatim, if any), human message (`error`),
opaque `details`, **correlation id**, raw response reference.

**[Decided]** Error idiom per ecosystem (DX contract §a):

| Language | Idiom **[Proposed mapping]** |
| --- | --- |
| .NET | Exception hierarchy: `RapCoreException` → `PermanentRejectionException` / `TransientFailureException` / `OutcomeUnknownException` |
| Java | Same shape, checked-vs-unchecked decided at bake-off with idiomatic reviewer |
| TypeScript | Typed error classes + discriminated-union result option |
| Python | Exception hierarchy |
| PHP | Exception hierarchy |
| Go | Sentinel-wrapped typed errors: `errors.As(&PermanentRejection{})` etc. |

**[Decided]** Forward compatibility: `code` parsed as open string (OQ-2 adds values later);
unrecognized → treated as absent → OutcomeUnknown path.

## 4. Reconcile helper

**[Decided]** Shape: `reconcile(merchantTransactionId, policy) → Found(...) | NotFoundYet` in V1;
`SafeToFailover` added only with P-2, as a **minor** release (ADR-SDK-009).

**[Decided]** Verdict types are designed **open for extension**: every language's construct
requires a default/else branch (sealed base + documented default; non-exhaustive union; enum +
`Unknown` guidance per ecosystem). Quickstart examples always show the default branch.

**[Decided]** `NotFoundYet` carries attempts, elapsed, last correlation id, last HTTP status.
`Found` distinguishes terminal outcomes from (post-P-2) pending intent as distinct variants.
(Explanatory note, 2026-07-23: a null/absent last HTTP status with attempts > 0 means no
reconcile attempt ever received an HTTP response — the API-unreachable signal. Degraded reads
(5xx/timeout/transport failure on the GET) keep polling within the caller's budget in every
language — visibility is widest exactly when RAP-core is degraded; the merchant action on
NotFoundYet is unchanged either way: hold + escalate.)

**[Proposed]** `policy` = backoff schedule (default exponential + jitter), per-attempt deadline,
overall budget; policy defaults deliberately not shipped in V1 — they need post-charge
visibility-lag telemetry, not charge latency (ADR-SDK-027 residual → SC-261 follow-up);
cancellable per language idiom (CancellationToken / context / AbortSignal / …). The helper is
GET-only and side-effect-free — the only loop the runtime owns (ADR-SDK-004).

## 5. Transport concerns

**[Decided]**
- Auth: API key header on every request, injected at transport level.
- `User-Agent: revaly-sdk-<language>/<semver> (<runtime-version>; <os>)` — exact grammar in
  ADR-SDK-005; set at transport level so the core cannot bypass it; merchant tokens may append,
  never replace.
- No hidden retries anywhere; single-shot semantics except the explicit reconcile loop.
- "Provably never sent" detection uses the transport's own connect-vs-response phase semantics;
  where the stack can't distinguish, classify OutcomeUnknown.

## 6. Logging, scrubbing, debuggability (DX contract §c · ADR-SDK-020)

**[Decided]**
- Pluggable logging via each ecosystem's native abstraction (`ILogger`, SLF4J, `logging`, PSR-3,
  `slog`, console-compatible).
- **Default output is values-free** — no payload values at default verbosity, ever. Debug level
  scrubs PAN/CVV/PII. API keys redacted from logs **and exception messages**.
- Correlation id on every response and every typed error — merchant support tickets join RAP-core
  telemetry directly.
- Wire-trace hook: request/response observer receiving **scrubbed** payloads (scrubbing in the
  runtime, not the consumer), for Enablement escalations.

**[Proposed]** Scrub by allowlist (emit only known-safe fields); central scrub function per
runtime, tested against the full payload schema; CI log-capture test asserts no sensitive material
at default and debug levels (ADR-SDK-020 guidance).

## 7. Package identity **[Decided — ADR-SDK-030]**

Final names (decided 2026-07-29, ratified 2026-07-30; consistent with the RFC's tokens —
`revaly-sdk-*` UA product token, group id `co.revaly`):

| Registry | Package name |
| --- | --- |
| npm | **`@revaly/sdk`** (scoped; the `revaly` org owns the scope) |
| PyPI | `revaly-sdk` |
| NuGet | `Revaly.Sdk` (runtime) + `Revaly.Sdk.Core` (generated core) |
| Packagist | `revaly/sdk` |
| Maven Central | `co.revaly:revaly-sdk` |
| Go | `github.com/revaly-co/rap-sdk/languages/go` (subdir module; layout per ADR-SDK-028) |

Names do **not** embed the GitHub org (except Go's module path — ADR-SDK-022 governs its timing).
Committed metadata now carries the final name in **all six** languages — the npm rename to
`@revaly/sdk` shipped with the stage-6 prep on 2026-08-03 (ADR-SDK-030 §Consequences,
ADR-SDK-031). Quickstart install lines switch from the interim GitHub-release artifact to
registry installs at the flip (runbook in `registry-provisioning.md`).

## 8. Mock transport (DX contract §d)

**[Decided]** First-class test double in every language, no network:
- simulates the full taxonomy: PermanentRejection statuses, TransientFailure (incl. **503 +
  `not_processed`**), OutcomeUnknown (timeout-after-send, 500, 502/504, bare 503);
- simulates both reconcile outcomes; post-P-2: pending-then-terminal and pending-then-absent;
- supports scripting consecutive outcomes (merchants test their suppression/escalation logic);
- asserts `User-Agent` presence; **synthetic data only** (ADR-SDK-020).

**[Proposed]** Scenario builder API mirroring the taxonomy names, so merchant test code reads as
the contract: `mock.charge().returnsNotProcessed503()`, `mock.reconcile("id").pendingThen(...)`.

## 9. Quickstart obligations (DX contract §b)

Each language ships a copy-paste quickstart: install → init → charge → **handle all three error
classes** → reconcile worked example (all §3 verdict branches incl. default). Sandbox key → first
successful sandbox charge in **≤ 15 minutes** using only the quickstart. The failover + reconcile
example is part of the quickstart, not an appendix.

## 10. Out of scope for the runtime

Circuit breaking, suppression, routing, resubmission, `bypassPlatform`, phone-home telemetry,
persistent state of any kind (ADR-SDK-004/005; PRD non-goals).
