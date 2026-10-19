# ThreeDSContext

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Channel** | Pointer to **NullableString** | Interaction channel: BROWSER, MOBILE_APP, SDK, POS or OTHER. Passed to the gateway unchanged; recorded on the 3DS context usage treatment record as one of those five values, matched case-insensitively, with any other value recorded as OTHER. | [optional] 
**UserAgent** | Pointer to **NullableString** | Browser user agent. | [optional] 
**AcceptHeader** | Pointer to **NullableString** | Browser HTTP Accept header. | [optional] 
**BrowserLanguage** | Pointer to **NullableString** | Browser language (IETF BCP 47). | [optional] 
**ColorDepth** | Pointer to **NullableInt32** | Screen colour depth in bits. | [optional] 
**ScreenHeight** | Pointer to **NullableInt32** | Screen height in pixels. | [optional] 
**ScreenWidth** | Pointer to **NullableInt32** | Screen width in pixels. | [optional] 
**TimezoneOffsetMinutes** | Pointer to **NullableInt32** | Browser UTC offset in minutes. | [optional] 
**IsJavaEnabled** | Pointer to **NullableBool** | Whether the browser has Java enabled. | [optional] 
**IsJavascriptEnabled** | Pointer to **NullableBool** | Whether the browser has JavaScript enabled. | [optional] 
**DeviceId** | Pointer to **NullableString** | Merchant or RTN device identifier. | [optional] 
**DeviceFingerprint** | Pointer to **NullableString** | Opaque fingerprint produced by the routed gateway&#39;s client-side script. | [optional] 

## Methods

### NewThreeDSContext

`func NewThreeDSContext() *ThreeDSContext`

NewThreeDSContext instantiates a new ThreeDSContext object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewThreeDSContextWithDefaults

`func NewThreeDSContextWithDefaults() *ThreeDSContext`

NewThreeDSContextWithDefaults instantiates a new ThreeDSContext object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetChannel

`func (o *ThreeDSContext) GetChannel() string`

GetChannel returns the Channel field if non-nil, zero value otherwise.

### GetChannelOk

`func (o *ThreeDSContext) GetChannelOk() (*string, bool)`

GetChannelOk returns a tuple with the Channel field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetChannel

`func (o *ThreeDSContext) SetChannel(v string)`

SetChannel sets Channel field to given value.

### HasChannel

`func (o *ThreeDSContext) HasChannel() bool`

HasChannel returns a boolean if a field has been set.

### SetChannelNil

`func (o *ThreeDSContext) SetChannelNil(b bool)`

 SetChannelNil sets the value for Channel to be an explicit nil

### UnsetChannel
`func (o *ThreeDSContext) UnsetChannel()`

UnsetChannel ensures that no value is present for Channel, not even an explicit nil
### GetUserAgent

`func (o *ThreeDSContext) GetUserAgent() string`

GetUserAgent returns the UserAgent field if non-nil, zero value otherwise.

### GetUserAgentOk

`func (o *ThreeDSContext) GetUserAgentOk() (*string, bool)`

GetUserAgentOk returns a tuple with the UserAgent field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetUserAgent

`func (o *ThreeDSContext) SetUserAgent(v string)`

SetUserAgent sets UserAgent field to given value.

### HasUserAgent

`func (o *ThreeDSContext) HasUserAgent() bool`

HasUserAgent returns a boolean if a field has been set.

### SetUserAgentNil

`func (o *ThreeDSContext) SetUserAgentNil(b bool)`

 SetUserAgentNil sets the value for UserAgent to be an explicit nil

### UnsetUserAgent
`func (o *ThreeDSContext) UnsetUserAgent()`

UnsetUserAgent ensures that no value is present for UserAgent, not even an explicit nil
### GetAcceptHeader

`func (o *ThreeDSContext) GetAcceptHeader() string`

GetAcceptHeader returns the AcceptHeader field if non-nil, zero value otherwise.

### GetAcceptHeaderOk

`func (o *ThreeDSContext) GetAcceptHeaderOk() (*string, bool)`

GetAcceptHeaderOk returns a tuple with the AcceptHeader field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcceptHeader

`func (o *ThreeDSContext) SetAcceptHeader(v string)`

SetAcceptHeader sets AcceptHeader field to given value.

### HasAcceptHeader

`func (o *ThreeDSContext) HasAcceptHeader() bool`

HasAcceptHeader returns a boolean if a field has been set.

### SetAcceptHeaderNil

`func (o *ThreeDSContext) SetAcceptHeaderNil(b bool)`

 SetAcceptHeaderNil sets the value for AcceptHeader to be an explicit nil

### UnsetAcceptHeader
`func (o *ThreeDSContext) UnsetAcceptHeader()`

UnsetAcceptHeader ensures that no value is present for AcceptHeader, not even an explicit nil
### GetBrowserLanguage

`func (o *ThreeDSContext) GetBrowserLanguage() string`

GetBrowserLanguage returns the BrowserLanguage field if non-nil, zero value otherwise.

### GetBrowserLanguageOk

