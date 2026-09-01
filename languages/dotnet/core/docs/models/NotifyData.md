# Revaly.Sdk.Core.Model.NotifyData
Event-specific data for notification requests

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | **string** | Revaly transaction identifier | [optional] 
**MerchantTransactionId** | **string** | Merchant&#39;s transaction identifier. For &#x60;recordRefund&#x60; events referencing a transaction that was processed through Revaly gateway routing, this field is required, must be at most 50 characters, and must not have been used by any previous transaction — it becomes the recorded refund&#39;s own merchant transaction id, retrievable via &#x60;GET /transactions/merchant/{merchantTransactionId}&#x60;. | [optional] 
**OrderID** | **string** | Order identifier associated with the transaction | [optional] 
**CustomerId** | **string** | Customer identifier | [optional] 
**Amount** | **int** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**Currency** | **string** | Three-letter ISO currency code | [optional] 
**CustomerAccountNumber** | **string** | Customer account number for recovery purposes | [optional] 
**DisableSmsNotification** | **bool** | Whether to disable SMS notifications for this customer | [optional] 
**DisableEmailNotification** | **bool** | Whether to disable email notifications for this customer | [optional] 
**ContactInformation** | [**NotifyContactInformation**](NotifyContactInformation.md) |  | [optional] 
**Address** | [**Address**](Address.md) |  | [optional] 
**ReasonCode** | **string** | Network chargeback reason code (e.g. Visa \&quot;10.4\&quot;). Chargeback-only, optional. | [optional] 
**Arn** | **string** | Acquirer Reference Number or network case ID for the dispute. Chargeback-only, optional. | [optional] 
**DisputeDate** | **DateTime** | When the dispute was raised. Chargeback-only, optional. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

