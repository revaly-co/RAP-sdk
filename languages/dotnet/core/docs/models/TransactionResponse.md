# Revaly.Sdk.Core.Model.TransactionResponse
Complete transaction information including processing details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | **string** | Unique identifier for the transaction | [optional] 
**TransactionDate** | **DateTime** | Date and time when the transaction was processed (ISO 8601) | [optional] 
**TransactionStatus** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**Message** | **string** | Human-readable message about the transaction result | [optional] 
**ResponseCode** | **string** | Gateway-specific response code | [optional] 
**TransactionType** | **string** | Type of transaction performed. Passthrough of the processing platform&#39;s transaction type — not a closed set. Payment operations return \&quot;Charge\&quot;, \&quot;Authorize\&quot;, \&quot;Capture\&quot;, \&quot;Void\&quot; or \&quot;Refund\&quot; (refund cancellation returns \&quot;Refund\&quot;). Transaction lookups can additionally return types created by other platform flows, e.g. \&quot;Verify\&quot;, \&quot;SuccessfulPayment\&quot;, \&quot;RefundedPayment\&quot;, \&quot;CreateCreditCard\&quot;, \&quot;UpdatePaymentMethod\&quot;, \&quot;RedactPaymentMethod\&quot;, \&quot;RecachePaymentMethod\&quot;, \&quot;CreateGatewayPaymentMethod\&quot;. Treat unrecognized values as informational. | [optional] 
**MerchantTransactionId** | **string** | Merchant-provided transaction identifier | [optional] 
**CustomerId** | **string** | Customer identifier associated with the transaction | [optional] 
**GatewayRoutingId** | **string** | Gateway-specific token for the transaction | [optional] 
**Currency** | **string** | Transaction currency code (ISO 4217) | [optional] 
**Amount** | **long** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**GatewayType** | **string** | Payment gateway used for processing | [optional] 
**GatewayTransactionId** | **string** | Gateway-specific transaction identifier | [optional] 
**AcquirerAuthCode** | **string** | Authorization code returned by the acquiring bank or network | [optional] 
**InlineRetryPreviousTransactionId** | **string** | Transaction identifier of the inline retry attempt when one was executed | [optional] 
**InlineRetryPreviousMerchantTransactionId** | **string** | Original merchant transaction identifier before an inline retry was executed | [optional] 
**IsInlineRetry** | **bool** | Indicates that an inline retry attempt occurred | [optional] 
**RetryDate** | **DateTime** | Date for retry attempt (if applicable) | [optional] 
**MitStoredTransactionId** | **string** | Merchant-initiated transaction stored credential ID | [optional] 
**StoredCredential** | [**StoredCredentialResponse**](StoredCredentialResponse.md) |  | [optional] 
**OrderId** | **string** | Order identifier from the merchant system | [optional] 
**StatementDescriptor** | **string** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. | [optional] 
**CustomerIp** | **string** | Customer&#39;s IP address at time of transaction | [optional] 
**EngagedRecoveryState** | **int** | Recovery state indicator (0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional] 
**Description** | **string** | Transaction description or notes | [optional] 
**GatewayFields** | **Dictionary&lt;string, Object&gt;** | Additional gateway-specific fields | [optional] 
**GatewaySpecificResponseFields** | **Dictionary&lt;string, Object&gt;** | Additional gateway-specific response details returned directly from the processor | [optional] 
**GatewayResponsePayload** | **string** | The processing gateway&#39;s own answer, as one JSON document in a string, reduced to the keys the platform lists for that gateway. Every other key is removed. Free-text values under the kept keys are checked for a value shaped like a card number: 13 to 19 digits that pass the Luhn check, with or without separators between the groups of digits. Such a number is never returned in full. Its first 6 and last 4 digits are kept and every digit between them is replaced with &#x60;*&#x60;; the rest of that value and the rest of the payload are returned as the gateway sent them, and the platform is alerted to it. A matching JSON number is returned as a masked string. A value that cannot be masked is left out, that key only. Gateway reference and token fields are returned as the gateway sent them and are not checked, because gateway references are often 16-digit numbers. Present only on the answer to a payment, capture, void or refund, and on the lookup by merchant transaction ID (&#x60;GET /transactions/merchant/{merchantTransactionId}&#x60;, for the attempt it returns), and only when the payload is switched on for the API key that made the request and the gateway&#39;s answer was returned or could be read again. In every other case the field is absent, never null and never an empty string. | [optional] 
**PaymentPlanData** | [**PaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**Recovery** | [**Recovery**](Recovery.md) |  | [optional] 
**Response** | [**TransactionResponseDetails**](TransactionResponseDetails.md) |  | [optional] 
**PaymentMethod** | [**PaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

