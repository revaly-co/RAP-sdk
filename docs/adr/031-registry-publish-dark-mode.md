# ADR-SDK-031 — Stage-6 Registry Publish Ships DARK; Double-Keyed Flip; Packagist via Split Mirror; GitHub Releases Stay

**Status:** Proposed — authored 2026-08-03 (build session after the NuGet `Revaly.*` prefix
reservation landed); ratification rides the PR review
**Source:** ADR-SDK-013 (publish mechanics — concretized here), ADR-SDK-026 (interim channel),
ADR-SDK-030 (final names), `../registry-provisioning.md` (per-registry board + flip runbook)
**Owner:** SC squad (per ADR-SDK-018)

## Context

Every publish gate that can close early has closed: names are final ×6 (ADR-SDK-030), all six
namespaces are held, the NuGet `Revaly.*` ID-prefix is reserved (2026-08-03), the protected
`publish` environment exists with per-language tag policies, and `SECURITY.md` + the
`security@` intake are live. What remains is outside this repo's control: PyPI org approval
(external queue), the ADR-SDK-019 **written** ratification, the git-history decision before
the repo goes public (ADR-SDK-012), and the publish-day OIDC/GPG/webhook bindings.

Waiting for those gates to *build* the registry job would put untested publish code on the
critical path of flip day — the exact day nothing should run for the first time. The
alternative is building it now and proving it inert.

## Decision

1. **The stage-6 registry job exists now and runs DARK on every release tag.** It runs in the
   protected `publish` environment (exercising the ADR-SDK-013 deployment policies release by
   release), downloads the stage-5 artifact set, re-verifies checksums, asserts the ADR-SDK-030
   names/versions inside the artifacts, and runs a per-registry **flip-readiness lint**. In
   dark mode, readiness findings are warnings (a per-release readiness report in the job
   summary); it contacts **no registry**. `pipeline/registry-publish.sh` is the only entry
   point, local and CI alike.

2. **The flip is double-keyed.** Going live requires BOTH:
   - the repo variable `REGISTRY_PUBLISH_MODE` set to exactly `live` (anything else,
     including unset, is dark — fail-closed), **and**
   - the flip-day guard-removal PR: the committed embargo guards (`"private": true` in the
     npm manifest; the `Private :: Do Not Upload` classifier in `pyproject.toml`) must be
     gone from the packed artifacts. Dark mode **requires the guards intact**; live mode
     **requires them removed**. Either mismatch is a hard failure — a half-executed flip
     cannot publish and cannot silently rehearse.
   In live mode every readiness warning becomes a blocker before any push.

3. **Per-registry live mechanics** (concretizing ADR-SDK-013's implementation guidance):
   - **npm** — `npm publish <stage-5 tgz> --access public --provenance` via OIDC trusted
     publishing (npm ≥ 11.5, no token).
   - **PyPI** — `pypa/gh-action-pypi-publish` via OIDC; the script stages a PyPI-canonical
     upload dir (`revaly_sdk-<v>.tar.gz`) because the GitHub asset name
     (`revaly-sdk-python.tar.gz`) is not a valid sdist filename.
   - **NuGet** — `NuGet/login` OIDC exchange → `dotnet nuget push`, core before runtime.
   - **Maven Central** — GPG-sign the stage-5 bundle bytes (keys fetched from Key Vault
     inside the environment-scoped job), add md5/sha1, upload to the Central Portal API.
     The registry publish **never rebuilds** — it signs exactly what stage 5 shipped.
   - **Packagist** — **amends ADR-SDK-013's "webhook from the public repo"**: packagist.org
     requires `composer.json` at the repository root, so the monorepo cannot be tracked
     directly. The job pushes `git subtree split --prefix=languages/php` of the tagged
     commit to the existing repo **`revaly-co/rap-sdk-php`**, repurposed as a **generated,
     read-only mirror** (its placeholder history is force-replaced — it is job output, never
     hand-edited; tags are never forced), and tags it `v<version>`; the Packagist webhook on
     the mirror does the rest. Packagist package `revaly/sdk` tracks the mirror.
   - **pkg.go.dev** — nothing to push (pull-based). The Go publish remains the deliberate
     `languages/go/v*` tag ceremony, last (ADR-SDK-026); the registry job is informational
     for `go/v*` tags.

4. **Ordering: GitHub release first, registries after — and GitHub releases stay at GA.**
   The registry job depends on the interim-release job, so the GitHub release (asset +
   `.sha256` + `provenance.json`) always exists before any registry sees the version, and a
   red registry job never blocks or retracts it. After the flip, GitHub releases continue as
   (a) the provenance anchor every registry package's release notes point back to, (b) the
   registry-outage/air-gap fallback channel, and (c) the only channel whose artifact model
   carries the full gate trail. Registries become the **primary, documented install path**;
   quickstart install lines switch at flip. pkg.go.dev consumes the repo+tags directly, so
   the GitHub side is load-bearing for Go regardless.

## Consequences

- Flip day executes a **runbook, not a build**: provision bindings, merge the guard-removal
  PR, set `REGISTRY_PUBLISH_MODE=live`, cut tags ×6 in GA order. The runbook lives in
  `../registry-provisioning.md` § Flip to LIVE.
- Every release until then emits a flip-readiness report; readiness regressions (a pom
  losing its `<developers>`, a metadata drift) surface on the next tag, not on flip day.
  Known findings today: the stage-5 Java bundle ships no javadoc jars (Maven Central
  requires them — fix lands before the Maven flip), and the placeholder deletion on
  Packagist is a one-time manual act at flip.
- The npm rename to `@revaly/sdk` (ADR-SDK-030 stage-6 prep) ships with this ADR's PR; the
  interim tarball name (`revaly-sdk-<v>.tgz`, thus `revaly-sdk-typescript.tgz`) is
  unchanged by scoping. The one known external consumer of the import specifier —
  `revaly-co/RAP-sdk-integration-tests` (`integrations/typescript/src/main.ts`) — updates
  its import to `@revaly/sdk` when it first consumes a post-rename release.
- `secrets`/`vars` referenced by the live path (`NUGET_TRUSTED_PUBLISHING_USER`,
  `PUBLISH_AZURE_*`, `PUBLISH_KEYVAULT_NAME`, `PACKAGIST_MIRROR_PUSH_TOKEN`) are
  deliberately **not** provisioned until flip day — in dark mode no step reads them, so
  their absence cannot fail a release.
- Rule 3's wording ("no registry publish surface") is refined, not weakened: the *surface*
  now exists in code, permanently dark and double-keyed; the *acts* (OIDC registration,
  tokens, any publish) remain embargoed exactly as before.
