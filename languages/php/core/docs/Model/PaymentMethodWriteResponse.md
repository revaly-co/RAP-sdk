# PaymentMethodWriteResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction** | [**\Revaly\Sdk\Core\Model\PaymentMethodWriteResponseTransaction**](PaymentMethodWriteResponseTransaction.md) |  | [optional]
**payment_method_id** | **string** | Unique identifier for the payment method | [optional]
**credit_card_number** | **string** | Masked credit card number | [optional]
**expiry_month** | **string** | Expiration month | [optional]
**expiry_year** | **string** | Expiration year | [optional]
**cvv** | **string** | Masked CVV | [optional]
**first_name** | **string** | Customer&#39;s first name | [optional]
**last_name** | **string** | Customer&#39;s last name | [optional]
**full_name** | **string** | Customer&#39;s full name | [optional]
**customer_id** | **string** | Customer identifier | [optional]
**billing_address** | [**\Revaly\Sdk\Core\Model\Address**](Address.md) |  | [optional]
**shipping_address** | [**\Revaly\Sdk\Core\Model\Address**](Address.md) |  | [optional]
**email** | **string** | Customer&#39;s email address | [optional]
**phone_number** | **string** | Customer&#39;s phone number | [optional]
**payment_method_type** | **string** | Type of payment method | [optional]
**fingerprint** | **string** | Unique fingerprint for the payment method | [optional]
**last_four_digits** | **string** | Last four digits of the payment method | [optional]
**first_six_digits** | **string** | First six digits (BIN) of the payment method | [optional]
**card_type** | **string** | Type of credit card | [optional]
**date_created** | **\DateTime** | Date when the payment method was created | [optional]
**storage_state** | **string** | Storage state of the payment method | [optional]
**bin** | **string** | Bank Identification Number. Must contain exactly 6 or 8 digits. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
