# PaymentMethodWriteResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Transaction** | Pointer to [**NullablePaymentMethodWriteResponseTransaction**](PaymentMethodWriteResponseTransaction.md) |  | [optional] 
**PaymentMethodId** | Pointer to **NullableString** | Unique identifier for the payment method | [optional] 
**CreditCardNumber** | Pointer to **NullableString** | Masked credit card number | [optional] 
**ExpiryMonth** | Pointer to **NullableString** | Expiration month | [optional] 
**ExpiryYear** | Pointer to **NullableString** | Expiration year | [optional] 
**Cvv** | Pointer to **NullableString** | Masked CVV | [optional] 
**FirstName** | Pointer to **NullableString** | Customer&#39;s first name | [optional] 
**LastName** | Pointer to **NullableString** | Customer&#39;s last name | [optional] 
**FullName** | Pointer to **NullableString** | Customer&#39;s full name | [optional] 
**CustomerId** | Pointer to **NullableString** | Customer identifier | [optional] 
**BillingAddress** | Pointer to [**NullableAddress**](Address.md) |  | [optional] 
**ShippingAddress** | Pointer to [**NullableAddress**](Address.md) |  | [optional] 
**Email** | Pointer to **NullableString** | Customer&#39;s email address | [optional] 
**PhoneNumber** | Pointer to **NullableString** | Customer&#39;s phone number | [optional] 
**PaymentMethodType** | Pointer to **NullableString** | Type of payment method | [optional] 
**Fingerprint** | Pointer to **NullableString** | Unique fingerprint for the payment method | [optional] 
**LastFourDigits** | Pointer to **NullableString** | Last four digits of the payment method | [optional] 
**FirstSixDigits** | Pointer to **NullableString** | First six digits (BIN) of the payment method | [optional] 
**CardType** | Pointer to **NullableString** | Type of credit card | [optional] 
**DateCreated** | Pointer to **NullableTime** | Date when the payment method was created | [optional] 
**StorageState** | Pointer to **NullableString** | Storage state of the payment method | [optional] 
**Bin** | Pointer to **NullableString** | Bank Identification Number. Must contain exactly 6 or 8 digits. | [optional] 

## Methods

### NewPaymentMethodWriteResponse

`func NewPaymentMethodWriteResponse() *PaymentMethodWriteResponse`

NewPaymentMethodWriteResponse instantiates a new PaymentMethodWriteResponse object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewPaymentMethodWriteResponseWithDefaults

`func NewPaymentMethodWriteResponseWithDefaults() *PaymentMethodWriteResponse`

NewPaymentMethodWriteResponseWithDefaults instantiates a new PaymentMethodWriteResponse object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransaction

`func (o *PaymentMethodWriteResponse) GetTransaction() PaymentMethodWriteResponseTransaction`

GetTransaction returns the Transaction field if non-nil, zero value otherwise.

### GetTransactionOk

`func (o *PaymentMethodWriteResponse) GetTransactionOk() (*PaymentMethodWriteResponseTransaction, bool)`

GetTransactionOk returns a tuple with the Transaction field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransaction

`func (o *PaymentMethodWriteResponse) SetTransaction(v PaymentMethodWriteResponseTransaction)`

SetTransaction sets Transaction field to given value.

### HasTransaction

`func (o *PaymentMethodWriteResponse) HasTransaction() bool`

HasTransaction returns a boolean if a field has been set.

### SetTransactionNil

`func (o *PaymentMethodWriteResponse) SetTransactionNil(b bool)`

 SetTransactionNil sets the value for Transaction to be an explicit nil

### UnsetTransaction
`func (o *PaymentMethodWriteResponse) UnsetTransaction()`

UnsetTransaction ensures that no value is present for Transaction, not even an explicit nil
### GetPaymentMethodId

`func (o *PaymentMethodWriteResponse) GetPaymentMethodId() string`

GetPaymentMethodId returns the PaymentMethodId field if non-nil, zero value otherwise.

### GetPaymentMethodIdOk

`func (o *PaymentMethodWriteResponse) GetPaymentMethodIdOk() (*string, bool)`

GetPaymentMethodIdOk returns a tuple with the PaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodId

