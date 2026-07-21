package runtime

import (
	"fmt"
	goruntime "runtime"
)

// buildUserAgent renders the exact ADR-SDK-005 grammar:
//
//	revaly-sdk-go/<semver> (<runtime-version>; <os>)
//
// The string is a contract with platform adoption dashboards — it is force-set
// at the transport layer so the generated core cannot bypass or replace it, and
// it carries only the coarse tokens below (no hostnames, no distro
// fingerprints).
func buildUserAgent() string {
	return fmt.Sprintf("revaly-sdk-go/%s (%s; %s)", Version, goruntime.Version(), osToken())
}

// osToken maps GOOS to the ADR-SDK-005 coarse platform tokens
// (linux / windows / darwin / other).
func osToken() string {
	switch goruntime.GOOS {
	case "linux", "windows", "darwin":
		return goruntime.GOOS
	default:
		return "other"
	}
}
