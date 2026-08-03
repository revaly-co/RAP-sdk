#!/usr/bin/env bash
# Stage 6 — registry publish, DARK until the rule-3 gates close (ADR-SDK-031).
#
# The only registry-publish entry point, local and CI alike:
#   pipeline/registry-publish.sh <language> <version> <dark|live>
#
# Consumes the stage-5 output in dist/<language>/ (pipeline/package.sh) and:
#   * DARK — full rehearsal, no network to any registry: re-verifies checksums,
#     asserts the ADR-SDK-030 names/versions inside the artifacts, asserts the
#     rule-3 embargo guards are INTACT, runs the per-registry flip-readiness
#     lint, and prints what live mode would publish. Readiness misses are
#     WARNINGS in dark mode (the per-release flip-readiness report) and HARD
#     FAILURES in live mode. Dark mode exits 0 unless artifact integrity, a
#     final name, or an embargo guard is wrong.
#   * LIVE — same checks fail-closed, then the real publish. Live requires the
#     embargo guards to be REMOVED (the flip-day PR), so flipping the CI
#     variable alone can never publish: the flip is double-keyed
#     (REGISTRY_PUBLISH_MODE=live AND the guard-removal PR), per ADR-SDK-031.
#
# Per-registry live mechanics (ADR-SDK-013 / ADR-SDK-031):
#   dotnet     dotnet nuget push ×2 (core first) — NUGET_API_KEY minted by the
#              NuGet/login OIDC step in the workflow
#   java       GPG-sign the stage-5 bundle (key file at MAVEN_GPG_KEY_FILE,
#              fetched from Key Vault in the workflow), add md5/sha1, zip the
#              co/ tree, POST to the Central Portal API (MAVEN_CENTRAL_TOKEN)
#   php        push `git subtree split --prefix=languages/php` + tag v<version>
#              to the generated read-only mirror revaly-co/rap-sdk-php
#              (PACKAGIST_MIRROR_PUSH_TOKEN); the Packagist webhook on the
#              mirror does the rest
#   typescript npm publish <tgz> --access public --provenance (npm >= 11.5
#              OIDC trusted publishing; no token)
#   python     this script only validates and stages dist/python/.pypi-upload/
#              with PyPI-canonical filenames; the pypa/gh-action-pypi-publish
#              OIDC step in the workflow performs the upload
#   go         nothing to push — pkg.go.dev is pull-based; the real Go publish
#              is the languages/go/v* ceremony, last (ADR-SDK-026)
#
# Requires: git, jq, sha256sum, tar; unzip or python3; composer (php), twine
# (python) — soft-reported in dark, required in live. On Windows run from
# Git Bash.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ALL_LANGS="dotnet java php typescript python go"

die() { echo "ERROR: $*" >&2; exit 1; }

usage() {
  sed -n '2,42p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

LANG_ID="${1:-}"
VERSION="${2:-}"
MODE="${3:-}"
[ -n "$LANG_ID" ] && [ -n "$VERSION" ] && [ -n "$MODE" ] || { usage; exit 1; }

case " $ALL_LANGS " in
  *" $LANG_ID "*) ;;
  *) die "unknown language '$LANG_ID' (expected one of: $ALL_LANGS)" ;;
esac

# Fail-closed mode parse: only the exact string "live" publishes. Anything
# else — including typos and an unset CI variable — is dark.
case "$MODE" in
  live) ;;
  dark) ;;
  *) die "mode '$MODE' is not dark|live (fail-closed: only exactly 'live' publishes)" ;;
esac

echo "$VERSION" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' \
  || die "version '$VERSION' is not plain X.Y.Z"

for tool in git jq sha256sum tar; do
  command -v "$tool" > /dev/null || die "required tool '$tool' not found on PATH"
done

