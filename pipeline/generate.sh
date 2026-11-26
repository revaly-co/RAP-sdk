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

# count_matches ERE FILE... : how many times ERE occurs across the FILEs. Zero is an
# answer; an unreadable FILE is not (cat fails, and pipefail fails the assignment that
# calls this). Always call it in an assignment: N=$(count_matches ...).
count_matches() {
  local re="$1"; shift
  cat -- "$@" | { grep -o -E -- "$re" || true; } | wc -l | tr -d ' '
}

# fail_if_found ERE MESSAGE FILE... : print every line of the FILEs that matches ERE
# (file:line:text, on stderr), then stop generation with MESSAGE. A grep error stops
# generation too.
fail_if_found() {
  local re="$1" msg="$2" rc=0; shift 2
  grep -n -E -- "$re" "$@" >&2 || rc=$?
  [ "$rc" -eq 1 ] || die "$msg"
}

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
  if [ "$LANG_ID" = "python" ]; then
    # ADR-SDK-034 (SC-886): an SDK never refuses a request because a model field is longer
    # than the spec's maxLength; the platform decides. The python generator hands the model
    # template each field's whole declaration as one precomputed string (x-py-typing), so a
    # template fork cannot drop one constraint. This step removes `max_length=N` from string
    # annotations (`Annotated[str, Field(...)]`) in models/ only (never api/: path and query
    # parameter checks stay), inside the same pinned image so the bytes match on every host.
    # Any max_length left anywhere in models/ (a list bound, or a shape this pattern misses)
    # fails generation instead of passing silently.
    PY_MODELS="$OUT_DIR/revaly_sdk_core/models"
    [ -d "$PY_MODELS" ] || die "python models directory $PY_MODELS not found (package rename?)."
    # shellcheck disable=SC2086  # DOCKER_USER intentionally word-splits
    docker run --rm $DOCKER_USER --entrypoint sh \
      -v "$HOST_REPO:/local" \
      "$IMAGE_REF" -c \
      "find '/local/$PY_MODELS' -name '*.py' -exec sed -E -i '/^    [a-z_0-9]+: /s/Annotated\[str, Field\(([^()]*), max_length=[0-9]+\)\]/Annotated[str, Field(\1)]/' {} +"
    if grep -rnE 'max_length=[0-9]' "$PY_MODELS" > /dev/null; then
      die "max_length survived in $PY_MODELS (ADR-SDK-034); extend the strip pattern."
    fi
    # ADR-SDK-034 amendment of 2026-11-26 (SC-1018): for the rtnData block (RtnData and its
    # ten nested models, the only schemas the platform exempts) the SDK never refuses a
    # value because it breaks a documented pattern, minimum or minLength; the platform
    # decides. In models/rtn_data*.py only, this step removes `ge=N` and `min_length=N` from
    # the field annotations (`Field(strict=True, ge=N)` and `Field(min_length=N, strict=True)`
    # both become `Field(strict=True)`) and deletes each `_validate_regular_expression`
    # validator together with the blank line before it, which is exactly what the template's
    # x-regex section prints. `strict=True` (the type check), the datetime type and the enum
    # validators stay. It runs after the SC-886 step, whose output shape
    # (`Field(min_length=N, strict=True)`) it matches, inside the same pinned image, and the
    # program reaches perl on stdin so no host shell or Windows command line rewrites it.
    # Generation fails if the glob matches no file, if a ge=, gt=, min_length= or regex
    # validator survives in the family, if the strict=True or enum validator count moves, or
    # if the family's line count is not the old count less 13 per regex validator. These
    # checks cannot see an edit that keeps the line count; the tests pin the rest (types on
    # construction, assignment and from_dict). Re-check the patterns on any generator upgrade.
    PY_RTN=( "$PY_MODELS"/rtn_data*.py )
    [ -f "${PY_RTN[0]}" ] || die "no $PY_MODELS/rtn_data*.py: the rtnData family was renamed or moved; fix the SC-1018 step's glob (ADR-SDK-034)."
    PY_STRICT=$(count_matches 'strict=True' "${PY_RTN[@]}")
    PY_ENUMS=$(count_matches '_validate_enum\(cls, value\):' "${PY_RTN[@]}")
    PY_REGEX=$(count_matches '_validate_regular_expression\(cls, value\):' "${PY_RTN[@]}")
    PY_LINES=$(cat -- "${PY_RTN[@]}" | wc -l | tr -d ' ')
    # shellcheck disable=SC2086  # DOCKER_USER intentionally word-splits
    docker run --rm -i $DOCKER_USER --entrypoint perl \
      -v "$HOST_REPO:/local" -w /local \
      "$IMAGE_REF" -0777 -i -p - "${PY_RTN[@]}" <<'PERL'
s/(Annotated\[\w+, )Field\(strict=True, ge=-?[0-9.]+\)\]/${1}Field(strict=True)]/g;
s/(Annotated\[\w+, )Field\(min_length=[0-9]+, strict=True\)\]/${1}Field(strict=True)]/g;
s/^\n    \@field_validator\('([a-z_0-9]+)'\)\n    def \1_validate_regular_expression\(cls, value\):\n        """Validates the regular expression"""\n        if value is None:\n            return value\n\n        if not isinstance\(value, str\):\n            value = str\(value\)\n\n        if not re\.match\(r"[^\n]*", value\):\n            raise ValueError\(r"must validate the regular expression [^\n]*"\)\n        return value\n//mg;
PERL
    fail_if_found '\bg[et]=|min_length=|_validate_regular_expression' \
      "a pattern, minimum or minLength check survived in $PY_MODELS/rtn_data*.py (lines above): extend the SC-1018 step's patterns (ADR-SDK-034)." \
      "${PY_RTN[@]}"
    N=$(count_matches 'strict=True' "${PY_RTN[@]}")
    [ "$N" = "$PY_STRICT" ] || die "the SC-1018 step changed the strict=True count in $PY_MODELS/rtn_data*.py from $PY_STRICT to $N: it removed a type check (ADR-SDK-034 keeps types)."
    N=$(count_matches '_validate_enum\(cls, value\):' "${PY_RTN[@]}")
    [ "$N" = "$PY_ENUMS" ] || die "the SC-1018 step changed the enum validator count in $PY_MODELS/rtn_data*.py from $PY_ENUMS to $N."
    N=$(cat -- "${PY_RTN[@]}" | wc -l | tr -d ' ')
    [ "$N" = "$((PY_LINES - 13 * PY_REGEX))" ] || die "$PY_MODELS/rtn_data*.py has $N lines after the SC-1018 step, expected $((PY_LINES - 13 * PY_REGEX)) ($PY_LINES less 13 for each of the $PY_REGEX regex validators): the step removed or added other lines."
  fi
  FILE_COUNT=$(find "$OUT_DIR" -type f | wc -l | tr -d ' ')
  echo "==> [$LANG_ID] done ($FILE_COUNT files)"
done

echo "==> Generation complete: $LANGS"
echo "    Regeneration diff = 'git status --porcelain -- languages/' (must be empty on a clean tree)."
