

# PaymentRequest

Request to process a payment (charge) transaction

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**paymentMethodType** | [**PaymentMethodTypeEnum**](#PaymentMethodTypeEnum) | Type of payment method to use: - **creditCard**: Use raw credit card details - **gatewayPaymentMethodId**: Use an existing gateway payment method identifier - **vaultToken**: Use a vault-issued token (any provider). Requires &#x60;paymentMethod.vaultPaymentMethod.vaultToken&#x60; and &#x60;paymentMethod.merchantAccountReferenceId&#x60;.  To bill a stored payment method, omit this property and send &#x60;paymentMethod.paymentMethodId&#x60;.  |  [optional] |
|**amount** | **Long** | Payment amount in smallest currency unit (e.g., cents for USD) |  |
|**merchantTransactionId** | **String** | Merchant-provided unique identifier for this transaction |  |
|**gatewayRoutingId** | **String** | Gateway-specific token for payment processing |  [optional] |
|**currency** | **String** | Three-letter ISO currency code |  [optional] |
|**initiatedBy** | **InitiatedBy** |  |  [optional] |
|**mitStoredTransactionId** | **String** | Merchant-initiated transaction stored credential ID |  [optional] |
|**storedCredential** | [**StoredCredential**](StoredCredential.md) |  |  [optional] |
|**paymentMethod** | [**PaymentMethod**](PaymentMethod.md) |  |  [optional] |
|**orderId** | **String** | Order identifier from the merchant system |  [optional] |
|**storeOnSuccess** | **Boolean** | Whether to store the payment method on successful transaction |  [optional] |
|**bypassPlatform** | **Boolean** | When true, bypass the primary Revaly processor and execute only the fallback flow |  [optional] |
|**customerIp** | **String** | Customer&#39;s IP address |  [optional] |
|**customerId** | **String** | Customer identifier |  [optional] |
|**gatewayFields** | **Map&lt;String, Object&gt;** | Additional gateway-specific fields |  [optional] |
|**rtnData** | [**RtnData**](RtnData.md) |  |  [optional] |
|**description** | **String** | Transaction description |  [optional] |
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



