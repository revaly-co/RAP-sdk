# ErrorResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Error** | **string** | A human-readable error message describing what went wrong | 
**Details** | Pointer to **interface{}** | Optional additional details about the error; structure varies by error type (may be an object, a string, or null) and is otherwise not part of the contract. Exactly one structured key is documented. A request that the edge firewall blocks in front of the platform is answered with HTTP 403 and an ErrorResponse body whose &#x60;details&#x60; is an object carrying &#x60;edgeRejection&#x60; set to the JSON boolean &#x60;true&#x60; and &#x60;reference&#x60;, the edge tracking reference (the same value as the response&#39;s &#x60;x-azure-ref&#x60; header). &#x60;details.edgeRejection: true&#x60; means that this request did not reach the payment platform. It is a statement about the request, not about the payment: nothing was received or processed, and the merchantTransactionId the request carried was not consumed. The edge serves this body with Content-Type text/html, so parse the body of every 403 as JSON regardless of the content type, and match on &#x60;details.edgeRejection&#x60;, never on the &#x60;error&#x60; sentence. A 403 without the marker, including the platform&#39;s own 403, is an application rejection and is final. &#x60;code&#x60; is absent, as on every 4xx. Per operation, after a 403 carrying the marker: a charge or authorize was never accepted, so either resubmit it with corrected content or fail over to another processor, never both for the same merchantTransactionId, and fail over only when no earlier submission of that id may have reached the platform (otherwise first retrieve its status with the transaction lookup by merchantTransactionId); after failing over, never resubmit that id. A capture, void, refund, refund cancellation, payment-method or notify call is never failed over: confirm the transaction&#39;s state with a lookup, then resubmit the same request once. In every case, never alter cardholder data to get past a block; an unchanged resubmission is blocked again until FlexPay support confirms the reference is cleared, so quote &#x60;details.reference&#x60; to support. | [optional] 
**Code** | Pointer to **string** | Machine-readable safety signal, present on every 5xx error response and never on 4xx responses (the edge firewall&#39;s 403 included; its marker is carried in &#x60;details&#x60;). &#x60;not_processed&#x60; is emitted only when the platform can prove the request was never dispatched to a payment gateway or upstream (for example, the upstream circuit breaker was already open), so the caller may safely fail over without risking a duplicate charge. &#x60;outcome_unknown&#x60; means the request may have reached an upstream and the outcome cannot be proven; reconcile the transaction before retrying. Emission is conservative — any 5xx without a provable determination carries &#x60;outcome_unknown&#x60;. | [optional] 

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


