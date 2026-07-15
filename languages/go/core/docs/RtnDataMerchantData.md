# RtnDataMerchantData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**AcquirerMerchantId** | Pointer to **string** | Acquirer-assigned merchant identifier. Hard-required by RTN; optional in this API. | [optional] 
**IssuerMerchantId** | Pointer to **string** | Issuer-side merchant identifier, if known. | [optional] 
**AcquirerBin** | Pointer to **string** | BIN of the acquiring institution. | [optional] 
**AcquirerReferenceNumber** | Pointer to **string** | Acquirer reference number (ARN) for network clearing. | [optional] 
**MerchantName** | Pointer to **string** | Merchant display name as it appears to the customer. | [optional] 
**MerchantAccountAgeIndicator** | Pointer to **string** | Merchant account age token. | [optional] 
**MerchantAccountOpenedDate** | Pointer to **string** | Date the merchant account was created. Format YYYYMMDD. | [optional] 
**IsTenuredMerchant** | Pointer to **bool** | True if the merchant has a long-standing, established account relationship. | [optional] 

## Methods

### NewRtnDataMerchantData

`func NewRtnDataMerchantData() *RtnDataMerchantData`

NewRtnDataMerchantData instantiates a new RtnDataMerchantData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataMerchantDataWithDefaults

`func NewRtnDataMerchantDataWithDefaults() *RtnDataMerchantData`

NewRtnDataMerchantDataWithDefaults instantiates a new RtnDataMerchantData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetAcquirerMerchantId

`func (o *RtnDataMerchantData) GetAcquirerMerchantId() string`

GetAcquirerMerchantId returns the AcquirerMerchantId field if non-nil, zero value otherwise.

### GetAcquirerMerchantIdOk

`func (o *RtnDataMerchantData) GetAcquirerMerchantIdOk() (*string, bool)`

GetAcquirerMerchantIdOk returns a tuple with the AcquirerMerchantId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcquirerMerchantId

`func (o *RtnDataMerchantData) SetAcquirerMerchantId(v string)`

SetAcquirerMerchantId sets AcquirerMerchantId field to given value.

### HasAcquirerMerchantId

`func (o *RtnDataMerchantData) HasAcquirerMerchantId() bool`

HasAcquirerMerchantId returns a boolean if a field has been set.

### GetIssuerMerchantId

`func (o *RtnDataMerchantData) GetIssuerMerchantId() string`

GetIssuerMerchantId returns the IssuerMerchantId field if non-nil, zero value otherwise.

### GetIssuerMerchantIdOk

`func (o *RtnDataMerchantData) GetIssuerMerchantIdOk() (*string, bool)`

GetIssuerMerchantIdOk returns a tuple with the IssuerMerchantId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIssuerMerchantId

`func (o *RtnDataMerchantData) SetIssuerMerchantId(v string)`

SetIssuerMerchantId sets IssuerMerchantId field to given value.

### HasIssuerMerchantId

`func (o *RtnDataMerchantData) HasIssuerMerchantId() bool`

HasIssuerMerchantId returns a boolean if a field has been set.

### GetAcquirerBin

`func (o *RtnDataMerchantData) GetAcquirerBin() string`

GetAcquirerBin returns the AcquirerBin field if non-nil, zero value otherwise.

### GetAcquirerBinOk

`func (o *RtnDataMerchantData) GetAcquirerBinOk() (*string, bool)`

GetAcquirerBinOk returns a tuple with the AcquirerBin field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcquirerBin

`func (o *RtnDataMerchantData) SetAcquirerBin(v string)`

SetAcquirerBin sets AcquirerBin field to given value.

### HasAcquirerBin

`func (o *RtnDataMerchantData) HasAcquirerBin() bool`

HasAcquirerBin returns a boolean if a field has been set.

### GetAcquirerReferenceNumber

`func (o *RtnDataMerchantData) GetAcquirerReferenceNumber() string`

GetAcquirerReferenceNumber returns the AcquirerReferenceNumber field if non-nil, zero value otherwise.

