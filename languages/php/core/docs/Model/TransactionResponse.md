# TransactionResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **string** | Unique identifier for the transaction | [optional]
**transaction_date** | **\DateTime** | Date and time when the transaction was processed (ISO 8601) | [optional]
**transaction_status** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional]
**message** | **string** | Human-readable message about the transaction result | [optional]
**response_code** | **string** | Gateway-specific response code | [optional]
**transaction_type** | **string** | Type of transaction performed. Passthrough of the processing platform&#39;s transaction type — not a closed set. Payment operations return \&quot;Charge\&quot;, \&quot;Authorize\&quot;, \&quot;Capture\&quot;, \&quot;Void\&quot; or \&quot;Refund\&quot; (refund cancellation returns \&quot;Refund\&quot;). Transaction lookups can additionally return types created by other platform flows, e.g. \&quot;Verify\&quot;, \&quot;SuccessfulPayment\&quot;, \&quot;RefundedPayment\&quot;, \&quot;CreateCreditCard\&quot;, \&quot;UpdatePaymentMethod\&quot;, \&quot;RedactPaymentMethod\&quot;, \&quot;RecachePaymentMethod\&quot;, \&quot;CreateGatewayPaymentMethod\&quot;. Treat unrecognized values as informational. | [optional]
**merchant_transaction_id** | **string** | Merchant-provided transaction identifier | [optional]
**customer_id** | **string** | Customer identifier associated with the transaction | [optional]
**gateway_routing_id** | **string** | Gateway-specific token for the transaction | [optional]
**currency** | **string** | Transaction currency code (ISO 4217) | [optional]
**amount** | **int** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional]
**gateway_type** | **string** | Payment gateway used for processing | [optional]
**gateway_transaction_id** | **string** | Gateway-specific transaction identifier | [optional]
**acquirer_auth_code** | **string** | Authorization code returned by the acquiring bank or network | [optional]
**inline_retry_previous_transaction_id** | **string** | Transaction identifier of the inline retry attempt when one was executed | [optional]
**inline_retry_previous_merchant_transaction_id** | **string** | Original merchant transaction identifier before an inline retry was executed | [optional]
**is_inline_retry** | **bool** | Indicates that an inline retry attempt occurred | [optional]
**retry_date** | **\DateTime** | Date for retry attempt (if applicable) | [optional]
**mit_stored_transaction_id** | **string** | Merchant-initiated transaction stored credential ID | [optional]
**stored_credential** | [**\Revaly\Sdk\Core\Model\StoredCredentialResponse**](StoredCredentialResponse.md) |  | [optional]
**order_id** | **string** | Order identifier from the merchant system | [optional]
**statement_descriptor** | **string** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. | [optional]
**customer_ip** | **string** | Customer&#39;s IP address at time of transaction | [optional]
**engaged_recovery_state** | **int** | Recovery state indicator (0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional]
**description** | **string** | Transaction description or notes | [optional]
**gateway_fields** | **array<string,mixed>** | Additional gateway-specific fields | [optional]
**gateway_specific_response_fields** | **array<string,mixed>** | Additional gateway-specific response details returned directly from the processor | [optional]
**gateway_response_payload** | **string** | The processing gateway&#39;s own answer, as one JSON document in a string, reduced to the keys the platform lists for that gateway. Every other key is removed. Free-text values under the kept keys are checked for a value shaped like a card number: 13 to 19 digits that pass the Luhn check, with or without separators between the groups of digits. Such a number is never returned in full. Its first 6 and last 4 digits are kept and every digit between them is replaced with &#x60;*&#x60;; the rest of that value and the rest of the payload are returned as the gateway sent them, and the platform is alerted to it. A matching JSON number is returned as a masked string. A value that cannot be masked is left out, that key only. Gateway reference and token fields are returned as the gateway sent them and are not checked, because gateway references are often 16-digit numbers. Present only on the answer to a payment, capture, void or refund sent directly to the gateway, and only when the payload is switched on for the API key that made the request and the gateway returned one. In every other case the field is absent, never null and never an empty string. | [optional]
**payment_plan_data** | [**\Revaly\Sdk\Core\Model\PaymentPlanData**](PaymentPlanData.md) |  | [optional]
**recovery** | [**\Revaly\Sdk\Core\Model\Recovery**](Recovery.md) |  | [optional]
**response** | [**\Revaly\Sdk\Core\Model\TransactionResponseDetails**](TransactionResponseDetails.md) |  | [optional]
**payment_method** | [**\Revaly\Sdk\Core\Model\PaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
