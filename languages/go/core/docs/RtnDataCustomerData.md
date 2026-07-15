# RtnDataCustomerData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**FirstName** | Pointer to **string** | Customer first name. | [optional] 
**LastName** | Pointer to **string** | Customer last name. | [optional] 
**Email** | Pointer to **string** | Customer email address. | [optional] 
**HomePhone** | Pointer to **string** | Home phone number. Digits only, no formatting. | [optional] 
**MobilePhone** | Pointer to **string** | Mobile phone number. Digits only, no formatting. | [optional] 
**WorkPhone** | Pointer to **string** | Work phone number. Digits only, no formatting. | [optional] 
**AccountOpenedDate** | Pointer to **string** | Account creation date. Format YYYYMMDD. | [optional] 
**AccountAgeIndicator** | Pointer to **string** | Account age token: 01 &#x3D; created during transaction, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**IsFreeAccount** | Pointer to **bool** | True if the customer account is a free (non-paying) account. | [optional] 
**AccountLastChangedDate** | Pointer to **string** | Last account modification date. Format YYYYMMDD. | [optional] 
**AccountChangeIndicator** | Pointer to **string** | Account change age token: 01 &#x3D; during transaction, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**PasswordLastChangedDate** | Pointer to **string** | Last password change date. Format YYYYMMDD. | [optional] 
**PasswordChangeIndicator** | Pointer to **string** | Password change age: 01 &#x3D; never reset, 02 &#x3D; during transaction, 03 &#x3D; &lt;30 days, 04 &#x3D; 30–60 days, 05 &#x3D; &gt;60 days. | [optional] 
**TransactionSuccessfulCountLastSixMonths** | Pointer to **int32** | Count of successful purchases in the past 6 months. | [optional] 
**TransactionAttemptedCountLast24Hours** | Pointer to **int32** | Count of transaction attempts in the past 24 hours. | [optional] 
**TransactionAttemptedCountLastYear** | Pointer to **int32** | Count of transaction attempts in the past year. | [optional] 
**PaymentMethodAddedDate** | Pointer to **string** | Date payment method was added. Format YYYYMMDD. | [optional] 
**PaymentMethodAgeIndicator** | Pointer to **string** | Payment method age token. | [optional] 
**PaymentMethodAddAttemptCountLast24Hours** | Pointer to **int32** | Number of payment method add attempts in the past 24 hours. | [optional] 
**IsPaymentMethodOnFile** | Pointer to **bool** | True if the payment method is stored on file for the customer. | [optional] 
**IsAccountSuspicious** | Pointer to **bool** | True if the merchant considers the account suspicious. | [optional] 
**CustomerId** | Pointer to **string** | Merchant&#39;s internal customer identifier. | [optional] 
**AccountAuthenticationMethod** | Pointer to **string** | Method used to authenticate the customer for this session. | [optional] 
**IsTenuredCustomer** | Pointer to **bool** | True if the customer has a long-standing, established account relationship. | [optional] 
**IsEmailKnownToCustomer** | Pointer to **bool** | True if the email address on file is associated with a known customer account. | [optional] 
**IsRegisteredCustomer** | Pointer to **string** | Whether the purchaser is a registered member (Y) or guest (N). | [optional] 
**IsRegistrationUpdated** | Pointer to **string** | Whether any registration information changed since account creation. | [optional] 
**RegisteredAccountTenure** | Pointer to **int32** | Number of days the customer has been registered with the merchant. | [optional] 
**RegisteredName** | Pointer to **string** | Customer name as registered with the merchant. | [optional] 
**RegisteredEmail** | Pointer to **string** | Registered email address with the merchant. | [optional] 
**RegisteredPostalCode** | Pointer to **string** | Registered postal code with the merchant. | [optional] 
**RegisteredAddress** | Pointer to **string** | Registered address with the merchant (no city/state). | [optional] 
**RegisteredPhone** | Pointer to **string** | Registered phone number. Digits only. | [optional] 
**DaysSinceNameChange** | Pointer to **int32** | Days between the last registered-name change and the purchase date. | [optional] 
**DaysSinceEmailChange** | Pointer to **int32** | Days between the last registered-email change and the purchase date. | [optional] 
**DaysSincePasswordChange** | Pointer to **int32** | Days between the last password change and the purchase date. | [optional] 
**DaysSincePostalCodeChange** | Pointer to **int32** | Days between the last registered-postal-code change and the purchase date. | [optional] 
**DaysSinceAddressChange** | Pointer to **int32** | Days between the last registered-address change and the purchase date. | [optional] 
**DaysSincePhoneChange** | Pointer to **int32** | Days between the last registered-phone change and the purchase date. | [optional] 
**DaysSinceShipToNameChange** | Pointer to **int32** | Days between the last ship-to-name change and the purchase date. | [optional] 
**CustomerAni** | Pointer to **string** | ANI 10-digit phone number used to place a phone order. Digits only. | [optional] 
**CustomerAniDigits** | Pointer to **string** | ANI Information Identifier (II) digits: e.g. cellular &#x3D; 61–63, payphone &#x3D; 27, toll-free &#x3D; 24/25. | [optional] 
**IsEmailAssociatedWithFraud** | Pointer to **bool** | True if the email has been associated with confirmed/suspected fraud (distinct from isAccountSuspicious). Carrier for BofA emailAssociatedWithFraudFlag. | [optional] 

