# ListTransactions200ResponseInner

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | **NullableString** | Unique transaction identifier | 
**TransactionDate** | Pointer to **time.Time** | Date and time when the transaction was processed (ISO 8601) | [optional] 
**TransactionStatus** | Pointer to **int32** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**ResponseCode** | Pointer to **NullableString** | Response code from the processing result | [optional] 
**Message** | Pointer to **NullableString** | Human-readable message about the transaction result | [optional] 
**TransactionType** | Pointer to **NullableString** | Type of transaction performed: Charge, PreAuth (an authorization), Capture, Void, Refund, RefundedPayment, SuccessfulPayment (a payment recorded through &#x60;/notify&#x60;), Verify, or, for a payment-method operation, CreateCreditCard, CreateGatewayPaymentMethod, UpdatePaymentMethod, RedactPaymentMethod or RecachePaymentMethod | [optional] 
**RetryDate** | Pointer to **NullableTime** | Scheduled retry date, if applicable | [optional] 
**Amount** | Pointer to **NullableInt64** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**InitialMerchantTransactionId** | Pointer to **NullableString** | The merchant transaction ID of the initial transaction in the recovery chain | [optional] 
**StorageState** | Pointer to **NullableString** | Storage state of the payment method. Returned on rows Olympus records (simplified and detailed); rows Backbone records report it in &#x60;paymentMethodStorageState&#x60; instead. | [optional] 
**CompletionStatus** | Pointer to **NullableString** | Recovery completion status of the transaction (e.g., RecoverySuccessful, RecoveryDeclined) | [optional] 
**GatewaySpecificResponseFields** | Pointer to **map[string]interface{}** | Gateway-specific response fields returned directly by the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle).  | [optional] 
**GatewaySpecificFields** | Pointer to **map[string]interface{}** | Gateway-specific request fields sent to the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle).  | [optional] 
**AcquirerAuthCode** | Pointer to **NullableString** | Authorization code returned by the acquiring bank | [optional] 
**GatewayTransactionId** | Pointer to **NullableString** | Gateway-specific transaction identifier | [optional] 
**GatewayPaymentMethodId** | Pointer to **NullableString** | Gateway-specific payment method identifier | [optional] 
**EngagedRecoveryState** | Pointer to **NullableInt32** | Recovery state indicator (null/0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional] 
**CurrencyCode** | Pointer to **NullableString** | Transaction currency code (ISO 4217) | [optional] 
**MerchantTransactionId** | Pointer to **NullableString** | Merchant-provided transaction identifier | [optional] 
**MerchantAccountReferenceId** | Pointer to **NullableString** | Merchant account reference identifier | [optional] 
**CustomerId** | Pointer to **NullableString** | Customer identifier associated with the transaction | [optional] 
**OrderId** | Pointer to **NullableString** | Order identifier from the merchant system | [optional] 
**StatementDescriptor** | Pointer to **NullableString** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. | [optional] 
**PaymentMethodId** | Pointer to **NullableString** | Payment method identifier used for the transaction | [optional] 
**PaymentMethodStorageState** | Pointer to **NullableString** | Storage state of the payment method. Returned on detailed rows and on simplified rows Backbone records; a simplified row Olympus records reports it in &#x60;storageState&#x60; instead. | [optional] 
**PaymentMethodType** | Pointer to **NullableString** | Type of payment method used | [optional] 
**PaymentMethodMerchantAccountReferenceId** | Pointer to **NullableString** | Merchant account reference ID associated with the payment method | [optional] 
**VaultToken** | Pointer to **NullableString** | Vault token for the credential this transaction ran against, reported flat on the row alongside the other &#x60;paymentMethod*&#x60; fields. Present only on rows that ran against a vault credential — omitted, not null or empty, on every other row. In practice this means the detailed response type: simplified rows carry no payment-method data to report a token from. | [optional] 
**ErrorCode** | Pointer to **NullableString** | Error code from the gateway response | [optional] 
**ErrorDetail** | Pointer to **NullableString** | Detailed error message from the gateway response | [optional] 
**AvsCode** | Pointer to **NullableString** | Address Verification System result code from the gateway | [optional] 
**Gateway** | Pointer to [**NullableTransactionGateway**](TransactionGateway.md) |  | [optional] 
**PaymentMethod** | Pointer to [**NullablePaymentMethodResponse**](PaymentMethodResponse.md) | Not returned on a flat row. The payment method of a payment-method operation is reported in &#x60;transaction.paymentMethod&#x60; of a &#x60;TransactionListPaymentMethodItem&#x60;. | [optional] 
**Transaction** | [**TransactionListPaymentMethodItemTransaction**](TransactionListPaymentMethodItemTransaction.md) |  | 

## Methods

### NewListTransactions200ResponseInner

`func NewListTransactions200ResponseInner(transactionId NullableString, transaction TransactionListPaymentMethodItemTransaction, ) *ListTransactions200ResponseInner`

NewListTransactions200ResponseInner instantiates a new ListTransactions200ResponseInner object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewListTransactions200ResponseInnerWithDefaults

`func NewListTransactions200ResponseInnerWithDefaults() *ListTransactions200ResponseInner`

NewListTransactions200ResponseInnerWithDefaults instantiates a new ListTransactions200ResponseInner object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionId

