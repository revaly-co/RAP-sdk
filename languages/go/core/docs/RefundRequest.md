# RefundRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this refund transaction | 
**Amount** | Pointer to **NullableInt64** | Refund amount in smallest currency unit (e.g., cents for USD). If null or omitted, a full refund will be processed.  | [optional] 

## Methods

### NewRefundRequest

`func NewRefundRequest(merchantTransactionId string, ) *RefundRequest`

NewRefundRequest instantiates a new RefundRequest object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRefundRequestWithDefaults

`func NewRefundRequestWithDefaults() *RefundRequest`

NewRefundRequestWithDefaults instantiates a new RefundRequest object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetMerchantTransactionId

`func (o *RefundRequest) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *RefundRequest) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *RefundRequest) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.


### GetAmount

`func (o *RefundRequest) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *RefundRequest) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *RefundRequest) SetAmount(v int64)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *RefundRequest) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *RefundRequest) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *RefundRequest) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


