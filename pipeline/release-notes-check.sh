#!/usr/bin/env bash
# release-notes-check.sh — published release notes vs the real distribution state (SC-517).
#
# Usage: pipeline/release-notes-check.sh [--tag <lang>/vX.Y.Z] [--min-age-hours N]
#
# For every per-language GitHub release from FIRST_REGISTRY_VERSION on (or just
# --tag), asserts the note matches what the registry actually serves:
#   - no pre-flip wording (embargo, interim channel, local-feed installs);
#   - version ON the registry   -> the note carries the exact install line from
#                                  pipeline/release-notes.sh (rn_install_cmd), as
#                                  its own indented code line (whole-line match,
#                                  so 0.6.1 never matches 0.6.10);
#   - version NOT on the registry -> the note says so (rn_not_published_marker)
#                                  and advertises no registry install.
# Releases younger than --min-age-hours (default 6) are skipped: Maven Central
# and the Go proxy take time to serve a fresh version, and a still-running
# release would otherwise read as drift.
#
# Exit 0 = every checked note matches; 1 = drift or an unreadable registry
# (each finding printed, and appended to $GITHUB_STEP_SUMMARY when set).
# Read-only: GitHub release reads + anonymous public registry GETs.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=pipeline/release-notes.sh
. "$REPO_ROOT/pipeline/release-notes.sh"

REPO="${GITHUB_REPOSITORY:-revaly-co/RAP-sdk}"
# The first version any registry carries (the 2026-08-07 flip). Earlier
# releases exist only as GitHub releases, and their notes were accurate when
# written, so they are out of scope.
FIRST_REGISTRY_VERSION="0.5.1"
FORBIDDEN='embargo|interim distribution|install \(interim\)|dark until|runs dark|supported install channel|nuget add source|go mod edit -replace|composer config repositories'

ONLY_TAG=""
MIN_AGE_HOURS=6
while [ $# -gt 0 ]; do
  case "$1" in
    --tag) ONLY_TAG="$2"; shift 2 ;;
    --min-age-hours) MIN_AGE_HOURS="$2"; shift 2 ;;
    -h|--help) sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

# Prints yes / no / unknown. 404 is the only "no"; anything else non-200 is
# unknown, so a registry outage never reads as a missing release.
registry_has() {
  local lang="$1" v="$2" url code
  case "$lang" in
    dotnet)     url="https://api.nuget.org/v3-flatcontainer/revaly.sdk/$v/revaly.sdk.nuspec" ;;
    java)       url="https://repo1.maven.org/maven2/co/revaly/revaly-sdk/$v/revaly-sdk-$v.pom" ;;
    typescript) url="https://registry.npmjs.org/@revaly%2Fsdk/$v" ;;
    python)     url="https://pypi.org/pypi/revaly-sdk/$v/json" ;;
    go)         url="https://proxy.golang.org/github.com/revaly-co/rap-sdk/languages/go/@v/v$v.info" ;;
    php)
      # Packagist has no per-version endpoint; the p2 metadata lists every tag.
      local json
      if ! json="$(curl -fsS --retry 2 --max-time 30 "https://repo.packagist.org/p2/revaly/sdk.json")"; then
        echo unknown; return
      fi
      if jq -e --arg v "$v" '.packages["revaly/sdk"] | any(.version == $v or .version == ("v" + $v))' >/dev/null <<<"$json"; then
        echo yes
      else
        echo no
      fi
      return ;;
  esac
  code="$(curl -sS -o /dev/null -w '%{http_code}' --retry 2 --max-time 30 "$url" || true)"
  case "$code" in
    200) echo yes ;;
    404) echo no ;;
    *)   echo unknown ;;
  esac
}

if [ -n "$ONLY_TAG" ]; then
  RELEASES="$(gh release view "$ONLY_TAG" --repo "$REPO" --json tagName,createdAt --jq '"\(.tagName) \(.createdAt)"')"
  MIN_AGE_HOURS=0
else
  RELEASES="$(gh release list --repo "$REPO" --limit 1000 --json tagName,createdAt --jq '.[] | "\(.tagName) \(.createdAt)"')"
fi

NOW="$(date -u +%s)"
FINDINGS=()
CHECKED=0
SKIPPED=0

while read -r TAG CREATED; do
  [ -n "$TAG" ] || continue
  if ! [[ "$TAG" =~ ^(dotnet|java|php|typescript|python|go)/v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
    continue
  fi
  LANG_ID="${BASH_REMATCH[1]}"
  VERSION="${BASH_REMATCH[2]}"
  if [ "$(printf '%s\n%s\n' "$FIRST_REGISTRY_VERSION" "$VERSION" | sort -V | head -1)" != "$FIRST_REGISTRY_VERSION" ]; then
    continue
  fi
  AGE_HOURS=$(( (NOW - $(date -u -d "$CREATED" +%s)) / 3600 ))
  if [ "$AGE_HOURS" -lt "$MIN_AGE_HOURS" ]; then
    echo "skip  $TAG (released ${AGE_HOURS}h ago, under --min-age-hours $MIN_AGE_HOURS)"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  BODY="$(gh release view "$TAG" --repo "$REPO" --json body --jq .body)"
  BODY="${BODY//$'\r'/}"   # notes edited in the web UI come back CRLF
  INSTALL="$(rn_install_cmd "$LANG_ID" "$VERSION")"
  INSTALL_LINE="    $INSTALL"   # rn_install_section prints it as an indented code line
  MARKER="$(rn_not_published_marker "$LANG_ID")"
  REGISTRY="$(rn_registry "$LANG_ID")"
  HAS="$(registry_has "$LANG_ID" "$VERSION")"
  BEFORE=${#FINDINGS[@]}

  if HIT="$(grep -o -i -E -m1 "$FORBIDDEN" <<<"$BODY")"; then
    FINDINGS+=("$TAG: note still carries pre-flip wording (\"${HIT%%$'\n'*}\")")
  fi
  case "$HAS" in
    yes)
      grep -q -x -F -- "$INSTALL_LINE" <<<"$BODY" ||
        FINDINGS+=("$TAG: $VERSION is on $REGISTRY but the note does not give the registry install (\`$INSTALL\`)") ;;
    no)
      if grep -q -x -F -- "$INSTALL_LINE" <<<"$BODY"; then
        FINDINGS+=("$TAG: note tells developers to install from $REGISTRY, which does not serve $VERSION")
      elif ! grep -q -F -- "$MARKER" <<<"$BODY"; then
        FINDINGS+=("$TAG: $VERSION is not on $REGISTRY and the note does not say so ($MARKER)")
      fi ;;
    *)
      FINDINGS+=("$TAG: could not read $REGISTRY for $VERSION (registry unreachable or erroring) — inconclusive") ;;
  esac

  if [ ${#FINDINGS[@]} -eq "$BEFORE" ]; then
    echo "ok    $TAG (on $REGISTRY: $HAS)"
  else
    echo "DRIFT $TAG (on $REGISTRY: $HAS)"
  fi
  CHECKED=$((CHECKED + 1))
done <<<"$RELEASES"

echo
echo "checked $CHECKED release(s), skipped $SKIPPED as too recent, ${#FINDINGS[@]} finding(s)."

if [ ${#FINDINGS[@]} -gt 0 ]; then
  for f in "${FINDINGS[@]}"; do echo "::error::$f"; done
  if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
    {
      echo "## Release-notes drift"
      echo
      for f in "${FINDINGS[@]}"; do echo "- $f"; done
    } >> "$GITHUB_STEP_SUMMARY"
  fi
  exit 1
fi
