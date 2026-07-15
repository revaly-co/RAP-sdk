# Revaly.Sdk.Core.Model.RtnDataShippingData
Shipping address and delivery signals. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ShippingIndicator** | **string** | Relationship between billing and shipping address: 01 &#x3D; Same as billing, 02 &#x3D; Different (verified), 03 &#x3D; Different (unverified), 04 &#x3D; Retail store pickup, 05 &#x3D; Digital delivery, 06 &#x3D; Not shipped, 07 &#x3D; Other. | [optional] 
**AddressLine1** | **string** | First line of the shipping address. | [optional] 
**AddressLine2** | **string** | Second line of the shipping address. | [optional] 
**AddressLine3** | **string** | Third line of the shipping address. | [optional] 
**City** | **string** | City of the shipping address. | [optional] 
**Region** | **string** | State or province of the shipping address. | [optional] 
**PostalCode** | **string** | Postal or ZIP code of the shipping address. | [optional] 
**Country** | **string** | ISO 3166-1 alpha-2 country code. | [optional] 
**AddressFirstUsedDate** | **string** | Date this shipping address was first used. Format YYYYMMDD. | [optional] 
**AddressFirstUsedIndicator** | **string** | Address age: 01 &#x3D; first time, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**IsShippingNameMatch** | **bool** | True if the shipping name matches the cardholder name. | [optional] 
**DeliveryEmailAddress** | **string** | Email address for electronic/digital delivery. | [optional] 
**DeliveryTimeframeIndicator** | **string** | Delivery timeframe: 01 &#x3D; electronic, 02 &#x3D; same day, 03 &#x3D; next day, 04 &#x3D; 2+ days. | [optional] 
**ShippingFirstName** | **string** | First name of the shipping recipient. | [optional] 
**ShippingLastName** | **string** | Last name of the shipping recipient. | [optional] 
**ShippingPhone** | **string** | Phone number of the shipping recipient. Digits only. | [optional] 
**ShippingAddressCount** | **int** | Number of shipping addresses on the customer&#39;s merchant account. | [optional] 
**DaysSinceShipToAddressChange** | **int** | Days between the last ship-to-address change and the purchase date. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

