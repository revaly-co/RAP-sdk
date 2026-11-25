# TransactionListPaymentMethodItemTransaction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | Unique transaction identifier | 
**transaction_date** | **datetime** | Date and time when the operation was processed (ISO 8601, UTC) | 
**transaction_status** | **int** | Status of the operation (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | 
**message** | **str** | Human-readable message about the result | [optional] 
**customer_id** | **str** | Customer identifier associated with the operation | [optional] 
**response_code** | **str** | Response code from the processing result | [optional] 
**transaction_type** | **str** | The payment-method operation: CreateCreditCard, CreateGatewayPaymentMethod, UpdatePaymentMethod, RedactPaymentMethod or RecachePaymentMethod | [optional] 
**payment_method** | [**TransactionListPaymentMethod**](TransactionListPaymentMethod.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.transaction_list_payment_method_item_transaction import TransactionListPaymentMethodItemTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionListPaymentMethodItemTransaction from a JSON string
transaction_list_payment_method_item_transaction_instance = TransactionListPaymentMethodItemTransaction.from_json(json)
# print the JSON string representation of the object
print(TransactionListPaymentMethodItemTransaction.to_json())

# convert the object into a dict
transaction_list_payment_method_item_transaction_dict = transaction_list_payment_method_item_transaction_instance.to_dict()
# create an instance of TransactionListPaymentMethodItemTransaction from a dict
transaction_list_payment_method_item_transaction_from_dict = TransactionListPaymentMethodItemTransaction.from_dict(transaction_list_payment_method_item_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


