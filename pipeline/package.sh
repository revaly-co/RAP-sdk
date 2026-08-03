#!/usr/bin/env bash
# Stage 5 — package one language as a GitHub release artifact set
# (docs/pipeline-and-release.md §2 row 5; ADR-SDK-026 interim distribution).
#
# The only packaging entry point, local and CI alike:
#   pipeline/package.sh <language> <version>       e.g.  pipeline/package.sh dotnet 0.1.0
#
# Output: dist/<language>/ containing the distributable asset(s), one .sha256 per
# asset, provenance.json, and RELEASE_NOTES.md — the same artifact model as the
# platform's spec/v* releases (asset + .sha256 + provenance.json).
#
# Guarantees (fail-closed):
#   * packages EXACTLY the committed tree at HEAD (git archive) — never the working
#     tree, never untracked files;
#   * <version> must be plain X.Y.Z — the interim channel refuses pre-release
#     identifiers (no alpha/beta/rc; ADR-SDK-026) and refuses a `v` prefix;
#   * committed manifests stay at their 0.0.0-dev placeholders; the release version
#     is stamped into the ephemeral staging copy only, and every stamp is verified
#     (a silently no-op sed is treated as failure);
#   * registry publish is EMBARGOED (repo rule 3): this script produces files on
#     disk and never talks to any registry.
#
# Requires: git, jq, sha256sum, tar; plus the language toolchain (dotnet / mvn /
# php / node+npm / python3 with the `build` package / go). zip is used when
# present, else python3's zipfile. On Windows run from Git Bash.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SPEC_PIN=spec/pin.yaml
GEN_PIN=pipeline/generator-pin.yaml
ALL_LANGS="dotnet java php typescript python go"

die() { echo "ERROR: $*" >&2; exit 1; }

usage() {
  sed -n '2,26p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

LANG_ID="${1:-}"
VERSION="${2:-}"
[ -n "$LANG_ID" ] && [ -n "$VERSION" ] || { usage; exit 1; }

case " $ALL_LANGS " in
  *" $LANG_ID "*) ;;
  *) die "unknown language '$LANG_ID' (expected one of: $ALL_LANGS)" ;;
esac

# Plain semver only. The interim GitHub-release channel ships no pre-release
# versions (decision 2026-07-20, ADR-SDK-026): a "beta" artifact would look like
# the pre-1.0 registry publishing that repo rule 3 embargoes.
echo "$VERSION" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' \
  || die "version '$VERSION' is not plain X.Y.Z — no v prefix, no pre-release/build suffix (ADR-SDK-026)"

for tool in git jq sha256sum tar; do
  command -v "$tool" > /dev/null || die "required tool '$tool' not found on PATH"
done

# Release tag scheme (ADR-SDK-026): <language>/vX.Y.Z. Go deliberately tags as
# go/vX.Y.Z — NOT languages/go/vX.Y.Z, which is the Go-module-activating form for
# the subdir module and is reserved for the real (last, gated) Go registry publish.
RELEASE_TAG="$LANG_ID/v$VERSION"

