# Contributing to the Revaly RAP SDK

Thanks for being here. This repository is a payment-path client library in six languages, so the
contribution rules are tighter than most — and they're all written down, so nothing is a surprise
at review time.

**Start with [`AGENTS.md`](AGENTS.md)** for the contract in one page, and
[`docs/README.md`](docs/README.md) for the full reading order.

## Where to put what

| You want to | Do this |
| --- | --- |
| Report a bug | [Open a bug report](https://github.com/revaly-co/RAP-sdk/issues/new/choose) — include language, version, and a minimal repro against the mock transport if you can |
| Ask a question about integrating | Start with your language's quickstart and the [failover cookbook](docs/failover-cookbook.md), then [open a question issue](https://github.com/revaly-co/RAP-sdk/issues/new/choose). See [`SUPPORT.md`](SUPPORT.md) |
| Report a vulnerability | [`SECURITY.md`](SECURITY.md) or `security@revaly.co` — privately, never a public issue |
| Raise anything about a live payment, amount, or account | Your Revaly account contact. Sensitive context does not belong in a public issue |
| Propose a change | Read the six ground rules below, then open a PR |

## What lives where

```
spec/                       pinned gated spec artifact reference + checksums
languages/<lang>/core/      GENERATED — never hand-edited
languages/<lang>/runtime/   hand-written product code (Go: revaly.go, internal/runtime/, raptest/)
languages/<lang>/tests/     unit + contract tests
pipeline/                   generation configs, templates, publish workflows
docs/                       ADRs and design docs — the source of truth
```

The split matters: the generated core is spec-derived plumbing, and the hand-written runtime is
the product. Almost every contribution belongs in `runtime/`, `tests/`, or `docs/`.

## The six ground rules

These are enforced by CI, by branch protection, and by the PR checklist. A change that breaks one
fails rather than merges.

**1. Generated code changes only by regeneration.** `languages/*/core/` is generator output
(ADR-SDK-001). It changes exclusively by regenerating against a newly pinned spec artifact, and CI
runs a regeneration-diff check that fails on a one-byte difference. If the generated core is wrong,
the fix is a spec correction or a generator-template change (an ADR revision, per ADR-SDK-023) —
never a hand edit.

**2. Spec input is a pinned, gated artifact.** Generation consumes a `spec/v*` release tag from the
platform repository, verified against its `.sha256` and `provenance.json`, with the pin recorded in
`spec/` (ADR-SDK-006). Never generate from a branch checkout, a URL, or a locally edited spec.

**3. The safety contract is normative.** Failure classification follows the algorithm in
[`docs/failover-contract.md`](docs/failover-contract.md) §2 — status and `code` only, `code` and
`transactionType` as open strings, unrecognized values handled as absent and landing on
`OutcomeUnknown`. No retries, no resubmission, no circuit breaker, no cross-request state; the
caller-bounded reconcile re-poll is the only loop. Every example that switches on a verdict or a
code keeps its default branch. Changing any of this requires an ADR revision, not a code choice.

**4. Logging stays values-free.** No payload values at default verbosity; debug level scrubs PAN,
CVV and PII; API keys appear in neither logs nor exception messages (ADR-SDK-020). Scrubbing goes
through the single central allowlist function per runtime, and each language ships log-capture tests
asserting it. Tests, fixtures and mock transports use synthetic data only.

**5. Publishing goes through the pipeline.** The one human act is a per-language release tag on
`main`; the stage-6 job publishes from the protected `publish` environment (ADR-SDK-013). Never
publish, re-publish, or yank out of band, and never mint registry credentials outside the custody
records in [`docs/registry-provisioning.md`](docs/registry-provisioning.md). A failed release is
fixed and re-tagged, never resumed by re-running build stages.

**6. Open items have owners.** Questions tracked in [`docs/open-items.md`](docs/open-items.md) are
not settled by a PR. Where code needs an undecided answer, leave an explicit marker referencing the
OQ.

## Making a change

1. **Branch** off `main`. `main` is protected and takes PR merges only.
2. **Match the neighbours.** Each SDK reads as native to its ecosystem (DX contract §a) — naming,
   error idiom, async model, package layout — with that ecosystem's standard linters enforced in CI.
3. **Test in the affected language(s).** New runtime behaviour needs unit tests; anything touching
   classification needs a mock-transport test per taxonomy row it affects.
4. **Keep six languages in step.** Behaviour is a cross-language contract. A change to
   classification, the reconcile surface, config defaults, or logging lands in all six languages or
   in none — a one-language fix to shared behaviour is an inconsistency bug in the making.
5. **Update the docs in the same PR.** Surface changes update the language quickstart and, where
   relevant, [`docs/runtime-tdd.md`](docs/runtime-tdd.md). Decisions become a numbered ADR in
   `docs/adr/` (Title / Status / Context / Decision / Consequences), and status changes are dated
   edits to `docs/README.md` § Status snapshot and `docs/open-items.md` — keep both current.
6. **Name the commit.** Conventional commits: `feat(dotnet): …`, `fix(go): …`, `docs: …`,
   `chore(ci): …`.
7. **Open the PR** and fill in the checklist. CODEOWNERS routes review automatically.

## What CI checks

Stages 1–3 run on every PR: spec-artifact validation, six-language generation with the
regeneration-diff check, then build and unit tests per language. The contract smoke (stage 4) runs
on release tags, on the nightly schedule, and on manual dispatch — not on plain PRs
(ADR-SDK-024). Packaging and publishing (stages 5–6) run only from release tags on `main`.

**Any language red blocks the release for all six.** That's the point: one behaviour across six
languages is a promise the pipeline keeps, not a review convention.

Stage 3 also reports test coverage per language, scoped to the hand-written runtime — the
generated core is excluded, since the regeneration diff and the contract smoke are what prove it
(`docs/pipeline-and-release.md` §2.1). No threshold gates the build, so treat the number as review
signal: if your PR moves it down, say why in the description.

Running it locally:

| Language | Command (from the language directory) |
| --- | --- |
| dotnet | `dotnet test Revaly.Sdk.slnx -c Release --collect:"XPlat Code Coverage" --settings coverlet.runsettings` |
| java | `mvn -B -ntp -f pom.xml test` (writes `tests/target/site/jacoco-aggregate/`) |
| php | `vendor/bin/phpunit --coverage-text` (needs pcov or xdebug) |
| typescript | `npm run test:coverage` |
| python | `python -m coverage run --source=revaly_sdk -m pytest tests && python -m coverage report` |
| go | `go test ./tests/... -coverpkg=./,./internal/runtime,./raptest -coverprofile=cover.out && go tool cover -func=cover.out` |

## House style

- Terminal commands in docs are single-line, copy-pasteable — no backslash continuations.
- .NET code carries no `#region` / `#endregion` directives.
- Every generated file keeps its generated-code banner.
- Docs speak in terms of what the SDK does and guarantees. Where a boundary matters, state it as a
  guarantee ("each charge is sent exactly once") rather than an absence.

## Code of conduct

Be decent to each other: assume good faith, keep review about the code, and remember that the
person on the other end is trying to ship a payment integration too. Conduct concerns go to
`security@revaly.co`, which reaches the maintainers privately.
