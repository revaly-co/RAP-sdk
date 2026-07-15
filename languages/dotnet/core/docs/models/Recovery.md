# Revaly.Sdk.Core.Model.Recovery
Recovery settings and customer recovery information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**DisableCustomerRecovery** | **bool** | Whether customer recovery is disabled for this transaction | [optional] 
**ExternalApproval** | **bool** | Describes whether the approval should be attributed to the merchant for billing purposes | [optional] 
**CustomerAccountNumber** | **string** | Customer account number for recovery purposes | [optional] 
**CustomerBalance** | **int** | Customer account balance in smallest currency unit (e.g., cents for USD) | [optional] 
**DisableSMSNotification** | **bool** | Whether SMS notifications are disabled for recovery | [optional] 
**DisableEmailNotification** | **bool** | Whether email notifications are disabled for recovery | [optional] 
**RetryCount** | **int** | Number of retry attempts for this billing cycle (initial attempt is 0) | [optional] 
**PaymentReferenceData** | **string** | Reference data received when a payment failed. This data should be returned on retry transactions for the same payment. | [optional] 
**DateFirstAttempt** | **DateTime** | Date and time of the first transaction attempt for this billing cycle. Required when retry count is greater than 0. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

