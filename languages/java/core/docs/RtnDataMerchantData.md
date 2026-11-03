

# RtnDataMerchantData

Merchant identification and account signals. acquirerMerchantId is optional; no destination financial institution requires it.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**acquirerMerchantId** | **String** | Acquirer-assigned merchant identifier. Optional; no destination financial institution requires it. |  [optional] |
|**issuerMerchantId** | **String** | Issuer-side merchant identifier, if known. |  [optional] |
|**acquirerBin** | **String** | BIN of the acquiring institution. |  [optional] |
|**acquirerReferenceNumber** | **String** | Acquirer reference number (ARN) for network clearing. |  [optional] |
|**merchantName** | **String** | Merchant display name as it appears to the customer. When omitted, Revaly sends the account&#39;s name as held in the Revaly account configuration, or the account&#39;s primary statement descriptor when no account name is configured. A value that is sent, including an empty string, is passed on as given. |  [optional] |
|**merchantAccountAgeIndicator** | [**MerchantAccountAgeIndicatorEnum**](#MerchantAccountAgeIndicatorEnum) | Merchant account age token. |  [optional] |
|**merchantAccountOpenedDate** | **String** | Date the merchant account was created. Format YYYYMMDD. |  [optional] |
|**isTenuredMerchant** | **Boolean** | True if the merchant has a long-standing, established account relationship. |  [optional] |



## Enum: MerchantAccountAgeIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _03 | &quot;03&quot; |
| _05 | &quot;05&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



