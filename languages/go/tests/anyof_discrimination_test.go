// anyOf / oneOf wrapper discrimination — pins the forked model_anyof.mustache behavior
// (pipeline/go/templates/, recorded in pipeline/go/config.yaml) on the two
// transaction-lookup response wrappers (spec v2.4.0, SC-408 B4: the unions
// switched oneOf -> anyOf with branches ordered most-specific first).
//
// The stock anyOf leg lenient-decodes branches first-match-wins, which stays
// names-correct only until the server evolves: branch models with required
// members strict-reject unknown fields, so one additive platform field would
// re-bind a pending body as a terminal transaction and hard-fail a group
// envelope. The fork (anyOf variant of the model_oneof fork) discriminates by
// field names only — strict unknown-fields pass first (first match in
// declaration order wins), then a lenient recognized-field-coverage pass so
// additive platform fields (minor releases) keep binding. These tests pin all
// of that.
//
// The list-item cases pin the model_oneof fork on ListTransactions200ResponseInner
// (spec v2.19.0: listTransactions items became oneOf TransactionListItem |
// TransactionListPaymentMethodItem): a flat row and a payment-method row each
// bind their own branch, with and without an additive top-level field, and a
// whole list array decodes item by item. The payment-method row carries the
// lastFourDigits / firstSixDigits pattern constraints — the shape that matched
// zero schemas under the stock validator.v2 pass the fork replaced.
package tests

