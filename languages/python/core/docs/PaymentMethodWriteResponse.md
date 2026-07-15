# PaymentMethodWriteResponse

Response after creating or modifying a payment method

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction** | [**PaymentMethodWriteResponseTransaction**](PaymentMethodWriteResponseTransaction.md) |  | [optional] 
**payment_method_id** | **str** | Unique identifier for the payment method | [optional] 
**credit_card_number** | **str** | Masked credit card number | [optional] 
**expiry_month** | **str** | Expiration month | [optional] 
**expiry_year** | **str** | Expiration year | [optional] 
**cvv** | **str** | Masked CVV | [optional] 
**first_name** | **str** | Customer&#39;s first name | [optional] 
**last_name** | **str** | Customer&#39;s last name | [optional] 
**full_name** | **str** | Customer&#39;s full name | [optional] 
**customer_id** | **str** | Customer identifier | [optional] 
**billing_address** | [**Address**](Address.md) |  | [optional] 
**shipping_address** | [**Address**](Address.md) |  | [optional] 
**email** | **str** | Customer&#39;s email address | [optional] 
**phone_number** | **str** | Customer&#39;s phone number | [optional] 
**payment_method_type** | **str** | Type of payment method | [optional] 
**fingerprint** | **str** | Unique fingerprint for the payment method | [optional] 
**last_four_digits** | **str** | Last four digits of the payment method | [optional] 
**first_six_digits** | **str** | First six digits (BIN) of the payment method | [optional] 
**card_type** | **str** | Type of credit card | [optional] 
**date_created** | **datetime** | Date when the payment method was created | [optional] 
**storage_state** | **str** | Storage state of the payment method | [optional] 
**bin** | **str** | Bank Identification Number. Must contain exactly 6 or 8 digits. | [optional] 

## Example

```python
from revaly_sdk_core.models.payment_method_write_response import PaymentMethodWriteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethodWriteResponse from a JSON string
payment_method_write_response_instance = PaymentMethodWriteResponse.from_json(json)
# print the JSON string representation of the object
print(PaymentMethodWriteResponse.to_json())

# convert the object into a dict
payment_method_write_response_dict = payment_method_write_response_instance.to_dict()
# create an instance of PaymentMethodWriteResponse from a dict
payment_method_write_response_from_dict = PaymentMethodWriteResponse.from_dict(payment_method_write_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


