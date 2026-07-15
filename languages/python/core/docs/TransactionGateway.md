# TransactionGateway

Gateway information associated with a transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** | Gateway routing token identifier | [optional] 
**gateway_type** | **str** | The type of payment gateway used | [optional] 
**name** | **str** | Human-readable gateway name | [optional] 
**reference_id** | **str** | Merchant account reference identifier at the gateway | [optional] 

## Example

```python
from revaly_sdk_core.models.transaction_gateway import TransactionGateway

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionGateway from a JSON string
transaction_gateway_instance = TransactionGateway.from_json(json)
# print the JSON string representation of the object
print(TransactionGateway.to_json())

# convert the object into a dict
transaction_gateway_dict = transaction_gateway_instance.to_dict()
# create an instance of TransactionGateway from a dict
transaction_gateway_from_dict = TransactionGateway.from_dict(transaction_gateway_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


