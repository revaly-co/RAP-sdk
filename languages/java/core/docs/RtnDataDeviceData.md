

# RtnDataDeviceData

Device and IP signals. All fields optional.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**ipAddress** | **String** | IPv4 or IPv6 address of the device. |  [optional] |
|**city** | **String** | City derived from IP geolocation. |  [optional] |
|**region** | **String** | State or province derived from IP geolocation. |  [optional] |
|**country** | **String** | ISO 3166-1 alpha-2 country code from IP geolocation. |  [optional] |
|**deviceId** | **String** | Device identifier or fingerprint token. |  [optional] |
|**isJavascriptEnabled** | **Boolean** | True if JavaScript is enabled in the device browser. |  [optional] |
|**isJavaEnabled** | **Boolean** | True if Java is enabled in the device browser. |  [optional] |
|**userAgent** | **String** | Browser User-Agent string. |  [optional] |
|**timezone** | **String** | IANA timezone identifier. |  [optional] |
|**timezoneOffsetMinutes** | **Integer** | UTC offset in minutes (negative for west of UTC). |  [optional] |
|**browserLanguage** | **String** | IETF BCP 47 language tag. |  [optional] |
|**deviceLongitude** | **String** | Device longitude in decimal degrees. West is negative. |  [optional] |
|**deviceLatitude** | **String** | Device latitude in decimal degrees. South is negative. |  [optional] |
|**channel** | [**ChannelEnum**](#ChannelEnum) | Application channel through which the transaction was initiated. |  [optional] |
|**digitalWalletProviderId** | **String** | Digital wallet provider identifier. |  [optional] |
|**isDeviceFraudAssociated** | **Boolean** | True if the device has a history of fraudulent transactions. |  [optional] |
|**isKnownDevice** | **Boolean** | True if the device has been seen before for this customer. |  [optional] |
|**deviceType** | [**DeviceTypeEnum**](#DeviceTypeEnum) | Hardware form factor, distinct from channel: 01 &#x3D; Phone, 02 &#x3D; Tablet, 03 &#x3D; Computer, 04 &#x3D; Other. |  [optional] |
|**browserTimezoneOffset** | **String** | Browser timezone offset as a string. String companion to timezoneOffsetMinutes for producers/FIs that exchange it as a string. |  [optional] |
|**sessionCookie** | **String** | Cookie associated with the purchaser&#39;s session. |  [optional] |
|**purchaseHostName** | **String** | Host name of the server where the customer placed the purchase. |  [optional] |



## Enum: ChannelEnum

| Name | Value |
|---- | -----|
| BROWSER | &quot;BROWSER&quot; |
| MOBILE_APP | &quot;MOBILE_APP&quot; |
| SDK | &quot;SDK&quot; |
| POS | &quot;POS&quot; |
| OTHER | &quot;OTHER&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: DeviceTypeEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



