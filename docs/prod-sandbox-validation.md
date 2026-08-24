# Prod sandbox key-scope validation — OQ-16 evidence record

**Evidence for:** OQ-16 (`open-items.md`) and **ADR-SDK-024 §Decision 4** — the GA retarget of
stage-4 contract smoke from Backbone staging to the **merchant sandbox key-scope on the shared
production URL**, gated on the ADR-SDK-014 environment-parity checklist + OQ-11.

**Run date:** 2026-07-25 · **Target:** `https://api.revaly.co` (production edge, AFD/WAF in path)
· **Credential:** sandbox-scoped merchant API key (key scope selects the environment — one URL,
per ADR-SDK-024) · **Gateway:** `RAP_GATEWAY_ROUTING_ID` set — the routing token, not the PAN,
selects the sandbox gateway (Finding 2).

**Software under test:** the released **v0.4.1** GitHub release artifacts for all six languages
(`spec/v2.3.0+80cc897`, source commit `f860130`, generator v7.23.0 — provenance identical ×6).

## Harness

The exercise runs from a **separate repository**, not from this monorepo:

> **https://github.com/revaly-co/RAP-sdk-integration-tests** (private)

One merchant-style integration app per language, each installing the SDK the way a merchant
would — from the released artifact (`.nupkg` / `.tgz` / `.whl` / `.zip`), SHA-256 verified
against `provenance.json`, **never** from `languages/*/` source. That separation is the point:
it proves what shipped, through the same install path a customer takes.

This is complementary to, not a replacement for, the in-repo stage-4 smoke suites
(`languages/*/smoke/`), which stay pinned to Backbone staging until the Decision 4 retarget.

**This document is the evidence of record** — the run output (live identifiers masked) is in Appendix A below, so
the evidence stands on its own inside this repo and does not depend on the harness repository
staying reachable. The link above is a cross-reference to the harness only.

> **Reproducibility caveat:** the harness repo's *committed* artifacts were still **v0.4.0** at the
> time of this run; the v0.4.1 upgrade (artifact refresh + build-config pins) existed only in the
> operator's working copy and was not pushed. Anyone re-running from a clean clone of that repo
> will exercise v0.4.0 until the upgrade lands there. The versions recorded here are what actually
> ran, verified against each artifact's `provenance.json` (`packageVersion: 0.4.1`, all six).

## Result: 6/6 languages green

| Language | Artifact under test | Exit | Passed | Skipped |
| --- | --- | --- | --- | --- |
| .NET | `Revaly.Sdk` 0.4.1 (nupkg) | 0 | 6/7 | fault-inject |
| TypeScript | `revaly-sdk` 0.4.1 (tgz) | 0 | 6/8 | fault-inject, outcome-unknown |
| Python | `revaly_sdk` 0.4.1 (wheel) | 0 | 7/9 | fault-inject, outcome-unknown |
| Go | `rap-sdk/languages/go` v0.4.1 (zip) | 0 | 6/7 | fault-inject |
| Java | `co.revaly:revaly-sdk` 0.4.1 (zip) | 0 | 7/8 | fault-inject |
| PHP | `revaly/sdk` 0.4.1 (zip) | 0 | 7/8 | fault-inject |

**39 passed · 0 failed · 8 skipped** across 47 scenario slots. All output values-free per
ADR-SDK-020; no language retried or resubmitted — the caller-bounded reconcile helper was the
only loop.

## failover-contract §2 rows exercised through the production edge

| Row | Result |
| --- | --- |
| Approved charge (`transactionStatus=1`) | ✅ proven ×6 |
| Business decline on the **success surface** (`transactionStatus=2`) | ✅ proven ×6 — never a typed error, exactly as contracted |
| 4xx → `PermanentRejection` | ✅ proven ×6 (HTTP 400) |
| `reconcile` → `Found(Approved)` | ✅ proven ×6, mandatory default/unknown-verdict branch present |
| `reconcile` → `NotFoundYet` | ✅ proven ×6 from real 404s, caller-bounded (2 attempts), never read as proof of absence |
| Generated-core secondary surface (get-by-id, payment-methods) | ✅ proven ×6 |
| **503 + `code=not_processed` → `TransientFailure`** | ❌ **not reproducible here** — see Finding 1 |
| Timeout-after-send → `OutcomeUnknown` | ⚪ no deterministic live trigger by design; mock/preflight only |

## Findings

### 1. The fault injector is inert against the prod sandbox scope

Probed directly (Go, 2026-07-25): with `X-Backbone-Fault-Inject: pre-dispatch` the charge
**simply approved** instead of returning `503 + code=not_processed`, turning the scenario into a
false FAIL (`RESULT: FAIL (6/7)`). The injector is a staging/sandbox-platform facility and is not
present on the production path.

