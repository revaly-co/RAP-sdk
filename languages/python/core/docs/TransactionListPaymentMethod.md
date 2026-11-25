# TransactionListPaymentMethod

The payment method of a payment-method operation in the list transactions endpoint, as stored when the operation ran. It is flat: the billing address fields sit beside the shipping address fields, and the BIN is `issuerIdentificationNumber`. This is not the nested shape the payment-method endpoints return. A field with no value is omitted. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_id** | **str** | Payment method identifier | [optional] 
**credit_card_number** | **str** | Masked card number; the full number is never returned | [optional] 
**expiry_month** | **str** | Card expiry month as stored | [optional] 
**expiry_year** | **str** | Card expiry year as stored | [optional] 
**first_name** | **str** |  | [optional] 
**last_name** | **str** |  | [optional] 
**full_name** | **str** |  | [optional] 
**customer_id** | **str** | Customer identifier of the operation | [optional] 
**address1** | **str** | Billing address, first line | [optional] 
**address2** | **str** | Billing address, second line | [optional] 
**city** | **str** | Billing address city | [optional] 
**state** | **str** | Billing address state or region | [optional] 
**postal_code** | **str** | Billing address postal code | [optional] 
**country** | **str** | Billing address country | [optional] 
**email** | **str** |  | [optional] 
**phone_number** | **str** |  | [optional] 
**shipping_address1** | **str** | Shipping address, first line | [optional] 
**shipping_address2** | **str** | Shipping address, second line | [optional] 
**shipping_city** | **str** |  | [optional] 
**shipping_state** | **str** |  | [optional] 
**shipping_postal_code** | **str** |  | [optional] 
**shipping_country** | **str** |  | [optional] 
**payment_method_type** | **str** | Type of the payment method | [optional] 
**last_four_digits** | **str** | Last four digits of the card number | [optional] 
**first_six_digits** | **str** | First six digits of the card number | [optional] 
**card_type** | **str** | Card brand as reported for the card (for example VISA) | [optional] 
**date_created** | **str** | Date and time the payment method was created, as reported when the operation ran (ISO 8601). It may carry no UTC offset. | [optional] 
**storage_state** | **str** | Storage state of the payment method | [optional] 
**issuer_identification_number** | **str** | BIN of the card as reported when the operation ran | [optional] 
**merchant_account_reference_id** | **str** | Merchant account reference identifier | [optional] 

## Example

```python
from revaly_sdk_core.models.transaction_list_payment_method import TransactionListPaymentMethod

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionListPaymentMethod from a JSON string
transaction_list_payment_method_instance = TransactionListPaymentMethod.from_json(json)
# print the JSON string representation of the object
print(TransactionListPaymentMethod.to_json())

# convert the object into a dict
transaction_list_payment_method_dict = transaction_list_payment_method_instance.to_dict()
# create an instance of TransactionListPaymentMethod from a dict
transaction_list_payment_method_from_dict = TransactionListPaymentMethod.from_dict(transaction_list_payment_method_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