# In CI the tag that triggered the run must agree with the arguments — argument
# drift between the workflow parse step and this script refuses the run.
if [ "${GITHUB_REF:-}" != "" ]; then
  case "$GITHUB_REF" in
    refs/tags/*)
      [ "$GITHUB_REF" = "refs/tags/$RELEASE_TAG" ] \
        || die "GITHUB_REF ($GITHUB_REF) does not match computed release tag refs/tags/$RELEASE_TAG" ;;
  esac
fi

SOURCE_COMMIT="$(git rev-parse HEAD)"
OUT="$REPO_ROOT/dist/$LANG_ID"
rm -rf "$OUT"
mkdir -p "$OUT"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# --- pin + generator metadata (same grep parse as pipeline stage 1) -----------

pin_field() {
  grep -m1 -E "^$1:" "$SPEC_PIN" | awk '{print $2}'
}

SPEC_REPO="$(pin_field repo)"
SPEC_TAG="$(pin_field releaseTag)"
SPEC_VERSION="$(pin_field specVersion)"
SPEC_COMMIT="$(pin_field sourceCommit)"
SPEC_SHA256="$(grep -m1 -E '^  openapi\.bundled\.yaml:' "$SPEC_PIN" | awk '{print $2}')"
for v in "$SPEC_REPO" "$SPEC_TAG" "$SPEC_VERSION" "$SPEC_COMMIT" "$SPEC_SHA256"; do
  [ -n "$v" ] || die "$SPEC_PIN is missing a required field (repo/releaseTag/specVersion/sourceCommit/sha256)"
done

GEN_NAME="$(grep -m1 -E '^generator:' "$GEN_PIN" | awk '{print $2}')"
GEN_VERSION="$(grep -m1 -E '^version:' "$GEN_PIN" | awk '{print $2}')"
GEN_DIGEST="$(grep -m1 -E '^imageDigest:' "$GEN_PIN" | awk '{print $2}')"
for v in "$GEN_NAME" "$GEN_VERSION" "$GEN_DIGEST"; do
  [ -n "$v" ] || die "$GEN_PIN is missing a required field (generator/version/imageDigest)"
done

# --- helpers ------------------------------------------------------------------

# Pristine copy of the committed tree at HEAD (tracked files only — build output,
# node_modules, vendor etc. can never leak into an artifact).
stage_tree() {
  git archive --format=tar HEAD LICENSE NOTICE "languages/$LANG_ID" | tar -x -C "$WORK"
}

# Resolve a working python interpreter: on Windows, `python3` may be the inert
# Microsoft Store alias stub — probe with an actual import before trusting it.
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

# stamp <file> <sed-expression> <must-contain> — sed that refuses to no-op.
stamp() {
  local file="$1" expr="$2" expect="$3"
  sed -i.bak "$expr" "$file" && rm -f "$file.bak"
  grep -qF "$expect" "$file" \
    || die "version stamp failed: '$expect' not present in $file after edit"
}

# make_zip <out.zip> <dir> — zip the CONTENTS of <dir> (archive root = dir root).
make_zip() {
  local out="$1" dir="$2"
  if command -v zip > /dev/null; then
    (cd "$dir" && zip -qr "$out" .)
  else
    local py
    py="$(resolve_python)" || die "neither zip nor a working python found for archive creation"
    "$py" - "$out" "$dir" <<'PYEOF'
import os, sys, zipfile
out, root = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for base, _, files in os.walk(root):
        for name in files:
            full = os.path.join(base, name)
            z.write(full, os.path.relpath(full, root))
PYEOF
  fi
}

# --- per-language packaging ---------------------------------------------------

package_dotnet() {
  command -v dotnet > /dev/null || die "dotnet SDK not found"
  stage_tree
  local src="$WORK/languages/dotnet"
  local core_csproj="$src/core/src/Revaly.Sdk.Core/Revaly.Sdk.Core.csproj"
  # Staged-copy fix to the GENERATED core csproj (external SDK audit 2026-07-23). Like
  # package_java's versions:set on the generated pom, this edit exists only in the
  # ephemeral staging copy that becomes the artifact — the committed tree is never
  # hand-edited (ADR-SDK-001): drop the Microsoft.Extensions.Http.Polly PackageReference,
  # generator-template baggage with zero code usage that a "no hidden retries" SDK must
  # not carry in its dependency tree. Fail-closed both directions so a template change at
  # the next regen can neither silently no-op nor silently reintroduce it. The
  # generator-config-level fix (packageAuthors/gitUserId/…) is a pre-GA follow-up under
  # ADR-SDK-023 discipline.
  grep -q 'Microsoft\.Extensions\.Http\.Polly' "$core_csproj" \
    || die "Polly PackageReference not found in staged core csproj — generator template changed; re-verify this strip"
  # The strip is designed for exactly the shape the pinned template emits: ONE
  # self-closing, single-line PackageReference. Refuse anything else — a
  # multi-line emission after a template change would leave orphaned attribute
  # fragments behind a single-line delete. (dotnet pack's MSB4025 would still
  # reject the malformed csproj; these guards just fail earlier and clearer.)
  [ "$(grep -c 'Microsoft\.Extensions\.Http\.Polly' "$core_csproj" || true)" = "1" ] \
    || die "expected exactly one Polly reference line in the staged core csproj — template shape changed; re-verify this strip"
  grep -Eq '^[[:space:]]*<PackageReference[[:space:]][^<>]*Microsoft\.Extensions\.Http\.Polly[^<>]*/>[[:space:]]*$' "$core_csproj" \
    || die "the Polly PackageReference is not a single self-closing line — template shape changed; re-verify this strip"
  sed -i.bak '/Microsoft\.Extensions\.Http\.Polly/d' "$core_csproj" && rm -f "$core_csproj.bak"
  if grep -q 'Microsoft\.Extensions\.Http\.Polly' "$core_csproj"; then
    die "Polly PackageReference still present in staged core csproj after strip"
  fi
  # -p:Version stamps the assembly informational version RapUserAgent.ResolveSemver
  # reads, the nupkg version, and the runtime→core package-dependency version.
  # PackageOutputPath as a property, not -o: under Git Bash (MSYS) the -o form
  # mis-parses when the project path is also being converted (verified 2026-07-20);
  # the property form behaves identically on the Linux runners.
  # The -p:Authors/-p:Copyright/-p:PackageDescription/-p:RepositoryUrl overrides replace
  # the generator's placeholder nuspec metadata (authors "OpenAPI", GIT_USER_ID repo URL,
  # "No Copyright") in the packed artifact only — same staging-copy philosophy as above.
  # %2C = MSBuild's escaped comma: bare commas in -p: values are pair separators
  # (MSB1006), so "Revaly, Inc." must ride through escaped.
  dotnet pack "$core_csproj" \
    -c Release -p:Version="$VERSION" -p:ContinuousIntegrationBuild=true \
    -p:Authors=Revaly -p:Company="Revaly%2C Inc." \
    -p:Copyright="Copyright 2026 Revaly%2C Inc." \
    -p:AssemblyTitle=Revaly.Sdk.Core \
    -p:PackageDescription="Generated API core for the Revaly RAP V2 .NET SDK. Reference the Revaly.Sdk runtime package instead of using this package directly." \
    -p:PackageReleaseNotes="See the GitHub release notes for the version-to-spec traceability table." \
    -p:RepositoryUrl="https://github.com/revaly-co/rap-sdk" \
    -p:PackageOutputPath="$OUT"
  dotnet pack "$src/runtime/Revaly.Sdk/Revaly.Sdk.csproj" \
    -c Release -p:Version="$VERSION" -p:ContinuousIntegrationBuild=true \
    -p:PackageOutputPath="$OUT"
  [ -f "$OUT/Revaly.Sdk.$VERSION.nupkg" ] && [ -f "$OUT/Revaly.Sdk.Core.$VERSION.nupkg" ] \
    || die "expected nupkgs missing from $OUT"
  # Fail closed on the metadata too: the packed core nuspec must carry none of
  # the placeholders this fix replaces (nor Polly, nor an undecoded %2C), and
  # MUST carry the injected values. Every read is guarded locally — an
  # unreadable or empty nuspec is a verification failure, never a pass, no
  # matter how this function is invoked (errexit is suppressed for the whole
  # function body when a caller wraps it in a condition — never rely on it).
  local nuspec py
  if command -v unzip > /dev/null; then
    nuspec="$(unzip -p "$OUT/Revaly.Sdk.Core.$VERSION.nupkg" Revaly.Sdk.Core.nuspec)" \
      || die "failed to read Revaly.Sdk.Core.nuspec out of the packed nupkg — verification cannot proceed"
  else
    py="$(resolve_python)" || die "neither unzip nor a working python found to verify the packed nuspec"
    nuspec="$("$py" -c "import sys,zipfile; sys.stdout.write(zipfile.ZipFile(sys.argv[1]).read('Revaly.Sdk.Core.nuspec').decode('utf-8'))" \
      "$OUT/Revaly.Sdk.Core.$VERSION.nupkg")" \
      || die "failed to read Revaly.Sdk.Core.nuspec out of the packed nupkg (python) — verification cannot proceed"
  fi
  [ -n "$nuspec" ] || die "extracted core nuspec is empty — verification cannot proceed"
  case "$nuspec" in
    *OpenAPI* | *GIT_USER_ID* | *"No Copyright"* | *%2C* | *Polly*)
      die "generator placeholder metadata, an undecoded %2C, or Polly still present in the packed core nuspec" ;;
  esac
  # Positive assertions: absence of the old values is not proof the new ones
  # landed — require the decoded replacements verbatim.
  case "$nuspec" in
    *"<authors>Revaly</authors>"*) ;;
    *) die "packed core nuspec is missing <authors>Revaly</authors> — metadata override did not land" ;;
  esac
  case "$nuspec" in
    *"Copyright 2026 Revaly, Inc."*) ;;
    *) die "packed core nuspec is missing the decoded copyright line (comma-escape regression?)" ;;
  esac
}

