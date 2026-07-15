# RtnDataShippingData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ShippingIndicator** | Pointer to **string** | Relationship between billing and shipping address: 01 &#x3D; Same as billing, 02 &#x3D; Different (verified), 03 &#x3D; Different (unverified), 04 &#x3D; Retail store pickup, 05 &#x3D; Digital delivery, 06 &#x3D; Not shipped, 07 &#x3D; Other. | [optional] 
**AddressLine1** | Pointer to **string** | First line of the shipping address. | [optional] 
**AddressLine2** | Pointer to **string** | Second line of the shipping address. | [optional] 
**AddressLine3** | Pointer to **string** | Third line of the shipping address. | [optional] 
**City** | Pointer to **string** | City of the shipping address. | [optional] 
**Region** | Pointer to **string** | State or province of the shipping address. | [optional] 
**PostalCode** | Pointer to **string** | Postal or ZIP code of the shipping address. | [optional] 
**Country** | Pointer to **string** | ISO 3166-1 alpha-2 country code. | [optional] 
**AddressFirstUsedDate** | Pointer to **string** | Date this shipping address was first used. Format YYYYMMDD. | [optional] 
**AddressFirstUsedIndicator** | Pointer to **string** | Address age: 01 &#x3D; first time, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**IsShippingNameMatch** | Pointer to **bool** | True if the shipping name matches the cardholder name. | [optional] 
**DeliveryEmailAddress** | Pointer to **string** | Email address for electronic/digital delivery. | [optional] 
**DeliveryTimeframeIndicator** | Pointer to **string** | Delivery timeframe: 01 &#x3D; electronic, 02 &#x3D; same day, 03 &#x3D; next day, 04 &#x3D; 2+ days. | [optional] 
**ShippingFirstName** | Pointer to **string** | First name of the shipping recipient. | [optional] 
**ShippingLastName** | Pointer to **string** | Last name of the shipping recipient. | [optional] 
**ShippingPhone** | Pointer to **string** | Phone number of the shipping recipient. Digits only. | [optional] 
**ShippingAddressCount** | Pointer to **int32** | Number of shipping addresses on the customer&#39;s merchant account. | [optional] 
**DaysSinceShipToAddressChange** | Pointer to **int32** | Days between the last ship-to-address change and the purchase date. | [optional] 

## Methods

### NewRtnDataShippingData

`func NewRtnDataShippingData() *RtnDataShippingData`

NewRtnDataShippingData instantiates a new RtnDataShippingData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataShippingDataWithDefaults

`func NewRtnDataShippingDataWithDefaults() *RtnDataShippingData`

NewRtnDataShippingDataWithDefaults instantiates a new RtnDataShippingData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetShippingIndicator

`func (o *RtnDataShippingData) GetShippingIndicator() string`

GetShippingIndicator returns the ShippingIndicator field if non-nil, zero value otherwise.

### GetShippingIndicatorOk

`func (o *RtnDataShippingData) GetShippingIndicatorOk() (*string, bool)`

GetShippingIndicatorOk returns a tuple with the ShippingIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingIndicator

`func (o *RtnDataShippingData) SetShippingIndicator(v string)`

SetShippingIndicator sets ShippingIndicator field to given value.

### HasShippingIndicator

`func (o *RtnDataShippingData) HasShippingIndicator() bool`

HasShippingIndicator returns a boolean if a field has been set.

### GetAddressLine1

`func (o *RtnDataShippingData) GetAddressLine1() string`

GetAddressLine1 returns the AddressLine1 field if non-nil, zero value otherwise.

### GetAddressLine1Ok

`func (o *RtnDataShippingData) GetAddressLine1Ok() (*string, bool)`

GetAddressLine1Ok returns a tuple with the AddressLine1 field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAddressLine1

`func (o *RtnDataShippingData) SetAddressLine1(v string)`

SetAddressLine1 sets AddressLine1 field to given value.

### HasAddressLine1