`func (o *ListTransactions200ResponseInner) GetTransactionId() string`

GetTransactionId returns the TransactionId field if non-nil, zero value otherwise.

### GetTransactionIdOk

`func (o *ListTransactions200ResponseInner) GetTransactionIdOk() (*string, bool)`

GetTransactionIdOk returns a tuple with the TransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionId

`func (o *ListTransactions200ResponseInner) SetTransactionId(v string)`

SetTransactionId sets TransactionId field to given value.


### SetTransactionIdNil

`func (o *ListTransactions200ResponseInner) SetTransactionIdNil(b bool)`

 SetTransactionIdNil sets the value for TransactionId to be an explicit nil

### UnsetTransactionId
`func (o *ListTransactions200ResponseInner) UnsetTransactionId()`

UnsetTransactionId ensures that no value is present for TransactionId, not even an explicit nil
### GetTransactionDate

`func (o *ListTransactions200ResponseInner) GetTransactionDate() time.Time`

GetTransactionDate returns the TransactionDate field if non-nil, zero value otherwise.

### GetTransactionDateOk

`func (o *ListTransactions200ResponseInner) GetTransactionDateOk() (*time.Time, bool)`

GetTransactionDateOk returns a tuple with the TransactionDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionDate

`func (o *ListTransactions200ResponseInner) SetTransactionDate(v time.Time)`

SetTransactionDate sets TransactionDate field to given value.

### HasTransactionDate

`func (o *ListTransactions200ResponseInner) HasTransactionDate() bool`

HasTransactionDate returns a boolean if a field has been set.

### GetTransactionStatus

`func (o *ListTransactions200ResponseInner) GetTransactionStatus() int32`

GetTransactionStatus returns the TransactionStatus field if non-nil, zero value otherwise.

### GetTransactionStatusOk

`func (o *ListTransactions200ResponseInner) GetTransactionStatusOk() (*int32, bool)`

GetTransactionStatusOk returns a tuple with the TransactionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionStatus

`func (o *ListTransactions200ResponseInner) SetTransactionStatus(v int32)`

SetTransactionStatus sets TransactionStatus field to given value.

### HasTransactionStatus

`func (o *ListTransactions200ResponseInner) HasTransactionStatus() bool`

HasTransactionStatus returns a boolean if a field has been set.

### GetResponseCode

`func (o *ListTransactions200ResponseInner) GetResponseCode() string`

GetResponseCode returns the ResponseCode field if non-nil, zero value otherwise.

### GetResponseCodeOk

`func (o *ListTransactions200ResponseInner) GetResponseCodeOk() (*string, bool)`

GetResponseCodeOk returns a tuple with the ResponseCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponseCode

`func (o *ListTransactions200ResponseInner) SetResponseCode(v string)`

SetResponseCode sets ResponseCode field to given value.

### HasResponseCode

`func (o *ListTransactions200ResponseInner) HasResponseCode() bool`

HasResponseCode returns a boolean if a field has been set.

### SetResponseCodeNil

`func (o *ListTransactions200ResponseInner) SetResponseCodeNil(b bool)`

 SetResponseCodeNil sets the value for ResponseCode to be an explicit nil

### UnsetResponseCode
`func (o *ListTransactions200ResponseInner) UnsetResponseCode()`

UnsetResponseCode ensures that no value is present for ResponseCode, not even an explicit nil
### GetMessage

`func (o *ListTransactions200ResponseInner) GetMessage() string`

GetMessage returns the Message field if non-nil, zero value otherwise.

### GetMessageOk

`func (o *ListTransactions200ResponseInner) GetMessageOk() (*string, bool)`

GetMessageOk returns a tuple with the Message field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessage

`func (o *ListTransactions200ResponseInner) SetMessage(v string)`

SetMessage sets Message field to given value.

### HasMessage

`func (o *ListTransactions200ResponseInner) HasMessage() bool`

HasMessage returns a boolean if a field has been set.

### SetMessageNil

`func (o *ListTransactions200ResponseInner) SetMessageNil(b bool)`

 SetMessageNil sets the value for Message to be an explicit nil

### UnsetMessage
`func (o *ListTransactions200ResponseInner) UnsetMessage()`

UnsetMessage ensures that no value is present for Message, not even an explicit nil
### GetTransactionType

`func (o *ListTransactions200ResponseInner) GetTransactionType() string`

GetTransactionType returns the TransactionType field if non-nil, zero value otherwise.

### GetTransactionTypeOk

`func (o *ListTransactions200ResponseInner) GetTransactionTypeOk() (*string, bool)`

GetTransactionTypeOk returns a tuple with the TransactionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionType

`func (o *ListTransactions200ResponseInner) SetTransactionType(v string)`

SetTransactionType sets TransactionType field to given value.

### HasTransactionType

`func (o *ListTransactions200ResponseInner) HasTransactionType() bool`

HasTransactionType returns a boolean if a field has been set.

### SetTransactionTypeNil

`func (o *ListTransactions200ResponseInner) SetTransactionTypeNil(b bool)`

 SetTransactionTypeNil sets the value for TransactionType to be an explicit nil

### UnsetTransactionType
`func (o *ListTransactions200ResponseInner) UnsetTransactionType()`

