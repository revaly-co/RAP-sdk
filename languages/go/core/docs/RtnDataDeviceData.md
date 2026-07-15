# RtnDataDeviceData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**IpAddress** | Pointer to **string** | IPv4 or IPv6 address of the device. | [optional] 
**City** | Pointer to **string** | City derived from IP geolocation. | [optional] 
**Region** | Pointer to **string** | State or province derived from IP geolocation. | [optional] 
**Country** | Pointer to **string** | ISO 3166-1 alpha-2 country code from IP geolocation. | [optional] 
**DeviceId** | Pointer to **string** | Device identifier or fingerprint token. | [optional] 
**IsJavascriptEnabled** | Pointer to **bool** | True if JavaScript is enabled in the device browser. | [optional] 
**IsJavaEnabled** | Pointer to **bool** | True if Java is enabled in the device browser. | [optional] 
**UserAgent** | Pointer to **string** | Browser User-Agent string. | [optional] 
**Timezone** | Pointer to **string** | IANA timezone identifier. | [optional] 
**TimezoneOffsetMinutes** | Pointer to **int32** | UTC offset in minutes (negative for west of UTC). | [optional] 
**BrowserLanguage** | Pointer to **string** | IETF BCP 47 language tag. | [optional] 
**DeviceLongitude** | Pointer to **string** | Device longitude in decimal degrees. West is negative. | [optional] 
**DeviceLatitude** | Pointer to **string** | Device latitude in decimal degrees. South is negative. | [optional] 
**Channel** | Pointer to **string** | Application channel through which the transaction was initiated. | [optional] 
**DigitalWalletProviderId** | Pointer to **string** | Digital wallet provider identifier. | [optional] 
**IsDeviceFraudAssociated** | Pointer to **bool** | True if the device has a history of fraudulent transactions. | [optional] 
**IsKnownDevice** | Pointer to **bool** | True if the device has been seen before for this customer. | [optional] 
**DeviceType** | Pointer to **string** | Hardware form factor, distinct from channel: 01 &#x3D; Phone, 02 &#x3D; Tablet, 03 &#x3D; Computer, 04 &#x3D; Other. | [optional] 
**BrowserTimezoneOffset** | Pointer to **string** | Browser timezone offset as a string. String companion to timezoneOffsetMinutes for producers/FIs that exchange it as a string. | [optional] 
**SessionCookie** | Pointer to **string** | Cookie associated with the purchaser&#39;s session. | [optional] 
**PurchaseHostName** | Pointer to **string** | Host name of the server where the customer placed the purchase. | [optional] 

## Methods

### NewRtnDataDeviceData

`func NewRtnDataDeviceData() *RtnDataDeviceData`

NewRtnDataDeviceData instantiates a new RtnDataDeviceData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataDeviceDataWithDefaults

`func NewRtnDataDeviceDataWithDefaults() *RtnDataDeviceData`

NewRtnDataDeviceDataWithDefaults instantiates a new RtnDataDeviceData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetIpAddress

`func (o *RtnDataDeviceData) GetIpAddress() string`

GetIpAddress returns the IpAddress field if non-nil, zero value otherwise.

### GetIpAddressOk

`func (o *RtnDataDeviceData) GetIpAddressOk() (*string, bool)`

GetIpAddressOk returns a tuple with the IpAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIpAddress

`func (o *RtnDataDeviceData) SetIpAddress(v string)`

SetIpAddress sets IpAddress field to given value.

### HasIpAddress

`func (o *RtnDataDeviceData) HasIpAddress() bool`

HasIpAddress returns a boolean if a field has been set.

### GetCity

`func (o *RtnDataDeviceData) GetCity() string`

GetCity returns the City field if non-nil, zero value otherwise.

### GetCityOk

`func (o *RtnDataDeviceData) GetCityOk() (*string, bool)`

GetCityOk returns a tuple with the City field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCity

`func (o *RtnDataDeviceData) SetCity(v string)`

SetCity sets City field to given value.

### HasCity

`func (o *RtnDataDeviceData) HasCity() bool`

HasCity returns a boolean if a field has been set.

### GetRegion

`func (o *RtnDataDeviceData) GetRegion() string`

GetRegion returns the Region field if non-nil, zero value otherwise.

### GetRegionOk

`func (o *RtnDataDeviceData) GetRegionOk() (*string, bool)`

GetRegionOk returns a tuple with the Region field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRegion

`func (o *RtnDataDeviceData) SetRegion(v string)`