`func (o *RtnDataShippingData) HasAddressLine1() bool`

HasAddressLine1 returns a boolean if a field has been set.

### GetAddressLine2

`func (o *RtnDataShippingData) GetAddressLine2() string`

GetAddressLine2 returns the AddressLine2 field if non-nil, zero value otherwise.

### GetAddressLine2Ok

`func (o *RtnDataShippingData) GetAddressLine2Ok() (*string, bool)`

GetAddressLine2Ok returns a tuple with the AddressLine2 field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAddressLine2

`func (o *RtnDataShippingData) SetAddressLine2(v string)`

SetAddressLine2 sets AddressLine2 field to given value.

### HasAddressLine2

`func (o *RtnDataShippingData) HasAddressLine2() bool`

HasAddressLine2 returns a boolean if a field has been set.

### GetAddressLine3

`func (o *RtnDataShippingData) GetAddressLine3() string`

GetAddressLine3 returns the AddressLine3 field if non-nil, zero value otherwise.

### GetAddressLine3Ok

`func (o *RtnDataShippingData) GetAddressLine3Ok() (*string, bool)`

GetAddressLine3Ok returns a tuple with the AddressLine3 field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAddressLine3

`func (o *RtnDataShippingData) SetAddressLine3(v string)`

SetAddressLine3 sets AddressLine3 field to given value.

### HasAddressLine3

`func (o *RtnDataShippingData) HasAddressLine3() bool`

HasAddressLine3 returns a boolean if a field has been set.

### GetCity

`func (o *RtnDataShippingData) GetCity() string`

GetCity returns the City field if non-nil, zero value otherwise.

### GetCityOk

`func (o *RtnDataShippingData) GetCityOk() (*string, bool)`

GetCityOk returns a tuple with the City field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCity

`func (o *RtnDataShippingData) SetCity(v string)`

SetCity sets City field to given value.

### HasCity

`func (o *RtnDataShippingData) HasCity() bool`

HasCity returns a boolean if a field has been set.

### GetRegion

`func (o *RtnDataShippingData) GetRegion() string`

GetRegion returns the Region field if non-nil, zero value otherwise.

### GetRegionOk

`func (o *RtnDataShippingData) GetRegionOk() (*string, bool)`

GetRegionOk returns a tuple with the Region field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRegion

`func (o *RtnDataShippingData) SetRegion(v string)`

SetRegion sets Region field to given value.

### HasRegion

`func (o *RtnDataShippingData) HasRegion() bool`

HasRegion returns a boolean if a field has been set.

### GetPostalCode

`func (o *RtnDataShippingData) GetPostalCode() string`

GetPostalCode returns the PostalCode field if non-nil, zero value otherwise.

### GetPostalCodeOk

`func (o *RtnDataShippingData) GetPostalCodeOk() (*string, bool)`

GetPostalCodeOk returns a tuple with the PostalCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPostalCode

`func (o *RtnDataShippingData) SetPostalCode(v string)`

SetPostalCode sets PostalCode field to given value.

### HasPostalCode

`func (o *RtnDataShippingData) HasPostalCode() bool`

HasPostalCode returns a boolean if a field has been set.

### GetCountry

`func (o *RtnDataShippingData) GetCountry() string`

GetCountry returns the Country field if non-nil, zero value otherwise.

### GetCountryOk

`func (o *RtnDataShippingData) GetCountryOk() (*string, bool)`

GetCountryOk returns a tuple with the Country field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCountry

`func (o *RtnDataShippingData) SetCountry(v string)`

SetCountry sets Country field to given value.

### HasCountry

`func (o *RtnDataShippingData) HasCountry() bool`

HasCountry returns a boolean if a field has been set.

### GetAddressFirstUsedDate

`func (o *RtnDataShippingData) GetAddressFirstUsedDate() string`

GetAddressFirstUsedDate returns the AddressFirstUsedDate field if non-nil, zero value otherwise.

### GetAddressFirstUsedDateOk

