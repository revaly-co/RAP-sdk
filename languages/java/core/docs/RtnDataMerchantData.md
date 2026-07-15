

# RtnDataMerchantData

Merchant identification and account signals. acquirerMerchantId is hard-required by RTN downstream but optional in this API.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**acquirerMerchantId** | **String** | Acquirer-assigned merchant identifier. Hard-required by RTN; optional in this API. |  [optional] |
|**issuerMerchantId** | **String** | Issuer-side merchant identifier, if known. |  [optional] |
|**acquirerBin** | **String** | BIN of the acquiring institution. |  [optional] |
|**acquirerReferenceNumber** | **String** | Acquirer reference number (ARN) for network clearing. |  [optional] |
|**merchantName** | **String** | Merchant display name as it appears to the customer. |  [optional] |
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



