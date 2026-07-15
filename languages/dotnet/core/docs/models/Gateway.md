# Revaly.Sdk.Core.Model.Gateway
Gateway configuration and settings

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Name** | **string** | Gateway name | [optional] 
**BankTypeCode** | **string** | Bank type code | [optional] 
**MerchantAccountReferenceId** | **string** | Merchant account reference ID at the gateway | [optional] 
**GatewayType** | **string** | Type of payment gateway | [optional] 
**CurrencyCode** | **string** | Primary currency code for this gateway | [optional] 
**AcceptedCurrencyCodes** | **List&lt;string&gt;** | List of accepted currency codes | [optional] 
**AcceptedCards** | [**AcceptedCards**](AcceptedCards.md) |  | [optional] 
**AcceptRetries** | **bool** | Whether the gateway accepts retry transactions | [optional] 
**CvvRequired** | **bool** | Whether CVV is required for transactions | [optional] 
**ApprovedChargeOrCaptureRateFee** | **double** | Rate fee for approved charges or captures | [optional] 
**ApprovedChargeOrCaptureFlatFee** | **double** | Flat fee for approved charges or captures | [optional] 
**OtherTransactionFlatFee** | **double** | Flat fee for other transaction types | [optional] 
**IssueRefundsThroughCredit** | **bool** | Whether refunds are issued through credit | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