package_java() {
  command -v mvn > /dev/null || die "mvn not found"
  stage_tree
  local src="$WORK/languages/java" m2="$WORK/m2" bundle="$WORK/bundle"
  # Ephemeral-copy stamp: reactor + inter-module dependency versions. The core pom
  # is generator output in the committed tree (ADR-SDK-001); this edit happens only
  # in the staging copy that becomes the artifact.
  mvn -B -ntp -f "$src/pom.xml" versions:set \
    -DnewVersion="$VERSION" -DprocessAllModules -DgenerateBackupPoms=false
  # -Dmaven.javadoc.skip=true: skip the generated core's attach-javadocs execution —
  # it doclints undocumented generated members into hundreds of "no comment" warnings,
  # and the interim file-repo bundle does not ship javadoc jars (sources jar is kept).
  # GA/Maven-Central javadoc is handled at the generator-template level, not here.
  mvn -B -ntp -f "$src/pom.xml" -pl runtime -am -DskipTests \
    -Dmaven.repo.local="$m2" -Dmaven.javadoc.skip=true install
  # Maven-repository bundle: exactly our two artifacts, consumable via a
  # file:// repository or an unzip into ~/.m2/repository.
  mkdir -p "$bundle/co/revaly"
  for artifact in revaly-sdk revaly-sdk-core; do
    [ -d "$m2/co/revaly/$artifact/$VERSION" ] \
      || die "expected $artifact/$VERSION missing from the scoped local repo"
    cp -R "$m2/co/revaly/$artifact" "$bundle/co/revaly/$artifact"
  done
  find "$bundle" -name "_remote.repositories" -delete
  find "$bundle" -name "maven-metadata-local.xml" -delete
  cp "$WORK/LICENSE" "$WORK/NOTICE" "$bundle/"
  make_zip "$OUT/revaly-sdk-java.zip" "$bundle"
}

