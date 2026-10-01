package runtime

// Version is the SDK package version reported in the User-Agent product token
// (ADR-SDK-005). Go release identity comes from the release tags (`go/vX.Y.Z`
// for the GitHub release, `languages/go/vX.Y.Z` for the module); the tree
// between releases carries this placeholder.
const Version = "0.0.0-dev"
