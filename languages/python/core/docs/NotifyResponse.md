# NotifyResponse

Response to a notification request indicating processing status

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Indicates whether the notification was processed successfully | [optional] 
**message** | **str** | Human-readable message about the notification processing result | [optional] 

## Example

```python
from revaly_sdk_core.models.notify_response import NotifyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of NotifyResponse from a JSON string
notify_response_instance = NotifyResponse.from_json(json)
# print the JSON string representation of the object
print(NotifyResponse.to_json())

# convert the object into a dict
notify_response_dict = notify_response_instance.to_dict()
# create an instance of NotifyResponse from a dict
notify_response_from_dict = NotifyResponse.from_dict(notify_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


