# StoredCredentialResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ReasonType** | Pointer to [**NullableStoredCredentialReasonType**](StoredCredentialReasonType.md) |  | [optional] 
**InitialNetworkTransactionId** | Pointer to **NullableString** | Network transaction ID from the initial transaction that established the stored credential, returned by the gateway | [optional] 
**LatestNetworkTransactionId** | Pointer to **NullableString** | Network transaction ID from the most recent transaction using this stored credential, returned by the gateway | [optional] 
**GatewayInitialTransactionId** | Pointer to **NullableString** | Gateway&#39;s own transaction ID from the initial transaction that established the stored credential | [optional] 
**GatewayLatestTransactionId** | Pointer to **NullableString** | Gateway&#39;s own transaction ID from the most recent transaction using this stored credential | [optional] 

## Methods

### NewStoredCredentialResponse

`func NewStoredCredentialResponse() *StoredCredentialResponse`

NewStoredCredentialResponse instantiates a new StoredCredentialResponse object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewStoredCredentialResponseWithDefaults

`func NewStoredCredentialResponseWithDefaults() *StoredCredentialResponse`

NewStoredCredentialResponseWithDefaults instantiates a new StoredCredentialResponse object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetReasonType

`func (o *StoredCredentialResponse) GetReasonType() StoredCredentialReasonType`

GetReasonType returns the ReasonType field if non-nil, zero value otherwise.

### GetReasonTypeOk

`func (o *StoredCredentialResponse) GetReasonTypeOk() (*StoredCredentialReasonType, bool)`

GetReasonTypeOk returns a tuple with the ReasonType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetReasonType

`func (o *StoredCredentialResponse) SetReasonType(v StoredCredentialReasonType)`

SetReasonType sets ReasonType field to given value.

### HasReasonType

`func (o *StoredCredentialResponse) HasReasonType() bool`

HasReasonType returns a boolean if a field has been set.

### SetReasonTypeNil

`func (o *StoredCredentialResponse) SetReasonTypeNil(b bool)`

 SetReasonTypeNil sets the value for ReasonType to be an explicit nil

### UnsetReasonType
`func (o *StoredCredentialResponse) UnsetReasonType()`

UnsetReasonType ensures that no value is present for ReasonType, not even an explicit nil
### GetInitialNetworkTransactionId

`func (o *StoredCredentialResponse) GetInitialNetworkTransactionId() string`

GetInitialNetworkTransactionId returns the InitialNetworkTransactionId field if non-nil, zero value otherwise.

### GetInitialNetworkTransactionIdOk

`func (o *StoredCredentialResponse) GetInitialNetworkTransactionIdOk() (*string, bool)`

GetInitialNetworkTransactionIdOk returns a tuple with the InitialNetworkTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInitialNetworkTransactionId

`func (o *StoredCredentialResponse) SetInitialNetworkTransactionId(v string)`

SetInitialNetworkTransactionId sets InitialNetworkTransactionId field to given value.

### HasInitialNetworkTransactionId

`func (o *StoredCredentialResponse) HasInitialNetworkTransactionId() bool`

HasInitialNetworkTransactionId returns a boolean if a field has been set.

### SetInitialNetworkTransactionIdNil

`func (o *StoredCredentialResponse) SetInitialNetworkTransactionIdNil(b bool)`

 SetInitialNetworkTransactionIdNil sets the value for InitialNetworkTransactionId to be an explicit nil

### UnsetInitialNetworkTransactionId
`func (o *StoredCredentialResponse) UnsetInitialNetworkTransactionId()`

UnsetInitialNetworkTransactionId ensures that no value is present for InitialNetworkTransactionId, not even an explicit nil
### GetLatestNetworkTransactionId

`func (o *StoredCredentialResponse) GetLatestNetworkTransactionId() string`

GetLatestNetworkTransactionId returns the LatestNetworkTransactionId field if non-nil, zero value otherwise.

