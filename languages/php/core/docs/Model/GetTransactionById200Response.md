# GetTransactionById200Response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction** | [**\Revaly\Sdk\Core\Model\TransactionResponse**](TransactionResponse.md) | The transaction matching the supplied id (the record the non-expanded lookup returns). | [optional]
**transactions** | [**\Revaly\Sdk\Core\Model\TransactionResponse[]**](TransactionResponse.md) | Every transaction in the payment, ordered by transaction date ascending. Capped at 100. |
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
**payment_plan_data** | [**\Revaly\Sdk\Core\Model\PaymentPlanData**](PaymentPlanData.md) |  | [optional]
**recovery** | [**\Revaly\Sdk\Core\Model\Recovery**](Recovery.md) |  | [optional]
**response** | [**\Revaly\Sdk\Core\Model\TransactionResponseDetails**](TransactionResponseDetails.md) |  | [optional]
**payment_method** | [**\Revaly\Sdk\Core\Model\PaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
