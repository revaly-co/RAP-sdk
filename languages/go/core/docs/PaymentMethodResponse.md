# PaymentMethodResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PaymentMethodId** | Pointer to **NullableString** | Unique identifier for the payment method | [optional] 
**CreditCardNumber** | Pointer to **NullableString** | Masked credit card number | [optional] 
**ExpiryMonth** | Pointer to **NullableString** | Credit card expiry month | [optional] 
**ExpiryYear** | Pointer to **NullableString** | Credit card expiry year | [optional] 
**Cvv** | Pointer to **NullableString** | Masked card verification value | [optional] 
**FirstName** | Pointer to **NullableString** | Cardholder&#39;s first name | [optional] 
**LastName** | Pointer to **NullableString** | Cardholder&#39;s last name | [optional] 
**FullName** | Pointer to **NullableString** | Cardholder&#39;s full name | [optional] 
**CustomerId** | Pointer to **NullableString** | Customer identifier | [optional] 
**BillingAddress** | Pointer to [**Address**](Address.md) |  | [optional] 
**ShippingAddress** | Pointer to [**Address**](Address.md) |  | [optional] 
**Email** | Pointer to **NullableString** | Customer&#39;s email address | [optional] 
**PhoneNumber** | Pointer to **NullableString** | Customer&#39;s phone number | [optional] 
**PaymentMethodType** | Pointer to **NullableString** | Type of payment method | [optional] 
**Fingerprint** | Pointer to **NullableString** | Unique fingerprint for the payment method | [optional] 
**LastFourDigits** | Pointer to **NullableString** | Last four digits of the payment method | [optional] 
**FirstSixDigits** | Pointer to **NullableString** | First six digits of the payment method (BIN) | [optional] 
**CardType** | Pointer to **NullableString** | Type of credit card | [optional] 
**DateCreated** | Pointer to **NullableTime** | Date when the payment method was created | [optional] 
**StorageState** | Pointer to **NullableString** | Storage state of the payment method | [optional] 
**Bin** | Pointer to **NullableString** | Bank Identification Number. Must contain exactly 6 or 8 digits. | [optional] 
**VaultToken** | Pointer to **NullableString** | Opaque reference to the stored card this payment method used, returned so a transaction can be tied back to its credential without a second lookup.  Present on the payment method nested inside a **charge or authorize** response, and on the **single-transaction reads** (&#x60;GET /transactions/{transactionId}&#x60; and &#x60;GET /transactions/merchant/{merchantTransactionId}&#x60;), whenever that transaction ran against a vault credential — either one you presented, or one this API created for you when it vaulted the card you sent. The paged list reports it too, but **flat on the row** rather than nested here. The transaction-group reads (&#x60;?includeAllTransactions&#x3D;true&#x60;) report it on every transaction in the group. Follow-up responses (capture, void, refund, refund-cancel) carry no payment method today, so they report no token. Always omitted on the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list): a stored payment method cannot be created from a vault token, so it never has one to report.  Reads are a snapshot of the value recorded at processing time and do not re-resolve the credential. Where the token can be resolved live, this is the token **currently live** for the credential, which is not always the token submitted — if the card was replaced by the Account Updater, the value is the new head of the lineage. Otherwise it is the token the transaction was dispatched with, and does not reflect a roll. Which of the two you get depends on how the transaction was processed, so treat it as optional throughout and do **not** treat a missing or unchanged value as proof the card was not rolled. Recording began with API version **2.6.0**: transactions processed earlier report no token at all and cannot be backfilled. This is the only place the token is reported — there is deliberately no copy at the transaction level. | [optional] 

## Methods

### NewPaymentMethodResponse

`func NewPaymentMethodResponse() *PaymentMethodResponse`

NewPaymentMethodResponse instantiates a new PaymentMethodResponse object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewPaymentMethodResponseWithDefaults

`func NewPaymentMethodResponseWithDefaults() *PaymentMethodResponse`

NewPaymentMethodResponseWithDefaults instantiates a new PaymentMethodResponse object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetPaymentMethodId

`func (o *PaymentMethodResponse) GetPaymentMethodId() string`

GetPaymentMethodId returns the PaymentMethodId field if non-nil, zero value otherwise.

### GetPaymentMethodIdOk

`func (o *PaymentMethodResponse) GetPaymentMethodIdOk() (*string, bool)`

GetPaymentMethodIdOk returns a tuple with the PaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodId

`func (o *PaymentMethodResponse) SetPaymentMethodId(v string)`

SetPaymentMethodId sets PaymentMethodId field to given value.

### HasPaymentMethodId

`func (o *PaymentMethodResponse) HasPaymentMethodId() bool`

HasPaymentMethodId returns a boolean if a field has been set.

### SetPaymentMethodIdNil

`func (o *PaymentMethodResponse) SetPaymentMethodIdNil(b bool)`

 SetPaymentMethodIdNil sets the value for PaymentMethodId to be an explicit nil

### UnsetPaymentMethodId
`func (o *PaymentMethodResponse) UnsetPaymentMethodId()`

UnsetPaymentMethodId ensures that no value is present for PaymentMethodId, not even an explicit nil
### GetCreditCardNumber

`func (o *PaymentMethodResponse) GetCreditCardNumber() string`

GetCreditCardNumber returns the CreditCardNumber field if non-nil, zero value otherwise.

### GetCreditCardNumberOk

`func (o *PaymentMethodResponse) GetCreditCardNumberOk() (*string, bool)`

GetCreditCardNumberOk returns a tuple with the CreditCardNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCreditCardNumber

`func (o *PaymentMethodResponse) SetCreditCardNumber(v string)`

SetCreditCardNumber sets CreditCardNumber field to given value.

### HasCreditCardNumber

`func (o *PaymentMethodResponse) HasCreditCardNumber() bool`

HasCreditCardNumber returns a boolean if a field has been set.

### SetCreditCardNumberNil

`func (o *PaymentMethodResponse) SetCreditCardNumberNil(b bool)`

 SetCreditCardNumberNil sets the value for CreditCardNumber to be an explicit nil

### UnsetCreditCardNumber
`func (o *PaymentMethodResponse) UnsetCreditCardNumber()`

UnsetCreditCardNumber ensures that no value is present for CreditCardNumber, not even an explicit nil
### GetExpiryMonth

`func (o *PaymentMethodResponse) GetExpiryMonth() string`

GetExpiryMonth returns the ExpiryMonth field if non-nil, zero value otherwise.

### GetExpiryMonthOk

`func (o *PaymentMethodResponse) GetExpiryMonthOk() (*string, bool)`

GetExpiryMonthOk returns a tuple with the ExpiryMonth field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryMonth

`func (o *PaymentMethodResponse) SetExpiryMonth(v string)`

SetExpiryMonth sets ExpiryMonth field to given value.

### HasExpiryMonth

`func (o *PaymentMethodResponse) HasExpiryMonth() bool`

HasExpiryMonth returns a boolean if a field has been set.

### SetExpiryMonthNil

`func (o *PaymentMethodResponse) SetExpiryMonthNil(b bool)`

 SetExpiryMonthNil sets the value for ExpiryMonth to be an explicit nil

### UnsetExpiryMonth
`func (o *PaymentMethodResponse) UnsetExpiryMonth()`

UnsetExpiryMonth ensures that no value is present for ExpiryMonth, not even an explicit nil
### GetExpiryYear

`func (o *PaymentMethodResponse) GetExpiryYear() string`

GetExpiryYear returns the ExpiryYear field if non-nil, zero value otherwise.

### GetExpiryYearOk

`func (o *PaymentMethodResponse) GetExpiryYearOk() (*string, bool)`

GetExpiryYearOk returns a tuple with the ExpiryYear field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExpiryYear

`func (o *PaymentMethodResponse) SetExpiryYear(v string)`

SetExpiryYear sets ExpiryYear field to given value.

### HasExpiryYear

`func (o *PaymentMethodResponse) HasExpiryYear() bool`

HasExpiryYear returns a boolean if a field has been set.

### SetExpiryYearNil

`func (o *PaymentMethodResponse) SetExpiryYearNil(b bool)`

 SetExpiryYearNil sets the value for ExpiryYear to be an explicit nil

### UnsetExpiryYear
`func (o *PaymentMethodResponse) UnsetExpiryYear()`

UnsetExpiryYear ensures that no value is present for ExpiryYear, not even an explicit nil
### GetCvv

`func (o *PaymentMethodResponse) GetCvv() string`

GetCvv returns the Cvv field if non-nil, zero value otherwise.

### GetCvvOk

`func (o *PaymentMethodResponse) GetCvvOk() (*string, bool)`

GetCvvOk returns a tuple with the Cvv field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCvv

`func (o *PaymentMethodResponse) SetCvv(v string)`

SetCvv sets Cvv field to given value.

### HasCvv

`func (o *PaymentMethodResponse) HasCvv() bool`

HasCvv returns a boolean if a field has been set.

### SetCvvNil

`func (o *PaymentMethodResponse) SetCvvNil(b bool)`

 SetCvvNil sets the value for Cvv to be an explicit nil

### UnsetCvv
`func (o *PaymentMethodResponse) UnsetCvv()`

UnsetCvv ensures that no value is present for Cvv, not even an explicit nil
### GetFirstName

`func (o *PaymentMethodResponse) GetFirstName() string`

GetFirstName returns the FirstName field if non-nil, zero value otherwise.

### GetFirstNameOk

`func (o *PaymentMethodResponse) GetFirstNameOk() (*string, bool)`

GetFirstNameOk returns a tuple with the FirstName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFirstName

`func (o *PaymentMethodResponse) SetFirstName(v string)`

SetFirstName sets FirstName field to given value.

### HasFirstName

`func (o *PaymentMethodResponse) HasFirstName() bool`

HasFirstName returns a boolean if a field has been set.

### SetFirstNameNil

`func (o *PaymentMethodResponse) SetFirstNameNil(b bool)`

 SetFirstNameNil sets the value for FirstName to be an explicit nil

### UnsetFirstName
`func (o *PaymentMethodResponse) UnsetFirstName()`

UnsetFirstName ensures that no value is present for FirstName, not even an explicit nil
### GetLastName

`func (o *PaymentMethodResponse) GetLastName() string`

GetLastName returns the LastName field if non-nil, zero value otherwise.

### GetLastNameOk

`func (o *PaymentMethodResponse) GetLastNameOk() (*string, bool)`

GetLastNameOk returns a tuple with the LastName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastName

`func (o *PaymentMethodResponse) SetLastName(v string)`

SetLastName sets LastName field to given value.

### HasLastName

`func (o *PaymentMethodResponse) HasLastName() bool`

HasLastName returns a boolean if a field has been set.

### SetLastNameNil

`func (o *PaymentMethodResponse) SetLastNameNil(b bool)`

 SetLastNameNil sets the value for LastName to be an explicit nil

### UnsetLastName
`func (o *PaymentMethodResponse) UnsetLastName()`

UnsetLastName ensures that no value is present for LastName, not even an explicit nil
### GetFullName

`func (o *PaymentMethodResponse) GetFullName() string`

GetFullName returns the FullName field if non-nil, zero value otherwise.

### GetFullNameOk

`func (o *PaymentMethodResponse) GetFullNameOk() (*string, bool)`

GetFullNameOk returns a tuple with the FullName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFullName

`func (o *PaymentMethodResponse) SetFullName(v string)`

SetFullName sets FullName field to given value.

### HasFullName

`func (o *PaymentMethodResponse) HasFullName() bool`

HasFullName returns a boolean if a field has been set.

### SetFullNameNil

`func (o *PaymentMethodResponse) SetFullNameNil(b bool)`

 SetFullNameNil sets the value for FullName to be an explicit nil

### UnsetFullName
`func (o *PaymentMethodResponse) UnsetFullName()`

UnsetFullName ensures that no value is present for FullName, not even an explicit nil
### GetCustomerId

`func (o *PaymentMethodResponse) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *PaymentMethodResponse) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *PaymentMethodResponse) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *PaymentMethodResponse) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *PaymentMethodResponse) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *PaymentMethodResponse) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetBillingAddress

`func (o *PaymentMethodResponse) GetBillingAddress() Address`

GetBillingAddress returns the BillingAddress field if non-nil, zero value otherwise.

### GetBillingAddressOk

`func (o *PaymentMethodResponse) GetBillingAddressOk() (*Address, bool)`

GetBillingAddressOk returns a tuple with the BillingAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBillingAddress

`func (o *PaymentMethodResponse) SetBillingAddress(v Address)`

SetBillingAddress sets BillingAddress field to given value.

### HasBillingAddress

`func (o *PaymentMethodResponse) HasBillingAddress() bool`

HasBillingAddress returns a boolean if a field has been set.

### GetShippingAddress

`func (o *PaymentMethodResponse) GetShippingAddress() Address`

GetShippingAddress returns the ShippingAddress field if non-nil, zero value otherwise.

### GetShippingAddressOk

`func (o *PaymentMethodResponse) GetShippingAddressOk() (*Address, bool)`

GetShippingAddressOk returns a tuple with the ShippingAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingAddress

`func (o *PaymentMethodResponse) SetShippingAddress(v Address)`

SetShippingAddress sets ShippingAddress field to given value.

### HasShippingAddress

`func (o *PaymentMethodResponse) HasShippingAddress() bool`

HasShippingAddress returns a boolean if a field has been set.

### GetEmail

`func (o *PaymentMethodResponse) GetEmail() string`

GetEmail returns the Email field if non-nil, zero value otherwise.

### GetEmailOk

`func (o *PaymentMethodResponse) GetEmailOk() (*string, bool)`

GetEmailOk returns a tuple with the Email field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEmail

`func (o *PaymentMethodResponse) SetEmail(v string)`

SetEmail sets Email field to given value.

### HasEmail

`func (o *PaymentMethodResponse) HasEmail() bool`

HasEmail returns a boolean if a field has been set.

### SetEmailNil

`func (o *PaymentMethodResponse) SetEmailNil(b bool)`

 SetEmailNil sets the value for Email to be an explicit nil

### UnsetEmail
`func (o *PaymentMethodResponse) UnsetEmail()`

UnsetEmail ensures that no value is present for Email, not even an explicit nil
### GetPhoneNumber

`func (o *PaymentMethodResponse) GetPhoneNumber() string`

GetPhoneNumber returns the PhoneNumber field if non-nil, zero value otherwise.

### GetPhoneNumberOk

`func (o *PaymentMethodResponse) GetPhoneNumberOk() (*string, bool)`

GetPhoneNumberOk returns a tuple with the PhoneNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPhoneNumber

`func (o *PaymentMethodResponse) SetPhoneNumber(v string)`

SetPhoneNumber sets PhoneNumber field to given value.

### HasPhoneNumber

`func (o *PaymentMethodResponse) HasPhoneNumber() bool`

HasPhoneNumber returns a boolean if a field has been set.

### SetPhoneNumberNil

`func (o *PaymentMethodResponse) SetPhoneNumberNil(b bool)`

 SetPhoneNumberNil sets the value for PhoneNumber to be an explicit nil

### UnsetPhoneNumber
`func (o *PaymentMethodResponse) UnsetPhoneNumber()`

UnsetPhoneNumber ensures that no value is present for PhoneNumber, not even an explicit nil
### GetPaymentMethodType

`func (o *PaymentMethodResponse) GetPaymentMethodType() string`

GetPaymentMethodType returns the PaymentMethodType field if non-nil, zero value otherwise.

### GetPaymentMethodTypeOk

`func (o *PaymentMethodResponse) GetPaymentMethodTypeOk() (*string, bool)`

GetPaymentMethodTypeOk returns a tuple with the PaymentMethodType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodType

`func (o *PaymentMethodResponse) SetPaymentMethodType(v string)`

SetPaymentMethodType sets PaymentMethodType field to given value.

### HasPaymentMethodType

`func (o *PaymentMethodResponse) HasPaymentMethodType() bool`

HasPaymentMethodType returns a boolean if a field has been set.

### SetPaymentMethodTypeNil

`func (o *PaymentMethodResponse) SetPaymentMethodTypeNil(b bool)`

 SetPaymentMethodTypeNil sets the value for PaymentMethodType to be an explicit nil

### UnsetPaymentMethodType
`func (o *PaymentMethodResponse) UnsetPaymentMethodType()`

UnsetPaymentMethodType ensures that no value is present for PaymentMethodType, not even an explicit nil
### GetFingerprint

`func (o *PaymentMethodResponse) GetFingerprint() string`

GetFingerprint returns the Fingerprint field if non-nil, zero value otherwise.

### GetFingerprintOk

`func (o *PaymentMethodResponse) GetFingerprintOk() (*string, bool)`

GetFingerprintOk returns a tuple with the Fingerprint field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFingerprint

`func (o *PaymentMethodResponse) SetFingerprint(v string)`

SetFingerprint sets Fingerprint field to given value.

### HasFingerprint

`func (o *PaymentMethodResponse) HasFingerprint() bool`

HasFingerprint returns a boolean if a field has been set.

### SetFingerprintNil

`func (o *PaymentMethodResponse) SetFingerprintNil(b bool)`

 SetFingerprintNil sets the value for Fingerprint to be an explicit nil

### UnsetFingerprint
`func (o *PaymentMethodResponse) UnsetFingerprint()`

UnsetFingerprint ensures that no value is present for Fingerprint, not even an explicit nil
### GetLastFourDigits

`func (o *PaymentMethodResponse) GetLastFourDigits() string`

GetLastFourDigits returns the LastFourDigits field if non-nil, zero value otherwise.

### GetLastFourDigitsOk

`func (o *PaymentMethodResponse) GetLastFourDigitsOk() (*string, bool)`

GetLastFourDigitsOk returns a tuple with the LastFourDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastFourDigits

`func (o *PaymentMethodResponse) SetLastFourDigits(v string)`

SetLastFourDigits sets LastFourDigits field to given value.

### HasLastFourDigits

`func (o *PaymentMethodResponse) HasLastFourDigits() bool`

HasLastFourDigits returns a boolean if a field has been set.

### SetLastFourDigitsNil

`func (o *PaymentMethodResponse) SetLastFourDigitsNil(b bool)`

 SetLastFourDigitsNil sets the value for LastFourDigits to be an explicit nil

### UnsetLastFourDigits
`func (o *PaymentMethodResponse) UnsetLastFourDigits()`

UnsetLastFourDigits ensures that no value is present for LastFourDigits, not even an explicit nil
### GetFirstSixDigits

`func (o *PaymentMethodResponse) GetFirstSixDigits() string`

GetFirstSixDigits returns the FirstSixDigits field if non-nil, zero value otherwise.

### GetFirstSixDigitsOk

`func (o *PaymentMethodResponse) GetFirstSixDigitsOk() (*string, bool)`

GetFirstSixDigitsOk returns a tuple with the FirstSixDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFirstSixDigits

`func (o *PaymentMethodResponse) SetFirstSixDigits(v string)`

SetFirstSixDigits sets FirstSixDigits field to given value.

### HasFirstSixDigits

`func (o *PaymentMethodResponse) HasFirstSixDigits() bool`

HasFirstSixDigits returns a boolean if a field has been set.

### SetFirstSixDigitsNil

`func (o *PaymentMethodResponse) SetFirstSixDigitsNil(b bool)`

 SetFirstSixDigitsNil sets the value for FirstSixDigits to be an explicit nil

### UnsetFirstSixDigits
`func (o *PaymentMethodResponse) UnsetFirstSixDigits()`

UnsetFirstSixDigits ensures that no value is present for FirstSixDigits, not even an explicit nil
### GetCardType

`func (o *PaymentMethodResponse) GetCardType() string`

GetCardType returns the CardType field if non-nil, zero value otherwise.

### GetCardTypeOk

`func (o *PaymentMethodResponse) GetCardTypeOk() (*string, bool)`

GetCardTypeOk returns a tuple with the CardType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCardType

`func (o *PaymentMethodResponse) SetCardType(v string)`

SetCardType sets CardType field to given value.

### HasCardType

`func (o *PaymentMethodResponse) HasCardType() bool`

HasCardType returns a boolean if a field has been set.

### SetCardTypeNil

`func (o *PaymentMethodResponse) SetCardTypeNil(b bool)`

 SetCardTypeNil sets the value for CardType to be an explicit nil

### UnsetCardType
`func (o *PaymentMethodResponse) UnsetCardType()`

UnsetCardType ensures that no value is present for CardType, not even an explicit nil
### GetDateCreated

`func (o *PaymentMethodResponse) GetDateCreated() time.Time`

GetDateCreated returns the DateCreated field if non-nil, zero value otherwise.

### GetDateCreatedOk

`func (o *PaymentMethodResponse) GetDateCreatedOk() (*time.Time, bool)`

GetDateCreatedOk returns a tuple with the DateCreated field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDateCreated

`func (o *PaymentMethodResponse) SetDateCreated(v time.Time)`

SetDateCreated sets DateCreated field to given value.

### HasDateCreated

`func (o *PaymentMethodResponse) HasDateCreated() bool`

HasDateCreated returns a boolean if a field has been set.

### SetDateCreatedNil

`func (o *PaymentMethodResponse) SetDateCreatedNil(b bool)`

 SetDateCreatedNil sets the value for DateCreated to be an explicit nil

### UnsetDateCreated
`func (o *PaymentMethodResponse) UnsetDateCreated()`

UnsetDateCreated ensures that no value is present for DateCreated, not even an explicit nil
### GetStorageState

`func (o *PaymentMethodResponse) GetStorageState() string`

GetStorageState returns the StorageState field if non-nil, zero value otherwise.

### GetStorageStateOk

`func (o *PaymentMethodResponse) GetStorageStateOk() (*string, bool)`

GetStorageStateOk returns a tuple with the StorageState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStorageState

`func (o *PaymentMethodResponse) SetStorageState(v string)`

SetStorageState sets StorageState field to given value.

### HasStorageState

`func (o *PaymentMethodResponse) HasStorageState() bool`

HasStorageState returns a boolean if a field has been set.

### SetStorageStateNil

`func (o *PaymentMethodResponse) SetStorageStateNil(b bool)`

 SetStorageStateNil sets the value for StorageState to be an explicit nil

### UnsetStorageState
`func (o *PaymentMethodResponse) UnsetStorageState()`

UnsetStorageState ensures that no value is present for StorageState, not even an explicit nil
### GetBin

`func (o *PaymentMethodResponse) GetBin() string`

GetBin returns the Bin field if non-nil, zero value otherwise.

### GetBinOk

`func (o *PaymentMethodResponse) GetBinOk() (*string, bool)`

GetBinOk returns a tuple with the Bin field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBin

`func (o *PaymentMethodResponse) SetBin(v string)`

SetBin sets Bin field to given value.

### HasBin

`func (o *PaymentMethodResponse) HasBin() bool`

HasBin returns a boolean if a field has been set.

### SetBinNil

`func (o *PaymentMethodResponse) SetBinNil(b bool)`

 SetBinNil sets the value for Bin to be an explicit nil

### UnsetBin
`func (o *PaymentMethodResponse) UnsetBin()`

UnsetBin ensures that no value is present for Bin, not even an explicit nil
### GetVaultToken

`func (o *PaymentMethodResponse) GetVaultToken() string`

GetVaultToken returns the VaultToken field if non-nil, zero value otherwise.

### GetVaultTokenOk

`func (o *PaymentMethodResponse) GetVaultTokenOk() (*string, bool)`

GetVaultTokenOk returns a tuple with the VaultToken field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetVaultToken

`func (o *PaymentMethodResponse) SetVaultToken(v string)`

SetVaultToken sets VaultToken field to given value.

### HasVaultToken

`func (o *PaymentMethodResponse) HasVaultToken() bool`

HasVaultToken returns a boolean if a field has been set.

### SetVaultTokenNil

`func (o *PaymentMethodResponse) SetVaultTokenNil(b bool)`

 SetVaultTokenNil sets the value for VaultToken to be an explicit nil

### UnsetVaultToken
`func (o *PaymentMethodResponse) UnsetVaultToken()`

UnsetVaultToken ensures that no value is present for VaultToken, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