## Methods

### NewRtnDataCustomerData

`func NewRtnDataCustomerData() *RtnDataCustomerData`

NewRtnDataCustomerData instantiates a new RtnDataCustomerData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataCustomerDataWithDefaults

`func NewRtnDataCustomerDataWithDefaults() *RtnDataCustomerData`

NewRtnDataCustomerDataWithDefaults instantiates a new RtnDataCustomerData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetFirstName

`func (o *RtnDataCustomerData) GetFirstName() string`

GetFirstName returns the FirstName field if non-nil, zero value otherwise.

### GetFirstNameOk

`func (o *RtnDataCustomerData) GetFirstNameOk() (*string, bool)`

GetFirstNameOk returns a tuple with the FirstName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFirstName

`func (o *RtnDataCustomerData) SetFirstName(v string)`

SetFirstName sets FirstName field to given value.

### HasFirstName

`func (o *RtnDataCustomerData) HasFirstName() bool`

HasFirstName returns a boolean if a field has been set.

### GetLastName

`func (o *RtnDataCustomerData) GetLastName() string`

GetLastName returns the LastName field if non-nil, zero value otherwise.

### GetLastNameOk

`func (o *RtnDataCustomerData) GetLastNameOk() (*string, bool)`

GetLastNameOk returns a tuple with the LastName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastName

`func (o *RtnDataCustomerData) SetLastName(v string)`

SetLastName sets LastName field to given value.

### HasLastName

`func (o *RtnDataCustomerData) HasLastName() bool`

HasLastName returns a boolean if a field has been set.

### GetEmail

`func (o *RtnDataCustomerData) GetEmail() string`

GetEmail returns the Email field if non-nil, zero value otherwise.

### GetEmailOk

`func (o *RtnDataCustomerData) GetEmailOk() (*string, bool)`

GetEmailOk returns a tuple with the Email field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEmail

`func (o *RtnDataCustomerData) SetEmail(v string)`

SetEmail sets Email field to given value.

### HasEmail

`func (o *RtnDataCustomerData) HasEmail() bool`

HasEmail returns a boolean if a field has been set.

### GetHomePhone

`func (o *RtnDataCustomerData) GetHomePhone() string`

GetHomePhone returns the HomePhone field if non-nil, zero value otherwise.

### GetHomePhoneOk

`func (o *RtnDataCustomerData) GetHomePhoneOk() (*string, bool)`

GetHomePhoneOk returns a tuple with the HomePhone field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetHomePhone

`func (o *RtnDataCustomerData) SetHomePhone(v string)`

SetHomePhone sets HomePhone field to given value.

### HasHomePhone

`func (o *RtnDataCustomerData) HasHomePhone() bool`

HasHomePhone returns a boolean if a field has been set.

### GetMobilePhone

`func (o *RtnDataCustomerData) GetMobilePhone() string`

GetMobilePhone returns the MobilePhone field if non-nil, zero value otherwise.

### GetMobilePhoneOk

`func (o *RtnDataCustomerData) GetMobilePhoneOk() (*string, bool)`

GetMobilePhoneOk returns a tuple with the MobilePhone field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMobilePhone

`func (o *RtnDataCustomerData) SetMobilePhone(v string)`

SetMobilePhone sets MobilePhone field to given value.

### HasMobilePhone

`func (o *RtnDataCustomerData) HasMobilePhone() bool`

HasMobilePhone returns a boolean if a field has been set.

### GetWorkPhone

`func (o *RtnDataCustomerData) GetWorkPhone() string`

GetWorkPhone returns the WorkPhone field if non-nil, zero value otherwise.

### GetWorkPhoneOk

`func (o *RtnDataCustomerData) GetWorkPhoneOk() (*string, bool)`

GetWorkPhoneOk returns a tuple with the WorkPhone field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetWorkPhone

`func (o *RtnDataCustomerData) SetWorkPhone(v string)`

SetWorkPhone sets WorkPhone field to given value.

### HasWorkPhone

`func (o *RtnDataCustomerData) HasWorkPhone() bool`

HasWorkPhone returns a boolean if a field has been set.

### GetAccountOpenedDate

`func (o *RtnDataCustomerData) GetAccountOpenedDate() string`

GetAccountOpenedDate returns the AccountOpenedDate field if non-nil, zero value otherwise.

### GetAccountOpenedDateOk

`func (o *RtnDataCustomerData) GetAccountOpenedDateOk() (*string, bool)`

GetAccountOpenedDateOk returns a tuple with the AccountOpenedDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAccountOpenedDate

`func (o *RtnDataCustomerData) SetAccountOpenedDate(v string)`

SetAccountOpenedDate sets AccountOpenedDate field to given value.

### HasAccountOpenedDate

`func (o *RtnDataCustomerData) HasAccountOpenedDate() bool`

HasAccountOpenedDate returns a boolean if a field has been set.

