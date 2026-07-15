# Revaly.Sdk.Core.Model.RtnDataSellerData
Seller details for marketplace or platform transactions where the client submits on behalf of a third-party seller (maps to Amex seller_information). All fields optional; omit rather than send nulls.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**SellerId** | **string** | The client&#39;s identifier for the seller. | [optional] 
**SellerBusinessName** | **string** | Business name of the seller. | [optional] 
**SellerOwnerName** | **string** | Name of the seller or the seller&#39;s owner. | [optional] 
**SellerTenure** | **int** | Number of months the seller has used the client&#39;s services. | [optional] 
**SellerLatitude** | **string** | Latitude (decimal degrees) where the purchase was made — seller location, not the cardholder device. | [optional] 
**SellerLongitude** | **string** | Longitude (decimal degrees) where the purchase was made — seller location. | [optional] 
**SellerAddress** | **string** | Business or contact address of the seller. | [optional] 
**SellerPhone** | **string** | Primary phone number of the seller. | [optional] 
**SellerEmail** | **string** | Primary email address of the seller. | [optional] 
**SellerPostalCode** | **string** | Postal code of the seller&#39;s primary address. | [optional] 
**SellerRegion** | **string** | Seller region. APA&#x3D;Asia Pacific &amp; Australia; EMEA&#x3D;Europe/Middle East/Africa; LA/C&#x3D;Latin America &amp; Caribbean. | [optional] 
**SellerCountryCode** | **string** | Country of the seller, ISO 3166-1 numeric code as a string. | [optional] 
**TransactionTypeIndicator** | **string** | Seller transaction classification. P2P&#x3D;Person to Person; P2M&#x3D;Person to Merchant; CSH&#x3D;Cash. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

