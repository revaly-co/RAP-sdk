# VoidRequest

Request to void (cancel) a payment transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**merchant_transaction_id** | **str** | Merchant-provided unique identifier for this void transaction | 

## Example

```python
from revaly_sdk_core.models.void_request import VoidRequest

# TODO update the JSON string below
json = "{}"
# create an instance of VoidRequest from a JSON string
void_request_instance = VoidRequest.from_json(json)
# print the JSON string representation of the object
print(VoidRequest.to_json())

# convert the object into a dict
void_request_dict = void_request_instance.to_dict()
# create an instance of VoidRequest from a dict
void_request_from_dict = VoidRequest.from_dict(void_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


