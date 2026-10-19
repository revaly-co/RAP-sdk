// Typed failure classes and the normative outcome classifier.
//
// The three classes of docs/failover-contract.md §2 as Go sentinel-wrapped
// typed errors (runtime-tdd §3): dispatch with errors.As, e.g.
//
//	var tf *TransientFailure
//	if errors.As(err, &tf) { ... }
//
// The class — never the message text, never latency — is what licenses (or
// forbids) failover. The Kind tokens match the other language runtimes so
// cross-language log lines join cleanly.
//
// The merchant API key can never appear in a message: no constructor in this
// file ever receives it (ADR-SDK-020).
package runtime

import (
	"crypto/tls"
	"encoding/json"
	"errors"
	"fmt"
	"net"
)

// RapError is the base of the three typed failure classes (runtime-tdd §3),
// embedded by each of them. Every instance carries the class discriminant
// (Kind), the HTTP status (if any), the verbatim open Code (if any — an open
// string; OQ-2 adds values later), the server's human APIError message, opaque
// Details, the X-Correlation-ID of the response, and the raw response body.
type RapError struct {
	// Kind is the class discriminant: "PermanentRejection", "TransientFailure"
	// or "OutcomeUnknown". Dispatch on the concrete type via errors.As; Kind
	// exists for logging and cross-language log joins.
	Kind string
	// Status is the HTTP status, 0 when the failure produced no response.
	Status int
	// Code is the ErrorResponse.code verbatim — an OPEN string ("" when
	// absent). Unrecognized values classify as absent (failover-contract §2).
	Code string
	// APIError is the server's human `error` message — carried, never
	// consulted for classification.
	APIError string
	// Details is the ErrorResponse.details payload, treated as opaque except
	// for the single key edgeRejection read on a 403 (ADR-SDK-033, surfaced as
	// IsEdgeRejection / EdgeReference).
	Details any
	// CorrelationID joins this failure to RAP-core telemetry ("" when the
	// request never produced a response).
	CorrelationID string
	// RawBody is the raw response body ("" when there was none).
	RawBody string
	// IsEdgeRejection is true when the production edge firewall blocked this
	// request before it reached the platform: an HTTP 403 whose body carries
	// details.edgeRejection: true (ADR-SDK-033). Such a failure is a
	// *TransientFailure — the payment was definitively not processed. Charge
	// and authorize: fail over, or fix the request content and retry; capture,
	// void, refund and refund-cancel: retry the same request.
	IsEdgeRejection bool
	// EdgeReference is the edge firewall's tracking reference
	// (details.reference, equal to the x-azure-ref response header) when
	// IsEdgeRejection is true; "" otherwise. Quote it to support — it
	// identifies the exact firewall decision.
	EdgeReference string

	message string
	cause   error
}

func (e *RapError) Error() string { return e.message }

// Unwrap exposes the underlying transport error (nil for HTTP-classified
// failures), so errors.As/Is reach the original chain.
func (e *RapError) Unwrap() error { return e.cause }

// PermanentRejection: received and rejected (HTTP 400/401/404/422, or a 403
// without the edge-rejection marker). Fix or decline. **Never fail over** — the
// same request fails anywhere.
type PermanentRejection struct{ RapError }

// TransientFailure: definitively not processed (client-provable never-sent,
// 503 with code "not_processed", or a 403 blocked at the edge firewall —
// IsEdgeRejection, ADR-SDK-033). Safe to route to your own gateway
// immediately.
type TransientFailure struct{ RapError }

// OutcomeUnknown: may have been processed (deadline after send, reset
// mid-flight, 5xx without the not_processed proof). **Reconcile before
// acting** — failing over blind can double-charge (failover-contract §3).
type OutcomeUnknown struct{ RapError }

var permanentRejectionStatuses = map[int]bool{400: true, 401: true, 403: true, 404: true, 422: true}

// ClassifyResponse classifies a received HTTP response per the
// failover-contract §2 algorithm. Returns nil for 2xx. Code is read verbatim
// as an open string; Details stays opaque except for the single key
// details.edgeRejection read on a 403 (ADR-SDK-033); the error message is
// carried but NEVER consulted for classification. Statuses outside the
// normative table (3xx, 409, 429, …) are ambiguous → OutcomeUnknown.
//
// Version-pin behaviour (runtime-tdd §1): on "2.0" the code field is not part
// of the documented contract, so a 503 with not_processed still classifies
// OutcomeUnknown — the fast-failover class narrows to client-provable
// never-sent failures plus the edge-rejection 403 (ADR-SDK-033, honoured on
// both pins).
//
// The body is parsed leniently HERE, never through the core's ErrorResponse
// model: the generated model rejects unknown fields, so an additive platform
// field would otherwise break classification (probed).
func ClassifyResponse(status int, rawBody string, correlationID string, apiVersion string) error {
	if status >= 200 && status <= 299 {
		return nil
	}

	code, apiError, details := readErrorBody(rawBody)
	correlationNote := ""
	if correlationID != "" {
		correlationNote = " correlation=" + correlationID
	}
	base := RapError{
		Status:        status,
		Code:          code,
		APIError:      apiError,
		Details:       details,
		CorrelationID: correlationID,
		RawBody:       rawBody,
	}

	if status == 403 {
		if isEdge, reference := readEdgeMarker(details); isEdge {
			// Edge rejection (ADR-SDK-033): the edge firewall blocked the
			// request and its marker proves it never reached the platform —
			// provable non-dispatch, the same class as connection-refused and
			// 503 + not_processed. Honoured on every API version pin, because
			// the edge sits in front of the API.
			base.Kind = "TransientFailure"
			base.IsEdgeRejection = true
			base.EdgeReference = reference
			base.message = fmt.Sprintf("TransientFailure: HTTP 403 edge rejection%s — blocked at the edge firewall; never reached the platform; safe to fail over", correlationNote)
			return &TransientFailure{base}
		}
	}

	if permanentRejectionStatuses[status] {
		base.Kind = "PermanentRejection"
		base.message = fmt.Sprintf("PermanentRejection: HTTP %d%s — fix or decline; never fail over", status, correlationNote)
		return &PermanentRejection{base}
	}

	if status == 503 && code == "not_processed" && apiVersion != "2.0" {
		base.Kind = "TransientFailure"
		base.message = fmt.Sprintf("TransientFailure: HTTP 503 code=not_processed%s — provably not dispatched; safe to fail over", correlationNote)
		return &TransientFailure{base}
	}

	base.Kind = "OutcomeUnknown"
	base.message = fmt.Sprintf("OutcomeUnknown: HTTP %d%s — may have been processed; reconcile before acting", status, correlationNote)
	return &OutcomeUnknown{base}
}

