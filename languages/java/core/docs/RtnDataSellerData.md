

# RtnDataSellerData

Seller details for marketplace or platform transactions where the client submits on behalf of a third-party seller (maps to Amex seller_information). All fields optional; omit rather than send nulls.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**sellerId** | **String** | The client&#39;s identifier for the seller. |  [optional] |
|**sellerBusinessName** | **String** | Business name of the seller. |  [optional] |
|**sellerOwnerName** | **String** | Name of the seller or the seller&#39;s owner. |  [optional] |
|**sellerTenure** | **Integer** | Number of months the seller has used the client&#39;s services. |  [optional] |
|**sellerLatitude** | **String** | Latitude (decimal degrees) where the purchase was made — seller location, not the cardholder device. |  [optional] |
|**sellerLongitude** | **String** | Longitude (decimal degrees) where the purchase was made — seller location. |  [optional] |
|**sellerAddress** | **String** | Business or contact address of the seller. |  [optional] |
|**sellerPhone** | **String** | Primary phone number of the seller. |  [optional] |
|**sellerEmail** | **String** | Primary email address of the seller. |  [optional] |
|**sellerPostalCode** | **String** | Postal code of the seller&#39;s primary address. |  [optional] |
|**sellerRegion** | [**SellerRegionEnum**](#SellerRegionEnum) | Seller region. APA&#x3D;Asia Pacific &amp; Australia; EMEA&#x3D;Europe/Middle East/Africa; LA/C&#x3D;Latin America &amp; Caribbean. |  [optional] |
|**sellerCountryCode** | **String** | Country of the seller, ISO 3166-1 numeric code as a string. |  [optional] |
|**transactionTypeIndicator** | [**TransactionTypeIndicatorEnum**](#TransactionTypeIndicatorEnum) | Seller transaction classification. P2P&#x3D;Person to Person; P2M&#x3D;Person to Merchant; CSH&#x3D;Cash. |  [optional] |



## Enum: SellerRegionEnum

| Name | Value |
|---- | -----|
| APA | &quot;APA&quot; |
| CANADA | &quot;Canada&quot; |
| EMEA | &quot;EMEA&quot; |
| LA_C | &quot;LA/C&quot; |
| USA | &quot;USA&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: TransactionTypeIndicatorEnum

| Name | Value |
|---- | -----|
| P2_P | &quot;P2P&quot; |
| P2_M | &quot;P2M&quot; |
| CSH | &quot;CSH&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



