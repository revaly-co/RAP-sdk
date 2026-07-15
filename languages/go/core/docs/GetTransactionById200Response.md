# GetTransactionById200Response

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
**CustomerIp** | Pointer to **NullableString** | Customer&#39;s IP address at time of transaction | [optional] 
**EngagedRecoveryState** | Pointer to **NullableInt32** | Recovery state indicator (0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional] 
**Description** | Pointer to **NullableString** | Transaction description or notes | [optional] 
**GatewayFields** | Pointer to **map[string]interface{}** | Additional gateway-specific fields | [optional] 
**GatewaySpecificResponseFields** | Pointer to **map[string]interface{}** | Additional gateway-specific response details returned directly from the processor | [optional] 
**PaymentPlanData** | Pointer to [**NullablePaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**Recovery** | Pointer to [**NullableRecovery**](Recovery.md) |  | [optional] 
**Response** | Pointer to [**NullableTransactionResponseDetails**](TransactionResponseDetails.md) |  | [optional] 
**PaymentMethod** | Pointer to [**NullablePaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional] 
**Transaction** | Pointer to [**TransactionResponse**](TransactionResponse.md) | The transaction matching the supplied id (the record the non-expanded lookup returns). | [optional] 
**Transactions** | Pointer to [**[]TransactionResponse**](TransactionResponse.md) | Every transaction in the payment, ordered by transaction date ascending. Capped at 100. | [optional] 

## Methods

### NewGetTransactionById200Response

`func NewGetTransactionById200Response() *GetTransactionById200Response`

NewGetTransactionById200Response instantiates a new GetTransactionById200Response object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewGetTransactionById200ResponseWithDefaults

`func NewGetTransactionById200ResponseWithDefaults() *GetTransactionById200Response`

NewGetTransactionById200ResponseWithDefaults instantiates a new GetTransactionById200Response object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionId

`func (o *GetTransactionById200Response) GetTransactionId() string`

GetTransactionId returns the TransactionId field if non-nil, zero value otherwise.

### GetTransactionIdOk

`func (o *GetTransactionById200Response) GetTransactionIdOk() (*string, bool)`

GetTransactionIdOk returns a tuple with the TransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionId

`func (o *GetTransactionById200Response) SetTransactionId(v string)`

SetTransactionId sets TransactionId field to given value.

### HasTransactionId

`func (o *GetTransactionById200Response) HasTransactionId() bool`

HasTransactionId returns a boolean if a field has been set.

### SetTransactionIdNil

`func (o *GetTransactionById200Response) SetTransactionIdNil(b bool)`

 SetTransactionIdNil sets the value for TransactionId to be an explicit nil

### UnsetTransactionId
`func (o *GetTransactionById200Response) UnsetTransactionId()`

UnsetTransactionId ensures that no value is present for TransactionId, not even an explicit nil
### GetTransactionDate

`func (o *GetTransactionById200Response) GetTransactionDate() time.Time`

GetTransactionDate returns the TransactionDate field if non-nil, zero value otherwise.

### GetTransactionDateOk

`func (o *GetTransactionById200Response) GetTransactionDateOk() (*time.Time, bool)`

GetTransactionDateOk returns a tuple with the TransactionDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionDate

`func (o *GetTransactionById200Response) SetTransactionDate(v time.Time)`

SetTransactionDate sets TransactionDate field to given value.

### HasTransactionDate

`func (o *GetTransactionById200Response) HasTransactionDate() bool`

HasTransactionDate returns a boolean if a field has been set.

### SetTransactionDateNil

`func (o *GetTransactionById200Response) SetTransactionDateNil(b bool)`

 SetTransactionDateNil sets the value for TransactionDate to be an explicit nil

### UnsetTransactionDate
`func (o *GetTransactionById200Response) UnsetTransactionDate()`

UnsetTransactionDate ensures that no value is present for TransactionDate, not even an explicit nil
### GetTransactionStatus

`func (o *GetTransactionById200Response) GetTransactionStatus() int32`

GetTransactionStatus returns the TransactionStatus field if non-nil, zero value otherwise.

### GetTransactionStatusOk

`func (o *GetTransactionById200Response) GetTransactionStatusOk() (*int32, bool)`

GetTransactionStatusOk returns a tuple with the TransactionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionStatus

`func (o *GetTransactionById200Response) SetTransactionStatus(v int32)`

SetTransactionStatus sets TransactionStatus field to given value.

### HasTransactionStatus

`func (o *GetTransactionById200Response) HasTransactionStatus() bool`

HasTransactionStatus returns a boolean if a field has been set.

### SetTransactionStatusNil

`func (o *GetTransactionById200Response) SetTransactionStatusNil(b bool)`

 SetTransactionStatusNil sets the value for TransactionStatus to be an explicit nil

### UnsetTransactionStatus
`func (o *GetTransactionById200Response) UnsetTransactionStatus()`

UnsetTransactionStatus ensures that no value is present for TransactionStatus, not even an explicit nil
### GetMessage

`func (o *GetTransactionById200Response) GetMessage() string`

GetMessage returns the Message field if non-nil, zero value otherwise.

### GetMessageOk

`func (o *GetTransactionById200Response) GetMessageOk() (*string, bool)`

GetMessageOk returns a tuple with the Message field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessage

`func (o *GetTransactionById200Response) SetMessage(v string)`

SetMessage sets Message field to given value.

### HasMessage

`func (o *GetTransactionById200Response) HasMessage() bool`

HasMessage returns a boolean if a field has been set.

### SetMessageNil

`func (o *GetTransactionById200Response) SetMessageNil(b bool)`

 SetMessageNil sets the value for Message to be an explicit nil

### UnsetMessage
`func (o *GetTransactionById200Response) UnsetMessage()`

UnsetMessage ensures that no value is present for Message, not even an explicit nil
### GetResponseCode

`func (o *GetTransactionById200Response) GetResponseCode() string`

GetResponseCode returns the ResponseCode field if non-nil, zero value otherwise.

### GetResponseCodeOk

`func (o *GetTransactionById200Response) GetResponseCodeOk() (*string, bool)`

GetResponseCodeOk returns a tuple with the ResponseCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponseCode

`func (o *GetTransactionById200Response) SetResponseCode(v string)`

SetResponseCode sets ResponseCode field to given value.

### HasResponseCode

`func (o *GetTransactionById200Response) HasResponseCode() bool`

HasResponseCode returns a boolean if a field has been set.

### SetResponseCodeNil

`func (o *GetTransactionById200Response) SetResponseCodeNil(b bool)`

 SetResponseCodeNil sets the value for ResponseCode to be an explicit nil

### UnsetResponseCode
`func (o *GetTransactionById200Response) UnsetResponseCode()`

UnsetResponseCode ensures that no value is present for ResponseCode, not even an explicit nil
### GetTransactionType

`func (o *GetTransactionById200Response) GetTransactionType() string`

GetTransactionType returns the TransactionType field if non-nil, zero value otherwise.

### GetTransactionTypeOk

`func (o *GetTransactionById200Response) GetTransactionTypeOk() (*string, bool)`

GetTransactionTypeOk returns a tuple with the TransactionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionType

`func (o *GetTransactionById200Response) SetTransactionType(v string)`

SetTransactionType sets TransactionType field to given value.

### HasTransactionType

`func (o *GetTransactionById200Response) HasTransactionType() bool`

HasTransactionType returns a boolean if a field has been set.

### SetTransactionTypeNil

`func (o *GetTransactionById200Response) SetTransactionTypeNil(b bool)`

 SetTransactionTypeNil sets the value for TransactionType to be an explicit nil

### UnsetTransactionType
`func (o *GetTransactionById200Response) UnsetTransactionType()`

UnsetTransactionType ensures that no value is present for TransactionType, not even an explicit nil
### GetMerchantTransactionId

`func (o *GetTransactionById200Response) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *GetTransactionById200Response) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *GetTransactionById200Response) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.

### HasMerchantTransactionId

`func (o *GetTransactionById200Response) HasMerchantTransactionId() bool`

HasMerchantTransactionId returns a boolean if a field has been set.

### SetMerchantTransactionIdNil

`func (o *GetTransactionById200Response) SetMerchantTransactionIdNil(b bool)`

 SetMerchantTransactionIdNil sets the value for MerchantTransactionId to be an explicit nil

### UnsetMerchantTransactionId
`func (o *GetTransactionById200Response) UnsetMerchantTransactionId()`

UnsetMerchantTransactionId ensures that no value is present for MerchantTransactionId, not even an explicit nil
### GetCustomerId

`func (o *GetTransactionById200Response) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *GetTransactionById200Response) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *GetTransactionById200Response) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *GetTransactionById200Response) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *GetTransactionById200Response) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *GetTransactionById200Response) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetGatewayRoutingId

