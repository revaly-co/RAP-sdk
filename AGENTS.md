# AGENTS.md — the Revaly RAP SDK in one page

Machine-readable orientation for AI coding agents integrating or modifying this SDK. Humans are
welcome here too; the prose is just denser than [`README.md`](README.md).

**Read this whole file before writing integration code.** The classification rules in §3 are
normative and safety-critical: getting them wrong is how a cardholder gets charged twice.

---

## 1. What this repository is

Six server-side SDKs for the **RAP V2 API** (RAP-core, `https://api.revaly.co`) — .NET, Java,
PHP, TypeScript, Python, Go — generated from one gated OpenAPI artifact and wrapped in a
hand-written runtime that implements a merchant-facing **failover & reconciliation contract**.

| Fact | Value |
| --- | --- |
| Repository | `github.com/revaly-co/RAP-sdk` (public, Apache-2.0) |
| API base URL | `https://api.revaly.co` — sandbox and live share it; the API key's scope selects the environment |
| API version header | `X-Api-Version: 2.1` (SDK default pin; `2.0` selectable and narrower) |
| Auth | API key, injected at client construction, sent on every request |
| Scope | Server-side only. Browser and mobile clients call your backend, which calls RAP |
| Normative contract | [`docs/failover-contract.md`](docs/failover-contract.md) |
| Current line | v0.5.x, pre-1.0; published on all six registries |

## 2. Install and import, per language

| Language | Install | Import / namespace | Client |
| --- | --- | --- | --- |
| .NET | `dotnet add package Revaly.Sdk` | `Revaly.Sdk` | `new RapClient(new RapClientOptions { ApiKey = ... })` |
| Java | `co.revaly:revaly-sdk` (Maven Central) | `co.revaly.sdk` | `RapClient` via builder |
| PHP | `composer require revaly/sdk` | `Revaly\Sdk` | `new RapClient(...)` |
| TypeScript | `npm install @revaly/sdk` | `@revaly/sdk` | `new RapClient({ apiKey })` |
| Python | `pip install revaly-sdk` | `revaly_sdk` | `RapClient(api_key)` |
| Go | `go get github.com/revaly-co/rap-sdk/languages/go` | package `revaly` | `revaly.NewClient(...)` |

One package per language: the generated core is re-exported through the runtime's namespace, so
integration code imports the runtime only.

## 3. The classification algorithm (normative)

Every failed payment call resolves to exactly one of three outcome classes. Apply this algorithm
and nothing else — never classify from the human-readable `error` message, from latency, or from
how long you waited:

```
if transport error and request provably never sent          → TransientFailure
if HTTP status in {400, 401, 403, 404, 422}                 → PermanentRejection
if HTTP status == 503 and body.code == "not_processed"      → TransientFailure
if HTTP status >= 500                                        → OutcomeUnknown
if deadline exceeded after send / reset / ambiguous          → OutcomeUnknown
```

Supporting rules:

- `ErrorResponse.code` and `transactionType` are **open strings**, never closed enums. A `code`
  the SDK does not recognize is handled as absent, which resolves to `OutcomeUnknown`.
- `details` is opaque. Do not parse it for control flow.
- When a language's HTTP stack cannot prove the request was never sent, the outcome is
  `OutcomeUnknown`. The safe-to-fail-over class is reserved for provable non-dispatch.
- Only RAP-core's own `503 {code: "not_processed"}` licenses immediate failover. Edge (Front
  Door / WAF) error bodies are HTML rather than `ErrorResponse`, and the edge cannot mint that
  code; a `504` can fire in about 4 seconds and never implies your deadline elapsed.

### What each class means for calling code

| Class | Payment state at RAP-core | Correct next action |
| --- | --- | --- |
| `PermanentRejection` | Received and rejected | Fix the request or decline the payment. Retrying or failing over reproduces the same rejection. |
| `TransientFailure` | Definitively not processed | Route this payment to your own gateway immediately. |
| `OutcomeUnknown` | May have been processed | Reconcile (§4), then act on the verdict. |

