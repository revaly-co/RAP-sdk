# PaymentMethodRecacheRequestPaymentMethodCreditCard

Credit card data for verification

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**verification_value** | **str** | CVV/CVC code for verification | 

## Example

```python
from revaly_sdk_core.models.payment_method_recache_request_payment_method_credit_card import PaymentMethodRecacheRequestPaymentMethodCreditCard

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethodRecacheRequestPaymentMethodCreditCard from a JSON string
payment_method_recache_request_payment_method_credit_card_instance = PaymentMethodRecacheRequestPaymentMethodCreditCard.from_json(json)
# print the JSON string representation of the object
print(PaymentMethodRecacheRequestPaymentMethodCreditCard.to_json())

# convert the object into a dict
payment_method_recache_request_payment_method_credit_card_dict = payment_method_recache_request_payment_method_credit_card_instance.to_dict()
# create an instance of PaymentMethodRecacheRequestPaymentMethodCreditCard from a dict
payment_method_recache_request_payment_method_credit_card_from_dict = PaymentMethodRecacheRequestPaymentMethodCreditCard.from_dict(payment_method_recache_request_payment_method_credit_card_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


