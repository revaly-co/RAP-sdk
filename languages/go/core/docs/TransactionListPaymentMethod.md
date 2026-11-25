# TransactionListPaymentMethod

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PaymentMethodId** | Pointer to **string** | Payment method identifier | [optional] 
**CreditCardNumber** | Pointer to **string** | Masked card number; the full number is never returned | [optional] 
**ExpiryMonth** | Pointer to **string** | Card expiry month as stored | [optional] 
**ExpiryYear** | Pointer to **string** | Card expiry year as stored | [optional] 
**FirstName** | Pointer to **string** |  | [optional] 
**LastName** | Pointer to **string** |  | [optional] 
**FullName** | Pointer to **string** |  | [optional] 
**CustomerId** | Pointer to **string** | Customer identifier of the operation | [optional] 
**Address1** | Pointer to **string** | Billing address, first line | [optional] 
**Address2** | Pointer to **string** | Billing address, second line | [optional] 
**City** | Pointer to **string** | Billing address city | [optional] 
**State** | Pointer to **string** | Billing address state or region | [optional] 
**PostalCode** | Pointer to **string** | Billing address postal code | [optional] 
**Country** | Pointer to **string** | Billing address country | [optional] 
**Email** | Pointer to **string** |  | [optional] 
**PhoneNumber** | Pointer to **string** |  | [optional] 
**ShippingAddress1** | Pointer to **string** | Shipping address, first line | [optional] 
**ShippingAddress2** | Pointer to **string** | Shipping address, second line | [optional] 
**ShippingCity** | Pointer to **string** |  | [optional] 
**ShippingState** | Pointer to **string** |  | [optional] 
**ShippingPostalCode** | Pointer to **string** |  | [optional] 
**ShippingCountry** | Pointer to **string** |  | [optional] 
**PaymentMethodType** | Pointer to **string** | Type of the payment method | [optional] 
**LastFourDigits** | Pointer to **string** | Last four digits of the card number | [optional] 
**FirstSixDigits** | Pointer to **string** | First six digits of the card number | [optional] 
**CardType** | Pointer to **string** | Card brand as reported for the card (for example VISA) | [optional] 
**DateCreated** | Pointer to **string** | Date and time the payment method was created, as reported when the operation ran (ISO 8601). It may carry no UTC offset. | [optional] 
**StorageState** | Pointer to **string** | Storage state of the payment method | [optional] 
**IssuerIdentificationNumber** | Pointer to **string** | BIN of the card as reported when the operation ran | [optional] 
**MerchantAccountReferenceId** | Pointer to **string** | Merchant account reference identifier | [optional] 

## Methods

### NewTransactionListPaymentMethod

`func NewTransactionListPaymentMethod() *TransactionListPaymentMethod`

NewTransactionListPaymentMethod instantiates a new TransactionListPaymentMethod object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewTransactionListPaymentMethodWithDefaults

`func NewTransactionListPaymentMethodWithDefaults() *TransactionListPaymentMethod`

NewTransactionListPaymentMethodWithDefaults instantiates a new TransactionListPaymentMethod object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetPaymentMethodId

`func (o *TransactionListPaymentMethod) GetPaymentMethodId() string`

GetPaymentMethodId returns the PaymentMethodId field if non-nil, zero value otherwise.

### GetPaymentMethodIdOk

`func (o *TransactionListPaymentMethod) GetPaymentMethodIdOk() (*string, bool)`

GetPaymentMethodIdOk returns a tuple with the PaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodId

`func (o *TransactionListPaymentMethod) SetPaymentMethodId(v string)`

SetPaymentMethodId sets PaymentMethodId field to given value.

### HasPaymentMethodId

`func (o *TransactionListPaymentMethod) HasPaymentMethodId() bool`

HasPaymentMethodId returns a boolean if a field has been set.

### GetCreditCardNumber

`func (o *TransactionListPaymentMethod) GetCreditCardNumber() string`

GetCreditCardNumber returns the CreditCardNumber field if non-nil, zero value otherwise.

### GetCreditCardNumberOk

`func (o *TransactionListPaymentMethod) GetCreditCardNumberOk() (*string, bool)`

GetCreditCardNumberOk returns a tuple with the CreditCardNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCreditCardNumber

`func (o *TransactionListPaymentMethod) SetCreditCardNumber(v string)`

SetCreditCardNumber sets CreditCardNumber field to given value.

### HasCreditCardNumber

`func (o *TransactionListPaymentMethod) HasCreditCardNumber() bool`

HasCreditCardNumber returns a boolean if a field has been set.

