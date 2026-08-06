# ADR-SDK-032 — Public Repo Ships via Fresh-Repo Cutover: Sanitized-History Transplant (Variant B); Current Repo Becomes the Private Archive

**Status:** Accepted — decided 2026-08-03 by Dimitri (SC-263 track); closes the standing
"git-history sanitize-vs-accept" leadership decision. Execution is gated on the flip
preconditions (ADR-SDK-019 written ratification — **recorded 2026-08-06**; PyPI org
approval — pending), per the flip runbook.
**Executed through runbook step 7 on 2026-08-05** (Dimitri-directed, private phase): rename,
transplant, plumbing recreation, green stages-1–4 dispatch, and the v0.5.0 ×6 cutover
release all landed; the repository stays private. Step 8 (public flip) now waits only on
the PyPI org approval (the ADR-SDK-019 written ratification was recorded 2026-08-06).
**Source:** ADR-SDK-012 (public repo requirement), ADR-SDK-013 (publish gate — trusted
publishers bind to repo identity), ADR-SDK-022 (namespace), ADR-SDK-031 (flip runbook),
2026-07-29 history leak-scan record
**Owner:** SC squad (execution) + Leadership (the decision)

## Context

ADR-SDK-012 requires the repo to go public before first publish. The full history contains
three object classes that must not ship publicly — none of them secrets (the 2026-07-29
leak scan found zero credentials, zero real PANs): the `c584d69` commit message repeating
internal AFD/WAF detail, the pre-redaction versions of the docs scrubbed at HEAD (PR #46
fixed HEAD only), and a 9.84 MB `smoke.exe` blob (scanned clean; optics). Author emails
throughout history are `@flexpay.io`.

Purging in place is structurally leaky on GitHub: ~50 read-only `refs/pull/*/head` refs
keep pre-rewrite objects alive after any `git filter-repo` + force-push (removable only via
a GitHub Support ticket + server-side GC), old SHAs stay fetchable meanwhile, and the 51 PR
conversations — platform data no git tool touches — would go public wholesale, requiring a
manual sweep of every thread for the same internal-infra detail class scrubbed from the
docs. The repo has **zero forks**, so no fork network holds the objects.

## Decision

The repository that goes public is a **new** repository; the current one never does.

1. **The current `revaly-co/RAP-sdk` is renamed `revaly-co/RAP-sdk-archive` and stays
   private permanently** — the complete record: true history, all PR/issue conversations,
   and the pre-cutover releases (v0.1.0–v0.4.1) whose `provenance.json` SHAs resolve there.
2. **A new repository reclaims the name `revaly-co/RAP-sdk`.** The name is load-bearing:
   the Go module path (`github.com/revaly-co/rap-sdk/languages/go`) and every committed
   `RepositoryUrl`/`scm`/docs reference stay valid with zero in-tree edits.
3. **Its history is the Variant B transplant**: a local `git filter-repo` pass over the
   full history — drop the `smoke.exe` blob, drop the pre-redaction doc blob versions,
   reword `c584d69`'s message, and rewrite author emails `@flexpay.io → @revaly.co`
   (mailmap) — pushed to the new repo as its complete, real history. The public repo shows
   its work (blame, archaeology, ~140 commits); the `filter-repo` old→new commit map is
   committed to the **archive**, keeping pre-cutover provenance resolvable internally.
   The new repo has only ever contained sanitized objects — there is nothing to purge, no
   support ticket, no pull-ref residue, and no PR-conversation exposure, ever.
4. **Old tags and releases are not ported.** On the new repo they would point at rewritten
   commits with no assets. Version numbering **continues** (no version is ever reused), and
   the cutover ends with a fresh release ×6 cut on the new repo — which end-to-end proves
   stages 1–6 (including the dark registry job) on the new plumbing and restores the
   `RAP-sdk-integration-tests` artifact feed.
