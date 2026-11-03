# Revaly.Sdk.Core.Model.RtnDataMerchantData
Merchant identification and account signals. acquirerMerchantId is optional; no destination financial institution requires it.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**AcquirerMerchantId** | **string** | Acquirer-assigned merchant identifier. Optional; no destination financial institution requires it. | [optional] 
**IssuerMerchantId** | **string** | Issuer-side merchant identifier, if known. | [optional] 
**AcquirerBin** | **string** | BIN of the acquiring institution. | [optional] 
**AcquirerReferenceNumber** | **string** | Acquirer reference number (ARN) for network clearing. | [optional] 
**MerchantName** | **string** | Merchant display name as it appears to the customer. When omitted, Revaly sends the account&#39;s name as held in the Revaly account configuration, or the account&#39;s primary statement descriptor when no account name is configured. A value that is sent, including an empty string, is passed on as given. | [optional] 
**MerchantAccountAgeIndicator** | **string** | Merchant account age token. | [optional] 
**MerchantAccountOpenedDate** | **string** | Date the merchant account was created. Format YYYYMMDD. | [optional] 
**IsTenuredMerchant** | **bool** | True if the merchant has a long-standing, established account relationship. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