`func (o *GetTransactionById200Response) GetGatewayRoutingId() string`

GetGatewayRoutingId returns the GatewayRoutingId field if non-nil, zero value otherwise.

### GetGatewayRoutingIdOk

`func (o *GetTransactionById200Response) GetGatewayRoutingIdOk() (*string, bool)`

GetGatewayRoutingIdOk returns a tuple with the GatewayRoutingId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayRoutingId

`func (o *GetTransactionById200Response) SetGatewayRoutingId(v string)`

SetGatewayRoutingId sets GatewayRoutingId field to given value.

### HasGatewayRoutingId

`func (o *GetTransactionById200Response) HasGatewayRoutingId() bool`

HasGatewayRoutingId returns a boolean if a field has been set.

### SetGatewayRoutingIdNil

`func (o *GetTransactionById200Response) SetGatewayRoutingIdNil(b bool)`

 SetGatewayRoutingIdNil sets the value for GatewayRoutingId to be an explicit nil

### UnsetGatewayRoutingId
`func (o *GetTransactionById200Response) UnsetGatewayRoutingId()`

UnsetGatewayRoutingId ensures that no value is present for GatewayRoutingId, not even an explicit nil
### GetCurrency

`func (o *GetTransactionById200Response) GetCurrency() string`

GetCurrency returns the Currency field if non-nil, zero value otherwise.

