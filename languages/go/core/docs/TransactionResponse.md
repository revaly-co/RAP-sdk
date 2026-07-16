# TransactionResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | Pointer to **NullableString** | Unique identifier for the transaction | [optional] 
**TransactionDate** | Pointer to **NullableTime** | Date and time when the transaction was processed (ISO 8601) | [optional] 
**TransactionStatus** | Pointer to **NullableInt32** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**Message** | Pointer to **NullableString** | Human-readable message about the transaction result | [optional] 
**ResponseCode** | Pointer to **NullableString** | Gateway-specific response code | [optional] 
**TransactionType** | Pointer to **NullableString** | Type of transaction performed. Passthrough of the processing platform&#39;s transaction type — not a closed set. Payment operations return \&quot;Charge\&quot;, \&quot;Authorize\&quot;, \&quot;Capture\&quot;, \&quot;Void\&quot; or \&quot;Refund\&quot; (refund cancellation returns \&quot;Refund\&quot;). Transaction lookups can additionally return types created by other platform flows, e.g. \&quot;Verify\&quot;, \&quot;SuccessfulPayment\&quot;, \&quot;RefundedPayment\&quot;, \&quot;CreateCreditCard\&quot;, \&quot;UpdatePaymentMethod\&quot;, \&quot;RedactPaymentMethod\&quot;, \&quot;RecachePaymentMethod\&quot;, \&quot;CreateGatewayPaymentMethod\&quot;. Treat unrecognized values as informational. | [optional] 
**MerchantTransactionId** | Pointer to **NullableString** | Merchant-provided transaction identifier | [optional] 
**CustomerId** | Pointer to **NullableString** | Customer identifier associated with the transaction | [optional] 
**GatewayRoutingId** | Pointer to **NullableString** | Gateway-specific token for the transaction | [optional] 
**Currency** | Pointer to **NullableString** | Transaction currency code (ISO 4217) | [optional] 
**Amount** | Pointer to **NullableInt64** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**GatewayType** | Pointer to **NullableString** | Payment gateway used for processing | [optional] 
**GatewayTransactionId** | Pointer to **NullableString** | Gateway-specific transaction identifier | [optional] 
**AcquirerAuthCode** | Pointer to **NullableString** | Authorization code returned by the acquiring bank or network | [optional] 
**InlineRetryPreviousTransactionId** | Pointer to **NullableString** | Transaction identifier of the inline retry attempt when one was executed | [optional] 
**InlineRetryPreviousMerchantTransactionId** | Pointer to **NullableString** | Original merchant transaction identifier before an inline retry was executed | [optional] 
**IsInlineRetry** | Pointer to **NullableBool** | Indicates that an inline retry attempt occurred | [optional] 
**RetryDate** | Pointer to **NullableTime** | Date for retry attempt (if applicable) | [optional] 
**MitStoredTransactionId** | Pointer to **NullableString** | Merchant-initiated transaction stored credential ID | [optional] 
**StoredCredential** | Pointer to [**NullableStoredCredentialResponse**](StoredCredentialResponse.md) |  | [optional] 
**OrderId** | Pointer to **NullableString** | Order identifier from the merchant system | [optional] 
**StatementDescriptor** | Pointer to **NullableString** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. | [optional] 
**CustomerIp** | Pointer to **NullableString** | Customer&#39;s IP address at time of transaction | [optional] 
**EngagedRecoveryState** | Pointer to **NullableInt32** | Recovery state indicator (0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional] 
**Description** | Pointer to **NullableString** | Transaction description or notes | [optional] 
**GatewayFields** | Pointer to **map[string]interface{}** | Additional gateway-specific fields | [optional] 
**GatewaySpecificResponseFields** | Pointer to **map[string]interface{}** | Additional gateway-specific response details returned directly from the processor | [optional] 
**PaymentPlanData** | Pointer to [**NullablePaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**Recovery** | Pointer to [**NullableRecovery**](Recovery.md) |  | [optional] 
**Response** | Pointer to [**NullableTransactionResponseDetails**](TransactionResponseDetails.md) |  | [optional] 
**PaymentMethod** | Pointer to [**NullablePaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional] 

## Methods

### NewTransactionResponse

`func NewTransactionResponse() *TransactionResponse`

NewTransactionResponse instantiates a new TransactionResponse object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewTransactionResponseWithDefaults

`func NewTransactionResponseWithDefaults() *TransactionResponse`

NewTransactionResponseWithDefaults instantiates a new TransactionResponse object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionId

`func (o *TransactionResponse) GetTransactionId() string`

GetTransactionId returns the TransactionId field if non-nil, zero value otherwise.

### GetTransactionIdOk

`func (o *TransactionResponse) GetTransactionIdOk() (*string, bool)`

GetTransactionIdOk returns a tuple with the TransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionId

`func (o *TransactionResponse) SetTransactionId(v string)`

SetTransactionId sets TransactionId field to given value.

### HasTransactionId

`func (o *TransactionResponse) HasTransactionId() bool`

HasTransactionId returns a boolean if a field has been set.

### SetTransactionIdNil

`func (o *TransactionResponse) SetTransactionIdNil(b bool)`

 SetTransactionIdNil sets the value for TransactionId to be an explicit nil

### UnsetTransactionId
`func (o *TransactionResponse) UnsetTransactionId()`

UnsetTransactionId ensures that no value is present for TransactionId, not even an explicit nil
### GetTransactionDate

`func (o *TransactionResponse) GetTransactionDate() time.Time`

GetTransactionDate returns the TransactionDate field if non-nil, zero value otherwise.

### GetTransactionDateOk

`func (o *TransactionResponse) GetTransactionDateOk() (*time.Time, bool)`

GetTransactionDateOk returns a tuple with the TransactionDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionDate

`func (o *TransactionResponse) SetTransactionDate(v time.Time)`

SetTransactionDate sets TransactionDate field to given value.

### HasTransactionDate

`func (o *TransactionResponse) HasTransactionDate() bool`

HasTransactionDate returns a boolean if a field has been set.

### SetTransactionDateNil

`func (o *TransactionResponse) SetTransactionDateNil(b bool)`

 SetTransactionDateNil sets the value for TransactionDate to be an explicit nil

### UnsetTransactionDate
`func (o *TransactionResponse) UnsetTransactionDate()`

UnsetTransactionDate ensures that no value is present for TransactionDate, not even an explicit nil
### GetTransactionStatus

`func (o *TransactionResponse) GetTransactionStatus() int32`

GetTransactionStatus returns the TransactionStatus field if non-nil, zero value otherwise.

### GetTransactionStatusOk

`func (o *TransactionResponse) GetTransactionStatusOk() (*int32, bool)`

GetTransactionStatusOk returns a tuple with the TransactionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionStatus

`func (o *TransactionResponse) SetTransactionStatus(v int32)`

SetTransactionStatus sets TransactionStatus field to given value.

### HasTransactionStatus

`func (o *TransactionResponse) HasTransactionStatus() bool`

HasTransactionStatus returns a boolean if a field has been set.

### SetTransactionStatusNil

`func (o *TransactionResponse) SetTransactionStatusNil(b bool)`

 SetTransactionStatusNil sets the value for TransactionStatus to be an explicit nil

### UnsetTransactionStatus
`func (o *TransactionResponse) UnsetTransactionStatus()`

UnsetTransactionStatus ensures that no value is present for TransactionStatus, not even an explicit nil
### GetMessage

`func (o *TransactionResponse) GetMessage() string`

GetMessage returns the Message field if non-nil, zero value otherwise.

### GetMessageOk

`func (o *TransactionResponse) GetMessageOk() (*string, bool)`

GetMessageOk returns a tuple with the Message field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessage

`func (o *TransactionResponse) SetMessage(v string)`

SetMessage sets Message field to given value.

### HasMessage

`func (o *TransactionResponse) HasMessage() bool`

HasMessage returns a boolean if a field has been set.

### SetMessageNil

`func (o *TransactionResponse) SetMessageNil(b bool)`

 SetMessageNil sets the value for Message to be an explicit nil

### UnsetMessage
`func (o *TransactionResponse) UnsetMessage()`

UnsetMessage ensures that no value is present for Message, not even an explicit nil
### GetResponseCode

`func (o *TransactionResponse) GetResponseCode() string`

GetResponseCode returns the ResponseCode field if non-nil, zero value otherwise.

### GetResponseCodeOk

`func (o *TransactionResponse) GetResponseCodeOk() (*string, bool)`

GetResponseCodeOk returns a tuple with the ResponseCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponseCode

`func (o *TransactionResponse) SetResponseCode(v string)`

SetResponseCode sets ResponseCode field to given value.

### HasResponseCode

`func (o *TransactionResponse) HasResponseCode() bool`

HasResponseCode returns a boolean if a field has been set.

### SetResponseCodeNil

`func (o *TransactionResponse) SetResponseCodeNil(b bool)`

 SetResponseCodeNil sets the value for ResponseCode to be an explicit nil

### UnsetResponseCode
`func (o *TransactionResponse) UnsetResponseCode()`

UnsetResponseCode ensures that no value is present for ResponseCode, not even an explicit nil
### GetTransactionType

`func (o *TransactionResponse) GetTransactionType() string`

GetTransactionType returns the TransactionType field if non-nil, zero value otherwise.

### GetTransactionTypeOk

`func (o *TransactionResponse) GetTransactionTypeOk() (*string, bool)`

GetTransactionTypeOk returns a tuple with the TransactionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionType

`func (o *TransactionResponse) SetTransactionType(v string)`

SetTransactionType sets TransactionType field to given value.

### HasTransactionType

`func (o *TransactionResponse) HasTransactionType() bool`

HasTransactionType returns a boolean if a field has been set.

### SetTransactionTypeNil

`func (o *TransactionResponse) SetTransactionTypeNil(b bool)`

 SetTransactionTypeNil sets the value for TransactionType to be an explicit nil

### UnsetTransactionType
`func (o *TransactionResponse) UnsetTransactionType()`

UnsetTransactionType ensures that no value is present for TransactionType, not even an explicit nil
### GetMerchantTransactionId

`func (o *TransactionResponse) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *TransactionResponse) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *TransactionResponse) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.

### HasMerchantTransactionId

`func (o *TransactionResponse) HasMerchantTransactionId() bool`

HasMerchantTransactionId returns a boolean if a field has been set.

### SetMerchantTransactionIdNil

`func (o *TransactionResponse) SetMerchantTransactionIdNil(b bool)`

 SetMerchantTransactionIdNil sets the value for MerchantTransactionId to be an explicit nil

### UnsetMerchantTransactionId
`func (o *TransactionResponse) UnsetMerchantTransactionId()`

UnsetMerchantTransactionId ensures that no value is present for MerchantTransactionId, not even an explicit nil
### GetCustomerId

`func (o *TransactionResponse) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *TransactionResponse) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *TransactionResponse) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *TransactionResponse) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *TransactionResponse) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *TransactionResponse) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetGatewayRoutingId

