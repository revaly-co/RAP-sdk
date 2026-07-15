# Address

Address information for billing or shipping

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address1** | **str** | Primary address line | [optional] 
**address2** | **str** | Secondary address line (apartment, suite, etc.) | [optional] 
**city** | **str** | City name | [optional] 
**state** | **str** | State or province code | [optional] 
**zip** | **str** | Postal or ZIP code | [optional] 
**country** | **str** | Country code (ISO 3166-1 alpha-2) | [optional] 
**phone_number** | **str** | Phone number associated with the address | [optional] 

## Example

```python
from revaly_sdk_core.models.address import Address

# TODO update the JSON string below
json = "{}"
# create an instance of Address from a JSON string
address_instance = Address.from_json(json)
# print the JSON string representation of the object
print(Address.to_json())

# convert the object into a dict
address_dict = address_instance.to_dict()
# create an instance of Address from a dict
address_from_dict = Address.from_dict(address_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


