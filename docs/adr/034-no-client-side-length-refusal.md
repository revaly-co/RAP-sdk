# ADR-SDK-034 — An SDK does not refuse a request for a string length bound; the platform decides (OQ-18)

**Status:** Accepted — decided 2026-11-05 by Dimitri Pankov as RAP SDK author (OQ-18, raised on
PR #118 by the fresh-context review of 2026-11-03, SC-869) · closes OQ-18 · no failover-contract
change: a request the SDK no longer refuses is sent and classified like any other request
**Source:** spec pins v2.15.0+693a36b (SC-869: the 256-character `description` bound from SC-785)
and v2.16.0+99cb098 (SC-661: the 45-character `customerIp` bound)
**Owner:** SC Eng
**Safety-critical:** no — a client-side length refusal happens before anything is sent, and the
platform's own answer to an over-long value (truncation, or a 400) is already classified by
`failover-contract.md` §2

## Context

The spec declares a `maxLength` on many request strings. For some of them the platform does not
refuse a longer value:

- `description` on charge and authorize is bounded at 256 characters since spec v2.13.1 (SC-785).
  The spec states that a longer value is truncated to its first 256 characters and never blocks
  the payment.
- `customerIp` on charge and authorize is bounded at 45 characters since spec v2.16.0 (SC-661).
  The platform's handling depends on the route today: Olympus declines a value over 45
  characters (code 50037), the direct path accepts up to 50, and Backbone's own contract check
  records the bound without refusing while a 30-day census runs (2026-11-04 to 2026-12-04).

The six generated cores treat the same bound differently:

| Core | What happens to a value over `maxLength` |
| --- | --- |
| Python | Refused when the model is built or a field is assigned (pydantic `max_length`); nothing is sent |
| PHP | Refused in the field's setter (`InvalidArgumentException`); the array constructor does not check and nothing calls `valid()` |
| .NET | Sent: the model implements `IValidatableObject`, but nothing in the core or runtime calls `Validate` |
| Java, TypeScript, Go | Sent: no length check is generated on model fields |

Path parameters are a separate case: Go, Python and PHP check a path parameter's `maxLength` in
the API layer (for example `transactionId` at 50 and `merchantTransactionId` at 100 on capture,
void, refund and refund-cancel); .NET, Java and TypeScript do not.

So a request with a 300-character description is refused before sending in two SDKs and
accepted, truncated, in four. After the v2.16.0 pin, a 46-character `customerIp` would be
refused by Python and PHP before sending, while the direct path accepts it. The SC-661 change
(Backbone PR #439) asked that RAP-sdk not re-pin to 2.16.0 with the client-side 45-character
limit until the field's census closes.

OQ-18 asked (a) whether the Python and PHP refusal is acceptable or the platform should drop
`maxLength` from the spec, and (b) which version the next release takes.

## Decision

1. **No client-side length refusal.** An SDK does not refuse a request before sending because a
   string is longer than a `maxLength` the spec declares. The platform is the single authority:
   it truncates, records or refuses, and a refusal comes back as the platform's own response,
   classified by the failover contract as today.
2. **Scope: `maxLength` on request body fields only.** Path-parameter checks (Go, Python and
   PHP), required fields, patterns, enum values, numeric ranges and `minLength` keep their
   generated checks; this ADR does not change them.
   The spec keeps its bounds: they document the contract, and asking the platform to drop
   them (OQ-18's alternative) is not pursued.
3. **Implementation: a Python and PHP template revision** (SC-886; ADR-SDK-023, like the `oneOf` forks)
   that stops emitting the `maxLength` check, with a test per language proving a value over the
   bound is sent. Python's `test_merchant_transaction_id_max_length_100` asserts today's
   refusal and changes with the revision. The unused .NET `Validate` stays as generated.
4. **Release gate until the revision lands.** Python and PHP are not released from a pin that
   adds or tightens a `maxLength` the platform does not enforce. The v2.16.0 release therefore
   ships .NET, Java, TypeScript and Go only; Python and PHP release with the template revision.
   This relaxes the SC-661 request above: the re-pin lands on `main` with the 45-character check
   in the unreleased Python and PHP cores, and this gate keeps it out of every published package
   (decided by Dimitri Pankov, SC-661 owner, 2026-11-05).
5. **Versions (OQ-18 b): a minor bump per package.** .NET, Java, TypeScript and Go go from 0.8.0
   to 0.9.0 with the v2.16.0 pin. With the template revision, Python goes from 0.8.0 to 0.9.0 and
   PHP from 0.9.1 to 0.10.0. The SDKs are pre-1.0 and the major tracks the RAP V2 API major
   (`pipeline-and-release.md` §4); the platform's breaking-change gate allowlisted the tightened
   `description` bound and reported the `customerIp` bound as a warning, not an error; the
   `merchantTrustLevel` reorder keeps source compatibility and breaks binary
   compatibility in .NET only. Precedent: v0.8.0 (ADR-SDK-033). The classification rationale is
   recorded in each annotated release tag.
6. **Release notes.** The .NET note states the `merchantTrustLevel` renumbering: `NOTTRUSTED`
   moves from 2 to 4, 2 now means `MODERATELYTRUSTED`, and the `UnknownDefaultOpenApi` sentinel
   moves from 4 to 5 (so a stored 4 now reads as `NOTTRUSTED`); recompiled code is unaffected, while
   code compiled against an earlier core, or a stored integer, sends the wrong level. Every note
   describes the bounds as the spec states them (a `description` over 256 characters is
   truncated to its first 256 and never blocks the payment; `customerIp` is IPv4 or IPv6 text of
   at most 45 characters) and does not describe platform enforcement plans.

## Consequences

- Once the revision lands, a request body behaves the same in all six SDKs: it is sent, and the
  platform decides. Path parameters keep their per-language checks.
- A merchant learns of an over-long value from the platform: a truncated `description` is
  silent by the platform's contract, and an enforced bound comes back as the platform's refusal.
- A future pin that adds or tightens a `maxLength` needs no per-language decision once the
  revision lands. Until then, decision 4 applies to every pin.
- Python and PHP are one release behind until the revision ships; their next release carries
  every pin change since v2.13.0.
- No released package refuses a longer `customerIp` before sending, which is what the SC-661
  request protects; `main` carries the check in the unreleased Python and PHP cores until the
  revision.
