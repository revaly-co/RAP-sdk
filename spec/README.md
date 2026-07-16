# `spec/` — Pinned Gated Spec Artifact (ADR-SDK-006)

The SDK pipeline consumes **exactly one spec input**: the platform release referenced in
[`pin.yaml`](pin.yaml). The bundle itself is deliberately not committed — pipeline stage 1
downloads it from the pinned release tag and verifies it against the committed checksums
before anything downstream runs (`../docs/pipeline-and-release.md` §2).

## Current pin

| Field | Value |
| --- | --- |
| Release | [`spec/v2.2.1+c4000e9`](https://github.com/FlexPay-io/Backbone/releases/tag/spec%2Fv2.2.1%2Bc4000e9) (platform repo) |
| Spec version | 2.2.1 |
| Source commit | `c4000e9715bd2f6a2f2f486c338659c9c77c6fc5` |
| Gates | lint ✅ · bundle ✅ · breaking ✅ · contract suite ✅ (see [`provenance.json`](provenance.json)) |
| sha256 (`openapi.bundled.yaml`) | `efc78066a4724b96e6401f6b08ca32b31c1952c6746aab9143f506aa615acbdf` |
| Pinned | 2026-07-16 |

Pin history: `v2.1.2+9af661b` (2026-07-14, first pin — int64 `maximum` fix, Backbone PR #241)
→ `v2.1.3+e75c71a` (2026-07-15 — orphan `PaymentMethodRequest` schema dropped, Backbone PR #242)
→ `v2.2.0+1e59620` (2026-07-16 — additive `statementDescriptor` on charge request/response,
Backbone STR-108 / PR #228) → `v2.2.1+c4000e9` (2026-07-16 — `X-Correlation-ID` response
header documented on every response, Backbone PR #247).

[`openapi.bundled.yaml.sha256`](openapi.bundled.yaml.sha256) and
[`provenance.json`](provenance.json) are verbatim copies of the release assets, committed as
review- and CI-verifiable evidence alongside the pin.

## Verify locally

From the repo root:

```sh
gh release download "spec/v2.2.1+c4000e9" -R FlexPay-io/Backbone -D /tmp/rap-spec --clobber
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
