# GetTransactionByMerchantTransactionId200Response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**State** | **string** | Always &#x60;pending&#x60; — discriminates this shape from a completed transaction. | 
**MerchantTransactionId** | **NullableString** | Merchant-provided transaction identifier | 
**TransactionType** | Pointer to **NullableString** | Type of transaction performed. Passthrough of the processing platform&#39;s transaction type — not a closed set. Payment operations return \&quot;Charge\&quot;, \&quot;Authorize\&quot;, \&quot;Capture\&quot;, \&quot;Void\&quot; or \&quot;Refund\&quot; (refund cancellation returns \&quot;Refund\&quot;). Transaction lookups can additionally return types created by other platform flows, e.g. \&quot;Verify\&quot;, \&quot;SuccessfulPayment\&quot;, \&quot;RefundedPayment\&quot;, \&quot;CreateCreditCard\&quot;, \&quot;UpdatePaymentMethod\&quot;, \&quot;RedactPaymentMethod\&quot;, \&quot;RecachePaymentMethod\&quot;, \&quot;CreateGatewayPaymentMethod\&quot;. Treat unrecognized values as informational. | [optional] 
**ReceivedAt** | Pointer to **NullableTime** | When the platform recorded the payment intent (ISO 8601) | [optional] 
**Transaction** | Pointer to [**TransactionResponse**](TransactionResponse.md) | The transaction matching the supplied id (the record the non-expanded lookup returns). | [optional] 
**Transactions** | [**[]TransactionResponse**](TransactionResponse.md) | Every transaction in the payment, ordered by transaction date ascending. Capped at 100. | 
**TransactionId** | Pointer to **NullableString** | Unique identifier for the transaction | [optional] 
**TransactionDate** | Pointer to **NullableTime** | Date and time when the transaction was processed (ISO 8601) | [optional] 
**TransactionStatus** | Pointer to **NullableInt32** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**Message** | Pointer to **NullableString** | Human-readable message about the transaction result | [optional] 
**ResponseCode** | Pointer to **NullableString** | Gateway-specific response code | [optional] 
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

### NewGetTransactionByMerchantTransactionId200Response

`func NewGetTransactionByMerchantTransactionId200Response(state string, merchantTransactionId NullableString, transactions []TransactionResponse, ) *GetTransactionByMerchantTransactionId200Response`

NewGetTransactionByMerchantTransactionId200Response instantiates a new GetTransactionByMerchantTransactionId200Response object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewGetTransactionByMerchantTransactionId200ResponseWithDefaults

`func NewGetTransactionByMerchantTransactionId200ResponseWithDefaults() *GetTransactionByMerchantTransactionId200Response`

NewGetTransactionByMerchantTransactionId200ResponseWithDefaults instantiates a new GetTransactionByMerchantTransactionId200Response object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetState

`func (o *GetTransactionByMerchantTransactionId200Response) GetState() string`

GetState returns the State field if non-nil, zero value otherwise.

### GetStateOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetStateOk() (*string, bool)`

GetStateOk returns a tuple with the State field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetState

`func (o *GetTransactionByMerchantTransactionId200Response) SetState(v string)`

SetState sets State field to given value.


### GetMerchantTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.


### SetMerchantTransactionIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetMerchantTransactionIdNil(b bool)`

 SetMerchantTransactionIdNil sets the value for MerchantTransactionId to be an explicit nil

### UnsetMerchantTransactionId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetMerchantTransactionId()`

UnsetMerchantTransactionId ensures that no value is present for MerchantTransactionId, not even an explicit nil
### GetTransactionType

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionType() string`

GetTransactionType returns the TransactionType field if non-nil, zero value otherwise.

### GetTransactionTypeOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionTypeOk() (*string, bool)`

GetTransactionTypeOk returns a tuple with the TransactionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionType

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactionType(v string)`

SetTransactionType sets TransactionType field to given value.

### HasTransactionType

`func (o *GetTransactionByMerchantTransactionId200Response) HasTransactionType() bool`

HasTransactionType returns a boolean if a field has been set.

### SetTransactionTypeNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactionTypeNil(b bool)`

 SetTransactionTypeNil sets the value for TransactionType to be an explicit nil