package_php() {
  stage_tree
  local src="$WORK/languages/php" pkg="$WORK/pkg"
  mkdir -p "$pkg"
  cp "$src/composer.json" "$src/README.md" "$pkg/"
  mkdir -p "$pkg/runtime" "$pkg/core"
  cp -R "$src/runtime/src" "$pkg/runtime/src"
  cp -R "$src/core/lib" "$pkg/core/lib"
  cp "$WORK/LICENSE" "$WORK/NOTICE" "$pkg/"
  # A composer "artifact" repository requires an explicit version INSIDE the
  # zipped composer.json; the committed manifest stays version-free (Packagist
  # derives versions from tags once publish opens).
  jq --arg v "$VERSION" '.version = $v' "$pkg/composer.json" > "$pkg/composer.json.tmp"
  mv "$pkg/composer.json.tmp" "$pkg/composer.json"
  stamp "$pkg/runtime/src/Transport/RapUserAgent.php" \
    "s/public const SEMVER = '0\\.0\\.0';/public const SEMVER = '$VERSION';/" \
    "public const SEMVER = '$VERSION';"
  make_zip "$OUT/revaly-sdk-php.zip" "$pkg"
}

package_typescript() {
  command -v npm > /dev/null || die "npm not found"
  stage_tree
  local src="$WORK/languages/typescript"
  cp "$WORK/LICENSE" "$WORK/NOTICE" "$src/"
  # Version stamp + "type" flip to commonjs: tsconfig.build.json emits under
  # `nodenext`, where format follows package.json "type" — commonjs keeps the
  # generated core's extensionless relative imports legal (see that file's
  # header). The committed manifest keeps "type": "module" for dev.
  jq --arg v "$VERSION" '.version = $v | .type = "commonjs"' \
    "$src/package.json" > "$src/package.json.tmp"
  mv "$src/package.json.tmp" "$src/package.json"
  stamp "$src/runtime/src/version.ts" \
    "s/export const SDK_VERSION = '0\\.0\\.0';/export const SDK_VERSION = '$VERSION';/" \
    "export const SDK_VERSION = '$VERSION';"
  # npm pack runs prepack → tsconfig.build.json emits dist/ (CommonJS + d.ts);
  # "private": true stays — it blocks npm publish (repo rule 3), not npm pack.
  (cd "$src" && npm ci --no-audit --no-fund && npm pack --pack-destination "$OUT")
  mv "$OUT/revaly-sdk-$VERSION.tgz" "$OUT/revaly-sdk-typescript.tgz"
  # Packed-typings gate: the hand-written runtime's packed d.ts must compile
  # Node-only (no DOM lib). The generated core's d.ts DOM aliases are the
  # documented, deferred exception (README "TypeScript config note"), so only
  # diagnostics touching dist/runtime fail the gate. Runs the staged
  # devDependency tsc — no new tooling. Fail-closed: a nonzero tsc exit with
  # no TypeScript diagnostics at all means the gate itself failed to run.
  local checkdir="$src/.tgz-check" entry="package/dist/runtime/src/index.d.ts" tscout rc=0
  mkdir -p "$checkdir"
  tar -xzf "$OUT/revaly-sdk-typescript.tgz" -C "$checkdir"
  [ -f "$checkdir/$entry" ] \
    || die "packed tgz is missing $entry — cannot run the packed-typings gate"
  [ -f "$src/node_modules/typescript/bin/tsc" ] \
    || die "staged typescript devDependency missing — cannot run the packed-typings gate"
  # --ignoreConfig is load-bearing: tsc 7's config discovery walks ANCESTOR
  # directories, finds the dev tsconfig.json above the extraction dir, refuses
  # the CLI-files invocation (TS5112) and checks NOTHING — a silent pass.
  # Negative-control verified 2026-07-23: without the flag the v0.4.0 tgz's two
  # known runtime DOM-alias errors go undetected; with it they are reported.
  # (The staged tsc is the pinned 7.0.2 devDependency, so the flag is stable.)
  # cwd = the extracted package root, so diagnostics print tgz-relative paths;
  # @types/node resolves by walking up into the staged node_modules.
  tscout="$(cd "$checkdir/package" && node ../../node_modules/typescript/bin/tsc --noEmit --strict \
    --ignoreConfig --lib es2022 --types node dist/runtime/src/index.d.ts 2>&1)" || rc=$?
  if [ "$rc" -ne 0 ] && printf '%s\n' "$tscout" | grep 'error TS' | grep -vq 'dist/'; then
    printf '%s\n' "$tscout" | head -5 >&2
    die "packed-typings gate hit non-file tsc diagnostics — the check itself did not run; verification cannot proceed"
  fi
  if [ "$rc" -ne 0 ] && ! printf '%s\n' "$tscout" | grep -q 'error TS'; then
    printf '%s\n' "$tscout" >&2
    die "packed-typings gate produced no TypeScript diagnostics — tsc failed to run; verification cannot proceed"
  fi
  if printf '%s\n' "$tscout" | grep 'dist/runtime' | grep -q 'error TS'; then
    printf '%s\n' "$tscout" | grep 'dist/runtime' | head -5 >&2
    die "packed runtime d.ts is not Node-only clean — a DOM-only alias leaked into the hand-written runtime surface"
  fi
}