SetRegion sets Region field to given value.

### HasRegion

`func (o *RtnDataDeviceData) HasRegion() bool`

HasRegion returns a boolean if a field has been set.

### GetCountry

`func (o *RtnDataDeviceData) GetCountry() string`

GetCountry returns the Country field if non-nil, zero value otherwise.

### GetCountryOk

`func (o *RtnDataDeviceData) GetCountryOk() (*string, bool)`

GetCountryOk returns a tuple with the Country field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCountry

`func (o *RtnDataDeviceData) SetCountry(v string)`

SetCountry sets Country field to given value.

### HasCountry

`func (o *RtnDataDeviceData) HasCountry() bool`

HasCountry returns a boolean if a field has been set.

### GetDeviceId

`func (o *RtnDataDeviceData) GetDeviceId() string`

GetDeviceId returns the DeviceId field if non-nil, zero value otherwise.

### GetDeviceIdOk

`func (o *RtnDataDeviceData) GetDeviceIdOk() (*string, bool)`

GetDeviceIdOk returns a tuple with the DeviceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeviceId

`func (o *RtnDataDeviceData) SetDeviceId(v string)`

SetDeviceId sets DeviceId field to given value.

### HasDeviceId

`func (o *RtnDataDeviceData) HasDeviceId() bool`

HasDeviceId returns a boolean if a field has been set.

### GetIsJavascriptEnabled

`func (o *RtnDataDeviceData) GetIsJavascriptEnabled() bool`

GetIsJavascriptEnabled returns the IsJavascriptEnabled field if non-nil, zero value otherwise.

### GetIsJavascriptEnabledOk

`func (o *RtnDataDeviceData) GetIsJavascriptEnabledOk() (*bool, bool)`

GetIsJavascriptEnabledOk returns a tuple with the IsJavascriptEnabled field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsJavascriptEnabled

`func (o *RtnDataDeviceData) SetIsJavascriptEnabled(v bool)`

SetIsJavascriptEnabled sets IsJavascriptEnabled field to given value.

### HasIsJavascriptEnabled

`func (o *RtnDataDeviceData) HasIsJavascriptEnabled() bool`

HasIsJavascriptEnabled returns a boolean if a field has been set.

### GetIsJavaEnabled

`func (o *RtnDataDeviceData) GetIsJavaEnabled() bool`

GetIsJavaEnabled returns the IsJavaEnabled field if non-nil, zero value otherwise.

### GetIsJavaEnabledOk

`func (o *RtnDataDeviceData) GetIsJavaEnabledOk() (*bool, bool)`

GetIsJavaEnabledOk returns a tuple with the IsJavaEnabled field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsJavaEnabled

`func (o *RtnDataDeviceData) SetIsJavaEnabled(v bool)`

SetIsJavaEnabled sets IsJavaEnabled field to given value.

### HasIsJavaEnabled

`func (o *RtnDataDeviceData) HasIsJavaEnabled() bool`

HasIsJavaEnabled returns a boolean if a field has been set.

### GetUserAgent

`func (o *RtnDataDeviceData) GetUserAgent() string`

GetUserAgent returns the UserAgent field if non-nil, zero value otherwise.

### GetUserAgentOk

`func (o *RtnDataDeviceData) GetUserAgentOk() (*string, bool)`

GetUserAgentOk returns a tuple with the UserAgent field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetUserAgent

`func (o *RtnDataDeviceData) SetUserAgent(v string)`

SetUserAgent sets UserAgent field to given value.

### HasUserAgent

`func (o *RtnDataDeviceData) HasUserAgent() bool`

HasUserAgent returns a boolean if a field has been set.

### GetTimezone

`func (o *RtnDataDeviceData) GetTimezone() string`

GetTimezone returns the Timezone field if non-nil, zero value otherwise.

### GetTimezoneOk

`func (o *RtnDataDeviceData) GetTimezoneOk() (*string, bool)`

GetTimezoneOk returns a tuple with the Timezone field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTimezone

`func (o *RtnDataDeviceData) SetTimezone(v string)`

SetTimezone sets Timezone field to given value.

### HasTimezone

`func (o *RtnDataDeviceData) HasTimezone() bool`

HasTimezone returns a boolean if a field has been set.

### GetTimezoneOffsetMinutes

`func (o *RtnDataDeviceData) GetTimezoneOffsetMinutes() int32`

GetTimezoneOffsetMinutes returns the TimezoneOffsetMinutes field if non-nil, zero value otherwise.

