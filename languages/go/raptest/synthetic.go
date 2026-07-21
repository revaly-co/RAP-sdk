package raptest

import "fmt"

// Synthetic bodies only (ADR-SDK-020): obviously fake identifiers, no PAN, no
// CVV, no customer data — never recorded live payloads.

// SyntheticTransaction renders a terminal transaction record with the given
// transactionStatus (1=Approved, 2=Declined, 3=Error).
func SyntheticTransaction(transactionStatus int) string {
	return fmt.Sprintf(`{"transactionId":"mock-tx-0001","merchantTransactionId":"mock-mtx-0001",`+
		`"transactionType":"Charge","transactionStatus":%d,"amount":1099,"currency":"USD",`+
		`"gatewayType":"MockGateway","responseCode":"00"}`, transactionStatus)
}

// SyntheticPending renders a post-P-2 pending intent record.
func SyntheticPending() string {
	return `{"state":"pending","merchantTransactionId":"mock-mtx-0001","transactionType":"Charge",` +
		`"receivedAt":"2026-01-01T00:00:00Z"}`
}

// SyntheticError renders an ErrorResponse body; pass code "" to omit the code
// field (a bare error).
func SyntheticError(message string, code string) string {
	if code == "" {
		return fmt.Sprintf(`{"error":%q}`, message)
	}
	return fmt.Sprintf(`{"error":%q,"code":%q}`, message, code)
}
