# RtnDataSellerData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**SellerId** | Pointer to **string** | The client&#39;s identifier for the seller. | [optional] 
**SellerBusinessName** | Pointer to **string** | Business name of the seller. | [optional] 
**SellerOwnerName** | Pointer to **string** | Name of the seller or the seller&#39;s owner. | [optional] 
**SellerTenure** | Pointer to **int32** | Number of months the seller has used the client&#39;s services. | [optional] 
**SellerLatitude** | Pointer to **string** | Latitude (decimal degrees) where the purchase was made — seller location, not the cardholder device. | [optional] 
**SellerLongitude** | Pointer to **string** | Longitude (decimal degrees) where the purchase was made — seller location. | [optional] 
**SellerAddress** | Pointer to **string** | Business or contact address of the seller. | [optional] 
**SellerPhone** | Pointer to **string** | Primary phone number of the seller. | [optional] 
**SellerEmail** | Pointer to **string** | Primary email address of the seller. | [optional] 
**SellerPostalCode** | Pointer to **string** | Postal code of the seller&#39;s primary address. | [optional] 
**SellerRegion** | Pointer to **string** | Seller region. APA&#x3D;Asia Pacific &amp; Australia; EMEA&#x3D;Europe/Middle East/Africa; LA/C&#x3D;Latin America &amp; Caribbean. | [optional] 
**SellerCountryCode** | Pointer to **string** | Country of the seller, ISO 3166-1 numeric code as a string. | [optional] 
**TransactionTypeIndicator** | Pointer to **string** | Seller transaction classification. P2P&#x3D;Person to Person; P2M&#x3D;Person to Merchant; CSH&#x3D;Cash. | [optional] 

## Methods

### NewRtnDataSellerData

`func NewRtnDataSellerData() *RtnDataSellerData`

NewRtnDataSellerData instantiates a new RtnDataSellerData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataSellerDataWithDefaults

`func NewRtnDataSellerDataWithDefaults() *RtnDataSellerData`

NewRtnDataSellerDataWithDefaults instantiates a new RtnDataSellerData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetSellerId

`func (o *RtnDataSellerData) GetSellerId() string`

GetSellerId returns the SellerId field if non-nil, zero value otherwise.

### GetSellerIdOk

`func (o *RtnDataSellerData) GetSellerIdOk() (*string, bool)`

GetSellerIdOk returns a tuple with the SellerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerId

`func (o *RtnDataSellerData) SetSellerId(v string)`

SetSellerId sets SellerId field to given value.

### HasSellerId

`func (o *RtnDataSellerData) HasSellerId() bool`

HasSellerId returns a boolean if a field has been set.

### GetSellerBusinessName

`func (o *RtnDataSellerData) GetSellerBusinessName() string`

GetSellerBusinessName returns the SellerBusinessName field if non-nil, zero value otherwise.

### GetSellerBusinessNameOk

`func (o *RtnDataSellerData) GetSellerBusinessNameOk() (*string, bool)`

GetSellerBusinessNameOk returns a tuple with the SellerBusinessName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerBusinessName

`func (o *RtnDataSellerData) SetSellerBusinessName(v string)`

SetSellerBusinessName sets SellerBusinessName field to given value.

### HasSellerBusinessName

`func (o *RtnDataSellerData) HasSellerBusinessName() bool`

HasSellerBusinessName returns a boolean if a field has been set.

### GetSellerOwnerName

`func (o *RtnDataSellerData) GetSellerOwnerName() string`

GetSellerOwnerName returns the SellerOwnerName field if non-nil, zero value otherwise.

### GetSellerOwnerNameOk

`func (o *RtnDataSellerData) GetSellerOwnerNameOk() (*string, bool)`

GetSellerOwnerNameOk returns a tuple with the SellerOwnerName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerOwnerName

`func (o *RtnDataSellerData) SetSellerOwnerName(v string)`

SetSellerOwnerName sets SellerOwnerName field to given value.

### HasSellerOwnerName

`func (o *RtnDataSellerData) HasSellerOwnerName() bool`

HasSellerOwnerName returns a boolean if a field has been set.

### GetSellerTenure

`func (o *RtnDataSellerData) GetSellerTenure() int32`

GetSellerTenure returns the SellerTenure field if non-nil, zero value otherwise.

### GetSellerTenureOk

`func (o *RtnDataSellerData) GetSellerTenureOk() (*int32, bool)`

GetSellerTenureOk returns a tuple with the SellerTenure field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerTenure

`func (o *RtnDataSellerData) SetSellerTenure(v int32)`

SetSellerTenure sets SellerTenure field to given value.

### HasSellerTenure

`func (o *RtnDataSellerData) HasSellerTenure() bool`

HasSellerTenure returns a boolean if a field has been set.

### GetSellerLatitude

`func (o *RtnDataSellerData) GetSellerLatitude() string`

GetSellerLatitude returns the SellerLatitude field if non-nil, zero value otherwise.

### GetSellerLatitudeOk

`func (o *RtnDataSellerData) GetSellerLatitudeOk() (*string, bool)`

GetSellerLatitudeOk returns a tuple with the SellerLatitude field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerLatitude

`func (o *RtnDataSellerData) SetSellerLatitude(v string)`

SetSellerLatitude sets SellerLatitude field to given value.

### HasSellerLatitude

`func (o *RtnDataSellerData) HasSellerLatitude() bool`

HasSellerLatitude returns a boolean if a field has been set.

### GetSellerLongitude