### GetCurrencyOk

`func (o *GetTransactionById200Response) GetCurrencyOk() (*string, bool)`

GetCurrencyOk returns a tuple with the Currency field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrency

`func (o *GetTransactionById200Response) SetCurrency(v string)`

SetCurrency sets Currency field to given value.

### HasCurrency

`func (o *GetTransactionById200Response) HasCurrency() bool`

HasCurrency returns a boolean if a field has been set.

### SetCurrencyNil

`func (o *GetTransactionById200Response) SetCurrencyNil(b bool)`

 SetCurrencyNil sets the value for Currency to be an explicit nil

### UnsetCurrency
`func (o *GetTransactionById200Response) UnsetCurrency()`

UnsetCurrency ensures that no value is present for Currency, not even an explicit nil
### GetAmount

`func (o *GetTransactionById200Response) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *GetTransactionById200Response) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *GetTransactionById200Response) SetAmount(v int64)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *GetTransactionById200Response) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *GetTransactionById200Response) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *GetTransactionById200Response) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil
### GetGatewayType

`func (o *GetTransactionById200Response) GetGatewayType() string`

GetGatewayType returns the GatewayType field if non-nil, zero value otherwise.

### GetGatewayTypeOk

`func (o *GetTransactionById200Response) GetGatewayTypeOk() (*string, bool)`

GetGatewayTypeOk returns a tuple with the GatewayType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayType

`func (o *GetTransactionById200Response) SetGatewayType(v string)`

SetGatewayType sets GatewayType field to given value.

### HasGatewayType

`func (o *GetTransactionById200Response) HasGatewayType() bool`

HasGatewayType returns a boolean if a field has been set.

### SetGatewayTypeNil

`func (o *GetTransactionById200Response) SetGatewayTypeNil(b bool)`

 SetGatewayTypeNil sets the value for GatewayType to be an explicit nil

### UnsetGatewayType
`func (o *GetTransactionById200Response) UnsetGatewayType()`

UnsetGatewayType ensures that no value is present for GatewayType, not even an explicit nil
### GetGatewayTransactionId

`func (o *GetTransactionById200Response) GetGatewayTransactionId() string`

GetGatewayTransactionId returns the GatewayTransactionId field if non-nil, zero value otherwise.

### GetGatewayTransactionIdOk

`func (o *GetTransactionById200Response) GetGatewayTransactionIdOk() (*string, bool)`

GetGatewayTransactionIdOk returns a tuple with the GatewayTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayTransactionId

`func (o *GetTransactionById200Response) SetGatewayTransactionId(v string)`

SetGatewayTransactionId sets GatewayTransactionId field to given value.

### HasGatewayTransactionId

`func (o *GetTransactionById200Response) HasGatewayTransactionId() bool`

HasGatewayTransactionId returns a boolean if a field has been set.

### SetGatewayTransactionIdNil

`func (o *GetTransactionById200Response) SetGatewayTransactionIdNil(b bool)`

 SetGatewayTransactionIdNil sets the value for GatewayTransactionId to be an explicit nil

### UnsetGatewayTransactionId
`func (o *GetTransactionById200Response) UnsetGatewayTransactionId()`

UnsetGatewayTransactionId ensures that no value is present for GatewayTransactionId, not even an explicit nil
### GetAcquirerAuthCode

`func (o *GetTransactionById200Response) GetAcquirerAuthCode() string`

GetAcquirerAuthCode returns the AcquirerAuthCode field if non-nil, zero value otherwise.

### GetAcquirerAuthCodeOk

`func (o *GetTransactionById200Response) GetAcquirerAuthCodeOk() (*string, bool)`

GetAcquirerAuthCodeOk returns a tuple with the AcquirerAuthCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcquirerAuthCode

`func (o *GetTransactionById200Response) SetAcquirerAuthCode(v string)`

SetAcquirerAuthCode sets AcquirerAuthCode field to given value.

### HasAcquirerAuthCode

`func (o *GetTransactionById200Response) HasAcquirerAuthCode() bool`

HasAcquirerAuthCode returns a boolean if a field has been set.

### SetAcquirerAuthCodeNil

`func (o *GetTransactionById200Response) SetAcquirerAuthCodeNil(b bool)`

 SetAcquirerAuthCodeNil sets the value for AcquirerAuthCode to be an explicit nil

### UnsetAcquirerAuthCode
`func (o *GetTransactionById200Response) UnsetAcquirerAuthCode()`

UnsetAcquirerAuthCode ensures that no value is present for AcquirerAuthCode, not even an explicit nil
### GetInlineRetryPreviousTransactionId

`func (o *GetTransactionById200Response) GetInlineRetryPreviousTransactionId() string`

GetInlineRetryPreviousTransactionId returns the InlineRetryPreviousTransactionId field if non-nil, zero value otherwise.

### GetInlineRetryPreviousTransactionIdOk

`func (o *GetTransactionById200Response) GetInlineRetryPreviousTransactionIdOk() (*string, bool)`

GetInlineRetryPreviousTransactionIdOk returns a tuple with the InlineRetryPreviousTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInlineRetryPreviousTransactionId

`func (o *GetTransactionById200Response) SetInlineRetryPreviousTransactionId(v string)`

SetInlineRetryPreviousTransactionId sets InlineRetryPreviousTransactionId field to given value.

### HasInlineRetryPreviousTransactionId

`func (o *GetTransactionById200Response) HasInlineRetryPreviousTransactionId() bool`

HasInlineRetryPreviousTransactionId returns a boolean if a field has been set.

### SetInlineRetryPreviousTransactionIdNil

`func (o *GetTransactionById200Response) SetInlineRetryPreviousTransactionIdNil(b bool)`

 SetInlineRetryPreviousTransactionIdNil sets the value for InlineRetryPreviousTransactionId to be an explicit nil

### UnsetInlineRetryPreviousTransactionId
`func (o *GetTransactionById200Response) UnsetInlineRetryPreviousTransactionId()`

UnsetInlineRetryPreviousTransactionId ensures that no value is present for InlineRetryPreviousTransactionId, not even an explicit nil
### GetInlineRetryPreviousMerchantTransactionId

`func (o *GetTransactionById200Response) GetInlineRetryPreviousMerchantTransactionId() string`

GetInlineRetryPreviousMerchantTransactionId returns the InlineRetryPreviousMerchantTransactionId field if non-nil, zero value otherwise.

### GetInlineRetryPreviousMerchantTransactionIdOk

`func (o *GetTransactionById200Response) GetInlineRetryPreviousMerchantTransactionIdOk() (*string, bool)`

GetInlineRetryPreviousMerchantTransactionIdOk returns a tuple with the InlineRetryPreviousMerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInlineRetryPreviousMerchantTransactionId

`func (o *GetTransactionById200Response) SetInlineRetryPreviousMerchantTransactionId(v string)`

SetInlineRetryPreviousMerchantTransactionId sets InlineRetryPreviousMerchantTransactionId field to given value.

### HasInlineRetryPreviousMerchantTransactionId

`func (o *GetTransactionById200Response) HasInlineRetryPreviousMerchantTransactionId() bool`

HasInlineRetryPreviousMerchantTransactionId returns a boolean if a field has been set.

### SetInlineRetryPreviousMerchantTransactionIdNil

`func (o *GetTransactionById200Response) SetInlineRetryPreviousMerchantTransactionIdNil(b bool)`

 SetInlineRetryPreviousMerchantTransactionIdNil sets the value for InlineRetryPreviousMerchantTransactionId to be an explicit nil

### UnsetInlineRetryPreviousMerchantTransactionId
`func (o *GetTransactionById200Response) UnsetInlineRetryPreviousMerchantTransactionId()`

UnsetInlineRetryPreviousMerchantTransactionId ensures that no value is present for InlineRetryPreviousMerchantTransactionId, not even an explicit nil
### GetIsInlineRetry

`func (o *GetTransactionById200Response) GetIsInlineRetry() bool`

GetIsInlineRetry returns the IsInlineRetry field if non-nil, zero value otherwise.

### GetIsInlineRetryOk

`func (o *GetTransactionById200Response) GetIsInlineRetryOk() (*bool, bool)`

GetIsInlineRetryOk returns a tuple with the IsInlineRetry field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsInlineRetry

`func (o *GetTransactionById200Response) SetIsInlineRetry(v bool)`

SetIsInlineRetry sets IsInlineRetry field to given value.

### HasIsInlineRetry

`func (o *GetTransactionById200Response) HasIsInlineRetry() bool`

HasIsInlineRetry returns a boolean if a field has been set.

### SetIsInlineRetryNil

`func (o *GetTransactionById200Response) SetIsInlineRetryNil(b bool)`

 SetIsInlineRetryNil sets the value for IsInlineRetry to be an explicit nil

### UnsetIsInlineRetry
`func (o *GetTransactionById200Response) UnsetIsInlineRetry()`

UnsetIsInlineRetry ensures that no value is present for IsInlineRetry, not even an explicit nil
### GetRetryDate

`func (o *GetTransactionById200Response) GetRetryDate() time.Time`

GetRetryDate returns the RetryDate field if non-nil, zero value otherwise.

### GetRetryDateOk

`func (o *GetTransactionById200Response) GetRetryDateOk() (*time.Time, bool)`

GetRetryDateOk returns a tuple with the RetryDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRetryDate

`func (o *GetTransactionById200Response) SetRetryDate(v time.Time)`

SetRetryDate sets RetryDate field to given value.

### HasRetryDate

`func (o *GetTransactionById200Response) HasRetryDate() bool`

HasRetryDate returns a boolean if a field has been set.

### SetRetryDateNil

`func (o *GetTransactionById200Response) SetRetryDateNil(b bool)`

 SetRetryDateNil sets the value for RetryDate to be an explicit nil

### UnsetRetryDate
`func (o *GetTransactionById200Response) UnsetRetryDate()`

UnsetRetryDate ensures that no value is present for RetryDate, not even an explicit nil
### GetMitStoredTransactionId

`func (o *GetTransactionById200Response) GetMitStoredTransactionId() string`

GetMitStoredTransactionId returns the MitStoredTransactionId field if non-nil, zero value otherwise.

### GetMitStoredTransactionIdOk

`func (o *GetTransactionById200Response) GetMitStoredTransactionIdOk() (*string, bool)`

GetMitStoredTransactionIdOk returns a tuple with the MitStoredTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMitStoredTransactionId

`func (o *GetTransactionById200Response) SetMitStoredTransactionId(v string)`

SetMitStoredTransactionId sets MitStoredTransactionId field to given value.

### HasMitStoredTransactionId

`func (o *GetTransactionById200Response) HasMitStoredTransactionId() bool`

HasMitStoredTransactionId returns a boolean if a field has been set.

### SetMitStoredTransactionIdNil

`func (o *GetTransactionById200Response) SetMitStoredTransactionIdNil(b bool)`

 SetMitStoredTransactionIdNil sets the value for MitStoredTransactionId to be an explicit nil

### UnsetMitStoredTransactionId
`func (o *GetTransactionById200Response) UnsetMitStoredTransactionId()`

UnsetMitStoredTransactionId ensures that no value is present for MitStoredTransactionId, not even an explicit nil
### GetStoredCredential

`func (o *GetTransactionById200Response) GetStoredCredential() StoredCredentialResponse`

GetStoredCredential returns the StoredCredential field if non-nil, zero value otherwise.

### GetStoredCredentialOk

`func (o *GetTransactionById200Response) GetStoredCredentialOk() (*StoredCredentialResponse, bool)`

GetStoredCredentialOk returns a tuple with the StoredCredential field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStoredCredential

`func (o *GetTransactionById200Response) SetStoredCredential(v StoredCredentialResponse)`

SetStoredCredential sets StoredCredential field to given value.

### HasStoredCredential

`func (o *GetTransactionById200Response) HasStoredCredential() bool`

HasStoredCredential returns a boolean if a field has been set.

### SetStoredCredentialNil

`func (o *GetTransactionById200Response) SetStoredCredentialNil(b bool)`

 SetStoredCredentialNil sets the value for StoredCredential to be an explicit nil

### UnsetStoredCredential
`func (o *GetTransactionById200Response) UnsetStoredCredential()`

UnsetStoredCredential ensures that no value is present for StoredCredential, not even an explicit nil
### GetOrderId

`func (o *GetTransactionById200Response) GetOrderId() string`

GetOrderId returns the OrderId field if non-nil, zero value otherwise.

### GetOrderIdOk

`func (o *GetTransactionById200Response) GetOrderIdOk() (*string, bool)`

GetOrderIdOk returns a tuple with the OrderId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderId

`func (o *GetTransactionById200Response) SetOrderId(v string)`

SetOrderId sets OrderId field to given value.

### HasOrderId

`func (o *GetTransactionById200Response) HasOrderId() bool`

HasOrderId returns a boolean if a field has been set.

### SetOrderIdNil

`func (o *GetTransactionById200Response) SetOrderIdNil(b bool)`

 SetOrderIdNil sets the value for OrderId to be an explicit nil

### UnsetOrderId
`func (o *GetTransactionById200Response) UnsetOrderId()`

UnsetOrderId ensures that no value is present for OrderId, not even an explicit nil
### GetCustomerIp

`func (o *GetTransactionById200Response) GetCustomerIp() string`

GetCustomerIp returns the CustomerIp field if non-nil, zero value otherwise.

### GetCustomerIpOk

`func (o *GetTransactionById200Response) GetCustomerIpOk() (*string, bool)`

GetCustomerIpOk returns a tuple with the CustomerIp field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerIp

`func (o *GetTransactionById200Response) SetCustomerIp(v string)`

SetCustomerIp sets CustomerIp field to given value.

### HasCustomerIp

`func (o *GetTransactionById200Response) HasCustomerIp() bool`

HasCustomerIp returns a boolean if a field has been set.

### SetCustomerIpNil

`func (o *GetTransactionById200Response) SetCustomerIpNil(b bool)`

 SetCustomerIpNil sets the value for CustomerIp to be an explicit nil

### UnsetCustomerIp
`func (o *GetTransactionById200Response) UnsetCustomerIp()`

UnsetCustomerIp ensures that no value is present for CustomerIp, not even an explicit nil
### GetEngagedRecoveryState

`func (o *GetTransactionById200Response) GetEngagedRecoveryState() int32`

GetEngagedRecoveryState returns the EngagedRecoveryState field if non-nil, zero value otherwise.

### GetEngagedRecoveryStateOk

`func (o *GetTransactionById200Response) GetEngagedRecoveryStateOk() (*int32, bool)`

GetEngagedRecoveryStateOk returns a tuple with the EngagedRecoveryState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEngagedRecoveryState

`func (o *GetTransactionById200Response) SetEngagedRecoveryState(v int32)`

SetEngagedRecoveryState sets EngagedRecoveryState field to given value.

### HasEngagedRecoveryState

`func (o *GetTransactionById200Response) HasEngagedRecoveryState() bool`

HasEngagedRecoveryState returns a boolean if a field has been set.

### SetEngagedRecoveryStateNil

`func (o *GetTransactionById200Response) SetEngagedRecoveryStateNil(b bool)`

 SetEngagedRecoveryStateNil sets the value for EngagedRecoveryState to be an explicit nil

### UnsetEngagedRecoveryState
`func (o *GetTransactionById200Response) UnsetEngagedRecoveryState()`

UnsetEngagedRecoveryState ensures that no value is present for EngagedRecoveryState, not even an explicit nil
### GetDescription

`func (o *GetTransactionById200Response) GetDescription() string`

GetDescription returns the Description field if non-nil, zero value otherwise.

### GetDescriptionOk

`func (o *GetTransactionById200Response) GetDescriptionOk() (*string, bool)`

GetDescriptionOk returns a tuple with the Description field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDescription

`func (o *GetTransactionById200Response) SetDescription(v string)`

SetDescription sets Description field to given value.

### HasDescription

`func (o *GetTransactionById200Response) HasDescription() bool`

HasDescription returns a boolean if a field has been set.

### SetDescriptionNil

`func (o *GetTransactionById200Response) SetDescriptionNil(b bool)`

 SetDescriptionNil sets the value for Description to be an explicit nil

### UnsetDescription
`func (o *GetTransactionById200Response) UnsetDescription()`

UnsetDescription ensures that no value is present for Description, not even an explicit nil
### GetGatewayFields

`func (o *GetTransactionById200Response) GetGatewayFields() map[string]interface{}`

GetGatewayFields returns the GatewayFields field if non-nil, zero value otherwise.

### GetGatewayFieldsOk

`func (o *GetTransactionById200Response) GetGatewayFieldsOk() (*map[string]interface{}, bool)`

GetGatewayFieldsOk returns a tuple with the GatewayFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayFields

`func (o *GetTransactionById200Response) SetGatewayFields(v map[string]interface{})`

SetGatewayFields sets GatewayFields field to given value.

### HasGatewayFields

`func (o *GetTransactionById200Response) HasGatewayFields() bool`

HasGatewayFields returns a boolean if a field has been set.

### SetGatewayFieldsNil

`func (o *GetTransactionById200Response) SetGatewayFieldsNil(b bool)`

 SetGatewayFieldsNil sets the value for GatewayFields to be an explicit nil

### UnsetGatewayFields
`func (o *GetTransactionById200Response) UnsetGatewayFields()`

UnsetGatewayFields ensures that no value is present for GatewayFields, not even an explicit nil
### GetGatewaySpecificResponseFields

`func (o *GetTransactionById200Response) GetGatewaySpecificResponseFields() map[string]interface{}`

GetGatewaySpecificResponseFields returns the GatewaySpecificResponseFields field if non-nil, zero value otherwise.

### GetGatewaySpecificResponseFieldsOk

`func (o *GetTransactionById200Response) GetGatewaySpecificResponseFieldsOk() (*map[string]interface{}, bool)`

GetGatewaySpecificResponseFieldsOk returns a tuple with the GatewaySpecificResponseFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewaySpecificResponseFields

`func (o *GetTransactionById200Response) SetGatewaySpecificResponseFields(v map[string]interface{})`

SetGatewaySpecificResponseFields sets GatewaySpecificResponseFields field to given value.

### HasGatewaySpecificResponseFields

`func (o *GetTransactionById200Response) HasGatewaySpecificResponseFields() bool`

HasGatewaySpecificResponseFields returns a boolean if a field has been set.

### SetGatewaySpecificResponseFieldsNil

`func (o *GetTransactionById200Response) SetGatewaySpecificResponseFieldsNil(b bool)`

 SetGatewaySpecificResponseFieldsNil sets the value for GatewaySpecificResponseFields to be an explicit nil

### UnsetGatewaySpecificResponseFields
`func (o *GetTransactionById200Response) UnsetGatewaySpecificResponseFields()`

UnsetGatewaySpecificResponseFields ensures that no value is present for GatewaySpecificResponseFields, not even an explicit nil
### GetPaymentPlanData

`func (o *GetTransactionById200Response) GetPaymentPlanData() PaymentPlanData`

GetPaymentPlanData returns the PaymentPlanData field if non-nil, zero value otherwise.

### GetPaymentPlanDataOk

`func (o *GetTransactionById200Response) GetPaymentPlanDataOk() (*PaymentPlanData, bool)`

GetPaymentPlanDataOk returns a tuple with the PaymentPlanData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentPlanData

`func (o *GetTransactionById200Response) SetPaymentPlanData(v PaymentPlanData)`

SetPaymentPlanData sets PaymentPlanData field to given value.

### HasPaymentPlanData

`func (o *GetTransactionById200Response) HasPaymentPlanData() bool`

HasPaymentPlanData returns a boolean if a field has been set.

### SetPaymentPlanDataNil

`func (o *GetTransactionById200Response) SetPaymentPlanDataNil(b bool)`

 SetPaymentPlanDataNil sets the value for PaymentPlanData to be an explicit nil

### UnsetPaymentPlanData
`func (o *GetTransactionById200Response) UnsetPaymentPlanData()`

UnsetPaymentPlanData ensures that no value is present for PaymentPlanData, not even an explicit nil
### GetRecovery

`func (o *GetTransactionById200Response) GetRecovery() Recovery`

GetRecovery returns the Recovery field if non-nil, zero value otherwise.

### GetRecoveryOk

`func (o *GetTransactionById200Response) GetRecoveryOk() (*Recovery, bool)`

GetRecoveryOk returns a tuple with the Recovery field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRecovery

`func (o *GetTransactionById200Response) SetRecovery(v Recovery)`

SetRecovery sets Recovery field to given value.

### HasRecovery

`func (o *GetTransactionById200Response) HasRecovery() bool`

HasRecovery returns a boolean if a field has been set.

### SetRecoveryNil

`func (o *GetTransactionById200Response) SetRecoveryNil(b bool)`

 SetRecoveryNil sets the value for Recovery to be an explicit nil

### UnsetRecovery
`func (o *GetTransactionById200Response) UnsetRecovery()`

UnsetRecovery ensures that no value is present for Recovery, not even an explicit nil
### GetResponse

`func (o *GetTransactionById200Response) GetResponse() TransactionResponseDetails`

GetResponse returns the Response field if non-nil, zero value otherwise.

### GetResponseOk

`func (o *GetTransactionById200Response) GetResponseOk() (*TransactionResponseDetails, bool)`

GetResponseOk returns a tuple with the Response field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponse

`func (o *GetTransactionById200Response) SetResponse(v TransactionResponseDetails)`

SetResponse sets Response field to given value.

### HasResponse

`func (o *GetTransactionById200Response) HasResponse() bool`

HasResponse returns a boolean if a field has been set.

### SetResponseNil

`func (o *GetTransactionById200Response) SetResponseNil(b bool)`

 SetResponseNil sets the value for Response to be an explicit nil

### UnsetResponse
`func (o *GetTransactionById200Response) UnsetResponse()`

UnsetResponse ensures that no value is present for Response, not even an explicit nil
### GetPaymentMethod

`func (o *GetTransactionById200Response) GetPaymentMethod() PaymentMethodResponse`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *GetTransactionById200Response) GetPaymentMethodOk() (*PaymentMethodResponse, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *GetTransactionById200Response) SetPaymentMethod(v PaymentMethodResponse)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *GetTransactionById200Response) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.

### SetPaymentMethodNil

`func (o *GetTransactionById200Response) SetPaymentMethodNil(b bool)`

 SetPaymentMethodNil sets the value for PaymentMethod to be an explicit nil

### UnsetPaymentMethod
`func (o *GetTransactionById200Response) UnsetPaymentMethod()`

UnsetPaymentMethod ensures that no value is present for PaymentMethod, not even an explicit nil
### GetTransaction

`func (o *GetTransactionById200Response) GetTransaction() TransactionResponse`

GetTransaction returns the Transaction field if non-nil, zero value otherwise.

### GetTransactionOk

`func (o *GetTransactionById200Response) GetTransactionOk() (*TransactionResponse, bool)`

GetTransactionOk returns a tuple with the Transaction field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransaction

`func (o *GetTransactionById200Response) SetTransaction(v TransactionResponse)`

SetTransaction sets Transaction field to given value.

### HasTransaction

`func (o *GetTransactionById200Response) HasTransaction() bool`

HasTransaction returns a boolean if a field has been set.

### GetTransactions

`func (o *GetTransactionById200Response) GetTransactions() []TransactionResponse`

GetTransactions returns the Transactions field if non-nil, zero value otherwise.

### GetTransactionsOk

`func (o *GetTransactionById200Response) GetTransactionsOk() (*[]TransactionResponse, bool)`

GetTransactionsOk returns a tuple with the Transactions field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactions

`func (o *GetTransactionById200Response) SetTransactions(v []TransactionResponse)`

SetTransactions sets Transactions field to given value.

### HasTransactions

`func (o *GetTransactionById200Response) HasTransactions() bool`

HasTransactions returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


