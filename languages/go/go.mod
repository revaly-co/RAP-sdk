// Module root for the Go SDK — one subdir module per ADR-SDK-016; the generated core
// (core/, generated with withGoMod=false) and the hand-written runtime are packages of
// this single module. The path is the canonical home (ADR-SDK-022): nothing publishes
// until the publish gates close, and Go module paths are the highest-permanence
// identifier (publish last, ADR-SDK-015).
module github.com/revaly-co/rap-sdk/languages/go

go 1.21

require gopkg.in/validator.v2 v2.0.1