### GetAccountAgeIndicator

`func (o *RtnDataCustomerData) GetAccountAgeIndicator() string`

GetAccountAgeIndicator returns the AccountAgeIndicator field if non-nil, zero value otherwise.

### GetAccountAgeIndicatorOk

`func (o *RtnDataCustomerData) GetAccountAgeIndicatorOk() (*string, bool)`

GetAccountAgeIndicatorOk returns a tuple with the AccountAgeIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAccountAgeIndicator

`func (o *RtnDataCustomerData) SetAccountAgeIndicator(v string)`

SetAccountAgeIndicator sets AccountAgeIndicator field to given value.

### HasAccountAgeIndicator

`func (o *RtnDataCustomerData) HasAccountAgeIndicator() bool`

HasAccountAgeIndicator returns a boolean if a field has been set.

### GetIsFreeAccount

`func (o *RtnDataCustomerData) GetIsFreeAccount() bool`

GetIsFreeAccount returns the IsFreeAccount field if non-nil, zero value otherwise.

### GetIsFreeAccountOk

`func (o *RtnDataCustomerData) GetIsFreeAccountOk() (*bool, bool)`

GetIsFreeAccountOk returns a tuple with the IsFreeAccount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsFreeAccount

`func (o *RtnDataCustomerData) SetIsFreeAccount(v bool)`

SetIsFreeAccount sets IsFreeAccount field to given value.

### HasIsFreeAccount

`func (o *RtnDataCustomerData) HasIsFreeAccount() bool`

HasIsFreeAccount returns a boolean if a field has been set.

### GetAccountLastChangedDate

`func (o *RtnDataCustomerData) GetAccountLastChangedDate() string`

GetAccountLastChangedDate returns the AccountLastChangedDate field if non-nil, zero value otherwise.

### GetAccountLastChangedDateOk

`func (o *RtnDataCustomerData) GetAccountLastChangedDateOk() (*string, bool)`

GetAccountLastChangedDateOk returns a tuple with the AccountLastChangedDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAccountLastChangedDate

`func (o *RtnDataCustomerData) SetAccountLastChangedDate(v string)`

SetAccountLastChangedDate sets AccountLastChangedDate field to given value.

### HasAccountLastChangedDate

`func (o *RtnDataCustomerData) HasAccountLastChangedDate() bool`

HasAccountLastChangedDate returns a boolean if a field has been set.

### GetAccountChangeIndicator

`func (o *RtnDataCustomerData) GetAccountChangeIndicator() string`

GetAccountChangeIndicator returns the AccountChangeIndicator field if non-nil, zero value otherwise.

### GetAccountChangeIndicatorOk

`func (o *RtnDataCustomerData) GetAccountChangeIndicatorOk() (*string, bool)`

GetAccountChangeIndicatorOk returns a tuple with the AccountChangeIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAccountChangeIndicator

`func (o *RtnDataCustomerData) SetAccountChangeIndicator(v string)`

SetAccountChangeIndicator sets AccountChangeIndicator field to given value.

### HasAccountChangeIndicator

`func (o *RtnDataCustomerData) HasAccountChangeIndicator() bool`

HasAccountChangeIndicator returns a boolean if a field has been set.

### GetPasswordLastChangedDate

`func (o *RtnDataCustomerData) GetPasswordLastChangedDate() string`

GetPasswordLastChangedDate returns the PasswordLastChangedDate field if non-nil, zero value otherwise.

### GetPasswordLastChangedDateOk

`func (o *RtnDataCustomerData) GetPasswordLastChangedDateOk() (*string, bool)`

GetPasswordLastChangedDateOk returns a tuple with the PasswordLastChangedDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPasswordLastChangedDate

`func (o *RtnDataCustomerData) SetPasswordLastChangedDate(v string)`

SetPasswordLastChangedDate sets PasswordLastChangedDate field to given value.

### HasPasswordLastChangedDate

`func (o *RtnDataCustomerData) HasPasswordLastChangedDate() bool`

HasPasswordLastChangedDate returns a boolean if a field has been set.

### GetPasswordChangeIndicator

`func (o *RtnDataCustomerData) GetPasswordChangeIndicator() string`

GetPasswordChangeIndicator returns the PasswordChangeIndicator field if non-nil, zero value otherwise.

### GetPasswordChangeIndicatorOk

`func (o *RtnDataCustomerData) GetPasswordChangeIndicatorOk() (*string, bool)`

GetPasswordChangeIndicatorOk returns a tuple with the PasswordChangeIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPasswordChangeIndicator

`func (o *RtnDataCustomerData) SetPasswordChangeIndicator(v string)`

SetPasswordChangeIndicator sets PasswordChangeIndicator field to given value.

### HasPasswordChangeIndicator

`func (o *RtnDataCustomerData) HasPasswordChangeIndicator() bool`

HasPasswordChangeIndicator returns a boolean if a field has been set.

### GetTransactionSuccessfulCountLastSixMonths

`func (o *RtnDataCustomerData) GetTransactionSuccessfulCountLastSixMonths() int32`

