

# Recovery

Recovery settings and customer recovery information

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**disableCustomerRecovery** | **Boolean** | Whether customer recovery is disabled for this transaction |  [optional] |
|**externalApproval** | **Boolean** | Describes whether the approval should be attributed to the merchant for billing purposes |  [optional] |
|**customerAccountNumber** | **String** | Customer account number for recovery purposes |  [optional] |
|**customerBalance** | **Integer** | Customer account balance in smallest currency unit (e.g., cents for USD) |  [optional] |
|**disableSMSNotification** | **Boolean** | Whether SMS notifications are disabled for recovery |  [optional] |
|**disableEmailNotification** | **Boolean** | Whether email notifications are disabled for recovery |  [optional] |
|**retryCount** | **Integer** | Number of retry attempts for this billing cycle (initial attempt is 0) |  [optional] |
|**paymentReferenceData** | **String** | Reference data received when a payment failed. This data should be returned on retry transactions for the same payment. The value is the reference Revaly returned on the failed attempt and must be echoed unchanged (base64, at most 60 characters as produced). |  [optional] |
|**dateFirstAttempt** | **OffsetDateTime** | Date and time of the first transaction attempt for this billing cycle. Required when retry count is greater than 0. |  [optional] |



