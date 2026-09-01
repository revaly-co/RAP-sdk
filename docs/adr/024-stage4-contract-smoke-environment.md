# ADR-SDK-024 — Stage-4 Contract Smoke: Per-Language Runtime Suites Against Backbone Staging (Interim); Merchant Sandbox Is Key-Scoped, Not URL-Scoped

**Status:** Accepted — ratified 2026-07-18 at the stage-4 build story (drafted 2026-07-17,
after all six runtimes; ADR-SDK-015 order). Was tracked as **OQ-16** in `../open-items.md`
(closed 2026-07-18). Implementation record below.
**Source:** post-RFC (stage 4 of `../pipeline-and-release.md` names "Sandbox" without pinning a
concrete environment); platform facts recorded 2026-07-17
**Owner:** SC Eng + DevOps (ADR-SDK-018)

## Context

Pipeline stage 4 is a release-blocking **live contract smoke of all six SDKs**: charge, each
error class where triggerable, reconcile both verdicts — "the taxonomy is unproven against
reality" until it runs (`../pipeline-and-release.md` §2 row 4). ADR-SDK-014 fixed the credential
path (Enablement-issued CI key, Key Vault) and left environment parity as a pre-GA task. What
"Sandbox" concretely *is* was never pinned, and nothing yet documents the per-language E2E
target. ADR-SDK-015 separately commits .NET to being **dogfooded via the platform's E2E tests**.

Platform environment facts (recorded 2026-07-17, from the platform repo's staging-deploy
workflow and squad confirmation):

- The platform's staging runs on **Azure Container Apps in the dev subscriptions**. It is an
  internal pre-release environment — **staging is NOT the merchant Sandbox**.
- **Merchant sandbox and live share the same production URL.** The separation is the **API
  key's scope**, not the URL — there is no `sandbox.` host for merchants.
- The platform repo already runs a post-staging-deploy E2E job with the operational problems
  solved: environment-scoped secrets (staging URL + API key), a **revision-serving gate** (ACA
  reports a deploy complete before the new revision takes traffic — E2E must wait for the new
  revision at 100%), and JUnit result publishing. SDK smoke jobs reach staging with the same
  environment-scoped secrets the platform's E2E job uses; no additional network provisioning
  is required for them.
- The platform's Playwright API suite (~39 specs) already covers the platform surface broadly,
  including rows the SDK taxonomy cares about: validation errors (400/422), API-key auth
  (401/403), declines, circuit-breaker fallback, and the transactions lookups.

## Problem

Fix, before it becomes tribal knowledge: what the per-language live E2E is (and is not), which
environment it targets in which phase, and which direction (SDK repo vs platform repo) runs it —
without re-deciding anything ADR-SDK-014 already fixed.

## Decision

1. **The per-language suite is a thin runtime-contract smoke, not a platform test.** Each
   language runs a ~6-scenario script *through its own runtime*: charge approved → a
   PermanentRejection row (validation and/or auth) → reconcile `Found` and `NotFoundYet` (fresh
   random `merchantTransactionId`) → further §2 rows only where live-triggerable. Its single
   purpose is **proving the SDK's classification against reality**. It deliberately does NOT
   replicate the platform's Playwright breadth — platform coverage is the platform's job.
2. **Interim stage-4 target = Backbone staging ACA** (dev subscriptions), reached with
   environment-scoped secrets (staging URL + staging API key) in the rap-sdk repo. No IP
   allowlisting required. **Blocking** on release tags (stage-4 gate: any language red blocks
   the release for all six); a scheduled nightly run is advisory.
3. **Reverse direction (dogfood), platform repo:** the post-staging-deploy job additionally
   runs the SDK smoke suites against the freshly-served revision — .NET first (the ADR-SDK-015
   dogfooding commitment), other languages as their suites exist. **Advisory** posture there
   (platform deploys must not be hostage to SDK-side reds), reusing the existing
   revision-serving gate.
