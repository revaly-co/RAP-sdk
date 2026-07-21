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
// github.com/revaly-co/rap-sdk/languages/go/raptest.
//
// The safety contract this SDK implements — the three failure classes, the
// classification algorithm, and the reconcile procedure — is
// docs/failover-contract.md; the quickstart in this directory's README walks
// the full failover + reconcile path.
package revaly

import (
	"time"

	core "github.com/revaly-co/rap-sdk/languages/go/core"
	"github.com/revaly-co/rap-sdk/languages/go/internal/runtime"
)

// Version is the SDK package version reported in the User-Agent product token.
// Release identity comes from per-language `go/vX.Y.Z` tags cut in pipeline
// stage 5; the tree carries the embargo placeholder until the registry-publish
// gates close (repo rule 3).
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
	DefaultBaseURL         = runtime.DefaultBaseURL
	DefaultAPIVersion      = runtime.DefaultAPIVersion
	DefaultOverallDeadline = runtime.DefaultOverallDeadline
	NoOverallDeadline      = runtime.NoOverallDeadline
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

// Constructors for the payment-path models, forwarded from the generated core
// so the quickstart path compiles against this package alone (runtime-tdd §2).
// These are thin functions rather than var bindings (ADR-SDK-028): the
// bindings are immutable and each carries a proper godoc signature.

// NewPaymentRequest builds a PaymentRequest (POST /payments) with the required
// fields. merchantTransactionID is YOUR reconcile key (failover-contract §3).
func NewPaymentRequest(amount int64, merchantTransactionID string) *PaymentRequest {
	return core.NewPaymentRequest(amount, merchantTransactionID)
}

// NewAuthorizeRequest builds an AuthorizeRequest with the required fields.
func NewAuthorizeRequest(amount int64, merchantTransactionID string) *AuthorizeRequest {
	return core.NewAuthorizeRequest(amount, merchantTransactionID)
}

// NewCaptureRequest builds a CaptureRequest with the required fields.
func NewCaptureRequest(merchantTransactionID string) *CaptureRequest {
	return core.NewCaptureRequest(merchantTransactionID)
}

// NewVoidRequest builds a VoidRequest with the required fields.
func NewVoidRequest(merchantTransactionID string) *VoidRequest {
	return core.NewVoidRequest(merchantTransactionID)
}

// NewRefundRequest builds a RefundRequest with the required fields.
func NewRefundRequest(merchantTransactionID string) *RefundRequest {
	return core.NewRefundRequest(merchantTransactionID)
}

// NewRefundCancelRequest builds a RefundCancelRequest with the required fields.
func NewRefundCancelRequest(merchantTransactionID string, customerID string) *RefundCancelRequest {
	return core.NewRefundCancelRequest(merchantTransactionID, customerID)
}

// NewCreditCard builds a CreditCard with the required fields.
func NewCreditCard(number string, expiryMonth string, expiryYear string) *CreditCard {
	return core.NewCreditCard(number, expiryMonth, expiryYear)
}

// NewPaymentMethod builds an empty PaymentMethod; populate exactly one
// concrete method object (e.g. SetCreditCard).
func NewPaymentMethod() *PaymentMethod {
	return core.NewPaymentMethod()
}

// Pointer helpers for optional model fields, forwarded from the core.

// PtrBool returns a pointer to the given bool value.
func PtrBool(v bool) *bool { return core.PtrBool(v) }

// PtrInt returns a pointer to the given int value.
func PtrInt(v int) *int { return core.PtrInt(v) }

// PtrInt32 returns a pointer to the given int32 value.
func PtrInt32(v int32) *int32 { return core.PtrInt32(v) }

// PtrInt64 returns a pointer to the given int64 value.
func PtrInt64(v int64) *int64 { return core.PtrInt64(v) }

// PtrFloat32 returns a pointer to the given float32 value.
func PtrFloat32(v float32) *float32 { return core.PtrFloat32(v) }

// PtrFloat64 returns a pointer to the given float64 value.
func PtrFloat64(v float64) *float64 { return core.PtrFloat64(v) }

// PtrString returns a pointer to the given string value.
func PtrString(v string) *string { return core.PtrString(v) }

// PtrTime returns a pointer to the given time.Time value.
func PtrTime(v time.Time) *time.Time { return core.PtrTime(v) }
