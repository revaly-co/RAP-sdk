# GatewayPaymentMethod

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**GatewayPaymentMethodId** | Pointer to **NullableString** | Token identifier from the payment gateway | [optional] 
**Bin** | Pointer to **NullableString** | Bank Identification Number (first 6 or 8 digits) | [optional] 
**LastFourDigits** | Pointer to **NullableString** | Last four digits of the payment method | [optional] 
**ExpiryYear** | Pointer to **NullableString** | Expiration year (YYYY) | [optional] 
**ExpiryMonth** | Pointer to **NullableString** | Expiration month (01-12) | [optional] 

## Methods

### NewGatewayPaymentMethod

`func NewGatewayPaymentMethod() *GatewayPaymentMethod`

NewGatewayPaymentMethod instantiates a new GatewayPaymentMethod object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewGatewayPaymentMethodWithDefaults

`func NewGatewayPaymentMethodWithDefaults() *GatewayPaymentMethod`

NewGatewayPaymentMethodWithDefaults instantiates a new GatewayPaymentMethod object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetGatewayPaymentMethodId

`func (o *GatewayPaymentMethod) GetGatewayPaymentMethodId() string`

GetGatewayPaymentMethodId returns the GatewayPaymentMethodId field if non-nil, zero value otherwise.

### GetGatewayPaymentMethodIdOk

`func (o *GatewayPaymentMethod) GetGatewayPaymentMethodIdOk() (*string, bool)`

GetGatewayPaymentMethodIdOk returns a tuple with the GatewayPaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayPaymentMethodId

`func (o *GatewayPaymentMethod) SetGatewayPaymentMethodId(v string)`

SetGatewayPaymentMethodId sets GatewayPaymentMethodId field to given value.

### HasGatewayPaymentMethodId

`func (o *GatewayPaymentMethod) HasGatewayPaymentMethodId() bool`

HasGatewayPaymentMethodId returns a boolean if a field has been set.

### SetGatewayPaymentMethodIdNil

`func (o *GatewayPaymentMethod) SetGatewayPaymentMethodIdNil(b bool)`

 SetGatewayPaymentMethodIdNil sets the value for GatewayPaymentMethodId to be an explicit nil

### UnsetGatewayPaymentMethodId
`func (o *GatewayPaymentMethod) UnsetGatewayPaymentMethodId()`

UnsetGatewayPaymentMethodId ensures that no value is present for GatewayPaymentMethodId, not even an explicit nil
### GetBin

`func (o *GatewayPaymentMethod) GetBin() string`

GetBin returns the Bin field if non-nil, zero value otherwise.

### GetBinOk

`func (o *GatewayPaymentMethod) GetBinOk() (*string, bool)`

GetBinOk returns a tuple with the Bin field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBin

`func (o *GatewayPaymentMethod) SetBin(v string)`

SetBin sets Bin field to given value.

### HasBin

`func (o *GatewayPaymentMethod) HasBin() bool`

HasBin returns a boolean if a field has been set.

### SetBinNil

`func (o *GatewayPaymentMethod) SetBinNil(b bool)`

 SetBinNil sets the value for Bin to be an explicit nil

### UnsetBin
`func (o *GatewayPaymentMethod) UnsetBin()`

UnsetBin ensures that no value is present for Bin, not even an explicit nil
### GetLastFourDigits

`func (o *GatewayPaymentMethod) GetLastFourDigits() string`

GetLastFourDigits returns the LastFourDigits field if non-nil, zero value otherwise.

### GetLastFourDigitsOk

`func (o *GatewayPaymentMethod) GetLastFourDigitsOk() (*string, bool)`

GetLastFourDigitsOk returns a tuple with the LastFourDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastFourDigits

`func (o *GatewayPaymentMethod) SetLastFourDigits(v string)`

SetLastFourDigits sets LastFourDigits field to given value.

### HasLastFourDigits

`func (o *GatewayPaymentMethod) HasLastFourDigits() bool`

HasLastFourDigits returns a boolean if a field has been set.

### SetLastFourDigitsNil

`func (o *GatewayPaymentMethod) SetLastFourDigitsNil(b bool)`

 SetLastFourDigitsNil sets the value for LastFourDigits to be an explicit nil

### UnsetLastFourDigits
`func (o *GatewayPaymentMethod) UnsetLastFourDigits()`

UnsetLastFourDigits ensures that no value is present for LastFourDigits, not even an explicit nil
### GetExpiryYear

`func (o *GatewayPaymentMethod) GetExpiryYear() string`

GetExpiryYear returns the ExpiryYear field if non-nil, zero value otherwise.

### GetExpiryYearOk

`func (o *GatewayPaymentMethod) GetExpiryYearOk() (*string, bool)`

GetExpiryYearOk returns a tuple with the ExpiryYear field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryYear

`func (o *GatewayPaymentMethod) SetExpiryYear(v string)`

SetExpiryYear sets ExpiryYear field to given value.

### HasExpiryYear

`func (o *GatewayPaymentMethod) HasExpiryYear() bool`

HasExpiryYear returns a boolean if a field has been set.

### SetExpiryYearNil

`func (o *GatewayPaymentMethod) SetExpiryYearNil(b bool)`

 SetExpiryYearNil sets the value for ExpiryYear to be an explicit nil

### UnsetExpiryYear
`func (o *GatewayPaymentMethod) UnsetExpiryYear()`

UnsetExpiryYear ensures that no value is present for ExpiryYear, not even an explicit nil
### GetExpiryMonth

`func (o *GatewayPaymentMethod) GetExpiryMonth() string`

GetExpiryMonth returns the ExpiryMonth field if non-nil, zero value otherwise.

### GetExpiryMonthOk

`func (o *GatewayPaymentMethod) GetExpiryMonthOk() (*string, bool)`

GetExpiryMonthOk returns a tuple with the ExpiryMonth field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryMonth

`func (o *GatewayPaymentMethod) SetExpiryMonth(v string)`

SetExpiryMonth sets ExpiryMonth field to given value.

### HasExpiryMonth

`func (o *GatewayPaymentMethod) HasExpiryMonth() bool`

HasExpiryMonth returns a boolean if a field has been set.

### SetExpiryMonthNil

`func (o *GatewayPaymentMethod) SetExpiryMonthNil(b bool)`

 SetExpiryMonthNil sets the value for ExpiryMonth to be an explicit nil

### UnsetExpiryMonth
`func (o *GatewayPaymentMethod) UnsetExpiryMonth()`

UnsetExpiryMonth ensures that no value is present for ExpiryMonth, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


