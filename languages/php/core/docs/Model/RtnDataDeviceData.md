# RtnDataDeviceData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ip_address** | **string** | IPv4 or IPv6 address of the device. | [optional]
**city** | **string** | City derived from IP geolocation. | [optional]
**region** | **string** | State or province derived from IP geolocation. | [optional]
**country** | **string** | ISO 3166-1 alpha-2 country code from IP geolocation. | [optional]
**device_id** | **string** | Device identifier or fingerprint token. | [optional]
**is_javascript_enabled** | **bool** | True if JavaScript is enabled in the device browser. | [optional]
**is_java_enabled** | **bool** | True if Java is enabled in the device browser. | [optional]
**user_agent** | **string** | Browser User-Agent string. | [optional]
**timezone** | **string** | IANA timezone identifier. | [optional]
**timezone_offset_minutes** | **int** | UTC offset in minutes (negative for west of UTC). | [optional]
**browser_language** | **string** | IETF BCP 47 language tag. | [optional]
**device_longitude** | **string** | Device longitude in decimal degrees. West is negative. | [optional]
**device_latitude** | **string** | Device latitude in decimal degrees. South is negative. | [optional]
**channel** | **string** | Application channel through which the transaction was initiated. | [optional]
**digital_wallet_provider_id** | **string** | Digital wallet provider identifier. | [optional]
**is_device_fraud_associated** | **bool** | True if the device has a history of fraudulent transactions. | [optional]
**is_known_device** | **bool** | True if the device has been seen before for this customer. | [optional]
**device_type** | **string** | Hardware form factor, distinct from channel: 01 &#x3D; Phone, 02 &#x3D; Tablet, 03 &#x3D; Computer, 04 &#x3D; Other. | [optional]
**browser_timezone_offset** | **string** | Browser timezone offset as a string. String companion to timezoneOffsetMinutes for producers/FIs that exchange it as a string. | [optional]
**session_cookie** | **string** | Cookie associated with the purchaser&#39;s session. | [optional]
**purchase_host_name** | **string** | Host name of the server where the customer placed the purchase. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
