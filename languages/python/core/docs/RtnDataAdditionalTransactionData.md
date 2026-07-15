# RtnDataAdditionalTransactionData

Core transaction signals supplied by the request producer. Transaction-routing fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) are derived by Revaly at submission time and must not be sent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider_auth_decision** | **str** | Authorization decision from the producer. Required for Trusted MID flows. | [optional] 
**provider_auth_decision_code** | **str** | Provider-specific reason code for the auth decision. Required for Trusted MID flows. | [optional] 
**payment_rail** | **str** | Payment routing rail. | [optional] 
**pos_entry_mode** | **str** | Credential capture method at the point of sale. | [optional] 
**retrieval_reference_number** | **str** | Transaction retrieval reference number. | [optional] 
**merchant_trust_level** | **str** | Merchant trust classification assigned by the producer. | [optional] 
**merchant_trust_data** | **str** | Producer metadata encoding the basis for the trust classification. | [optional] 
**card_brand** | **str** | Card product brand. | [optional] 
**message_category** | **str** | Message type: 1 &#x3D; Pre-Auth Approved, 2 &#x3D; Pre-Auth Declined, 3 &#x3D; Pre-Auth Test. | [optional] 
**full_pan** | **str** | Full card Primary Account Number (cardholder data / CHD). Optional. Forwarded to RTN in-flight only — never persisted or logged at rest by RAP. Sending this field transmits cardholder data; ensure your integration is authorized under your PCI-DSS obligations. | [optional] 
**dpan** | **str** | Device Primary Account Number (tokenized card number from a digital wallet). | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_additional_transaction_data import RtnDataAdditionalTransactionData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataAdditionalTransactionData from a JSON string
rtn_data_additional_transaction_data_instance = RtnDataAdditionalTransactionData.from_json(json)
# print the JSON string representation of the object
print(RtnDataAdditionalTransactionData.to_json())

# convert the object into a dict
rtn_data_additional_transaction_data_dict = rtn_data_additional_transaction_data_instance.to_dict()
# create an instance of RtnDataAdditionalTransactionData from a dict
rtn_data_additional_transaction_data_from_dict = RtnDataAdditionalTransactionData.from_dict(rtn_data_additional_transaction_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


