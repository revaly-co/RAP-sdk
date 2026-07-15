# CreatePaymentMethodRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PaymentMethodType** | **string** | Type of payment method to create: - **creditCard**: Use raw credit card details that will be tokenized - **gatewayPaymentMethodId**: Use an existing token from a supported payment gateway  | 
**CustomerId** | Pointer to **NullableString** | Unique identifier for the customer | [optional] 
**PaymentMethod** | Pointer to [**PaymentMethod**](PaymentMethod.md) |  | [optional] 

## Methods

### NewCreatePaymentMethodRequest

`func NewCreatePaymentMethodRequest(paymentMethodType string, ) *CreatePaymentMethodRequest`

NewCreatePaymentMethodRequest instantiates a new CreatePaymentMethodRequest object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewCreatePaymentMethodRequestWithDefaults

`func NewCreatePaymentMethodRequestWithDefaults() *CreatePaymentMethodRequest`

NewCreatePaymentMethodRequestWithDefaults instantiates a new CreatePaymentMethodRequest object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetPaymentMethodType

`func (o *CreatePaymentMethodRequest) GetPaymentMethodType() string`

GetPaymentMethodType returns the PaymentMethodType field if non-nil, zero value otherwise.

### GetPaymentMethodTypeOk

`func (o *CreatePaymentMethodRequest) GetPaymentMethodTypeOk() (*string, bool)`

GetPaymentMethodTypeOk returns a tuple with the PaymentMethodType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodType

`func (o *CreatePaymentMethodRequest) SetPaymentMethodType(v string)`

SetPaymentMethodType sets PaymentMethodType field to given value.


### GetCustomerId

`func (o *CreatePaymentMethodRequest) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *CreatePaymentMethodRequest) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *CreatePaymentMethodRequest) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *CreatePaymentMethodRequest) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *CreatePaymentMethodRequest) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *CreatePaymentMethodRequest) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetPaymentMethod

`func (o *CreatePaymentMethodRequest) GetPaymentMethod() PaymentMethod`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *CreatePaymentMethodRequest) GetPaymentMethodOk() (*PaymentMethod, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *CreatePaymentMethodRequest) SetPaymentMethod(v PaymentMethod)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *CreatePaymentMethodRequest) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