GetTransactionSuccessfulCountLastSixMonths returns the TransactionSuccessfulCountLastSixMonths field if non-nil, zero value otherwise.

### GetTransactionSuccessfulCountLastSixMonthsOk

`func (o *RtnDataCustomerData) GetTransactionSuccessfulCountLastSixMonthsOk() (*int32, bool)`

GetTransactionSuccessfulCountLastSixMonthsOk returns a tuple with the TransactionSuccessfulCountLastSixMonths field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionSuccessfulCountLastSixMonths

`func (o *RtnDataCustomerData) SetTransactionSuccessfulCountLastSixMonths(v int32)`

SetTransactionSuccessfulCountLastSixMonths sets TransactionSuccessfulCountLastSixMonths field to given value.

### HasTransactionSuccessfulCountLastSixMonths

`func (o *RtnDataCustomerData) HasTransactionSuccessfulCountLastSixMonths() bool`

HasTransactionSuccessfulCountLastSixMonths returns a boolean if a field has been set.

### GetTransactionAttemptedCountLast24Hours

`func (o *RtnDataCustomerData) GetTransactionAttemptedCountLast24Hours() int32`

GetTransactionAttemptedCountLast24Hours returns the TransactionAttemptedCountLast24Hours field if non-nil, zero value otherwise.

### GetTransactionAttemptedCountLast24HoursOk

`func (o *RtnDataCustomerData) GetTransactionAttemptedCountLast24HoursOk() (*int32, bool)`

GetTransactionAttemptedCountLast24HoursOk returns a tuple with the TransactionAttemptedCountLast24Hours field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionAttemptedCountLast24Hours

`func (o *RtnDataCustomerData) SetTransactionAttemptedCountLast24Hours(v int32)`

SetTransactionAttemptedCountLast24Hours sets TransactionAttemptedCountLast24Hours field to given value.

### HasTransactionAttemptedCountLast24Hours

`func (o *RtnDataCustomerData) HasTransactionAttemptedCountLast24Hours() bool`

HasTransactionAttemptedCountLast24Hours returns a boolean if a field has been set.

### GetTransactionAttemptedCountLastYear

`func (o *RtnDataCustomerData) GetTransactionAttemptedCountLastYear() int32`

GetTransactionAttemptedCountLastYear returns the TransactionAttemptedCountLastYear field if non-nil, zero value otherwise.

### GetTransactionAttemptedCountLastYearOk

`func (o *RtnDataCustomerData) GetTransactionAttemptedCountLastYearOk() (*int32, bool)`

GetTransactionAttemptedCountLastYearOk returns a tuple with the TransactionAttemptedCountLastYear field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionAttemptedCountLastYear

`func (o *RtnDataCustomerData) SetTransactionAttemptedCountLastYear(v int32)`

SetTransactionAttemptedCountLastYear sets TransactionAttemptedCountLastYear field to given value.

### HasTransactionAttemptedCountLastYear

`func (o *RtnDataCustomerData) HasTransactionAttemptedCountLastYear() bool`

HasTransactionAttemptedCountLastYear returns a boolean if a field has been set.

### GetPaymentMethodAddedDate

`func (o *RtnDataCustomerData) GetPaymentMethodAddedDate() string`

GetPaymentMethodAddedDate returns the PaymentMethodAddedDate field if non-nil, zero value otherwise.

### GetPaymentMethodAddedDateOk

`func (o *RtnDataCustomerData) GetPaymentMethodAddedDateOk() (*string, bool)`

GetPaymentMethodAddedDateOk returns a tuple with the PaymentMethodAddedDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodAddedDate

`func (o *RtnDataCustomerData) SetPaymentMethodAddedDate(v string)`

SetPaymentMethodAddedDate sets PaymentMethodAddedDate field to given value.

### HasPaymentMethodAddedDate

`func (o *RtnDataCustomerData) HasPaymentMethodAddedDate() bool`

HasPaymentMethodAddedDate returns a boolean if a field has been set.

### GetPaymentMethodAgeIndicator

`func (o *RtnDataCustomerData) GetPaymentMethodAgeIndicator() string`

GetPaymentMethodAgeIndicator returns the PaymentMethodAgeIndicator field if non-nil, zero value otherwise.

### GetPaymentMethodAgeIndicatorOk

`func (o *RtnDataCustomerData) GetPaymentMethodAgeIndicatorOk() (*string, bool)`

GetPaymentMethodAgeIndicatorOk returns a tuple with the PaymentMethodAgeIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodAgeIndicator

`func (o *RtnDataCustomerData) SetPaymentMethodAgeIndicator(v string)`

SetPaymentMethodAgeIndicator sets PaymentMethodAgeIndicator field to given value.

### HasPaymentMethodAgeIndicator

`func (o *RtnDataCustomerData) HasPaymentMethodAgeIndicator() bool`

HasPaymentMethodAgeIndicator returns a boolean if a field has been set.

### GetPaymentMethodAddAttemptCountLast24Hours

`func (o *RtnDataCustomerData) GetPaymentMethodAddAttemptCountLast24Hours() int32`

