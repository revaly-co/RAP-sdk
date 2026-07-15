

# RtnDataPartnerRiskData

Risk scores and trust signals from the producer. All fields optional.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transactionRiskScore** | **String** | Transaction-level risk score assigned by the producer. String to accommodate decimal scores. |  [optional] |
|**isTrustedMidPartner** | **Boolean** | True if the producer is operating in Trusted MID capacity for this transaction. |  [optional] |
|**customerRiskScore** | **String** | Customer-level risk score. |  [optional] |
|**deviceRiskScore** | **String** | Device-level risk score. |  [optional] |
|**ipRiskScore** | **String** | IP address risk score. |  [optional] |
|**merchantRiskScore** | **String** | Merchant-level risk score. |  [optional] |



