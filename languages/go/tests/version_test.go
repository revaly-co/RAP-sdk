package tests

import (
	"regexp"
	"runtime/debug"
	"testing"

	"github.com/revaly-co/rap-sdk/languages/go/internal/runtime"
)

// The <semver> token of the ADR-SDK-005 User-Agent grammar, release and
// pre-release (Go pseudo-versions are semver pre-releases).
var semverToken = regexp.MustCompile(`^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$`)

func buildInfo(deps ...*debug.Module) *debug.BuildInfo {
	return &debug.BuildInfo{Main: debug.Module{Path: "example.com/merchant-app", Version: "(devel)"}, Deps: deps}
}

func sdkDep(version string, replace *debug.Module) *debug.Module {
	return &debug.Module{Path: runtime.ModulePath, Version: version, Replace: replace}
}

// SC-624: a module-proxy install builds the unstamped tag tree, so the
// User-Agent version must come from the consumer's build info; a stamped build
// (the GitHub release zip) and builds with no module version keep the constant.
func TestResolveVersion(t *testing.T) {
	const placeholder = "0.0.0-dev"
	cases := []struct {
		name    string
		stamped string
		info    *debug.BuildInfo
		ok      bool
		want    string
	}{
		{"proxy install reports the module version", placeholder,
			buildInfo(sdkDep("v0.7.0", nil)), true, "0.7.0"},
		{"pseudo-version (commit pin) is reported as-is", placeholder,
			buildInfo(sdkDep("v0.7.1-0.20261001160000-099ea43a4d61", nil)), true,
			"0.7.1-0.20261001160000-099ea43a4d61"},
		{"stamped GitHub zip wins over build info", "0.7.0",
			buildInfo(sdkDep("v0.9.9", nil)), true, "0.7.0"},
		{"stamped GitHub zip via local replace keeps its stamp", "0.7.0",
			buildInfo(sdkDep("v0.0.0-00010101000000-000000000000", &debug.Module{Path: "./third_party/revaly-sdk-go"})), true, "0.7.0"},
		{"unstamped local replace has no module version", placeholder,
			buildInfo(sdkDep("v0.0.0-00010101000000-000000000000", &debug.Module{Path: "../rap-sdk/languages/go"})), true, placeholder},
		{"replace by a versioned fork reports the fork's version", placeholder,
			buildInfo(sdkDep("v0.7.0", &debug.Module{Path: "github.com/example/fork", Version: "v1.2.3"})), true, "1.2.3"},
		{"(devel) is not a version", placeholder,
			buildInfo(sdkDep("(devel)", nil)), true, placeholder},
		{"no build info", placeholder, nil, false, placeholder},
		{"nil build info reported as ok", placeholder, nil, true, placeholder},
		{"SDK is the main module (in-repo build)", placeholder,
			&debug.BuildInfo{Main: debug.Module{Path: runtime.ModulePath, Version: "(devel)"}}, true, placeholder},
		{"other dependencies only", placeholder,
			buildInfo(&debug.Module{Path: "github.com/google/uuid", Version: "v1.6.0"}), true, placeholder},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got := runtime.ResolveVersion(tc.stamped, tc.info, tc.ok)
			if got != tc.want {
				t.Fatalf("ResolveVersion = %q, want %q", got, tc.want)
			}
			if !semverToken.MatchString(got) {
				t.Fatalf("%q is not an ADR-SDK-005 <semver> token", got)
			}
		})
	}
}

// In this repository the SDK is the main module, so the User-Agent keeps the
// placeholder (the transport-header test pins the full string).
func TestSDKVersionInRepoIsThePlaceholder(t *testing.T) {
	if got := runtime.SDKVersion(); got != "0.0.0-dev" {
		t.Fatalf("SDKVersion() = %q in-repo, want the 0.0.0-dev placeholder", got)
	}
}