UnsetTransactionType ensures that no value is present for TransactionType, not even an explicit nil
### GetRetryDate

`func (o *ListTransactions200ResponseInner) GetRetryDate() time.Time`

GetRetryDate returns the RetryDate field if non-nil, zero value otherwise.

### GetRetryDateOk

`func (o *ListTransactions200ResponseInner) GetRetryDateOk() (*time.Time, bool)`

GetRetryDateOk returns a tuple with the RetryDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRetryDate

`func (o *ListTransactions200ResponseInner) SetRetryDate(v time.Time)`

SetRetryDate sets RetryDate field to given value.

### HasRetryDate

`func (o *ListTransactions200ResponseInner) HasRetryDate() bool`

HasRetryDate returns a boolean if a field has been set.

### SetRetryDateNil

`func (o *ListTransactions200ResponseInner) SetRetryDateNil(b bool)`

 SetRetryDateNil sets the value for RetryDate to be an explicit nil

### UnsetRetryDate
`func (o *ListTransactions200ResponseInner) UnsetRetryDate()`

UnsetRetryDate ensures that no value is present for RetryDate, not even an explicit nil
### GetAmount

`func (o *ListTransactions200ResponseInner) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *ListTransactions200ResponseInner) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *ListTransactions200ResponseInner) SetAmount(v int64)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *ListTransactions200ResponseInner) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *ListTransactions200ResponseInner) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *ListTransactions200ResponseInner) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil
### GetInitialMerchantTransactionId

`func (o *ListTransactions200ResponseInner) GetInitialMerchantTransactionId() string`

GetInitialMerchantTransactionId returns the InitialMerchantTransactionId field if non-nil, zero value otherwise.

### GetInitialMerchantTransactionIdOk

`func (o *ListTransactions200ResponseInner) GetInitialMerchantTransactionIdOk() (*string, bool)`

GetInitialMerchantTransactionIdOk returns a tuple with the InitialMerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInitialMerchantTransactionId

`func (o *ListTransactions200ResponseInner) SetInitialMerchantTransactionId(v string)`

SetInitialMerchantTransactionId sets InitialMerchantTransactionId field to given value.

### HasInitialMerchantTransactionId

`func (o *ListTransactions200ResponseInner) HasInitialMerchantTransactionId() bool`

HasInitialMerchantTransactionId returns a boolean if a field has been set.

### SetInitialMerchantTransactionIdNil

`func (o *ListTransactions200ResponseInner) SetInitialMerchantTransactionIdNil(b bool)`

 SetInitialMerchantTransactionIdNil sets the value for InitialMerchantTransactionId to be an explicit nil

### UnsetInitialMerchantTransactionId
`func (o *ListTransactions200ResponseInner) UnsetInitialMerchantTransactionId()`

UnsetInitialMerchantTransactionId ensures that no value is present for InitialMerchantTransactionId, not even an explicit nil
### GetStorageState

`func (o *ListTransactions200ResponseInner) GetStorageState() string`

GetStorageState returns the StorageState field if non-nil, zero value otherwise.

### GetStorageStateOk

`func (o *ListTransactions200ResponseInner) GetStorageStateOk() (*string, bool)`

GetStorageStateOk returns a tuple with the StorageState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStorageState

`func (o *ListTransactions200ResponseInner) SetStorageState(v string)`

SetStorageState sets StorageState field to given value.

### HasStorageState

`func (o *ListTransactions200ResponseInner) HasStorageState() bool`

HasStorageState returns a boolean if a field has been set.

### SetStorageStateNil

`func (o *ListTransactions200ResponseInner) SetStorageStateNil(b bool)`

 SetStorageStateNil sets the value for StorageState to be an explicit nil

### UnsetStorageState
`func (o *ListTransactions200ResponseInner) UnsetStorageState()`

UnsetStorageState ensures that no value is present for StorageState, not even an explicit nil
### GetCompletionStatus

`func (o *ListTransactions200ResponseInner) GetCompletionStatus() string`

GetCompletionStatus returns the CompletionStatus field if non-nil, zero value otherwise.

### GetCompletionStatusOk

`func (o *ListTransactions200ResponseInner) GetCompletionStatusOk() (*string, bool)`

GetCompletionStatusOk returns a tuple with the CompletionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCompletionStatus

`func (o *ListTransactions200ResponseInner) SetCompletionStatus(v string)`

SetCompletionStatus sets CompletionStatus field to given value.

### HasCompletionStatus

`func (o *ListTransactions200ResponseInner) HasCompletionStatus() bool`

HasCompletionStatus returns a boolean if a field has been set.

### SetCompletionStatusNil

`func (o *ListTransactions200ResponseInner) SetCompletionStatusNil(b bool)`

 SetCompletionStatusNil sets the value for CompletionStatus to be an explicit nil

### UnsetCompletionStatus
`func (o *ListTransactions200ResponseInner) UnsetCompletionStatus()`

UnsetCompletionStatus ensures that no value is present for CompletionStatus, not even an explicit nil
### GetGatewaySpecificResponseFields

`func (o *ListTransactions200ResponseInner) GetGatewaySpecificResponseFields() map[string]interface{}`

GetGatewaySpecificResponseFields returns the GatewaySpecificResponseFields field if non-nil, zero value otherwise.

### GetGatewaySpecificResponseFieldsOk

`func (o *ListTransactions200ResponseInner) GetGatewaySpecificResponseFieldsOk() (*map[string]interface{}, bool)`

GetGatewaySpecificResponseFieldsOk returns a tuple with the GatewaySpecificResponseFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewaySpecificResponseFields

`func (o *ListTransactions200ResponseInner) SetGatewaySpecificResponseFields(v map[string]interface{})`

SetGatewaySpecificResponseFields sets GatewaySpecificResponseFields field to given value.

### HasGatewaySpecificResponseFields

`func (o *ListTransactions200ResponseInner) HasGatewaySpecificResponseFields() bool`

HasGatewaySpecificResponseFields returns a boolean if a field has been set.

### SetGatewaySpecificResponseFieldsNil

`func (o *ListTransactions200ResponseInner) SetGatewaySpecificResponseFieldsNil(b bool)`

 SetGatewaySpecificResponseFieldsNil sets the value for GatewaySpecificResponseFields to be an explicit nil

### UnsetGatewaySpecificResponseFields
`func (o *ListTransactions200ResponseInner) UnsetGatewaySpecificResponseFields()`

UnsetGatewaySpecificResponseFields ensures that no value is present for GatewaySpecificResponseFields, not even an explicit nil
### GetGatewaySpecificFields

`func (o *ListTransactions200ResponseInner) GetGatewaySpecificFields() map[string]interface{}`

GetGatewaySpecificFields returns the GatewaySpecificFields field if non-nil, zero value otherwise.

### GetGatewaySpecificFieldsOk

`func (o *ListTransactions200ResponseInner) GetGatewaySpecificFieldsOk() (*map[string]interface{}, bool)`

GetGatewaySpecificFieldsOk returns a tuple with the GatewaySpecificFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewaySpecificFields

`func (o *ListTransactions200ResponseInner) SetGatewaySpecificFields(v map[string]interface{})`

SetGatewaySpecificFields sets GatewaySpecificFields field to given value.

### HasGatewaySpecificFields

`func (o *ListTransactions200ResponseInner) HasGatewaySpecificFields() bool`

HasGatewaySpecificFields returns a boolean if a field has been set.

### SetGatewaySpecificFieldsNil

`func (o *ListTransactions200ResponseInner) SetGatewaySpecificFieldsNil(b bool)`

 SetGatewaySpecificFieldsNil sets the value for GatewaySpecificFields to be an explicit nil

### UnsetGatewaySpecificFields
`func (o *ListTransactions200ResponseInner) UnsetGatewaySpecificFields()`

UnsetGatewaySpecificFields ensures that no value is present for GatewaySpecificFields, not even an explicit nil
### GetAcquirerAuthCode

`func (o *ListTransactions200ResponseInner) GetAcquirerAuthCode() string`

GetAcquirerAuthCode returns the AcquirerAuthCode field if non-nil, zero value otherwise.

### GetAcquirerAuthCodeOk

`func (o *ListTransactions200ResponseInner) GetAcquirerAuthCodeOk() (*string, bool)`

GetAcquirerAuthCodeOk returns a tuple with the AcquirerAuthCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcquirerAuthCode

`func (o *ListTransactions200ResponseInner) SetAcquirerAuthCode(v string)`

SetAcquirerAuthCode sets AcquirerAuthCode field to given value.

### HasAcquirerAuthCode

`func (o *ListTransactions200ResponseInner) HasAcquirerAuthCode() bool`

HasAcquirerAuthCode returns a boolean if a field has been set.

### SetAcquirerAuthCodeNil

`func (o *ListTransactions200ResponseInner) SetAcquirerAuthCodeNil(b bool)`

 SetAcquirerAuthCodeNil sets the value for AcquirerAuthCode to be an explicit nil

### UnsetAcquirerAuthCode
`func (o *ListTransactions200ResponseInner) UnsetAcquirerAuthCode()`

UnsetAcquirerAuthCode ensures that no value is present for AcquirerAuthCode, not even an explicit nil
### GetGatewayTransactionId

`func (o *ListTransactions200ResponseInner) GetGatewayTransactionId() string`

GetGatewayTransactionId returns the GatewayTransactionId field if non-nil, zero value otherwise.

### GetGatewayTransactionIdOk

`func (o *ListTransactions200ResponseInner) GetGatewayTransactionIdOk() (*string, bool)`

GetGatewayTransactionIdOk returns a tuple with the GatewayTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayTransactionId

`func (o *ListTransactions200ResponseInner) SetGatewayTransactionId(v string)`

SetGatewayTransactionId sets GatewayTransactionId field to given value.

### HasGatewayTransactionId

`func (o *ListTransactions200ResponseInner) HasGatewayTransactionId() bool`

HasGatewayTransactionId returns a boolean if a field has been set.

### SetGatewayTransactionIdNil

`func (o *ListTransactions200ResponseInner) SetGatewayTransactionIdNil(b bool)`

 SetGatewayTransactionIdNil sets the value for GatewayTransactionId to be an explicit nil

### UnsetGatewayTransactionId
`func (o *ListTransactions200ResponseInner) UnsetGatewayTransactionId()`

UnsetGatewayTransactionId ensures that no value is present for GatewayTransactionId, not even an explicit nil
### GetGatewayPaymentMethodId

`func (o *ListTransactions200ResponseInner) GetGatewayPaymentMethodId() string`

GetGatewayPaymentMethodId returns the GatewayPaymentMethodId field if non-nil, zero value otherwise.

### GetGatewayPaymentMethodIdOk

`func (o *ListTransactions200ResponseInner) GetGatewayPaymentMethodIdOk() (*string, bool)`

GetGatewayPaymentMethodIdOk returns a tuple with the GatewayPaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayPaymentMethodId

`func (o *ListTransactions200ResponseInner) SetGatewayPaymentMethodId(v string)`

SetGatewayPaymentMethodId sets GatewayPaymentMethodId field to given value.

### HasGatewayPaymentMethodId

`func (o *ListTransactions200ResponseInner) HasGatewayPaymentMethodId() bool`

HasGatewayPaymentMethodId returns a boolean if a field has been set.

### SetGatewayPaymentMethodIdNil

`func (o *ListTransactions200ResponseInner) SetGatewayPaymentMethodIdNil(b bool)`

 SetGatewayPaymentMethodIdNil sets the value for GatewayPaymentMethodId to be an explicit nil

### UnsetGatewayPaymentMethodId
`func (o *ListTransactions200ResponseInner) UnsetGatewayPaymentMethodId()`

UnsetGatewayPaymentMethodId ensures that no value is present for GatewayPaymentMethodId, not even an explicit nil
### GetEngagedRecoveryState

`func (o *ListTransactions200ResponseInner) GetEngagedRecoveryState() int32`

GetEngagedRecoveryState returns the EngagedRecoveryState field if non-nil, zero value otherwise.

### GetEngagedRecoveryStateOk

`func (o *ListTransactions200ResponseInner) GetEngagedRecoveryStateOk() (*int32, bool)`

GetEngagedRecoveryStateOk returns a tuple with the EngagedRecoveryState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEngagedRecoveryState

`func (o *ListTransactions200ResponseInner) SetEngagedRecoveryState(v int32)`

SetEngagedRecoveryState sets EngagedRecoveryState field to given value.

### HasEngagedRecoveryState

`func (o *ListTransactions200ResponseInner) HasEngagedRecoveryState() bool`

HasEngagedRecoveryState returns a boolean if a field has been set.

### SetEngagedRecoveryStateNil

`func (o *ListTransactions200ResponseInner) SetEngagedRecoveryStateNil(b bool)`

 SetEngagedRecoveryStateNil sets the value for EngagedRecoveryState to be an explicit nil

### UnsetEngagedRecoveryState
`func (o *ListTransactions200ResponseInner) UnsetEngagedRecoveryState()`

UnsetEngagedRecoveryState ensures that no value is present for EngagedRecoveryState, not even an explicit nil
### GetCurrencyCode

`func (o *ListTransactions200ResponseInner) GetCurrencyCode() string`

GetCurrencyCode returns the CurrencyCode field if non-nil, zero value otherwise.

### GetCurrencyCodeOk

`func (o *ListTransactions200ResponseInner) GetCurrencyCodeOk() (*string, bool)`

GetCurrencyCodeOk returns a tuple with the CurrencyCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrencyCode

`func (o *ListTransactions200ResponseInner) SetCurrencyCode(v string)`

SetCurrencyCode sets CurrencyCode field to given value.

### HasCurrencyCode

`func (o *ListTransactions200ResponseInner) HasCurrencyCode() bool`

HasCurrencyCode returns a boolean if a field has been set.

### SetCurrencyCodeNil

`func (o *ListTransactions200ResponseInner) SetCurrencyCodeNil(b bool)`

 SetCurrencyCodeNil sets the value for CurrencyCode to be an explicit nil

### UnsetCurrencyCode
`func (o *ListTransactions200ResponseInner) UnsetCurrencyCode()`

UnsetCurrencyCode ensures that no value is present for CurrencyCode, not even an explicit nil
### GetMerchantTransactionId

`func (o *ListTransactions200ResponseInner) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *ListTransactions200ResponseInner) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *ListTransactions200ResponseInner) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.