**This corroborates ADR-SDK-024 §Decision 4's instruction to drop `RAP_SMOKE_FAULT_INJECT` at the
retarget — and names its cost.** The `not_processed` row is the *only* row that licenses immediate
failover, and retargeting stage-4 smoke to the prod sandbox key-scope removes its live coverage;
it would then be covered exclusively by each runtime's mock transport (`runtime-tdd.md` §8) and
unit suites. That is an acceptable but deliberate trade — it should be recorded as a known
coverage delta at retarget, not discovered afterwards.

### 2. Charge routing on this scope is driven by `gatewayRoutingId`, not BIN

Without `RAP_GATEWAY_ROUTING_ID` every charge lands in the `flexpay_declined` sink
(responseCode 50130) and nothing approves. This is the practical shape of the ADR-SDK-014 "test
card BIN-routing coverage" checklist leg on the prod sandbox scope: the routing token, not the
test PAN, selects the gateway. Any retargeted smoke job must carry the token as a third
environment secret alongside URL + key.

> **Update 2026-08-24 — 50130 on this scope now has a SECOND cause, and the token no longer
> rules it out.** Backbone enrolled this same sandbox account
> (`08fd0caa-…`) on the **direct path** in production on 2026-08-11 (`Migration_2026081100_`
> `EnrolDirectPathPilotAccount`, commit `33d172ed`). A charge that presents as a **first
> attempt** — `recovery.retryCount` absent or `0` — is admitted to the direct fork, where the
> gateway route resolver declines it `50130` **with no fallback to the existing route**. The
> routing token is set and valid; it is simply not consulted on that fork. Probed live
> 2026-08-24 with the token present: first attempt = `transactionStatus 2` / `50130`; the
> byte-identical charge carrying `recovery.retryCount: 1` = `transactionStatus 1` / `10000`
> approved, and the 12/2020 row = `transactionStatus 2` / `30026` "Expired card" (a real gateway
> decline rather than the sink).
>
> **Timeline, verified vs inferred.** Verified: the enrolment migration landed 2026-08-11; the
> 2026-08-12 nightly failed stage-4 across all six languages with exactly this `50130` signature;
> nightly runs from 2026-08-13 through 2026-08-24 06:09 UTC were green; a live probe on
> 2026-08-24 at 18:49 UTC reproduced the first-attempt decline. Inferred, not confirmed from any
> repo artefact: the direct path was evidently not active for this account during the green
> window and was (re-)enabled on 2026-08-24 — that is operational/DB state
> (`direct_path_enrollments.is_active`, the store execution kill switch), which git does not
> record. Do not read the green window as evidence the fork was absent by design.
>
> This is why the `languages/*/smoke/` harnesses stamp `recovery.retryCount` on **every** charge:
> Backbone's
> `DirectPathAttemptEligibility.IsFirstAttempt` short-circuits a retry back onto the existing
> TransactionApi dispatch route before the enrollment read, the treatment pipeline and the
> resolver. Reading a bare `50130` as "the routing token is missing" is no longer sound on this
> scope — check the attempt shape first.

### 3. `ErrorResponse.code` was absent on the observed 4xx bodies

The invalid-request scenario returned HTTP 400 with no `code` (`class=PERMANENT_REJECTION
status=400 code=null`) — an `error`-only 400 body, which `spec/v2.3.0` documents as a valid
`ErrorResponse`. The SDKs classified it correctly: unrecognized/absent `code` → not
`not_processed` → `PermanentRejection`, per failover-contract §2 and ADR-SDK-007. P-1 `code`
emission itself remains unobserved on this scope, because the only row that carries
`not_processed` is the one Finding 1 shows cannot be triggered here.

### 4. SC-326 (`firstSixDigits`/`bin` deserialization crash) — fix verified live

The Backbone-side fix shipped shortly before this run. Root cause was an **empty**
`bin`/`firstSixDigits` value, not the 8-digit BIN passthrough originally hypothesised; the fix
returns **null** instead, which every generated validator skips. Values-free shape probe over the
prod-sandbox list endpoint:

```
payment methods bound (no client-side throw): 20
  firstSixDigits shapes: {'6-digit': 2, 'null': 18}
  bin shapes:            {'6-digit': 2, 'null': 18}
```

18 of 20 records carry the null; pre-fix those were empty strings and the first would have raised
`ValidationError` (Python) / `InvalidArgumentException` (PHP). Python bound all 20 and PHP its 5
cleanly. Mechanism: both fields are optional-with-`None` default and each generated regex
validator short-circuits on null, so null passes while `""` fails `^[0-9]{6}$`. Note `bin`'s
pattern is `^(?:[0-9]{6}|[0-9]{8})$` — it already admits 8 digits, so the 8-digit theory never
held for that field.

