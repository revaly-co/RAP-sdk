# ADR-SDK-028: Pre-GA idiom ratifications and cross-language coherence corrections

## Status

**Accepted (2026-07-21).** Post-RFC record. Amends **ADR-SDK-016** (Go hand-written layout).
Closes the `[Proposed]` idiom deferrals of the java/go/python/typescript build stories
(dx-contract §a) and the §a "ecosystem's standard linters enforced in CI" clause for those four
languages. The breaking subset ships as the next release cut (**v0.3.0 ×6** — pre-GA, registry
publish embargoed, interim GitHub release artifacts only, ADR-SDK-026).

## Context

The four runtimes built with explicitly deferred idiom choices carried `[Proposed]` markers
awaiting the dx-contract §a bar ("each SDK reads as native to its ecosystem — naming, error
idiom, async model, package layout — with the ecosystem's standard linters enforced in CI").
On 2026-07-21 four independent per-language idiomatic reviews ran against that bar (java: 4
flagged items; go: 5; python: 2; typescript: 1), followed by a cross-language coherence pass
that adversarially re-verified every claim against the tree before adoption. Scope was strictly
the flagged idiom set: registry package names (OQ-3), reconcile-policy defaults (SC-261), the
connect default (OQ-11), and the generated cores (ADR-SDK-001) were out of bounds throughout.

## Decision

### 1. Ratifications (unchanged designs, now [Decided])

- **Java checked exceptions** — the three failure classes stay CHECKED (`RapCoreException` base):
  recoverable conditions with mandatory caller reactions (Effective Java Item 70); compile-time
  forcing of the three-way failover decision is the only mechanism that makes dx-contract §b's
  "handling all three error classes" compiler-enforced; flagship payment-SDK precedent
  (Stripe-java, Square, Adyen) is checked — the unchecked flagships are infrastructure SDKs
  whose callers cannot act on failures, the opposite case.
- **Java interruption → OutcomeUnknown on payment ops** — restore-interrupt-then-translate
  (JCiP §7.1.3; AWS SDK v2 precedent), because interruption proves nothing about whether the
  request was sent; raw `InterruptedException` propagation from `charge()` would invite
  catch-and-failover — the double-charge trap. `reconcile` (side-effect-free read loop)
  correctly propagates raw. Now pinned by test (`InterruptionTests`).
- **Java body-read timeout mechanism** — `HttpRequest.timeout()` per request is the JDK-blessed
  bound; the residual (post-headers body stall) can only under-classify toward OutcomeUnknown,
  never mis-classify. Documentation corrected — see §2.
- **Go `time.Duration` for all bounds**; **pointer-typed error classes dispatched via
  `errors.As`** (the post-1.13 idiom; type-driven dispatch is the Go-native encoding of
  "classify by the algorithm, never message text"); **sealed-interface verdicts with the
  mandatory default branch** (go/ast precedent; non-exhaustive type switches make ADR-SDK-009
  verdict openness native — `SafeToFailover` lands as a compile-compatible minor); **`raptest`
  companion-package name** (httptest/iotest/pstest convention).
- **Go root-package re-export mechanism** — one-import happy path via type ALIASES at the module
  root (Go 1.9 aliases preserve type identity, so `errors.As` targets survive both paths).
  Layout corrected around it — see §2.
- **Python cancellation idiom** — per-call timeout overrides over client defaults, keyword-only;
  sync Python has no cancellation primitive and the SDK refuses to pretend otherwise (requests/
  httpx/boto3 shape; urllib3's own `Timeout(connect=, total=)` vocabulary). Deadline expiry
  after send is an OutcomeUnknown payment outcome, not a cancellation.
- **Python TLS conservatism** — only `ssl.SSLCertVerificationError` (chain-inspected) is
  phase-provable never-sent ⇒ TransientFailure; any other `SSLError` ⇒ OutcomeUnknown. urllib3
  puts TLS phase only in message strings, which the failover contract forbids reading; the
  deliberate divergence from java/TS (whose stacks CAN prove the phase) is the contract's
  per-stack-provability design, php errno-28 precedent.
- **TypeScript: no `connectTimeout` key** — WHATWG fetch cannot bound the connect phase; an
  SDK-emulated bound could never carry never-sent proof (strictly worse classification), and a
  silently-unhonored key is a lie. The `dispatcher` passthrough is the openai-node shape;
  aws-sdk-js-v3 ships connect knobs only on transports that can honor them. undici's distinctly
  typed `UND_ERR_CONNECT_TIMEOUT` already classifies TransientFailure.
- **Java spotless + google-java-format** ratified as the formatter (previously `[Proposed]` in
  pom/pipeline comments).

### 2. Adopted corrections (this change set; breaking subset → v0.3.0)

**Breaking (batched deliberately into ONE pre-GA break):**

- TS verdict discriminants → PascalCase (`'Found' | 'NotFoundYet' | 'ReconcileVerdictExtension'`):
  `failure.kind`, the outcome tokens, and the reconciler's own log literals were already
  PascalCase and cross-language log-join-locked; the API now matches the fleet vocabulary.
  Log output verified byte-identical (literals were already right).
- Go layout fence (ADR-SDK-016 amendment): `runtime/` → `internal/runtime/` (compiler-enforced
  fence — the importable `runtime/` was a second frozen public API surface and shadowed the std
  lib package name), mock lifted OUT of internals to `languages/go/raptest/` (httptest-shape
  placement; the merchant-importable test companion cannot live under `internal/`).
- Go payment ops take pointer requests (`*core.PaymentRequest` …) with a plain-error nil guard —
  stripe-go/aws-sdk-go-v2 shape; kills the quickstart's leading-deref wart.
- Go `Config.Wire` → `Config.Transport` — runtime-tdd §1 names the cross-language key
  `transport` and the other five languages all use it (verified 5-of-5); `Transport` is also
  the std lib vocabulary. The `WireTrace` hook family keeps its name (distinct §6 concept).
- Java `RapRequestDecorator.userAgent()` → `getUserAgent()` (JavaBeans consistency).

**Non-breaking:**

- Go `var`-bound constructor/Ptr re-exports → thin forwarding functions (immutable, godoc
  signatures render); type aliases unchanged. Accepted trade-off: a regen changing a core ctor
  signature now breaks the build loudly instead of silently tracking — the right default for a
  payments SDK.
- Java `ReconcilePolicy.builder()` (three adjacent same-typed `Duration` ctor params forced
  comment-labeled args in the quickstart). SHAPE ONLY: `build()` delegates to the existing
  4-arg ctor — validation identical, zero new defaults (SC-261 untouched). Ctors kept.
- Java `rootException()` inlined (3 call sites; the name promised unwrapping that never
  happened), intent comment hoisted to `classifyTransportFailure` javadoc.
- Java interruption pinning test added (see §1).
- TS `RapDispatcherLike` structural type replaces `dispatcher?: unknown` (undici `Agent`
  satisfies it structurally; catches passing an options object; no undici types leak).
- TS `{@link}` targets imported type-only so editor/typedoc links resolve.
- Python `py.typed` ×2 wired (runtime marker created; `[tool.setuptools.package-data]` declares
  BOTH markers — the core's existing marker was silently dropped from wheels), `__all__`
  (static 33-name runtime surface + dynamic extension with the core models so the §2
  one-package surface never shrinks), `__version__ = SDK_VERSION`, and a PEP 544
  `RapWire` Protocol typing the wire seam (`transport=`/`wire=` were `Optional[Any]`;
  mock unaffected — Protocols are structural). `RapWire` deliberately keeps the python-local
  name (coherent with `RapWireRequest`/`RapWireResponse`); the cross-language contract is the
  config KEY `transport`, not type names.

**Documentation corrections:**

- Java deadline caveat (README Timeouts + javadoc): the deadline bounds time-to-response per
  `HttpRequest.timeout()` semantics (through response headers); a post-headers body stall is
  not bounded by it and surfaces as OutcomeUnknown when the connection dies; a hard wall-clock
  bound belongs in the merchant's execution layer — expiry = OutcomeUnknown → reconcile, never
  resubmit.
- Python per-call deadline `None` asymmetry made explicit (README + docstring): per-call
  `None`/omitted = inherit the client value; DISABLING is a client-construction decision only.
  Deliberately no per-call disable sentinel — the safe direction.
- Copy-block deadline hygiene: the TS dispatcher recipe dropped its unannotated
  `overallDeadlineMs: 10_000` and the Go quickstart dropped its `OverallDeadline: 30s` — 10 s
  sits INSIDE the telemetry-observed 20–26.5 s gateway stall cluster ADR-SDK-027's 75 s default
  was ratified to clear; quickstart copy blocks never silently undercut a ratified default.
- Go README: stale "no release tags yet" note corrected (go/v0.1.0 + go/v0.2.0 shipped
  2026-07-20); supported-floor sentence added (§5).

### 3. Linter-clause closures (dx-contract §a; CI-only; hand-written surfaces, never `core/`)

| Language | Tooling (pinned) | Wiring |
| --- | --- | --- |
| Java | **Error Prone 2.50.0** (default ERROR checks) + spotless/google-java-format | annotationProcessorPaths + forked-compiler jvmArgs in runtime/tests/smoke poms — NOT `.mvn/jvm.config`, which CI's repo-root `mvn -f` invocation would silently not load; rides every `mvn test` compile |
| TypeScript | **eslint 10.7.0 + typescript-eslint 8.65.0** (recommendedTypeChecked; `no-floating-promises` et al. — an unawaited `charge()` swallows the failure classification) | flat config, `core/` globally ignored; toolchain lockfile-isolated in `languages/typescript/lint/` because the native tsc 7.x compiler exposes no JS API for the linter (peer range `<6.1`); typescript 6.0.3 serves as the linter's type engine only — build/typecheck stay on native 7.x. Same isolated-toolchain pattern as `pipeline/typescript/compile-check/` |
| Python | **ruff 0.15.22** (`check` + `format --check`) | `RUFF_VERSION` env pin in `pipeline.yml` (REDOCLY pattern); `[tool.ruff]` in `languages/python/pyproject.toml`; one-time format normalization landed with this change |
| Go | **staticcheck v0.7.0** (+ existing gofmt, go vet) | `STATICCHECK_VERSION` env pin; hand-written packages only. Adopted NOW (not deferred): the §a bar this ADR sets — formatter + pinned real static analyzer per language — must not vary by reviewer strictness |

Zero suppressions were needed in safety-contract code across all four languages (TS carries five
narrow `prefer-promise-reject-errors` disables where the failover contract REQUIRES verbatim
abort-reason propagation, each with a justification comment; one WARNING-severity Error Prone
finding is deliberately retained in a java regeneration probe).

### 4. OQ-11 forward-compatibility note (TypeScript connect default)

A future OQ-11-ratified connect default is absorbed at **documentation level** (the README
dispatcher recipe gains the number; undici's own 10 s connect default bounds Node merchants
today). A code-level enforced default would require an optional/peer undici dependency — a
dependency-policy revision needing its own ADR note; it is deliberately NOT promised here.
Constraint for OQ-11: any ratified connect default stays below the 75 s overall deadline
(ADR-SDK-027) — otherwise the phase-blind overall deadline fires first during connect and
classifies OutcomeUnknown where the connect bound would have proven TransientFailure.

### 5. Go toolchain floor

`go 1.21` retained. The floor's entire cost is two tiny shims (`discardHandler` pre-1.24;
legacy `math/rand` jitter pre-1.22, auto-seeded since 1.20 and statistically irrelevant to
±20 % jitter); against that, payment-SDK merchants skew toward pinned corporate toolchains
where a raised directive is a hard build failure (stripe-go's conservative floors are the
product-class precedent). Policy: the floor rides Go's official support window, re-evaluated
at the Go GA gate; at ≥1.24 delete the shim and migrate jitter to `math/rand/v2`.

### 6. dotnet / php boundary

Neither carried flagged `[Proposed]` idiom items, and this ADR changes nothing in either.
Absence of flagged items is NOT §a sign-off: the full per-language GA checklist signed off by
an experienced developer in that language (dx-contract §a acceptance) remains a GA-gate
activity for all six languages, dotnet and php included. New checklist item from this pass:
verify and document per-language overall-deadline semantics caveats (python's per-read timeout
component, php, dotnet) mirroring the Java caveat of §2.

### 7. Explicit non-decisions (unchanged, with owners)

- Registry package names remain **[Proposed]** until OQ-3 provisioning (runtime-tdd §7).
- Reconcile-policy defaults remain explicit-only pending SC-261 telemetry (the Java builder
  adds shape, no values).
- Connect-timeout defaults remain absent in all six languages pending OQ-11.
- The error-code taxonomy remains open (OQ-2); `code` stays an open string everywhere.

## Consequences

- One coordinated pre-GA break (v0.3.0 ×6) instead of four dribbled ones; migration notes go in
  the release notes (dx-contract §e discipline applied early). Breaking set: TS verdict
  discriminants, Go raptest import path + pointer params + `Transport` field, Java accessor.
  The design-partner beta (§f) starts on the post-028 surface.
- The cross-language vocabulary (PascalCase classes/verdicts/outcomes, the `transport` config
  key) now holds across all six languages, API and logs alike.
- Go merchants lose direct `runtime/` imports (compile-enforced); the root package is the
  supported surface; `raptest` import path changes once. ADR-SDK-016's layout diagram carries a
  dated amendment pointing here.
- §a linter bar is uniform across the four reviewed languages: formatter + pinned static
  analyzer, hand-written code only, generated cores never linted (ADR-SDK-001). dotnet
  (`dotnet format`) and php (manifest/lint/PSR-4 checks) are assessed at their GA checklists.
- Verification at adoption: java 79 tests (was 75), python 138, typescript 115, go full gate
  set (build/vet/test/gofmt/staticcheck) — all green with the new linters active; TS reconciler
  log output byte-identical across the rename; python wheel proven to carry both `py.typed`
  markers.
- No OQ advanced or decided; `open-items.md` unchanged by this ADR.