### HasMerchantTransactionId

`func (o *ListTransactions200ResponseInner) HasMerchantTransactionId() bool`

HasMerchantTransactionId returns a boolean if a field has been set.

### SetMerchantTransactionIdNil

`func (o *ListTransactions200ResponseInner) SetMerchantTransactionIdNil(b bool)`

 SetMerchantTransactionIdNil sets the value for MerchantTransactionId to be an explicit nil

### UnsetMerchantTransactionId
`func (o *ListTransactions200ResponseInner) UnsetMerchantTransactionId()`

UnsetMerchantTransactionId ensures that no value is present for MerchantTransactionId, not even an explicit nil
### GetMerchantAccountReferenceId

`func (o *ListTransactions200ResponseInner) GetMerchantAccountReferenceId() string`

GetMerchantAccountReferenceId returns the MerchantAccountReferenceId field if non-nil, zero value otherwise.

### GetMerchantAccountReferenceIdOk

`func (o *ListTransactions200ResponseInner) GetMerchantAccountReferenceIdOk() (*string, bool)`

GetMerchantAccountReferenceIdOk returns a tuple with the MerchantAccountReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantAccountReferenceId

`func (o *ListTransactions200ResponseInner) SetMerchantAccountReferenceId(v string)`

SetMerchantAccountReferenceId sets MerchantAccountReferenceId field to given value.