package_python() {
  local py
  py="$(resolve_python)" || die "no working python interpreter found"
  "$py" -m build --version > /dev/null 2>&1 \
    || die "python 'build' package not installed ($py -m pip install build)"
  stage_tree
  local src="$WORK/languages/python"
  cp "$WORK/LICENSE" "$WORK/NOTICE" "$src/"
  stamp "$src/pyproject.toml" \
    "s/^version = \"0\\.0\\.0\\.dev0\"/version = \"$VERSION\"/" \
    "version = \"$VERSION\""
  stamp "$src/runtime/revaly_sdk/_version.py" \
    "s/SDK_VERSION = \"0\\.0\\.0\\.dev0\"/SDK_VERSION = \"$VERSION\"/" \
    "SDK_VERSION = \"$VERSION\""
  # The "Private :: Do Not Upload" classifier stays in the artifact: it makes PyPI
  # reject any upload (embargo guard, repo rule 3) and is inert for file installs.
  (cd "$src" && "$py" -m build --outdir "$WORK/pydist")
  cp "$WORK/pydist/revaly_sdk-$VERSION.tar.gz" "$OUT/revaly-sdk-python.tar.gz" \
    || die "expected sdist revaly_sdk-$VERSION.tar.gz missing"
  cp "$WORK/pydist/revaly_sdk-$VERSION-py3-none-any.whl" "$OUT/" \
    || die "expected wheel revaly_sdk-$VERSION-py3-none-any.whl missing"
}