`func (o *TransactionResponse) GetGatewayRoutingId() string`

GetGatewayRoutingId returns the GatewayRoutingId field if non-nil, zero value otherwise.

### GetGatewayRoutingIdOk

`func (o *TransactionResponse) GetGatewayRoutingIdOk() (*string, bool)`

GetGatewayRoutingIdOk returns a tuple with the GatewayRoutingId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayRoutingId

`func (o *TransactionResponse) SetGatewayRoutingId(v string)`

SetGatewayRoutingId sets GatewayRoutingId field to given value.

### HasGatewayRoutingId

`func (o *TransactionResponse) HasGatewayRoutingId() bool`

HasGatewayRoutingId returns a boolean if a field has been set.

### SetGatewayRoutingIdNil

`func (o *TransactionResponse) SetGatewayRoutingIdNil(b bool)`

 SetGatewayRoutingIdNil sets the value for GatewayRoutingId to be an explicit nil

### UnsetGatewayRoutingId
`func (o *TransactionResponse) UnsetGatewayRoutingId()`

UnsetGatewayRoutingId ensures that no value is present for GatewayRoutingId, not even an explicit nil
### GetCurrency

`func (o *TransactionResponse) GetCurrency() string`

GetCurrency returns the Currency field if non-nil, zero value otherwise.

