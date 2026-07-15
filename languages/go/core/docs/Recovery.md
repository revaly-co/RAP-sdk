# Recovery

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**DisableCustomerRecovery** | Pointer to **NullableBool** | Whether customer recovery is disabled for this transaction | [optional] 
**ExternalApproval** | Pointer to **NullableBool** | Describes whether the approval should be attributed to the merchant for billing purposes | [optional] 
**CustomerAccountNumber** | Pointer to **NullableString** | Customer account number for recovery purposes | [optional] 
**CustomerBalance** | Pointer to **NullableInt32** | Customer account balance in smallest currency unit (e.g., cents for USD) | [optional] 
**DisableSMSNotification** | Pointer to **NullableBool** | Whether SMS notifications are disabled for recovery | [optional] 
**DisableEmailNotification** | Pointer to **NullableBool** | Whether email notifications are disabled for recovery | [optional] 
**RetryCount** | Pointer to **NullableInt32** | Number of retry attempts for this billing cycle (initial attempt is 0) | [optional] 
**PaymentReferenceData** | Pointer to **NullableString** | Reference data received when a payment failed. This data should be returned on retry transactions for the same payment. | [optional] 
**DateFirstAttempt** | Pointer to **NullableTime** | Date and time of the first transaction attempt for this billing cycle. Required when retry count is greater than 0. | [optional] 

## Methods

### NewRecovery

`func NewRecovery() *Recovery`

NewRecovery instantiates a new Recovery object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRecoveryWithDefaults

`func NewRecoveryWithDefaults() *Recovery`

NewRecoveryWithDefaults instantiates a new Recovery object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetDisableCustomerRecovery

`func (o *Recovery) GetDisableCustomerRecovery() bool`

GetDisableCustomerRecovery returns the DisableCustomerRecovery field if non-nil, zero value otherwise.

### GetDisableCustomerRecoveryOk

`func (o *Recovery) GetDisableCustomerRecoveryOk() (*bool, bool)`

GetDisableCustomerRecoveryOk returns a tuple with the DisableCustomerRecovery field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDisableCustomerRecovery

`func (o *Recovery) SetDisableCustomerRecovery(v bool)`

SetDisableCustomerRecovery sets DisableCustomerRecovery field to given value.

### HasDisableCustomerRecovery

`func (o *Recovery) HasDisableCustomerRecovery() bool`

HasDisableCustomerRecovery returns a boolean if a field has been set.

### SetDisableCustomerRecoveryNil

`func (o *Recovery) SetDisableCustomerRecoveryNil(b bool)`

 SetDisableCustomerRecoveryNil sets the value for DisableCustomerRecovery to be an explicit nil

### UnsetDisableCustomerRecovery
`func (o *Recovery) UnsetDisableCustomerRecovery()`

UnsetDisableCustomerRecovery ensures that no value is present for DisableCustomerRecovery, not even an explicit nil
### GetExternalApproval

`func (o *Recovery) GetExternalApproval() bool`

GetExternalApproval returns the ExternalApproval field if non-nil, zero value otherwise.

### GetExternalApprovalOk

`func (o *Recovery) GetExternalApprovalOk() (*bool, bool)`

GetExternalApprovalOk returns a tuple with the ExternalApproval field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExternalApproval

`func (o *Recovery) SetExternalApproval(v bool)`

SetExternalApproval sets ExternalApproval field to given value.

### HasExternalApproval

`func (o *Recovery) HasExternalApproval() bool`

HasExternalApproval returns a boolean if a field has been set.

### SetExternalApprovalNil

`func (o *Recovery) SetExternalApprovalNil(b bool)`

 SetExternalApprovalNil sets the value for ExternalApproval to be an explicit nil

### UnsetExternalApproval
`func (o *Recovery) UnsetExternalApproval()`

UnsetExternalApproval ensures that no value is present for ExternalApproval, not even an explicit nil
### GetCustomerAccountNumber

`func (o *Recovery) GetCustomerAccountNumber() string`

GetCustomerAccountNumber returns the CustomerAccountNumber field if non-nil, zero value otherwise.

### GetCustomerAccountNumberOk

`func (o *Recovery) GetCustomerAccountNumberOk() (*string, bool)`

GetCustomerAccountNumberOk returns a tuple with the CustomerAccountNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerAccountNumber

`func (o *Recovery) SetCustomerAccountNumber(v string)`

SetCustomerAccountNumber sets CustomerAccountNumber field to given value.

### HasCustomerAccountNumber

`func (o *Recovery) HasCustomerAccountNumber() bool`

HasCustomerAccountNumber returns a boolean if a field has been set.

### SetCustomerAccountNumberNil

`func (o *Recovery) SetCustomerAccountNumberNil(b bool)`

 SetCustomerAccountNumberNil sets the value for CustomerAccountNumber to be an explicit nil

### UnsetCustomerAccountNumber
`func (o *Recovery) UnsetCustomerAccountNumber()`

UnsetCustomerAccountNumber ensures that no value is present for CustomerAccountNumber, not even an explicit nil
### GetCustomerBalance

`func (o *Recovery) GetCustomerBalance() int32`

GetCustomerBalance returns the CustomerBalance field if non-nil, zero value otherwise.

### GetCustomerBalanceOk

`func (o *Recovery) GetCustomerBalanceOk() (*int32, bool)`

GetCustomerBalanceOk returns a tuple with the CustomerBalance field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerBalance

`func (o *Recovery) SetCustomerBalance(v int32)`

SetCustomerBalance sets CustomerBalance field to given value.

### HasCustomerBalance

`func (o *Recovery) HasCustomerBalance() bool`

HasCustomerBalance returns a boolean if a field has been set.

### SetCustomerBalanceNil