### UnsetTransactionType
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetTransactionType()`

UnsetTransactionType ensures that no value is present for TransactionType, not even an explicit nil
### GetReceivedAt

`func (o *GetTransactionByMerchantTransactionId200Response) GetReceivedAt() time.Time`

GetReceivedAt returns the ReceivedAt field if non-nil, zero value otherwise.

### GetReceivedAtOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetReceivedAtOk() (*time.Time, bool)`

GetReceivedAtOk returns a tuple with the ReceivedAt field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetReceivedAt

`func (o *GetTransactionByMerchantTransactionId200Response) SetReceivedAt(v time.Time)`

SetReceivedAt sets ReceivedAt field to given value.

### HasReceivedAt

`func (o *GetTransactionByMerchantTransactionId200Response) HasReceivedAt() bool`

HasReceivedAt returns a boolean if a field has been set.

### SetReceivedAtNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetReceivedAtNil(b bool)`

 SetReceivedAtNil sets the value for ReceivedAt to be an explicit nil

### UnsetReceivedAt
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetReceivedAt()`

UnsetReceivedAt ensures that no value is present for ReceivedAt, not even an explicit nil
### GetTransaction

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransaction() TransactionResponse`

GetTransaction returns the Transaction field if non-nil, zero value otherwise.

### GetTransactionOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionOk() (*TransactionResponse, bool)`

GetTransactionOk returns a tuple with the Transaction field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransaction

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransaction(v TransactionResponse)`

SetTransaction sets Transaction field to given value.

### HasTransaction

`func (o *GetTransactionByMerchantTransactionId200Response) HasTransaction() bool`

HasTransaction returns a boolean if a field has been set.

### GetTransactions

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactions() []TransactionResponse`

GetTransactions returns the Transactions field if non-nil, zero value otherwise.

### GetTransactionsOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionsOk() (*[]TransactionResponse, bool)`

GetTransactionsOk returns a tuple with the Transactions field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactions

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactions(v []TransactionResponse)`

SetTransactions sets Transactions field to given value.


### GetTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionId() string`

GetTransactionId returns the TransactionId field if non-nil, zero value otherwise.

### GetTransactionIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionIdOk() (*string, bool)`

GetTransactionIdOk returns a tuple with the TransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactionId(v string)`

SetTransactionId sets TransactionId field to given value.

### HasTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) HasTransactionId() bool`

HasTransactionId returns a boolean if a field has been set.

### SetTransactionIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactionIdNil(b bool)`

 SetTransactionIdNil sets the value for TransactionId to be an explicit nil

### UnsetTransactionId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetTransactionId()`

UnsetTransactionId ensures that no value is present for TransactionId, not even an explicit nil
### GetTransactionDate

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionDate() time.Time`

GetTransactionDate returns the TransactionDate field if non-nil, zero value otherwise.

### GetTransactionDateOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionDateOk() (*time.Time, bool)`

GetTransactionDateOk returns a tuple with the TransactionDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionDate

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactionDate(v time.Time)`

SetTransactionDate sets TransactionDate field to given value.

### HasTransactionDate

`func (o *GetTransactionByMerchantTransactionId200Response) HasTransactionDate() bool`

HasTransactionDate returns a boolean if a field has been set.

### SetTransactionDateNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactionDateNil(b bool)`

 SetTransactionDateNil sets the value for TransactionDate to be an explicit nil

### UnsetTransactionDate
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetTransactionDate()`

UnsetTransactionDate ensures that no value is present for TransactionDate, not even an explicit nil
### GetTransactionStatus

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionStatus() int32`

GetTransactionStatus returns the TransactionStatus field if non-nil, zero value otherwise.

### GetTransactionStatusOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetTransactionStatusOk() (*int32, bool)`

GetTransactionStatusOk returns a tuple with the TransactionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionStatus

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactionStatus(v int32)`

SetTransactionStatus sets TransactionStatus field to given value.

### HasTransactionStatus

`func (o *GetTransactionByMerchantTransactionId200Response) HasTransactionStatus() bool`

HasTransactionStatus returns a boolean if a field has been set.

### SetTransactionStatusNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetTransactionStatusNil(b bool)`

 SetTransactionStatusNil sets the value for TransactionStatus to be an explicit nil

