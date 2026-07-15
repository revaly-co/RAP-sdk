

# TransactionResponse

Complete transaction information including processing details

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transactionId** | **String** | Unique identifier for the transaction |  [optional] |
|**transactionDate** | **OffsetDateTime** | Date and time when the transaction was processed (ISO 8601) |  [optional] |
|**transactionStatus** | **Integer** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) |  [optional] |
|**message** | **String** | Human-readable message about the transaction result |  [optional] |
|**responseCode** | **String** | Gateway-specific response code |  [optional] |
|**transactionType** | **String** | Type of transaction performed. Passthrough of the processing platform&#39;s transaction type — not a closed set. Payment operations return \&quot;Charge\&quot;, \&quot;Authorize\&quot;, \&quot;Capture\&quot;, \&quot;Void\&quot; or \&quot;Refund\&quot; (refund cancellation returns \&quot;Refund\&quot;). Transaction lookups can additionally return types created by other platform flows, e.g. \&quot;Verify\&quot;, \&quot;SuccessfulPayment\&quot;, \&quot;RefundedPayment\&quot;, \&quot;CreateCreditCard\&quot;, \&quot;UpdatePaymentMethod\&quot;, \&quot;RedactPaymentMethod\&quot;, \&quot;RecachePaymentMethod\&quot;, \&quot;CreateGatewayPaymentMethod\&quot;. Treat unrecognized values as informational. |  [optional] |
|**merchantTransactionId** | **String** | Merchant-provided transaction identifier |  [optional] |
|**customerId** | **String** | Customer identifier associated with the transaction |  [optional] |
|**gatewayRoutingId** | **String** | Gateway-specific token for the transaction |  [optional] |
|**currency** | **String** | Transaction currency code (ISO 4217) |  [optional] |
|**amount** | **Long** | Transaction amount in smallest currency unit (e.g., cents for USD) |  [optional] |
|**gatewayType** | **String** | Payment gateway used for processing |  [optional] |
|**gatewayTransactionId** | **String** | Gateway-specific transaction identifier |  [optional] |
|**acquirerAuthCode** | **String** | Authorization code returned by the acquiring bank or network |  [optional] |
|**inlineRetryPreviousTransactionId** | **String** | Transaction identifier of the inline retry attempt when one was executed |  [optional] |
|**inlineRetryPreviousMerchantTransactionId** | **String** | Original merchant transaction identifier before an inline retry was executed |  [optional] |
|**isInlineRetry** | **Boolean** | Indicates that an inline retry attempt occurred |  [optional] |
|**retryDate** | **OffsetDateTime** | Date for retry attempt (if applicable) |  [optional] |
|**mitStoredTransactionId** | **String** | Merchant-initiated transaction stored credential ID |  [optional] |
|**storedCredential** | [**StoredCredentialResponse**](StoredCredentialResponse.md) |  |  [optional] |
|**orderId** | **String** | Order identifier from the merchant system |  [optional] |
|**customerIp** | **String** | Customer&#39;s IP address at time of transaction |  [optional] |
|**engagedRecoveryState** | **Integer** | Recovery state indicator (0 &#x3D; not engaged, 1+ &#x3D; recovery level) |  [optional] |
|**description** | **String** | Transaction description or notes |  [optional] |
|**gatewayFields** | **Map&lt;String, Object&gt;** | Additional gateway-specific fields |  [optional] |
|**gatewaySpecificResponseFields** | **Map&lt;String, Object&gt;** | Additional gateway-specific response details returned directly from the processor |  [optional] |
|**paymentPlanData** | [**PaymentPlanData**](PaymentPlanData.md) |  |  [optional] |
|**recovery** | [**Recovery**](Recovery.md) |  |  [optional] |
|**response** | [**TransactionResponseDetails**](TransactionResponseDetails.md) |  |  [optional] |
|**paymentMethod** | [**PaymentMethodResponse**](PaymentMethodResponse.md) |  |  [optional] |



