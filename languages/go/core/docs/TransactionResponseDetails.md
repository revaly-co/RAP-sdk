# TransactionResponseDetails

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**AvsCode** | Pointer to **NullableString** | Address Verification System result code | [optional] 
**AvsMessage** | Pointer to **NullableString** | Address Verification System result message | [optional] 
**CvvCode** | Pointer to **NullableString** | Card Verification Value result code | [optional] 
**CvvMessage** | Pointer to **NullableString** | Card Verification Value result message | [optional] 
**ErrorCode** | Pointer to **NullableString** | Error code if transaction failed | [optional] 
**ErrorDetail** | Pointer to **NullableString** | Detailed error message if transaction failed | [optional] 

## Methods

### NewTransactionResponseDetails

`func NewTransactionResponseDetails() *TransactionResponseDetails`

NewTransactionResponseDetails instantiates a new TransactionResponseDetails object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewTransactionResponseDetailsWithDefaults

`func NewTransactionResponseDetailsWithDefaults() *TransactionResponseDetails`

NewTransactionResponseDetailsWithDefaults instantiates a new TransactionResponseDetails object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetAvsCode

`func (o *TransactionResponseDetails) GetAvsCode() string`

GetAvsCode returns the AvsCode field if non-nil, zero value otherwise.

### GetAvsCodeOk

`func (o *TransactionResponseDetails) GetAvsCodeOk() (*string, bool)`

GetAvsCodeOk returns a tuple with the AvsCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAvsCode

`func (o *TransactionResponseDetails) SetAvsCode(v string)`

SetAvsCode sets AvsCode field to given value.

### HasAvsCode

`func (o *TransactionResponseDetails) HasAvsCode() bool`

HasAvsCode returns a boolean if a field has been set.

### SetAvsCodeNil

`func (o *TransactionResponseDetails) SetAvsCodeNil(b bool)`

 SetAvsCodeNil sets the value for AvsCode to be an explicit nil

### UnsetAvsCode
`func (o *TransactionResponseDetails) UnsetAvsCode()`

UnsetAvsCode ensures that no value is present for AvsCode, not even an explicit nil
### GetAvsMessage

`func (o *TransactionResponseDetails) GetAvsMessage() string`

GetAvsMessage returns the AvsMessage field if non-nil, zero value otherwise.

### GetAvsMessageOk

`func (o *TransactionResponseDetails) GetAvsMessageOk() (*string, bool)`

GetAvsMessageOk returns a tuple with the AvsMessage field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAvsMessage

`func (o *TransactionResponseDetails) SetAvsMessage(v string)`

SetAvsMessage sets AvsMessage field to given value.

### HasAvsMessage

`func (o *TransactionResponseDetails) HasAvsMessage() bool`

HasAvsMessage returns a boolean if a field has been set.

### SetAvsMessageNil

`func (o *TransactionResponseDetails) SetAvsMessageNil(b bool)`

 SetAvsMessageNil sets the value for AvsMessage to be an explicit nil

### UnsetAvsMessage
`func (o *TransactionResponseDetails) UnsetAvsMessage()`

UnsetAvsMessage ensures that no value is present for AvsMessage, not even an explicit nil
### GetCvvCode

`func (o *TransactionResponseDetails) GetCvvCode() string`

GetCvvCode returns the CvvCode field if non-nil, zero value otherwise.

### GetCvvCodeOk

`func (o *TransactionResponseDetails) GetCvvCodeOk() (*string, bool)`

GetCvvCodeOk returns a tuple with the CvvCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCvvCode

`func (o *TransactionResponseDetails) SetCvvCode(v string)`

SetCvvCode sets CvvCode field to given value.

### HasCvvCode

`func (o *TransactionResponseDetails) HasCvvCode() bool`

HasCvvCode returns a boolean if a field has been set.

### SetCvvCodeNil

`func (o *TransactionResponseDetails) SetCvvCodeNil(b bool)`

 SetCvvCodeNil sets the value for CvvCode to be an explicit nil

### UnsetCvvCode
`func (o *TransactionResponseDetails) UnsetCvvCode()`

UnsetCvvCode ensures that no value is present for CvvCode, not even an explicit nil
### GetCvvMessage

`func (o *TransactionResponseDetails) GetCvvMessage() string`

GetCvvMessage returns the CvvMessage field if non-nil, zero value otherwise.

### GetCvvMessageOk

`func (o *TransactionResponseDetails) GetCvvMessageOk() (*string, bool)`

GetCvvMessageOk returns a tuple with the CvvMessage field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCvvMessage

`func (o *TransactionResponseDetails) SetCvvMessage(v string)`

SetCvvMessage sets CvvMessage field to given value.

### HasCvvMessage

`func (o *TransactionResponseDetails) HasCvvMessage() bool`

HasCvvMessage returns a boolean if a field has been set.

### SetCvvMessageNil

`func (o *TransactionResponseDetails) SetCvvMessageNil(b bool)`

 SetCvvMessageNil sets the value for CvvMessage to be an explicit nil

### UnsetCvvMessage
`func (o *TransactionResponseDetails) UnsetCvvMessage()`

UnsetCvvMessage ensures that no value is present for CvvMessage, not even an explicit nil
### GetErrorCode

`func (o *TransactionResponseDetails) GetErrorCode() string`

GetErrorCode returns the ErrorCode field if non-nil, zero value otherwise.

### GetErrorCodeOk

`func (o *TransactionResponseDetails) GetErrorCodeOk() (*string, bool)`

GetErrorCodeOk returns a tuple with the ErrorCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetErrorCode

`func (o *TransactionResponseDetails) SetErrorCode(v string)`

SetErrorCode sets ErrorCode field to given value.

### HasErrorCode

`func (o *TransactionResponseDetails) HasErrorCode() bool`

HasErrorCode returns a boolean if a field has been set.

### SetErrorCodeNil

`func (o *TransactionResponseDetails) SetErrorCodeNil(b bool)`

 SetErrorCodeNil sets the value for ErrorCode to be an explicit nil

### UnsetErrorCode
`func (o *TransactionResponseDetails) UnsetErrorCode()`

UnsetErrorCode ensures that no value is present for ErrorCode, not even an explicit nil
### GetErrorDetail

`func (o *TransactionResponseDetails) GetErrorDetail() string`

GetErrorDetail returns the ErrorDetail field if non-nil, zero value otherwise.

### GetErrorDetailOk

`func (o *TransactionResponseDetails) GetErrorDetailOk() (*string, bool)`

GetErrorDetailOk returns a tuple with the ErrorDetail field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetErrorDetail

`func (o *TransactionResponseDetails) SetErrorDetail(v string)`

SetErrorDetail sets ErrorDetail field to given value.

### HasErrorDetail

`func (o *TransactionResponseDetails) HasErrorDetail() bool`

HasErrorDetail returns a boolean if a field has been set.

### SetErrorDetailNil

`func (o *TransactionResponseDetails) SetErrorDetailNil(b bool)`

 SetErrorDetailNil sets the value for ErrorDetail to be an explicit nil

### UnsetErrorDetail
`func (o *TransactionResponseDetails) UnsetErrorDetail()`

UnsetErrorDetail ensures that no value is present for ErrorDetail, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


