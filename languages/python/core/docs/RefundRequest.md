# RefundRequest

Request to refund a payment transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**merchant_transaction_id** | **str** | Merchant-provided unique identifier for this refund transaction | 
**amount** | **int** | Refund amount in smallest currency unit (e.g., cents for USD). If null or omitted, a full refund will be processed.  | [optional] 

## Example

```python
from revaly_sdk_core.models.refund_request import RefundRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RefundRequest from a JSON string
refund_request_instance = RefundRequest.from_json(json)
# print the JSON string representation of the object
print(RefundRequest.to_json())

# convert the object into a dict
refund_request_dict = refund_request_instance.to_dict()
# create an instance of RefundRequest from a dict
refund_request_from_dict = RefundRequest.from_dict(refund_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