`func (o *ThreeDSContext) GetBrowserLanguageOk() (*string, bool)`

GetBrowserLanguageOk returns a tuple with the BrowserLanguage field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBrowserLanguage

`func (o *ThreeDSContext) SetBrowserLanguage(v string)`

SetBrowserLanguage sets BrowserLanguage field to given value.

### HasBrowserLanguage

`func (o *ThreeDSContext) HasBrowserLanguage() bool`

HasBrowserLanguage returns a boolean if a field has been set.

### SetBrowserLanguageNil

`func (o *ThreeDSContext) SetBrowserLanguageNil(b bool)`

 SetBrowserLanguageNil sets the value for BrowserLanguage to be an explicit nil

### UnsetBrowserLanguage
`func (o *ThreeDSContext) UnsetBrowserLanguage()`

UnsetBrowserLanguage ensures that no value is present for BrowserLanguage, not even an explicit nil
### GetColorDepth

`func (o *ThreeDSContext) GetColorDepth() int32`

GetColorDepth returns the ColorDepth field if non-nil, zero value otherwise.

### GetColorDepthOk

`func (o *ThreeDSContext) GetColorDepthOk() (*int32, bool)`

GetColorDepthOk returns a tuple with the ColorDepth field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetColorDepth

`func (o *ThreeDSContext) SetColorDepth(v int32)`

SetColorDepth sets ColorDepth field to given value.

### HasColorDepth

`func (o *ThreeDSContext) HasColorDepth() bool`

HasColorDepth returns a boolean if a field has been set.

### SetColorDepthNil

`func (o *ThreeDSContext) SetColorDepthNil(b bool)`

 SetColorDepthNil sets the value for ColorDepth to be an explicit nil

### UnsetColorDepth
`func (o *ThreeDSContext) UnsetColorDepth()`

UnsetColorDepth ensures that no value is present for ColorDepth, not even an explicit nil
### GetScreenHeight

`func (o *ThreeDSContext) GetScreenHeight() int32`

GetScreenHeight returns the ScreenHeight field if non-nil, zero value otherwise.

### GetScreenHeightOk

`func (o *ThreeDSContext) GetScreenHeightOk() (*int32, bool)`

GetScreenHeightOk returns a tuple with the ScreenHeight field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetScreenHeight

`func (o *ThreeDSContext) SetScreenHeight(v int32)`

SetScreenHeight sets ScreenHeight field to given value.

### HasScreenHeight

`func (o *ThreeDSContext) HasScreenHeight() bool`

HasScreenHeight returns a boolean if a field has been set.

### SetScreenHeightNil

`func (o *ThreeDSContext) SetScreenHeightNil(b bool)`

 SetScreenHeightNil sets the value for ScreenHeight to be an explicit nil

### UnsetScreenHeight
`func (o *ThreeDSContext) UnsetScreenHeight()`

UnsetScreenHeight ensures that no value is present for ScreenHeight, not even an explicit nil
### GetScreenWidth

`func (o *ThreeDSContext) GetScreenWidth() int32`

GetScreenWidth returns the ScreenWidth field if non-nil, zero value otherwise.

### GetScreenWidthOk

`func (o *ThreeDSContext) GetScreenWidthOk() (*int32, bool)`

GetScreenWidthOk returns a tuple with the ScreenWidth field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetScreenWidth

`func (o *ThreeDSContext) SetScreenWidth(v int32)`

SetScreenWidth sets ScreenWidth field to given value.

### HasScreenWidth

`func (o *ThreeDSContext) HasScreenWidth() bool`

HasScreenWidth returns a boolean if a field has been set.

### SetScreenWidthNil

`func (o *ThreeDSContext) SetScreenWidthNil(b bool)`

 SetScreenWidthNil sets the value for ScreenWidth to be an explicit nil

### UnsetScreenWidth
`func (o *ThreeDSContext) UnsetScreenWidth()`

UnsetScreenWidth ensures that no value is present for ScreenWidth, not even an explicit nil
### GetTimezoneOffsetMinutes

`func (o *ThreeDSContext) GetTimezoneOffsetMinutes() int32`

GetTimezoneOffsetMinutes returns the TimezoneOffsetMinutes field if non-nil, zero value otherwise.

### GetTimezoneOffsetMinutesOk

`func (o *ThreeDSContext) GetTimezoneOffsetMinutesOk() (*int32, bool)`

GetTimezoneOffsetMinutesOk returns a tuple with the TimezoneOffsetMinutes field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTimezoneOffsetMinutes

`func (o *ThreeDSContext) SetTimezoneOffsetMinutes(v int32)`

SetTimezoneOffsetMinutes sets TimezoneOffsetMinutes field to given value.

### HasTimezoneOffsetMinutes

`func (o *ThreeDSContext) HasTimezoneOffsetMinutes() bool`

HasTimezoneOffsetMinutes returns a boolean if a field has been set.

### SetTimezoneOffsetMinutesNil

