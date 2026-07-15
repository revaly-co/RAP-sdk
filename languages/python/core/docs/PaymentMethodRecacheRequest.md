# PaymentMethodRecacheRequest

Request to recache a payment method

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method** | [**PaymentMethodRecacheRequestPaymentMethod**](PaymentMethodRecacheRequestPaymentMethod.md) |  | 

## Example

```python
from revaly_sdk_core.models.payment_method_recache_request import PaymentMethodRecacheRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethodRecacheRequest from a JSON string
payment_method_recache_request_instance = PaymentMethodRecacheRequest.from_json(json)
# print the JSON string representation of the object
print(PaymentMethodRecacheRequest.to_json())

# convert the object into a dict
payment_method_recache_request_dict = payment_method_recache_request_instance.to_dict()
# create an instance of PaymentMethodRecacheRequest from a dict
payment_method_recache_request_from_dict = PaymentMethodRecacheRequest.from_dict(payment_method_recache_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


