# `spec/` — Pinned Gated Spec Artifact (ADR-SDK-006)

The SDK pipeline consumes **exactly one spec input**: the platform release referenced in
[`pin.yaml`](pin.yaml). The bundle itself is deliberately not committed — pipeline stage 1
downloads it from the pinned release tag and verifies it against the committed checksums
before anything downstream runs (`../docs/pipeline-and-release.md` §2).

## Current pin

| Field | Value |
| --- | --- |
| Release | [`spec/v2.19.0+ec71a82`](https://github.com/revaly-co/Backbone/releases/tag/spec%2Fv2.19.0%2Bec71a82) (platform repo) |
| Spec version | 2.19.0 |
| Source commit | `ec71a824de502d4d1cdb1cef1b5ff34e1d9f428c` |
| Gates | lint ✅ · bundle ✅ · breaking allowlisted (two spec-accuracy entries) · contract suite ✅ (see [`provenance.json`](provenance.json)) |
| sha256 (`openapi.bundled.yaml`) | `43f47ef26d5696173c8bb5b0e5e9ef251cbc6975599e26a4fd1071b4ca5e84a1` |
| Pinned | 2026-11-25 |

Pin history: `v2.1.2+9af661b` (2026-07-14, first pin — int64 `maximum` fix, Backbone PR #241)
→ `v2.1.3+e75c71a` (2026-07-15 — orphan `PaymentMethodRequest` schema dropped, Backbone PR #242)
→ `v2.2.0+1e59620` (2026-07-16 — additive `statementDescriptor` on charge request/response,
Backbone STR-108 / PR #228) → `v2.2.1+c4000e9` (2026-07-16 — `X-Correlation-ID` response
header documented on every response, Backbone PR #247) → `v2.3.0+80cc897` (2026-07-20 —
spec-vs-reality alignment: `paymentMethodType` inference documented, per-type required fields
on `PaymentMethod`, `error`-only 400 bodies documented, ≤48-char reference-id guidance,
Backbone ADR 020 / PR #251) → `v2.4.0+4ce73e2` (2026-08-27 — nested `vaultToken` on
charge/authorize response payment methods, transaction-lookup unions `oneOf` → `anyOf` with
documented discriminators, 404 documented on charge/authorize, SC-478) → `v2.6.0+abf71b6`
(2026-09-01 — flat `vaultToken` on `TransactionListItem`, nested `vaultToken` extended to the
transaction reads, `recordRefund` documented for gateway-routed transactions) →
`v2.7.0+7a05e7b` (2026-10-01 — `bypassPlatform` on charge/authorize deprecated: `true` is now
refused with 404 before any processor; no shape change) → `v2.12.2+cec0b33` (2026-10-19 —
seven platform artifacts in one bump: `recordRefund` 422 for a never-approved transaction
documented (SC-636); returned-expiry prose (SC-640); `expiryUpdated` / `cardReplaced` on the
charge/authorize response payment method (SC-653); previous-transaction echo fields widened
to 1,024 and `paymentReferenceData` documented as the base64 reference Revaly returned
(SC-659); optional 3DS `context` block (STR-262, RFC-068); the `context.acceptHeader` example
no longer carries `*/`, which closed the .NET core's generated doc comment (SC-660, Backbone
PR #388); `context` / `context.channel` prose states how Backbone records the channel
(STR-258, Backbone PRs #367 / #391); no error-code, verdict or enum change) →
`v2.13.0+98915d8` (2026-10-19 — the SC-660 AC1 prose, Backbone PR #392: the `ErrorResponse`
`details` description documents the edge firewall's 403 block body (`details.edgeRejection`
equal to the JSON boolean `true` means the request never reached the platform and its
`merchantTransactionId` was not consumed; `details.reference` is the edge tracking reference;
the body is served as `text/html`, so every 403 body is parsed as JSON; the match is on the
marker, never on the `error` sentence; a 403 without the marker is final) and carries the
per-operation instruction; `code` stays documented as absent on every 4xx, the edge 403
included; the 403 and 409 descriptions gain the matching prose. `details` stays typeless; no
shape, bound, enum, status or error-code change; the bundle differs from v2.12.2 in exactly
five lines. This is the pin that ADR-SDK-033 Decision 9 requires before the minor release of
all six packages) → `v2.15.0+693a36b` (2026-11-03, SC-869 — four platform artifacts in one
bump, all on the charge and authorize requests and the `RtnData` schema: `description` on
`PaymentRequest` / `AuthorizeRequest` bounded at 256 characters instead of 500, with prose
that a longer value is truncated and never blocks the payment (SC-785, Backbone PR #419; the
Python core and the PHP setter enforce the bound in the client, so they now refuse 257 to 500
characters before sending, see OQ-18); `merchantTrustLevel` gains `MODERATELY_TRUSTED` with
`NOT_TRUSTED` moved to the end, which renumbers the implicit .NET enum values,
`merchantTrustData` is redefined as the trusted signal code and `acquirerMerchantId` is stated
optional (SC-837, PR #427); prose on `merchantName` and `merchantData` (SC-846, PR #433); the
optional
`rtnData.additionalTransactionData.fraudPreventionPlatform`, without which Revaly does not
submit RTN data (SC-867, PR #442); no response shape, error-code, verdict or status change)
→ `v2.16.0+99cb098` (2026-11-05, SC-661 — Backbone PR #439, five lines on three request
schemas: `customerIp` on `PaymentRequest` / `AuthorizeRequest` gains `maxLength: 45` with prose
naming IPv4 or IPv6 text, and `merchantTransactionId` on `RefundCancelRequest` rises from 50 to
100 characters; Backbone's contract check records a longer `customerIp` without refusing it
while its census runs, Olympus already declines one over 45 characters (50037), and the direct
path accepts up to 50. The Python core and the PHP setters refused a longer `customerIp` before
sending, so under ADR-SDK-034 (OQ-18) Python and PHP waited for their template revision
(SC-886, RAP-sdk PR #121); all six released from this pin on 2026-11-05, .NET, Java,
TypeScript, Go and Python at 0.9.0 and PHP at 0.10.0; no response shape, error-code, verdict or
status change) → `v2.18.0+834f684` (2026-11-21, SC-934 — three platform artifacts in one bump;
the bundle differs from v2.16.0 in four changed and 17 added lines: the `expiryMonth`,
`expiryYear` and `cardReplaced` descriptions name Worldpay Litle V11 and Adyen as real-time
account updaters (v2.16.1, SC-842, Backbone PR #474; prose only); the optional response field
`gatewayResponsePayload` on `TransactionResponse`, the processing gateway's own answer as one
JSON document in a string, reduced to the keys the platform lists for that gateway with a
card-number-shaped value masked, present only on a payment, capture, void or refund sent
directly to the gateway for an API key with the payload switched on (v2.17.0, EI-113, Backbone
PR #477); the optional, nullable `transactionLinkId` (Mastercard Transaction Link ID) on the
`StoredCredential` block of `PaymentRequest` / `AuthorizeRequest`, bounded at 22 characters,
and on the `StoredCredentialResponse` block of `TransactionResponse` (v2.18.0, SC-934, Backbone
PR #495). No SDK refuses a longer `transactionLinkId` before sending (ADR-SDK-034), so its
release gate holds no language back from this pin; both response fields are additive; no
error-code, verdict or status change; released 2026-11-23 as v0.10.0, PHP v0.11.0) →
`v2.19.0+ec71a82` (2026-11-25, SC-409 — Backbone PR #512, the remainder of the SC-408
spec-drift audit; the bundle loses 25 lines and gains 261: each `listTransactions` item is now
a `oneOf` of the flat `TransactionListItem`, which gains `required: [transactionId]`, and the
new `TransactionListPaymentMethodItem`, a detailed payment-method operation whose fields are
wrapped in `transaction` and whose payment method is the new flat `TransactionListPaymentMethod`;
the generator emits the union as `ListTransactions200ResponseInner`, so the `listTransactions`
return type changes in all six SDKs; `CreatePaymentMethodRequest.paymentMethod` becomes required
(the platform already answered 400 without it; ADR-SDK-034 §2 keeps generated required-field
checks); `NotifyResponse.success` becomes required and the `/notify` per-event requirements are
documented; the list's deprecated top-level `paymentMethod`, default window, `endDate` rule and
`transactionType` names are documented. The breaking gate reports `allowlisted` for the
required `paymentMethod` and the list item `oneOf`; no error-code, verdict or status change).

Thirteen published artifacts were never consumed and are superseded rather than skipped:
`v2.3.1+40d659b` (2026-08-10), `v2.5.0+6d41224` (2026-08-27), `v2.8.0+95bd397`,
`v2.9.0+026291d`, `v2.10.0+65b730f`, `v2.11.0+8241a0d`, `v2.12.0+c1c7485`,
`v2.12.1+4bd7ff6` (2026-10-05 to 2026-10-19, absorbed by the v2.12.2 pin; `v2.12.0` breaks
the .NET core build, so it is not a usable pin on its own), and `v2.13.1+f6b9766`,
`v2.14.0+66c63c6`, `v2.14.1+d3c5b38` (2026-10-29 to 2026-11-02, absorbed by the v2.15.0 pin),
and `v2.16.1+8cf9914`, `v2.17.0+19b899b` (2026-11-12 and 2026-11-19, absorbed by the v2.18.0
pin).

[`openapi.bundled.yaml.sha256`](openapi.bundled.yaml.sha256) and
[`provenance.json`](provenance.json) are verbatim copies of the release assets, committed as
review- and CI-verifiable evidence alongside the pin.

## Verify locally

From the repo root:

```sh
gh release download "spec/v2.19.0+ec71a82" -R revaly-co/Backbone -D /tmp/rap-spec --clobber
(cd /tmp/rap-spec && sha256sum -c openapi.bundled.yaml.sha256)
diff /tmp/rap-spec/openapi.bundled.yaml.sha256 spec/openapi.bundled.yaml.sha256
diff /tmp/rap-spec/provenance.json spec/provenance.json
```

All four commands must succeed; the sha256 in `pin.yaml` must match both copies.

## Bumping the pin

1. The spec change lands in the **platform repo** first and publishes a new `spec/v*` release —
   the release cannot exist unless all four platform gates passed (lint, bundle, breaking,
   contract suite).
2. Update `pin.yaml` and replace the committed `.sha256` / `provenance.json` copies — by PR,
   like any dependency bump.
3. Regenerate the six cores against the new artifact in the same PR (once pipeline stage 2
   exists) — the regeneration diff is the review surface.
4. Release notes stamp `sourceCommit` from provenance (pipeline stage 5), keeping every package
   version traceable to a spec commit SHA.

## Hard rules

- Never generate from a branch checkout, a URL, or a locally edited spec (repo rule 2;
  ADR-SDK-006).
- "Latest" is not a pin — this committed reference is the pin, and it moves only by PR.
- A red platform contract suite blocks artifact publication, so it blocks any pin bump too:
  "nothing ships" is meant literally.
