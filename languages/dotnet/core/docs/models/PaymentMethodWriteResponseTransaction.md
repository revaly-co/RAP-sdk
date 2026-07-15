# Revaly.Sdk.Core.Model.PaymentMethodWriteResponseTransaction
Associated transaction information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | **string** | Unique identifier for the transaction | [optional] 
**TransactionDate** | **DateTime** | Date and time when the transaction was processed | [optional] 
**TransactionStatus** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**Message** | **string** | Human-readable message about the transaction | [optional] 
**ResponseCode** | **string** | Gateway response code | [optional] 
**TransactionType** | **string** | Type of transaction | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