import (
	"encoding/json"
	"strings"
	"testing"
	"time"

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

// A group envelope always carries the required `transactions` member (v2.4.0
// made it required — it IS the documented discriminator); additive fields
// nested inside its transactions must not break the group bind. The lenient
// pass binds through a methodless alias precisely so nested unknowns pass.
func TestNestedAdditiveFieldStillBindsGroup(t *testing.T) {
	inner := withAdditive(trPayload, "settlementBatchId", `"sb-1"`)
	payload := `{"transaction":` + inner + `,"transactions":[` + inner + `]}`
	w := boundByMerchant(t, payload)
	if w.TransactionGroupResponse == nil {
		t.Fatal("expected TransactionGroupResponse branch despite nested additive field")
	}
	if n := len(w.TransactionGroupResponse.GetTransactions()); n != 1 {
		t.Fatalf("transactions len = %d, want 1", n)
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

// Pinned fork behavior: payloads that fit no branch by names stay errors.
func TestUnrecognizedPayloadsError(t *testing.T) {
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

const listFlatPayload = `{"transactionId":"t-1","transactionDate":"2025-09-13T03:19:54.86Z","transactionStatus":1,"responseCode":"10000","transactionType":"Charge","amount":2500,"currencyCode":"USD"}`

const listPaymentMethodPayload = `{"transaction":{"transactionId":"t-2","transactionDate":"2025-12-02T14:44:42.209Z","transactionStatus":1,"message":"Succeeded!","responseCode":"10000","transactionType":"CreateCreditCard","paymentMethod":{"paymentMethodId":"pm-1","lastFourDigits":"1111","firstSixDigits":"411111","cardType":"VISA","storageState":"Cached","issuerIdentificationNumber":"41111111"}}}`

func boundListItem(t *testing.T, payload string) *core.ListTransactions200ResponseInner {
	t.Helper()
	var w core.ListTransactions200ResponseInner
	if err := w.UnmarshalJSON([]byte(payload)); err != nil {
		t.Fatalf("UnmarshalJSON failed: %v (payload %s)", err, payload)
	}
	return &w
}

func TestListItemBindsTransactionListItem(t *testing.T) {
	w := boundListItem(t, listFlatPayload)
	if w.TransactionListItem == nil {
		t.Fatal("expected TransactionListItem branch")
	}
	if w.TransactionListPaymentMethodItem != nil {
		t.Fatal("TransactionListPaymentMethodItem branch must stay nil")
	}
	item := w.TransactionListItem
	if got := item.GetTransactionId(); got != "t-1" {
		t.Fatalf("transactionId = %q, want t-1", got)
	}
	if got, want := item.GetTransactionDate(), time.Date(2025, 9, 13, 3, 19, 54, 860000000, time.UTC); !got.Equal(want) {
		t.Fatalf("transactionDate = %v, want %v", got, want)
	}
	if got := item.GetTransactionStatus(); got != 1 {
		t.Fatalf("transactionStatus = %d, want 1", got)
	}
	if got := item.GetResponseCode(); got != "10000" {
		t.Fatalf("responseCode = %q, want 10000", got)
	}
	if got := item.GetTransactionType(); got != "Charge" {
		t.Fatalf("transactionType = %q, want Charge", got)
	}
	if got := item.GetAmount(); got != 2500 {
		t.Fatalf("amount = %d, want 2500", got)
	}
	if got := item.GetCurrencyCode(); got != "USD" {
		t.Fatalf("currencyCode = %q, want USD", got)
	}
}

// The payment-method row carries pattern-constrained card fields
// (lastFourDigits ^[0-9]{4}$, firstSixDigits ^[0-9]{6}$) — the validator.v2
// shape that once matched zero schemas — and must still bind by names.
func TestListItemBindsTransactionListPaymentMethodItem(t *testing.T) {
	w := boundListItem(t, listPaymentMethodPayload)
	if w.TransactionListPaymentMethodItem == nil {
		t.Fatal("expected TransactionListPaymentMethodItem branch")
	}
	if w.TransactionListItem != nil {
		t.Fatal("TransactionListItem branch must stay nil")
	}
	tx := w.TransactionListPaymentMethodItem.GetTransaction()
	if got := tx.GetTransactionId(); got != "t-2" {
		t.Fatalf("transaction.transactionId = %q, want t-2", got)
	}
	if got := tx.GetTransactionType(); got != "CreateCreditCard" {
		t.Fatalf("transaction.transactionType = %q, want CreateCreditCard", got)
	}
	pm := tx.GetPaymentMethod()
	if got := pm.GetLastFourDigits(); got != "1111" {
		t.Fatalf("transaction.paymentMethod.lastFourDigits = %q, want 1111", got)
	}
	if got := pm.GetFirstSixDigits(); got != "411111" {
		t.Fatalf("transaction.paymentMethod.firstSixDigits = %q, want 411111", got)
	}
	if got := pm.GetCardType(); got != "VISA" {
		t.Fatalf("transaction.paymentMethod.cardType = %q, want VISA", got)
	}
}

func TestListItemAdditiveFieldStillBindsTransactionListItem(t *testing.T) {
	w := boundListItem(t, withAdditive(listFlatPayload, "futureAdditiveField", `"x"`))
	if w.TransactionListItem == nil {
		t.Fatal("expected TransactionListItem branch despite additive field")
	}
	if w.TransactionListPaymentMethodItem != nil {
		t.Fatal("TransactionListPaymentMethodItem branch must stay nil")
	}
	if got := w.TransactionListItem.GetTransactionId(); got != "t-1" {
		t.Fatalf("transactionId = %q, want t-1", got)
	}
}

func TestListItemAdditiveFieldStillBindsTransactionListPaymentMethodItem(t *testing.T) {
	w := boundListItem(t, withAdditive(listPaymentMethodPayload, "futureAdditiveField", `"x"`))
	if w.TransactionListPaymentMethodItem == nil {
		t.Fatal("expected TransactionListPaymentMethodItem branch despite additive field")
	}
	if w.TransactionListItem != nil {
		t.Fatal("TransactionListItem branch must stay nil")
	}
	tx := w.TransactionListPaymentMethodItem.GetTransaction()
	pm := tx.GetPaymentMethod()
	if got := pm.GetLastFourDigits(); got != "1111" {
		t.Fatalf("transaction.paymentMethod.lastFourDigits = %q, want 1111", got)
	}
}

// A listTransactions 200 body is a JSON array of wrappers; each item binds its
// own branch independently.
func TestListTransactionsArrayBindsEachItem(t *testing.T) {
	var items []core.ListTransactions200ResponseInner
	if err := json.Unmarshal([]byte("["+listFlatPayload+","+listPaymentMethodPayload+"]"), &items); err != nil {
		t.Fatalf("json.Unmarshal failed: %v", err)
	}
	if n := len(items); n != 2 {
		t.Fatalf("items len = %d, want 2", n)
	}
	if items[0].TransactionListItem == nil || items[0].TransactionListPaymentMethodItem != nil {
		t.Fatalf("items[0] = %T, want *core.TransactionListItem", items[0].GetActualInstance())
	}
	if items[1].TransactionListPaymentMethodItem == nil || items[1].TransactionListItem != nil {
		t.Fatalf("items[1] = %T, want *core.TransactionListPaymentMethodItem", items[1].GetActualInstance())
	}
}
