# Revaly.Sdk.Core.Model.RtnDataMerchantData
Merchant identification and account signals. acquirerMerchantId is hard-required by RTN downstream but optional in this API.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**AcquirerMerchantId** | **string** | Acquirer-assigned merchant identifier. Hard-required by RTN; optional in this API. | [optional] 
**IssuerMerchantId** | **string** | Issuer-side merchant identifier, if known. | [optional] 
**AcquirerBin** | **string** | BIN of the acquiring institution. | [optional] 
**AcquirerReferenceNumber** | **string** | Acquirer reference number (ARN) for network clearing. | [optional] 
**MerchantName** | **string** | Merchant display name as it appears to the customer. | [optional] 
**MerchantAccountAgeIndicator** | **string** | Merchant account age token. | [optional] 
**MerchantAccountOpenedDate** | **string** | Date the merchant account was created. Format YYYYMMDD. | [optional] 
**IsTenuredMerchant** | **bool** | True if the merchant has a long-standing, established account relationship. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