## ADR-SDK-014 environment-parity checklist — status after this run

| Leg | Status |
| --- | --- |
| Error taxonomy rows reproducible in Sandbox | **Partial** — every row except `503 + not_processed` proven ×6 through the real edge (Finding 1 explains the gap and why it is structural, not a defect) |
| P-1 `code` emission | **Unobserved** — blocked by the same gap (Finding 3) |
| Test card BIN-routing coverage | **Characterised** — routing is `gatewayRoutingId`-driven on this scope (Finding 2) |
| OQ-11 edge verification | ✅ **Closed 2026-07-21** → ADR-SDK-029 |

## What this does and does not settle

**Settled:** the released v0.4.1 SDKs — all six, installed as a merchant installs them — work
end-to-end against the merchant sandbox key-scope on the production URL, through the real AFD/WAF
edge, honouring the failover contract on every row reachable there. The credential model of
ADR-SDK-024 (one URL, key scope selects the environment) is confirmed in practice.

**Not settled:** the Decision 4 retarget itself, which remains an act of provisioning — repointing
the `staging` GitHub environment secrets to the sandbox key-scope, adding the routing token, and
dropping `RAP_SMOKE_FAULT_INJECT` with the coverage delta in Finding 1 accepted in writing. The
ADR-SDK-014 parity checklist closes only as far as Finding 1 permits: the `not_processed` row
cannot be a live-sandbox assertion and must be reassigned to mock coverage. Also still open under
OQ-16: the platform-repo reverse-dogfood job (ADR-SDK-024 §Decision 3).

## Appendix A — run output (identifiers masked)

Values-free per ADR-SDK-020: scenario names, error class names, HTTP statuses. Transaction ids
and correlation ids are masked as `…` for the public record; the unmasked output lives in the
internal evidence record. Reproduce with the harness repo's per-language commands; all six read
the same shared `.env` contract (`RAP_API_KEY`, `RAP_GATEWAY_ROUTING_ID`, optional `RAP_BASE_URL`).

### .NET — `dotnet run`

```
RAP full contract exercise (dotnet, Revaly.Sdk 0.4.0) — live sandbox: 7 scenarios
PASS charge-approved (txn=06FSP… status=approved correlation=…)
PASS charge-declined (txn=06FSP… status=declined correlation=…)
PASS charge-invalid-request (class=PermanentRejectionException status=400 correlation=…)
SKIP charge-fault-injected-not-processed (RAP_FAULT_INJECT not set)
PASS reconcile-found (verdict=Found outcome=Approved correlation=…)
PASS reconcile-not-found-yet (verdict=NotFoundYet attempts=2 correlation=…)
PASS secondary-surface (txn=06FSP… paymentMethods=5)
RESULT: PASS (6/7 passed, 1 skipped)
```

The `0.4.0` in the banner is a hardcoded display string in the harness, not the package that ran —
the `PackageReference` resolved **0.4.1**. Corrected in the harness working copy and re-run, which
printed `Revaly.Sdk 0.4.1` with an identical `RESULT: PASS (6/7 passed, 1 skipped)`. The Java
banner had the same defect and the same correction.

### TypeScript — `node dist/main.js`

```
Revaly RAP SDK integration exercise — TypeScript (revaly-sdk 0.4.1, live sandbox)
PASS  charge-approved                  approved (transactionStatus=1) transactionId=06FSP…
PASS  charge-declined                  declined on the success surface (transactionStatus=2) transactionId=06FSP…
PASS  charge-invalid-request           RapPermanentRejection status=400 correlation=…
SKIP  charge-not-processed-503         RAP_FAULT_INJECT not set — fault injector unavailable
SKIP  charge-outcome-unknown           preflight-only (not deterministically triggerable live)
PASS  reconcile-found                  Found(Approved) transactionId=06FSP… correlation=…
PASS  reconcile-not-found-yet          NotFoundYet attempts=2 lastStatus=404 correlation=…
PASS  secondary-get-transaction-by-id  status=200 transactionId=06FSP… correlation=…
total=8 pass=6 fail=0 skip=2
```

### Python — `.venv/Scripts/python rap_integration.py`

```
RAP SDK integration (python, SDK wheel): 9 scenarios -- live sandbox
PASS charge-approved (txn=06FSP… correlation=…)
PASS charge-declined (declined on the success surface, txn=06FSP… correlation=…)
PASS charge-invalid-request (status=400 correlation=…)
SKIP charge-not-processed-503 (RAP_FAULT_INJECT not set)
SKIP charge-outcome-unknown (no deterministic live trigger -- preflight-only)
PASS reconcile-found (outcome=Approved correlation=…)
PASS reconcile-not-found-yet (attempts=2 last_status=404 correlation=…)
PASS secondary-get-transaction (status=200 txn=06FSP… correlation=…)
PASS secondary-list-payment-methods (count=20 correlation=…)
RESULT: PASS (7/9 passed, 2 skipped)
```

