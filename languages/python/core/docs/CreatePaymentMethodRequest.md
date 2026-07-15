# CreatePaymentMethodRequest

Request to create a new payment method

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_type** | **str** | Type of payment method to create: - **creditCard**: Use raw credit card details that will be tokenized - **gatewayPaymentMethodId**: Use an existing token from a supported payment gateway  | 
**customer_id** | **str** | Unique identifier for the customer | [optional] 
**payment_method** | [**PaymentMethod**](PaymentMethod.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.create_payment_method_request import CreatePaymentMethodRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePaymentMethodRequest from a JSON string
create_payment_method_request_instance = CreatePaymentMethodRequest.from_json(json)
# print the JSON string representation of the object
print(CreatePaymentMethodRequest.to_json())

# convert the object into a dict
create_payment_method_request_dict = create_payment_method_request_instance.to_dict()
# create an instance of CreatePaymentMethodRequest from a dict
create_payment_method_request_from_dict = CreatePaymentMethodRequest.from_dict(create_payment_method_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


