

# VaultPaymentMethod

Vault-issued payment token details for payment processing

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**vaultToken** | **String** | Vault-issued token (any provider) used to authorize a payment. Valid only on &#x60;/payments/charge&#x60; and &#x60;/payments/authorize&#x60; when &#x60;paymentMethodType&#x60; is &#x60;vaultToken&#x60;. Requires &#x60;paymentMethod.merchantAccountReferenceId&#x60; for gateway routing. Must not be combined with &#x60;creditCard&#x60; or &#x60;gatewayPaymentMethod&#x60;.  |  [optional] |
|**bin** | **String** | Bank Identification Number (first 6 or 8 digits) |  [optional] |
|**lastFourDigits** | **String** | Last four digits of the payment method |  [optional] |
|**expiryYear** | **String** | Expiration year (YYYY) |  [optional] |
|**expiryMonth** | **String** | Expiration month (01-12) |  [optional] |