`func (o *ThreeDSContext) SetTimezoneOffsetMinutesNil(b bool)`

 SetTimezoneOffsetMinutesNil sets the value for TimezoneOffsetMinutes to be an explicit nil

### UnsetTimezoneOffsetMinutes
`func (o *ThreeDSContext) UnsetTimezoneOffsetMinutes()`

UnsetTimezoneOffsetMinutes ensures that no value is present for TimezoneOffsetMinutes, not even an explicit nil
### GetIsJavaEnabled

`func (o *ThreeDSContext) GetIsJavaEnabled() bool`

GetIsJavaEnabled returns the IsJavaEnabled field if non-nil, zero value otherwise.

### GetIsJavaEnabledOk

`func (o *ThreeDSContext) GetIsJavaEnabledOk() (*bool, bool)`

GetIsJavaEnabledOk returns a tuple with the IsJavaEnabled field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsJavaEnabled

`func (o *ThreeDSContext) SetIsJavaEnabled(v bool)`

SetIsJavaEnabled sets IsJavaEnabled field to given value.

### HasIsJavaEnabled

`func (o *ThreeDSContext) HasIsJavaEnabled() bool`

HasIsJavaEnabled returns a boolean if a field has been set.

### SetIsJavaEnabledNil

`func (o *ThreeDSContext) SetIsJavaEnabledNil(b bool)`

 SetIsJavaEnabledNil sets the value for IsJavaEnabled to be an explicit nil

### UnsetIsJavaEnabled
`func (o *ThreeDSContext) UnsetIsJavaEnabled()`

UnsetIsJavaEnabled ensures that no value is present for IsJavaEnabled, not even an explicit nil
### GetIsJavascriptEnabled

`func (o *ThreeDSContext) GetIsJavascriptEnabled() bool`

GetIsJavascriptEnabled returns the IsJavascriptEnabled field if non-nil, zero value otherwise.

### GetIsJavascriptEnabledOk

`func (o *ThreeDSContext) GetIsJavascriptEnabledOk() (*bool, bool)`

GetIsJavascriptEnabledOk returns a tuple with the IsJavascriptEnabled field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsJavascriptEnabled

`func (o *ThreeDSContext) SetIsJavascriptEnabled(v bool)`

SetIsJavascriptEnabled sets IsJavascriptEnabled field to given value.

### HasIsJavascriptEnabled

`func (o *ThreeDSContext) HasIsJavascriptEnabled() bool`

HasIsJavascriptEnabled returns a boolean if a field has been set.

### SetIsJavascriptEnabledNil

`func (o *ThreeDSContext) SetIsJavascriptEnabledNil(b bool)`

 SetIsJavascriptEnabledNil sets the value for IsJavascriptEnabled to be an explicit nil

### UnsetIsJavascriptEnabled
`func (o *ThreeDSContext) UnsetIsJavascriptEnabled()`

UnsetIsJavascriptEnabled ensures that no value is present for IsJavascriptEnabled, not even an explicit nil
### GetDeviceId

`func (o *ThreeDSContext) GetDeviceId() string`

GetDeviceId returns the DeviceId field if non-nil, zero value otherwise.

### GetDeviceIdOk

`func (o *ThreeDSContext) GetDeviceIdOk() (*string, bool)`

GetDeviceIdOk returns a tuple with the DeviceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeviceId

`func (o *ThreeDSContext) SetDeviceId(v string)`

SetDeviceId sets DeviceId field to given value.

### HasDeviceId

`func (o *ThreeDSContext) HasDeviceId() bool`

HasDeviceId returns a boolean if a field has been set.

### SetDeviceIdNil

`func (o *ThreeDSContext) SetDeviceIdNil(b bool)`

 SetDeviceIdNil sets the value for DeviceId to be an explicit nil

### UnsetDeviceId
`func (o *ThreeDSContext) UnsetDeviceId()`

UnsetDeviceId ensures that no value is present for DeviceId, not even an explicit nil
### GetDeviceFingerprint

`func (o *ThreeDSContext) GetDeviceFingerprint() string`

GetDeviceFingerprint returns the DeviceFingerprint field if non-nil, zero value otherwise.

### GetDeviceFingerprintOk

`func (o *ThreeDSContext) GetDeviceFingerprintOk() (*string, bool)`

GetDeviceFingerprintOk returns a tuple with the DeviceFingerprint field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeviceFingerprint

`func (o *ThreeDSContext) SetDeviceFingerprint(v string)`

SetDeviceFingerprint sets DeviceFingerprint field to given value.

### HasDeviceFingerprint

`func (o *ThreeDSContext) HasDeviceFingerprint() bool`

HasDeviceFingerprint returns a boolean if a field has been set.

### SetDeviceFingerprintNil

`func (o *ThreeDSContext) SetDeviceFingerprintNil(b bool)`

 SetDeviceFingerprintNil sets the value for DeviceFingerprint to be an explicit nil

### UnsetDeviceFingerprint
`func (o *ThreeDSContext) UnsetDeviceFingerprint()`

UnsetDeviceFingerprint ensures that no value is present for DeviceFingerprint, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


