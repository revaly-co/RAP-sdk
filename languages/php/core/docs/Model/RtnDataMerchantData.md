# RtnDataMerchantData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**acquirer_merchant_id** | **string** | Acquirer-assigned merchant identifier. Optional; no destination financial institution requires it. | [optional]
**issuer_merchant_id** | **string** | Issuer-side merchant identifier, if known. | [optional]
**acquirer_bin** | **string** | BIN of the acquiring institution. | [optional]
**acquirer_reference_number** | **string** | Acquirer reference number (ARN) for network clearing. | [optional]
**merchant_name** | **string** | Merchant display name as it appears to the customer. When omitted, Revaly sends the account&#39;s name as held in the Revaly account configuration, or the account&#39;s primary statement descriptor when no account name is configured. A value that is sent, including an empty string, is passed on as given. | [optional]
**merchant_account_age_indicator** | **string** | Merchant account age token. | [optional]
**merchant_account_opened_date** | **string** | Date the merchant account was created. Format YYYYMMDD. | [optional]
**is_tenured_merchant** | **bool** | True if the merchant has a long-standing, established account relationship. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