`func (o *PaymentMethodWriteResponse) SetPaymentMethodId(v string)`

SetPaymentMethodId sets PaymentMethodId field to given value.

### HasPaymentMethodId

`func (o *PaymentMethodWriteResponse) HasPaymentMethodId() bool`

HasPaymentMethodId returns a boolean if a field has been set.

### SetPaymentMethodIdNil

`func (o *PaymentMethodWriteResponse) SetPaymentMethodIdNil(b bool)`

 SetPaymentMethodIdNil sets the value for PaymentMethodId to be an explicit nil

### UnsetPaymentMethodId
`func (o *PaymentMethodWriteResponse) UnsetPaymentMethodId()`

UnsetPaymentMethodId ensures that no value is present for PaymentMethodId, not even an explicit nil
### GetCreditCardNumber

`func (o *PaymentMethodWriteResponse) GetCreditCardNumber() string`

GetCreditCardNumber returns the CreditCardNumber field if non-nil, zero value otherwise.

### GetCreditCardNumberOk

`func (o *PaymentMethodWriteResponse) GetCreditCardNumberOk() (*string, bool)`

GetCreditCardNumberOk returns a tuple with the CreditCardNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCreditCardNumber

`func (o *PaymentMethodWriteResponse) SetCreditCardNumber(v string)`

SetCreditCardNumber sets CreditCardNumber field to given value.

### HasCreditCardNumber

`func (o *PaymentMethodWriteResponse) HasCreditCardNumber() bool`

HasCreditCardNumber returns a boolean if a field has been set.

### SetCreditCardNumberNil

`func (o *PaymentMethodWriteResponse) SetCreditCardNumberNil(b bool)`

 SetCreditCardNumberNil sets the value for CreditCardNumber to be an explicit nil

### UnsetCreditCardNumber
`func (o *PaymentMethodWriteResponse) UnsetCreditCardNumber()`

UnsetCreditCardNumber ensures that no value is present for CreditCardNumber, not even an explicit nil
### GetExpiryMonth

`func (o *PaymentMethodWriteResponse) GetExpiryMonth() string`

GetExpiryMonth returns the ExpiryMonth field if non-nil, zero value otherwise.

### GetExpiryMonthOk

`func (o *PaymentMethodWriteResponse) GetExpiryMonthOk() (*string, bool)`

GetExpiryMonthOk returns a tuple with the ExpiryMonth field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryMonth

`func (o *PaymentMethodWriteResponse) SetExpiryMonth(v string)`

SetExpiryMonth sets ExpiryMonth field to given value.

### HasExpiryMonth

`func (o *PaymentMethodWriteResponse) HasExpiryMonth() bool`

HasExpiryMonth returns a boolean if a field has been set.

### SetExpiryMonthNil

`func (o *PaymentMethodWriteResponse) SetExpiryMonthNil(b bool)`

 SetExpiryMonthNil sets the value for ExpiryMonth to be an explicit nil

### UnsetExpiryMonth
`func (o *PaymentMethodWriteResponse) UnsetExpiryMonth()`

UnsetExpiryMonth ensures that no value is present for ExpiryMonth, not even an explicit nil
### GetExpiryYear

`func (o *PaymentMethodWriteResponse) GetExpiryYear() string`

GetExpiryYear returns the ExpiryYear field if non-nil, zero value otherwise.

### GetExpiryYearOk

`func (o *PaymentMethodWriteResponse) GetExpiryYearOk() (*string, bool)`

GetExpiryYearOk returns a tuple with the ExpiryYear field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryYear

`func (o *PaymentMethodWriteResponse) SetExpiryYear(v string)`

SetExpiryYear sets ExpiryYear field to given value.

### HasExpiryYear

`func (o *PaymentMethodWriteResponse) HasExpiryYear() bool`

HasExpiryYear returns a boolean if a field has been set.

### SetExpiryYearNil

`func (o *PaymentMethodWriteResponse) SetExpiryYearNil(b bool)`

 SetExpiryYearNil sets the value for ExpiryYear to be an explicit nil

### UnsetExpiryYear
`func (o *PaymentMethodWriteResponse) UnsetExpiryYear()`

UnsetExpiryYear ensures that no value is present for ExpiryYear, not even an explicit nil
### GetCvv