### GetTimezoneOffsetMinutesOk

`func (o *RtnDataDeviceData) GetTimezoneOffsetMinutesOk() (*int32, bool)`

GetTimezoneOffsetMinutesOk returns a tuple with the TimezoneOffsetMinutes field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTimezoneOffsetMinutes

`func (o *RtnDataDeviceData) SetTimezoneOffsetMinutes(v int32)`

SetTimezoneOffsetMinutes sets TimezoneOffsetMinutes field to given value.

### HasTimezoneOffsetMinutes

`func (o *RtnDataDeviceData) HasTimezoneOffsetMinutes() bool`

HasTimezoneOffsetMinutes returns a boolean if a field has been set.

### GetBrowserLanguage

`func (o *RtnDataDeviceData) GetBrowserLanguage() string`

GetBrowserLanguage returns the BrowserLanguage field if non-nil, zero value otherwise.

### GetBrowserLanguageOk

`func (o *RtnDataDeviceData) GetBrowserLanguageOk() (*string, bool)`

GetBrowserLanguageOk returns a tuple with the BrowserLanguage field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBrowserLanguage

`func (o *RtnDataDeviceData) SetBrowserLanguage(v string)`

SetBrowserLanguage sets BrowserLanguage field to given value.

### HasBrowserLanguage

`func (o *RtnDataDeviceData) HasBrowserLanguage() bool`

HasBrowserLanguage returns a boolean if a field has been set.

### GetDeviceLongitude

`func (o *RtnDataDeviceData) GetDeviceLongitude() string`

GetDeviceLongitude returns the DeviceLongitude field if non-nil, zero value otherwise.

### GetDeviceLongitudeOk

`func (o *RtnDataDeviceData) GetDeviceLongitudeOk() (*string, bool)`

GetDeviceLongitudeOk returns a tuple with the DeviceLongitude field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeviceLongitude

`func (o *RtnDataDeviceData) SetDeviceLongitude(v string)`

SetDeviceLongitude sets DeviceLongitude field to given value.

### HasDeviceLongitude

`func (o *RtnDataDeviceData) HasDeviceLongitude() bool`

HasDeviceLongitude returns a boolean if a field has been set.

### GetDeviceLatitude

`func (o *RtnDataDeviceData) GetDeviceLatitude() string`

GetDeviceLatitude returns the DeviceLatitude field if non-nil, zero value otherwise.

### GetDeviceLatitudeOk

`func (o *RtnDataDeviceData) GetDeviceLatitudeOk() (*string, bool)`

GetDeviceLatitudeOk returns a tuple with the DeviceLatitude field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeviceLatitude

`func (o *RtnDataDeviceData) SetDeviceLatitude(v string)`

SetDeviceLatitude sets DeviceLatitude field to given value.

### HasDeviceLatitude

`func (o *RtnDataDeviceData) HasDeviceLatitude() bool`

HasDeviceLatitude returns a boolean if a field has been set.

### GetChannel

`func (o *RtnDataDeviceData) GetChannel() string`

GetChannel returns the Channel field if non-nil, zero value otherwise.

### GetChannelOk

`func (o *RtnDataDeviceData) GetChannelOk() (*string, bool)`

GetChannelOk returns a tuple with the Channel field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetChannel

`func (o *RtnDataDeviceData) SetChannel(v string)`

SetChannel sets Channel field to given value.

### HasChannel

`func (o *RtnDataDeviceData) HasChannel() bool`

HasChannel returns a boolean if a field has been set.

### GetDigitalWalletProviderId

`func (o *RtnDataDeviceData) GetDigitalWalletProviderId() string`

GetDigitalWalletProviderId returns the DigitalWalletProviderId field if non-nil, zero value otherwise.

### GetDigitalWalletProviderIdOk

`func (o *RtnDataDeviceData) GetDigitalWalletProviderIdOk() (*string, bool)`

GetDigitalWalletProviderIdOk returns a tuple with the DigitalWalletProviderId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDigitalWalletProviderId

`func (o *RtnDataDeviceData) SetDigitalWalletProviderId(v string)`

SetDigitalWalletProviderId sets DigitalWalletProviderId field to given value.

### HasDigitalWalletProviderId

`func (o *RtnDataDeviceData) HasDigitalWalletProviderId() bool`

HasDigitalWalletProviderId returns a boolean if a field has been set.

### GetIsDeviceFraudAssociated

`func (o *RtnDataDeviceData) GetIsDeviceFraudAssociated() bool`

