# RtnDataCustomData

Producer-reserved custom fields for metadata not covered by the canonical schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_field1** | **str** | Free-form name-value pair string. Format is producer-defined. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_custom_data import RtnDataCustomData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataCustomData from a JSON string
rtn_data_custom_data_instance = RtnDataCustomData.from_json(json)
# print the JSON string representation of the object
print(RtnDataCustomData.to_json())

# convert the object into a dict
rtn_data_custom_data_dict = rtn_data_custom_data_instance.to_dict()
# create an instance of RtnDataCustomData from a dict
rtn_data_custom_data_from_dict = RtnDataCustomData.from_dict(rtn_data_custom_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


