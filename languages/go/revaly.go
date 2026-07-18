// Package revaly is the RAP Integration SDK for Go — the one-package merchant
// surface (runtime-tdd §2): construction, the typed failure classes, and the
// reconcile contract re-exported from the hand-written runtime, plus the
// payment-path request/response models re-exported from the generated core.
//
//	import revaly "github.com/revaly-co/rap-sdk/languages/go"
//
// The full generated V2 surface (payment methods, transactions, notify) is
// reachable through Client.Core(); the mock transport for merchant tests lives
// in the companion package
// github.com/revaly-co/rap-sdk/languages/go/runtime/raptest.
//
// The safety contract this SDK implements — the three failure classes, the
// classification algorithm, and the reconcile procedure — is
// docs/failover-contract.md; the quickstart in this directory's README walks
// the full failover + reconcile path.
package revaly

import (
	core "github.com/revaly-co/rap-sdk/languages/go/core"
	"github.com/revaly-co/rap-sdk/languages/go/runtime"
)

// Version is the SDK package version (embargo placeholder until per-language
// release tags exist — repo rule 3).
const Version = runtime.Version

// Client construction and configuration (runtime-tdd §1).
type (
	Client = runtime.Client
	Config = runtime.Config
)

// NewClient validates the configuration and builds a client. One client per
// configuration; safe for concurrent use.
func NewClient(cfg Config) (*Client, error) { return runtime.NewClient(cfg) }

// Configuration defaults.
const (
	DefaultBaseURL    = runtime.DefaultBaseURL
	DefaultAPIVersion = runtime.DefaultAPIVersion
)

// The three typed failure classes (runtime-tdd §3, failover-contract §2).
// Dispatch by type with errors.As — never by message text:
//
//	var tf *revaly.TransientFailure
//	if errors.As(err, &tf) { /* safe to fail over */ }
type (
	RapError           = runtime.RapError
	PermanentRejection = runtime.PermanentRejection
	TransientFailure   = runtime.TransientFailure
	OutcomeUnknown     = runtime.OutcomeUnknown
)

// Reconcile contract (runtime-tdd §4, failover-contract §3). The verdict set
// is OPEN for extension (ADR-SDK-009) — always dispatch with a default branch.
type (
	ReconcileVerdict   = runtime.ReconcileVerdict
	Found              = runtime.Found
	NotFoundYet        = runtime.NotFoundYet
	ReconcilePolicy    = runtime.ReconcilePolicy
	TransactionOutcome = runtime.TransactionOutcome
)

// Terminal transaction outcomes carried by Found.
const (
	TransactionOutcomeApproved = runtime.TransactionOutcomeApproved
	TransactionOutcomeDeclined = runtime.TransactionOutcomeDeclined
	TransactionOutcomeError    = runtime.TransactionOutcomeError
	TransactionOutcomePending  = runtime.TransactionOutcomePending
	TransactionOutcomeUnknown  = runtime.TransactionOutcomeUnknown
)

// Wire-trace observation surface (runtime-tdd §6): scrubbed request/response
// events for Enablement escalations.
type (
	WireTraceEvent = runtime.WireTraceEvent
	WireTraceHook  = runtime.WireTraceHook
)

// CorrelationIDHeader is the response header joining every request to RAP-core
// telemetry.
const CorrelationIDHeader = runtime.CorrelationIDHeader

// Payment-path models re-exported from the generated core so the quickstart
// path needs only this package. The long tail of models is available under
// the core package this aliases.
type (
	PaymentRequest             = core.PaymentRequest
	AuthorizeRequest           = core.AuthorizeRequest
	CaptureRequest             = core.CaptureRequest
	VoidRequest                = core.VoidRequest
	RefundRequest              = core.RefundRequest
	RefundCancelRequest        = core.RefundCancelRequest
	CreditCard                 = core.CreditCard
	PaymentMethod              = core.PaymentMethod
	TransactionResponse        = core.TransactionResponse
	TransactionGroupResponse   = core.TransactionGroupResponse
	PendingTransactionResponse = core.PendingTransactionResponse
	ErrorResponse              = core.ErrorResponse
)

// Pointer helpers for optional model fields, re-exported from the core.
var (
	PtrBool    = core.PtrBool
	PtrInt     = core.PtrInt
	PtrInt32   = core.PtrInt32
	PtrInt64   = core.PtrInt64
	PtrFloat32 = core.PtrFloat32
	PtrFloat64 = core.PtrFloat64
	PtrString  = core.PtrString
	PtrTime    = core.PtrTime
)