RELEASE_TAG="$LANG_ID/v$VERSION"
if [ "${GITHUB_REF:-}" != "" ]; then
  case "$GITHUB_REF" in
    refs/tags/*)
      [ "$GITHUB_REF" = "refs/tags/$RELEASE_TAG" ] \
        || die "GITHUB_REF ($GITHUB_REF) does not match computed release tag refs/tags/$RELEASE_TAG" ;;
  esac
fi

OUT="$REPO_ROOT/dist/$LANG_ID"
[ -d "$OUT" ] || die "dist/$LANG_ID not found — run pipeline/package.sh $LANG_ID $VERSION first"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# --- helpers ------------------------------------------------------------------

resolve_python() {
  local p
  for p in python3 python; do
    if command -v "$p" > /dev/null 2>&1 && "$p" -c 'import sys' > /dev/null 2>&1; then
      echo "$p"
      return 0
    fi
  done
  return 1
}

# unzip_read <zip> <entry> — print one entry of a zip to stdout.
unzip_read() {
  local zip="$1" entry="$2" py
  if command -v unzip > /dev/null; then
    unzip -p "$zip" "$entry"
  else
    py="$(resolve_python)" || die "neither unzip nor a working python found to read $zip"
    "$py" -c "import sys,zipfile; sys.stdout.write(zipfile.ZipFile(sys.argv[1]).read(sys.argv[2]).decode('utf-8'))" \
      "$zip" "$entry"
  fi
}

# unzip_all <zip> <dir>
unzip_all() {
  local zip="$1" dir="$2" py
  mkdir -p "$dir"
  if command -v unzip > /dev/null; then
    unzip -q "$zip" -d "$dir"
  else
    py="$(resolve_python)" || die "neither unzip nor a working python found to extract $zip"
    "$py" -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$zip" "$dir"
  fi
}

# Flip-readiness findings: WARN in dark (report), HARD FAIL in live (before
# any push). Integrity/name/guard violations use `die` directly in both modes.
READINESS_FILE="$WORK/readiness"
: > "$READINESS_FILE"
note() {
  echo "$*" >> "$READINESS_FILE"
  echo "::warning::[$LANG_ID $VERSION] flip-readiness: $*"
  echo "  ! $*" >&2
}

# --- artifact integrity (both modes) ------------------------------------------

echo "== stage 6 ($MODE): $LANG_ID $VERSION (tag $RELEASE_TAG)"
(
  cd "$OUT"
  ls ./*.sha256 > /dev/null 2>&1 || die "no .sha256 files in dist/$LANG_ID"
  sha256sum -c ./*.sha256 > /dev/null
)
echo "   checksums verified for $(ls "$OUT"/*.sha256 | wc -l) asset(s)"

# --- per-registry checks (both modes) -----------------------------------------

check_dotnet() {
  local nupkg nuspec
  for pkgid in Revaly.Sdk.Core Revaly.Sdk; do
    nupkg="$OUT/$pkgid.$VERSION.nupkg"
    [ -f "$nupkg" ] || die "expected $pkgid.$VERSION.nupkg missing from dist/dotnet"
    nuspec="$(unzip_read "$nupkg" "$pkgid.nuspec")" || die "cannot read $pkgid.nuspec"
    [ -n "$nuspec" ] || die "$pkgid.nuspec is empty"
    case "$nuspec" in
      *"<id>$pkgid</id>"*) ;;
      *) die "$pkgid nuspec id does not match the ADR-SDK-030 final name" ;;
    esac
    case "$nuspec" in
      *"<version>$VERSION</version>"*) ;;
      *) die "$pkgid nuspec version is not $VERSION" ;;
    esac
    case "$nuspec" in
      *Apache-2.0*) ;;
      *) note "dotnet: $pkgid nuspec carries no Apache-2.0 license expression (ADR-SDK-019)" ;;
    esac
  done
  # The Revaly.* ID prefix was reserved 2026-08-03 for account `revaly`; both
  # ids sit under it by construction — nothing else to check until publish.
  echo "   dotnet: Revaly.Sdk + Revaly.Sdk.Core nuspecs match ADR-SDK-030 @ $VERSION"
}

check_java() {
  local zip="$OUT/revaly-sdk-java.zip" root="$WORK/java" base pom
  [ -f "$zip" ] || die "expected revaly-sdk-java.zip missing from dist/java"
  unzip_all "$zip" "$root"
  for artifact in revaly-sdk revaly-sdk-core; do
    base="$root/co/revaly/$artifact/$VERSION/$artifact-$VERSION"
    [ -f "$base.pom" ] || die "java: $artifact-$VERSION.pom missing from the bundle"
    [ -f "$base.jar" ] || die "java: $artifact-$VERSION.jar missing from the bundle"
    pom="$(cat "$base.pom")"
    for element in name description url licenses scm developers; do
      case "$pom" in
        *"<$element>"*) ;;
        *) note "java: $artifact pom is missing <$element> — Maven Central rejects poms without it" ;;
      esac
    done
    [ -f "$base-sources.jar" ] \
      || note "java: $artifact-$VERSION-sources.jar missing — Maven Central requires a sources jar"
    [ -f "$base-javadoc.jar" ] \
      || note "java: $artifact-$VERSION-javadoc.jar missing — Maven Central requires a javadoc jar (known stage-5 gap: javadoc is skipped for the interim channel; fix before flip)"
  done
  echo "   java: bundle layout co.revaly:{revaly-sdk,revaly-sdk-core}:$VERSION verified"
}

check_php() {
  local zip="$OUT/revaly-sdk-php.zip" name version split_sha tree="$WORK/php-split"
  [ -f "$zip" ] || die "expected revaly-sdk-php.zip missing from dist/php"
  name="$(unzip_read "$zip" composer.json | jq -r '.name')"
  version="$(unzip_read "$zip" composer.json | jq -r '.version')"
  [ "$name" = "revaly/sdk" ] || die "php: artifact composer name '$name' != revaly/sdk (ADR-SDK-030)"
  [ "$version" = "$VERSION" ] || die "php: artifact composer version '$version' != $VERSION"
  # Packagist derives versions from mirror tags — the COMMITTED manifest must
  # stay version-free (the stage-5 artifact copy is the only place a version
  # field is injected).
  git show HEAD:languages/php/composer.json | jq -e 'has("version") | not' > /dev/null \
    || die "php: committed languages/php/composer.json carries a version field — Packagist tags must drive versions"
  # Split rehearsal: packagist.org requires composer.json at the repo root, so
  # the monorepo publishes via a generated subtree-split mirror (ADR-SDK-031).
  if git subtree split -q --prefix=languages/php HEAD > "$WORK/split-sha" 2> /dev/null; then
    split_sha="$(cat "$WORK/split-sha")"
    mkdir -p "$tree"
    git archive "$split_sha" | tar -x -C "$tree"
    [ -f "$tree/composer.json" ] || die "php: subtree split has no composer.json at its root"
    [ "$(jq -r '.name' "$tree/composer.json")" = "revaly/sdk" ] \
      || die "php: split composer name != revaly/sdk"
    if command -v composer > /dev/null; then
      (cd "$tree" && composer validate --strict --no-check-lock) \
        || note "php: composer validate --strict failed on the split root — Packagist will reject it"
    else
      note "php: composer not available in this run — strict validation of the split not performed"
    fi
    echo "   php: subtree split $split_sha rehearsed; composer.json at split root is revaly/sdk"
  else
    note "php: git subtree split failed (shallow clone?) — mirror push cannot be rehearsed"
  fi
}

check_typescript() {
  local tgz="$OUT/revaly-sdk-typescript.tgz" manifest name version private
  [ -f "$tgz" ] || die "expected revaly-sdk-typescript.tgz missing from dist/typescript"
  manifest="$(tar -xOzf "$tgz" package/package.json)"
  name="$(echo "$manifest" | jq -r '.name')"
  version="$(echo "$manifest" | jq -r '.version')"
  private="$(echo "$manifest" | jq -r '.private // "absent"')"
  [ "$name" = "@revaly/sdk" ] || die "typescript: packed name '$name' != @revaly/sdk (ADR-SDK-030)"
  [ "$version" = "$VERSION" ] || die "typescript: packed version '$version' != $VERSION"
  [ "$(echo "$manifest" | jq -r '.license')" = "Apache-2.0" ] \
    || note "typescript: packed license is not Apache-2.0 (ADR-SDK-019)"
  # Rule-3 embargo guard: "private": true blocks npm publish. Dark REQUIRES it
  # intact; live REQUIRES it removed (the flip-day PR). Either mismatch means a
  # half-executed flip — refuse loudly.
  if [ "$MODE" = "dark" ] && [ "$private" != "true" ]; then
    die "typescript: embargo guard missing — packed package.json has no \"private\": true while publish is embargoed (half-flip?)"
  fi
  if [ "$MODE" = "live" ] && [ "$private" != "absent" ]; then
    die "typescript: packed package.json still carries \"private\" — merge the flip-day guard-removal PR before going live"
  fi
  echo "   typescript: @revaly/sdk@$VERSION verified (embargo guard: $private)"
}

check_python() {
  local sdist="$OUT/revaly-sdk-python.tar.gz" wheel="$OUT/revaly_sdk-$VERSION-py3-none-any.whl"
  local metadata upload="$OUT/.pypi-upload"
  [ -f "$sdist" ] || die "expected revaly-sdk-python.tar.gz missing from dist/python"
  [ -f "$wheel" ] || die "expected revaly_sdk-$VERSION-py3-none-any.whl missing from dist/python"
  metadata="$(unzip_read "$wheel" "revaly_sdk-$VERSION.dist-info/METADATA")"
  echo "$metadata" | grep -q '^Name: revaly-sdk$' \
    || die "python: wheel METADATA Name is not revaly-sdk (ADR-SDK-030)"
  echo "$metadata" | grep -q "^Version: $VERSION$" \
    || die "python: wheel METADATA Version is not $VERSION"
  # Rule-3 embargo guard: the Private :: Do Not Upload classifier makes PyPI
  # reject any upload. Same double-key as typescript's "private": true.
  if [ "$MODE" = "dark" ] && ! echo "$metadata" | grep -q 'Private :: Do Not Upload'; then
    die "python: embargo guard missing — wheel has no 'Private :: Do Not Upload' classifier while publish is embargoed (half-flip?)"
  fi
  if [ "$MODE" = "live" ] && echo "$metadata" | grep -q 'Private :: Do Not Upload'; then
    die "python: 'Private :: Do Not Upload' classifier still present — merge the flip-day guard-removal PR before going live"
  fi
  # PyPI requires canonical filenames; the GitHub asset name is friendly
  # (revaly-sdk-python.tar.gz). Stage a PyPI-shaped upload dir either way so
  # dark rehearses exactly what live uploads.
  rm -rf "$upload"
  mkdir -p "$upload"
  cp "$sdist" "$upload/revaly_sdk-$VERSION.tar.gz"
  cp "$wheel" "$upload/"
  if command -v twine > /dev/null; then
    twine check --strict "$upload"/* || note "python: twine check --strict failed — PyPI will reject the upload"
  else
    note "python: twine not available in this run — metadata check not performed"
  fi
  echo "   python: revaly-sdk $VERSION staged for PyPI at dist/python/.pypi-upload/"
}

check_go() {
  local zip="$OUT/revaly-sdk-go.zip" gomod
  [ -f "$zip" ] || die "expected revaly-sdk-go.zip missing from dist/go"
  gomod="$(unzip_read "$zip" go.mod)"
  echo "$gomod" | grep -q '^module github.com/revaly-co/rap-sdk/languages/go$' \
    || die "go: module path in the zip is not github.com/revaly-co/rap-sdk/languages/go"
  echo "   go: pkg.go.dev is pull-based — nothing to push. The real Go publish is the"
  echo "       languages/go/v* tag ceremony on the public repo, last (ADR-SDK-026)."
}

"check_$LANG_ID"

# --- flip-readiness report ----------------------------------------------------

summary() {
  {
    echo "## Stage 6 registry publish — $LANG_ID $VERSION (${MODE^^} mode)"
    echo
    if [ -s "$READINESS_FILE" ]; then
      echo "Flip-readiness findings (warnings in dark, blockers in live):"
      echo
      sed 's/^/- ⚠️ /' "$READINESS_FILE"
    else
      echo "- ✅ no flip-readiness findings — this artifact set could publish as-is once the rule-3 gates close"
    fi
    echo
    if [ "$MODE" = "dark" ]; then
      echo "**DARK MODE — no registry was contacted.** Flip: \`REGISTRY_PUBLISH_MODE=live\` + the guard-removal PR (ADR-SDK-031; runbook in docs/registry-provisioning.md)."
    fi
  } >> "${GITHUB_STEP_SUMMARY:-/dev/null}"
}

if [ "$MODE" = "dark" ]; then
  summary
  echo ""
  echo "== DARK MODE — rehearsal complete; no registry was contacted (rule 3 embargo intact)."
  if [ -s "$READINESS_FILE" ]; then
    echo "   Flip-readiness findings ($(wc -l < "$READINESS_FILE")) — these BLOCK live mode:"
    sed 's/^/     - /' "$READINESS_FILE"
  else
    echo "   No flip-readiness findings."
  fi
  exit 0
fi

# --- LIVE ---------------------------------------------------------------------

if [ -s "$READINESS_FILE" ]; then
  summary
  die "live mode refused: $(wc -l < "$READINESS_FILE") flip-readiness finding(s) above must be fixed first"
fi

publish_dotnet() {
  command -v dotnet > /dev/null || die "dotnet SDK not found"
  [ -n "${NUGET_API_KEY:-}" ] || die "NUGET_API_KEY not set — the NuGet/login OIDC step must run first"
  # Core first: the runtime package depends on it; never let a consumer resolve
  # Revaly.Sdk before its core exists. No --skip-duplicate: a re-push fails
  # loudly — a failed release resumes only via a new tag.
  for pkgid in Revaly.Sdk.Core Revaly.Sdk; do
    dotnet nuget push "$OUT/$pkgid.$VERSION.nupkg" \
      --source https://api.nuget.org/v3/index.json \
      --api-key "$NUGET_API_KEY"
  done
}

publish_java() {
  command -v gpg > /dev/null || die "gpg not found"
  command -v curl > /dev/null || die "curl not found"
  [ -n "${MAVEN_CENTRAL_TOKEN:-}" ] || die "MAVEN_CENTRAL_TOKEN not set (Key Vault fetch step)"
  [ -f "${MAVEN_GPG_KEY_FILE:-/nonexistent}" ] || die "MAVEN_GPG_KEY_FILE not set or missing (Key Vault fetch step)"
  export GNUPGHOME="$WORK/gnupg"
  mkdir -p "$GNUPGHOME" && chmod 700 "$GNUPGHOME"
  gpg --batch --import "$MAVEN_GPG_KEY_FILE"
  local root="$WORK/java" bundle="$WORK/central-bundle.zip" f
  # check_java already extracted the stage-5 bundle to $root; sign + checksum
  # exactly those bytes — the registry publish never rebuilds.
  find "$root/co" -type f | while read -r f; do
    gpg --batch --yes --pinentry-mode loopback \
      ${MAVEN_GPG_PASSPHRASE:+--passphrase "$MAVEN_GPG_PASSPHRASE"} \
      --armor --detach-sign "$f"
    md5sum "$f" | awk '{print $1}' > "$f.md5"
    sha1sum "$f" | awk '{print $1}' > "$f.sha1"
  done
  (cd "$root" && if command -v zip > /dev/null; then zip -qr "$bundle" co; else
    "$(resolve_python)" -c "import shutil,sys; shutil.make_archive(sys.argv[1][:-4],'zip',root_dir='.',base_dir='co')" "$bundle"; fi)
  curl --fail-with-body -sS -X POST \
    -H "Authorization: Bearer $MAVEN_CENTRAL_TOKEN" \
    -F "bundle=@$bundle" \
    "https://central.sonatype.com/api/v1/publisher/upload?name=co.revaly:revaly-sdk:$VERSION&publishingType=AUTOMATIC"
  echo ""
  echo "   java: bundle accepted by the Central Portal (AUTOMATIC publishing)"
}

publish_php() {
  [ -n "${PACKAGIST_MIRROR_PUSH_TOKEN:-}" ] || die "PACKAGIST_MIRROR_PUSH_TOKEN not set"
  local split_sha mirror="https://x-access-token:${PACKAGIST_MIRROR_PUSH_TOKEN}@github.com/revaly-co/rap-sdk-php.git"
  split_sha="$(git subtree split -q --prefix=languages/php HEAD)"
  # The mirror is GENERATED, read-only output of this job (ADR-SDK-031): its
  # main branch is forcibly aligned to the split of the tagged monorepo commit.
  # Tags are never forced — a duplicate v-tag fails loudly (new tag to resume).
  git push --force "$mirror" "$split_sha:refs/heads/main"
  git push "$mirror" "$split_sha:refs/tags/v$VERSION"
  echo "   php: mirror revaly-co/rap-sdk-php updated to split $split_sha, tag v$VERSION — Packagist webhook takes it from here"
}

publish_typescript() {
  command -v npm > /dev/null || die "npm not found"
  # OIDC trusted publishing needs npm >= 11.5.1 (no token; requires the
  # trusted publisher registered for @revaly/sdk and a public repo for
  # --provenance).
  npm --version | awk -F. '($1 > 11) || ($1 == 11 && $2 >= 5) {ok=1} END {exit !ok}' \
    || die "npm $(npm --version) < 11.5 — OIDC trusted publishing needs a newer npm"
  npm publish "$OUT/revaly-sdk-typescript.tgz" --access public --provenance
}

publish_python() {
  echo "   python: upload dir staged — the pypa/gh-action-pypi-publish OIDC step performs the upload"
}

publish_go() {
  echo "   go: nothing to publish here (pull-based; languages/go/v* ceremony per ADR-SDK-026)"
}

"publish_$LANG_ID"
summary
echo "== stage 6 LIVE complete for $LANG_ID $VERSION"
