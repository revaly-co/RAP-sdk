# PreviousTransaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionDate** | Pointer to **NullableTime** | Date of the previous transaction | [optional] 
**MerchantAccountReferenceId** | Pointer to **NullableString** | Merchant account reference ID from the previous transaction | [optional] 
**GatewayCode** | Pointer to **NullableString** | Gateway response code from the previous transaction | [optional] 
**GatewayMessage** | Pointer to **NullableString** | Gateway response message from the previous transaction | [optional] 
**GatewayMessageKey** | Pointer to **NullableString** | Gateway message key from the previous transaction | [optional] 
**TransactionStatus** | Pointer to **NullableInt32** | Previous status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**AvsCode** | Pointer to **NullableString** | AVS code from the previous transaction | [optional] 
**AvsMessage** | Pointer to **NullableString** | AVS message from the previous transaction | [optional] 
**CvvCode** | Pointer to **NullableString** | CVV code from the previous transaction | [optional] 
**CvvMessage** | Pointer to **NullableString** | CVV message from the previous transaction | [optional] 

## Methods

### NewPreviousTransaction

`func NewPreviousTransaction() *PreviousTransaction`

NewPreviousTransaction instantiates a new PreviousTransaction object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewPreviousTransactionWithDefaults

`func NewPreviousTransactionWithDefaults() *PreviousTransaction`

NewPreviousTransactionWithDefaults instantiates a new PreviousTransaction object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionDate

`func (o *PreviousTransaction) GetTransactionDate() time.Time`

GetTransactionDate returns the TransactionDate field if non-nil, zero value otherwise.

### GetTransactionDateOk

`func (o *PreviousTransaction) GetTransactionDateOk() (*time.Time, bool)`

GetTransactionDateOk returns a tuple with the TransactionDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionDate

`func (o *PreviousTransaction) SetTransactionDate(v time.Time)`

SetTransactionDate sets TransactionDate field to given value.

### HasTransactionDate

`func (o *PreviousTransaction) HasTransactionDate() bool`

HasTransactionDate returns a boolean if a field has been set.

### SetTransactionDateNil

`func (o *PreviousTransaction) SetTransactionDateNil(b bool)`

 SetTransactionDateNil sets the value for TransactionDate to be an explicit nil

### UnsetTransactionDate
`func (o *PreviousTransaction) UnsetTransactionDate()`

UnsetTransactionDate ensures that no value is present for TransactionDate, not even an explicit nil
### GetMerchantAccountReferenceId

`func (o *PreviousTransaction) GetMerchantAccountReferenceId() string`

GetMerchantAccountReferenceId returns the MerchantAccountReferenceId field if non-nil, zero value otherwise.

### GetMerchantAccountReferenceIdOk

`func (o *PreviousTransaction) GetMerchantAccountReferenceIdOk() (*string, bool)`

GetMerchantAccountReferenceIdOk returns a tuple with the MerchantAccountReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantAccountReferenceId

`func (o *PreviousTransaction) SetMerchantAccountReferenceId(v string)`

SetMerchantAccountReferenceId sets MerchantAccountReferenceId field to given value.

### HasMerchantAccountReferenceId

`func (o *PreviousTransaction) HasMerchantAccountReferenceId() bool`

HasMerchantAccountReferenceId returns a boolean if a field has been set.

### SetMerchantAccountReferenceIdNil

`func (o *PreviousTransaction) SetMerchantAccountReferenceIdNil(b bool)`

 SetMerchantAccountReferenceIdNil sets the value for MerchantAccountReferenceId to be an explicit nil

### UnsetMerchantAccountReferenceId
`func (o *PreviousTransaction) UnsetMerchantAccountReferenceId()`

UnsetMerchantAccountReferenceId ensures that no value is present for MerchantAccountReferenceId, not even an explicit nil
### GetGatewayCode

`func (o *PreviousTransaction) GetGatewayCode() string`

GetGatewayCode returns the GatewayCode field if non-nil, zero value otherwise.

### GetGatewayCodeOk

