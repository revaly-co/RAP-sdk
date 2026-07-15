# TransactionGateway

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Token** | Pointer to **NullableString** | Gateway routing token identifier | [optional] 
**GatewayType** | Pointer to **NullableString** | The type of payment gateway used | [optional] 
**Name** | Pointer to **NullableString** | Human-readable gateway name | [optional] 
**ReferenceId** | Pointer to **NullableString** | Merchant account reference identifier at the gateway | [optional] 

## Methods

### NewTransactionGateway

`func NewTransactionGateway() *TransactionGateway`

NewTransactionGateway instantiates a new TransactionGateway object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewTransactionGatewayWithDefaults

`func NewTransactionGatewayWithDefaults() *TransactionGateway`

NewTransactionGatewayWithDefaults instantiates a new TransactionGateway object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetToken

`func (o *TransactionGateway) GetToken() string`

GetToken returns the Token field if non-nil, zero value otherwise.

### GetTokenOk

`func (o *TransactionGateway) GetTokenOk() (*string, bool)`

GetTokenOk returns a tuple with the Token field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetToken

`func (o *TransactionGateway) SetToken(v string)`

SetToken sets Token field to given value.

### HasToken

`func (o *TransactionGateway) HasToken() bool`

HasToken returns a boolean if a field has been set.

### SetTokenNil

`func (o *TransactionGateway) SetTokenNil(b bool)`

 SetTokenNil sets the value for Token to be an explicit nil

### UnsetToken
`func (o *TransactionGateway) UnsetToken()`

UnsetToken ensures that no value is present for Token, not even an explicit nil
### GetGatewayType

`func (o *TransactionGateway) GetGatewayType() string`

GetGatewayType returns the GatewayType field if non-nil, zero value otherwise.

### GetGatewayTypeOk

`func (o *TransactionGateway) GetGatewayTypeOk() (*string, bool)`

GetGatewayTypeOk returns a tuple with the GatewayType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayType

`func (o *TransactionGateway) SetGatewayType(v string)`

SetGatewayType sets GatewayType field to given value.

### HasGatewayType

`func (o *TransactionGateway) HasGatewayType() bool`

HasGatewayType returns a boolean if a field has been set.

### SetGatewayTypeNil

`func (o *TransactionGateway) SetGatewayTypeNil(b bool)`

 SetGatewayTypeNil sets the value for GatewayType to be an explicit nil

### UnsetGatewayType
`func (o *TransactionGateway) UnsetGatewayType()`

UnsetGatewayType ensures that no value is present for GatewayType, not even an explicit nil
### GetName

`func (o *TransactionGateway) GetName() string`

GetName returns the Name field if non-nil, zero value otherwise.

### GetNameOk

`func (o *TransactionGateway) GetNameOk() (*string, bool)`

GetNameOk returns a tuple with the Name field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetName

`func (o *TransactionGateway) SetName(v string)`

SetName sets Name field to given value.

### HasName

`func (o *TransactionGateway) HasName() bool`

HasName returns a boolean if a field has been set.

### SetNameNil

`func (o *TransactionGateway) SetNameNil(b bool)`

 SetNameNil sets the value for Name to be an explicit nil

### UnsetName
`func (o *TransactionGateway) UnsetName()`

UnsetName ensures that no value is present for Name, not even an explicit nil
### GetReferenceId

`func (o *TransactionGateway) GetReferenceId() string`

GetReferenceId returns the ReferenceId field if non-nil, zero value otherwise.

### GetReferenceIdOk

`func (o *TransactionGateway) GetReferenceIdOk() (*string, bool)`

GetReferenceIdOk returns a tuple with the ReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetReferenceId

`func (o *TransactionGateway) SetReferenceId(v string)`

SetReferenceId sets ReferenceId field to given value.

### HasReferenceId

`func (o *TransactionGateway) HasReferenceId() bool`

HasReferenceId returns a boolean if a field has been set.

### SetReferenceIdNil

`func (o *TransactionGateway) SetReferenceIdNil(b bool)`

 SetReferenceIdNil sets the value for ReferenceId to be an explicit nil

### UnsetReferenceId
`func (o *TransactionGateway) UnsetReferenceId()`

UnsetReferenceId ensures that no value is present for ReferenceId, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


