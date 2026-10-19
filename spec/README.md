# `spec/` — Pinned Gated Spec Artifact (ADR-SDK-006)

The SDK pipeline consumes **exactly one spec input**: the platform release referenced in
[`pin.yaml`](pin.yaml). The bundle itself is deliberately not committed — pipeline stage 1
downloads it from the pinned release tag and verifies it against the committed checksums
before anything downstream runs (`../docs/pipeline-and-release.md` §2).

## Current pin

| Field | Value |
| --- | --- |
| Release | [`spec/v2.13.0+98915d8`](https://github.com/revaly-co/Backbone/releases/tag/spec%2Fv2.13.0%2B98915d8) (platform repo) |
| Spec version | 2.13.0 |
| Source commit | `98915d8fe0b27df33e7117866674a4b8e8a22bbb` |
| Gates | lint ✅ · bundle ✅ · breaking ✅ · contract suite ✅ (see [`provenance.json`](provenance.json)) |
| sha256 (`openapi.bundled.yaml`) | `ac8db33744bd9328b636329320362f58af2c690876cacc1965db30341eb66364` |
| Pinned | 2026-10-19 |

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
all six packages).

Eight published artifacts were never consumed and are superseded rather than skipped:
`v2.3.1+40d659b` (2026-08-10), `v2.5.0+6d41224` (2026-08-27), and `v2.8.0+95bd397`,
`v2.9.0+026291d`, `v2.10.0+65b730f`, `v2.11.0+8241a0d`, `v2.12.0+c1c7485`,
`v2.12.1+4bd7ff6` (2026-10-05 to 2026-10-19, absorbed by the v2.12.2 pin; `v2.12.0` breaks
the .NET core build, so it is not a usable pin on its own).

[`openapi.bundled.yaml.sha256`](openapi.bundled.yaml.sha256) and
[`provenance.json`](provenance.json) are verbatim copies of the release assets, committed as
review- and CI-verifiable evidence alongside the pin.

## Verify locally

From the repo root:

```sh
gh release download "spec/v2.13.0+98915d8" -R revaly-co/Backbone -D /tmp/rap-spec --clobber
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