4. **At GA, retarget to the merchant sandbox key-scope on the shared production URL** once the
   ADR-SDK-014 environment-parity checklist passes (with OQ-11's edge verification). Staging
   remains the pre-release target thereafter; the sandbox-scoped run is the release gate.

## Rationale

- The value of stage 4 is classification-vs-reality, and staging is the earliest real
  environment that emits the real taxonomy (incl. P-1 `code` on 5xx and the circuit-breaker
  fallback path). Waiting for sandbox-scope provisioning would idle the gate for no safety gain.
- Reusing the platform's E2E machinery (secrets model, revision gate) avoids re-solving solved
  operational problems and keeps one environment-truth between the two repos.
- Thin suites keep six-language maintenance honest: the mock transport (runtime-tdd §8) already
  covers every §2 row deterministically; live smoke only needs to prove the rows reality can
  produce.

## Alternatives considered

- **Replicate the Playwright suite per language:** rejected — duplicates platform coverage ×6,
  tests the platform rather than the SDK contract, unmaintainable.
- **Wait for the merchant sandbox key-scope for all smoke:** rejected as the only path — parity
  confirmation is pre-GA anyway; staging exists now and catches drift during the build phase.
- **Mock-only (no live smoke):** rejected — stage 4 exists precisely because simulated taxonomy
  is not proof (`../pipeline-and-release.md`).

## Consequences

- **OQ-11 is NOT discharged by this.** Direct ACA staging hits bypass the AFD/WAF edge; the
  502/504/reset rows of failover-contract §2 stay design assumptions until the edge
  verification runs against the real path.
- **Quickstart wording sweep required** (before repo-public at the latest): shipped
  dotnet/java/php READMEs and `runtime-tdd.md` §1 phrase testing as "point `baseUrl` at the
  Sandbox URL" — with key-scoped sandbox there is no separate merchant URL. Wording becomes
  "use your sandbox-scoped API key"; the `baseUrl` override remains for internal/staging use.
- ADR-SDK-020 applies to smoke CI logs: values-free output, keys via environment secrets only,
  never echoed.
- The platform's own E2E stays advisory on staging deploys; the rap-sdk stage-4 run of the SAME
  suites is blocking — same machinery, opposite gate posture, and that asymmetry is intentional.
- One provisioning act per phase: a staging API key for the rap-sdk repo's environment now
  (analog of the platform's E2E key); the sandbox-scoped key via Enablement (ADR-SDK-014) at GA.

## Implementation guidance (for the stage-4 build story)

- rap-sdk: `smoke-<language>` jobs chained after stage 3, gated to release tags + nightly
  schedule + manual dispatch — never on plain PRs (network + secrets stay out of the PR path).
- Suites live per language beside the unit tests (e.g. `languages/<lang>/smoke/`), reusing each
  runtime's quickstart shape; every reconcile scenario uses a fresh random
  `merchantTransactionId`; assert correlation ids present on every path (DX §c).
- Platform repo: extend the existing post-deploy E2E job to invoke the SDK smoke artifacts;
  keep `continue-on-error` there.
- Record the staging URL/key names and the (future) sandbox key-scope in the pipeline secrets
  table (`../pipeline-and-release.md` §"Secrets") when built.

## Implementation record (2026-07-18)

Built as `smoke-<language>` jobs in `.github/workflows/pipeline.yml` (chained after each
`build-<language>` job; gating condition = release-tag push (`**/v*`) OR nightly schedule
(06:00 UTC) OR `workflow_dispatch`; `timeout-minutes: 15`; fail-closed when secrets are
unprovisioned — a silent skip would read as coverage that never ran). Suites live at
`languages/<lang>/smoke/` and are compile-guarded by stage 3 (dotnet: slnx project; java:
reactor module; go: `go build ./...`; python: `compileall`; php: `php -l`; ts: tsconfig
include — the suites double as a quickstart-surface compile proof).

**Environment contract (identical across all six runners; exit 0 pass / 1 fail / 2
unconfigured):**

| Variable | Source | Meaning |
| --- | --- | --- |
| `RAP_SMOKE_BASE_URL` | GitHub environment **`staging`**, secret | Target base URL (kept out of logs and code — the repo goes public pre-GA) |
| `RAP_SMOKE_API_KEY` | environment `staging`, secret | Staging key borrowed from the platform's E2E pool. Scope lives ON the key; staging (dev subs) always executes via the simulator gateway either way — prefer a sandbox-scoped key for GA parity |
| `RAP_SMOKE_GATEWAY_ROUTING_ID` | environment `staging`, secret | Included in charge payloads when set (the platform's E2E sends it on every charge; staging routes by it) |
| `RAP_SMOKE_FAULT_INJECT` | workflow env (not a secret), value `pre-dispatch` | Sent as the platform's `X-Backbone-Fault-Inject` header — the executor fault seam (platform ADR 014 test affordance) that fails a charge between intent reservation and gateway dispatch. **Structurally inert in production**; the scenario SKIPs when unset. Remove the workflow line at the GA retarget |

**Scenario matrix (8, identical order in all six languages; every id fresh, ≤ 100 chars;
values-free output — identifiers/statuses/classes/correlation ids only, unexpected non-SDK
errors reported by type name so transport chains cannot leak endpoint detail into public CI
logs):**

1. `charge-approved` — `4111111111111111` 12/**2027**, USD — success surface, `transactionId`
   non-empty, correlation id observed via the wire-trace hook (the designed success-path
   observer, DX §c).
2. `charge-declined` — the **same PAN** with 12/**2020**: the expiry drives the outcome
   (staging-verified matrix, Backbone test run 2026-07-18 — `transactionStatus 1` at 12/2027,
   `2` at 12/2020; supersedes the CHG-032 18-digit-card row from the Playwright spec). A
   decline is a **success-surface business outcome**, not a failure class.
3. `charge-validation-rejected` — **empty card number** → PermanentRejection 400. Chosen
   because it passes every client-side model (python's pydantic enforces the spec's
   `amount ≥ 0` and id max-length locally, so those triggers never reach the wire) while the
   platform's `[Required]` validation rejects it — the rejection is proven to come from
   reality. 4xx carries no `code` (platform strips it off non-5xx).
4. `charge-auth-rejected` — synthetic invalid key → PermanentRejection 401 (platform's
   `UnauthorizedErrorResponse` is `{error, details}` — no `code`; correlation header still
   echoed by middleware).
5. `charge-not-processed-503` — fault-inject header via a real-HTTP wrapper at each runtime's
   transport seam (inside the runtime's own header injection) → **TransientFailure with
   status 503 + `code=not_processed`** — the fast-failover row valid input cannot reach
   deterministically. SKIPs when `RAP_SMOKE_FAULT_INJECT` is unset.
6. `reconcile-found-approved` — scenario 1's id → `Found(Approved)` through the runtime's own
   outcome mapping (this is the approval proof), correlation id present.
7. `reconcile-found-declined` — scenario 2's id → `Found(Declined)` — the outcome branch that
   tells a merchant their own gateway is safe.
8. `reconcile-not-found-yet` — fresh never-used id, tight policy → `NotFoundYet` with last
   HTTP status asserted **404** (proves the API was reached, not a transport short-circuit)
   and the last correlation id present.

**Edge note (2026-07-18, at secret provisioning):** the provisioned `RAP_SMOKE_BASE_URL`
fronts staging **via AFD** — smoke traffic traverses the AFD/WAF path, better parity than the
direct-ACA assumption in Consequences. OQ-11 still requires observing the edge *failure* rows
(502/504/reset classification) and remains open; routine smoke passes do not discharge it.

**Live-run findings (2026-07-18, first stage-4 execution — exactly what this stage exists
for; findings 1/4/7 resolved or corrected 2026-07-20 — see the dated resolution note after
the list):**

1. **Spec-vs-reality gaps (markers for the platform; SDK does not decide them):** controller
   business validation on `POST /payments` REQUIRES `paymentMethodType` ("Valid values are:
   'creditCard', 'gatewayPaymentMethodId', 'vaultToken'") and, with `creditCard`, a cardholder
   name ("If FirstName or LastName is missing, FullName is required") — the gated spec marks
   both optional, so every generated core accepts payloads reality rejects with 400. These
   business-validation 400s carry an `{error}`-only body (neither ProblemDetails nor the
   5xx `code` shape) — a third 4xx body variant the SDKs' lenient parsing already tolerates.
2. **Staging-simulator approval requirements (environment facts, not contract):** the
   configured routing targets a CyberSource simulator, which approves only when
   `orderId` and `paymentMethod.email` are also present — omitting
   either yields a clean decline (`transactionStatus 2`). Bisected via direct probes;
   encoded in the smoke builders (`buildCharge`), with `initiatedBy`/`billingAddress`
   confirmed droppable and amount not outcome-relevant.
3. **The fault-inject header traverses AFD unmodified** — the `503 + code=not_processed`
   row is triggerable through the edge path.
4. **Merchant-reference length ceiling (platform marker):** the CyberSource simulator path
   declines any charge whose `merchantTransactionId`/`orderId` exceeds ~50 characters
   (live-bisected: 58 declines, 47/42 approve) even though the platform accepts up to 100 —
   surfaced by the dotnet suite alone because its generated ids were 60 chars. Real
   merchants with long ids would hit this on the CyberSource route; smoke ids are kept
   under ~48.
5. **Cross-SDK client-validation divergence (recorded):** the php/python cores reject an
   empty card number client-side (`InvalidArgumentException` / pydantic `ValidationError`)
   while dotnet/go/ts/java pass it to the wire — so the cross-language validation scenario
   uses a NAMELESS charge (valid card, no `fullName`/`firstName`/`lastName`), which every
   client model accepts and the server deterministically 400s.
6. **First full live proof:** all six suites pass — go/dotnet/python verified locally
   **8/8** (go also 8/8 in CI dispatch 29669808901, with typescript and java), and the
   final cross-language CI dispatch runs on the same commit as this record.
7. **Follow-up (marker):** the six quickstart READMEs show charge payloads reality would
   400 (missing `paymentMethodType`/name) — align them with the proven minimal shape in a
   follow-up sweep (DX §9 copy-paste bar), coordinated with the platform's answer to
   finding 1.

**Platform resolution + corrections (2026-07-20 — the `spec/v2.3.0+80cc897` re-pin):**

1. **Finding 1 is resolved at the source.** Backbone PR #251 (platform ADR 020 — "validation
   reality matches the published contract") moved the wire toward the spec: `paymentMethodType`
   is now genuinely optional — inferred at the API boundary when exactly one payment-method
   object is populated (two-plus without an explicit type = 400; stored-method and
   recommendation flows are never inferred) — and the cardholder-name rule remains server-side
   but is now documented per-type in the spec (`PaymentMethod` description + both request
   schemas' enum prose). The gated artifact documenting both is `spec/v2.3.0+80cc897`,
   pinned 2026-07-20.
2. **Correction to finding 1's body-shape claim.** The `{error}`-only 400 body is **not** a
   third 4xx variant — it is a valid `ErrorResponse` instance (`details` and `code` are
   optional in that schema, and always were). Spec 2.3.0's shared 400 response now says so
   explicitly ("validation failures carry a `details` object keyed by the offending fields;
   business-rule rejections may carry `error` alone"). Nothing SDK-side depended on the
   mis-read: the lenient parse path already handled it, and no runtime treats body shape as a
   classification input (the failover-contract §2 algorithm uses status + `code` only).
3. **Finding 4's platform marker is discharged docs-only.** `merchantTransactionId` on both
   request schemas now carries the ≤ 48-character gateway-compatibility guidance (the platform
   stays gateway-agnostic; the 100-char platform limit is unchanged). Smoke ids stay < 48.
4. **Finding 7 is discharged.** The six quickstart READMEs were swept in the re-pin PR to the
   proven minimal shape — cardholder name present, `paymentMethodType` omitted per the
   now-documented inference. The smoke builders still send the explicit type (contract-legal
   indefinitely) to keep one deterministic cross-language wire shape; their comments no longer
   claim the type is server-required.

**Still open after this record:** the platform-repo reverse-dogfood job (§Decision 3 —
advisory invocation of these suites from the platform's post-staging-deploy workflow), and
the GA retarget (§Decision 4 — repoint the `staging` environment secrets to the merchant
sandbox key-scope, drop `RAP_SMOKE_FAULT_INJECT`), gated on the ADR-SDK-014 parity checklist
+ OQ-11. OQ-11 remains NOT discharged (staging bypasses the AFD/WAF edge).

## Decision-4 evidence, 2026-07-25 (OQ-11 now closed)

OQ-11 **was** discharged 2026-07-21 (ADR-SDK-029), and the sandbox key-scope has since been
exercised directly. Evidence record: [`../prod-sandbox-validation.md`](../prod-sandbox-validation.md).

The released **v0.4.1** artifacts for all six languages — installed from the GitHub release
assets exactly as a merchant installs them — ran a merchant-style contract exercise against the
**merchant sandbox key-scope on the shared production URL**, through the real AFD/WAF edge:
**6/6 languages green, 39 passed / 0 failed / 8 skipped**. The harness deliberately lives outside
this monorepo, in **`revaly-co/RAP-sdk-integration-tests`**, and never consumes `languages/*/`
source — it tests what shipped, via the customer install path. §Decision 1's credential model
(one URL, the key's scope selects the environment) is confirmed in practice.

**This does not by itself execute the retarget**, which stays a provisioning act. Two findings
change how it must be executed:

1. **The fault injector is inert on the production path.** Probed directly: with
   `X-Backbone-Fault-Inject: pre-dispatch` the charge simply approved instead of returning
   `503 + code=not_processed`. Dropping `RAP_SMOKE_FAULT_INJECT` at the retarget (as §Decision 4
   already instructs) therefore **removes live coverage of the only row that licenses immediate
   failover**. That row reverts to mock-transport coverage (`runtime-tdd.md` §8) plus unit
   suites. This is an acceptable trade, but it must be accepted **in writing at retarget time**,
   not discovered afterwards — it is the one contract row where the SDK's safety guarantee stops
   being exercised against a real server.
2. **Charge routing on the sandbox key-scope is `gatewayRoutingId`-driven, not BIN-driven.**
   Without the routing token every charge lands in the `flexpay_declined` sink (responseCode
   50130). The retargeted jobs must carry `RAP_SMOKE_GATEWAY_ROUTING_ID` as a first-class third
   secret, not an optional one.

ADR-SDK-014 parity checklist after this run: taxonomy rows **partial** (every row but
`not_processed`, proven ×6), P-1 `code` emission **unobserved** (blocked by finding 1 — the only
carrier of `not_processed` is untriggerable here; the observed 4xx bodies were `error`-only,
which `spec/v2.3.0` documents as valid and which the SDKs classified correctly), BIN-routing
**characterised** (finding 2), OQ-11 leg **closed**.

## Decision-4 retarget: two-target smoke (2026-07-25, supersedes the acceptance below)

**The coverage delta is recovered, not accepted.** The acceptance recorded further down was the
right call for a single-target retarget, but it is **superseded**: rather than demote the
`503 + not_processed` row to mock-only, stage 4 now runs each language's suite against **two
targets in one job**.

| Step | Target | Secrets | Injector | Proves |
| --- | --- | --- | --- | --- |
| 1 | merchant sandbox key-scope on the production URL (GA target) | `RAP_SANDBOX_*` | not passed → row SKIPs | every §2 row reachable in production, through the real AFD/WAF edge |
| 2 | Backbone staging | `RAP_SMOKE_*` | `RAP_SMOKE_FAULT_INJECT=pre-dispatch` | the `503 + not_processed` row — the only one licensing immediate failover |

Neither target can prove the whole taxonomy alone: the injector does not exist in production, and
staging does not exercise the GA edge or credential path. Running both is what keeps the taxonomy
fully covered while the GA target becomes the primary one. Both steps live in a single job per
language, so either failing blocks that language — and any language red still blocks the release
for all six.

**Fail-closed on the injector.** The job aborts if the `RAP_SMOKE_FAULT_INJECT` variable is unset.
An unset value would make step 2 *silently SKIP* the immediate-failover row, which is exactly the
quiet-coverage-loss this design exists to prevent — the suites treat it as a skip, so CI must treat
its absence as an error.

**Secrets required in the `staging` environment** (six, plus one variable):

```
RAP_SANDBOX_BASE_URL            https://api.revaly.co
RAP_SANDBOX_API_KEY             sandbox-scoped merchant key
RAP_SANDBOX_GATEWAY_ROUTING_ID  sandbox gateway routing token
RAP_SMOKE_BASE_URL              Backbone staging base URL — HOST ROOT ONLY, no /payments
RAP_SMOKE_API_KEY               staging E2E-pool key
RAP_SMOKE_GATEWAY_ROUTING_ID    staging routing token for a gateway where expiry drives
                                the outcome (12/2027 approves, 12/2020 DECLINES)
vars.RAP_SMOKE_FAULT_INJECT     pre-dispatch
```

## Vault-token rows on both targets (2026-09-01, spec 2.6.0 / SC-477)

Spec 2.6.0 added a `vaultToken` on the transaction **list row** (flat, alongside the other
`paymentMethod*` fields) and extended the existing nested token to the two single-transaction
reads. The eight rows above were written at spec 2.1.x and never exercise a vault credential, so
that surface shipped with no stage-4 coverage. Two rows close it, and they run on **both** targets:

| Row | Proves |
| --- | --- |
| `charge-vault-token` | a presented vault token is accepted as a real credential (`responseCode != 50167`), the request flips to `paymentMethodType: VaultToken`, and the charge response reports the token |
| `vault-token-on-reads` | the spec-2.6.0 delta itself — the token nested on `GET /transactions/{id}`, and **FLAT** on the `responseType=detailed` list row |

**Presenting an existing token, not auto-vaulting a card.** Backbone will mint a token for a raw
PAN when a `customerId` is present, but the smoke deliberately presents one instead. Presenting is
non-mutating (it writes no new vault record on every CI run), deterministic (the reported token
must equal the one presented, whereas a minted token may roll under the Account Updater), and it
is the one shape that behaves identically on both targets.

**No approval assertion, on purpose.** The approval outcome on a vault route is amount- and
gateway-specific per target — staging's Chase sandbox approves 2500 and declines 1999 with
"Do not honor" — while the thing 2.6.0 changed, that the token is *reported*, holds on approved
and declined transactions alike. Gating these rows on `transactionStatus` would buy nothing and
break on the other target.

**The customer is part of the credential.** A vault token is stored against a `(token, customer)`
PAIR; presenting it under any other customer resolves to nothing and declines 50168, which reads
like a broken token and is not. That is why `RAP_*_VAULT_CUSTOMER_ID` is required alongside the
token rather than inferred. (The platform's own prod probe records the same trap —
`tools/direct-path-prod-pilot/methods.mjs`.)

**Gate posture: partial fails, absent warns.** A *partially* provisioned set is a hard error — a
half-configured credential degrades the row into a decline that reads like a product defect. A
*wholly absent* set emits a `::warning::` and the rows SKIP visibly, which is the state until the
secrets are provisioned. This is deliberately weaker than the injector's fail-closed gate: the
injector's absence silently loses a row that already had coverage, whereas these rows are new and
their skip is loud and counted.

**Eight further secrets in the `staging` environment** (four per target):

```
RAP_SANDBOX_VAULT_API_KEY       vault-enrolled merchant key on the sandbox/production URL
RAP_SANDBOX_VAULT_CUSTOMER_ID   the customer the token is bound to
RAP_SANDBOX_VAULT_ROUTING_ID    routing token for the vault-capable gateway
RAP_SANDBOX_VAULT_TOKEN         a format-preserving vault token minted for that customer
RAP_SMOKE_VAULT_API_KEY         Backbone staging vault-enrolled key (NOT the main smoke key —
                                the vault merchant is a different key-scope)
RAP_SMOKE_VAULT_CUSTOMER_ID     the customer the staging token is bound to
RAP_SMOKE_VAULT_ROUTING_ID      staging vault gateway routing token
RAP_SMOKE_VAULT_TOKEN           the staging vault token
```

`bin` and `lastFourDigits` are **derived from the token**, not configured: vault tokens are
format-preserving, so the value carries both.

**VALIDATED 2026-09-01 against Backbone staging, green ×6** — every language reports
`RESULT: PASS (10/10 passed, 0 skipped)` with `PASS charge-vault-token` and
`PASS vault-token-on-reads`. The skip path was exercised too: with the vault set unset all six
report `SKIP` on both rows and stay green.

`RAP_SMOKE_*` keeps its original name and now denotes the **step-2 (staging) target** specifically.

**VALIDATED 2026-07-25 — two-target stage 4 is green ×6.**
[Run 30178436668](https://github.com/revaly-co/RAP-sdk/actions/runs/30178436668): every language
passes **both** steps — step 1 `RESULT: PASS (7/8 passed, 1 skipped)` with
`SKIP charge-not-processed-503 (injector is staging-only)`, step 2
`RESULT: PASS (8/8 passed, 0 skipped)` with
`PASS charge-not-processed-503 (status=503 code=not_processed)`. The full failover-contract §2
taxonomy is now proven against real servers in all six languages, with **nothing demoted to
mock-only coverage**. The staging gateway that makes this work is one where expiry drives the
outcome; it also restores `reconcile-found-declined (outcome=Declined)`.

**Two staging-provisioning traps, both hit on 2026-07-25 and both reproduced locally:**

1. **`RAP_SMOKE_BASE_URL` must be the host root, not an endpoint.** A value ending in `/payments`
   makes the SDK append its own path (`/payments/payments`) and **every** call returns 404. The
   signature is unmistakable and misleading: 7 of 8 scenarios fail while `reconcile-not-found-yet`
   *passes*, because that is the one scenario expecting a 404. Verified by reproducing the exact
   CI result (`1/8 passed`) locally with the suffixed URL.
2. **The staging gateway must be one where the expiry drives the outcome.** The suites depend on
   12/2027 approving and 12/2020 **declining**. A routing token pointing at a gateway that approves
   regardless passes `charge-declined` — which only asserts that a transaction binds — and then
   fails `reconcile-found-declined` with `expected outcome Declined, got Approved`. Confirmed
   independently by the integration app reporting `transactionStatus=1` where 2 was required.

---

## Superseded: the single-target acceptance (2026-07-25)

*Retained for the record — the reasoning below still explains why the row cannot be proven in
production, but its conclusion (mock-only coverage) no longer applies now that step 2 exists.*

**Written acceptance, as required above.** At the GA retarget the
`503 + code=not_processed → TransientFailure` row **loses live server coverage** and is carried
by mock-transport coverage alone (`runtime-tdd.md` §8, `RapMockTransport` and its per-language
equivalents) plus each runtime's unit suites. This is accepted deliberately, with eyes open:

- It is the **only** failover-contract §2 row that licenses immediate failover, so it is the row
  where losing a real-server assertion carries the most weight.
- It is unavoidable, not a shortcut: the fault injector is a staging/sandbox-platform facility and
  is **inert on the production path** (verified 2026-07-25 — the injected charge simply approved;
  `../prod-sandbox-validation.md` Finding 1). No configuration of the sandbox key-scope can
  produce the row.
- The compensating controls are: the mock row is asserted in all six runtimes on **every PR**
  (stage 3), the classification algorithm it exercises is the same transport-level code path the
  live rows traverse, and the platform-side behaviour is owned by Backbone ADR 014 with its own
  tests.
- **Revisit trigger:** if the platform ever exposes a production-safe fault seam on the sandbox
  key-scope, this delta should be closed by restoring the row — reopen under OQ-16.

**The retarget is now a pure provisioning act — no workflow edit.** `pipeline.yml` reads
`RAP_SMOKE_FAULT_INJECT` from the `staging` environment **variable** (set to `pre-dispatch` today,
preserving staging behaviour unchanged), and the fail-closed guard now requires
`RAP_SMOKE_GATEWAY_ROUTING_ID` alongside URL and key — per Finding 2 the routing id is required,
not optional, because without it charges route to the declining sink and no approval row can pass.

Retarget runbook — **delete the variable first**, then repoint:

1. **Delete** the `staging` environment variable `RAP_SMOKE_FAULT_INJECT`. All six suites SKIP the
   row when it is unset (verified per suite). While the secrets still point at staging this costs
   only that one row and stage 4 stays green.
2. Repoint the three `staging` environment **secrets** to the merchant sandbox key-scope:
   `RAP_SMOKE_BASE_URL` (→ the shared production URL), `RAP_SMOKE_API_KEY` (→ the sandbox-scoped
   key), `RAP_SMOKE_GATEWAY_ROUTING_ID` (→ the sandbox gateway routing token).
3. Trigger stage 4 via `workflow_dispatch` and confirm 6/6 green with the row reported as SKIP.

**Order matters, and this direction is the safe one.** Repointing the secrets while the variable
is still set makes the fault-inject row a false failure — and stage 4 is **blocking on release
tags**, so a release cut in that window would be blocked for all six languages. Deleting the
variable first never produces a red state: there is no intermediate configuration in which a
scheduled or tag-triggered run fails.

**EXECUTED 2026-07-25 — Decision 4 is retargeted.** The runbook above was run in order: the
`staging` variable `RAP_SMOKE_FAULT_INJECT` was deleted, then all three `staging` secrets were
repointed to the merchant sandbox key-scope on the shared production URL. Proof run (dispatched on
the `chore/oq16-decision4-retarget-prep` ref so it exercised the variable-based workflow):
[run 30176984589](https://github.com/revaly-co/RAP-sdk/actions/runs/30176984589) — **all six
stage-4 smoke jobs green**, each reporting `SKIP charge-not-processed-503
(RAP_SMOKE_FAULT_INJECT not set (injector is staging-only))` and otherwise
`RESULT: PASS (7/8 passed, 1 skipped)`. Stage 4 now exercises the GA target.

*Consistency note:* the environment is retargeted, but `main` carries the old hardcoded
`RAP_SMOKE_FAULT_INJECT: pre-dispatch` until the accompanying PR merges. In that window a stage-4
run from `main` (nightly 06:00 UTC, or a release tag) sends the header to a path where the injector
is inert and the row fails. The PR must land before the next scheduled run; until it does, treat a
red nightly stage 4 as this known cause rather than a regression.

**Tracked deviation — CI key provenance (2026-07-25, owner: Dimitri).** The retarget was executed
with the **already-held sandbox-scoped key** rather than a key issued through Enablement.
ADR-SDK-014 §Implementation guidance specifies the Enablement-issued key for the GA phase, so this
is a deviation, accepted deliberately to close Decision 4 now rather than wait on an issuance
queue. It is the same key used for the 2026-07-25 validation run, so its scope is proven
sandbox-only. **Follow-up:** swap `RAP_SMOKE_API_KEY` for an Enablement-issued CI key and rotate
the current value out; until then the key's custody is wider than the single issuance path
ADR-SDK-014 intends. Same posture as the tracked Packagist placeholder deviation under OQ-3:
recorded, owned, reversible.

**Provisioning status correction (2026-07-25):** the `staging` environment and all three secrets
**already exist** — earlier records in this ADR and in `../open-items.md` described provisioning
them as the one open act, which is stale. They are currently pointed at Backbone staging: the
v0.4.1 release run (2026-07-23) passed stage 4 including the fault-injected row, which only the
staging injector can satisfy. What remains is the repoint above, not the creation.