### HasMerchantAccountReferenceId

`func (o *ListTransactions200ResponseInner) HasMerchantAccountReferenceId() bool`

HasMerchantAccountReferenceId returns a boolean if a field has been set.

### SetMerchantAccountReferenceIdNil

`func (o *ListTransactions200ResponseInner) SetMerchantAccountReferenceIdNil(b bool)`

 SetMerchantAccountReferenceIdNil sets the value for MerchantAccountReferenceId to be an explicit nil

### UnsetMerchantAccountReferenceId
`func (o *ListTransactions200ResponseInner) UnsetMerchantAccountReferenceId()`

UnsetMerchantAccountReferenceId ensures that no value is present for MerchantAccountReferenceId, not even an explicit nil
### GetCustomerId

`func (o *ListTransactions200ResponseInner) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *ListTransactions200ResponseInner) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *ListTransactions200ResponseInner) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *ListTransactions200ResponseInner) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *ListTransactions200ResponseInner) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *ListTransactions200ResponseInner) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetOrderId

`func (o *ListTransactions200ResponseInner) GetOrderId() string`

GetOrderId returns the OrderId field if non-nil, zero value otherwise.

### GetOrderIdOk

`func (o *ListTransactions200ResponseInner) GetOrderIdOk() (*string, bool)`

GetOrderIdOk returns a tuple with the OrderId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderId

`func (o *ListTransactions200ResponseInner) SetOrderId(v string)`

SetOrderId sets OrderId field to given value.

### HasOrderId

`func (o *ListTransactions200ResponseInner) HasOrderId() bool`

HasOrderId returns a boolean if a field has been set.

### SetOrderIdNil

`func (o *ListTransactions200ResponseInner) SetOrderIdNil(b bool)`

 SetOrderIdNil sets the value for OrderId to be an explicit nil

### UnsetOrderId
`func (o *ListTransactions200ResponseInner) UnsetOrderId()`

UnsetOrderId ensures that no value is present for OrderId, not even an explicit nil
### GetStatementDescriptor

`func (o *ListTransactions200ResponseInner) GetStatementDescriptor() string`

GetStatementDescriptor returns the StatementDescriptor field if non-nil, zero value otherwise.

### GetStatementDescriptorOk

`func (o *ListTransactions200ResponseInner) GetStatementDescriptorOk() (*string, bool)`

GetStatementDescriptorOk returns a tuple with the StatementDescriptor field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStatementDescriptor

`func (o *ListTransactions200ResponseInner) SetStatementDescriptor(v string)`

SetStatementDescriptor sets StatementDescriptor field to given value.

### HasStatementDescriptor

`func (o *ListTransactions200ResponseInner) HasStatementDescriptor() bool`

HasStatementDescriptor returns a boolean if a field has been set.

### SetStatementDescriptorNil

`func (o *ListTransactions200ResponseInner) SetStatementDescriptorNil(b bool)`

 SetStatementDescriptorNil sets the value for StatementDescriptor to be an explicit nil

### UnsetStatementDescriptor
`func (o *ListTransactions200ResponseInner) UnsetStatementDescriptor()`

UnsetStatementDescriptor ensures that no value is present for StatementDescriptor, not even an explicit nil
### GetPaymentMethodId

`func (o *ListTransactions200ResponseInner) GetPaymentMethodId() string`

GetPaymentMethodId returns the PaymentMethodId field if non-nil, zero value otherwise.

### GetPaymentMethodIdOk

`func (o *ListTransactions200ResponseInner) GetPaymentMethodIdOk() (*string, bool)`

GetPaymentMethodIdOk returns a tuple with the PaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodId

`func (o *ListTransactions200ResponseInner) SetPaymentMethodId(v string)`

SetPaymentMethodId sets PaymentMethodId field to given value.

### HasPaymentMethodId

`func (o *ListTransactions200ResponseInner) HasPaymentMethodId() bool`

HasPaymentMethodId returns a boolean if a field has been set.

### SetPaymentMethodIdNil

`func (o *ListTransactions200ResponseInner) SetPaymentMethodIdNil(b bool)`

 SetPaymentMethodIdNil sets the value for PaymentMethodId to be an explicit nil

### UnsetPaymentMethodId
`func (o *ListTransactions200ResponseInner) UnsetPaymentMethodId()`

UnsetPaymentMethodId ensures that no value is present for PaymentMethodId, not even an explicit nil
### GetPaymentMethodStorageState

`func (o *ListTransactions200ResponseInner) GetPaymentMethodStorageState() string`

GetPaymentMethodStorageState returns the PaymentMethodStorageState field if non-nil, zero value otherwise.

### GetPaymentMethodStorageStateOk

`func (o *ListTransactions200ResponseInner) GetPaymentMethodStorageStateOk() (*string, bool)`

GetPaymentMethodStorageStateOk returns a tuple with the PaymentMethodStorageState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodStorageState

`func (o *ListTransactions200ResponseInner) SetPaymentMethodStorageState(v string)`

SetPaymentMethodStorageState sets PaymentMethodStorageState field to given value.

### HasPaymentMethodStorageState

`func (o *ListTransactions200ResponseInner) HasPaymentMethodStorageState() bool`

HasPaymentMethodStorageState returns a boolean if a field has been set.

### SetPaymentMethodStorageStateNil

`func (o *ListTransactions200ResponseInner) SetPaymentMethodStorageStateNil(b bool)`

 SetPaymentMethodStorageStateNil sets the value for PaymentMethodStorageState to be an explicit nil

### UnsetPaymentMethodStorageState
`func (o *ListTransactions200ResponseInner) UnsetPaymentMethodStorageState()`

UnsetPaymentMethodStorageState ensures that no value is present for PaymentMethodStorageState, not even an explicit nil
### GetPaymentMethodType

`func (o *ListTransactions200ResponseInner) GetPaymentMethodType() string`

GetPaymentMethodType returns the PaymentMethodType field if non-nil, zero value otherwise.

### GetPaymentMethodTypeOk

`func (o *ListTransactions200ResponseInner) GetPaymentMethodTypeOk() (*string, bool)`

GetPaymentMethodTypeOk returns a tuple with the PaymentMethodType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodType

`func (o *ListTransactions200ResponseInner) SetPaymentMethodType(v string)`

SetPaymentMethodType sets PaymentMethodType field to given value.

### HasPaymentMethodType

`func (o *ListTransactions200ResponseInner) HasPaymentMethodType() bool`

HasPaymentMethodType returns a boolean if a field has been set.

### SetPaymentMethodTypeNil

`func (o *ListTransactions200ResponseInner) SetPaymentMethodTypeNil(b bool)`

 SetPaymentMethodTypeNil sets the value for PaymentMethodType to be an explicit nil

### UnsetPaymentMethodType
`func (o *ListTransactions200ResponseInner) UnsetPaymentMethodType()`

UnsetPaymentMethodType ensures that no value is present for PaymentMethodType, not even an explicit nil
### GetPaymentMethodMerchantAccountReferenceId

`func (o *ListTransactions200ResponseInner) GetPaymentMethodMerchantAccountReferenceId() string`

GetPaymentMethodMerchantAccountReferenceId returns the PaymentMethodMerchantAccountReferenceId field if non-nil, zero value otherwise.

### GetPaymentMethodMerchantAccountReferenceIdOk

`func (o *ListTransactions200ResponseInner) GetPaymentMethodMerchantAccountReferenceIdOk() (*string, bool)`

GetPaymentMethodMerchantAccountReferenceIdOk returns a tuple with the PaymentMethodMerchantAccountReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodMerchantAccountReferenceId

`func (o *ListTransactions200ResponseInner) SetPaymentMethodMerchantAccountReferenceId(v string)`

SetPaymentMethodMerchantAccountReferenceId sets PaymentMethodMerchantAccountReferenceId field to given value.

### HasPaymentMethodMerchantAccountReferenceId

`func (o *ListTransactions200ResponseInner) HasPaymentMethodMerchantAccountReferenceId() bool`

HasPaymentMethodMerchantAccountReferenceId returns a boolean if a field has been set.

### SetPaymentMethodMerchantAccountReferenceIdNil

`func (o *ListTransactions200ResponseInner) SetPaymentMethodMerchantAccountReferenceIdNil(b bool)`

 SetPaymentMethodMerchantAccountReferenceIdNil sets the value for PaymentMethodMerchantAccountReferenceId to be an explicit nil

### UnsetPaymentMethodMerchantAccountReferenceId
`func (o *ListTransactions200ResponseInner) UnsetPaymentMethodMerchantAccountReferenceId()`

UnsetPaymentMethodMerchantAccountReferenceId ensures that no value is present for PaymentMethodMerchantAccountReferenceId, not even an explicit nil
### GetVaultToken

`func (o *ListTransactions200ResponseInner) GetVaultToken() string`

GetVaultToken returns the VaultToken field if non-nil, zero value otherwise.

### GetVaultTokenOk

`func (o *ListTransactions200ResponseInner) GetVaultTokenOk() (*string, bool)`

GetVaultTokenOk returns a tuple with the VaultToken field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetVaultToken

`func (o *ListTransactions200ResponseInner) SetVaultToken(v string)`

SetVaultToken sets VaultToken field to given value.

### HasVaultToken

`func (o *ListTransactions200ResponseInner) HasVaultToken() bool`

HasVaultToken returns a boolean if a field has been set.

### SetVaultTokenNil

`func (o *ListTransactions200ResponseInner) SetVaultTokenNil(b bool)`

 SetVaultTokenNil sets the value for VaultToken to be an explicit nil

### UnsetVaultToken
`func (o *ListTransactions200ResponseInner) UnsetVaultToken()`

UnsetVaultToken ensures that no value is present for VaultToken, not even an explicit nil
### GetErrorCode

`func (o *ListTransactions200ResponseInner) GetErrorCode() string`

GetErrorCode returns the ErrorCode field if non-nil, zero value otherwise.

### GetErrorCodeOk

`func (o *ListTransactions200ResponseInner) GetErrorCodeOk() (*string, bool)`

GetErrorCodeOk returns a tuple with the ErrorCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetErrorCode

`func (o *ListTransactions200ResponseInner) SetErrorCode(v string)`

SetErrorCode sets ErrorCode field to given value.

### HasErrorCode

`func (o *ListTransactions200ResponseInner) HasErrorCode() bool`

HasErrorCode returns a boolean if a field has been set.

### SetErrorCodeNil

`func (o *ListTransactions200ResponseInner) SetErrorCodeNil(b bool)`

 SetErrorCodeNil sets the value for ErrorCode to be an explicit nil

### UnsetErrorCode
`func (o *ListTransactions200ResponseInner) UnsetErrorCode()`

UnsetErrorCode ensures that no value is present for ErrorCode, not even an explicit nil
### GetErrorDetail

`func (o *ListTransactions200ResponseInner) GetErrorDetail() string`

GetErrorDetail returns the ErrorDetail field if non-nil, zero value otherwise.

### GetErrorDetailOk

`func (o *ListTransactions200ResponseInner) GetErrorDetailOk() (*string, bool)`

GetErrorDetailOk returns a tuple with the ErrorDetail field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetErrorDetail

`func (o *ListTransactions200ResponseInner) SetErrorDetail(v string)`

SetErrorDetail sets ErrorDetail field to given value.

### HasErrorDetail

`func (o *ListTransactions200ResponseInner) HasErrorDetail() bool`

HasErrorDetail returns a boolean if a field has been set.

### SetErrorDetailNil

`func (o *ListTransactions200ResponseInner) SetErrorDetailNil(b bool)`

 SetErrorDetailNil sets the value for ErrorDetail to be an explicit nil

### UnsetErrorDetail
`func (o *ListTransactions200ResponseInner) UnsetErrorDetail()`

UnsetErrorDetail ensures that no value is present for ErrorDetail, not even an explicit nil
### GetAvsCode

`func (o *ListTransactions200ResponseInner) GetAvsCode() string`

GetAvsCode returns the AvsCode field if non-nil, zero value otherwise.

### GetAvsCodeOk

`func (o *ListTransactions200ResponseInner) GetAvsCodeOk() (*string, bool)`

GetAvsCodeOk returns a tuple with the AvsCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAvsCode

`func (o *ListTransactions200ResponseInner) SetAvsCode(v string)`

SetAvsCode sets AvsCode field to given value.

### HasAvsCode

`func (o *ListTransactions200ResponseInner) HasAvsCode() bool`

HasAvsCode returns a boolean if a field has been set.

### SetAvsCodeNil

`func (o *ListTransactions200ResponseInner) SetAvsCodeNil(b bool)`

 SetAvsCodeNil sets the value for AvsCode to be an explicit nil

### UnsetAvsCode
`func (o *ListTransactions200ResponseInner) UnsetAvsCode()`

UnsetAvsCode ensures that no value is present for AvsCode, not even an explicit nil
### GetGateway

`func (o *ListTransactions200ResponseInner) GetGateway() TransactionGateway`

GetGateway returns the Gateway field if non-nil, zero value otherwise.

### GetGatewayOk

`func (o *ListTransactions200ResponseInner) GetGatewayOk() (*TransactionGateway, bool)`

GetGatewayOk returns a tuple with the Gateway field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGateway

`func (o *ListTransactions200ResponseInner) SetGateway(v TransactionGateway)`

SetGateway sets Gateway field to given value.

### HasGateway

`func (o *ListTransactions200ResponseInner) HasGateway() bool`

HasGateway returns a boolean if a field has been set.

### SetGatewayNil

`func (o *ListTransactions200ResponseInner) SetGatewayNil(b bool)`

 SetGatewayNil sets the value for Gateway to be an explicit nil

### UnsetGateway
`func (o *ListTransactions200ResponseInner) UnsetGateway()`

UnsetGateway ensures that no value is present for Gateway, not even an explicit nil
### GetPaymentMethod

`func (o *ListTransactions200ResponseInner) GetPaymentMethod() PaymentMethodResponse`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *ListTransactions200ResponseInner) GetPaymentMethodOk() (*PaymentMethodResponse, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *ListTransactions200ResponseInner) SetPaymentMethod(v PaymentMethodResponse)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *ListTransactions200ResponseInner) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.

### SetPaymentMethodNil

`func (o *ListTransactions200ResponseInner) SetPaymentMethodNil(b bool)`

 SetPaymentMethodNil sets the value for PaymentMethod to be an explicit nil

### UnsetPaymentMethod
`func (o *ListTransactions200ResponseInner) UnsetPaymentMethod()`

UnsetPaymentMethod ensures that no value is present for PaymentMethod, not even an explicit nil
### GetTransaction

`func (o *ListTransactions200ResponseInner) GetTransaction() TransactionListPaymentMethodItemTransaction`

GetTransaction returns the Transaction field if non-nil, zero value otherwise.

### GetTransactionOk

`func (o *ListTransactions200ResponseInner) GetTransactionOk() (*TransactionListPaymentMethodItemTransaction, bool)`

GetTransactionOk returns a tuple with the Transaction field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransaction

`func (o *ListTransactions200ResponseInner) SetTransaction(v TransactionListPaymentMethodItemTransaction)`

SetTransaction sets Transaction field to given value.



[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


