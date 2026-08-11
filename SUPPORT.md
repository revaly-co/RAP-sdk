# Getting help

## Try these first

Most integration questions are answered in three places:

| Question | Go to |
| --- | --- |
| How do I get from an API key to a first charge? | Your language's quickstart — `languages/<language>/README.md` |
| How do I handle this outcome / tune reconcile / test offline? | [`docs/failover-cookbook.md`](docs/failover-cookbook.md) |
| What exactly does the contract guarantee? | [`docs/failover-contract.md`](docs/failover-contract.md) |
| What's the full config and runtime surface? | [`docs/runtime-tdd.md`](docs/runtime-tdd.md) |
| Why is it built this way? | [`docs/architecture.md`](docs/architecture.md) and [`docs/adr/README.md`](docs/adr/README.md) |

Building with an AI coding agent? Point it at [`AGENTS.md`](AGENTS.md) — the whole contract on one
page, including the rules that keep generated integration code correct.

## Choosing a channel

| Your situation | Channel |
| --- | --- |
| The SDK behaves differently than documented | [Bug report](https://github.com/revaly-co/RAP-sdk/issues/new/choose) |
| You want a capability the SDK doesn't have | [Feature request](https://github.com/revaly-co/RAP-sdk/issues/new/choose) |
| You're unsure how to use something | [Question issue](https://github.com/revaly-co/RAP-sdk/issues/new/choose) |
| You found a security vulnerability | **Privately** — [`SECURITY.md`](SECURITY.md) or `security@revaly.co`. Never a public issue |
| It involves your account, a live transaction, real amounts, or real IDs | **Your Revaly account or support contact.** Sensitive context must not land in a public issue |

## What to include in an issue

The more of this you can give, the faster the answer:

- **Language and SDK version** (for example `python revaly-sdk 0.5.1`), plus your language runtime
  version.
- **What you expected and what happened**, in terms of outcome classes and verdicts where relevant
  — "I expected `TransientFailure` and got `OutcomeUnknown`" is worth ten paragraphs.
- **A minimal reproduction**, ideally scripted against the mock transport so it runs with no
  network and no credentials. Recipe 7 of the [cookbook](docs/failover-cookbook.md) shows the
  shape.
- **The correlation ID** from the response or typed error, if a real request was involved. One
  correlation ID plus one `merchantTransactionId` is enough to trace a payment end to end.
- **Values-free logs only.** Please redact everything real: never paste card numbers, CVVs, API
  keys, live IDs, amounts tied to real customers, or personal data. Default-verbosity SDK log
  output is already values-free and safe to share.

## What to expect

Issues are triaged by the maintainers on a response rotation (ADR-SDK-012), and first-response time
is tracked as a developer-experience KPI rather than left to chance.

**Supported versions.** Security fixes land on the latest release of each language SDK while the
SDKs are pre-1.0; at GA this widens to current plus previous minor. Deprecations are announced in
release notes and in registry metadata, every major ships with a migration guide, and a yanked
release is always announced together with its patched replacement in the same notice.

**Versions and provenance.** Every published version's release notes pin the exact spec commit it
was generated from, and each GitHub release artifact carries a `.sha256` checksum and a
`provenance.json` binding it to that source — useful when you need to prove what you installed.