5. **Repo plumbing is recreated, not migrated** (none of it transfers): the `staging`
   environment (six smoke secrets + the fail-closed injector variable), the `publish`
   environment with its six `<lang>/v*` tag policies, the `main` ruleset (1 peer review +
   the 8 required checks), CODEOWNERS/maintainer team, and a **re-issued**
   `SPEC_ARTIFACT_READ_TOKEN` (fine-grained PATs are repo-scoped and do not follow —
   org-migration lesson, `pipeline/README.md`). Actions are **disabled on the archive**
   (else the nightly smoke + spec-freshness watchdog double-run). The flip-day admin
   toggles (private-vuln-reporting, secret scanning + push protection, fork-PR approval)
   apply to the new repo.
6. **Sequencing slots into the ADR-SDK-031 flip runbook as gate 3.** OIDC
   trusted-publisher registrations happen only at flip, *after* the cutover — so
   ADR-SDK-013's "re-establish bindings if repo identity changes" consequence is satisfied
   by construction, with nothing to redo.

## Cutover sequence (execution runbook)

Trigger: flip gates 1–2 closed (written ADR-SDK-019 ack recorded; PyPI org resolved).

1. **Freeze**: no merges, no release tags until the swap completes (announce; short window).
2. **Prepare locally**: fresh clone → `git filter-repo` (blob drop `smoke.exe`;
   pre-redaction doc versions; `c584d69` message reword; author-email mailmap). Save the
   commit map.
3. **Rename** `RAP-sdk` → `RAP-sdk-archive` (stays private).
4. **Create** new private `revaly-co/RAP-sdk`; push the transplanted history (`main` only,
   no old tags).
5. **Recreate plumbing** per Decision 5; commit the old→new SHA map to the archive; add the
   archive README banner ("superseded by the public revaly-co/RAP-sdk; PRs #1–#5x and
   pre-cutover releases live here"); disable archive Actions.
6. **Prove green**: `workflow_dispatch` pipeline run (stages 1–4) on the new repo.
7. **Cutover release ×6** (next version numbers, one tag per push) — proves stages 5–6
   (registry job dark) and refeeds the integration-tests harness.
8. **Flip public** (the ADR-SDK-012 moment), then continue the flip runbook (guard-removal
   PR, OIDC registrations, Key Vault material, Packagist webhook + placeholder deletion,
   `REGISTRY_PUBLISH_MODE=live`, GA-order tags).
9. **Comms**: org members re-point local clones to the archive name if they need old
   history; SC-263 updated with the cutover record.

## Alternatives considered

- **`git filter-repo` in place + GitHub Support GC**: rejected — support-ticket dependency
  with unverifiable residue (pull refs, cached SHAs), breaks provenance SHAs *under* the
  existing releases, and still exposes all 51 PR conversations at flip (manual sweep).
- **Accept-at-HEAD + written risk acceptance**: rejected — defensible on secrets (there are
  none) but ships the internal-infra history and the `smoke.exe` optics forever, plus the
  same PR-conversation exposure.
- **Clean-slate single initial commit (Variant A)**: viable fallback, rejected in favor of
  B — a public repo with real history is better collateral for a merchant-facing payments
  SDK, and B costs only the `filter-repo` pass B shares with no one.

## Consequences

- **Reversible until step 8** — worst case is renaming back; nothing is ever destroyed.
- Old PR/commit URLs (internal-only today) dead-end on the new repo; the archive banner +
  SC-263 note are the pointer. Jira/Confluence links to old PRs resolve against the archive.
- Public history SHAs ≠ archive SHAs; the committed commit map bridges them. Pre-cutover
  release provenance resolves **only** against the archive — documented, deliberate.
- The public repo's day-one state must already contain everything ADR-SDK-012 requires
  (SECURITY.md, CODEOWNERS, templates — all merged since 2026-07-30) — they ride the
  transplanted history.
- `revaly-co/rap-sdk-php` (Packagist mirror) and `RAP-sdk-integration-tests` are separate
  repos, unaffected; the harness needs one version bump to the cutover release.
