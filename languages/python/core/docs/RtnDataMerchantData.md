# RtnDataMerchantData

Merchant identification and account signals. acquirerMerchantId is hard-required by RTN downstream but optional in this API.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**acquirer_merchant_id** | **str** | Acquirer-assigned merchant identifier. Hard-required by RTN; optional in this API. | [optional] 
**issuer_merchant_id** | **str** | Issuer-side merchant identifier, if known. | [optional] 
**acquirer_bin** | **str** | BIN of the acquiring institution. | [optional] 
**acquirer_reference_number** | **str** | Acquirer reference number (ARN) for network clearing. | [optional] 
**merchant_name** | **str** | Merchant display name as it appears to the customer. | [optional] 
**merchant_account_age_indicator** | **str** | Merchant account age token. | [optional] 
**merchant_account_opened_date** | **str** | Date the merchant account was created. Format YYYYMMDD. | [optional] 
**is_tenured_merchant** | **bool** | True if the merchant has a long-standing, established account relationship. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_merchant_data import RtnDataMerchantData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataMerchantData from a JSON string
rtn_data_merchant_data_instance = RtnDataMerchantData.from_json(json)
# print the JSON string representation of the object
print(RtnDataMerchantData.to_json())

# convert the object into a dict
rtn_data_merchant_data_dict = rtn_data_merchant_data_instance.to_dict()
# create an instance of RtnDataMerchantData from a dict
rtn_data_merchant_data_from_dict = RtnDataMerchantData.from_dict(rtn_data_merchant_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