### UnsetTransactionStatus
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetTransactionStatus()`

UnsetTransactionStatus ensures that no value is present for TransactionStatus, not even an explicit nil
### GetMessage

`func (o *GetTransactionByMerchantTransactionId200Response) GetMessage() string`

GetMessage returns the Message field if non-nil, zero value otherwise.

### GetMessageOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetMessageOk() (*string, bool)`

GetMessageOk returns a tuple with the Message field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessage

`func (o *GetTransactionByMerchantTransactionId200Response) SetMessage(v string)`

SetMessage sets Message field to given value.

### HasMessage

`func (o *GetTransactionByMerchantTransactionId200Response) HasMessage() bool`

HasMessage returns a boolean if a field has been set.

### SetMessageNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetMessageNil(b bool)`

 SetMessageNil sets the value for Message to be an explicit nil

### UnsetMessage
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetMessage()`

UnsetMessage ensures that no value is present for Message, not even an explicit nil
### GetResponseCode

`func (o *GetTransactionByMerchantTransactionId200Response) GetResponseCode() string`

GetResponseCode returns the ResponseCode field if non-nil, zero value otherwise.

### GetResponseCodeOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetResponseCodeOk() (*string, bool)`

GetResponseCodeOk returns a tuple with the ResponseCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponseCode

`func (o *GetTransactionByMerchantTransactionId200Response) SetResponseCode(v string)`

SetResponseCode sets ResponseCode field to given value.

### HasResponseCode

`func (o *GetTransactionByMerchantTransactionId200Response) HasResponseCode() bool`

HasResponseCode returns a boolean if a field has been set.

### SetResponseCodeNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetResponseCodeNil(b bool)`

 SetResponseCodeNil sets the value for ResponseCode to be an explicit nil

### UnsetResponseCode
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetResponseCode()`

UnsetResponseCode ensures that no value is present for ResponseCode, not even an explicit nil
### GetCustomerId

`func (o *GetTransactionByMerchantTransactionId200Response) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *GetTransactionByMerchantTransactionId200Response) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *GetTransactionByMerchantTransactionId200Response) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetGatewayRoutingId

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewayRoutingId() string`

GetGatewayRoutingId returns the GatewayRoutingId field if non-nil, zero value otherwise.

### GetGatewayRoutingIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewayRoutingIdOk() (*string, bool)`

GetGatewayRoutingIdOk returns a tuple with the GatewayRoutingId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayRoutingId

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewayRoutingId(v string)`

SetGatewayRoutingId sets GatewayRoutingId field to given value.

### HasGatewayRoutingId

`func (o *GetTransactionByMerchantTransactionId200Response) HasGatewayRoutingId() bool`

HasGatewayRoutingId returns a boolean if a field has been set.

### SetGatewayRoutingIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewayRoutingIdNil(b bool)`

 SetGatewayRoutingIdNil sets the value for GatewayRoutingId to be an explicit nil

### UnsetGatewayRoutingId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetGatewayRoutingId()`

UnsetGatewayRoutingId ensures that no value is present for GatewayRoutingId, not even an explicit nil
### GetCurrency

`func (o *GetTransactionByMerchantTransactionId200Response) GetCurrency() string`

GetCurrency returns the Currency field if non-nil, zero value otherwise.

### GetCurrencyOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetCurrencyOk() (*string, bool)`

GetCurrencyOk returns a tuple with the Currency field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrency

`func (o *GetTransactionByMerchantTransactionId200Response) SetCurrency(v string)`

SetCurrency sets Currency field to given value.

### HasCurrency

`func (o *GetTransactionByMerchantTransactionId200Response) HasCurrency() bool`

HasCurrency returns a boolean if a field has been set.

### SetCurrencyNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetCurrencyNil(b bool)`

 SetCurrencyNil sets the value for Currency to be an explicit nil

### UnsetCurrency
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetCurrency()`

UnsetCurrency ensures that no value is present for Currency, not even an explicit nil
### GetAmount

`func (o *GetTransactionByMerchantTransactionId200Response) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *GetTransactionByMerchantTransactionId200Response) SetAmount(v int64)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *GetTransactionByMerchantTransactionId200Response) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil
### GetGatewayType

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewayType() string`

GetGatewayType returns the GatewayType field if non-nil, zero value otherwise.

### GetGatewayTypeOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewayTypeOk() (*string, bool)`