### GetLatestNetworkTransactionIdOk

`func (o *StoredCredentialResponse) GetLatestNetworkTransactionIdOk() (*string, bool)`

GetLatestNetworkTransactionIdOk returns a tuple with the LatestNetworkTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLatestNetworkTransactionId

`func (o *StoredCredentialResponse) SetLatestNetworkTransactionId(v string)`

SetLatestNetworkTransactionId sets LatestNetworkTransactionId field to given value.

### HasLatestNetworkTransactionId

`func (o *StoredCredentialResponse) HasLatestNetworkTransactionId() bool`

HasLatestNetworkTransactionId returns a boolean if a field has been set.

### SetLatestNetworkTransactionIdNil

`func (o *StoredCredentialResponse) SetLatestNetworkTransactionIdNil(b bool)`

 SetLatestNetworkTransactionIdNil sets the value for LatestNetworkTransactionId to be an explicit nil

### UnsetLatestNetworkTransactionId
`func (o *StoredCredentialResponse) UnsetLatestNetworkTransactionId()`

UnsetLatestNetworkTransactionId ensures that no value is present for LatestNetworkTransactionId, not even an explicit nil
### GetGatewayInitialTransactionId

`func (o *StoredCredentialResponse) GetGatewayInitialTransactionId() string`

GetGatewayInitialTransactionId returns the GatewayInitialTransactionId field if non-nil, zero value otherwise.

### GetGatewayInitialTransactionIdOk

`func (o *StoredCredentialResponse) GetGatewayInitialTransactionIdOk() (*string, bool)`

GetGatewayInitialTransactionIdOk returns a tuple with the GatewayInitialTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayInitialTransactionId

`func (o *StoredCredentialResponse) SetGatewayInitialTransactionId(v string)`

SetGatewayInitialTransactionId sets GatewayInitialTransactionId field to given value.

### HasGatewayInitialTransactionId

`func (o *StoredCredentialResponse) HasGatewayInitialTransactionId() bool`

HasGatewayInitialTransactionId returns a boolean if a field has been set.

### SetGatewayInitialTransactionIdNil

`func (o *StoredCredentialResponse) SetGatewayInitialTransactionIdNil(b bool)`

 SetGatewayInitialTransactionIdNil sets the value for GatewayInitialTransactionId to be an explicit nil

### UnsetGatewayInitialTransactionId
`func (o *StoredCredentialResponse) UnsetGatewayInitialTransactionId()`

UnsetGatewayInitialTransactionId ensures that no value is present for GatewayInitialTransactionId, not even an explicit nil
### GetGatewayLatestTransactionId

`func (o *StoredCredentialResponse) GetGatewayLatestTransactionId() string`

GetGatewayLatestTransactionId returns the GatewayLatestTransactionId field if non-nil, zero value otherwise.

### GetGatewayLatestTransactionIdOk

`func (o *StoredCredentialResponse) GetGatewayLatestTransactionIdOk() (*string, bool)`

GetGatewayLatestTransactionIdOk returns a tuple with the GatewayLatestTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayLatestTransactionId

`func (o *StoredCredentialResponse) SetGatewayLatestTransactionId(v string)`

SetGatewayLatestTransactionId sets GatewayLatestTransactionId field to given value.

### HasGatewayLatestTransactionId

`func (o *StoredCredentialResponse) HasGatewayLatestTransactionId() bool`

HasGatewayLatestTransactionId returns a boolean if a field has been set.

### SetGatewayLatestTransactionIdNil

`func (o *StoredCredentialResponse) SetGatewayLatestTransactionIdNil(b bool)`

 SetGatewayLatestTransactionIdNil sets the value for GatewayLatestTransactionId to be an explicit nil

### UnsetGatewayLatestTransactionId
`func (o *StoredCredentialResponse) UnsetGatewayLatestTransactionId()`

UnsetGatewayLatestTransactionId ensures that no value is present for GatewayLatestTransactionId, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


