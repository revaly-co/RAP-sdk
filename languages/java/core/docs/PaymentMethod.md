

# PaymentMethod

Payment method details. Which fields are required depends on the payment-method type of the request: creditCard requires a cardholder name (fullName, or firstName together with lastName) plus creditCard.number/expiryMonth/expiryYear; gatewayPaymentMethodId requires gatewayPaymentMethod.gatewayPaymentMethodId and merchantAccountReferenceId; vaultToken requires vaultPaymentMethod.vaultToken plus the request-level customerId. When billing a stored payment method, supply paymentMethodId alone.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**firstName** | **String** | Customer&#39;s first name |  [optional] |
|**lastName** | **String** | Customer&#39;s last name |  [optional] |
|**fullName** | **String** | Customer&#39;s full name |  [optional] |
|**email** | **String** | Customer&#39;s email address |  [optional] |
|**merchantAccountReferenceId** | **String** | Merchant account identifier at the gateway |  [optional] |
|**paymentMethodId** | **String** | Existing payment method identifier (for updates) |  [optional] |
|**issuerIdentificationNumber** | **String** | Bank Identification Number (BIN). Must contain exactly 6 or 8 digits. |  [optional] |
|**billingAddress** | [**Address**](Address.md) |  |  [optional] |
|**shippingAddress** | [**Address**](Address.md) |  |  [optional] |
|**creditCard** | [**CreditCard**](CreditCard.md) |  |  [optional] |
|**gatewayPaymentMethod** | [**GatewayPaymentMethod**](GatewayPaymentMethod.md) |  |  [optional] |
|**vaultPaymentMethod** | [**VaultPaymentMethod**](VaultPaymentMethod.md) |  |  [optional] |