`func (o *RtnDataShippingData) GetAddressFirstUsedDateOk() (*string, bool)`

GetAddressFirstUsedDateOk returns a tuple with the AddressFirstUsedDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAddressFirstUsedDate

`func (o *RtnDataShippingData) SetAddressFirstUsedDate(v string)`

SetAddressFirstUsedDate sets AddressFirstUsedDate field to given value.

### HasAddressFirstUsedDate

`func (o *RtnDataShippingData) HasAddressFirstUsedDate() bool`

HasAddressFirstUsedDate returns a boolean if a field has been set.

### GetAddressFirstUsedIndicator

`func (o *RtnDataShippingData) GetAddressFirstUsedIndicator() string`

GetAddressFirstUsedIndicator returns the AddressFirstUsedIndicator field if non-nil, zero value otherwise.

### GetAddressFirstUsedIndicatorOk

`func (o *RtnDataShippingData) GetAddressFirstUsedIndicatorOk() (*string, bool)`

GetAddressFirstUsedIndicatorOk returns a tuple with the AddressFirstUsedIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAddressFirstUsedIndicator

`func (o *RtnDataShippingData) SetAddressFirstUsedIndicator(v string)`

SetAddressFirstUsedIndicator sets AddressFirstUsedIndicator field to given value.

### HasAddressFirstUsedIndicator

`func (o *RtnDataShippingData) HasAddressFirstUsedIndicator() bool`

HasAddressFirstUsedIndicator returns a boolean if a field has been set.

### GetIsShippingNameMatch

`func (o *RtnDataShippingData) GetIsShippingNameMatch() bool`

GetIsShippingNameMatch returns the IsShippingNameMatch field if non-nil, zero value otherwise.

### GetIsShippingNameMatchOk

`func (o *RtnDataShippingData) GetIsShippingNameMatchOk() (*bool, bool)`

GetIsShippingNameMatchOk returns a tuple with the IsShippingNameMatch field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsShippingNameMatch

`func (o *RtnDataShippingData) SetIsShippingNameMatch(v bool)`

SetIsShippingNameMatch sets IsShippingNameMatch field to given value.

### HasIsShippingNameMatch

`func (o *RtnDataShippingData) HasIsShippingNameMatch() bool`

HasIsShippingNameMatch returns a boolean if a field has been set.

### GetDeliveryEmailAddress

`func (o *RtnDataShippingData) GetDeliveryEmailAddress() string`

GetDeliveryEmailAddress returns the DeliveryEmailAddress field if non-nil, zero value otherwise.

### GetDeliveryEmailAddressOk

`func (o *RtnDataShippingData) GetDeliveryEmailAddressOk() (*string, bool)`

GetDeliveryEmailAddressOk returns a tuple with the DeliveryEmailAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeliveryEmailAddress

`func (o *RtnDataShippingData) SetDeliveryEmailAddress(v string)`

SetDeliveryEmailAddress sets DeliveryEmailAddress field to given value.

### HasDeliveryEmailAddress

`func (o *RtnDataShippingData) HasDeliveryEmailAddress() bool`

HasDeliveryEmailAddress returns a boolean if a field has been set.

### GetDeliveryTimeframeIndicator

`func (o *RtnDataShippingData) GetDeliveryTimeframeIndicator() string`

GetDeliveryTimeframeIndicator returns the DeliveryTimeframeIndicator field if non-nil, zero value otherwise.

### GetDeliveryTimeframeIndicatorOk

`func (o *RtnDataShippingData) GetDeliveryTimeframeIndicatorOk() (*string, bool)`

GetDeliveryTimeframeIndicatorOk returns a tuple with the DeliveryTimeframeIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeliveryTimeframeIndicator

`func (o *RtnDataShippingData) SetDeliveryTimeframeIndicator(v string)`

SetDeliveryTimeframeIndicator sets DeliveryTimeframeIndicator field to given value.