### GetAcquirerReferenceNumberOk

`func (o *RtnDataMerchantData) GetAcquirerReferenceNumberOk() (*string, bool)`

GetAcquirerReferenceNumberOk returns a tuple with the AcquirerReferenceNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcquirerReferenceNumber

`func (o *RtnDataMerchantData) SetAcquirerReferenceNumber(v string)`

SetAcquirerReferenceNumber sets AcquirerReferenceNumber field to given value.

### HasAcquirerReferenceNumber

`func (o *RtnDataMerchantData) HasAcquirerReferenceNumber() bool`

HasAcquirerReferenceNumber returns a boolean if a field has been set.

### GetMerchantName

`func (o *RtnDataMerchantData) GetMerchantName() string`

GetMerchantName returns the MerchantName field if non-nil, zero value otherwise.

### GetMerchantNameOk

`func (o *RtnDataMerchantData) GetMerchantNameOk() (*string, bool)`

GetMerchantNameOk returns a tuple with the MerchantName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantName

`func (o *RtnDataMerchantData) SetMerchantName(v string)`

SetMerchantName sets MerchantName field to given value.

### HasMerchantName

`func (o *RtnDataMerchantData) HasMerchantName() bool`

HasMerchantName returns a boolean if a field has been set.

### GetMerchantAccountAgeIndicator

`func (o *RtnDataMerchantData) GetMerchantAccountAgeIndicator() string`

GetMerchantAccountAgeIndicator returns the MerchantAccountAgeIndicator field if non-nil, zero value otherwise.

### GetMerchantAccountAgeIndicatorOk

`func (o *RtnDataMerchantData) GetMerchantAccountAgeIndicatorOk() (*string, bool)`

GetMerchantAccountAgeIndicatorOk returns a tuple with the MerchantAccountAgeIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantAccountAgeIndicator

`func (o *RtnDataMerchantData) SetMerchantAccountAgeIndicator(v string)`

SetMerchantAccountAgeIndicator sets MerchantAccountAgeIndicator field to given value.

### HasMerchantAccountAgeIndicator

`func (o *RtnDataMerchantData) HasMerchantAccountAgeIndicator() bool`

HasMerchantAccountAgeIndicator returns a boolean if a field has been set.

### GetMerchantAccountOpenedDate

`func (o *RtnDataMerchantData) GetMerchantAccountOpenedDate() string`

GetMerchantAccountOpenedDate returns the MerchantAccountOpenedDate field if non-nil, zero value otherwise.

### GetMerchantAccountOpenedDateOk

`func (o *RtnDataMerchantData) GetMerchantAccountOpenedDateOk() (*string, bool)`

GetMerchantAccountOpenedDateOk returns a tuple with the MerchantAccountOpenedDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantAccountOpenedDate

`func (o *RtnDataMerchantData) SetMerchantAccountOpenedDate(v string)`

SetMerchantAccountOpenedDate sets MerchantAccountOpenedDate field to given value.

### HasMerchantAccountOpenedDate

`func (o *RtnDataMerchantData) HasMerchantAccountOpenedDate() bool`

HasMerchantAccountOpenedDate returns a boolean if a field has been set.

### GetIsTenuredMerchant

`func (o *RtnDataMerchantData) GetIsTenuredMerchant() bool`

GetIsTenuredMerchant returns the IsTenuredMerchant field if non-nil, zero value otherwise.

### GetIsTenuredMerchantOk

`func (o *RtnDataMerchantData) GetIsTenuredMerchantOk() (*bool, bool)`

GetIsTenuredMerchantOk returns a tuple with the IsTenuredMerchant field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsTenuredMerchant

`func (o *RtnDataMerchantData) SetIsTenuredMerchant(v bool)`

SetIsTenuredMerchant sets IsTenuredMerchant field to given value.

### HasIsTenuredMerchant

`func (o *RtnDataMerchantData) HasIsTenuredMerchant() bool`

HasIsTenuredMerchant returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