### GetExpiryMonth

`func (o *TransactionListPaymentMethod) GetExpiryMonth() string`

GetExpiryMonth returns the ExpiryMonth field if non-nil, zero value otherwise.

### GetExpiryMonthOk

`func (o *TransactionListPaymentMethod) GetExpiryMonthOk() (*string, bool)`

GetExpiryMonthOk returns a tuple with the ExpiryMonth field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryMonth

`func (o *TransactionListPaymentMethod) SetExpiryMonth(v string)`

SetExpiryMonth sets ExpiryMonth field to given value.

### HasExpiryMonth

`func (o *TransactionListPaymentMethod) HasExpiryMonth() bool`

HasExpiryMonth returns a boolean if a field has been set.

### GetExpiryYear

`func (o *TransactionListPaymentMethod) GetExpiryYear() string`

GetExpiryYear returns the ExpiryYear field if non-nil, zero value otherwise.

### GetExpiryYearOk

`func (o *TransactionListPaymentMethod) GetExpiryYearOk() (*string, bool)`

GetExpiryYearOk returns a tuple with the ExpiryYear field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryYear

`func (o *TransactionListPaymentMethod) SetExpiryYear(v string)`

SetExpiryYear sets ExpiryYear field to given value.

### HasExpiryYear

`func (o *TransactionListPaymentMethod) HasExpiryYear() bool`

HasExpiryYear returns a boolean if a field has been set.

### GetFirstName

`func (o *TransactionListPaymentMethod) GetFirstName() string`

GetFirstName returns the FirstName field if non-nil, zero value otherwise.

### GetFirstNameOk

`func (o *TransactionListPaymentMethod) GetFirstNameOk() (*string, bool)`

GetFirstNameOk returns a tuple with the FirstName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFirstName

`func (o *TransactionListPaymentMethod) SetFirstName(v string)`

SetFirstName sets FirstName field to given value.

### HasFirstName

`func (o *TransactionListPaymentMethod) HasFirstName() bool`

HasFirstName returns a boolean if a field has been set.

### GetLastName

`func (o *TransactionListPaymentMethod) GetLastName() string`

GetLastName returns the LastName field if non-nil, zero value otherwise.

### GetLastNameOk

`func (o *TransactionListPaymentMethod) GetLastNameOk() (*string, bool)`

GetLastNameOk returns a tuple with the LastName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastName

`func (o *TransactionListPaymentMethod) SetLastName(v string)`

SetLastName sets LastName field to given value.

### HasLastName

`func (o *TransactionListPaymentMethod) HasLastName() bool`

HasLastName returns a boolean if a field has been set.

### GetFullName

`func (o *TransactionListPaymentMethod) GetFullName() string`

GetFullName returns the FullName field if non-nil, zero value otherwise.

### GetFullNameOk

`func (o *TransactionListPaymentMethod) GetFullNameOk() (*string, bool)`

GetFullNameOk returns a tuple with the FullName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFullName

`func (o *TransactionListPaymentMethod) SetFullName(v string)`

SetFullName sets FullName field to given value.

### HasFullName

`func (o *TransactionListPaymentMethod) HasFullName() bool`

HasFullName returns a boolean if a field has been set.

### GetCustomerId

