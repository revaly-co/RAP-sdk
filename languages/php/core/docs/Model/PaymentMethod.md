# PaymentMethod

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**first_name** | **string** | Customer&#39;s first name | [optional]
**last_name** | **string** | Customer&#39;s last name | [optional]
**full_name** | **string** | Customer&#39;s full name | [optional]
**email** | **string** | Customer&#39;s email address | [optional]
**merchant_account_reference_id** | **string** | Merchant account identifier at the gateway | [optional]
**payment_method_id** | **string** | Existing payment method identifier (for updates) | [optional]
**issuer_identification_number** | **string** | Bank Identification Number (BIN). Must contain exactly 6 or 8 digits. | [optional]
**billing_address** | [**\Revaly\Sdk\Core\Model\Address**](Address.md) |  | [optional]
**shipping_address** | [**\Revaly\Sdk\Core\Model\Address**](Address.md) |  | [optional]
**credit_card** | [**\Revaly\Sdk\Core\Model\CreditCard**](CreditCard.md) |  | [optional]
**gateway_payment_method** | [**\Revaly\Sdk\Core\Model\GatewayPaymentMethod**](GatewayPaymentMethod.md) |  | [optional]
**vault_payment_method** | [**\Revaly\Sdk\Core\Model\VaultPaymentMethod**](VaultPaymentMethod.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
