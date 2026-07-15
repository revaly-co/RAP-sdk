# NotifyResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Success** | Pointer to **bool** | Indicates whether the notification was processed successfully | [optional] 
**Message** | Pointer to **NullableString** | Human-readable message about the notification processing result | [optional] 

## Methods

### NewNotifyResponse

`func NewNotifyResponse() *NotifyResponse`

NewNotifyResponse instantiates a new NotifyResponse object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewNotifyResponseWithDefaults

`func NewNotifyResponseWithDefaults() *NotifyResponse`

NewNotifyResponseWithDefaults instantiates a new NotifyResponse object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetSuccess

`func (o *NotifyResponse) GetSuccess() bool`

GetSuccess returns the Success field if non-nil, zero value otherwise.

### GetSuccessOk

`func (o *NotifyResponse) GetSuccessOk() (*bool, bool)`

GetSuccessOk returns a tuple with the Success field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSuccess

`func (o *NotifyResponse) SetSuccess(v bool)`

SetSuccess sets Success field to given value.

### HasSuccess

`func (o *NotifyResponse) HasSuccess() bool`

HasSuccess returns a boolean if a field has been set.

### GetMessage

`func (o *NotifyResponse) GetMessage() string`

GetMessage returns the Message field if non-nil, zero value otherwise.

### GetMessageOk

`func (o *NotifyResponse) GetMessageOk() (*string, bool)`

GetMessageOk returns a tuple with the Message field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessage

`func (o *NotifyResponse) SetMessage(v string)`

SetMessage sets Message field to given value.

### HasMessage

`func (o *NotifyResponse) HasMessage() bool`

HasMessage returns a boolean if a field has been set.

### SetMessageNil

`func (o *NotifyResponse) SetMessageNil(b bool)`

 SetMessageNil sets the value for Message to be an explicit nil

### UnsetMessage
`func (o *NotifyResponse) UnsetMessage()`

UnsetMessage ensures that no value is present for Message, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