`func (o *Recovery) SetCustomerBalanceNil(b bool)`

 SetCustomerBalanceNil sets the value for CustomerBalance to be an explicit nil

### UnsetCustomerBalance
`func (o *Recovery) UnsetCustomerBalance()`

UnsetCustomerBalance ensures that no value is present for CustomerBalance, not even an explicit nil
### GetDisableSMSNotification

`func (o *Recovery) GetDisableSMSNotification() bool`

GetDisableSMSNotification returns the DisableSMSNotification field if non-nil, zero value otherwise.

### GetDisableSMSNotificationOk

`func (o *Recovery) GetDisableSMSNotificationOk() (*bool, bool)`

GetDisableSMSNotificationOk returns a tuple with the DisableSMSNotification field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDisableSMSNotification

`func (o *Recovery) SetDisableSMSNotification(v bool)`

SetDisableSMSNotification sets DisableSMSNotification field to given value.

### HasDisableSMSNotification

`func (o *Recovery) HasDisableSMSNotification() bool`

HasDisableSMSNotification returns a boolean if a field has been set.

### SetDisableSMSNotificationNil

`func (o *Recovery) SetDisableSMSNotificationNil(b bool)`

 SetDisableSMSNotificationNil sets the value for DisableSMSNotification to be an explicit nil

### UnsetDisableSMSNotification
`func (o *Recovery) UnsetDisableSMSNotification()`

UnsetDisableSMSNotification ensures that no value is present for DisableSMSNotification, not even an explicit nil
### GetDisableEmailNotification

`func (o *Recovery) GetDisableEmailNotification() bool`

GetDisableEmailNotification returns the DisableEmailNotification field if non-nil, zero value otherwise.

### GetDisableEmailNotificationOk

`func (o *Recovery) GetDisableEmailNotificationOk() (*bool, bool)`

GetDisableEmailNotificationOk returns a tuple with the DisableEmailNotification field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDisableEmailNotification

`func (o *Recovery) SetDisableEmailNotification(v bool)`

SetDisableEmailNotification sets DisableEmailNotification field to given value.

### HasDisableEmailNotification

`func (o *Recovery) HasDisableEmailNotification() bool`

HasDisableEmailNotification returns a boolean if a field has been set.

### SetDisableEmailNotificationNil

`func (o *Recovery) SetDisableEmailNotificationNil(b bool)`

 SetDisableEmailNotificationNil sets the value for DisableEmailNotification to be an explicit nil

### UnsetDisableEmailNotification
`func (o *Recovery) UnsetDisableEmailNotification()`

UnsetDisableEmailNotification ensures that no value is present for DisableEmailNotification, not even an explicit nil
### GetRetryCount

`func (o *Recovery) GetRetryCount() int32`

GetRetryCount returns the RetryCount field if non-nil, zero value otherwise.

### GetRetryCountOk

`func (o *Recovery) GetRetryCountOk() (*int32, bool)`

GetRetryCountOk returns a tuple with the RetryCount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRetryCount

`func (o *Recovery) SetRetryCount(v int32)`

SetRetryCount sets RetryCount field to given value.

### HasRetryCount

`func (o *Recovery) HasRetryCount() bool`

HasRetryCount returns a boolean if a field has been set.

### SetRetryCountNil

`func (o *Recovery) SetRetryCountNil(b bool)`

 SetRetryCountNil sets the value for RetryCount to be an explicit nil

### UnsetRetryCount
`func (o *Recovery) UnsetRetryCount()`

UnsetRetryCount ensures that no value is present for RetryCount, not even an explicit nil
### GetPaymentReferenceData

`func (o *Recovery) GetPaymentReferenceData() string`

GetPaymentReferenceData returns the PaymentReferenceData field if non-nil, zero value otherwise.

### GetPaymentReferenceDataOk

`func (o *Recovery) GetPaymentReferenceDataOk() (*string, bool)`

GetPaymentReferenceDataOk returns a tuple with the PaymentReferenceData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentReferenceData

`func (o *Recovery) SetPaymentReferenceData(v string)`

SetPaymentReferenceData sets PaymentReferenceData field to given value.

### HasPaymentReferenceData

`func (o *Recovery) HasPaymentReferenceData() bool`

HasPaymentReferenceData returns a boolean if a field has been set.

### SetPaymentReferenceDataNil

`func (o *Recovery) SetPaymentReferenceDataNil(b bool)`

 SetPaymentReferenceDataNil sets the value for PaymentReferenceData to be an explicit nil

### UnsetPaymentReferenceData
`func (o *Recovery) UnsetPaymentReferenceData()`

UnsetPaymentReferenceData ensures that no value is present for PaymentReferenceData, not even an explicit nil
### GetDateFirstAttempt

`func (o *Recovery) GetDateFirstAttempt() time.Time`

GetDateFirstAttempt returns the DateFirstAttempt field if non-nil, zero value otherwise.

### GetDateFirstAttemptOk

`func (o *Recovery) GetDateFirstAttemptOk() (*time.Time, bool)`

GetDateFirstAttemptOk returns a tuple with the DateFirstAttempt field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDateFirstAttempt

`func (o *Recovery) SetDateFirstAttempt(v time.Time)`

SetDateFirstAttempt sets DateFirstAttempt field to given value.

### HasDateFirstAttempt

`func (o *Recovery) HasDateFirstAttempt() bool`

HasDateFirstAttempt returns a boolean if a field has been set.

### SetDateFirstAttemptNil

`func (o *Recovery) SetDateFirstAttemptNil(b bool)`

 SetDateFirstAttemptNil sets the value for DateFirstAttempt to be an explicit nil

### UnsetDateFirstAttempt
`func (o *Recovery) UnsetDateFirstAttempt()`

UnsetDateFirstAttempt ensures that no value is present for DateFirstAttempt, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


