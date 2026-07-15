# Revaly.Sdk.Core.Model.PreviousTransaction
Information about a previous transaction for reference

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionDate** | **DateTime** | Date of the previous transaction | [optional] 
**MerchantAccountReferenceId** | **string** | Merchant account reference ID from the previous transaction | [optional] 
**GatewayCode** | **string** | Gateway response code from the previous transaction | [optional] 
**GatewayMessage** | **string** | Gateway response message from the previous transaction | [optional] 
**GatewayMessageKey** | **string** | Gateway message key from the previous transaction | [optional] 
**TransactionStatus** | **int** | Previous status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**AvsCode** | **string** | AVS code from the previous transaction | [optional] 
**AvsMessage** | **string** | AVS message from the previous transaction | [optional] 
**CvvCode** | **string** | CVV code from the previous transaction | [optional] 
**CvvMessage** | **string** | CVV message from the previous transaction | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

