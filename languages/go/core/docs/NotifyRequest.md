# NotifyRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**EventType** | **string** | Type of business event being reported. The event type determines how Revaly processes the notification.  - **recordPayment**: Record a payment transaction - **recordRefund**: Record a refund transaction - **recordChargeback**: Record a chargeback on a transaction - **endOutreach**: End an outreach campaign for a customer - **updateCustomerData**: Update customer information and contact details  | 
**Data** | Pointer to [**NotifyData**](NotifyData.md) |  | [optional] 

## Methods

### NewNotifyRequest

`func NewNotifyRequest(eventType string, ) *NotifyRequest`

NewNotifyRequest instantiates a new NotifyRequest object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewNotifyRequestWithDefaults

`func NewNotifyRequestWithDefaults() *NotifyRequest`

NewNotifyRequestWithDefaults instantiates a new NotifyRequest object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetEventType

`func (o *NotifyRequest) GetEventType() string`

GetEventType returns the EventType field if non-nil, zero value otherwise.

### GetEventTypeOk

`func (o *NotifyRequest) GetEventTypeOk() (*string, bool)`

GetEventTypeOk returns a tuple with the EventType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEventType

`func (o *NotifyRequest) SetEventType(v string)`

SetEventType sets EventType field to given value.


### GetData

`func (o *NotifyRequest) GetData() NotifyData`

GetData returns the Data field if non-nil, zero value otherwise.

### GetDataOk

`func (o *NotifyRequest) GetDataOk() (*NotifyData, bool)`

GetDataOk returns a tuple with the Data field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetData

`func (o *NotifyRequest) SetData(v NotifyData)`

SetData sets Data field to given value.

### HasData

`func (o *NotifyRequest) HasData() bool`

HasData returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