### Go — `./rap-contract-exercise.exe`

```
RAP contract exercise (go, live): 7 scenarios
PASS charge-approved (txn=06FSP… mtid=integ-go-charge-… transactionStatus=Approved)
PASS charge-declined-permanent-rejection (declined on the success surface: txn=06FSP… transactionStatus=Declined)
PASS charge-invalid-rejected (class=PermanentRejection status=400 correlation=…)
SKIP charge-fault-injected-not-processed (RAP_FAULT_INJECT not set (the fault injector is inert outside sandbox/staging))
PASS reconcile-found (verdict=Found outcome=Approved correlation=…)
PASS reconcile-not-found-yet (verdict=NotFoundYet attempts=2 correlation=…)
PASS core-get-transaction-by-id (status=200 correlation=…)
RESULT: PASS (6/7 passed, 1 skipped)
```

### Java — `java -jar target/rap-sdk-integration.jar`

Interleaved `INFO`/`WARN` lines are the SDK's own SLF4J output, retained here because they
demonstrate the ADR-SDK-020 values-free logging surface on a live path.

```
RAP full contract exercise (java, released SDK 0.4.0) — live sandbox: 8 scenarios
INFO co.revaly.sdk.RapClient - rap.request operation=charge status=200 correlation=…
PASS charge-approved (txn=06FSP… transactionStatus=1 correlation=…)
INFO co.revaly.sdk.RapClient - rap.request operation=charge status=200 correlation=…
PASS charge-declined (declined on success surface: txn=06FSP… transactionStatus=2 correlation=…)
WARN co.revaly.sdk.RapClient - rap.request failed operation=charge class=PERMANENT_REJECTION status=400 code=null correlation=…
PASS charge-invalid-request (PermanentRejectionException status=400 correlation=…)
SKIP charge-fault-injected-not-processed-503 (RAP_FAULT_INJECT not set)
INFO co.revaly.sdk.reconcile.RapReconciler - rap.reconcile verdict=Found outcome=APPROVED correlation=…
PASS reconcile-found (Found outcome=APPROVED correlation=…)
INFO co.revaly.sdk.reconcile.RapReconciler - rap.reconcile verdict=NotFoundYet attempts=2 elapsedMs=1361 lastStatus=404 correlation=…
PASS reconcile-not-found-yet (NotFoundYet attempts=2 correlation=…)
PASS secondary-surface-get-transaction-by-id (shape=TransactionResponse txn=06FSP…)
PASS secondary-surface-list-payment-methods (count=5)
RESULT: PASS (7/8 passed, 1 skipped)
```

The `code=null` on the 400 is Finding 3: an `error`-only body, valid per `spec/v2.3.0`, correctly
classified as `PermanentRejection` because absent `code` ≠ `not_processed`.

### PHP — `./run.sh` (php:8.4-cli in Docker)

```
RAP full contract exercise (php, live sandbox): 8 scenarios
PASS charge-approved (txn=06FSP… correlation=…)
PASS charge-declined (shape=success-surface-decline transactionStatus=2 txn=06FSP… correlation=…)
PASS charge-invalid-request-rejected (class=PermanentRejectionException status=400 correlation=…)
SKIP charge-fault-injected-not-processed-503 (RAP_FAULT_INJECT not set — set it to "pre-dispatch" where the injector is enabled)
PASS reconcile-found (verdict=Found outcome=Approved action=acknowledge-success correlation=…)
PASS reconcile-not-found-yet (verdict=NotFoundYet attempts=2 action=hold-and-escalate correlation=…)
PASS transactions-get-by-id (txn=06FSP…)
PASS payment-methods-list (count=5)
RESULT: PASS (7/8 passed, 1 skipped)
```

### Fault-injector probe (Finding 1)

Same Go binary, `RAP_FAULT_INJECT=pre-dispatch` exported:

```
FAIL charge-fault-injected-not-processed: charge succeeded — expected TransientFailure
RESULT: FAIL (6/7 passed, 0 skipped)
```

### SC-326 shape probe (Finding 4)

Values-free field-shape census over `GET /payment-methods` on the same scope — counts only, no
values:

```
payment methods bound (no client-side throw): 20
  firstSixDigits shapes: {'6-digit': 2, 'null': 18}
  bin shapes:            {'6-digit': 2, 'null': 18}
```