### Class names per language

| Language | PermanentRejection | TransientFailure | OutcomeUnknown | Idiom |
| --- | --- | --- | --- | --- |
| .NET | `PermanentRejectionException` | `TransientFailureException` | `OutcomeUnknownException` | `RapCoreException` hierarchy |
| Java | `PermanentRejectionException` | `TransientFailureException` | `OutcomeUnknownException` | exception hierarchy |
| PHP | `PermanentRejectionException` | `TransientFailureException` | `OutcomeUnknownException` | exception hierarchy |
| TypeScript | `RapPermanentRejection` | `RapTransientFailure` | `RapOutcomeUnknown` | typed classes, plus `toRapResult()` discriminated union |
| Python | `RapPermanentRejection` | `RapTransientFailure` | `RapOutcomeUnknown` | exception hierarchy |
| Go | `*revaly.PermanentRejection` | `*revaly.TransientFailure` | `*revaly.OutcomeUnknown` | `errors.As` on typed error values |

Every typed error carries: class, HTTP status (when there was one), verbatim `code` (when
present), human message, opaque `details`, **correlation ID**, and a reference to the raw
response.

## 4. Reconcile — the `OutcomeUnknown` procedure

`merchantTransactionId` is **required on every payment request** (max length 100) and is the key
reconcile looks the payment up by. Generate it as unique and durable in your own system before
you send the charge; persist it before the call, not after.

```
reconcile(merchantTransactionId, policy) → Found(outcome) | NotFoundYet
```

Verdict handling:

| Verdict | Meaning | Action |
| --- | --- | --- |
| `Found(approved)` | The money moved | This payment is complete. Do not send it anywhere else. |
| `Found(declined / terminal-failed)` | Reached a terminal state at RAP-core | Your decision; your own gateway is safe to use. |
| `Found(pending)` *(post-P-2)* | Intent reserved, outcome not yet settled | Keep polling within your budget. |
| `NotFoundYet` | Not visible **yet** — absence is not provable in V1 | Hold and escalate per your risk policy. |
| anything else | Verdict types are open for extension | **Keep a default branch.** `SafeToFailover` arrives with platform P-2 as a minor release. |

**A `default` / `else` branch on the verdict switch is mandatory in every language.** Generated
integration code that omits it is incorrect even though it compiles today.

`NotFoundYet` carries attempts, elapsed time, last correlation ID, and last HTTP status. A null
last HTTP status with attempts > 0 means no attempt ever received an HTTP response — the
API-unreachable signal. Degraded reads (5xx or timeout on the GET) keep polling within the
caller's budget; the merchant action on `NotFoundYet` is the same either way.

`policy` bounds the loop: backoff schedule, per-attempt deadline, overall budget, cancellation in
the language's idiom (`CancellationToken` / `context.Context` / `AbortSignal` / …). V1 ships no
default policy — pass one explicitly. The helper is GET-only and side-effect-free.

Reconcile symbols: `rap.ReconcileAsync(...)` + `ReconcilePolicy` (.NET) · `client.reconcile(...)`
+ `ReconcilePolicy.builder()` + `RapReconcileVerdict.Found` / `.NotFoundYet` (Java) ·
`$client->reconcile(...)` + `Revaly\Sdk\Reconcile\{Found, NotFoundYet, ReconcilePolicy}` (PHP) ·
`client.reconcile(id, { maxAttempts, overallBudgetMs, initialDelayMs })` returning
`verdict.kind` (TypeScript) · `client.reconcile(...)` (Python) ·
`client.Reconcile(ctx, id, revaly.ReconcilePolicy{...})` (Go).

## 5. Configuration surface

