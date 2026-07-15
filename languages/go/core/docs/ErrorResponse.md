# ErrorResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Error** | **string** | A human-readable error message describing what went wrong | 
**Details** | Pointer to **interface{}** | Optional additional details about the error; structure varies by error type (may be an object, a string, or null) | [optional] 
**Code** | Pointer to **string** | Machine-readable safety signal, present on every 5xx error response and never on 4xx responses. &#x60;not_processed&#x60; is emitted only when the platform can prove the request was never dispatched to a payment gateway or upstream (for example, the upstream circuit breaker was already open), so the caller may safely fail over without risking a duplicate charge. &#x60;outcome_unknown&#x60; means the request may have reached an upstream and the outcome cannot be proven; reconcile the transaction before retrying. Emission is conservative — any 5xx without a provable determination carries &#x60;outcome_unknown&#x60;. | [optional] 

## Methods

### NewErrorResponse

`func NewErrorResponse(error_ string, ) *ErrorResponse`

NewErrorResponse instantiates a new ErrorResponse object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewErrorResponseWithDefaults

`func NewErrorResponseWithDefaults() *ErrorResponse`

NewErrorResponseWithDefaults instantiates a new ErrorResponse object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetError

`func (o *ErrorResponse) GetError() string`

GetError returns the Error field if non-nil, zero value otherwise.

### GetErrorOk

`func (o *ErrorResponse) GetErrorOk() (*string, bool)`

GetErrorOk returns a tuple with the Error field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetError

`func (o *ErrorResponse) SetError(v string)`

SetError sets Error field to given value.


### GetDetails

`func (o *ErrorResponse) GetDetails() interface{}`

GetDetails returns the Details field if non-nil, zero value otherwise.

### GetDetailsOk

`func (o *ErrorResponse) GetDetailsOk() (*interface{}, bool)`

GetDetailsOk returns a tuple with the Details field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDetails

`func (o *ErrorResponse) SetDetails(v interface{})`

SetDetails sets Details field to given value.

### HasDetails

`func (o *ErrorResponse) HasDetails() bool`

HasDetails returns a boolean if a field has been set.

### SetDetailsNil

`func (o *ErrorResponse) SetDetailsNil(b bool)`

 SetDetailsNil sets the value for Details to be an explicit nil

### UnsetDetails
`func (o *ErrorResponse) UnsetDetails()`

UnsetDetails ensures that no value is present for Details, not even an explicit nil
### GetCode

`func (o *ErrorResponse) GetCode() string`

GetCode returns the Code field if non-nil, zero value otherwise.

### GetCodeOk

`func (o *ErrorResponse) GetCodeOk() (*string, bool)`

GetCodeOk returns a tuple with the Code field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCode

`func (o *ErrorResponse) SetCode(v string)`

SetCode sets Code field to given value.

### HasCode

`func (o *ErrorResponse) HasCode() bool`

HasCode returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


