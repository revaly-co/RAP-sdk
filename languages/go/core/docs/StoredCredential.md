# StoredCredential

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ReasonType** | Pointer to [**NullableStoredCredentialReasonType**](StoredCredentialReasonType.md) |  | [optional] 
**InitialNetworkTransactionId** | Pointer to **NullableString** | Network transaction ID from the initial transaction that established the stored credential | [optional] 
**LatestNetworkTransactionId** | Pointer to **NullableString** | Network transaction ID from the most recent transaction using this stored credential | [optional] 
**InitialGatewayTransactionId** | Pointer to **NullableString** | Gateway transaction ID from the initial transaction that established the stored credential | [optional] 
**LatestGatewayTransactionId** | Pointer to **NullableString** | Gateway transaction ID from the most recent transaction using this stored credential | [optional] 

## Methods

### NewStoredCredential

`func NewStoredCredential() *StoredCredential`

NewStoredCredential instantiates a new StoredCredential object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewStoredCredentialWithDefaults

`func NewStoredCredentialWithDefaults() *StoredCredential`

NewStoredCredentialWithDefaults instantiates a new StoredCredential object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetReasonType

`func (o *StoredCredential) GetReasonType() StoredCredentialReasonType`

GetReasonType returns the ReasonType field if non-nil, zero value otherwise.

### GetReasonTypeOk

`func (o *StoredCredential) GetReasonTypeOk() (*StoredCredentialReasonType, bool)`

GetReasonTypeOk returns a tuple with the ReasonType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetReasonType

`func (o *StoredCredential) SetReasonType(v StoredCredentialReasonType)`

SetReasonType sets ReasonType field to given value.

### HasReasonType

`func (o *StoredCredential) HasReasonType() bool`

HasReasonType returns a boolean if a field has been set.

### SetReasonTypeNil

`func (o *StoredCredential) SetReasonTypeNil(b bool)`

 SetReasonTypeNil sets the value for ReasonType to be an explicit nil

### UnsetReasonType
`func (o *StoredCredential) UnsetReasonType()`

UnsetReasonType ensures that no value is present for ReasonType, not even an explicit nil
### GetInitialNetworkTransactionId

`func (o *StoredCredential) GetInitialNetworkTransactionId() string`

GetInitialNetworkTransactionId returns the InitialNetworkTransactionId field if non-nil, zero value otherwise.

### GetInitialNetworkTransactionIdOk

`func (o *StoredCredential) GetInitialNetworkTransactionIdOk() (*string, bool)`

GetInitialNetworkTransactionIdOk returns a tuple with the InitialNetworkTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInitialNetworkTransactionId

`func (o *StoredCredential) SetInitialNetworkTransactionId(v string)`

SetInitialNetworkTransactionId sets InitialNetworkTransactionId field to given value.

### HasInitialNetworkTransactionId

`func (o *StoredCredential) HasInitialNetworkTransactionId() bool`

HasInitialNetworkTransactionId returns a boolean if a field has been set.

### SetInitialNetworkTransactionIdNil

`func (o *StoredCredential) SetInitialNetworkTransactionIdNil(b bool)`

 SetInitialNetworkTransactionIdNil sets the value for InitialNetworkTransactionId to be an explicit nil

### UnsetInitialNetworkTransactionId
`func (o *StoredCredential) UnsetInitialNetworkTransactionId()`

UnsetInitialNetworkTransactionId ensures that no value is present for InitialNetworkTransactionId, not even an explicit nil
### GetLatestNetworkTransactionId

`func (o *StoredCredential) GetLatestNetworkTransactionId() string`

GetLatestNetworkTransactionId returns the LatestNetworkTransactionId field if non-nil, zero value otherwise.

### GetLatestNetworkTransactionIdOk

`func (o *StoredCredential) GetLatestNetworkTransactionIdOk() (*string, bool)`

GetLatestNetworkTransactionIdOk returns a tuple with the LatestNetworkTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLatestNetworkTransactionId

`func (o *StoredCredential) SetLatestNetworkTransactionId(v string)`

SetLatestNetworkTransactionId sets LatestNetworkTransactionId field to given value.

### HasLatestNetworkTransactionId

`func (o *StoredCredential) HasLatestNetworkTransactionId() bool`

HasLatestNetworkTransactionId returns a boolean if a field has been set.

### SetLatestNetworkTransactionIdNil

`func (o *StoredCredential) SetLatestNetworkTransactionIdNil(b bool)`

 SetLatestNetworkTransactionIdNil sets the value for LatestNetworkTransactionId to be an explicit nil

### UnsetLatestNetworkTransactionId
`func (o *StoredCredential) UnsetLatestNetworkTransactionId()`

UnsetLatestNetworkTransactionId ensures that no value is present for LatestNetworkTransactionId, not even an explicit nil
### GetInitialGatewayTransactionId

`func (o *StoredCredential) GetInitialGatewayTransactionId() string`

GetInitialGatewayTransactionId returns the InitialGatewayTransactionId field if non-nil, zero value otherwise.

### GetInitialGatewayTransactionIdOk

`func (o *StoredCredential) GetInitialGatewayTransactionIdOk() (*string, bool)`

GetInitialGatewayTransactionIdOk returns a tuple with the InitialGatewayTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInitialGatewayTransactionId

`func (o *StoredCredential) SetInitialGatewayTransactionId(v string)`

SetInitialGatewayTransactionId sets InitialGatewayTransactionId field to given value.

### HasInitialGatewayTransactionId

`func (o *StoredCredential) HasInitialGatewayTransactionId() bool`

HasInitialGatewayTransactionId returns a boolean if a field has been set.

### SetInitialGatewayTransactionIdNil

`func (o *StoredCredential) SetInitialGatewayTransactionIdNil(b bool)`

 SetInitialGatewayTransactionIdNil sets the value for InitialGatewayTransactionId to be an explicit nil

### UnsetInitialGatewayTransactionId
`func (o *StoredCredential) UnsetInitialGatewayTransactionId()`

UnsetInitialGatewayTransactionId ensures that no value is present for InitialGatewayTransactionId, not even an explicit nil
### GetLatestGatewayTransactionId

`func (o *StoredCredential) GetLatestGatewayTransactionId() string`

GetLatestGatewayTransactionId returns the LatestGatewayTransactionId field if non-nil, zero value otherwise.

### GetLatestGatewayTransactionIdOk

`func (o *StoredCredential) GetLatestGatewayTransactionIdOk() (*string, bool)`

GetLatestGatewayTransactionIdOk returns a tuple with the LatestGatewayTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLatestGatewayTransactionId

`func (o *StoredCredential) SetLatestGatewayTransactionId(v string)`

SetLatestGatewayTransactionId sets LatestGatewayTransactionId field to given value.

### HasLatestGatewayTransactionId

`func (o *StoredCredential) HasLatestGatewayTransactionId() bool`

HasLatestGatewayTransactionId returns a boolean if a field has been set.

### SetLatestGatewayTransactionIdNil

`func (o *StoredCredential) SetLatestGatewayTransactionIdNil(b bool)`

 SetLatestGatewayTransactionIdNil sets the value for LatestGatewayTransactionId to be an explicit nil

### UnsetLatestGatewayTransactionId
`func (o *StoredCredential) UnsetLatestGatewayTransactionId()`

UnsetLatestGatewayTransactionId ensures that no value is present for LatestGatewayTransactionId, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


