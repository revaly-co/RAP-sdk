# NotifyContactInformation

Contact information for customer notifications

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**first_name** | **str** | Customer&#39;s first name | [optional] 
**last_name** | **str** | Customer&#39;s last name | [optional] 
**phone_number** | **str** | Customer&#39;s phone number | [optional] 
**email** | **str** | Customer&#39;s email address | [optional] 

## Example

```python
from revaly_sdk_core.models.notify_contact_information import NotifyContactInformation

# TODO update the JSON string below
json = "{}"
# create an instance of NotifyContactInformation from a JSON string
notify_contact_information_instance = NotifyContactInformation.from_json(json)
# print the JSON string representation of the object
print(NotifyContactInformation.to_json())

# convert the object into a dict
notify_contact_information_dict = notify_contact_information_instance.to_dict()
# create an instance of NotifyContactInformation from a dict
notify_contact_information_from_dict = NotifyContactInformation.from_dict(notify_contact_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


