# TransactionGroupResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Transaction** | Pointer to [**TransactionResponse**](TransactionResponse.md) | The transaction matching the supplied id (the record the non-expanded lookup returns). | [optional] 
**Transactions** | Pointer to [**[]TransactionResponse**](TransactionResponse.md) | Every transaction in the payment, ordered by transaction date ascending. Capped at 100. | [optional] 

## Methods

### NewTransactionGroupResponse

`func NewTransactionGroupResponse() *TransactionGroupResponse`

NewTransactionGroupResponse instantiates a new TransactionGroupResponse object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewTransactionGroupResponseWithDefaults

`func NewTransactionGroupResponseWithDefaults() *TransactionGroupResponse`

NewTransactionGroupResponseWithDefaults instantiates a new TransactionGroupResponse object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransaction

`func (o *TransactionGroupResponse) GetTransaction() TransactionResponse`

GetTransaction returns the Transaction field if non-nil, zero value otherwise.

### GetTransactionOk

`func (o *TransactionGroupResponse) GetTransactionOk() (*TransactionResponse, bool)`

GetTransactionOk returns a tuple with the Transaction field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransaction

`func (o *TransactionGroupResponse) SetTransaction(v TransactionResponse)`

SetTransaction sets Transaction field to given value.

### HasTransaction

`func (o *TransactionGroupResponse) HasTransaction() bool`

HasTransaction returns a boolean if a field has been set.

### GetTransactions

`func (o *TransactionGroupResponse) GetTransactions() []TransactionResponse`

GetTransactions returns the Transactions field if non-nil, zero value otherwise.

### GetTransactionsOk

`func (o *TransactionGroupResponse) GetTransactionsOk() (*[]TransactionResponse, bool)`

GetTransactionsOk returns a tuple with the Transactions field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactions

`func (o *TransactionGroupResponse) SetTransactions(v []TransactionResponse)`

SetTransactions sets Transactions field to given value.

### HasTransactions

`func (o *TransactionGroupResponse) HasTransactions() bool`

HasTransactions returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