`func (o *PaymentMethodWriteResponse) GetCvv() string`

GetCvv returns the Cvv field if non-nil, zero value otherwise.

### GetCvvOk

`func (o *PaymentMethodWriteResponse) GetCvvOk() (*string, bool)`

GetCvvOk returns a tuple with the Cvv field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCvv

`func (o *PaymentMethodWriteResponse) SetCvv(v string)`

SetCvv sets Cvv field to given value.

### HasCvv

`func (o *PaymentMethodWriteResponse) HasCvv() bool`

HasCvv returns a boolean if a field has been set.

### SetCvvNil

`func (o *PaymentMethodWriteResponse) SetCvvNil(b bool)`

 SetCvvNil sets the value for Cvv to be an explicit nil

### UnsetCvv
`func (o *PaymentMethodWriteResponse) UnsetCvv()`

UnsetCvv ensures that no value is present for Cvv, not even an explicit nil
### GetFirstName

`func (o *PaymentMethodWriteResponse) GetFirstName() string`

GetFirstName returns the FirstName field if non-nil, zero value otherwise.

### GetFirstNameOk

`func (o *PaymentMethodWriteResponse) GetFirstNameOk() (*string, bool)`

GetFirstNameOk returns a tuple with the FirstName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFirstName

`func (o *PaymentMethodWriteResponse) SetFirstName(v string)`

SetFirstName sets FirstName field to given value.

### HasFirstName

`func (o *PaymentMethodWriteResponse) HasFirstName() bool`

HasFirstName returns a boolean if a field has been set.

### SetFirstNameNil

`func (o *PaymentMethodWriteResponse) SetFirstNameNil(b bool)`

 SetFirstNameNil sets the value for FirstName to be an explicit nil

### UnsetFirstName
`func (o *PaymentMethodWriteResponse) UnsetFirstName()`

UnsetFirstName ensures that no value is present for FirstName, not even an explicit nil
### GetLastName

`func (o *PaymentMethodWriteResponse) GetLastName() string`

GetLastName returns the LastName field if non-nil, zero value otherwise.

### GetLastNameOk

`func (o *PaymentMethodWriteResponse) GetLastNameOk() (*string, bool)`

GetLastNameOk returns a tuple with the LastName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastName

`func (o *PaymentMethodWriteResponse) SetLastName(v string)`

SetLastName sets LastName field to given value.

### HasLastName

`func (o *PaymentMethodWriteResponse) HasLastName() bool`

HasLastName returns a boolean if a field has been set.

### SetLastNameNil

`func (o *PaymentMethodWriteResponse) SetLastNameNil(b bool)`

 SetLastNameNil sets the value for LastName to be an explicit nil

### UnsetLastName
`func (o *PaymentMethodWriteResponse) UnsetLastName()`

UnsetLastName ensures that no value is present for LastName, not even an explicit nil
### GetFullName

`func (o *PaymentMethodWriteResponse) GetFullName() string`

GetFullName returns the FullName field if non-nil, zero value otherwise.

### GetFullNameOk

`func (o *PaymentMethodWriteResponse) GetFullNameOk() (*string, bool)`

GetFullNameOk returns a tuple with the FullName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFullName

`func (o *PaymentMethodWriteResponse) SetFullName(v string)`

SetFullName sets FullName field to given value.

### HasFullName

`func (o *PaymentMethodWriteResponse) HasFullName() bool`

HasFullName returns a boolean if a field has been set.

### SetFullNameNil

`func (o *PaymentMethodWriteResponse) SetFullNameNil(b bool)`

 SetFullNameNil sets the value for FullName to be an explicit nil

### UnsetFullName
`func (o *PaymentMethodWriteResponse) UnsetFullName()`

UnsetFullName ensures that no value is present for FullName, not even an explicit nil
### GetCustomerId

