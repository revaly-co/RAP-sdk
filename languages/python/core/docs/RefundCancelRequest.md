# RefundCancelRequest

Request to refund or cancel a payment transaction using merchant transaction ID

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**merchant_transaction_id** | **str** | Merchant-provided unique identifier for this refund/cancel transaction | 
**amount** | **int** | Refund amount in smallest currency unit (e.g., cents for USD). If null or omitted, a full refund will be processed.  | [optional] 
**customer_id** | **str** | Unique identifier of the customer associated with this transaction | 

## Example

```python
from revaly_sdk_core.models.refund_cancel_request import RefundCancelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RefundCancelRequest from a JSON string
refund_cancel_request_instance = RefundCancelRequest.from_json(json)
# print the JSON string representation of the object
print(RefundCancelRequest.to_json())

# convert the object into a dict
refund_cancel_request_dict = refund_cancel_request_instance.to_dict()
# create an instance of RefundCancelRequest from a dict
refund_cancel_request_from_dict = RefundCancelRequest.from_dict(refund_cancel_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


