# Revaly.Sdk.Core.Model.PaymentMethod
Payment method details. Which fields are required depends on the payment-method type of the request: creditCard requires a cardholder name (fullName, or firstName together with lastName) plus creditCard.number/expiryMonth/expiryYear; gatewayPaymentMethodId requires gatewayPaymentMethod.gatewayPaymentMethodId and merchantAccountReferenceId; vaultToken requires vaultPaymentMethod.vaultToken plus the request-level customerId. When billing a stored payment method, supply paymentMethodId alone.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**FirstName** | **string** | Customer&#39;s first name | [optional] 
**LastName** | **string** | Customer&#39;s last name | [optional] 
**FullName** | **string** | Customer&#39;s full name | [optional] 
**Email** | **string** | Customer&#39;s email address | [optional] 
**MerchantAccountReferenceId** | **string** | Merchant account identifier at the gateway | [optional] 
**PaymentMethodId** | **string** | Existing payment method identifier (for updates) | [optional] 
**IssuerIdentificationNumber** | **string** | Bank Identification Number (BIN). Must contain exactly 6 or 8 digits. | [optional] 
**BillingAddress** | [**Address**](Address.md) |  | [optional] 
**ShippingAddress** | [**Address**](Address.md) |  | [optional] 
**CreditCard** | [**CreditCard**](CreditCard.md) |  | [optional] 
**GatewayPaymentMethod** | [**GatewayPaymentMethod**](GatewayPaymentMethod.md) |  | [optional] 
**VaultPaymentMethod** | [**VaultPaymentMethod**](VaultPaymentMethod.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

