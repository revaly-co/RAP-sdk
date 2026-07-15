#!/usr/bin/env bash
# Stage 2 — generate the six language cores (docs/pipeline-and-release.md §2).
#
# The only generation entry point, local and CI alike:
#   pipeline/generate.sh [--spec <path>] [language ...]     (default: all six)
#
# Guarantees (fail-closed, ADR-SDK-006/023):
#   * the spec input is the pinned gated artifact — downloaded from the pinned release
#     (or taken from --spec) and sha256-verified against spec/pin.yaml BEFORE any
#     generation; a mismatch refuses the run;
#   * the generator runs from the digest-pinned image in pipeline/generator-pin.yaml —
#     never a floating tag, never a local install;
#   * each languages/<lang>/core/ is wiped and fully regenerated, so deleted upstream
#     files surface in the regeneration diff (ADR-SDK-001).
#
# Requires: docker; gh (authenticated, or GH_TOKEN with read access to the platform
# repo) unless --spec is given. On Windows run from Git Bash.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SPEC_PIN=spec/pin.yaml
GEN_PIN=pipeline/generator-pin.yaml
ALL_LANGS="dotnet java php typescript python go"

die() { echo "ERROR: $*" >&2; exit 1; }

usage() {
  sed -n '2,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

SPEC_PATH=""
LANGS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --spec)
      [ $# -ge 2 ] || die "--spec requires a path"
      SPEC_PATH="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    -*) die "unknown option: $1" ;;
    *) LANGS="$LANGS $1"; shift ;;
  esac
done
[ -n "$LANGS" ] || LANGS="$ALL_LANGS"
for LANG_ID in $LANGS; do
  case " $ALL_LANGS " in
    *" $LANG_ID "*) ;;
    *) die "unknown language '$LANG_ID' (expected one of: $ALL_LANGS)" ;;
  esac
done

# --- read the pins (same parsing style as pipeline stage 1) -----------------------------
for f in "$SPEC_PIN" "$GEN_PIN"; do
  [ -f "$f" ] || die "$f is missing — the pin set is incomplete."
done
PIN_REPO=$(grep -m1 -E '^repo:' "$SPEC_PIN" | awk '{print $2}')
PIN_TAG=$(grep -m1 -E '^releaseTag:' "$SPEC_PIN" | awk '{print $2}')
PIN_SHA=$(grep -m1 -E '^  openapi\.bundled\.yaml:' "$SPEC_PIN" | awk '{print $2}')
GEN_IMAGE=$(grep -m1 -E '^image:' "$GEN_PIN" | awk '{print $2}')
GEN_DIGEST=$(grep -m1 -E '^imageDigest:' "$GEN_PIN" | awk '{print $2}')
for v in "$PIN_REPO" "$PIN_TAG" "$PIN_SHA" "$GEN_IMAGE" "$GEN_DIGEST"; do
  [ -n "$v" ] || die "a required pin field is empty (spec/pin.yaml or pipeline/generator-pin.yaml)."
done
# Run by digest only (ADR-SDK-023) — the tag part of `image:` is documentation.
IMAGE_REF="${GEN_IMAGE%%:*}@${GEN_DIGEST}"

# --- resolve + verify the spec artifact (ADR-SDK-006: verify BEFORE generating) ---------
if [ -z "$SPEC_PATH" ]; then
  CACHE_DIR="$REPO_ROOT/.spec-work/$(printf '%s' "$PIN_TAG" | tr '/' '_')"
  SPEC_PATH="$CACHE_DIR/openapi.bundled.yaml"
  CACHED_SHA=""
  [ -f "$SPEC_PATH" ] && CACHED_SHA=$(sha256sum "$SPEC_PATH" | awk '{print $1}')
  if [ "$CACHED_SHA" != "$PIN_SHA" ]; then
    command -v gh >/dev/null 2>&1 || die "gh is required to download the pinned artifact (or pass --spec <path>)."
    rm -rf "$CACHE_DIR"; mkdir -p "$CACHE_DIR"
    echo "==> Downloading pinned artifact: $PIN_REPO @ $PIN_TAG"
    gh release download "$PIN_TAG" --repo "$PIN_REPO" --pattern openapi.bundled.yaml --dir "$CACHE_DIR"
  fi
fi
[ -f "$SPEC_PATH" ] || die "spec artifact not found: $SPEC_PATH"
ACTUAL_SHA=$(sha256sum "$SPEC_PATH" | awk '{print $1}')
[ "$ACTUAL_SHA" = "$PIN_SHA" ] || die "spec artifact sha256 ($ACTUAL_SHA) does not match spec/pin.yaml ($PIN_SHA) — refusing to generate (ADR-SDK-006)."
echo "==> Spec artifact verified: $PIN_TAG (sha256 ${PIN_SHA:0:12}…)"
echo "==> Generator toolchain: $IMAGE_REF"

# --- docker invocation plumbing ----------------------------------------------------------
SPEC_DIR="$(cd "$(dirname "$SPEC_PATH")" && pwd)"
SPEC_FILE="$(basename "$SPEC_PATH")"

# Git Bash (MSYS) rewrites container paths like /local unless conversion is disabled;
# Docker Desktop wants Windows-style host paths on the left of -v.
host_path() {
  if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else printf '%s\n' "$1"; fi
}
HOST_REPO="$(host_path "$REPO_ROOT")"
HOST_SPEC_DIR="$(host_path "$SPEC_DIR")"
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) export MSYS_NO_PATHCONV=1 ;; esac

# On Linux CI, run as the invoking user so the regenerated tree stays diffable/cleanable.
DOCKER_USER=""
if [ "$(uname -s)" = "Linux" ]; then DOCKER_USER="--user $(id -u):$(id -g)"; fi

# --- generate ----------------------------------------------------------------------------
for LANG_ID in $LANGS; do
  OUT_DIR="languages/$LANG_ID/core"
  CFG_DIR="pipeline/$LANG_ID"
  for f in "$CFG_DIR/config.yaml" "$CFG_DIR/.openapi-generator-ignore"; do
    [ -f "$f" ] || die "$f is missing."
  done
  echo "==> [$LANG_ID] regenerating $OUT_DIR"
  rm -rf "$OUT_DIR"
  mkdir -p "$OUT_DIR"
  # shellcheck disable=SC2086  # DOCKER_USER intentionally word-splits
  docker run --rm $DOCKER_USER \
    -v "$HOST_REPO:/local" \
    -v "$HOST_SPEC_DIR:/spec:ro" \
    "$IMAGE_REF" generate \
    -i "/spec/$SPEC_FILE" \
    -c "/local/$CFG_DIR/config.yaml" \
    -t "/local/$CFG_DIR/templates" \
    -o "/local/$OUT_DIR" \
    --ignore-file-override "/local/$CFG_DIR/.openapi-generator-ignore" \
    > /dev/null
  FILE_COUNT=$(find "$OUT_DIR" -type f | wc -l | tr -d ' ')
  echo "==> [$LANG_ID] done ($FILE_COUNT files)"
done

echo "==> Generation complete: $LANGS"
echo "    Regeneration diff = 'git status --porcelain -- languages/' (must be empty on a clean tree)."