`func (o *PreviousTransaction) GetGatewayCodeOk() (*string, bool)`

GetGatewayCodeOk returns a tuple with the GatewayCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayCode

`func (o *PreviousTransaction) SetGatewayCode(v string)`

SetGatewayCode sets GatewayCode field to given value.

### HasGatewayCode

`func (o *PreviousTransaction) HasGatewayCode() bool`

HasGatewayCode returns a boolean if a field has been set.

### SetGatewayCodeNil

`func (o *PreviousTransaction) SetGatewayCodeNil(b bool)`

 SetGatewayCodeNil sets the value for GatewayCode to be an explicit nil

### UnsetGatewayCode
`func (o *PreviousTransaction) UnsetGatewayCode()`

UnsetGatewayCode ensures that no value is present for GatewayCode, not even an explicit nil
### GetGatewayMessage

`func (o *PreviousTransaction) GetGatewayMessage() string`

GetGatewayMessage returns the GatewayMessage field if non-nil, zero value otherwise.

### GetGatewayMessageOk

`func (o *PreviousTransaction) GetGatewayMessageOk() (*string, bool)`

GetGatewayMessageOk returns a tuple with the GatewayMessage field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayMessage

`func (o *PreviousTransaction) SetGatewayMessage(v string)`

SetGatewayMessage sets GatewayMessage field to given value.

### HasGatewayMessage

`func (o *PreviousTransaction) HasGatewayMessage() bool`

HasGatewayMessage returns a boolean if a field has been set.

### SetGatewayMessageNil

`func (o *PreviousTransaction) SetGatewayMessageNil(b bool)`

 SetGatewayMessageNil sets the value for GatewayMessage to be an explicit nil

### UnsetGatewayMessage
`func (o *PreviousTransaction) UnsetGatewayMessage()`

UnsetGatewayMessage ensures that no value is present for GatewayMessage, not even an explicit nil
### GetGatewayMessageKey

`func (o *PreviousTransaction) GetGatewayMessageKey() string`

GetGatewayMessageKey returns the GatewayMessageKey field if non-nil, zero value otherwise.

### GetGatewayMessageKeyOk

`func (o *PreviousTransaction) GetGatewayMessageKeyOk() (*string, bool)`

GetGatewayMessageKeyOk returns a tuple with the GatewayMessageKey field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayMessageKey

`func (o *PreviousTransaction) SetGatewayMessageKey(v string)`

SetGatewayMessageKey sets GatewayMessageKey field to given value.

### HasGatewayMessageKey

`func (o *PreviousTransaction) HasGatewayMessageKey() bool`

HasGatewayMessageKey returns a boolean if a field has been set.

### SetGatewayMessageKeyNil

`func (o *PreviousTransaction) SetGatewayMessageKeyNil(b bool)`

 SetGatewayMessageKeyNil sets the value for GatewayMessageKey to be an explicit nil

### UnsetGatewayMessageKey
`func (o *PreviousTransaction) UnsetGatewayMessageKey()`

UnsetGatewayMessageKey ensures that no value is present for GatewayMessageKey, not even an explicit nil
### GetTransactionStatus

`func (o *PreviousTransaction) GetTransactionStatus() int32`

GetTransactionStatus returns the TransactionStatus field if non-nil, zero value otherwise.

### GetTransactionStatusOk

`func (o *PreviousTransaction) GetTransactionStatusOk() (*int32, bool)`

GetTransactionStatusOk returns a tuple with the TransactionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionStatus

`func (o *PreviousTransaction) SetTransactionStatus(v int32)`

SetTransactionStatus sets TransactionStatus field to given value.

### HasTransactionStatus

`func (o *PreviousTransaction) HasTransactionStatus() bool`

HasTransactionStatus returns a boolean if a field has been set.

### SetTransactionStatusNil

`func (o *PreviousTransaction) SetTransactionStatusNil(b bool)`

 SetTransactionStatusNil sets the value for TransactionStatus to be an explicit nil

### UnsetTransactionStatus
`func (o *PreviousTransaction) UnsetTransactionStatus()`

