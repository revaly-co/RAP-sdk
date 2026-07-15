# RtnDataBillingData

Cardholder billing address. All fields optional; omit rather than send nulls.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address_line1** | **str** | First line of the billing address. | [optional] 
**address_line2** | **str** | Second line of the billing address. | [optional] 
**address_line3** | **str** | Third line of the billing address. | [optional] 
**city** | **str** | City of the billing address. | [optional] 
**region** | **str** | State or province name. | [optional] 
**postal_code** | **str** | Postal or ZIP code of the billing address. | [optional] 
**country** | **str** | ISO 3166-1 alpha-2 country code. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_billing_data import RtnDataBillingData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataBillingData from a JSON string
rtn_data_billing_data_instance = RtnDataBillingData.from_json(json)
# print the JSON string representation of the object
print(RtnDataBillingData.to_json())

# convert the object into a dict
rtn_data_billing_data_dict = rtn_data_billing_data_instance.to_dict()
# create an instance of RtnDataBillingData from a dict
rtn_data_billing_data_from_dict = RtnDataBillingData.from_dict(rtn_data_billing_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


