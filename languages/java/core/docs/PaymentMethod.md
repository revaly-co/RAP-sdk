

# PaymentMethod

Payment method details for either credit card or gatewayPaymentMethodId

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



