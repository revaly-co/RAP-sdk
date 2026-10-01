#!/usr/bin/env bash
# Shared release-notes text — sourced, never executed.
#
# One source for what a correct per-language release note says, used by both
# stage 5 (package.sh writes RELEASE_NOTES.md) and the published-notes drift
# check (release-notes-check.sh). The check looks for the exact install line
# these functions emit, so the generator and the check cannot disagree.
#
# Since the 2026-08-07 flip (ADR-SDK-031) every release is published to its
# registry; the GitHub release is the provenance anchor and the
# registry-outage fallback (ADR-SDK-026 as amended 2026-10-01, SC-517).
# Names are ADR-SDK-030; keep them in step with notify-teams-on-release.yml.

rn_registry() {
  case "$1" in
    dotnet)     echo "NuGet" ;;
    java)       echo "Maven Central" ;;
    php)        echo "Packagist" ;;
    typescript) echo "npm" ;;
    python)     echo "PyPI" ;;
    go)         echo "the Go module proxy" ;;
    *) return 1 ;;
  esac
}

rn_package() {
  case "$1" in
    dotnet)     echo "Revaly.Sdk" ;;
    java)       echo "co.revaly:revaly-sdk" ;;
    php)        echo "revaly/sdk" ;;
    typescript) echo "@revaly/sdk" ;;
    python)     echo "revaly-sdk" ;;
    go)         echo "github.com/revaly-co/rap-sdk/languages/go" ;;
    *) return 1 ;;
  esac
}

# The one install line per ecosystem, pinned to the release's version. The
# drift check requires this exact string in a note whose version the registry
# serves (for java: the Gradle form; the Maven block is printed alongside it).
rn_install_cmd() {
  local lang="$1" version="$2"
  case "$lang" in
    dotnet)     echo "dotnet add package Revaly.Sdk --version $version" ;;
    java)       echo "implementation(\"co.revaly:revaly-sdk:$version\")" ;;
    php)        echo "composer require revaly/sdk:$version" ;;
    typescript) echo "npm install @revaly/sdk@$version" ;;
    python)     echo "pip install revaly-sdk==$version" ;;
    go)         echo "go get github.com/revaly-co/rap-sdk/languages/go@v$version" ;;
    *) return 1 ;;
  esac
}

# Marker a note carries when its version is NOT on the registry (a failed
# registry leg is never re-run — fix, new tag; precedent: typescript 0.5.2,
# registry-provisioning.md § Known deviation). The drift check accepts a
# missing registry version only when the note says so with this marker.
rn_not_published_marker() {
  echo "**Not published to $(rn_registry "$1").**"
}

rn_preamble() {
  local lang="$1" version="$2"
  cat <<EOF
\`$(rn_package "$lang")\` $version is published on $(rn_registry "$lang") — install it from
there (below). This GitHub release is the provenance anchor and registry-outage fallback
(ADR-SDK-031): each asset carries a \`.sha256\` checksum, and \`provenance.json\` ties it to
the exact source commit and spec artifact it was built from.
EOF
}

# $3 = the release's source commit, so the quickstart link resolves to the
# README as it was at that release.
rn_install_section() {
  local lang="$1" version="$2" commit="$3"
  local repo="${GITHUB_REPOSITORY:-revaly-co/RAP-sdk}"
  echo "## Install"
  echo
  echo "From $(rn_registry "$lang"):"
  echo
  case "$lang" in
    java)
      cat <<EOF
    <dependency>
      <groupId>co.revaly</groupId>
      <artifactId>revaly-sdk</artifactId>
      <version>$version</version>
    </dependency>

or with Gradle:

    $(rn_install_cmd java "$version")

Artifacts are GPG-signed (\`packages@revaly.co\`).
EOF
      ;;
    dotnet)
      echo "    $(rn_install_cmd dotnet "$version")"
      echo
      echo "The generated core, \`Revaly.Sdk.Core\`, comes in as a dependency."
      ;;
    *)
      echo "    $(rn_install_cmd "$lang" "$version")"
      ;;
  esac
  cat <<EOF

Quickstart (a charge, all three error classes, and reconcile, in under 15 minutes):
[\`languages/$lang/README.md\`](https://github.com/$repo/blob/$commit/languages/$lang/README.md).
EOF
}
