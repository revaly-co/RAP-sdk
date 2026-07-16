# Revaly.Sdk.Core.Model.PaymentRequest
Request to process a payment (charge) transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Amount** | **long** | Payment amount in smallest currency unit (e.g., cents for USD) | 
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this transaction | 
**PaymentMethodType** | **string** | Type of payment method to use: - **creditCard**: Use raw credit card details - **gatewayPaymentMethodId**: Use an existing gateway payment method identifier - **vaultToken**: Use a vault-issued token (any provider). Requires &#x60;paymentMethod.vaultPaymentMethod.vaultToken&#x60; and &#x60;paymentMethod.merchantAccountReferenceId&#x60;.  To bill a stored payment method, omit this property and send &#x60;paymentMethod.paymentMethodId&#x60;.  | [optional] 
**GatewayRoutingId** | **string** | Gateway-specific token for payment processing | [optional] 
**Currency** | **string** | Three-letter ISO currency code | [optional] 
**InitiatedBy** | **InitiatedBy** |  | [optional] 
**MitStoredTransactionId** | **string** | Merchant-initiated transaction stored credential ID | [optional] 
**StoredCredential** | [**StoredCredential**](StoredCredential.md) |  | [optional] 
**PaymentMethod** | [**PaymentMethod**](PaymentMethod.md) |  | [optional] 
**OrderId** | **string** | Order identifier from the merchant system | [optional] 
**StoreOnSuccess** | **bool** | Whether to store the payment method on successful transaction | [optional] 
**BypassPlatform** | **bool** | When true, bypass the primary Revaly processor and execute only the fallback flow | [optional] [default to false]
**CustomerIp** | **string** | Customer&#39;s IP address | [optional] 
**CustomerId** | **string** | Customer identifier | [optional] 
**GatewayFields** | **Dictionary&lt;string, Object&gt;** | Additional gateway-specific fields | [optional] 
**RtnData** | [**RtnData**](RtnData.md) |  | [optional] 
**Description** | **string** | Transaction description | [optional] 
**StatementDescriptor** | **string** | Merchant-supplied text intended to appear on the customer&#39;s bank/card statement. Accepted as free text; per-gateway length and character adaptation is applied at submission and never blocks the charge. | [optional] 
**ThreeDS** | [**ThreeDS**](ThreeDS.md) |  | [optional] 
**PaymentPlanData** | [**PaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**Recovery** | [**Recovery**](Recovery.md) |  | [optional] 
**PreviousTransaction** | [**PreviousTransaction**](PreviousTransaction.md) |  | [optional] 
**Gateway** | [**Gateway**](Gateway.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