GetPaymentMethodAddAttemptCountLast24Hours returns the PaymentMethodAddAttemptCountLast24Hours field if non-nil, zero value otherwise.

### GetPaymentMethodAddAttemptCountLast24HoursOk

`func (o *RtnDataCustomerData) GetPaymentMethodAddAttemptCountLast24HoursOk() (*int32, bool)`

GetPaymentMethodAddAttemptCountLast24HoursOk returns a tuple with the PaymentMethodAddAttemptCountLast24Hours field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodAddAttemptCountLast24Hours

`func (o *RtnDataCustomerData) SetPaymentMethodAddAttemptCountLast24Hours(v int32)`

SetPaymentMethodAddAttemptCountLast24Hours sets PaymentMethodAddAttemptCountLast24Hours field to given value.

### HasPaymentMethodAddAttemptCountLast24Hours

`func (o *RtnDataCustomerData) HasPaymentMethodAddAttemptCountLast24Hours() bool`

HasPaymentMethodAddAttemptCountLast24Hours returns a boolean if a field has been set.

### GetIsPaymentMethodOnFile

`func (o *RtnDataCustomerData) GetIsPaymentMethodOnFile() bool`

GetIsPaymentMethodOnFile returns the IsPaymentMethodOnFile field if non-nil, zero value otherwise.

### GetIsPaymentMethodOnFileOk

`func (o *RtnDataCustomerData) GetIsPaymentMethodOnFileOk() (*bool, bool)`

GetIsPaymentMethodOnFileOk returns a tuple with the IsPaymentMethodOnFile field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsPaymentMethodOnFile

`func (o *RtnDataCustomerData) SetIsPaymentMethodOnFile(v bool)`

SetIsPaymentMethodOnFile sets IsPaymentMethodOnFile field to given value.

### HasIsPaymentMethodOnFile

`func (o *RtnDataCustomerData) HasIsPaymentMethodOnFile() bool`

HasIsPaymentMethodOnFile returns a boolean if a field has been set.

### GetIsAccountSuspicious

`func (o *RtnDataCustomerData) GetIsAccountSuspicious() bool`

GetIsAccountSuspicious returns the IsAccountSuspicious field if non-nil, zero value otherwise.

### GetIsAccountSuspiciousOk

`func (o *RtnDataCustomerData) GetIsAccountSuspiciousOk() (*bool, bool)`

GetIsAccountSuspiciousOk returns a tuple with the IsAccountSuspicious field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsAccountSuspicious

`func (o *RtnDataCustomerData) SetIsAccountSuspicious(v bool)`

SetIsAccountSuspicious sets IsAccountSuspicious field to given value.

### HasIsAccountSuspicious

`func (o *RtnDataCustomerData) HasIsAccountSuspicious() bool`

HasIsAccountSuspicious returns a boolean if a field has been set.

### GetCustomerId

