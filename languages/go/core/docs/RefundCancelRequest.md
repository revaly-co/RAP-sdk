# RefundCancelRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this refund/cancel transaction | 
**Amount** | Pointer to **NullableInt64** | Refund amount in smallest currency unit (e.g., cents for USD). If null or omitted, a full refund will be processed.  | [optional] 
**CustomerId** | **string** | Unique identifier of the customer associated with this transaction | 

## Methods

### NewRefundCancelRequest

`func NewRefundCancelRequest(merchantTransactionId string, customerId string, ) *RefundCancelRequest`

NewRefundCancelRequest instantiates a new RefundCancelRequest object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRefundCancelRequestWithDefaults

`func NewRefundCancelRequestWithDefaults() *RefundCancelRequest`

NewRefundCancelRequestWithDefaults instantiates a new RefundCancelRequest object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetMerchantTransactionId

`func (o *RefundCancelRequest) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *RefundCancelRequest) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *RefundCancelRequest) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.


### GetAmount

`func (o *RefundCancelRequest) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *RefundCancelRequest) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *RefundCancelRequest) SetAmount(v int64)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *RefundCancelRequest) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *RefundCancelRequest) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *RefundCancelRequest) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil
### GetCustomerId

`func (o *RefundCancelRequest) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *RefundCancelRequest) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *RefundCancelRequest) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.



[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