GetGatewayTypeOk returns a tuple with the GatewayType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayType

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewayType(v string)`

SetGatewayType sets GatewayType field to given value.

### HasGatewayType

`func (o *GetTransactionByMerchantTransactionId200Response) HasGatewayType() bool`

HasGatewayType returns a boolean if a field has been set.

### SetGatewayTypeNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewayTypeNil(b bool)`

 SetGatewayTypeNil sets the value for GatewayType to be an explicit nil

### UnsetGatewayType
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetGatewayType()`

UnsetGatewayType ensures that no value is present for GatewayType, not even an explicit nil
### GetGatewayTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewayTransactionId() string`

GetGatewayTransactionId returns the GatewayTransactionId field if non-nil, zero value otherwise.

### GetGatewayTransactionIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewayTransactionIdOk() (*string, bool)`

GetGatewayTransactionIdOk returns a tuple with the GatewayTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewayTransactionId(v string)`

SetGatewayTransactionId sets GatewayTransactionId field to given value.

### HasGatewayTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) HasGatewayTransactionId() bool`

HasGatewayTransactionId returns a boolean if a field has been set.

### SetGatewayTransactionIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewayTransactionIdNil(b bool)`

 SetGatewayTransactionIdNil sets the value for GatewayTransactionId to be an explicit nil

### UnsetGatewayTransactionId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetGatewayTransactionId()`

UnsetGatewayTransactionId ensures that no value is present for GatewayTransactionId, not even an explicit nil
### GetAcquirerAuthCode

`func (o *GetTransactionByMerchantTransactionId200Response) GetAcquirerAuthCode() string`

GetAcquirerAuthCode returns the AcquirerAuthCode field if non-nil, zero value otherwise.

### GetAcquirerAuthCodeOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetAcquirerAuthCodeOk() (*string, bool)`

GetAcquirerAuthCodeOk returns a tuple with the AcquirerAuthCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcquirerAuthCode

`func (o *GetTransactionByMerchantTransactionId200Response) SetAcquirerAuthCode(v string)`

SetAcquirerAuthCode sets AcquirerAuthCode field to given value.

### HasAcquirerAuthCode

`func (o *GetTransactionByMerchantTransactionId200Response) HasAcquirerAuthCode() bool`

HasAcquirerAuthCode returns a boolean if a field has been set.

### SetAcquirerAuthCodeNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetAcquirerAuthCodeNil(b bool)`

 SetAcquirerAuthCodeNil sets the value for AcquirerAuthCode to be an explicit nil

### UnsetAcquirerAuthCode
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetAcquirerAuthCode()`

UnsetAcquirerAuthCode ensures that no value is present for AcquirerAuthCode, not even an explicit nil
### GetInlineRetryPreviousTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) GetInlineRetryPreviousTransactionId() string`

GetInlineRetryPreviousTransactionId returns the InlineRetryPreviousTransactionId field if non-nil, zero value otherwise.

### GetInlineRetryPreviousTransactionIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetInlineRetryPreviousTransactionIdOk() (*string, bool)`

GetInlineRetryPreviousTransactionIdOk returns a tuple with the InlineRetryPreviousTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInlineRetryPreviousTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) SetInlineRetryPreviousTransactionId(v string)`

SetInlineRetryPreviousTransactionId sets InlineRetryPreviousTransactionId field to given value.

### HasInlineRetryPreviousTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) HasInlineRetryPreviousTransactionId() bool`

HasInlineRetryPreviousTransactionId returns a boolean if a field has been set.

### SetInlineRetryPreviousTransactionIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetInlineRetryPreviousTransactionIdNil(b bool)`

 SetInlineRetryPreviousTransactionIdNil sets the value for InlineRetryPreviousTransactionId to be an explicit nil

### UnsetInlineRetryPreviousTransactionId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetInlineRetryPreviousTransactionId()`

UnsetInlineRetryPreviousTransactionId ensures that no value is present for InlineRetryPreviousTransactionId, not even an explicit nil
### GetInlineRetryPreviousMerchantTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) GetInlineRetryPreviousMerchantTransactionId() string`

GetInlineRetryPreviousMerchantTransactionId returns the InlineRetryPreviousMerchantTransactionId field if non-nil, zero value otherwise.

### GetInlineRetryPreviousMerchantTransactionIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetInlineRetryPreviousMerchantTransactionIdOk() (*string, bool)`

GetInlineRetryPreviousMerchantTransactionIdOk returns a tuple with the InlineRetryPreviousMerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInlineRetryPreviousMerchantTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) SetInlineRetryPreviousMerchantTransactionId(v string)`

SetInlineRetryPreviousMerchantTransactionId sets InlineRetryPreviousMerchantTransactionId field to given value.

### HasInlineRetryPreviousMerchantTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) HasInlineRetryPreviousMerchantTransactionId() bool`

HasInlineRetryPreviousMerchantTransactionId returns a boolean if a field has been set.

### SetInlineRetryPreviousMerchantTransactionIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetInlineRetryPreviousMerchantTransactionIdNil(b bool)`

 SetInlineRetryPreviousMerchantTransactionIdNil sets the value for InlineRetryPreviousMerchantTransactionId to be an explicit nil

### UnsetInlineRetryPreviousMerchantTransactionId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetInlineRetryPreviousMerchantTransactionId()`

UnsetInlineRetryPreviousMerchantTransactionId ensures that no value is present for InlineRetryPreviousMerchantTransactionId, not even an explicit nil
### GetIsInlineRetry

`func (o *GetTransactionByMerchantTransactionId200Response) GetIsInlineRetry() bool`

GetIsInlineRetry returns the IsInlineRetry field if non-nil, zero value otherwise.

### GetIsInlineRetryOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetIsInlineRetryOk() (*bool, bool)`

GetIsInlineRetryOk returns a tuple with the IsInlineRetry field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsInlineRetry

`func (o *GetTransactionByMerchantTransactionId200Response) SetIsInlineRetry(v bool)`

SetIsInlineRetry sets IsInlineRetry field to given value.

### HasIsInlineRetry

`func (o *GetTransactionByMerchantTransactionId200Response) HasIsInlineRetry() bool`

HasIsInlineRetry returns a boolean if a field has been set.

### SetIsInlineRetryNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetIsInlineRetryNil(b bool)`

 SetIsInlineRetryNil sets the value for IsInlineRetry to be an explicit nil

### UnsetIsInlineRetry
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetIsInlineRetry()`

UnsetIsInlineRetry ensures that no value is present for IsInlineRetry, not even an explicit nil
### GetRetryDate

`func (o *GetTransactionByMerchantTransactionId200Response) GetRetryDate() time.Time`

GetRetryDate returns the RetryDate field if non-nil, zero value otherwise.

### GetRetryDateOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetRetryDateOk() (*time.Time, bool)`

GetRetryDateOk returns a tuple with the RetryDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRetryDate

`func (o *GetTransactionByMerchantTransactionId200Response) SetRetryDate(v time.Time)`

SetRetryDate sets RetryDate field to given value.

### HasRetryDate

`func (o *GetTransactionByMerchantTransactionId200Response) HasRetryDate() bool`

HasRetryDate returns a boolean if a field has been set.

### SetRetryDateNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetRetryDateNil(b bool)`

 SetRetryDateNil sets the value for RetryDate to be an explicit nil

### UnsetRetryDate
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetRetryDate()`

UnsetRetryDate ensures that no value is present for RetryDate, not even an explicit nil
### GetMitStoredTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) GetMitStoredTransactionId() string`

GetMitStoredTransactionId returns the MitStoredTransactionId field if non-nil, zero value otherwise.

### GetMitStoredTransactionIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetMitStoredTransactionIdOk() (*string, bool)`

