# Revaly.Sdk.Core.Model.RtnDataPartnerRiskData
Risk scores and trust signals from the producer. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionRiskScore** | **string** | Transaction-level risk score assigned by the producer. String to accommodate decimal scores. | [optional] 
**IsTrustedMidPartner** | **bool** | True if the producer is operating in Trusted MID capacity for this transaction. | [optional] 
**CustomerRiskScore** | **string** | Customer-level risk score. | [optional] 
**DeviceRiskScore** | **string** | Device-level risk score. | [optional] 
**IpRiskScore** | **string** | IP address risk score. | [optional] 
**MerchantRiskScore** | **string** | Merchant-level risk score. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

