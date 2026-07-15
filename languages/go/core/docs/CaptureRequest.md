# CaptureRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this capture transaction | 
**Amount** | Pointer to **NullableInt64** | Capture amount in smallest currency unit (e.g., cents for USD). If null or omitted, the full authorized amount will be captured.  | [optional] 

## Methods

### NewCaptureRequest

`func NewCaptureRequest(merchantTransactionId string, ) *CaptureRequest`

NewCaptureRequest instantiates a new CaptureRequest object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewCaptureRequestWithDefaults

`func NewCaptureRequestWithDefaults() *CaptureRequest`

NewCaptureRequestWithDefaults instantiates a new CaptureRequest object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetMerchantTransactionId

`func (o *CaptureRequest) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *CaptureRequest) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *CaptureRequest) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.


### GetAmount

`func (o *CaptureRequest) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *CaptureRequest) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *CaptureRequest) SetAmount(v int64)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *CaptureRequest) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *CaptureRequest) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *CaptureRequest) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


