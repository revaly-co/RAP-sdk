// oneOf wrapper discrimination — pins the forked model_oneof.mustache behavior
// (pipeline/go/templates/, recorded in pipeline/go/config.yaml).
//
// The stock template's per-branch validator.v2 pass eliminated valid branches
// unconditionally on this spec (regexp validators on Nullable* struct fields are
// "unsupported type"; {m,n} regexp quantifiers split on the tag comma), so every
// terminal-transaction payload failed to match any schema on both response
// wrappers. The fork discriminates by field names only — strict unknown-fields
// pass first, then a lenient recognized-field-coverage pass so additive platform
// fields (minor releases) keep binding. These tests pin all of that.
package tests

import (
	"strings"
	"testing"

	core "github.com/revaly-co/rap-sdk/languages/go/core"
)

const trPayload = `{"transactionId":"t-1","transactionType":"Charge","merchantTransactionId":"mtx-1","transactionStatus":1,"amount":1099,"currency":"USD","gatewayType":"TestGw"}`

const ptrPayload = `{"state":"pending","merchantTransactionId":"mtx-1","transactionType":"Charge","receivedAt":"2026-07-18T12:00:00Z"}`

func tgrPayload() string {
	return `{"transaction":` + trPayload + `,"transactions":[` + trPayload + `]}`
}

func withAdditive(payload, key, value string) string {
	return strings.TrimSuffix(payload, "}") + `,"` + key + `":` + value + `}`
}

func boundByMerchant(t *testing.T, payload string) *core.GetTransactionByMerchantTransactionId200Response {
	t.Helper()
	var w core.GetTransactionByMerchantTransactionId200Response
	if err := w.UnmarshalJSON([]byte(payload)); err != nil {
		t.Fatalf("UnmarshalJSON failed: %v (payload %s)", err, payload)
	}
	return &w
}

func TestByMerchantBindsTransactionResponse(t *testing.T) {
	w := boundByMerchant(t, trPayload)
	if w.TransactionResponse == nil {
		t.Fatal("expected TransactionResponse branch")
	}
	if got := w.TransactionResponse.GetTransactionType(); got != "Charge" {
		t.Fatalf("transactionType = %q, want Charge", got)
	}
	if w.PendingTransactionResponse != nil || w.TransactionGroupResponse != nil {
		t.Fatal("other branches must stay nil")
	}
}

func TestByMerchantBindsPendingTransactionResponse(t *testing.T) {
	w := boundByMerchant(t, ptrPayload)
	if w.PendingTransactionResponse == nil {
		t.Fatal("expected PendingTransactionResponse branch")
	}
	if got := w.PendingTransactionResponse.GetState(); got != "pending" {
		t.Fatalf("state = %q, want pending", got)
	}
}

func TestByMerchantBindsTransactionGroupResponse(t *testing.T) {
	w := boundByMerchant(t, tgrPayload())
	if w.TransactionGroupResponse == nil {
		t.Fatal("expected TransactionGroupResponse branch")
	}
	if n := len(w.TransactionGroupResponse.GetTransactions()); n != 1 {
		t.Fatalf("transactions len = %d, want 1", n)
	}
}

// Additive platform fields (minor releases) must not break binding — the strict
// pass rejects them, the lenient coverage pass recovers the right branch.
func TestAdditiveFieldStillBindsTransactionResponse(t *testing.T) {
	w := boundByMerchant(t, withAdditive(trPayload, "settlementBatchId", `"sb-1"`))
	if w.TransactionResponse == nil {
		t.Fatal("expected TransactionResponse branch despite additive field")
	}
	if got := w.TransactionResponse.GetMerchantTransactionId(); got != "mtx-1" {
		t.Fatalf("merchantTransactionId = %q, want mtx-1", got)
	}
}

func TestAdditiveFieldStillBindsPending(t *testing.T) {
	w := boundByMerchant(t, withAdditive(ptrPayload, "reservationExpiresAt", `"2026-08-01T00:00:00Z"`))
	if w.PendingTransactionResponse == nil {
		t.Fatal("expected PendingTransactionResponse branch despite additive field")
	}
}

func TestNestedAdditiveFieldStillBindsGroup(t *testing.T) {
	payload := `{"transaction":` + withAdditive(trPayload, "settlementBatchId", `"sb-1"`) + `}`
	w := boundByMerchant(t, payload)
	if w.TransactionGroupResponse == nil {
		t.Fatal("expected TransactionGroupResponse branch despite nested additive field")
	}
}

// Discrimination is by field names only — a recognizable shape with a value the
// spec's patterns would reject still binds (validation is not the wrapper's job,
// and failover-contract §2 forbids value heuristics).
func TestValuesNeverDiscriminate(t *testing.T) {
	w := boundByMerchant(t, `{"transactionId":"t-1","currency":"usd!"}`)
	if w.TransactionResponse == nil {
		t.Fatal("expected TransactionResponse branch for name-recognizable payload")
	}
}

// Pinned stock behavior: payloads that fit no branch by names stay errors.
func TestAmbiguousAndUnrecognizedPayloadsError(t *testing.T) {
	for name, payload := range map[string]string{
		"empty object":      `{}`,
		"unrecognized keys": `{"whatever":1}`,
		"non-object scalar": `"x"`,
		"null":              `null`,
	} {
		var w core.GetTransactionByMerchantTransactionId200Response
		if err := w.UnmarshalJSON([]byte(payload)); err == nil {
			t.Fatalf("%s: expected error, got bind %+v", name, w)
		}
	}
}

func TestByIdWrapperBindsBothShapes(t *testing.T) {
	var byID core.GetTransactionById200Response
	if err := byID.UnmarshalJSON([]byte(trPayload)); err != nil || byID.TransactionResponse == nil {
		t.Fatalf("TR payload: err=%v", err)
	}
	var byID2 core.GetTransactionById200Response
	if err := byID2.UnmarshalJSON([]byte(tgrPayload())); err != nil || byID2.TransactionGroupResponse == nil {
		t.Fatalf("TGR payload: err=%v", err)
	}
	var byID3 core.GetTransactionById200Response
	if err := byID3.UnmarshalJSON([]byte(withAdditive(trPayload, "settlementBatchId", `"sb-1"`))); err != nil || byID3.TransactionResponse == nil {
		t.Fatalf("TR+additive payload: err=%v", err)
	}
}

func TestGetActualInstanceAndMarshalRoundTrip(t *testing.T) {
	w := boundByMerchant(t, trPayload)
	if _, ok := w.GetActualInstance().(*core.TransactionResponse); !ok {
		t.Fatalf("GetActualInstance = %T, want *core.TransactionResponse", w.GetActualInstance())
	}
	out, err := w.MarshalJSON()
	if err != nil {
		t.Fatalf("MarshalJSON: %v", err)
	}
	var re core.GetTransactionByMerchantTransactionId200Response
	if err := re.UnmarshalJSON(out); err != nil || re.TransactionResponse == nil {
		t.Fatalf("round-trip: err=%v", err)
	}
}
