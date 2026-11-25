# TransactionListPaymentMethodItem

A payment-method operation (create, update, redact or recache) in the list transactions endpoint with the detailed response type. Its fields are wrapped in `transaction`, and its payment method is the flat `TransactionListPaymentMethod`. In simplified mode the same operations are returned as a flat `TransactionListItem`. A field with no value is omitted. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction** | [**TransactionListPaymentMethodItemTransaction**](TransactionListPaymentMethodItemTransaction.md) |  | 

## Example

```python
from revaly_sdk_core.models.transaction_list_payment_method_item import TransactionListPaymentMethodItem

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionListPaymentMethodItem from a JSON string
transaction_list_payment_method_item_instance = TransactionListPaymentMethodItem.from_json(json)
# print the JSON string representation of the object
print(TransactionListPaymentMethodItem.to_json())

# convert the object into a dict
transaction_list_payment_method_item_dict = transaction_list_payment_method_item_instance.to_dict()
# create an instance of TransactionListPaymentMethodItem from a dict
transaction_list_payment_method_item_from_dict = TransactionListPaymentMethodItem.from_dict(transaction_list_payment_method_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


