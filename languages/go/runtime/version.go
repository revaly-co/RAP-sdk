package runtime

// Version is the SDK package version reported in the User-Agent product token
// (ADR-SDK-005). Go release identity comes from per-language tags cut in
// pipeline stage 5 (`go/vX.Y.Z`); until the publish gates close (repo rule 3)
// the tree carries the embargo placeholder.
const Version = "0.0.0-dev"
