# NotifyData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | Pointer to **NullableString** | Revaly transaction identifier | [optional] 
**MerchantTransactionId** | Pointer to **NullableString** | Merchant&#39;s transaction identifier | [optional] 
**OrderID** | Pointer to **NullableString** | Order identifier associated with the transaction | [optional] 
**CustomerId** | Pointer to **NullableString** | Customer identifier | [optional] 
**Amount** | Pointer to **NullableInt32** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**Currency** | Pointer to **NullableString** | Three-letter ISO currency code | [optional] 
**CustomerAccountNumber** | Pointer to **NullableString** | Customer account number for recovery purposes | [optional] 
**DisableSmsNotification** | Pointer to **NullableBool** | Whether to disable SMS notifications for this customer | [optional] 
**DisableEmailNotification** | Pointer to **NullableBool** | Whether to disable email notifications for this customer | [optional] 
**ContactInformation** | Pointer to [**NotifyContactInformation**](NotifyContactInformation.md) |  | [optional] 
**Address** | Pointer to [**Address**](Address.md) |  | [optional] 
**ReasonCode** | Pointer to **NullableString** | Network chargeback reason code (e.g. Visa \&quot;10.4\&quot;). Chargeback-only, optional. | [optional] 
**Arn** | Pointer to **NullableString** | Acquirer Reference Number or network case ID for the dispute. Chargeback-only, optional. | [optional] 
**DisputeDate** | Pointer to **NullableTime** | When the dispute was raised. Chargeback-only, optional. | [optional] 

## Methods

### NewNotifyData

`func NewNotifyData() *NotifyData`

NewNotifyData instantiates a new NotifyData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewNotifyDataWithDefaults

`func NewNotifyDataWithDefaults() *NotifyData`

NewNotifyDataWithDefaults instantiates a new NotifyData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionId

`func (o *NotifyData) GetTransactionId() string`

GetTransactionId returns the TransactionId field if non-nil, zero value otherwise.

### GetTransactionIdOk

`func (o *NotifyData) GetTransactionIdOk() (*string, bool)`

GetTransactionIdOk returns a tuple with the TransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionId

`func (o *NotifyData) SetTransactionId(v string)`

SetTransactionId sets TransactionId field to given value.

### HasTransactionId

`func (o *NotifyData) HasTransactionId() bool`

HasTransactionId returns a boolean if a field has been set.

### SetTransactionIdNil

`func (o *NotifyData) SetTransactionIdNil(b bool)`

 SetTransactionIdNil sets the value for TransactionId to be an explicit nil

### UnsetTransactionId
`func (o *NotifyData) UnsetTransactionId()`

UnsetTransactionId ensures that no value is present for TransactionId, not even an explicit nil
### GetMerchantTransactionId

`func (o *NotifyData) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *NotifyData) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *NotifyData) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.

### HasMerchantTransactionId

`func (o *NotifyData) HasMerchantTransactionId() bool`

HasMerchantTransactionId returns a boolean if a field has been set.

### SetMerchantTransactionIdNil

`func (o *NotifyData) SetMerchantTransactionIdNil(b bool)`

 SetMerchantTransactionIdNil sets the value for MerchantTransactionId to be an explicit nil

### UnsetMerchantTransactionId
`func (o *NotifyData) UnsetMerchantTransactionId()`

UnsetMerchantTransactionId ensures that no value is present for MerchantTransactionId, not even an explicit nil
### GetOrderID

`func (o *NotifyData) GetOrderID() string`

GetOrderID returns the OrderID field if non-nil, zero value otherwise.

### GetOrderIDOk

`func (o *NotifyData) GetOrderIDOk() (*string, bool)`

GetOrderIDOk returns a tuple with the OrderID field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderID

`func (o *NotifyData) SetOrderID(v string)`

SetOrderID sets OrderID field to given value.

### HasOrderID

`func (o *NotifyData) HasOrderID() bool`

HasOrderID returns a boolean if a field has been set.

### SetOrderIDNil

`func (o *NotifyData) SetOrderIDNil(b bool)`

 SetOrderIDNil sets the value for OrderID to be an explicit nil

### UnsetOrderID
`func (o *NotifyData) UnsetOrderID()`

UnsetOrderID ensures that no value is present for OrderID, not even an explicit nil
### GetCustomerId

`func (o *NotifyData) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *NotifyData) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *NotifyData) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *NotifyData) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *NotifyData) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *NotifyData) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetAmount

