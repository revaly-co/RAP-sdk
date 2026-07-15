# VaultPaymentMethod

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**VaultToken** | Pointer to **NullableString** | Vault-issued token (any provider) used to authorize a payment. Valid only on &#x60;/payments/charge&#x60; and &#x60;/payments/authorize&#x60; when &#x60;paymentMethodType&#x60; is &#x60;vaultToken&#x60;. Requires &#x60;paymentMethod.merchantAccountReferenceId&#x60; for gateway routing. Must not be combined with &#x60;creditCard&#x60; or &#x60;gatewayPaymentMethod&#x60;.  | [optional] 
**Bin** | Pointer to **NullableString** | Bank Identification Number (first 6 or 8 digits) | [optional] 
**LastFourDigits** | Pointer to **NullableString** | Last four digits of the payment method | [optional] 
**ExpiryYear** | Pointer to **NullableString** | Expiration year (YYYY) | [optional] 
**ExpiryMonth** | Pointer to **NullableString** | Expiration month (01-12) | [optional] 

## Methods

### NewVaultPaymentMethod

`func NewVaultPaymentMethod() *VaultPaymentMethod`

NewVaultPaymentMethod instantiates a new VaultPaymentMethod object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewVaultPaymentMethodWithDefaults

`func NewVaultPaymentMethodWithDefaults() *VaultPaymentMethod`

NewVaultPaymentMethodWithDefaults instantiates a new VaultPaymentMethod object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetVaultToken

`func (o *VaultPaymentMethod) GetVaultToken() string`

GetVaultToken returns the VaultToken field if non-nil, zero value otherwise.

### GetVaultTokenOk

`func (o *VaultPaymentMethod) GetVaultTokenOk() (*string, bool)`

GetVaultTokenOk returns a tuple with the VaultToken field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetVaultToken

`func (o *VaultPaymentMethod) SetVaultToken(v string)`

SetVaultToken sets VaultToken field to given value.

### HasVaultToken

`func (o *VaultPaymentMethod) HasVaultToken() bool`

HasVaultToken returns a boolean if a field has been set.

### SetVaultTokenNil

`func (o *VaultPaymentMethod) SetVaultTokenNil(b bool)`

 SetVaultTokenNil sets the value for VaultToken to be an explicit nil

### UnsetVaultToken
`func (o *VaultPaymentMethod) UnsetVaultToken()`

UnsetVaultToken ensures that no value is present for VaultToken, not even an explicit nil
### GetBin

`func (o *VaultPaymentMethod) GetBin() string`

GetBin returns the Bin field if non-nil, zero value otherwise.

### GetBinOk

`func (o *VaultPaymentMethod) GetBinOk() (*string, bool)`

GetBinOk returns a tuple with the Bin field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBin

`func (o *VaultPaymentMethod) SetBin(v string)`

SetBin sets Bin field to given value.

### HasBin

`func (o *VaultPaymentMethod) HasBin() bool`

HasBin returns a boolean if a field has been set.

### SetBinNil

`func (o *VaultPaymentMethod) SetBinNil(b bool)`

 SetBinNil sets the value for Bin to be an explicit nil

### UnsetBin
`func (o *VaultPaymentMethod) UnsetBin()`

UnsetBin ensures that no value is present for Bin, not even an explicit nil
### GetLastFourDigits

`func (o *VaultPaymentMethod) GetLastFourDigits() string`

GetLastFourDigits returns the LastFourDigits field if non-nil, zero value otherwise.

### GetLastFourDigitsOk

`func (o *VaultPaymentMethod) GetLastFourDigitsOk() (*string, bool)`

GetLastFourDigitsOk returns a tuple with the LastFourDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastFourDigits

`func (o *VaultPaymentMethod) SetLastFourDigits(v string)`

SetLastFourDigits sets LastFourDigits field to given value.

### HasLastFourDigits

`func (o *VaultPaymentMethod) HasLastFourDigits() bool`

HasLastFourDigits returns a boolean if a field has been set.

### SetLastFourDigitsNil

`func (o *VaultPaymentMethod) SetLastFourDigitsNil(b bool)`

 SetLastFourDigitsNil sets the value for LastFourDigits to be an explicit nil

### UnsetLastFourDigits
`func (o *VaultPaymentMethod) UnsetLastFourDigits()`

UnsetLastFourDigits ensures that no value is present for LastFourDigits, not even an explicit nil
### GetExpiryYear

`func (o *VaultPaymentMethod) GetExpiryYear() string`

GetExpiryYear returns the ExpiryYear field if non-nil, zero value otherwise.

### GetExpiryYearOk

`func (o *VaultPaymentMethod) GetExpiryYearOk() (*string, bool)`

GetExpiryYearOk returns a tuple with the ExpiryYear field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryYear

`func (o *VaultPaymentMethod) SetExpiryYear(v string)`

SetExpiryYear sets ExpiryYear field to given value.

### HasExpiryYear

`func (o *VaultPaymentMethod) HasExpiryYear() bool`

HasExpiryYear returns a boolean if a field has been set.

### SetExpiryYearNil

`func (o *VaultPaymentMethod) SetExpiryYearNil(b bool)`

 SetExpiryYearNil sets the value for ExpiryYear to be an explicit nil

### UnsetExpiryYear
`func (o *VaultPaymentMethod) UnsetExpiryYear()`

UnsetExpiryYear ensures that no value is present for ExpiryYear, not even an explicit nil
### GetExpiryMonth

`func (o *VaultPaymentMethod) GetExpiryMonth() string`

GetExpiryMonth returns the ExpiryMonth field if non-nil, zero value otherwise.

### GetExpiryMonthOk

`func (o *VaultPaymentMethod) GetExpiryMonthOk() (*string, bool)`

GetExpiryMonthOk returns a tuple with the ExpiryMonth field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryMonth

`func (o *VaultPaymentMethod) SetExpiryMonth(v string)`

SetExpiryMonth sets ExpiryMonth field to given value.

### HasExpiryMonth

`func (o *VaultPaymentMethod) HasExpiryMonth() bool`

HasExpiryMonth returns a boolean if a field has been set.

### SetExpiryMonthNil

`func (o *VaultPaymentMethod) SetExpiryMonthNil(b bool)`

 SetExpiryMonthNil sets the value for ExpiryMonth to be an explicit nil

### UnsetExpiryMonth
`func (o *VaultPaymentMethod) UnsetExpiryMonth()`

UnsetExpiryMonth ensures that no value is present for ExpiryMonth, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


