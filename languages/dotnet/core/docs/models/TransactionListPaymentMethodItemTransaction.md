# Revaly.Sdk.Core.Model.TransactionListPaymentMethodItemTransaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | **string** | Unique transaction identifier | 
**TransactionDate** | **DateTime** | Date and time when the operation was processed (ISO 8601, UTC) | 
**TransactionStatus** | **int** | Status of the operation (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | 
**Message** | **string** | Human-readable message about the result | [optional] 
**CustomerId** | **string** | Customer identifier associated with the operation | [optional] 
**ResponseCode** | **string** | Response code from the processing result | [optional] 
**TransactionType** | **string** | The payment-method operation: CreateCreditCard, CreateGatewayPaymentMethod, UpdatePaymentMethod, RedactPaymentMethod or RecachePaymentMethod | [optional] 
**PaymentMethod** | [**TransactionListPaymentMethod**](TransactionListPaymentMethod.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