package_go() {
  stage_tree
  local src="$WORK/languages/go"
  cp "$WORK/LICENSE" "$WORK/NOTICE" "$src/"
  stamp "$src/internal/runtime/version.go" \
    "s/const Version = \"0\\.0\\.0-dev\"/const Version = \"$VERSION\"/" \
    "const Version = \"$VERSION\""
  # Source-module zip (go.mod at the archive root). Consumed via unzip + a local
  # `replace` directive; the go/vX.Y.Z release tag is inert to Go tooling — the
  # module-activating languages/go/vX.Y.Z form is reserved for the gated, last
  # registry publish (ADR-SDK-026).
  make_zip "$OUT/revaly-sdk-go.zip" "$src"
}

echo "== stage 5: packaging $LANG_ID $VERSION (tag $RELEASE_TAG) from ${SOURCE_COMMIT:0:7}"
"package_$LANG_ID"

# --- checksums (spec-release model: "<sha256>  <filename>", sha256sum -c ready) -

(
  cd "$OUT"
  for f in *; do
    case "$f" in
      *.sha256 | provenance.json | RELEASE_NOTES.md) continue ;;
    esac
    sha256sum "$f" > "$f.sha256"
  done
)

# --- provenance.json (mirrors the platform spec artifact's provenance model) ---

if [ "${GITHUB_ACTIONS:-}" = "true" ]; then
  # The package job runs only after stages 1–4 succeeded (workflow needs-chain);
  # the run URL is the audit trail for those jobs.
  GATE_VALUE="pass"
  CI_RUN_ID="${GITHUB_RUN_ID:-unknown}"
  CI_RUN_URL="${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-}/actions/runs/${GITHUB_RUN_ID:-}"
else
  GATE_VALUE="unverified-local-build"
  CI_RUN_ID="local"
  CI_RUN_URL="local"
fi

CHECKSUMS_JSON="$(
  cd "$OUT"
  for f in *.sha256; do
    jq -n --arg name "${f%.sha256}" --arg sha "$(awk '{print $1}' "$f")" \
      '{($name): ("sha256:" + $sha)}'
  done | jq -s 'add'
)"

jq -n \
  --arg language "$LANG_ID" \
  --arg packageVersion "$VERSION" \
  --arg releaseTag "$RELEASE_TAG" \
  --arg sourceCommit "$SOURCE_COMMIT" \
  --arg specRepo "$SPEC_REPO" \
  --arg specTag "$SPEC_TAG" \
  --arg specVersion "$SPEC_VERSION" \
  --arg specCommit "$SPEC_COMMIT" \
  --arg specSha "$SPEC_SHA256" \
  --arg genName "$GEN_NAME" \
  --arg genVersion "$GEN_VERSION" \
  --arg genDigest "$GEN_DIGEST" \
  --arg gate "$GATE_VALUE" \
  --arg ciRunId "$CI_RUN_ID" \
  --arg ciRunUrl "$CI_RUN_URL" \
  --argjson checksums "$CHECKSUMS_JSON" \
  '{
    language: $language,
    packageVersion: $packageVersion,
    releaseTag: $releaseTag,
    sourceCommit: $sourceCommit,
    spec: {
      repo: $specRepo,
      releaseTag: $specTag,
      specVersion: $specVersion,
      sourceCommit: $specCommit,
      checksums: { "openapi.bundled.yaml": ("sha256:" + $specSha) }
    },
    generator: { name: $genName, version: $genVersion, imageDigest: $genDigest },
    gates: {
      validate: $gate,
      generate: $gate,
      buildTest: $gate,
      contractSmoke: $gate
    },
    ciRunId: $ciRunId,
    ciRunUrl: $ciRunUrl,
    checksums: $checksums
  }' > "$OUT/provenance.json"

