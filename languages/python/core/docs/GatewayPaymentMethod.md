# GatewayPaymentMethod

GatewayPaymentMethodId details for payment processing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**gateway_payment_method_id** | **str** | Token identifier from the payment gateway | [optional] 
**bin** | **str** | Bank Identification Number (first 6 or 8 digits) | [optional] 
**last_four_digits** | **str** | Last four digits of the payment method | [optional] 
**expiry_year** | **str** | Expiration year (YYYY) | [optional] 
**expiry_month** | **str** | Expiration month (01-12) | [optional] 

## Example

```python
from revaly_sdk_core.models.gateway_payment_method import GatewayPaymentMethod

# TODO update the JSON string below
json = "{}"
# create an instance of GatewayPaymentMethod from a JSON string
gateway_payment_method_instance = GatewayPaymentMethod.from_json(json)
# print the JSON string representation of the object
print(GatewayPaymentMethod.to_json())

# convert the object into a dict
gateway_payment_method_dict = gateway_payment_method_instance.to_dict()
# create an instance of GatewayPaymentMethod from a dict
gateway_payment_method_from_dict = GatewayPaymentMethod.from_dict(gateway_payment_method_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