### HasDeliveryTimeframeIndicator

`func (o *RtnDataShippingData) HasDeliveryTimeframeIndicator() bool`

HasDeliveryTimeframeIndicator returns a boolean if a field has been set.

### GetShippingFirstName

`func (o *RtnDataShippingData) GetShippingFirstName() string`

GetShippingFirstName returns the ShippingFirstName field if non-nil, zero value otherwise.

### GetShippingFirstNameOk

`func (o *RtnDataShippingData) GetShippingFirstNameOk() (*string, bool)`

GetShippingFirstNameOk returns a tuple with the ShippingFirstName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingFirstName

`func (o *RtnDataShippingData) SetShippingFirstName(v string)`

SetShippingFirstName sets ShippingFirstName field to given value.

### HasShippingFirstName

`func (o *RtnDataShippingData) HasShippingFirstName() bool`

HasShippingFirstName returns a boolean if a field has been set.

### GetShippingLastName

`func (o *RtnDataShippingData) GetShippingLastName() string`

GetShippingLastName returns the ShippingLastName field if non-nil, zero value otherwise.

### GetShippingLastNameOk

`func (o *RtnDataShippingData) GetShippingLastNameOk() (*string, bool)`

GetShippingLastNameOk returns a tuple with the ShippingLastName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingLastName

`func (o *RtnDataShippingData) SetShippingLastName(v string)`

SetShippingLastName sets ShippingLastName field to given value.

### HasShippingLastName

`func (o *RtnDataShippingData) HasShippingLastName() bool`

HasShippingLastName returns a boolean if a field has been set.

### GetShippingPhone

`func (o *RtnDataShippingData) GetShippingPhone() string`

GetShippingPhone returns the ShippingPhone field if non-nil, zero value otherwise.

### GetShippingPhoneOk

`func (o *RtnDataShippingData) GetShippingPhoneOk() (*string, bool)`

GetShippingPhoneOk returns a tuple with the ShippingPhone field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingPhone

`func (o *RtnDataShippingData) SetShippingPhone(v string)`

SetShippingPhone sets ShippingPhone field to given value.

### HasShippingPhone

`func (o *RtnDataShippingData) HasShippingPhone() bool`

HasShippingPhone returns a boolean if a field has been set.

### GetShippingAddressCount

`func (o *RtnDataShippingData) GetShippingAddressCount() int32`

GetShippingAddressCount returns the ShippingAddressCount field if non-nil, zero value otherwise.

### GetShippingAddressCountOk

`func (o *RtnDataShippingData) GetShippingAddressCountOk() (*int32, bool)`

GetShippingAddressCountOk returns a tuple with the ShippingAddressCount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingAddressCount

`func (o *RtnDataShippingData) SetShippingAddressCount(v int32)`

SetShippingAddressCount sets ShippingAddressCount field to given value.

### HasShippingAddressCount

`func (o *RtnDataShippingData) HasShippingAddressCount() bool`

HasShippingAddressCount returns a boolean if a field has been set.

### GetDaysSinceShipToAddressChange

`func (o *RtnDataShippingData) GetDaysSinceShipToAddressChange() int32`

GetDaysSinceShipToAddressChange returns the DaysSinceShipToAddressChange field if non-nil, zero value otherwise.

### GetDaysSinceShipToAddressChangeOk

`func (o *RtnDataShippingData) GetDaysSinceShipToAddressChangeOk() (*int32, bool)`

GetDaysSinceShipToAddressChangeOk returns a tuple with the DaysSinceShipToAddressChange field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDaysSinceShipToAddressChange

`func (o *RtnDataShippingData) SetDaysSinceShipToAddressChange(v int32)`

SetDaysSinceShipToAddressChange sets DaysSinceShipToAddressChange field to given value.

### HasDaysSinceShipToAddressChange

`func (o *RtnDataShippingData) HasDaysSinceShipToAddressChange() bool`

HasDaysSinceShipToAddressChange returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


