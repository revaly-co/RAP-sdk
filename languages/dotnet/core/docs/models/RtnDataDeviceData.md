# Revaly.Sdk.Core.Model.RtnDataDeviceData
Device and IP signals. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**IpAddress** | **string** | IPv4 or IPv6 address of the device. | [optional] 
**City** | **string** | City derived from IP geolocation. | [optional] 
**Region** | **string** | State or province derived from IP geolocation. | [optional] 
**Country** | **string** | ISO 3166-1 alpha-2 country code from IP geolocation. | [optional] 
**DeviceId** | **string** | Device identifier or fingerprint token. | [optional] 
**IsJavascriptEnabled** | **bool** | True if JavaScript is enabled in the device browser. | [optional] 
**IsJavaEnabled** | **bool** | True if Java is enabled in the device browser. | [optional] 
**UserAgent** | **string** | Browser User-Agent string. | [optional] 
**Timezone** | **string** | IANA timezone identifier. | [optional] 
**TimezoneOffsetMinutes** | **int** | UTC offset in minutes (negative for west of UTC). | [optional] 
**BrowserLanguage** | **string** | IETF BCP 47 language tag. | [optional] 
**DeviceLongitude** | **string** | Device longitude in decimal degrees. West is negative. | [optional] 
**DeviceLatitude** | **string** | Device latitude in decimal degrees. South is negative. | [optional] 
**Channel** | **string** | Application channel through which the transaction was initiated. | [optional] 
**DigitalWalletProviderId** | **string** | Digital wallet provider identifier. | [optional] 
**IsDeviceFraudAssociated** | **bool** | True if the device has a history of fraudulent transactions. | [optional] 
**IsKnownDevice** | **bool** | True if the device has been seen before for this customer. | [optional] 
**DeviceType** | **string** | Hardware form factor, distinct from channel: 01 &#x3D; Phone, 02 &#x3D; Tablet, 03 &#x3D; Computer, 04 &#x3D; Other. | [optional] 
**BrowserTimezoneOffset** | **string** | Browser timezone offset as a string. String companion to timezoneOffsetMinutes for producers/FIs that exchange it as a string. | [optional] 
**SessionCookie** | **string** | Cookie associated with the purchaser&#39;s session. | [optional] 
**PurchaseHostName** | **string** | Host name of the server where the customer placed the purchase. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

