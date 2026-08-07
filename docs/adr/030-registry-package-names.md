# ADR-SDK-030 — Registry Package Names Finalized ×6 (OQ-3 naming)

**Status:** Accepted — decided 2026-07-29 by the OQ-3 owner; ratified 2026-07-30
**Closes:** the naming leg of OQ-3 (`../open-items.md`); the provisioning residuals stay open
under the OQ with their own owners
**Drives:** `../runtime-tdd.md` §7 · `../registry-provisioning.md` · the stage-6 registry
publish job (successor to the ADR-SDK-026 interim channel) · the NuGet `Revaly.*` ID-prefix
reservation

## Context

`runtime-tdd.md` §7 has carried the package-name scheme as **[Proposed — finalize at OQ-3
provisioning]** since the RFC: nothing may hardcode a registry name before it is final — the
stage-6 publish job, the NuGet prefix reservation, quickstart install lines, and the
ADR-SDK-012 public documentation all depend on it. The one genuinely open choice was npm:
unscoped `revaly-sdk` vs the scoped `@revaly/sdk`, deliberately deferred until provisioning
reality existed.

Provisioning reality now exists (`../registry-provisioning.md`): all six namespaces are
reserved — the npm org `revaly` (owner of the `@revaly` scope), the Maven Central `co.revaly`
namespace (domain-verified), the Packagist vendor `revaly` (held via the tracked placeholder),
the NuGet org, the PyPI org application (pending approval), and the Go module path bound to
the GitHub org (ADR-SDK-022). Publishing remains embargoed (rule 3): OIDC registrations,
registry tokens, and any publish — pre-1.0 included — wait on the remaining OQ-3 provisioning
acts and the ADR-SDK-019 written ratification (the latter recorded 2026-08-06; the remaining
OQ-3 act is the PyPI org approval).

## Decision

| Registry | Final package name |
| --- | --- |
| npm | **`@revaly/sdk`** (scoped) |
| PyPI | `revaly-sdk` |
| NuGet | `Revaly.Sdk` (runtime) + `Revaly.Sdk.Core` (generated core) |
| Packagist | `revaly/sdk` |
| Maven Central | `co.revaly:revaly-sdk` |
| Go | `github.com/revaly-co/rap-sdk/languages/go` (unchanged — ADR-SDK-022, layout per ADR-SDK-028) |

**npm ships scoped.** The `revaly` org already owns the `@revaly` scope, a scoped name is
immune to squatting and typo-adjacency in the flat namespace, and it puts the brand token in
the install line (`npm install @revaly/sdk`) exactly as NuGet, Maven, and Packagist names do.
The `User-Agent` product token (`revaly-sdk-<language>/<semver>`, ADR-SDK-005) is unaffected —
it is a telemetry token, not a registry name.

Names do **not** embed the GitHub org — except Go's module path, whose permanence is exactly
why Go publishes last (ADR-SDK-015/022).

## Consequences

- `../runtime-tdd.md` §7 flips **[Proposed] → [Decided]** referencing this ADR;
  `../registry-provisioning.md` records the names as final and tracks the per-registry
  remaining acts.
- **Committed metadata is already final in five of six languages** (.NET `Revaly.Sdk` +
  `Revaly.Sdk.Core` PackageIds; PHP composer name `revaly/sdk`; Python project name
  `revaly-sdk` — the `revaly_sdk_core` wheel is an internal artifact, not a registry name;
  Maven `co.revaly` groupId; the Go path). The single rename is npm:
  `languages/typescript/package.json` still says `revaly-sdk` and becomes `@revaly/sdk` in
  the stage-6 prep — together with the quickstart install-line sweep — before the first npm
  publish. The interim GitHub-release channel (ADR-SDK-026) is unaffected in the meantime.
- The NuGet `Revaly.*` ID-prefix reservation can now be requested against final package ids.
- The Packagist first-publish act deletes the placeholder `revaly/rap-sdk` and publishes
  `revaly/sdk` through the gated pipeline (the deviation record in
  `../registry-provisioning.md` stands until then).
- **Nothing here relaxes the publish embargo.** The gates of rule 3 stand unchanged: OQ-3
  provisioning residuals (NuGet prefix — reserved 2026-08-03; PyPI org — pending) and the
  ADR-SDK-019 written ratification (recorded 2026-08-06).
