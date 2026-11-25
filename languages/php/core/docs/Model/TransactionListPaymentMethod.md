# TransactionListPaymentMethod

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_id** | **string** | Payment method identifier | [optional]
**credit_card_number** | **string** | Masked card number; the full number is never returned | [optional]
**expiry_month** | **string** | Card expiry month as stored | [optional]
**expiry_year** | **string** | Card expiry year as stored | [optional]
**first_name** | **string** |  | [optional]
**last_name** | **string** |  | [optional]
**full_name** | **string** |  | [optional]
**customer_id** | **string** | Customer identifier of the operation | [optional]
**address1** | **string** | Billing address, first line | [optional]
**address2** | **string** | Billing address, second line | [optional]
**city** | **string** | Billing address city | [optional]
**state** | **string** | Billing address state or region | [optional]
**postal_code** | **string** | Billing address postal code | [optional]
**country** | **string** | Billing address country | [optional]
**email** | **string** |  | [optional]
**phone_number** | **string** |  | [optional]
**shipping_address1** | **string** | Shipping address, first line | [optional]
**shipping_address2** | **string** | Shipping address, second line | [optional]
**shipping_city** | **string** |  | [optional]
**shipping_state** | **string** |  | [optional]
**shipping_postal_code** | **string** |  | [optional]
**shipping_country** | **string** |  | [optional]
**payment_method_type** | **string** | Type of the payment method | [optional]
**last_four_digits** | **string** | Last four digits of the card number | [optional]
**first_six_digits** | **string** | First six digits of the card number | [optional]
**card_type** | **string** | Card brand as reported for the card (for example VISA) | [optional]
**date_created** | **string** | Date and time the payment method was created, as reported when the operation ran (ISO 8601). It may carry no UTC offset. | [optional]
**storage_state** | **string** | Storage state of the payment method | [optional]
**issuer_identification_number** | **string** | BIN of the card as reported when the operation ran | [optional]
**merchant_account_reference_id** | **string** | Merchant account reference identifier | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