`func (o *TransactionListPaymentMethod) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *TransactionListPaymentMethod) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *TransactionListPaymentMethod) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *TransactionListPaymentMethod) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### GetAddress1

`func (o *TransactionListPaymentMethod) GetAddress1() string`

GetAddress1 returns the Address1 field if non-nil, zero value otherwise.

### GetAddress1Ok

`func (o *TransactionListPaymentMethod) GetAddress1Ok() (*string, bool)`

GetAddress1Ok returns a tuple with the Address1 field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAddress1

`func (o *TransactionListPaymentMethod) SetAddress1(v string)`

SetAddress1 sets Address1 field to given value.

### HasAddress1

`func (o *TransactionListPaymentMethod) HasAddress1() bool`

HasAddress1 returns a boolean if a field has been set.

### GetAddress2

`func (o *TransactionListPaymentMethod) GetAddress2() string`

GetAddress2 returns the Address2 field if non-nil, zero value otherwise.

### GetAddress2Ok

`func (o *TransactionListPaymentMethod) GetAddress2Ok() (*string, bool)`

GetAddress2Ok returns a tuple with the Address2 field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAddress2

`func (o *TransactionListPaymentMethod) SetAddress2(v string)`

SetAddress2 sets Address2 field to given value.

### HasAddress2

`func (o *TransactionListPaymentMethod) HasAddress2() bool`

HasAddress2 returns a boolean if a field has been set.

### GetCity

`func (o *TransactionListPaymentMethod) GetCity() string`

GetCity returns the City field if non-nil, zero value otherwise.

### GetCityOk

`func (o *TransactionListPaymentMethod) GetCityOk() (*string, bool)`

GetCityOk returns a tuple with the City field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCity

`func (o *TransactionListPaymentMethod) SetCity(v string)`

SetCity sets City field to given value.

### HasCity

`func (o *TransactionListPaymentMethod) HasCity() bool`

HasCity returns a boolean if a field has been set.

### GetState

`func (o *TransactionListPaymentMethod) GetState() string`

GetState returns the State field if non-nil, zero value otherwise.

### GetStateOk

`func (o *TransactionListPaymentMethod) GetStateOk() (*string, bool)`

GetStateOk returns a tuple with the State field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetState

`func (o *TransactionListPaymentMethod) SetState(v string)`

SetState sets State field to given value.

### HasState

`func (o *TransactionListPaymentMethod) HasState() bool`

HasState returns a boolean if a field has been set.

### GetPostalCode

`func (o *TransactionListPaymentMethod) GetPostalCode() string`

GetPostalCode returns the PostalCode field if non-nil, zero value otherwise.

### GetPostalCodeOk

`func (o *TransactionListPaymentMethod) GetPostalCodeOk() (*string, bool)`

GetPostalCodeOk returns a tuple with the PostalCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPostalCode

`func (o *TransactionListPaymentMethod) SetPostalCode(v string)`

SetPostalCode sets PostalCode field to given value.

### HasPostalCode

`func (o *TransactionListPaymentMethod) HasPostalCode() bool`

HasPostalCode returns a boolean if a field has been set.

### GetCountry

`func (o *TransactionListPaymentMethod) GetCountry() string`

GetCountry returns the Country field if non-nil, zero value otherwise.

### GetCountryOk

`func (o *TransactionListPaymentMethod) GetCountryOk() (*string, bool)`

GetCountryOk returns a tuple with the Country field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCountry

`func (o *TransactionListPaymentMethod) SetCountry(v string)`

SetCountry sets Country field to given value.

### HasCountry

`func (o *TransactionListPaymentMethod) HasCountry() bool`

HasCountry returns a boolean if a field has been set.

### GetEmail

`func (o *TransactionListPaymentMethod) GetEmail() string`

GetEmail returns the Email field if non-nil, zero value otherwise.

### GetEmailOk

`func (o *TransactionListPaymentMethod) GetEmailOk() (*string, bool)`

GetEmailOk returns a tuple with the Email field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEmail

`func (o *TransactionListPaymentMethod) SetEmail(v string)`

SetEmail sets Email field to given value.

### HasEmail

`func (o *TransactionListPaymentMethod) HasEmail() bool`

HasEmail returns a boolean if a field has been set.

### GetPhoneNumber

`func (o *TransactionListPaymentMethod) GetPhoneNumber() string`

GetPhoneNumber returns the PhoneNumber field if non-nil, zero value otherwise.

### GetPhoneNumberOk

`func (o *TransactionListPaymentMethod) GetPhoneNumberOk() (*string, bool)`

GetPhoneNumberOk returns a tuple with the PhoneNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPhoneNumber

`func (o *TransactionListPaymentMethod) SetPhoneNumber(v string)`

SetPhoneNumber sets PhoneNumber field to given value.

### HasPhoneNumber

`func (o *TransactionListPaymentMethod) HasPhoneNumber() bool`

HasPhoneNumber returns a boolean if a field has been set.

### GetShippingAddress1

`func (o *TransactionListPaymentMethod) GetShippingAddress1() string`

GetShippingAddress1 returns the ShippingAddress1 field if non-nil, zero value otherwise.

### GetShippingAddress1Ok

`func (o *TransactionListPaymentMethod) GetShippingAddress1Ok() (*string, bool)`

GetShippingAddress1Ok returns a tuple with the ShippingAddress1 field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingAddress1

`func (o *TransactionListPaymentMethod) SetShippingAddress1(v string)`

SetShippingAddress1 sets ShippingAddress1 field to given value.

### HasShippingAddress1

`func (o *TransactionListPaymentMethod) HasShippingAddress1() bool`

HasShippingAddress1 returns a boolean if a field has been set.

### GetShippingAddress2

`func (o *TransactionListPaymentMethod) GetShippingAddress2() string`

GetShippingAddress2 returns the ShippingAddress2 field if non-nil, zero value otherwise.

### GetShippingAddress2Ok

`func (o *TransactionListPaymentMethod) GetShippingAddress2Ok() (*string, bool)`

GetShippingAddress2Ok returns a tuple with the ShippingAddress2 field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingAddress2

`func (o *TransactionListPaymentMethod) SetShippingAddress2(v string)`

SetShippingAddress2 sets ShippingAddress2 field to given value.

### HasShippingAddress2

`func (o *TransactionListPaymentMethod) HasShippingAddress2() bool`

HasShippingAddress2 returns a boolean if a field has been set.

### GetShippingCity

`func (o *TransactionListPaymentMethod) GetShippingCity() string`

GetShippingCity returns the ShippingCity field if non-nil, zero value otherwise.

### GetShippingCityOk

`func (o *TransactionListPaymentMethod) GetShippingCityOk() (*string, bool)`

GetShippingCityOk returns a tuple with the ShippingCity field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingCity

`func (o *TransactionListPaymentMethod) SetShippingCity(v string)`

SetShippingCity sets ShippingCity field to given value.

### HasShippingCity

`func (o *TransactionListPaymentMethod) HasShippingCity() bool`

HasShippingCity returns a boolean if a field has been set.

### GetShippingState

`func (o *TransactionListPaymentMethod) GetShippingState() string`

GetShippingState returns the ShippingState field if non-nil, zero value otherwise.

### GetShippingStateOk

`func (o *TransactionListPaymentMethod) GetShippingStateOk() (*string, bool)`

GetShippingStateOk returns a tuple with the ShippingState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingState

`func (o *TransactionListPaymentMethod) SetShippingState(v string)`

SetShippingState sets ShippingState field to given value.

### HasShippingState

`func (o *TransactionListPaymentMethod) HasShippingState() bool`

HasShippingState returns a boolean if a field has been set.

### GetShippingPostalCode

`func (o *TransactionListPaymentMethod) GetShippingPostalCode() string`

GetShippingPostalCode returns the ShippingPostalCode field if non-nil, zero value otherwise.

### GetShippingPostalCodeOk

`func (o *TransactionListPaymentMethod) GetShippingPostalCodeOk() (*string, bool)`

GetShippingPostalCodeOk returns a tuple with the ShippingPostalCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingPostalCode

`func (o *TransactionListPaymentMethod) SetShippingPostalCode(v string)`

SetShippingPostalCode sets ShippingPostalCode field to given value.

### HasShippingPostalCode

`func (o *TransactionListPaymentMethod) HasShippingPostalCode() bool`

HasShippingPostalCode returns a boolean if a field has been set.

### GetShippingCountry

`func (o *TransactionListPaymentMethod) GetShippingCountry() string`

GetShippingCountry returns the ShippingCountry field if non-nil, zero value otherwise.

### GetShippingCountryOk

`func (o *TransactionListPaymentMethod) GetShippingCountryOk() (*string, bool)`

GetShippingCountryOk returns a tuple with the ShippingCountry field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingCountry

`func (o *TransactionListPaymentMethod) SetShippingCountry(v string)`

SetShippingCountry sets ShippingCountry field to given value.

### HasShippingCountry

`func (o *TransactionListPaymentMethod) HasShippingCountry() bool`

HasShippingCountry returns a boolean if a field has been set.

### GetPaymentMethodType

`func (o *TransactionListPaymentMethod) GetPaymentMethodType() string`

GetPaymentMethodType returns the PaymentMethodType field if non-nil, zero value otherwise.

### GetPaymentMethodTypeOk

`func (o *TransactionListPaymentMethod) GetPaymentMethodTypeOk() (*string, bool)`

GetPaymentMethodTypeOk returns a tuple with the PaymentMethodType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodType

`func (o *TransactionListPaymentMethod) SetPaymentMethodType(v string)`

SetPaymentMethodType sets PaymentMethodType field to given value.

### HasPaymentMethodType

`func (o *TransactionListPaymentMethod) HasPaymentMethodType() bool`

HasPaymentMethodType returns a boolean if a field has been set.

### GetLastFourDigits

`func (o *TransactionListPaymentMethod) GetLastFourDigits() string`

GetLastFourDigits returns the LastFourDigits field if non-nil, zero value otherwise.

### GetLastFourDigitsOk

`func (o *TransactionListPaymentMethod) GetLastFourDigitsOk() (*string, bool)`

GetLastFourDigitsOk returns a tuple with the LastFourDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastFourDigits

`func (o *TransactionListPaymentMethod) SetLastFourDigits(v string)`

SetLastFourDigits sets LastFourDigits field to given value.

### HasLastFourDigits

`func (o *TransactionListPaymentMethod) HasLastFourDigits() bool`

HasLastFourDigits returns a boolean if a field has been set.

### GetFirstSixDigits

`func (o *TransactionListPaymentMethod) GetFirstSixDigits() string`

GetFirstSixDigits returns the FirstSixDigits field if non-nil, zero value otherwise.

### GetFirstSixDigitsOk

`func (o *TransactionListPaymentMethod) GetFirstSixDigitsOk() (*string, bool)`

GetFirstSixDigitsOk returns a tuple with the FirstSixDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFirstSixDigits

`func (o *TransactionListPaymentMethod) SetFirstSixDigits(v string)`

SetFirstSixDigits sets FirstSixDigits field to given value.

### HasFirstSixDigits

`func (o *TransactionListPaymentMethod) HasFirstSixDigits() bool`

HasFirstSixDigits returns a boolean if a field has been set.

### GetCardType

`func (o *TransactionListPaymentMethod) GetCardType() string`

GetCardType returns the CardType field if non-nil, zero value otherwise.

### GetCardTypeOk

`func (o *TransactionListPaymentMethod) GetCardTypeOk() (*string, bool)`

GetCardTypeOk returns a tuple with the CardType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCardType

`func (o *TransactionListPaymentMethod) SetCardType(v string)`

SetCardType sets CardType field to given value.

### HasCardType

`func (o *TransactionListPaymentMethod) HasCardType() bool`

HasCardType returns a boolean if a field has been set.

### GetDateCreated

`func (o *TransactionListPaymentMethod) GetDateCreated() string`

GetDateCreated returns the DateCreated field if non-nil, zero value otherwise.

### GetDateCreatedOk

`func (o *TransactionListPaymentMethod) GetDateCreatedOk() (*string, bool)`

GetDateCreatedOk returns a tuple with the DateCreated field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDateCreated

`func (o *TransactionListPaymentMethod) SetDateCreated(v string)`

SetDateCreated sets DateCreated field to given value.

### HasDateCreated

`func (o *TransactionListPaymentMethod) HasDateCreated() bool`

HasDateCreated returns a boolean if a field has been set.

### GetStorageState

`func (o *TransactionListPaymentMethod) GetStorageState() string`

GetStorageState returns the StorageState field if non-nil, zero value otherwise.

### GetStorageStateOk

`func (o *TransactionListPaymentMethod) GetStorageStateOk() (*string, bool)`

GetStorageStateOk returns a tuple with the StorageState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStorageState

`func (o *TransactionListPaymentMethod) SetStorageState(v string)`

SetStorageState sets StorageState field to given value.

### HasStorageState

`func (o *TransactionListPaymentMethod) HasStorageState() bool`

HasStorageState returns a boolean if a field has been set.

### GetIssuerIdentificationNumber

`func (o *TransactionListPaymentMethod) GetIssuerIdentificationNumber() string`

GetIssuerIdentificationNumber returns the IssuerIdentificationNumber field if non-nil, zero value otherwise.

### GetIssuerIdentificationNumberOk

`func (o *TransactionListPaymentMethod) GetIssuerIdentificationNumberOk() (*string, bool)`

GetIssuerIdentificationNumberOk returns a tuple with the IssuerIdentificationNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIssuerIdentificationNumber

`func (o *TransactionListPaymentMethod) SetIssuerIdentificationNumber(v string)`

SetIssuerIdentificationNumber sets IssuerIdentificationNumber field to given value.

### HasIssuerIdentificationNumber

`func (o *TransactionListPaymentMethod) HasIssuerIdentificationNumber() bool`

HasIssuerIdentificationNumber returns a boolean if a field has been set.

### GetMerchantAccountReferenceId

`func (o *TransactionListPaymentMethod) GetMerchantAccountReferenceId() string`

GetMerchantAccountReferenceId returns the MerchantAccountReferenceId field if non-nil, zero value otherwise.

### GetMerchantAccountReferenceIdOk

`func (o *TransactionListPaymentMethod) GetMerchantAccountReferenceIdOk() (*string, bool)`

GetMerchantAccountReferenceIdOk returns a tuple with the MerchantAccountReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantAccountReferenceId

`func (o *TransactionListPaymentMethod) SetMerchantAccountReferenceId(v string)`

SetMerchantAccountReferenceId sets MerchantAccountReferenceId field to given value.

### HasMerchantAccountReferenceId

`func (o *TransactionListPaymentMethod) HasMerchantAccountReferenceId() bool`

HasMerchantAccountReferenceId returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


