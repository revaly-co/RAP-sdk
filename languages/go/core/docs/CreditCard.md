# CreditCard

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Number** | **string** | Credit card number (will be tokenized) | 
**CardVerificationCode** | Pointer to **NullableString** | Card verification code (CVV/CVC) | [optional] 
**ExpiryMonth** | **string** | Expiration month (01-12) | 
**ExpiryYear** | **string** | Expiration year (YYYY) | 
**Company** | Pointer to **NullableString** | Card issuing company | [optional] 
**CardType** | Pointer to **NullableString** | Type of credit card | [optional] 

## Methods

### NewCreditCard

`func NewCreditCard(number string, expiryMonth string, expiryYear string, ) *CreditCard`

NewCreditCard instantiates a new CreditCard object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewCreditCardWithDefaults

`func NewCreditCardWithDefaults() *CreditCard`

NewCreditCardWithDefaults instantiates a new CreditCard object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetNumber

`func (o *CreditCard) GetNumber() string`

GetNumber returns the Number field if non-nil, zero value otherwise.

### GetNumberOk

`func (o *CreditCard) GetNumberOk() (*string, bool)`

GetNumberOk returns a tuple with the Number field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetNumber

`func (o *CreditCard) SetNumber(v string)`

SetNumber sets Number field to given value.


### GetCardVerificationCode

`func (o *CreditCard) GetCardVerificationCode() string`

GetCardVerificationCode returns the CardVerificationCode field if non-nil, zero value otherwise.

### GetCardVerificationCodeOk

`func (o *CreditCard) GetCardVerificationCodeOk() (*string, bool)`

GetCardVerificationCodeOk returns a tuple with the CardVerificationCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCardVerificationCode

`func (o *CreditCard) SetCardVerificationCode(v string)`

SetCardVerificationCode sets CardVerificationCode field to given value.

### HasCardVerificationCode

`func (o *CreditCard) HasCardVerificationCode() bool`

HasCardVerificationCode returns a boolean if a field has been set.

### SetCardVerificationCodeNil

`func (o *CreditCard) SetCardVerificationCodeNil(b bool)`

 SetCardVerificationCodeNil sets the value for CardVerificationCode to be an explicit nil

### UnsetCardVerificationCode
`func (o *CreditCard) UnsetCardVerificationCode()`

UnsetCardVerificationCode ensures that no value is present for CardVerificationCode, not even an explicit nil
### GetExpiryMonth

`func (o *CreditCard) GetExpiryMonth() string`

GetExpiryMonth returns the ExpiryMonth field if non-nil, zero value otherwise.

### GetExpiryMonthOk

`func (o *CreditCard) GetExpiryMonthOk() (*string, bool)`

GetExpiryMonthOk returns a tuple with the ExpiryMonth field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryMonth

`func (o *CreditCard) SetExpiryMonth(v string)`

SetExpiryMonth sets ExpiryMonth field to given value.


### GetExpiryYear

`func (o *CreditCard) GetExpiryYear() string`

GetExpiryYear returns the ExpiryYear field if non-nil, zero value otherwise.

### GetExpiryYearOk

`func (o *CreditCard) GetExpiryYearOk() (*string, bool)`

GetExpiryYearOk returns a tuple with the ExpiryYear field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryYear

`func (o *CreditCard) SetExpiryYear(v string)`

SetExpiryYear sets ExpiryYear field to given value.


### GetCompany

`func (o *CreditCard) GetCompany() string`

GetCompany returns the Company field if non-nil, zero value otherwise.

### GetCompanyOk

`func (o *CreditCard) GetCompanyOk() (*string, bool)`

GetCompanyOk returns a tuple with the Company field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCompany

`func (o *CreditCard) SetCompany(v string)`

SetCompany sets Company field to given value.

### HasCompany

`func (o *CreditCard) HasCompany() bool`

HasCompany returns a boolean if a field has been set.

### SetCompanyNil

`func (o *CreditCard) SetCompanyNil(b bool)`

 SetCompanyNil sets the value for Company to be an explicit nil

### UnsetCompany
`func (o *CreditCard) UnsetCompany()`

UnsetCompany ensures that no value is present for Company, not even an explicit nil
### GetCardType

`func (o *CreditCard) GetCardType() string`

GetCardType returns the CardType field if non-nil, zero value otherwise.

### GetCardTypeOk

`func (o *CreditCard) GetCardTypeOk() (*string, bool)`

GetCardTypeOk returns a tuple with the CardType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCardType

`func (o *CreditCard) SetCardType(v string)`

SetCardType sets CardType field to given value.

### HasCardType

`func (o *CreditCard) HasCardType() bool`

HasCardType returns a boolean if a field has been set.

### SetCardTypeNil

`func (o *CreditCard) SetCardTypeNil(b bool)`

 SetCardTypeNil sets the value for CardType to be an explicit nil

### UnsetCardType
`func (o *CreditCard) UnsetCardType()`

UnsetCardType ensures that no value is present for CardType, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