`func (o *NotifyData) GetAmount() int32`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *NotifyData) GetAmountOk() (*int32, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *NotifyData) SetAmount(v int32)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *NotifyData) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *NotifyData) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *NotifyData) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil
### GetCurrency

`func (o *NotifyData) GetCurrency() string`

GetCurrency returns the Currency field if non-nil, zero value otherwise.

### GetCurrencyOk

`func (o *NotifyData) GetCurrencyOk() (*string, bool)`

GetCurrencyOk returns a tuple with the Currency field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrency

`func (o *NotifyData) SetCurrency(v string)`

SetCurrency sets Currency field to given value.

### HasCurrency

`func (o *NotifyData) HasCurrency() bool`

HasCurrency returns a boolean if a field has been set.

### SetCurrencyNil

`func (o *NotifyData) SetCurrencyNil(b bool)`

 SetCurrencyNil sets the value for Currency to be an explicit nil

### UnsetCurrency
`func (o *NotifyData) UnsetCurrency()`

UnsetCurrency ensures that no value is present for Currency, not even an explicit nil
### GetCustomerAccountNumber

`func (o *NotifyData) GetCustomerAccountNumber() string`

GetCustomerAccountNumber returns the CustomerAccountNumber field if non-nil, zero value otherwise.

### GetCustomerAccountNumberOk

`func (o *NotifyData) GetCustomerAccountNumberOk() (*string, bool)`

GetCustomerAccountNumberOk returns a tuple with the CustomerAccountNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerAccountNumber

`func (o *NotifyData) SetCustomerAccountNumber(v string)`

SetCustomerAccountNumber sets CustomerAccountNumber field to given value.

### HasCustomerAccountNumber

`func (o *NotifyData) HasCustomerAccountNumber() bool`

HasCustomerAccountNumber returns a boolean if a field has been set.

### SetCustomerAccountNumberNil

`func (o *NotifyData) SetCustomerAccountNumberNil(b bool)`

 SetCustomerAccountNumberNil sets the value for CustomerAccountNumber to be an explicit nil

### UnsetCustomerAccountNumber
`func (o *NotifyData) UnsetCustomerAccountNumber()`

UnsetCustomerAccountNumber ensures that no value is present for CustomerAccountNumber, not even an explicit nil
### GetDisableSmsNotification

`func (o *NotifyData) GetDisableSmsNotification() bool`

GetDisableSmsNotification returns the DisableSmsNotification field if non-nil, zero value otherwise.

### GetDisableSmsNotificationOk

`func (o *NotifyData) GetDisableSmsNotificationOk() (*bool, bool)`

GetDisableSmsNotificationOk returns a tuple with the DisableSmsNotification field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDisableSmsNotification

`func (o *NotifyData) SetDisableSmsNotification(v bool)`

SetDisableSmsNotification sets DisableSmsNotification field to given value.

### HasDisableSmsNotification

`func (o *NotifyData) HasDisableSmsNotification() bool`

HasDisableSmsNotification returns a boolean if a field has been set.

### SetDisableSmsNotificationNil

`func (o *NotifyData) SetDisableSmsNotificationNil(b bool)`

 SetDisableSmsNotificationNil sets the value for DisableSmsNotification to be an explicit nil

### UnsetDisableSmsNotification
`func (o *NotifyData) UnsetDisableSmsNotification()`

UnsetDisableSmsNotification ensures that no value is present for DisableSmsNotification, not even an explicit nil
### GetDisableEmailNotification

`func (o *NotifyData) GetDisableEmailNotification() bool`

GetDisableEmailNotification returns the DisableEmailNotification field if non-nil, zero value otherwise.

### GetDisableEmailNotificationOk

`func (o *NotifyData) GetDisableEmailNotificationOk() (*bool, bool)`

GetDisableEmailNotificationOk returns a tuple with the DisableEmailNotification field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDisableEmailNotification

`func (o *NotifyData) SetDisableEmailNotification(v bool)`

SetDisableEmailNotification sets DisableEmailNotification field to given value.

### HasDisableEmailNotification

`func (o *NotifyData) HasDisableEmailNotification() bool`

