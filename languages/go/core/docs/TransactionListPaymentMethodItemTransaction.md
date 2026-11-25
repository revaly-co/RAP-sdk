# TransactionListPaymentMethodItemTransaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | **string** | Unique transaction identifier | 
**TransactionDate** | **time.Time** | Date and time when the operation was processed (ISO 8601, UTC) | 
**TransactionStatus** | **int32** | Status of the operation (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | 
**Message** | Pointer to **string** | Human-readable message about the result | [optional] 
**CustomerId** | Pointer to **string** | Customer identifier associated with the operation | [optional] 
**ResponseCode** | Pointer to **string** | Response code from the processing result | [optional] 
**TransactionType** | Pointer to **string** | The payment-method operation: CreateCreditCard, CreateGatewayPaymentMethod, UpdatePaymentMethod, RedactPaymentMethod or RecachePaymentMethod | [optional] 
**PaymentMethod** | Pointer to [**TransactionListPaymentMethod**](TransactionListPaymentMethod.md) |  | [optional] 

## Methods

### NewTransactionListPaymentMethodItemTransaction

`func NewTransactionListPaymentMethodItemTransaction(transactionId string, transactionDate time.Time, transactionStatus int32, ) *TransactionListPaymentMethodItemTransaction`

NewTransactionListPaymentMethodItemTransaction instantiates a new TransactionListPaymentMethodItemTransaction object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewTransactionListPaymentMethodItemTransactionWithDefaults

`func NewTransactionListPaymentMethodItemTransactionWithDefaults() *TransactionListPaymentMethodItemTransaction`

NewTransactionListPaymentMethodItemTransactionWithDefaults instantiates a new TransactionListPaymentMethodItemTransaction object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionId

`func (o *TransactionListPaymentMethodItemTransaction) GetTransactionId() string`

GetTransactionId returns the TransactionId field if non-nil, zero value otherwise.

### GetTransactionIdOk

`func (o *TransactionListPaymentMethodItemTransaction) GetTransactionIdOk() (*string, bool)`

GetTransactionIdOk returns a tuple with the TransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionId

`func (o *TransactionListPaymentMethodItemTransaction) SetTransactionId(v string)`

SetTransactionId sets TransactionId field to given value.


### GetTransactionDate

`func (o *TransactionListPaymentMethodItemTransaction) GetTransactionDate() time.Time`

GetTransactionDate returns the TransactionDate field if non-nil, zero value otherwise.

### GetTransactionDateOk

`func (o *TransactionListPaymentMethodItemTransaction) GetTransactionDateOk() (*time.Time, bool)`

GetTransactionDateOk returns a tuple with the TransactionDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionDate

`func (o *TransactionListPaymentMethodItemTransaction) SetTransactionDate(v time.Time)`

SetTransactionDate sets TransactionDate field to given value.


### GetTransactionStatus

`func (o *TransactionListPaymentMethodItemTransaction) GetTransactionStatus() int32`

GetTransactionStatus returns the TransactionStatus field if non-nil, zero value otherwise.

### GetTransactionStatusOk

`func (o *TransactionListPaymentMethodItemTransaction) GetTransactionStatusOk() (*int32, bool)`

GetTransactionStatusOk returns a tuple with the TransactionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionStatus

`func (o *TransactionListPaymentMethodItemTransaction) SetTransactionStatus(v int32)`

SetTransactionStatus sets TransactionStatus field to given value.


### GetMessage

`func (o *TransactionListPaymentMethodItemTransaction) GetMessage() string`

GetMessage returns the Message field if non-nil, zero value otherwise.

### GetMessageOk

`func (o *TransactionListPaymentMethodItemTransaction) GetMessageOk() (*string, bool)`

GetMessageOk returns a tuple with the Message field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessage

`func (o *TransactionListPaymentMethodItemTransaction) SetMessage(v string)`

SetMessage sets Message field to given value.

### HasMessage

`func (o *TransactionListPaymentMethodItemTransaction) HasMessage() bool`

HasMessage returns a boolean if a field has been set.

### GetCustomerId

`func (o *TransactionListPaymentMethodItemTransaction) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *TransactionListPaymentMethodItemTransaction) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *TransactionListPaymentMethodItemTransaction) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *TransactionListPaymentMethodItemTransaction) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### GetResponseCode

`func (o *TransactionListPaymentMethodItemTransaction) GetResponseCode() string`

GetResponseCode returns the ResponseCode field if non-nil, zero value otherwise.

### GetResponseCodeOk

`func (o *TransactionListPaymentMethodItemTransaction) GetResponseCodeOk() (*string, bool)`

GetResponseCodeOk returns a tuple with the ResponseCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponseCode

`func (o *TransactionListPaymentMethodItemTransaction) SetResponseCode(v string)`

SetResponseCode sets ResponseCode field to given value.

### HasResponseCode

`func (o *TransactionListPaymentMethodItemTransaction) HasResponseCode() bool`

HasResponseCode returns a boolean if a field has been set.

### GetTransactionType

`func (o *TransactionListPaymentMethodItemTransaction) GetTransactionType() string`

GetTransactionType returns the TransactionType field if non-nil, zero value otherwise.

### GetTransactionTypeOk

`func (o *TransactionListPaymentMethodItemTransaction) GetTransactionTypeOk() (*string, bool)`

GetTransactionTypeOk returns a tuple with the TransactionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionType

`func (o *TransactionListPaymentMethodItemTransaction) SetTransactionType(v string)`

SetTransactionType sets TransactionType field to given value.

### HasTransactionType

`func (o *TransactionListPaymentMethodItemTransaction) HasTransactionType() bool`

HasTransactionType returns a boolean if a field has been set.

### GetPaymentMethod

`func (o *TransactionListPaymentMethodItemTransaction) GetPaymentMethod() TransactionListPaymentMethod`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *TransactionListPaymentMethodItemTransaction) GetPaymentMethodOk() (*TransactionListPaymentMethod, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *TransactionListPaymentMethodItemTransaction) SetPaymentMethod(v TransactionListPaymentMethod)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *TransactionListPaymentMethodItemTransaction) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


