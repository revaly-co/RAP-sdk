# VoidRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this void transaction | 

## Methods

### NewVoidRequest

`func NewVoidRequest(merchantTransactionId string, ) *VoidRequest`

NewVoidRequest instantiates a new VoidRequest object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewVoidRequestWithDefaults

`func NewVoidRequestWithDefaults() *VoidRequest`

NewVoidRequestWithDefaults instantiates a new VoidRequest object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetMerchantTransactionId

`func (o *VoidRequest) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *VoidRequest) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *VoidRequest) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.



[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


