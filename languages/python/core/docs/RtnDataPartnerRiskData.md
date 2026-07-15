# RtnDataPartnerRiskData

Risk scores and trust signals from the producer. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_risk_score** | **str** | Transaction-level risk score assigned by the producer. String to accommodate decimal scores. | [optional] 
**is_trusted_mid_partner** | **bool** | True if the producer is operating in Trusted MID capacity for this transaction. | [optional] 
**customer_risk_score** | **str** | Customer-level risk score. | [optional] 
**device_risk_score** | **str** | Device-level risk score. | [optional] 
**ip_risk_score** | **str** | IP address risk score. | [optional] 
**merchant_risk_score** | **str** | Merchant-level risk score. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_partner_risk_data import RtnDataPartnerRiskData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataPartnerRiskData from a JSON string
rtn_data_partner_risk_data_instance = RtnDataPartnerRiskData.from_json(json)
# print the JSON string representation of the object
print(RtnDataPartnerRiskData.to_json())

# convert the object into a dict
rtn_data_partner_risk_data_dict = rtn_data_partner_risk_data_instance.to_dict()
# create an instance of RtnDataPartnerRiskData from a dict
rtn_data_partner_risk_data_from_dict = RtnDataPartnerRiskData.from_dict(rtn_data_partner_risk_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


