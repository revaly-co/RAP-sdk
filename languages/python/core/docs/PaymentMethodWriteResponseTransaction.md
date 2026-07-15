# PaymentMethodWriteResponseTransaction

Associated transaction information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | Unique identifier for the transaction | [optional] 
**transaction_date** | **datetime** | Date and time when the transaction was processed | [optional] 
**transaction_status** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**message** | **str** | Human-readable message about the transaction | [optional] 
**response_code** | **str** | Gateway response code | [optional] 
**transaction_type** | **str** | Type of transaction | [optional] 

## Example

```python
from revaly_sdk_core.models.payment_method_write_response_transaction import PaymentMethodWriteResponseTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethodWriteResponseTransaction from a JSON string
payment_method_write_response_transaction_instance = PaymentMethodWriteResponseTransaction.from_json(json)
# print the JSON string representation of the object
print(PaymentMethodWriteResponseTransaction.to_json())

# convert the object into a dict
payment_method_write_response_transaction_dict = payment_method_write_response_transaction_instance.to_dict()
# create an instance of PaymentMethodWriteResponseTransaction from a dict
payment_method_write_response_transaction_from_dict = PaymentMethodWriteResponseTransaction.from_dict(payment_method_write_response_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