`func (o *RtnDataCustomerData) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *RtnDataCustomerData) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *RtnDataCustomerData) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *RtnDataCustomerData) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### GetAccountAuthenticationMethod

`func (o *RtnDataCustomerData) GetAccountAuthenticationMethod() string`

GetAccountAuthenticationMethod returns the AccountAuthenticationMethod field if non-nil, zero value otherwise.

### GetAccountAuthenticationMethodOk

`func (o *RtnDataCustomerData) GetAccountAuthenticationMethodOk() (*string, bool)`

GetAccountAuthenticationMethodOk returns a tuple with the AccountAuthenticationMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAccountAuthenticationMethod

`func (o *RtnDataCustomerData) SetAccountAuthenticationMethod(v string)`

SetAccountAuthenticationMethod sets AccountAuthenticationMethod field to given value.

### HasAccountAuthenticationMethod

`func (o *RtnDataCustomerData) HasAccountAuthenticationMethod() bool`

HasAccountAuthenticationMethod returns a boolean if a field has been set.

### GetIsTenuredCustomer

`func (o *RtnDataCustomerData) GetIsTenuredCustomer() bool`

GetIsTenuredCustomer returns the IsTenuredCustomer field if non-nil, zero value otherwise.

### GetIsTenuredCustomerOk

`func (o *RtnDataCustomerData) GetIsTenuredCustomerOk() (*bool, bool)`

GetIsTenuredCustomerOk returns a tuple with the IsTenuredCustomer field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsTenuredCustomer

`func (o *RtnDataCustomerData) SetIsTenuredCustomer(v bool)`

SetIsTenuredCustomer sets IsTenuredCustomer field to given value.

### HasIsTenuredCustomer

`func (o *RtnDataCustomerData) HasIsTenuredCustomer() bool`

HasIsTenuredCustomer returns a boolean if a field has been set.

### GetIsEmailKnownToCustomer

`func (o *RtnDataCustomerData) GetIsEmailKnownToCustomer() bool`

GetIsEmailKnownToCustomer returns the IsEmailKnownToCustomer field if non-nil, zero value otherwise.

### GetIsEmailKnownToCustomerOk

`func (o *RtnDataCustomerData) GetIsEmailKnownToCustomerOk() (*bool, bool)`

GetIsEmailKnownToCustomerOk returns a tuple with the IsEmailKnownToCustomer field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsEmailKnownToCustomer

`func (o *RtnDataCustomerData) SetIsEmailKnownToCustomer(v bool)`

SetIsEmailKnownToCustomer sets IsEmailKnownToCustomer field to given value.

### HasIsEmailKnownToCustomer

`func (o *RtnDataCustomerData) HasIsEmailKnownToCustomer() bool`

HasIsEmailKnownToCustomer returns a boolean if a field has been set.

### GetIsRegisteredCustomer

`func (o *RtnDataCustomerData) GetIsRegisteredCustomer() string`

GetIsRegisteredCustomer returns the IsRegisteredCustomer field if non-nil, zero value otherwise.

### GetIsRegisteredCustomerOk

`func (o *RtnDataCustomerData) GetIsRegisteredCustomerOk() (*string, bool)`

GetIsRegisteredCustomerOk returns a tuple with the IsRegisteredCustomer field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsRegisteredCustomer

`func (o *RtnDataCustomerData) SetIsRegisteredCustomer(v string)`

SetIsRegisteredCustomer sets IsRegisteredCustomer field to given value.

### HasIsRegisteredCustomer

`func (o *RtnDataCustomerData) HasIsRegisteredCustomer() bool`

HasIsRegisteredCustomer returns a boolean if a field has been set.

### GetIsRegistrationUpdated

`func (o *RtnDataCustomerData) GetIsRegistrationUpdated() string`

GetIsRegistrationUpdated returns the IsRegistrationUpdated field if non-nil, zero value otherwise.

### GetIsRegistrationUpdatedOk

`func (o *RtnDataCustomerData) GetIsRegistrationUpdatedOk() (*string, bool)`

GetIsRegistrationUpdatedOk returns a tuple with the IsRegistrationUpdated field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsRegistrationUpdated

`func (o *RtnDataCustomerData) SetIsRegistrationUpdated(v string)`

SetIsRegistrationUpdated sets IsRegistrationUpdated field to given value.

### HasIsRegistrationUpdated

`func (o *RtnDataCustomerData) HasIsRegistrationUpdated() bool`

HasIsRegistrationUpdated returns a boolean if a field has been set.

### GetRegisteredAccountTenure

`func (o *RtnDataCustomerData) GetRegisteredAccountTenure() int32`

GetRegisteredAccountTenure returns the RegisteredAccountTenure field if non-nil, zero value otherwise.

### GetRegisteredAccountTenureOk

`func (o *RtnDataCustomerData) GetRegisteredAccountTenureOk() (*int32, bool)`

GetRegisteredAccountTenureOk returns a tuple with the RegisteredAccountTenure field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRegisteredAccountTenure

`func (o *RtnDataCustomerData) SetRegisteredAccountTenure(v int32)`

SetRegisteredAccountTenure sets RegisteredAccountTenure field to given value.

### HasRegisteredAccountTenure

`func (o *RtnDataCustomerData) HasRegisteredAccountTenure() bool`

HasRegisteredAccountTenure returns a boolean if a field has been set.

### GetRegisteredName

`func (o *RtnDataCustomerData) GetRegisteredName() string`

GetRegisteredName returns the RegisteredName field if non-nil, zero value otherwise.

### GetRegisteredNameOk

`func (o *RtnDataCustomerData) GetRegisteredNameOk() (*string, bool)`

GetRegisteredNameOk returns a tuple with the RegisteredName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRegisteredName

`func (o *RtnDataCustomerData) SetRegisteredName(v string)`

SetRegisteredName sets RegisteredName field to given value.

### HasRegisteredName

`func (o *RtnDataCustomerData) HasRegisteredName() bool`

HasRegisteredName returns a boolean if a field has been set.

### GetRegisteredEmail

`func (o *RtnDataCustomerData) GetRegisteredEmail() string`

GetRegisteredEmail returns the RegisteredEmail field if non-nil, zero value otherwise.

### GetRegisteredEmailOk

`func (o *RtnDataCustomerData) GetRegisteredEmailOk() (*string, bool)`

GetRegisteredEmailOk returns a tuple with the RegisteredEmail field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRegisteredEmail

`func (o *RtnDataCustomerData) SetRegisteredEmail(v string)`

SetRegisteredEmail sets RegisteredEmail field to given value.

### HasRegisteredEmail

`func (o *RtnDataCustomerData) HasRegisteredEmail() bool`

HasRegisteredEmail returns a boolean if a field has been set.

### GetRegisteredPostalCode

`func (o *RtnDataCustomerData) GetRegisteredPostalCode() string`

GetRegisteredPostalCode returns the RegisteredPostalCode field if non-nil, zero value otherwise.

### GetRegisteredPostalCodeOk

`func (o *RtnDataCustomerData) GetRegisteredPostalCodeOk() (*string, bool)`

GetRegisteredPostalCodeOk returns a tuple with the RegisteredPostalCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRegisteredPostalCode

`func (o *RtnDataCustomerData) SetRegisteredPostalCode(v string)`

SetRegisteredPostalCode sets RegisteredPostalCode field to given value.

### HasRegisteredPostalCode

`func (o *RtnDataCustomerData) HasRegisteredPostalCode() bool`

HasRegisteredPostalCode returns a boolean if a field has been set.

### GetRegisteredAddress

`func (o *RtnDataCustomerData) GetRegisteredAddress() string`

GetRegisteredAddress returns the RegisteredAddress field if non-nil, zero value otherwise.

### GetRegisteredAddressOk

`func (o *RtnDataCustomerData) GetRegisteredAddressOk() (*string, bool)`

GetRegisteredAddressOk returns a tuple with the RegisteredAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRegisteredAddress

`func (o *RtnDataCustomerData) SetRegisteredAddress(v string)`

SetRegisteredAddress sets RegisteredAddress field to given value.

### HasRegisteredAddress

`func (o *RtnDataCustomerData) HasRegisteredAddress() bool`

HasRegisteredAddress returns a boolean if a field has been set.

### GetRegisteredPhone

`func (o *RtnDataCustomerData) GetRegisteredPhone() string`

GetRegisteredPhone returns the RegisteredPhone field if non-nil, zero value otherwise.

### GetRegisteredPhoneOk

`func (o *RtnDataCustomerData) GetRegisteredPhoneOk() (*string, bool)`

GetRegisteredPhoneOk returns a tuple with the RegisteredPhone field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRegisteredPhone

`func (o *RtnDataCustomerData) SetRegisteredPhone(v string)`

SetRegisteredPhone sets RegisteredPhone field to given value.

### HasRegisteredPhone

`func (o *RtnDataCustomerData) HasRegisteredPhone() bool`

HasRegisteredPhone returns a boolean if a field has been set.

### GetDaysSinceNameChange

`func (o *RtnDataCustomerData) GetDaysSinceNameChange() int32`

GetDaysSinceNameChange returns the DaysSinceNameChange field if non-nil, zero value otherwise.

### GetDaysSinceNameChangeOk

`func (o *RtnDataCustomerData) GetDaysSinceNameChangeOk() (*int32, bool)`

GetDaysSinceNameChangeOk returns a tuple with the DaysSinceNameChange field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDaysSinceNameChange

`func (o *RtnDataCustomerData) SetDaysSinceNameChange(v int32)`

SetDaysSinceNameChange sets DaysSinceNameChange field to given value.

### HasDaysSinceNameChange

`func (o *RtnDataCustomerData) HasDaysSinceNameChange() bool`

HasDaysSinceNameChange returns a boolean if a field has been set.

### GetDaysSinceEmailChange

`func (o *RtnDataCustomerData) GetDaysSinceEmailChange() int32`

GetDaysSinceEmailChange returns the DaysSinceEmailChange field if non-nil, zero value otherwise.

### GetDaysSinceEmailChangeOk

`func (o *RtnDataCustomerData) GetDaysSinceEmailChangeOk() (*int32, bool)`

GetDaysSinceEmailChangeOk returns a tuple with the DaysSinceEmailChange field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDaysSinceEmailChange

`func (o *RtnDataCustomerData) SetDaysSinceEmailChange(v int32)`

SetDaysSinceEmailChange sets DaysSinceEmailChange field to given value.

### HasDaysSinceEmailChange

`func (o *RtnDataCustomerData) HasDaysSinceEmailChange() bool`

HasDaysSinceEmailChange returns a boolean if a field has been set.

### GetDaysSincePasswordChange

`func (o *RtnDataCustomerData) GetDaysSincePasswordChange() int32`

GetDaysSincePasswordChange returns the DaysSincePasswordChange field if non-nil, zero value otherwise.

### GetDaysSincePasswordChangeOk

`func (o *RtnDataCustomerData) GetDaysSincePasswordChangeOk() (*int32, bool)`

GetDaysSincePasswordChangeOk returns a tuple with the DaysSincePasswordChange field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDaysSincePasswordChange

`func (o *RtnDataCustomerData) SetDaysSincePasswordChange(v int32)`

SetDaysSincePasswordChange sets DaysSincePasswordChange field to given value.

### HasDaysSincePasswordChange

`func (o *RtnDataCustomerData) HasDaysSincePasswordChange() bool`

HasDaysSincePasswordChange returns a boolean if a field has been set.

### GetDaysSincePostalCodeChange

`func (o *RtnDataCustomerData) GetDaysSincePostalCodeChange() int32`

GetDaysSincePostalCodeChange returns the DaysSincePostalCodeChange field if non-nil, zero value otherwise.

### GetDaysSincePostalCodeChangeOk

`func (o *RtnDataCustomerData) GetDaysSincePostalCodeChangeOk() (*int32, bool)`

GetDaysSincePostalCodeChangeOk returns a tuple with the DaysSincePostalCodeChange field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDaysSincePostalCodeChange

`func (o *RtnDataCustomerData) SetDaysSincePostalCodeChange(v int32)`

SetDaysSincePostalCodeChange sets DaysSincePostalCodeChange field to given value.

### HasDaysSincePostalCodeChange

`func (o *RtnDataCustomerData) HasDaysSincePostalCodeChange() bool`

HasDaysSincePostalCodeChange returns a boolean if a field has been set.

### GetDaysSinceAddressChange

`func (o *RtnDataCustomerData) GetDaysSinceAddressChange() int32`

GetDaysSinceAddressChange returns the DaysSinceAddressChange field if non-nil, zero value otherwise.

### GetDaysSinceAddressChangeOk

`func (o *RtnDataCustomerData) GetDaysSinceAddressChangeOk() (*int32, bool)`

GetDaysSinceAddressChangeOk returns a tuple with the DaysSinceAddressChange field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDaysSinceAddressChange

`func (o *RtnDataCustomerData) SetDaysSinceAddressChange(v int32)`

SetDaysSinceAddressChange sets DaysSinceAddressChange field to given value.

### HasDaysSinceAddressChange

`func (o *RtnDataCustomerData) HasDaysSinceAddressChange() bool`

HasDaysSinceAddressChange returns a boolean if a field has been set.

### GetDaysSincePhoneChange

`func (o *RtnDataCustomerData) GetDaysSincePhoneChange() int32`

GetDaysSincePhoneChange returns the DaysSincePhoneChange field if non-nil, zero value otherwise.

### GetDaysSincePhoneChangeOk

`func (o *RtnDataCustomerData) GetDaysSincePhoneChangeOk() (*int32, bool)`

GetDaysSincePhoneChangeOk returns a tuple with the DaysSincePhoneChange field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDaysSincePhoneChange

`func (o *RtnDataCustomerData) SetDaysSincePhoneChange(v int32)`

SetDaysSincePhoneChange sets DaysSincePhoneChange field to given value.

### HasDaysSincePhoneChange

`func (o *RtnDataCustomerData) HasDaysSincePhoneChange() bool`

HasDaysSincePhoneChange returns a boolean if a field has been set.

### GetDaysSinceShipToNameChange

`func (o *RtnDataCustomerData) GetDaysSinceShipToNameChange() int32`

GetDaysSinceShipToNameChange returns the DaysSinceShipToNameChange field if non-nil, zero value otherwise.

### GetDaysSinceShipToNameChangeOk

`func (o *RtnDataCustomerData) GetDaysSinceShipToNameChangeOk() (*int32, bool)`

GetDaysSinceShipToNameChangeOk returns a tuple with the DaysSinceShipToNameChange field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDaysSinceShipToNameChange

`func (o *RtnDataCustomerData) SetDaysSinceShipToNameChange(v int32)`

SetDaysSinceShipToNameChange sets DaysSinceShipToNameChange field to given value.

### HasDaysSinceShipToNameChange

`func (o *RtnDataCustomerData) HasDaysSinceShipToNameChange() bool`

HasDaysSinceShipToNameChange returns a boolean if a field has been set.

### GetCustomerAni

`func (o *RtnDataCustomerData) GetCustomerAni() string`

GetCustomerAni returns the CustomerAni field if non-nil, zero value otherwise.

### GetCustomerAniOk

`func (o *RtnDataCustomerData) GetCustomerAniOk() (*string, bool)`

GetCustomerAniOk returns a tuple with the CustomerAni field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerAni

`func (o *RtnDataCustomerData) SetCustomerAni(v string)`

SetCustomerAni sets CustomerAni field to given value.

### HasCustomerAni

`func (o *RtnDataCustomerData) HasCustomerAni() bool`

HasCustomerAni returns a boolean if a field has been set.

### GetCustomerAniDigits

`func (o *RtnDataCustomerData) GetCustomerAniDigits() string`

GetCustomerAniDigits returns the CustomerAniDigits field if non-nil, zero value otherwise.

### GetCustomerAniDigitsOk

`func (o *RtnDataCustomerData) GetCustomerAniDigitsOk() (*string, bool)`

GetCustomerAniDigitsOk returns a tuple with the CustomerAniDigits field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerAniDigits

`func (o *RtnDataCustomerData) SetCustomerAniDigits(v string)`

SetCustomerAniDigits sets CustomerAniDigits field to given value.

### HasCustomerAniDigits

`func (o *RtnDataCustomerData) HasCustomerAniDigits() bool`

HasCustomerAniDigits returns a boolean if a field has been set.

### GetIsEmailAssociatedWithFraud

`func (o *RtnDataCustomerData) GetIsEmailAssociatedWithFraud() bool`

GetIsEmailAssociatedWithFraud returns the IsEmailAssociatedWithFraud field if non-nil, zero value otherwise.

### GetIsEmailAssociatedWithFraudOk

`func (o *RtnDataCustomerData) GetIsEmailAssociatedWithFraudOk() (*bool, bool)`

GetIsEmailAssociatedWithFraudOk returns a tuple with the IsEmailAssociatedWithFraud field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsEmailAssociatedWithFraud

`func (o *RtnDataCustomerData) SetIsEmailAssociatedWithFraud(v bool)`

SetIsEmailAssociatedWithFraud sets IsEmailAssociatedWithFraud field to given value.

### HasIsEmailAssociatedWithFraud

`func (o *RtnDataCustomerData) HasIsEmailAssociatedWithFraud() bool`

HasIsEmailAssociatedWithFraud returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


