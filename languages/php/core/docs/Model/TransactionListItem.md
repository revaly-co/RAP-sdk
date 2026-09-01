# TransactionListItem

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **string** | Unique transaction identifier | [optional]
**transaction_date** | **\DateTime** | Date and time when the transaction was processed (ISO 8601) | [optional]
**transaction_status** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional]
**response_code** | **string** | Response code from the processing result | [optional]
**message** | **string** | Human-readable message about the transaction result | [optional]
**transaction_type** | **string** | Type of transaction performed | [optional]
**retry_date** | **\DateTime** | Scheduled retry date, if applicable | [optional]
**amount** | **int** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional]
**initial_merchant_transaction_id** | **string** | The merchant transaction ID of the initial transaction in the recovery chain | [optional]
**storage_state** | **string** | Payment method storage state at the time of transaction | [optional]
**completion_status** | **string** | Recovery completion status of the transaction (e.g., RecoverySuccessful, RecoveryDeclined) | [optional]
**gateway_specific_response_fields** | **array<string,mixed>** | Gateway-specific response fields returned directly by the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle). | [optional]
**gateway_specific_fields** | **array<string,mixed>** | Gateway-specific request fields sent to the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle). | [optional]
**acquirer_auth_code** | **string** | Authorization code returned by the acquiring bank | [optional]
**gateway_transaction_id** | **string** | Gateway-specific transaction identifier | [optional]
**gateway_payment_method_id** | **string** | Gateway-specific payment method identifier | [optional]
**engaged_recovery_state** | **int** | Recovery state indicator (null/0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional]
**currency_code** | **string** | Transaction currency code (ISO 4217) | [optional]
**merchant_transaction_id** | **string** | Merchant-provided transaction identifier | [optional]
**merchant_account_reference_id** | **string** | Merchant account reference identifier | [optional]
**customer_id** | **string** | Customer identifier associated with the transaction | [optional]
**order_id** | **string** | Order identifier from the merchant system | [optional]
**statement_descriptor** | **string** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. | [optional]
**payment_method_id** | **string** | Payment method identifier used for the transaction | [optional]
**payment_method_storage_state** | **string** | Storage state of the payment method | [optional]
**payment_method_type** | **string** | Type of payment method used | [optional]
**payment_method_merchant_account_reference_id** | **string** | Merchant account reference ID associated with the payment method | [optional]
**vault_token** | **string** | Vault token for the credential this transaction ran against, reported flat on the row alongside the other &#x60;paymentMethod*&#x60; fields. Present only on rows that ran against a vault credential — omitted, not null or empty, on every other row. In practice this means the detailed response type: simplified rows carry no payment-method data to report a token from. | [optional]
**error_code** | **string** | Error code from the gateway response | [optional]
**error_detail** | **string** | Detailed error message from the gateway response | [optional]
**avs_code** | **string** | Address Verification System result code from the gateway | [optional]
**gateway** | [**\Revaly\Sdk\Core\Model\TransactionGateway**](TransactionGateway.md) |  | [optional]
**payment_method** | [**\Revaly\Sdk\Core\Model\PaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