// ClassifyTransportError classifies a wire-level failure by error TYPE ONLY —
// never message text (failover-contract §2 rules). It always returns one of
// the typed classes, wrapping the original error (Unwrap reaches the chain).
//
// Never-sent proof on net/http (all probed):
//   - *net.OpError with Op == "dial" covers connection refused, unreachable,
//     DNS failure (*net.DNSError nests inside the dial OpError) and the
//     dialer's connect-phase timeout — all provably before any HTTP bytes →
//     TransientFailure. The dial-phase proof for connect timeouts exists only
//     when ConnectTimeout maps to net.Dialer.Timeout: a context deadline that
//     expires during the dial surfaces as context.DeadlineExceeded WITHOUT the
//     OpError, which is not phase-provable → OutcomeUnknown.
//   - *tls.CertificateVerificationError is emitted strictly during the
//     handshake, before the request is written → TransientFailure.
//
// TLS conservatism (matches the php/python precedent): any other TLS failure
// (record-header errors, alerts, handshake TIMEOUT — an unexported net/http
// type) is not provably pre-send by TYPE → OutcomeUnknown.
func ClassifyTransportError(err error) error {
	if isTyped(err) {
		// Already one of the typed classes — pass it through unchanged.
		return err
	}

	var opErr *net.OpError
	if errors.As(err, &opErr) && opErr.Op == "dial" {
		return &TransientFailure{RapError{
			Kind:    "TransientFailure",
			message: "TransientFailure: dial-phase failure (refused, unreachable, DNS, or connect timeout) — the request was provably never sent",
			cause:   err,
		}}
	}

	var certErr *tls.CertificateVerificationError
	if errors.As(err, &certErr) {
		return &TransientFailure{RapError{
			Kind:    "TransientFailure",
			message: "TransientFailure: TLS certificate verification failed during the handshake — the request was provably never sent",
			cause:   err,
		}}
	}

	// Deadlines after send, resets mid-flight, generic TLS failures, and
	// anything else: the stack has not proven the request was never sent —
	// never guess toward "safe".
	return &OutcomeUnknown{RapError{
		Kind:    "OutcomeUnknown",
		message: "OutcomeUnknown: transport failure without never-sent proof — reconcile before acting",
		cause:   err,
	}}
}

// isTyped reports whether the chain already carries one of the three classes.
// (Embedding RapError does not make the concrete types match a *RapError
// errors.As target, so each class is checked explicitly.)
func isTyped(err error) bool {
	var pr *PermanentRejection
	var tf *TransientFailure
	var ou *OutcomeUnknown
	return errors.As(err, &pr) || errors.As(err, &tf) || errors.As(err, &ou)
}

// readEdgeMarker reads the one structured key of details the contract allows
// (ADR-SDK-033): details.edgeRejection must be the JSON boolean true — never
// the string "true", a number, or anything else. details.reference (the
// edge's tracking reference, equal to the x-azure-ref header) is carried when
// it is a string. The body is parsed regardless of Content-Type: the
// production edge serves this JSON as text/html.
func readEdgeMarker(details any) (isEdgeRejection bool, reference string) {
	object, ok := details.(map[string]any)
	if !ok {
		return false, ""
	}
	marker, ok := object["edgeRejection"].(bool)
	if !ok || !marker {
		return false, ""
	}
	reference, _ = object["reference"].(string)
	return true, reference
}

// readErrorBody leniently reads ErrorResponse fields from the raw body.
// Classification must survive any body shape: non-JSON or non-object bodies
// yield all-absent fields (unrecognized/absent code falls to the
// OutcomeUnknown path per §2).
func readErrorBody(rawBody string) (code string, apiError string, details any) {
	if rawBody == "" {
		return "", "", nil
	}
	var root map[string]json.RawMessage
	if err := json.Unmarshal([]byte(rawBody), &root); err != nil || root == nil {
		return "", "", nil
	}
	if raw, ok := root["code"]; ok {
		var s string
		if json.Unmarshal(raw, &s) == nil {
			code = s
		}
	}
	if raw, ok := root["error"]; ok {
		var s string
		if json.Unmarshal(raw, &s) == nil {
			apiError = s
		}
	}
	if raw, ok := root["details"]; ok {
		var d any
		if json.Unmarshal(raw, &d) == nil {
			details = d
		}
	}
	return code, apiError, details
}