`func (o *PaymentMethodWriteResponse) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *PaymentMethodWriteResponse) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *PaymentMethodWriteResponse) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *PaymentMethodWriteResponse) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *PaymentMethodWriteResponse) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *PaymentMethodWriteResponse) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetBillingAddress

`func (o *PaymentMethodWriteResponse) GetBillingAddress() Address`

GetBillingAddress returns the BillingAddress field if non-nil, zero value otherwise.

### GetBillingAddressOk

`func (o *PaymentMethodWriteResponse) GetBillingAddressOk() (*Address, bool)`

GetBillingAddressOk returns a tuple with the BillingAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBillingAddress

`func (o *PaymentMethodWriteResponse) SetBillingAddress(v Address)`

SetBillingAddress sets BillingAddress field to given value.

### HasBillingAddress

`func (o *PaymentMethodWriteResponse) HasBillingAddress() bool`

HasBillingAddress returns a boolean if a field has been set.

### SetBillingAddressNil

`func (o *PaymentMethodWriteResponse) SetBillingAddressNil(b bool)`

 SetBillingAddressNil sets the value for BillingAddress to be an explicit nil

### UnsetBillingAddress
`func (o *PaymentMethodWriteResponse) UnsetBillingAddress()`

UnsetBillingAddress ensures that no value is present for BillingAddress, not even an explicit nil
### GetShippingAddress

`func (o *PaymentMethodWriteResponse) GetShippingAddress() Address`

GetShippingAddress returns the ShippingAddress field if non-nil, zero value otherwise.

### GetShippingAddressOk

`func (o *PaymentMethodWriteResponse) GetShippingAddressOk() (*Address, bool)`

GetShippingAddressOk returns a tuple with the ShippingAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingAddress

`func (o *PaymentMethodWriteResponse) SetShippingAddress(v Address)`

SetShippingAddress sets ShippingAddress field to given value.

### HasShippingAddress

`func (o *PaymentMethodWriteResponse) HasShippingAddress() bool`

HasShippingAddress returns a boolean if a field has been set.

### SetShippingAddressNil

`func (o *PaymentMethodWriteResponse) SetShippingAddressNil(b bool)`

 SetShippingAddressNil sets the value for ShippingAddress to be an explicit nil

### UnsetShippingAddress
`func (o *PaymentMethodWriteResponse) UnsetShippingAddress()`

UnsetShippingAddress ensures that no value is present for ShippingAddress, not even an explicit nil
### GetEmail

`func (o *PaymentMethodWriteResponse) GetEmail() string`

GetEmail returns the Email field if non-nil, zero value otherwise.

### GetEmailOk

`func (o *PaymentMethodWriteResponse) GetEmailOk() (*string, bool)`

GetEmailOk returns a tuple with the Email field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEmail

`func (o *PaymentMethodWriteResponse) SetEmail(v string)`

SetEmail sets Email field to given value.

### HasEmail

`func (o *PaymentMethodWriteResponse) HasEmail() bool`

HasEmail returns a boolean if a field has been set.

### SetEmailNil

`func (o *PaymentMethodWriteResponse) SetEmailNil(b bool)`

 SetEmailNil sets the value for Email to be an explicit nil

### UnsetEmail
`func (o *PaymentMethodWriteResponse) UnsetEmail()`

UnsetEmail ensures that no value is present for Email, not even an explicit nil
### GetPhoneNumber

`func (o *PaymentMethodWriteResponse) GetPhoneNumber() string`

GetPhoneNumber returns the PhoneNumber field if non-nil, zero value otherwise.

### GetPhoneNumberOk

`func (o *PaymentMethodWriteResponse) GetPhoneNumberOk() (*string, bool)`

GetPhoneNumberOk returns a tuple with the PhoneNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPhoneNumber

`func (o *PaymentMethodWriteResponse) SetPhoneNumber(v string)`

SetPhoneNumber sets PhoneNumber field to given value.

### HasPhoneNumber

`func (o *PaymentMethodWriteResponse) HasPhoneNumber() bool`

HasPhoneNumber returns a boolean if a field has been set.

### SetPhoneNumberNil

`func (o *PaymentMethodWriteResponse) SetPhoneNumberNil(b bool)`

 SetPhoneNumberNil sets the value for PhoneNumber to be an explicit nil

### UnsetPhoneNumber
`func (o *PaymentMethodWriteResponse) UnsetPhoneNumber()`

UnsetPhoneNumber ensures that no value is present for PhoneNumber, not even an explicit nil
### GetPaymentMethodType

`func (o *PaymentMethodWriteResponse) GetPaymentMethodType() string`

GetPaymentMethodType returns the PaymentMethodType field if non-nil, zero value otherwise.

### GetPaymentMethodTypeOk

`func (o *PaymentMethodWriteResponse) GetPaymentMethodTypeOk() (*string, bool)`

GetPaymentMethodTypeOk returns a tuple with the PaymentMethodType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodType

`func (o *PaymentMethodWriteResponse) SetPaymentMethodType(v string)`

SetPaymentMethodType sets PaymentMethodType field to given value.

### HasPaymentMethodType

`func (o *PaymentMethodWriteResponse) HasPaymentMethodType() bool`

HasPaymentMethodType returns a boolean if a field has been set.

### SetPaymentMethodTypeNil

`func (o *PaymentMethodWriteResponse) SetPaymentMethodTypeNil(b bool)`

 SetPaymentMethodTypeNil sets the value for PaymentMethodType to be an explicit nil

### UnsetPaymentMethodType
`func (o *PaymentMethodWriteResponse) UnsetPaymentMethodType()`

UnsetPaymentMethodType ensures that no value is present for PaymentMethodType, not even an explicit nil
### GetFingerprint

`func (o *PaymentMethodWriteResponse) GetFingerprint() string`

GetFingerprint returns the Fingerprint field if non-nil, zero value otherwise.

### GetFingerprintOk

`func (o *PaymentMethodWriteResponse) GetFingerprintOk() (*string, bool)`

GetFingerprintOk returns a tuple with the Fingerprint field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFingerprint

`func (o *PaymentMethodWriteResponse) SetFingerprint(v string)`

SetFingerprint sets Fingerprint field to given value.

### HasFingerprint

`func (o *PaymentMethodWriteResponse) HasFingerprint() bool`

HasFingerprint returns a boolean if a field has been set.

### SetFingerprintNil

`func (o *PaymentMethodWriteResponse) SetFingerprintNil(b bool)`

 SetFingerprintNil sets the value for Fingerprint to be an explicit nil

### UnsetFingerprint
`func (o *PaymentMethodWriteResponse) UnsetFingerprint()`

UnsetFingerprint ensures that no value is present for Fingerprint, not even an explicit nil
### GetLastFourDigits

`func (o *PaymentMethodWriteResponse) GetLastFourDigits() string`

GetLastFourDigits returns the LastFourDigits field if non-nil, zero value otherwise.

### GetLastFourDigitsOk

`func (o *PaymentMethodWriteResponse) GetLastFourDigitsOk() (*string, bool)`

GetLastFourDigitsOk returns a tuple with the LastFourDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastFourDigits

`func (o *PaymentMethodWriteResponse) SetLastFourDigits(v string)`

SetLastFourDigits sets LastFourDigits field to given value.

### HasLastFourDigits

`func (o *PaymentMethodWriteResponse) HasLastFourDigits() bool`

HasLastFourDigits returns a boolean if a field has been set.

### SetLastFourDigitsNil

`func (o *PaymentMethodWriteResponse) SetLastFourDigitsNil(b bool)`

 SetLastFourDigitsNil sets the value for LastFourDigits to be an explicit nil

### UnsetLastFourDigits
`func (o *PaymentMethodWriteResponse) UnsetLastFourDigits()`

UnsetLastFourDigits ensures that no value is present for LastFourDigits, not even an explicit nil
### GetFirstSixDigits

`func (o *PaymentMethodWriteResponse) GetFirstSixDigits() string`

GetFirstSixDigits returns the FirstSixDigits field if non-nil, zero value otherwise.

### GetFirstSixDigitsOk

`func (o *PaymentMethodWriteResponse) GetFirstSixDigitsOk() (*string, bool)`

GetFirstSixDigitsOk returns a tuple with the FirstSixDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFirstSixDigits

`func (o *PaymentMethodWriteResponse) SetFirstSixDigits(v string)`

SetFirstSixDigits sets FirstSixDigits field to given value.

### HasFirstSixDigits

`func (o *PaymentMethodWriteResponse) HasFirstSixDigits() bool`

HasFirstSixDigits returns a boolean if a field has been set.

### SetFirstSixDigitsNil

`func (o *PaymentMethodWriteResponse) SetFirstSixDigitsNil(b bool)`

 SetFirstSixDigitsNil sets the value for FirstSixDigits to be an explicit nil

### UnsetFirstSixDigits
`func (o *PaymentMethodWriteResponse) UnsetFirstSixDigits()`

UnsetFirstSixDigits ensures that no value is present for FirstSixDigits, not even an explicit nil
### GetCardType

`func (o *PaymentMethodWriteResponse) GetCardType() string`

GetCardType returns the CardType field if non-nil, zero value otherwise.

### GetCardTypeOk

`func (o *PaymentMethodWriteResponse) GetCardTypeOk() (*string, bool)`

GetCardTypeOk returns a tuple with the CardType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCardType

`func (o *PaymentMethodWriteResponse) SetCardType(v string)`

SetCardType sets CardType field to given value.

### HasCardType

`func (o *PaymentMethodWriteResponse) HasCardType() bool`

HasCardType returns a boolean if a field has been set.

### SetCardTypeNil

`func (o *PaymentMethodWriteResponse) SetCardTypeNil(b bool)`

 SetCardTypeNil sets the value for CardType to be an explicit nil

### UnsetCardType
`func (o *PaymentMethodWriteResponse) UnsetCardType()`

UnsetCardType ensures that no value is present for CardType, not even an explicit nil
### GetDateCreated

`func (o *PaymentMethodWriteResponse) GetDateCreated() time.Time`

GetDateCreated returns the DateCreated field if non-nil, zero value otherwise.

### GetDateCreatedOk

`func (o *PaymentMethodWriteResponse) GetDateCreatedOk() (*time.Time, bool)`

GetDateCreatedOk returns a tuple with the DateCreated field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDateCreated

`func (o *PaymentMethodWriteResponse) SetDateCreated(v time.Time)`

SetDateCreated sets DateCreated field to given value.

### HasDateCreated

`func (o *PaymentMethodWriteResponse) HasDateCreated() bool`

HasDateCreated returns a boolean if a field has been set.

### SetDateCreatedNil

`func (o *PaymentMethodWriteResponse) SetDateCreatedNil(b bool)`

 SetDateCreatedNil sets the value for DateCreated to be an explicit nil

### UnsetDateCreated
`func (o *PaymentMethodWriteResponse) UnsetDateCreated()`

UnsetDateCreated ensures that no value is present for DateCreated, not even an explicit nil
### GetStorageState

`func (o *PaymentMethodWriteResponse) GetStorageState() string`

GetStorageState returns the StorageState field if non-nil, zero value otherwise.

### GetStorageStateOk

`func (o *PaymentMethodWriteResponse) GetStorageStateOk() (*string, bool)`

GetStorageStateOk returns a tuple with the StorageState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStorageState

`func (o *PaymentMethodWriteResponse) SetStorageState(v string)`

SetStorageState sets StorageState field to given value.

### HasStorageState

`func (o *PaymentMethodWriteResponse) HasStorageState() bool`

HasStorageState returns a boolean if a field has been set.

### SetStorageStateNil

`func (o *PaymentMethodWriteResponse) SetStorageStateNil(b bool)`

 SetStorageStateNil sets the value for StorageState to be an explicit nil

### UnsetStorageState
`func (o *PaymentMethodWriteResponse) UnsetStorageState()`

UnsetStorageState ensures that no value is present for StorageState, not even an explicit nil
### GetBin

`func (o *PaymentMethodWriteResponse) GetBin() string`

GetBin returns the Bin field if non-nil, zero value otherwise.

### GetBinOk

`func (o *PaymentMethodWriteResponse) GetBinOk() (*string, bool)`

GetBinOk returns a tuple with the Bin field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBin

`func (o *PaymentMethodWriteResponse) SetBin(v string)`

SetBin sets Bin field to given value.

### HasBin

`func (o *PaymentMethodWriteResponse) HasBin() bool`

HasBin returns a boolean if a field has been set.

### SetBinNil

`func (o *PaymentMethodWriteResponse) SetBinNil(b bool)`

 SetBinNil sets the value for Bin to be an explicit nil

### UnsetBin
`func (o *PaymentMethodWriteResponse) UnsetBin()`

UnsetBin ensures that no value is present for Bin, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