### GetCurrencyOk

`func (o *TransactionResponse) GetCurrencyOk() (*string, bool)`

GetCurrencyOk returns a tuple with the Currency field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrency

`func (o *TransactionResponse) SetCurrency(v string)`

SetCurrency sets Currency field to given value.

### HasCurrency

`func (o *TransactionResponse) HasCurrency() bool`

HasCurrency returns a boolean if a field has been set.

### SetCurrencyNil

`func (o *TransactionResponse) SetCurrencyNil(b bool)`

 SetCurrencyNil sets the value for Currency to be an explicit nil

### UnsetCurrency
`func (o *TransactionResponse) UnsetCurrency()`

UnsetCurrency ensures that no value is present for Currency, not even an explicit nil
### GetAmount

`func (o *TransactionResponse) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *TransactionResponse) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *TransactionResponse) SetAmount(v int64)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *TransactionResponse) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *TransactionResponse) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *TransactionResponse) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil
### GetGatewayType

`func (o *TransactionResponse) GetGatewayType() string`

GetGatewayType returns the GatewayType field if non-nil, zero value otherwise.

### GetGatewayTypeOk

`func (o *TransactionResponse) GetGatewayTypeOk() (*string, bool)`

GetGatewayTypeOk returns a tuple with the GatewayType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayType

`func (o *TransactionResponse) SetGatewayType(v string)`

SetGatewayType sets GatewayType field to given value.

### HasGatewayType

`func (o *TransactionResponse) HasGatewayType() bool`

HasGatewayType returns a boolean if a field has been set.

### SetGatewayTypeNil

`func (o *TransactionResponse) SetGatewayTypeNil(b bool)`

 SetGatewayTypeNil sets the value for GatewayType to be an explicit nil

### UnsetGatewayType
`func (o *TransactionResponse) UnsetGatewayType()`

UnsetGatewayType ensures that no value is present for GatewayType, not even an explicit nil
### GetGatewayTransactionId

`func (o *TransactionResponse) GetGatewayTransactionId() string`

GetGatewayTransactionId returns the GatewayTransactionId field if non-nil, zero value otherwise.

### GetGatewayTransactionIdOk

`func (o *TransactionResponse) GetGatewayTransactionIdOk() (*string, bool)`

GetGatewayTransactionIdOk returns a tuple with the GatewayTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayTransactionId

`func (o *TransactionResponse) SetGatewayTransactionId(v string)`

SetGatewayTransactionId sets GatewayTransactionId field to given value.

### HasGatewayTransactionId

`func (o *TransactionResponse) HasGatewayTransactionId() bool`

HasGatewayTransactionId returns a boolean if a field has been set.

### SetGatewayTransactionIdNil

`func (o *TransactionResponse) SetGatewayTransactionIdNil(b bool)`

 SetGatewayTransactionIdNil sets the value for GatewayTransactionId to be an explicit nil

### UnsetGatewayTransactionId
`func (o *TransactionResponse) UnsetGatewayTransactionId()`

UnsetGatewayTransactionId ensures that no value is present for GatewayTransactionId, not even an explicit nil
### GetAcquirerAuthCode

`func (o *TransactionResponse) GetAcquirerAuthCode() string`

GetAcquirerAuthCode returns the AcquirerAuthCode field if non-nil, zero value otherwise.

### GetAcquirerAuthCodeOk

`func (o *TransactionResponse) GetAcquirerAuthCodeOk() (*string, bool)`

GetAcquirerAuthCodeOk returns a tuple with the AcquirerAuthCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcquirerAuthCode

`func (o *TransactionResponse) SetAcquirerAuthCode(v string)`

SetAcquirerAuthCode sets AcquirerAuthCode field to given value.

### HasAcquirerAuthCode

`func (o *TransactionResponse) HasAcquirerAuthCode() bool`

HasAcquirerAuthCode returns a boolean if a field has been set.

### SetAcquirerAuthCodeNil

`func (o *TransactionResponse) SetAcquirerAuthCodeNil(b bool)`

 SetAcquirerAuthCodeNil sets the value for AcquirerAuthCode to be an explicit nil

### UnsetAcquirerAuthCode
`func (o *TransactionResponse) UnsetAcquirerAuthCode()`

UnsetAcquirerAuthCode ensures that no value is present for AcquirerAuthCode, not even an explicit nil
### GetInlineRetryPreviousTransactionId

`func (o *TransactionResponse) GetInlineRetryPreviousTransactionId() string`

GetInlineRetryPreviousTransactionId returns the InlineRetryPreviousTransactionId field if non-nil, zero value otherwise.

### GetInlineRetryPreviousTransactionIdOk

`func (o *TransactionResponse) GetInlineRetryPreviousTransactionIdOk() (*string, bool)`

GetInlineRetryPreviousTransactionIdOk returns a tuple with the InlineRetryPreviousTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInlineRetryPreviousTransactionId

`func (o *TransactionResponse) SetInlineRetryPreviousTransactionId(v string)`

SetInlineRetryPreviousTransactionId sets InlineRetryPreviousTransactionId field to given value.

### HasInlineRetryPreviousTransactionId

`func (o *TransactionResponse) HasInlineRetryPreviousTransactionId() bool`

HasInlineRetryPreviousTransactionId returns a boolean if a field has been set.

### SetInlineRetryPreviousTransactionIdNil

`func (o *TransactionResponse) SetInlineRetryPreviousTransactionIdNil(b bool)`

 SetInlineRetryPreviousTransactionIdNil sets the value for InlineRetryPreviousTransactionId to be an explicit nil

### UnsetInlineRetryPreviousTransactionId
`func (o *TransactionResponse) UnsetInlineRetryPreviousTransactionId()`

UnsetInlineRetryPreviousTransactionId ensures that no value is present for InlineRetryPreviousTransactionId, not even an explicit nil
### GetInlineRetryPreviousMerchantTransactionId

`func (o *TransactionResponse) GetInlineRetryPreviousMerchantTransactionId() string`

GetInlineRetryPreviousMerchantTransactionId returns the InlineRetryPreviousMerchantTransactionId field if non-nil, zero value otherwise.

### GetInlineRetryPreviousMerchantTransactionIdOk

`func (o *TransactionResponse) GetInlineRetryPreviousMerchantTransactionIdOk() (*string, bool)`

GetInlineRetryPreviousMerchantTransactionIdOk returns a tuple with the InlineRetryPreviousMerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInlineRetryPreviousMerchantTransactionId

`func (o *TransactionResponse) SetInlineRetryPreviousMerchantTransactionId(v string)`

SetInlineRetryPreviousMerchantTransactionId sets InlineRetryPreviousMerchantTransactionId field to given value.

### HasInlineRetryPreviousMerchantTransactionId

`func (o *TransactionResponse) HasInlineRetryPreviousMerchantTransactionId() bool`

HasInlineRetryPreviousMerchantTransactionId returns a boolean if a field has been set.

### SetInlineRetryPreviousMerchantTransactionIdNil

`func (o *TransactionResponse) SetInlineRetryPreviousMerchantTransactionIdNil(b bool)`

 SetInlineRetryPreviousMerchantTransactionIdNil sets the value for InlineRetryPreviousMerchantTransactionId to be an explicit nil

### UnsetInlineRetryPreviousMerchantTransactionId
`func (o *TransactionResponse) UnsetInlineRetryPreviousMerchantTransactionId()`

UnsetInlineRetryPreviousMerchantTransactionId ensures that no value is present for InlineRetryPreviousMerchantTransactionId, not even an explicit nil
### GetIsInlineRetry

`func (o *TransactionResponse) GetIsInlineRetry() bool`

GetIsInlineRetry returns the IsInlineRetry field if non-nil, zero value otherwise.

### GetIsInlineRetryOk

`func (o *TransactionResponse) GetIsInlineRetryOk() (*bool, bool)`

GetIsInlineRetryOk returns a tuple with the IsInlineRetry field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsInlineRetry

`func (o *TransactionResponse) SetIsInlineRetry(v bool)`

SetIsInlineRetry sets IsInlineRetry field to given value.

### HasIsInlineRetry

`func (o *TransactionResponse) HasIsInlineRetry() bool`

HasIsInlineRetry returns a boolean if a field has been set.

### SetIsInlineRetryNil

`func (o *TransactionResponse) SetIsInlineRetryNil(b bool)`

 SetIsInlineRetryNil sets the value for IsInlineRetry to be an explicit nil

### UnsetIsInlineRetry
`func (o *TransactionResponse) UnsetIsInlineRetry()`

UnsetIsInlineRetry ensures that no value is present for IsInlineRetry, not even an explicit nil
### GetRetryDate

`func (o *TransactionResponse) GetRetryDate() time.Time`

GetRetryDate returns the RetryDate field if non-nil, zero value otherwise.

### GetRetryDateOk

`func (o *TransactionResponse) GetRetryDateOk() (*time.Time, bool)`

GetRetryDateOk returns a tuple with the RetryDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRetryDate

`func (o *TransactionResponse) SetRetryDate(v time.Time)`

SetRetryDate sets RetryDate field to given value.

### HasRetryDate

`func (o *TransactionResponse) HasRetryDate() bool`

HasRetryDate returns a boolean if a field has been set.

### SetRetryDateNil

`func (o *TransactionResponse) SetRetryDateNil(b bool)`

 SetRetryDateNil sets the value for RetryDate to be an explicit nil

### UnsetRetryDate
`func (o *TransactionResponse) UnsetRetryDate()`

UnsetRetryDate ensures that no value is present for RetryDate, not even an explicit nil
### GetMitStoredTransactionId

`func (o *TransactionResponse) GetMitStoredTransactionId() string`

GetMitStoredTransactionId returns the MitStoredTransactionId field if non-nil, zero value otherwise.

### GetMitStoredTransactionIdOk

`func (o *TransactionResponse) GetMitStoredTransactionIdOk() (*string, bool)`

GetMitStoredTransactionIdOk returns a tuple with the MitStoredTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMitStoredTransactionId

`func (o *TransactionResponse) SetMitStoredTransactionId(v string)`

SetMitStoredTransactionId sets MitStoredTransactionId field to given value.

### HasMitStoredTransactionId

`func (o *TransactionResponse) HasMitStoredTransactionId() bool`

HasMitStoredTransactionId returns a boolean if a field has been set.

### SetMitStoredTransactionIdNil

`func (o *TransactionResponse) SetMitStoredTransactionIdNil(b bool)`

 SetMitStoredTransactionIdNil sets the value for MitStoredTransactionId to be an explicit nil

### UnsetMitStoredTransactionId
`func (o *TransactionResponse) UnsetMitStoredTransactionId()`

UnsetMitStoredTransactionId ensures that no value is present for MitStoredTransactionId, not even an explicit nil
### GetStoredCredential

`func (o *TransactionResponse) GetStoredCredential() StoredCredentialResponse`

GetStoredCredential returns the StoredCredential field if non-nil, zero value otherwise.

### GetStoredCredentialOk

`func (o *TransactionResponse) GetStoredCredentialOk() (*StoredCredentialResponse, bool)`

GetStoredCredentialOk returns a tuple with the StoredCredential field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStoredCredential

`func (o *TransactionResponse) SetStoredCredential(v StoredCredentialResponse)`

SetStoredCredential sets StoredCredential field to given value.

### HasStoredCredential

`func (o *TransactionResponse) HasStoredCredential() bool`

HasStoredCredential returns a boolean if a field has been set.

### SetStoredCredentialNil

`func (o *TransactionResponse) SetStoredCredentialNil(b bool)`

 SetStoredCredentialNil sets the value for StoredCredential to be an explicit nil

### UnsetStoredCredential
`func (o *TransactionResponse) UnsetStoredCredential()`

UnsetStoredCredential ensures that no value is present for StoredCredential, not even an explicit nil
### GetOrderId

`func (o *TransactionResponse) GetOrderId() string`

GetOrderId returns the OrderId field if non-nil, zero value otherwise.

### GetOrderIdOk

`func (o *TransactionResponse) GetOrderIdOk() (*string, bool)`

GetOrderIdOk returns a tuple with the OrderId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderId

`func (o *TransactionResponse) SetOrderId(v string)`

SetOrderId sets OrderId field to given value.

### HasOrderId

`func (o *TransactionResponse) HasOrderId() bool`

HasOrderId returns a boolean if a field has been set.

### SetOrderIdNil

`func (o *TransactionResponse) SetOrderIdNil(b bool)`

 SetOrderIdNil sets the value for OrderId to be an explicit nil

### UnsetOrderId
`func (o *TransactionResponse) UnsetOrderId()`

UnsetOrderId ensures that no value is present for OrderId, not even an explicit nil
### GetStatementDescriptor

`func (o *TransactionResponse) GetStatementDescriptor() string`

GetStatementDescriptor returns the StatementDescriptor field if non-nil, zero value otherwise.

### GetStatementDescriptorOk

`func (o *TransactionResponse) GetStatementDescriptorOk() (*string, bool)`

GetStatementDescriptorOk returns a tuple with the StatementDescriptor field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStatementDescriptor

`func (o *TransactionResponse) SetStatementDescriptor(v string)`

SetStatementDescriptor sets StatementDescriptor field to given value.

### HasStatementDescriptor

`func (o *TransactionResponse) HasStatementDescriptor() bool`

HasStatementDescriptor returns a boolean if a field has been set.

### SetStatementDescriptorNil

`func (o *TransactionResponse) SetStatementDescriptorNil(b bool)`

 SetStatementDescriptorNil sets the value for StatementDescriptor to be an explicit nil

### UnsetStatementDescriptor
`func (o *TransactionResponse) UnsetStatementDescriptor()`

UnsetStatementDescriptor ensures that no value is present for StatementDescriptor, not even an explicit nil
### GetCustomerIp

`func (o *TransactionResponse) GetCustomerIp() string`

GetCustomerIp returns the CustomerIp field if non-nil, zero value otherwise.

### GetCustomerIpOk

`func (o *TransactionResponse) GetCustomerIpOk() (*string, bool)`

GetCustomerIpOk returns a tuple with the CustomerIp field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerIp

`func (o *TransactionResponse) SetCustomerIp(v string)`

SetCustomerIp sets CustomerIp field to given value.

### HasCustomerIp

`func (o *TransactionResponse) HasCustomerIp() bool`

HasCustomerIp returns a boolean if a field has been set.

### SetCustomerIpNil

`func (o *TransactionResponse) SetCustomerIpNil(b bool)`

 SetCustomerIpNil sets the value for CustomerIp to be an explicit nil

### UnsetCustomerIp
`func (o *TransactionResponse) UnsetCustomerIp()`

UnsetCustomerIp ensures that no value is present for CustomerIp, not even an explicit nil
### GetEngagedRecoveryState

`func (o *TransactionResponse) GetEngagedRecoveryState() int32`

GetEngagedRecoveryState returns the EngagedRecoveryState field if non-nil, zero value otherwise.

### GetEngagedRecoveryStateOk

`func (o *TransactionResponse) GetEngagedRecoveryStateOk() (*int32, bool)`

GetEngagedRecoveryStateOk returns a tuple with the EngagedRecoveryState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEngagedRecoveryState

`func (o *TransactionResponse) SetEngagedRecoveryState(v int32)`

SetEngagedRecoveryState sets EngagedRecoveryState field to given value.

### HasEngagedRecoveryState

`func (o *TransactionResponse) HasEngagedRecoveryState() bool`

HasEngagedRecoveryState returns a boolean if a field has been set.

### SetEngagedRecoveryStateNil

`func (o *TransactionResponse) SetEngagedRecoveryStateNil(b bool)`

 SetEngagedRecoveryStateNil sets the value for EngagedRecoveryState to be an explicit nil

### UnsetEngagedRecoveryState
`func (o *TransactionResponse) UnsetEngagedRecoveryState()`

UnsetEngagedRecoveryState ensures that no value is present for EngagedRecoveryState, not even an explicit nil
### GetDescription

`func (o *TransactionResponse) GetDescription() string`

GetDescription returns the Description field if non-nil, zero value otherwise.

### GetDescriptionOk

`func (o *TransactionResponse) GetDescriptionOk() (*string, bool)`

GetDescriptionOk returns a tuple with the Description field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDescription

`func (o *TransactionResponse) SetDescription(v string)`

SetDescription sets Description field to given value.

### HasDescription

`func (o *TransactionResponse) HasDescription() bool`

HasDescription returns a boolean if a field has been set.

### SetDescriptionNil

`func (o *TransactionResponse) SetDescriptionNil(b bool)`

 SetDescriptionNil sets the value for Description to be an explicit nil

### UnsetDescription
`func (o *TransactionResponse) UnsetDescription()`

UnsetDescription ensures that no value is present for Description, not even an explicit nil
### GetGatewayFields

`func (o *TransactionResponse) GetGatewayFields() map[string]interface{}`

GetGatewayFields returns the GatewayFields field if non-nil, zero value otherwise.

### GetGatewayFieldsOk

`func (o *TransactionResponse) GetGatewayFieldsOk() (*map[string]interface{}, bool)`

GetGatewayFieldsOk returns a tuple with the GatewayFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayFields

`func (o *TransactionResponse) SetGatewayFields(v map[string]interface{})`

SetGatewayFields sets GatewayFields field to given value.

### HasGatewayFields

`func (o *TransactionResponse) HasGatewayFields() bool`

HasGatewayFields returns a boolean if a field has been set.

### SetGatewayFieldsNil

`func (o *TransactionResponse) SetGatewayFieldsNil(b bool)`

 SetGatewayFieldsNil sets the value for GatewayFields to be an explicit nil

### UnsetGatewayFields
`func (o *TransactionResponse) UnsetGatewayFields()`

UnsetGatewayFields ensures that no value is present for GatewayFields, not even an explicit nil
### GetGatewaySpecificResponseFields

`func (o *TransactionResponse) GetGatewaySpecificResponseFields() map[string]interface{}`

GetGatewaySpecificResponseFields returns the GatewaySpecificResponseFields field if non-nil, zero value otherwise.

### GetGatewaySpecificResponseFieldsOk

`func (o *TransactionResponse) GetGatewaySpecificResponseFieldsOk() (*map[string]interface{}, bool)`

GetGatewaySpecificResponseFieldsOk returns a tuple with the GatewaySpecificResponseFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewaySpecificResponseFields

`func (o *TransactionResponse) SetGatewaySpecificResponseFields(v map[string]interface{})`

SetGatewaySpecificResponseFields sets GatewaySpecificResponseFields field to given value.

### HasGatewaySpecificResponseFields

`func (o *TransactionResponse) HasGatewaySpecificResponseFields() bool`

HasGatewaySpecificResponseFields returns a boolean if a field has been set.

### SetGatewaySpecificResponseFieldsNil

`func (o *TransactionResponse) SetGatewaySpecificResponseFieldsNil(b bool)`

 SetGatewaySpecificResponseFieldsNil sets the value for GatewaySpecificResponseFields to be an explicit nil

### UnsetGatewaySpecificResponseFields
`func (o *TransactionResponse) UnsetGatewaySpecificResponseFields()`

UnsetGatewaySpecificResponseFields ensures that no value is present for GatewaySpecificResponseFields, not even an explicit nil
### GetPaymentPlanData

`func (o *TransactionResponse) GetPaymentPlanData() PaymentPlanData`

GetPaymentPlanData returns the PaymentPlanData field if non-nil, zero value otherwise.

### GetPaymentPlanDataOk

`func (o *TransactionResponse) GetPaymentPlanDataOk() (*PaymentPlanData, bool)`

GetPaymentPlanDataOk returns a tuple with the PaymentPlanData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentPlanData

`func (o *TransactionResponse) SetPaymentPlanData(v PaymentPlanData)`

SetPaymentPlanData sets PaymentPlanData field to given value.

### HasPaymentPlanData

`func (o *TransactionResponse) HasPaymentPlanData() bool`

HasPaymentPlanData returns a boolean if a field has been set.

### SetPaymentPlanDataNil

`func (o *TransactionResponse) SetPaymentPlanDataNil(b bool)`

 SetPaymentPlanDataNil sets the value for PaymentPlanData to be an explicit nil

### UnsetPaymentPlanData
`func (o *TransactionResponse) UnsetPaymentPlanData()`

UnsetPaymentPlanData ensures that no value is present for PaymentPlanData, not even an explicit nil
### GetRecovery

`func (o *TransactionResponse) GetRecovery() Recovery`

GetRecovery returns the Recovery field if non-nil, zero value otherwise.

### GetRecoveryOk

`func (o *TransactionResponse) GetRecoveryOk() (*Recovery, bool)`

GetRecoveryOk returns a tuple with the Recovery field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRecovery

`func (o *TransactionResponse) SetRecovery(v Recovery)`

SetRecovery sets Recovery field to given value.

### HasRecovery

`func (o *TransactionResponse) HasRecovery() bool`

HasRecovery returns a boolean if a field has been set.

### SetRecoveryNil

`func (o *TransactionResponse) SetRecoveryNil(b bool)`

 SetRecoveryNil sets the value for Recovery to be an explicit nil

### UnsetRecovery
`func (o *TransactionResponse) UnsetRecovery()`

UnsetRecovery ensures that no value is present for Recovery, not even an explicit nil
### GetResponse

`func (o *TransactionResponse) GetResponse() TransactionResponseDetails`

GetResponse returns the Response field if non-nil, zero value otherwise.

### GetResponseOk

`func (o *TransactionResponse) GetResponseOk() (*TransactionResponseDetails, bool)`

GetResponseOk returns a tuple with the Response field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponse

`func (o *TransactionResponse) SetResponse(v TransactionResponseDetails)`

SetResponse sets Response field to given value.

### HasResponse

`func (o *TransactionResponse) HasResponse() bool`

HasResponse returns a boolean if a field has been set.

### SetResponseNil

`func (o *TransactionResponse) SetResponseNil(b bool)`

 SetResponseNil sets the value for Response to be an explicit nil

### UnsetResponse
`func (o *TransactionResponse) UnsetResponse()`

UnsetResponse ensures that no value is present for Response, not even an explicit nil
### GetPaymentMethod

`func (o *TransactionResponse) GetPaymentMethod() PaymentMethodResponse`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *TransactionResponse) GetPaymentMethodOk() (*PaymentMethodResponse, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *TransactionResponse) SetPaymentMethod(v PaymentMethodResponse)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *TransactionResponse) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.

### SetPaymentMethodNil

`func (o *TransactionResponse) SetPaymentMethodNil(b bool)`

 SetPaymentMethodNil sets the value for PaymentMethod to be an explicit nil

### UnsetPaymentMethod
`func (o *TransactionResponse) UnsetPaymentMethod()`

UnsetPaymentMethod ensures that no value is present for PaymentMethod, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


