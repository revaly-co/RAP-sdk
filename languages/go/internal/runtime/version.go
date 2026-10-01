package runtime

import (
	"runtime/debug"
	"strings"
	"sync"
)

// Version is the SDK package version reported in the User-Agent product token
// (ADR-SDK-005). Go release identity comes from the release tags (`go/vX.Y.Z`
// for the GitHub release, `languages/go/vX.Y.Z` for the module); the tree
// between releases carries this placeholder, and stage 5 stamps the real
// version into the GitHub release zip only. A module-proxy install builds the
// unstamped tag tree, so the User-Agent resolves its version through
// SDKVersion instead of reading this constant directly.
const Version = "0.0.0-dev"

// ModulePath is this module's path, as consumers require it.
const ModulePath = "github.com/revaly-co/rap-sdk/languages/go"

// placeholderVersion is what Version holds in an unstamped tree. Kept separate
// from Version, which stage 5 rewrites, so a stamped build still knows it is
// stamped.
const placeholderVersion = "0.0.0-dev"

var sdkVersion = sync.OnceValue(func() string {
	info, ok := debug.ReadBuildInfo()
	return ResolveVersion(Version, info, ok)
})

// SDKVersion is the version the User-Agent reports, resolved once per process.
func SDKVersion() string { return sdkVersion() }

// ResolveVersion picks the version to report (SC-624). A stamped build (the
// GitHub release zip, consumed through a local replace) carries its version in
// the constant, which wins. An unstamped build is either a module-proxy install,
// where the Go toolchain records the real module version in the consumer's
// build info, or a local or in-repo build, which has no module version and
// keeps the placeholder. Exported for the tests only; the package is internal.
func ResolveVersion(stamped string, info *debug.BuildInfo, ok bool) string {
	if stamped != placeholderVersion || !ok || info == nil {
		return stamped
	}
	for _, dep := range info.Deps {
		if dep.Path != ModulePath {
			continue
		}
		mod := dep
		if dep.Replace != nil {
			mod = dep.Replace
		}
		// Module versions are "v" + semver (pseudo-versions included); a local
		// replace has none, and "(devel)" is not a version.
		if v, found := strings.CutPrefix(mod.Version, "v"); found && v != "" && v[0] >= '0' && v[0] <= '9' {
			return v
		}
		return stamped
	}
	return stamped
}
