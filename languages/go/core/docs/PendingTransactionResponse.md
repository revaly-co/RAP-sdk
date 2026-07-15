# PendingTransactionResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**State** | **string** | Always &#x60;pending&#x60; — discriminates this shape from a completed transaction. | 
**MerchantTransactionId** | **string** | Merchant-provided transaction identifier the intent was recorded under | 
**TransactionType** | Pointer to **NullableString** | Operation the intent was recorded for — \&quot;Charge\&quot; or \&quot;Authorize\&quot; (same vocabulary as TransactionResponse.transactionType). | [optional] 
**ReceivedAt** | Pointer to **NullableTime** | When the platform recorded the payment intent (ISO 8601) | [optional] 

## Methods

### NewPendingTransactionResponse

`func NewPendingTransactionResponse(state string, merchantTransactionId string, ) *PendingTransactionResponse`

NewPendingTransactionResponse instantiates a new PendingTransactionResponse object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewPendingTransactionResponseWithDefaults

`func NewPendingTransactionResponseWithDefaults() *PendingTransactionResponse`

NewPendingTransactionResponseWithDefaults instantiates a new PendingTransactionResponse object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetState

`func (o *PendingTransactionResponse) GetState() string`

GetState returns the State field if non-nil, zero value otherwise.

### GetStateOk

`func (o *PendingTransactionResponse) GetStateOk() (*string, bool)`

GetStateOk returns a tuple with the State field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetState

`func (o *PendingTransactionResponse) SetState(v string)`

SetState sets State field to given value.


### GetMerchantTransactionId

`func (o *PendingTransactionResponse) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *PendingTransactionResponse) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *PendingTransactionResponse) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.


### GetTransactionType

`func (o *PendingTransactionResponse) GetTransactionType() string`

GetTransactionType returns the TransactionType field if non-nil, zero value otherwise.

### GetTransactionTypeOk

`func (o *PendingTransactionResponse) GetTransactionTypeOk() (*string, bool)`

GetTransactionTypeOk returns a tuple with the TransactionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionType

`func (o *PendingTransactionResponse) SetTransactionType(v string)`

SetTransactionType sets TransactionType field to given value.

### HasTransactionType

`func (o *PendingTransactionResponse) HasTransactionType() bool`

HasTransactionType returns a boolean if a field has been set.

### SetTransactionTypeNil

`func (o *PendingTransactionResponse) SetTransactionTypeNil(b bool)`

 SetTransactionTypeNil sets the value for TransactionType to be an explicit nil

### UnsetTransactionType
`func (o *PendingTransactionResponse) UnsetTransactionType()`

UnsetTransactionType ensures that no value is present for TransactionType, not even an explicit nil
### GetReceivedAt

`func (o *PendingTransactionResponse) GetReceivedAt() time.Time`

GetReceivedAt returns the ReceivedAt field if non-nil, zero value otherwise.

### GetReceivedAtOk

`func (o *PendingTransactionResponse) GetReceivedAtOk() (*time.Time, bool)`

GetReceivedAtOk returns a tuple with the ReceivedAt field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetReceivedAt

`func (o *PendingTransactionResponse) SetReceivedAt(v time.Time)`

SetReceivedAt sets ReceivedAt field to given value.

### HasReceivedAt

`func (o *PendingTransactionResponse) HasReceivedAt() bool`

HasReceivedAt returns a boolean if a field has been set.

### SetReceivedAtNil

`func (o *PendingTransactionResponse) SetReceivedAtNil(b bool)`

 SetReceivedAtNil sets the value for ReceivedAt to be an explicit nil

### UnsetReceivedAt
`func (o *PendingTransactionResponse) UnsetReceivedAt()`

UnsetReceivedAt ensures that no value is present for ReceivedAt, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