`func (o *RtnDataSellerData) GetSellerLongitude() string`

GetSellerLongitude returns the SellerLongitude field if non-nil, zero value otherwise.

### GetSellerLongitudeOk

`func (o *RtnDataSellerData) GetSellerLongitudeOk() (*string, bool)`

GetSellerLongitudeOk returns a tuple with the SellerLongitude field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerLongitude

`func (o *RtnDataSellerData) SetSellerLongitude(v string)`

SetSellerLongitude sets SellerLongitude field to given value.

### HasSellerLongitude

`func (o *RtnDataSellerData) HasSellerLongitude() bool`

HasSellerLongitude returns a boolean if a field has been set.

### GetSellerAddress

`func (o *RtnDataSellerData) GetSellerAddress() string`

GetSellerAddress returns the SellerAddress field if non-nil, zero value otherwise.

### GetSellerAddressOk

`func (o *RtnDataSellerData) GetSellerAddressOk() (*string, bool)`

GetSellerAddressOk returns a tuple with the SellerAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerAddress

`func (o *RtnDataSellerData) SetSellerAddress(v string)`

SetSellerAddress sets SellerAddress field to given value.

### HasSellerAddress

`func (o *RtnDataSellerData) HasSellerAddress() bool`

HasSellerAddress returns a boolean if a field has been set.

### GetSellerPhone

`func (o *RtnDataSellerData) GetSellerPhone() string`

GetSellerPhone returns the SellerPhone field if non-nil, zero value otherwise.

### GetSellerPhoneOk

`func (o *RtnDataSellerData) GetSellerPhoneOk() (*string, bool)`

GetSellerPhoneOk returns a tuple with the SellerPhone field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerPhone

`func (o *RtnDataSellerData) SetSellerPhone(v string)`

SetSellerPhone sets SellerPhone field to given value.

### HasSellerPhone

`func (o *RtnDataSellerData) HasSellerPhone() bool`

HasSellerPhone returns a boolean if a field has been set.

### GetSellerEmail

`func (o *RtnDataSellerData) GetSellerEmail() string`

GetSellerEmail returns the SellerEmail field if non-nil, zero value otherwise.

### GetSellerEmailOk

`func (o *RtnDataSellerData) GetSellerEmailOk() (*string, bool)`

GetSellerEmailOk returns a tuple with the SellerEmail field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerEmail

`func (o *RtnDataSellerData) SetSellerEmail(v string)`

SetSellerEmail sets SellerEmail field to given value.

### HasSellerEmail

`func (o *RtnDataSellerData) HasSellerEmail() bool`

HasSellerEmail returns a boolean if a field has been set.

### GetSellerPostalCode

`func (o *RtnDataSellerData) GetSellerPostalCode() string`

GetSellerPostalCode returns the SellerPostalCode field if non-nil, zero value otherwise.

### GetSellerPostalCodeOk

`func (o *RtnDataSellerData) GetSellerPostalCodeOk() (*string, bool)`

GetSellerPostalCodeOk returns a tuple with the SellerPostalCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerPostalCode

`func (o *RtnDataSellerData) SetSellerPostalCode(v string)`

SetSellerPostalCode sets SellerPostalCode field to given value.

### HasSellerPostalCode

`func (o *RtnDataSellerData) HasSellerPostalCode() bool`

HasSellerPostalCode returns a boolean if a field has been set.

### GetSellerRegion

`func (o *RtnDataSellerData) GetSellerRegion() string`

GetSellerRegion returns the SellerRegion field if non-nil, zero value otherwise.

### GetSellerRegionOk

`func (o *RtnDataSellerData) GetSellerRegionOk() (*string, bool)`

GetSellerRegionOk returns a tuple with the SellerRegion field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerRegion

`func (o *RtnDataSellerData) SetSellerRegion(v string)`

SetSellerRegion sets SellerRegion field to given value.

### HasSellerRegion

`func (o *RtnDataSellerData) HasSellerRegion() bool`

HasSellerRegion returns a boolean if a field has been set.

### GetSellerCountryCode

`func (o *RtnDataSellerData) GetSellerCountryCode() string`

GetSellerCountryCode returns the SellerCountryCode field if non-nil, zero value otherwise.

### GetSellerCountryCodeOk

`func (o *RtnDataSellerData) GetSellerCountryCodeOk() (*string, bool)`

GetSellerCountryCodeOk returns a tuple with the SellerCountryCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerCountryCode

`func (o *RtnDataSellerData) SetSellerCountryCode(v string)`

SetSellerCountryCode sets SellerCountryCode field to given value.

### HasSellerCountryCode

`func (o *RtnDataSellerData) HasSellerCountryCode() bool`

HasSellerCountryCode returns a boolean if a field has been set.

### GetTransactionTypeIndicator

`func (o *RtnDataSellerData) GetTransactionTypeIndicator() string`

GetTransactionTypeIndicator returns the TransactionTypeIndicator field if non-nil, zero value otherwise.

### GetTransactionTypeIndicatorOk

`func (o *RtnDataSellerData) GetTransactionTypeIndicatorOk() (*string, bool)`

GetTransactionTypeIndicatorOk returns a tuple with the TransactionTypeIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionTypeIndicator

`func (o *RtnDataSellerData) SetTransactionTypeIndicator(v string)`

SetTransactionTypeIndicator sets TransactionTypeIndicator field to given value.

### HasTransactionTypeIndicator

`func (o *RtnDataSellerData) HasTransactionTypeIndicator() bool`

HasTransactionTypeIndicator returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


