# PaymentMethodWriteResponseTransaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | Pointer to **NullableString** | Unique identifier for the transaction | [optional] 
**TransactionDate** | Pointer to **NullableTime** | Date and time when the transaction was processed | [optional] 
**TransactionStatus** | Pointer to **NullableInt32** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**Message** | Pointer to **NullableString** | Human-readable message about the transaction | [optional] 
**ResponseCode** | Pointer to **NullableString** | Gateway response code | [optional] 
**TransactionType** | Pointer to **NullableString** | Type of transaction | [optional] 

## Methods

### NewPaymentMethodWriteResponseTransaction

`func NewPaymentMethodWriteResponseTransaction() *PaymentMethodWriteResponseTransaction`

NewPaymentMethodWriteResponseTransaction instantiates a new PaymentMethodWriteResponseTransaction object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewPaymentMethodWriteResponseTransactionWithDefaults

`func NewPaymentMethodWriteResponseTransactionWithDefaults() *PaymentMethodWriteResponseTransaction`

NewPaymentMethodWriteResponseTransactionWithDefaults instantiates a new PaymentMethodWriteResponseTransaction object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionId

`func (o *PaymentMethodWriteResponseTransaction) GetTransactionId() string`

GetTransactionId returns the TransactionId field if non-nil, zero value otherwise.

### GetTransactionIdOk

`func (o *PaymentMethodWriteResponseTransaction) GetTransactionIdOk() (*string, bool)`

GetTransactionIdOk returns a tuple with the TransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionId

`func (o *PaymentMethodWriteResponseTransaction) SetTransactionId(v string)`

SetTransactionId sets TransactionId field to given value.

### HasTransactionId

`func (o *PaymentMethodWriteResponseTransaction) HasTransactionId() bool`

HasTransactionId returns a boolean if a field has been set.

### SetTransactionIdNil

`func (o *PaymentMethodWriteResponseTransaction) SetTransactionIdNil(b bool)`

 SetTransactionIdNil sets the value for TransactionId to be an explicit nil

### UnsetTransactionId
`func (o *PaymentMethodWriteResponseTransaction) UnsetTransactionId()`

UnsetTransactionId ensures that no value is present for TransactionId, not even an explicit nil
### GetTransactionDate

`func (o *PaymentMethodWriteResponseTransaction) GetTransactionDate() time.Time`

GetTransactionDate returns the TransactionDate field if non-nil, zero value otherwise.

### GetTransactionDateOk

`func (o *PaymentMethodWriteResponseTransaction) GetTransactionDateOk() (*time.Time, bool)`

GetTransactionDateOk returns a tuple with the TransactionDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionDate

`func (o *PaymentMethodWriteResponseTransaction) SetTransactionDate(v time.Time)`

SetTransactionDate sets TransactionDate field to given value.

### HasTransactionDate

`func (o *PaymentMethodWriteResponseTransaction) HasTransactionDate() bool`

HasTransactionDate returns a boolean if a field has been set.

### SetTransactionDateNil

`func (o *PaymentMethodWriteResponseTransaction) SetTransactionDateNil(b bool)`

 SetTransactionDateNil sets the value for TransactionDate to be an explicit nil

### UnsetTransactionDate
`func (o *PaymentMethodWriteResponseTransaction) UnsetTransactionDate()`

UnsetTransactionDate ensures that no value is present for TransactionDate, not even an explicit nil
### GetTransactionStatus

`func (o *PaymentMethodWriteResponseTransaction) GetTransactionStatus() int32`

GetTransactionStatus returns the TransactionStatus field if non-nil, zero value otherwise.

### GetTransactionStatusOk

`func (o *PaymentMethodWriteResponseTransaction) GetTransactionStatusOk() (*int32, bool)`

GetTransactionStatusOk returns a tuple with the TransactionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionStatus

`func (o *PaymentMethodWriteResponseTransaction) SetTransactionStatus(v int32)`

