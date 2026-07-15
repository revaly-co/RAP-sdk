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
**CustomerIp** | **string** | Customer&#39;s IP address at time of transaction | [optional] 
**EngagedRecoveryState** | **int** | Recovery state indicator (0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional] 
**Description** | **string** | Transaction description or notes | [optional] 
**GatewayFields** | **Dictionary&lt;string, Object&gt;** | Additional gateway-specific fields | [optional] 
**GatewaySpecificResponseFields** | **Dictionary&lt;string, Object&gt;** | Additional gateway-specific response details returned directly from the processor | [optional] 
**PaymentPlanData** | [**PaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**Recovery** | [**Recovery**](Recovery.md) |  | [optional] 
**Response** | [**TransactionResponseDetails**](TransactionResponseDetails.md) |  | [optional] 
**PaymentMethod** | [**PaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

