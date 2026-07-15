# CaptureRequest

Request to capture an authorized payment transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**merchant_transaction_id** | **str** | Merchant-provided unique identifier for this capture transaction | 
**amount** | **int** | Capture amount in smallest currency unit (e.g., cents for USD). If null or omitted, the full authorized amount will be captured.  | [optional] 

## Example

```python
from revaly_sdk_core.models.capture_request import CaptureRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CaptureRequest from a JSON string
capture_request_instance = CaptureRequest.from_json(json)
# print the JSON string representation of the object
print(CaptureRequest.to_json())

# convert the object into a dict
capture_request_dict = capture_request_instance.to_dict()
# create an instance of CaptureRequest from a dict
capture_request_from_dict = CaptureRequest.from_dict(capture_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