GetIsDeviceFraudAssociated returns the IsDeviceFraudAssociated field if non-nil, zero value otherwise.

### GetIsDeviceFraudAssociatedOk

`func (o *RtnDataDeviceData) GetIsDeviceFraudAssociatedOk() (*bool, bool)`

GetIsDeviceFraudAssociatedOk returns a tuple with the IsDeviceFraudAssociated field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsDeviceFraudAssociated

`func (o *RtnDataDeviceData) SetIsDeviceFraudAssociated(v bool)`

SetIsDeviceFraudAssociated sets IsDeviceFraudAssociated field to given value.

### HasIsDeviceFraudAssociated

`func (o *RtnDataDeviceData) HasIsDeviceFraudAssociated() bool`

HasIsDeviceFraudAssociated returns a boolean if a field has been set.

### GetIsKnownDevice

`func (o *RtnDataDeviceData) GetIsKnownDevice() bool`

GetIsKnownDevice returns the IsKnownDevice field if non-nil, zero value otherwise.

### GetIsKnownDeviceOk

`func (o *RtnDataDeviceData) GetIsKnownDeviceOk() (*bool, bool)`

GetIsKnownDeviceOk returns a tuple with the IsKnownDevice field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsKnownDevice

`func (o *RtnDataDeviceData) SetIsKnownDevice(v bool)`

SetIsKnownDevice sets IsKnownDevice field to given value.

### HasIsKnownDevice

`func (o *RtnDataDeviceData) HasIsKnownDevice() bool`

HasIsKnownDevice returns a boolean if a field has been set.

### GetDeviceType

`func (o *RtnDataDeviceData) GetDeviceType() string`

GetDeviceType returns the DeviceType field if non-nil, zero value otherwise.

### GetDeviceTypeOk

`func (o *RtnDataDeviceData) GetDeviceTypeOk() (*string, bool)`

GetDeviceTypeOk returns a tuple with the DeviceType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeviceType

`func (o *RtnDataDeviceData) SetDeviceType(v string)`

SetDeviceType sets DeviceType field to given value.

### HasDeviceType

`func (o *RtnDataDeviceData) HasDeviceType() bool`

HasDeviceType returns a boolean if a field has been set.

### GetBrowserTimezoneOffset

`func (o *RtnDataDeviceData) GetBrowserTimezoneOffset() string`

GetBrowserTimezoneOffset returns the BrowserTimezoneOffset field if non-nil, zero value otherwise.

### GetBrowserTimezoneOffsetOk

`func (o *RtnDataDeviceData) GetBrowserTimezoneOffsetOk() (*string, bool)`

GetBrowserTimezoneOffsetOk returns a tuple with the BrowserTimezoneOffset field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBrowserTimezoneOffset

`func (o *RtnDataDeviceData) SetBrowserTimezoneOffset(v string)`

SetBrowserTimezoneOffset sets BrowserTimezoneOffset field to given value.

### HasBrowserTimezoneOffset

`func (o *RtnDataDeviceData) HasBrowserTimezoneOffset() bool`

HasBrowserTimezoneOffset returns a boolean if a field has been set.

### GetSessionCookie

`func (o *RtnDataDeviceData) GetSessionCookie() string`

GetSessionCookie returns the SessionCookie field if non-nil, zero value otherwise.

### GetSessionCookieOk

`func (o *RtnDataDeviceData) GetSessionCookieOk() (*string, bool)`

GetSessionCookieOk returns a tuple with the SessionCookie field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSessionCookie

`func (o *RtnDataDeviceData) SetSessionCookie(v string)`

SetSessionCookie sets SessionCookie field to given value.

### HasSessionCookie

`func (o *RtnDataDeviceData) HasSessionCookie() bool`

HasSessionCookie returns a boolean if a field has been set.

### GetPurchaseHostName

`func (o *RtnDataDeviceData) GetPurchaseHostName() string`

GetPurchaseHostName returns the PurchaseHostName field if non-nil, zero value otherwise.

### GetPurchaseHostNameOk

`func (o *RtnDataDeviceData) GetPurchaseHostNameOk() (*string, bool)`

GetPurchaseHostNameOk returns a tuple with the PurchaseHostName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPurchaseHostName

`func (o *RtnDataDeviceData) SetPurchaseHostName(v string)`

SetPurchaseHostName sets PurchaseHostName field to given value.

### HasPurchaseHostName

`func (o *RtnDataDeviceData) HasPurchaseHostName() bool`

HasPurchaseHostName returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