SetTransactionStatus sets TransactionStatus field to given value.

### HasTransactionStatus

`func (o *PaymentMethodWriteResponseTransaction) HasTransactionStatus() bool`

HasTransactionStatus returns a boolean if a field has been set.

### SetTransactionStatusNil

`func (o *PaymentMethodWriteResponseTransaction) SetTransactionStatusNil(b bool)`

 SetTransactionStatusNil sets the value for TransactionStatus to be an explicit nil

### UnsetTransactionStatus
`func (o *PaymentMethodWriteResponseTransaction) UnsetTransactionStatus()`

UnsetTransactionStatus ensures that no value is present for TransactionStatus, not even an explicit nil
### GetMessage

`func (o *PaymentMethodWriteResponseTransaction) GetMessage() string`

GetMessage returns the Message field if non-nil, zero value otherwise.

### GetMessageOk

`func (o *PaymentMethodWriteResponseTransaction) GetMessageOk() (*string, bool)`

GetMessageOk returns a tuple with the Message field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessage

`func (o *PaymentMethodWriteResponseTransaction) SetMessage(v string)`

SetMessage sets Message field to given value.

### HasMessage

`func (o *PaymentMethodWriteResponseTransaction) HasMessage() bool`

HasMessage returns a boolean if a field has been set.

### SetMessageNil

`func (o *PaymentMethodWriteResponseTransaction) SetMessageNil(b bool)`

 SetMessageNil sets the value for Message to be an explicit nil

### UnsetMessage
`func (o *PaymentMethodWriteResponseTransaction) UnsetMessage()`

UnsetMessage ensures that no value is present for Message, not even an explicit nil
### GetResponseCode

`func (o *PaymentMethodWriteResponseTransaction) GetResponseCode() string`

GetResponseCode returns the ResponseCode field if non-nil, zero value otherwise.

### GetResponseCodeOk

`func (o *PaymentMethodWriteResponseTransaction) GetResponseCodeOk() (*string, bool)`

GetResponseCodeOk returns a tuple with the ResponseCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponseCode

`func (o *PaymentMethodWriteResponseTransaction) SetResponseCode(v string)`

SetResponseCode sets ResponseCode field to given value.

### HasResponseCode

`func (o *PaymentMethodWriteResponseTransaction) HasResponseCode() bool`

HasResponseCode returns a boolean if a field has been set.

### SetResponseCodeNil

`func (o *PaymentMethodWriteResponseTransaction) SetResponseCodeNil(b bool)`

 SetResponseCodeNil sets the value for ResponseCode to be an explicit nil

### UnsetResponseCode
`func (o *PaymentMethodWriteResponseTransaction) UnsetResponseCode()`

UnsetResponseCode ensures that no value is present for ResponseCode, not even an explicit nil
### GetTransactionType

`func (o *PaymentMethodWriteResponseTransaction) GetTransactionType() string`

GetTransactionType returns the TransactionType field if non-nil, zero value otherwise.

### GetTransactionTypeOk

`func (o *PaymentMethodWriteResponseTransaction) GetTransactionTypeOk() (*string, bool)`

GetTransactionTypeOk returns a tuple with the TransactionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionType

`func (o *PaymentMethodWriteResponseTransaction) SetTransactionType(v string)`

SetTransactionType sets TransactionType field to given value.

### HasTransactionType

`func (o *PaymentMethodWriteResponseTransaction) HasTransactionType() bool`

HasTransactionType returns a boolean if a field has been set.

### SetTransactionTypeNil

`func (o *PaymentMethodWriteResponseTransaction) SetTransactionTypeNil(b bool)`

 SetTransactionTypeNil sets the value for TransactionType to be an explicit nil

### UnsetTransactionType
`func (o *PaymentMethodWriteResponseTransaction) UnsetTransactionType()`

UnsetTransactionType ensures that no value is present for TransactionType, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


