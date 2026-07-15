# Revaly.Sdk.Core.Model.VaultPaymentMethod
Vault-issued payment token details for payment processing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**VaultToken** | **string** | Vault-issued token (any provider) used to authorize a payment. Valid only on &#x60;/payments/charge&#x60; and &#x60;/payments/authorize&#x60; when &#x60;paymentMethodType&#x60; is &#x60;vaultToken&#x60;. Requires &#x60;paymentMethod.merchantAccountReferenceId&#x60; for gateway routing. Must not be combined with &#x60;creditCard&#x60; or &#x60;gatewayPaymentMethod&#x60;.  | [optional] 
**Bin** | **string** | Bank Identification Number (first 6 or 8 digits) | [optional] 
**LastFourDigits** | **string** | Last four digits of the payment method | [optional] 
**ExpiryYear** | **string** | Expiration year (YYYY) | [optional] 
**ExpiryMonth** | **string** | Expiration month (01-12) | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

