# Revaly RAP SDK (`rap-sdk`)

Server-side SDKs for the **RAP V2 API** (RAP-core) in six languages — **.NET, Java, PHP,
TypeScript, Python, Go** — built around one promise: **you never have to guess what happened
to a payment.**

Every SDK ships the same merchant-facing **failover & reconciliation contract**: every failed
call is classified into exactly one of three typed outcomes that tell you what you may safely
do next, and an ambiguous outcome comes with the tool to resolve it. One monorepo, one
deterministic generation pipeline consuming only cryptographically gated API specifications,
one behavior across all six languages.

## The contract in thirty seconds

A failed charge does **not** mean the payment didn't happen. Blind-failing-over to your own
gateway on an ambiguous failure can charge the cardholder **twice**. So the SDKs never hand
you a raw error — they hand you a verdict:

| You get | It means | You do |
| --- | --- | --- |
| **PermanentRejection** | Received and rejected (400/401/403/404/422) | Fix or decline. **Never fail over** — the same request fails anywhere. |
| **TransientFailure** | **Definitively not processed** (provably never sent, or `503` + `code: not_processed`) | Route to your own gateway immediately. |
| **OutcomeUnknown** | **May have been processed** (timeout after send, connection reset, ambiguous 5xx) | **Reconcile before acting** — never guess. |

Each language expresses this in its native idiom — exceptions in .NET/Java/PHP/Python, typed
classes in TypeScript, error values in Go — but the classification algorithm is identical and
normative ([`docs/failover-contract.md`](docs/failover-contract.md)).

## What it looks like

TypeScript shown; the same flow, in your language's idiom, is the first thing in every
quickstart below.

```ts
import { RapClient, RapOutcomeUnknown, RapPermanentRejection, RapTransientFailure } from '@revaly/sdk';

const client = new RapClient({ apiKey: process.env.RAP_API_KEY! });

try {
    const transaction = await client.charge({
        amount: 1999,
        currency: 'USD',
        merchantTransactionId: 'order-1042', // your reconcile handle — required on every payment
        orderId: 'order-1042',
        paymentMethod: {
            fullName: 'Ada Lovelace',
            email: 'ada@example.com',
            creditCard: { number: '4111111111111111', cardVerificationCode: '999', expiryMonth: '12', expiryYear: '2030' },
        },
    });
    console.log('approved', transaction.transactionId);
} catch (failure) {
    if (failure instanceof RapPermanentRejection) {
        // Received and rejected. Fix or decline — never fail over.
    } else if (failure instanceof RapTransientFailure) {
        // Definitively not processed — route to your own gateway immediately.
    } else if (failure instanceof RapOutcomeUnknown) {
        // May have been processed — reconcile BEFORE acting (double-charge hazard).
        const verdict = await client.reconcile('order-1042', {
            maxAttempts: 5,
            overallBudgetMs: 30_000,
            initialDelayMs: 500,
        });
        if (verdict.kind === 'Found') {
            // The record IS visible — Found(Approved) means the money moved;
            // failing over now would double-charge.
        } else if (verdict.kind === 'NotFoundYet') {
            // Not visible YET — absence is not provable. Hold, per your risk policy.
        } else {
            // Verdicts are open for extension — always keep this branch.
        }
    } else {
        throw failure; // not a payment outcome (cancellation, validation, bugs)
    }
}
```

Payments are the safety-critical path, but the full API surface is covered: payment methods,
transactions, and notify.

## Pick your language

Each quickstart takes a sandbox API key to a first classified charge in **under 15 minutes**,
and every example ships all three outcome classes plus the reconcile loop — the safety path
is never an exercise for the reader.

| Language | Quickstart | Package (final name) |
| --- | --- | --- |
| .NET | [`languages/dotnet`](languages/dotnet/README.md) | `Revaly.Sdk` (NuGet) |
| Java | [`languages/java`](languages/java/README.md) | `co.revaly:revaly-sdk` (Maven Central) |
| PHP | [`languages/php`](languages/php/README.md) | `revaly/sdk` (Packagist) |
| TypeScript | [`languages/typescript`](languages/typescript/README.md) | `@revaly/sdk` (npm) |
| Python | [`languages/python`](languages/python/README.md) | `revaly-sdk` (PyPI) |
| Go | [`languages/go`](languages/go/README.md) | `github.com/revaly-co/rap-sdk/languages/go` |

**Installing:** install from the registries above — they are the primary, documented
install path. Per-language
[GitHub release artifacts](https://github.com/revaly-co/RAP-sdk/releases) continue with
every version — each asset comes with a `.sha256` checksum and a `provenance.json`
binding it to the exact source and spec it was built from — as the provenance anchor
and registry-outage fallback (ADR-SDK-031). There is no separate sandbox host: your API
key's scope selects sandbox or live on the same URL.

## What these SDKs never do — deliberately

The absence of magic is the feature. In a payments client, silent cleverness is where double
charges come from:

- **No automatic retries, no resubmission, no circuit breakers.** A charge is sent exactly
  once; retry policy belongs to you, with the classification to make it safe.
- **No cross-request state.** Every call stands alone; the caller-bounded reconcile re-poll
  is the only loop in the product.
- **No guessing.** Error codes and transaction types are open sets — an unrecognized code is
  treated as *unknown outcome*, never coerced toward "safe". If the transport cannot prove a
  request was never sent, the SDK says so.
- **No payload values in logs.** Logging is values-free by design (PCI scope): identifiers,
  statuses, classes and correlation IDs — never card data, never keys, never hosts. A
  wire-trace hook exists for your own structured observability.
- **No hand-written API bindings.** The generated core is produced deterministically from a
  pinned, checksum-verified spec artifact and never edited by hand — CI fails the build on a
  one-byte drift between the committed core and a clean regeneration.

## How a release is proven

Every release tag runs the full gauntlet: spec-artifact re-verification, six-language
regeneration diff, build + unit tests per language, and a **live contract smoke** that
exercises the failover taxonomy — including a fault-injected `503 + not_processed` and
reconcile verdicts — against real infrastructure, twice, in every language. Any language red
blocks the release for all six. Each published version's release notes pin the exact spec
commit it was generated from.

Versioning is semver per package, with per-language tags (`typescript/v0.5.0`); a mock
transport ships in every SDK so your failover handler is testable without network
(see each quickstart's "testing your failover handler" section).

## Documentation

The design record is public and complete — the docs are the source of truth, not an
afterthought:

- [`docs/README.md`](docs/README.md) — index and reading order
- [`docs/failover-contract.md`](docs/failover-contract.md) — the normative safety contract
- [`docs/runtime-tdd.md`](docs/runtime-tdd.md) — the per-language runtime surface
- [`docs/dx-contract.md`](docs/dx-contract.md) — the developer-experience bar each SDK meets
- [`docs/adr/README.md`](docs/adr/README.md) — every architectural decision, numbered and dated

## Security

Please report vulnerabilities via [`SECURITY.md`](SECURITY.md) or `security@revaly.co` —
not via public issues. Test suites and mock transports use synthetic data only.

## Status

Pre-1.0: the API surface is stable in shape but may still evolve in idiom until GA
(per-language release notes call out any breaking change). Current distribution is GitHub
release artifacts; registry publishing follows once the release gates close.

## License

[Apache-2.0](LICENSE) · [NOTICE](NOTICE)
