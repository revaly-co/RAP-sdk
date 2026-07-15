# PaymentMethodRecacheRequestPaymentMethod

Payment method data for recaching

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**credit_card** | [**PaymentMethodRecacheRequestPaymentMethodCreditCard**](PaymentMethodRecacheRequestPaymentMethodCreditCard.md) |  | 

## Example

```python
from revaly_sdk_core.models.payment_method_recache_request_payment_method import PaymentMethodRecacheRequestPaymentMethod

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethodRecacheRequestPaymentMethod from a JSON string
payment_method_recache_request_payment_method_instance = PaymentMethodRecacheRequestPaymentMethod.from_json(json)
# print the JSON string representation of the object
print(PaymentMethodRecacheRequestPaymentMethod.to_json())

# convert the object into a dict
payment_method_recache_request_payment_method_dict = payment_method_recache_request_payment_method_instance.to_dict()
# create an instance of PaymentMethodRecacheRequestPaymentMethod from a dict
payment_method_recache_request_payment_method_from_dict = PaymentMethodRecacheRequestPaymentMethod.from_dict(payment_method_recache_request_payment_method_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