GetMitStoredTransactionIdOk returns a tuple with the MitStoredTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMitStoredTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) SetMitStoredTransactionId(v string)`

SetMitStoredTransactionId sets MitStoredTransactionId field to given value.

### HasMitStoredTransactionId

`func (o *GetTransactionByMerchantTransactionId200Response) HasMitStoredTransactionId() bool`

HasMitStoredTransactionId returns a boolean if a field has been set.

### SetMitStoredTransactionIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetMitStoredTransactionIdNil(b bool)`

 SetMitStoredTransactionIdNil sets the value for MitStoredTransactionId to be an explicit nil

### UnsetMitStoredTransactionId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetMitStoredTransactionId()`

UnsetMitStoredTransactionId ensures that no value is present for MitStoredTransactionId, not even an explicit nil
### GetStoredCredential

`func (o *GetTransactionByMerchantTransactionId200Response) GetStoredCredential() StoredCredentialResponse`

GetStoredCredential returns the StoredCredential field if non-nil, zero value otherwise.

### GetStoredCredentialOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetStoredCredentialOk() (*StoredCredentialResponse, bool)`

GetStoredCredentialOk returns a tuple with the StoredCredential field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStoredCredential

`func (o *GetTransactionByMerchantTransactionId200Response) SetStoredCredential(v StoredCredentialResponse)`

SetStoredCredential sets StoredCredential field to given value.

### HasStoredCredential

`func (o *GetTransactionByMerchantTransactionId200Response) HasStoredCredential() bool`

HasStoredCredential returns a boolean if a field has been set.

### SetStoredCredentialNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetStoredCredentialNil(b bool)`

 SetStoredCredentialNil sets the value for StoredCredential to be an explicit nil

### UnsetStoredCredential
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetStoredCredential()`

UnsetStoredCredential ensures that no value is present for StoredCredential, not even an explicit nil
### GetOrderId

`func (o *GetTransactionByMerchantTransactionId200Response) GetOrderId() string`

GetOrderId returns the OrderId field if non-nil, zero value otherwise.

### GetOrderIdOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetOrderIdOk() (*string, bool)`

GetOrderIdOk returns a tuple with the OrderId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderId

`func (o *GetTransactionByMerchantTransactionId200Response) SetOrderId(v string)`

SetOrderId sets OrderId field to given value.

### HasOrderId

`func (o *GetTransactionByMerchantTransactionId200Response) HasOrderId() bool`

HasOrderId returns a boolean if a field has been set.

### SetOrderIdNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetOrderIdNil(b bool)`

 SetOrderIdNil sets the value for OrderId to be an explicit nil

### UnsetOrderId
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetOrderId()`

UnsetOrderId ensures that no value is present for OrderId, not even an explicit nil
### GetStatementDescriptor

`func (o *GetTransactionByMerchantTransactionId200Response) GetStatementDescriptor() string`

GetStatementDescriptor returns the StatementDescriptor field if non-nil, zero value otherwise.

### GetStatementDescriptorOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetStatementDescriptorOk() (*string, bool)`

GetStatementDescriptorOk returns a tuple with the StatementDescriptor field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStatementDescriptor

`func (o *GetTransactionByMerchantTransactionId200Response) SetStatementDescriptor(v string)`

SetStatementDescriptor sets StatementDescriptor field to given value.

### HasStatementDescriptor

`func (o *GetTransactionByMerchantTransactionId200Response) HasStatementDescriptor() bool`

HasStatementDescriptor returns a boolean if a field has been set.

### SetStatementDescriptorNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetStatementDescriptorNil(b bool)`

 SetStatementDescriptorNil sets the value for StatementDescriptor to be an explicit nil

### UnsetStatementDescriptor
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetStatementDescriptor()`

UnsetStatementDescriptor ensures that no value is present for StatementDescriptor, not even an explicit nil
### GetCustomerIp

`func (o *GetTransactionByMerchantTransactionId200Response) GetCustomerIp() string`

GetCustomerIp returns the CustomerIp field if non-nil, zero value otherwise.

### GetCustomerIpOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetCustomerIpOk() (*string, bool)`

GetCustomerIpOk returns a tuple with the CustomerIp field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerIp

`func (o *GetTransactionByMerchantTransactionId200Response) SetCustomerIp(v string)`

SetCustomerIp sets CustomerIp field to given value.

### HasCustomerIp

`func (o *GetTransactionByMerchantTransactionId200Response) HasCustomerIp() bool`

HasCustomerIp returns a boolean if a field has been set.

### SetCustomerIpNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetCustomerIpNil(b bool)`

 SetCustomerIpNil sets the value for CustomerIp to be an explicit nil

### UnsetCustomerIp
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetCustomerIp()`

UnsetCustomerIp ensures that no value is present for CustomerIp, not even an explicit nil
### GetEngagedRecoveryState

`func (o *GetTransactionByMerchantTransactionId200Response) GetEngagedRecoveryState() int32`

GetEngagedRecoveryState returns the EngagedRecoveryState field if non-nil, zero value otherwise.

### GetEngagedRecoveryStateOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetEngagedRecoveryStateOk() (*int32, bool)`

GetEngagedRecoveryStateOk returns a tuple with the EngagedRecoveryState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEngagedRecoveryState

`func (o *GetTransactionByMerchantTransactionId200Response) SetEngagedRecoveryState(v int32)`

SetEngagedRecoveryState sets EngagedRecoveryState field to given value.

### HasEngagedRecoveryState

`func (o *GetTransactionByMerchantTransactionId200Response) HasEngagedRecoveryState() bool`

HasEngagedRecoveryState returns a boolean if a field has been set.

### SetEngagedRecoveryStateNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetEngagedRecoveryStateNil(b bool)`

 SetEngagedRecoveryStateNil sets the value for EngagedRecoveryState to be an explicit nil

### UnsetEngagedRecoveryState
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetEngagedRecoveryState()`

UnsetEngagedRecoveryState ensures that no value is present for EngagedRecoveryState, not even an explicit nil
### GetDescription

`func (o *GetTransactionByMerchantTransactionId200Response) GetDescription() string`

GetDescription returns the Description field if non-nil, zero value otherwise.

### GetDescriptionOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetDescriptionOk() (*string, bool)`

GetDescriptionOk returns a tuple with the Description field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDescription

`func (o *GetTransactionByMerchantTransactionId200Response) SetDescription(v string)`

SetDescription sets Description field to given value.

### HasDescription

`func (o *GetTransactionByMerchantTransactionId200Response) HasDescription() bool`

HasDescription returns a boolean if a field has been set.

### SetDescriptionNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetDescriptionNil(b bool)`

 SetDescriptionNil sets the value for Description to be an explicit nil

### UnsetDescription
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetDescription()`

UnsetDescription ensures that no value is present for Description, not even an explicit nil
### GetGatewayFields

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewayFields() map[string]interface{}`

GetGatewayFields returns the GatewayFields field if non-nil, zero value otherwise.

### GetGatewayFieldsOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewayFieldsOk() (*map[string]interface{}, bool)`

GetGatewayFieldsOk returns a tuple with the GatewayFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayFields

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewayFields(v map[string]interface{})`

SetGatewayFields sets GatewayFields field to given value.

### HasGatewayFields

`func (o *GetTransactionByMerchantTransactionId200Response) HasGatewayFields() bool`

HasGatewayFields returns a boolean if a field has been set.

### SetGatewayFieldsNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewayFieldsNil(b bool)`

 SetGatewayFieldsNil sets the value for GatewayFields to be an explicit nil

### UnsetGatewayFields
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetGatewayFields()`

UnsetGatewayFields ensures that no value is present for GatewayFields, not even an explicit nil
### GetGatewaySpecificResponseFields

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewaySpecificResponseFields() map[string]interface{}`

GetGatewaySpecificResponseFields returns the GatewaySpecificResponseFields field if non-nil, zero value otherwise.

### GetGatewaySpecificResponseFieldsOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetGatewaySpecificResponseFieldsOk() (*map[string]interface{}, bool)`

GetGatewaySpecificResponseFieldsOk returns a tuple with the GatewaySpecificResponseFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewaySpecificResponseFields

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewaySpecificResponseFields(v map[string]interface{})`

SetGatewaySpecificResponseFields sets GatewaySpecificResponseFields field to given value.

### HasGatewaySpecificResponseFields

`func (o *GetTransactionByMerchantTransactionId200Response) HasGatewaySpecificResponseFields() bool`

HasGatewaySpecificResponseFields returns a boolean if a field has been set.

### SetGatewaySpecificResponseFieldsNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetGatewaySpecificResponseFieldsNil(b bool)`

 SetGatewaySpecificResponseFieldsNil sets the value for GatewaySpecificResponseFields to be an explicit nil