HasDisableEmailNotification returns a boolean if a field has been set.

### SetDisableEmailNotificationNil

`func (o *NotifyData) SetDisableEmailNotificationNil(b bool)`

 SetDisableEmailNotificationNil sets the value for DisableEmailNotification to be an explicit nil

### UnsetDisableEmailNotification
`func (o *NotifyData) UnsetDisableEmailNotification()`

UnsetDisableEmailNotification ensures that no value is present for DisableEmailNotification, not even an explicit nil
### GetContactInformation

`func (o *NotifyData) GetContactInformation() NotifyContactInformation`

GetContactInformation returns the ContactInformation field if non-nil, zero value otherwise.

### GetContactInformationOk

`func (o *NotifyData) GetContactInformationOk() (*NotifyContactInformation, bool)`

GetContactInformationOk returns a tuple with the ContactInformation field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetContactInformation

`func (o *NotifyData) SetContactInformation(v NotifyContactInformation)`

SetContactInformation sets ContactInformation field to given value.

### HasContactInformation

`func (o *NotifyData) HasContactInformation() bool`

HasContactInformation returns a boolean if a field has been set.

### GetAddress

`func (o *NotifyData) GetAddress() Address`

GetAddress returns the Address field if non-nil, zero value otherwise.

### GetAddressOk

`func (o *NotifyData) GetAddressOk() (*Address, bool)`

GetAddressOk returns a tuple with the Address field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAddress

`func (o *NotifyData) SetAddress(v Address)`

SetAddress sets Address field to given value.

### HasAddress

`func (o *NotifyData) HasAddress() bool`

HasAddress returns a boolean if a field has been set.

### GetReasonCode

`func (o *NotifyData) GetReasonCode() string`

GetReasonCode returns the ReasonCode field if non-nil, zero value otherwise.

### GetReasonCodeOk

`func (o *NotifyData) GetReasonCodeOk() (*string, bool)`

GetReasonCodeOk returns a tuple with the ReasonCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetReasonCode

`func (o *NotifyData) SetReasonCode(v string)`

SetReasonCode sets ReasonCode field to given value.

### HasReasonCode

`func (o *NotifyData) HasReasonCode() bool`

HasReasonCode returns a boolean if a field has been set.

### SetReasonCodeNil

`func (o *NotifyData) SetReasonCodeNil(b bool)`

 SetReasonCodeNil sets the value for ReasonCode to be an explicit nil

### UnsetReasonCode
`func (o *NotifyData) UnsetReasonCode()`

UnsetReasonCode ensures that no value is present for ReasonCode, not even an explicit nil
### GetArn

`func (o *NotifyData) GetArn() string`

GetArn returns the Arn field if non-nil, zero value otherwise.

### GetArnOk

`func (o *NotifyData) GetArnOk() (*string, bool)`

GetArnOk returns a tuple with the Arn field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetArn

`func (o *NotifyData) SetArn(v string)`

SetArn sets Arn field to given value.

### HasArn

`func (o *NotifyData) HasArn() bool`

HasArn returns a boolean if a field has been set.

### SetArnNil

`func (o *NotifyData) SetArnNil(b bool)`

 SetArnNil sets the value for Arn to be an explicit nil

### UnsetArn
`func (o *NotifyData) UnsetArn()`

UnsetArn ensures that no value is present for Arn, not even an explicit nil
### GetDisputeDate

`func (o *NotifyData) GetDisputeDate() time.Time`

GetDisputeDate returns the DisputeDate field if non-nil, zero value otherwise.

### GetDisputeDateOk

`func (o *NotifyData) GetDisputeDateOk() (*time.Time, bool)`

GetDisputeDateOk returns a tuple with the DisputeDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDisputeDate

`func (o *NotifyData) SetDisputeDate(v time.Time)`

SetDisputeDate sets DisputeDate field to given value.

### HasDisputeDate

`func (o *NotifyData) HasDisputeDate() bool`

HasDisputeDate returns a boolean if a field has been set.

### SetDisputeDateNil

`func (o *NotifyData) SetDisputeDateNil(b bool)`

 SetDisputeDateNil sets the value for DisputeDate to be an explicit nil

### UnsetDisputeDate
`func (o *NotifyData) UnsetDisputeDate()`

UnsetDisputeDate ensures that no value is present for DisputeDate, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


