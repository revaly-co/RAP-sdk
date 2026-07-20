

# AuthorizeRequest

Request to authorize a payment transaction

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**paymentMethodType** | [**PaymentMethodTypeEnum**](#PaymentMethodTypeEnum) | Type of payment method to use: - **creditCard**: Use raw credit card details. Requires &#x60;paymentMethod.creditCard&#x60;   (&#x60;number&#x60;, &#x60;expiryMonth&#x60;, &#x60;expiryYear&#x60;) and a cardholder name — &#x60;paymentMethod.fullName&#x60;,   or &#x60;paymentMethod.firstName&#x60; together with &#x60;paymentMethod.lastName&#x60;. - **gatewayPaymentMethodId**: Use an existing gateway payment method identifier. Requires   &#x60;paymentMethod.gatewayPaymentMethod.gatewayPaymentMethodId&#x60; and   &#x60;paymentMethod.merchantAccountReferenceId&#x60;. - **vaultToken**: Use a vault-issued token (any provider). Requires   &#x60;paymentMethod.vaultPaymentMethod.vaultToken&#x60; and the request-level &#x60;customerId&#x60; — the   token is scoped to the customer it was minted for and cannot be detokenized without it.   Vault tokens are gateway-agnostic and can be processed on any gateway.  **Omitting this property.** When exactly one of &#x60;paymentMethod.creditCard&#x60;, &#x60;paymentMethod.gatewayPaymentMethod&#x60;, or &#x60;paymentMethod.vaultPaymentMethod&#x60; is supplied, the type is inferred from it. Supplying more than one of those objects without an explicit type is rejected with &#x60;400&#x60;. To bill a stored payment method, omit this property (and the objects above) and send &#x60;paymentMethod.paymentMethodId&#x60;; recommendation flows (&#x60;previousTransaction&#x60; / &#x60;gateway&#x60;) also carry no type.  |  [optional] |
|**amount** | **Long** | Authorization amount in smallest currency unit (e.g., cents for USD) |  |
|**merchantTransactionId** | **String** | Merchant-provided unique identifier for this authorization. The platform accepts up to 100 characters, but downstream gateways may enforce shorter limits on merchant references (limits near 50 characters have been observed); keep ids at or below 48 characters for the broadest gateway compatibility. |  |
|**gatewayRoutingId** | **String** | Gateway-specific token for payment processing |  [optional] |
|**currency** | **String** | Three-letter ISO currency code |  [optional] |
|**initiatedBy** | **InitiatedBy** |  |  [optional] |
|**mitStoredTransactionId** | **String** | Merchant-initiated transaction stored credential ID |  [optional] |
|**storedCredential** | [**StoredCredential**](StoredCredential.md) |  |  [optional] |
|**paymentMethod** | [**PaymentMethod**](PaymentMethod.md) |  |  [optional] |
|**orderId** | **String** | Order identifier from the merchant system |  [optional] |
|**storeOnSuccess** | **Boolean** | Whether to store the payment method on successful authorization |  [optional] |
|**bypassPlatform** | **Boolean** | When true, bypass the primary Revaly processor and execute only the fallback flow |  [optional] |
|**customerIp** | **String** | Customer&#39;s IP address |  [optional] |
|**customerId** | **String** | Customer identifier |  [optional] |
|**gatewayFields** | **Map&lt;String, Object&gt;** | Additional gateway-specific fields |  [optional] |
|**rtnData** | [**RtnData**](RtnData.md) |  |  [optional] |
|**description** | **String** | Authorization description |  [optional] |
|**statementDescriptor** | **String** | Merchant-supplied text intended to appear on the customer&#39;s bank/card statement. Accepted as free text; per-gateway length and character adaptation is applied at submission and never blocks the charge. |  [optional] |
|**threeDS** | [**ThreeDS**](ThreeDS.md) |  |  [optional] |
|**paymentPlanData** | [**PaymentPlanData**](PaymentPlanData.md) |  |  [optional] |
|**recovery** | [**Recovery**](Recovery.md) |  |  [optional] |
|**previousTransaction** | [**PreviousTransaction**](PreviousTransaction.md) |  |  [optional] |
|**gateway** | [**Gateway**](Gateway.md) |  |  [optional] |



## Enum: PaymentMethodTypeEnum

| Name | Value |
|---- | -----|
| CREDIT_CARD | &quot;creditCard&quot; |
| GATEWAY_PAYMENT_METHOD_ID | &quot;gatewayPaymentMethodId&quot; |
| VAULT_TOKEN | &quot;vaultToken&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