### UnsetGatewaySpecificResponseFields
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetGatewaySpecificResponseFields()`

UnsetGatewaySpecificResponseFields ensures that no value is present for GatewaySpecificResponseFields, not even an explicit nil
### GetPaymentPlanData

`func (o *GetTransactionByMerchantTransactionId200Response) GetPaymentPlanData() PaymentPlanData`

GetPaymentPlanData returns the PaymentPlanData field if non-nil, zero value otherwise.

### GetPaymentPlanDataOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetPaymentPlanDataOk() (*PaymentPlanData, bool)`

GetPaymentPlanDataOk returns a tuple with the PaymentPlanData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentPlanData

`func (o *GetTransactionByMerchantTransactionId200Response) SetPaymentPlanData(v PaymentPlanData)`

SetPaymentPlanData sets PaymentPlanData field to given value.

### HasPaymentPlanData

`func (o *GetTransactionByMerchantTransactionId200Response) HasPaymentPlanData() bool`

HasPaymentPlanData returns a boolean if a field has been set.

### SetPaymentPlanDataNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetPaymentPlanDataNil(b bool)`

 SetPaymentPlanDataNil sets the value for PaymentPlanData to be an explicit nil

### UnsetPaymentPlanData
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetPaymentPlanData()`

UnsetPaymentPlanData ensures that no value is present for PaymentPlanData, not even an explicit nil
### GetRecovery

`func (o *GetTransactionByMerchantTransactionId200Response) GetRecovery() Recovery`

GetRecovery returns the Recovery field if non-nil, zero value otherwise.

### GetRecoveryOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetRecoveryOk() (*Recovery, bool)`

GetRecoveryOk returns a tuple with the Recovery field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRecovery

`func (o *GetTransactionByMerchantTransactionId200Response) SetRecovery(v Recovery)`

SetRecovery sets Recovery field to given value.

### HasRecovery

`func (o *GetTransactionByMerchantTransactionId200Response) HasRecovery() bool`

HasRecovery returns a boolean if a field has been set.

### SetRecoveryNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetRecoveryNil(b bool)`

 SetRecoveryNil sets the value for Recovery to be an explicit nil

### UnsetRecovery
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetRecovery()`

UnsetRecovery ensures that no value is present for Recovery, not even an explicit nil
### GetResponse

`func (o *GetTransactionByMerchantTransactionId200Response) GetResponse() TransactionResponseDetails`

GetResponse returns the Response field if non-nil, zero value otherwise.

### GetResponseOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetResponseOk() (*TransactionResponseDetails, bool)`

GetResponseOk returns a tuple with the Response field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponse

`func (o *GetTransactionByMerchantTransactionId200Response) SetResponse(v TransactionResponseDetails)`

SetResponse sets Response field to given value.

### HasResponse

`func (o *GetTransactionByMerchantTransactionId200Response) HasResponse() bool`

HasResponse returns a boolean if a field has been set.

### SetResponseNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetResponseNil(b bool)`

 SetResponseNil sets the value for Response to be an explicit nil

### UnsetResponse
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetResponse()`

UnsetResponse ensures that no value is present for Response, not even an explicit nil
### GetPaymentMethod

`func (o *GetTransactionByMerchantTransactionId200Response) GetPaymentMethod() PaymentMethodResponse`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *GetTransactionByMerchantTransactionId200Response) GetPaymentMethodOk() (*PaymentMethodResponse, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *GetTransactionByMerchantTransactionId200Response) SetPaymentMethod(v PaymentMethodResponse)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *GetTransactionByMerchantTransactionId200Response) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.

### SetPaymentMethodNil

`func (o *GetTransactionByMerchantTransactionId200Response) SetPaymentMethodNil(b bool)`

 SetPaymentMethodNil sets the value for PaymentMethod to be an explicit nil

### UnsetPaymentMethod
`func (o *GetTransactionByMerchantTransactionId200Response) UnsetPaymentMethod()`

UnsetPaymentMethod ensures that no value is present for PaymentMethod, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