UnsetTransactionStatus ensures that no value is present for TransactionStatus, not even an explicit nil
### GetAvsCode

`func (o *PreviousTransaction) GetAvsCode() string`

GetAvsCode returns the AvsCode field if non-nil, zero value otherwise.

### GetAvsCodeOk

`func (o *PreviousTransaction) GetAvsCodeOk() (*string, bool)`

GetAvsCodeOk returns a tuple with the AvsCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAvsCode

`func (o *PreviousTransaction) SetAvsCode(v string)`

SetAvsCode sets AvsCode field to given value.

### HasAvsCode

`func (o *PreviousTransaction) HasAvsCode() bool`

HasAvsCode returns a boolean if a field has been set.

### SetAvsCodeNil

`func (o *PreviousTransaction) SetAvsCodeNil(b bool)`

 SetAvsCodeNil sets the value for AvsCode to be an explicit nil

### UnsetAvsCode
`func (o *PreviousTransaction) UnsetAvsCode()`

UnsetAvsCode ensures that no value is present for AvsCode, not even an explicit nil
### GetAvsMessage

`func (o *PreviousTransaction) GetAvsMessage() string`

GetAvsMessage returns the AvsMessage field if non-nil, zero value otherwise.

### GetAvsMessageOk

`func (o *PreviousTransaction) GetAvsMessageOk() (*string, bool)`

GetAvsMessageOk returns a tuple with the AvsMessage field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAvsMessage

`func (o *PreviousTransaction) SetAvsMessage(v string)`

SetAvsMessage sets AvsMessage field to given value.

### HasAvsMessage

`func (o *PreviousTransaction) HasAvsMessage() bool`

HasAvsMessage returns a boolean if a field has been set.

### SetAvsMessageNil

`func (o *PreviousTransaction) SetAvsMessageNil(b bool)`

 SetAvsMessageNil sets the value for AvsMessage to be an explicit nil

### UnsetAvsMessage
`func (o *PreviousTransaction) UnsetAvsMessage()`

UnsetAvsMessage ensures that no value is present for AvsMessage, not even an explicit nil
### GetCvvCode

`func (o *PreviousTransaction) GetCvvCode() string`

GetCvvCode returns the CvvCode field if non-nil, zero value otherwise.

### GetCvvCodeOk

`func (o *PreviousTransaction) GetCvvCodeOk() (*string, bool)`

GetCvvCodeOk returns a tuple with the CvvCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCvvCode

`func (o *PreviousTransaction) SetCvvCode(v string)`

SetCvvCode sets CvvCode field to given value.

### HasCvvCode

`func (o *PreviousTransaction) HasCvvCode() bool`

HasCvvCode returns a boolean if a field has been set.

### SetCvvCodeNil

`func (o *PreviousTransaction) SetCvvCodeNil(b bool)`

 SetCvvCodeNil sets the value for CvvCode to be an explicit nil

### UnsetCvvCode
`func (o *PreviousTransaction) UnsetCvvCode()`

UnsetCvvCode ensures that no value is present for CvvCode, not even an explicit nil
### GetCvvMessage

`func (o *PreviousTransaction) GetCvvMessage() string`

GetCvvMessage returns the CvvMessage field if non-nil, zero value otherwise.

### GetCvvMessageOk

`func (o *PreviousTransaction) GetCvvMessageOk() (*string, bool)`

GetCvvMessageOk returns a tuple with the CvvMessage field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCvvMessage

`func (o *PreviousTransaction) SetCvvMessage(v string)`

SetCvvMessage sets CvvMessage field to given value.

### HasCvvMessage

`func (o *PreviousTransaction) HasCvvMessage() bool`

HasCvvMessage returns a boolean if a field has been set.

### SetCvvMessageNil

`func (o *PreviousTransaction) SetCvvMessageNil(b bool)`

 SetCvvMessageNil sets the value for CvvMessage to be an explicit nil

### UnsetCvvMessage
`func (o *PreviousTransaction) UnsetCvvMessage()`

UnsetCvvMessage ensures that no value is present for CvvMessage, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