# --- release notes (stage 5 stamps the version → spec SHA mapping) -------------

case "$LANG_ID" in
  dotnet)
    INSTALL_SNIPPET="Download both nupkgs and their .sha256 files, verify, then use the folder as a local NuGet feed:

    dotnet nuget add source ./release-artifacts --name revaly-local
    dotnet add package Revaly.Sdk --version $VERSION" ;;
  java)
    INSTALL_SNIPPET="Download revaly-sdk-java.zip, verify its .sha256, unzip, then consume as a file repository (or unzip into ~/.m2/repository):

    <repository><id>revaly-local</id><url>file://\${basedir}/revaly-sdk-java</url></repository>
    <dependency><groupId>co.revaly</groupId><artifactId>revaly-sdk</artifactId><version>$VERSION</version></dependency>" ;;
  php)
    INSTALL_SNIPPET="Download revaly-sdk-php.zip, verify its .sha256, then:

    composer config repositories.revaly artifact ./release-artifacts/
    composer require revaly/sdk:$VERSION" ;;
  typescript)
    INSTALL_SNIPPET="Download revaly-sdk-typescript.tgz, verify its .sha256, then:

    npm install ./revaly-sdk-typescript.tgz" ;;
  python)
    INSTALL_SNIPPET="Download revaly-sdk-python.tar.gz, verify its .sha256, then:

    pip install ./revaly-sdk-python.tar.gz" ;;
  go)
    INSTALL_SNIPPET="Download revaly-sdk-go.zip, verify its .sha256, unzip (e.g. to ./third_party/revaly-sdk-go), then:

    go mod edit -replace github.com/revaly-co/rap-sdk/languages/go=./third_party/revaly-sdk-go
    go get github.com/revaly-co/rap-sdk/languages/go" ;;
esac

ASSET_TABLE="$(
  cd "$OUT"
  for f in *.sha256; do
    printf '| `%s` | `%s` |\n' "${f%.sha256}" "$(awk '{print $1}' "$f")"
  done
)"

if [ "$GATE_VALUE" = "pass" ]; then
  GATE_SENTENCE="Stages 1–4 (validate, generate ×6, build+test ×6, contract smoke ×6) passed on
this run before packaging — any language red blocks every language's release."
else
  GATE_SENTENCE="**Local build — stages 1–4 were NOT verified on this run** (provenance gates
read \`$GATE_VALUE\`). Only CI runs from a release tag publish releases."
fi

cat > "$OUT/RELEASE_NOTES.md" <<EOF
Interim distribution artifact (ADR-SDK-026): registry publish remains embargoed
(repo rule 3) — this GitHub release is the supported install channel. Registry
names are **final** (ADR-SDK-030) and registry publish goes live when the
rule-3 gates close (the stage-6 registry job runs dark until then,
ADR-SDK-031); GitHub releases continue as the provenance anchor afterwards.

## Traceability (version → spec)

| | |
| --- | --- |
| SDK package version | \`$VERSION\` (\`$RELEASE_TAG\`) |
| rap-sdk source commit | \`$SOURCE_COMMIT\` |
| Spec artifact | \`$SPEC_TAG\` (spec \`$SPEC_VERSION\`, \`$SPEC_REPO@${SPEC_COMMIT:0:7}\`) |
| Generator | $GEN_NAME \`$GEN_VERSION\` (digest-pinned) |
| Pipeline run | $CI_RUN_URL |

$GATE_SENTENCE

## Assets

| asset | sha256 |
| --- | --- |
$ASSET_TABLE

Verify: \`sha256sum -c <asset>.sha256\` next to the downloaded files.
\`provenance.json\` carries the full spec + generator + gate trail.

## Install (interim)

$INSTALL_SNIPPET

See \`languages/$LANG_ID/README.md\` for the quickstart (charge + all three
error classes + reconcile, ≤ 15 minutes).
EOF

echo "== stage 5 complete: $(ls "$OUT" | tr '\n' ' ')"
echo "   dist/$LANG_ID ready for the GitHub release ($RELEASE_TAG)"