| Setting | Default | Behaviour that matters |
| --- | --- | --- |
| `apiKey` | required | Merchant-held, injected per request, never persisted or logged |
| `baseUrl` | `https://api.revaly.co` | Override only for internal targets; the key's scope selects sandbox vs live |
| `apiVersion` | `"2.1"` | `"2.0"` drops `ErrorResponse.code` from the documented surface, narrowing fast failover to provable never-sent |
| `connectTimeout` | **10 s** (ADR-SDK-029) | Expiry classifies `TransientFailure` where the stack proves the connect phase. TypeScript has no per-request option (fetch cannot bound connect); Node's undici default is already 10 s. PHP errno 28 stays `OutcomeUnknown` |
| `overallDeadline` | **75 s** (ADR-SDK-027) | Expiry **after send** classifies `OutcomeUnknown`, never `TransientFailure` |
| `logger` | ecosystem-native | Values-free at default verbosity |
| `wireTraceHook` | off | Receives already-scrubbed request/response payloads |
| `transport` | real HTTP | The mock-transport injection point |

## 6. Testing integration code offline

Every language ships a first-class mock transport that reproduces every row of the taxonomy plus
both reconcile verdicts, with **synthetic data only**. Scenario methods mirror the contract
vocabulary, so a test reads as the row it covers:

```ts
const mock = new RapMockTransport();
mock.charge().returnsNotProcessed503();                    // → TransientFailure
mock.reconcile('order-1042').notFoundYet(2).thenFoundApproved();
const client = new RapClient({ apiKey: 'sk-synthetic', transport: mock });
```

Namespaces: `Revaly.Sdk.Testing` (.NET) · `co.revaly.sdk.testing` (Java) · `Revaly\Sdk\Testing`
(PHP) · `@revaly/sdk` (TypeScript) · `revaly_sdk.testing` (Python) · `.../languages/go/raptest`
(Go). Method casing follows each language (`ReturnsNotProcessed503`,
`returns_not_processed_503`, …).

A complete failover handler test suite covers, at minimum: each of the three classes, `Found`
after `NotFoundYet`, sustained `NotFoundYet`, and the default verdict branch.

## 7. Rules for agents modifying this repository

These are enforced by CI and by [`CONTRIBUTING.md`](CONTRIBUTING.md); a PR that breaks one fails
rather than merges.

1. **`languages/*/core/` is generated. Never hand-edit it.** It changes only by regeneration
   against a newly pinned spec artifact. CI runs a regeneration-diff check and fails on a
   one-byte difference. The hand-written product code is `languages/*/runtime/` (Go:
   `revaly.go`, `internal/runtime/`, `raptest/`).
2. **Spec input is a pinned, gated artifact only** — a `spec/v*` release tag verified against its
   `.sha256` and `provenance.json`, pinned in `spec/`. Never generate from a branch, a URL, or a
   locally edited spec.
3. **Publishing runs through the pipeline.** The one human act is a per-language release tag on
   `main`. Never publish, re-publish, or yank out of band. A failed release is fixed and re-tagged,
   never resumed by re-running build stages.
4. **The safety-contract invariants in §3 and §4 are fixed by ADR.** Changing one requires an ADR
   revision, never a code choice. Reproducing them incorrectly in generated integration code is a
   correctness bug.
5. **Logging stays values-free.** No payload values at default verbosity; debug scrubs PAN, CVV
   and PII; API keys appear in neither logs nor exception messages. Scrubbing goes through the one
   central allowlist function per runtime, and every language ships log-capture tests asserting it.
6. **Do not decide open items.** Items in [`docs/open-items.md`](docs/open-items.md) have owners.
   Where code needs an undecided answer, leave a marker referencing the OQ.

## 8. Where to look next

| Question | File |
| --- | --- |
| How do I handle outcome X in my language? | [`docs/failover-cookbook.md`](docs/failover-cookbook.md) |
| What exactly does the contract require? | [`docs/failover-contract.md`](docs/failover-contract.md) |
| What is the full runtime surface? | [`docs/runtime-tdd.md`](docs/runtime-tdd.md) |
| Why is it built this way? | [`docs/architecture.md`](docs/architecture.md) · [`docs/adr/README.md`](docs/adr/README.md) |
| How does a release get proven? | [`docs/pipeline-and-release.md`](docs/pipeline-and-release.md) |
| Language-specific quickstart | `languages/<language>/README.md` |
