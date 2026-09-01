# TransactionListItem

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | Pointer to **NullableString** | Unique transaction identifier | [optional] 
**TransactionDate** | Pointer to **time.Time** | Date and time when the transaction was processed (ISO 8601) | [optional] 
**TransactionStatus** | Pointer to **int32** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**ResponseCode** | Pointer to **NullableString** | Response code from the processing result | [optional] 
**Message** | Pointer to **NullableString** | Human-readable message about the transaction result | [optional] 
**TransactionType** | Pointer to **NullableString** | Type of transaction performed | [optional] 
**RetryDate** | Pointer to **NullableTime** | Scheduled retry date, if applicable | [optional] 
**Amount** | Pointer to **NullableInt64** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**InitialMerchantTransactionId** | Pointer to **NullableString** | The merchant transaction ID of the initial transaction in the recovery chain | [optional] 
**StorageState** | Pointer to **NullableString** | Payment method storage state at the time of transaction | [optional] 
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
**PaymentMethodStorageState** | Pointer to **NullableString** | Storage state of the payment method | [optional] 
**PaymentMethodType** | Pointer to **NullableString** | Type of payment method used | [optional] 
**PaymentMethodMerchantAccountReferenceId** | Pointer to **NullableString** | Merchant account reference ID associated with the payment method | [optional] 
**VaultToken** | Pointer to **NullableString** | Vault token for the credential this transaction ran against, reported flat on the row alongside the other &#x60;paymentMethod*&#x60; fields. Present only on rows that ran against a vault credential — omitted, not null or empty, on every other row. In practice this means the detailed response type: simplified rows carry no payment-method data to report a token from. | [optional] 
**ErrorCode** | Pointer to **NullableString** | Error code from the gateway response | [optional] 
**ErrorDetail** | Pointer to **NullableString** | Detailed error message from the gateway response | [optional] 
**AvsCode** | Pointer to **NullableString** | Address Verification System result code from the gateway | [optional] 
**Gateway** | Pointer to [**NullableTransactionGateway**](TransactionGateway.md) |  | [optional] 
**PaymentMethod** | Pointer to [**NullablePaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional] 

## Methods

### NewTransactionListItem

`func NewTransactionListItem() *TransactionListItem`

NewTransactionListItem instantiates a new TransactionListItem object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewTransactionListItemWithDefaults

`func NewTransactionListItemWithDefaults() *TransactionListItem`

NewTransactionListItemWithDefaults instantiates a new TransactionListItem object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionId

`func (o *TransactionListItem) GetTransactionId() string`

GetTransactionId returns the TransactionId field if non-nil, zero value otherwise.

### GetTransactionIdOk

`func (o *TransactionListItem) GetTransactionIdOk() (*string, bool)`

GetTransactionIdOk returns a tuple with the TransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionId

`func (o *TransactionListItem) SetTransactionId(v string)`

SetTransactionId sets TransactionId field to given value.

### HasTransactionId

`func (o *TransactionListItem) HasTransactionId() bool`

HasTransactionId returns a boolean if a field has been set.

### SetTransactionIdNil

`func (o *TransactionListItem) SetTransactionIdNil(b bool)`

 SetTransactionIdNil sets the value for TransactionId to be an explicit nil

### UnsetTransactionId
`func (o *TransactionListItem) UnsetTransactionId()`

UnsetTransactionId ensures that no value is present for TransactionId, not even an explicit nil
### GetTransactionDate

`func (o *TransactionListItem) GetTransactionDate() time.Time`

GetTransactionDate returns the TransactionDate field if non-nil, zero value otherwise.

### GetTransactionDateOk

`func (o *TransactionListItem) GetTransactionDateOk() (*time.Time, bool)`

GetTransactionDateOk returns a tuple with the TransactionDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionDate

`func (o *TransactionListItem) SetTransactionDate(v time.Time)`

SetTransactionDate sets TransactionDate field to given value.

### HasTransactionDate

`func (o *TransactionListItem) HasTransactionDate() bool`

HasTransactionDate returns a boolean if a field has been set.

### GetTransactionStatus

`func (o *TransactionListItem) GetTransactionStatus() int32`

GetTransactionStatus returns the TransactionStatus field if non-nil, zero value otherwise.

### GetTransactionStatusOk

`func (o *TransactionListItem) GetTransactionStatusOk() (*int32, bool)`

GetTransactionStatusOk returns a tuple with the TransactionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionStatus

`func (o *TransactionListItem) SetTransactionStatus(v int32)`

SetTransactionStatus sets TransactionStatus field to given value.

### HasTransactionStatus

`func (o *TransactionListItem) HasTransactionStatus() bool`

HasTransactionStatus returns a boolean if a field has been set.

### GetResponseCode

`func (o *TransactionListItem) GetResponseCode() string`

GetResponseCode returns the ResponseCode field if non-nil, zero value otherwise.

### GetResponseCodeOk

`func (o *TransactionListItem) GetResponseCodeOk() (*string, bool)`

GetResponseCodeOk returns a tuple with the ResponseCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetResponseCode

`func (o *TransactionListItem) SetResponseCode(v string)`

SetResponseCode sets ResponseCode field to given value.

### HasResponseCode

`func (o *TransactionListItem) HasResponseCode() bool`

HasResponseCode returns a boolean if a field has been set.

### SetResponseCodeNil

`func (o *TransactionListItem) SetResponseCodeNil(b bool)`

 SetResponseCodeNil sets the value for ResponseCode to be an explicit nil

### UnsetResponseCode
`func (o *TransactionListItem) UnsetResponseCode()`

UnsetResponseCode ensures that no value is present for ResponseCode, not even an explicit nil
### GetMessage

`func (o *TransactionListItem) GetMessage() string`

GetMessage returns the Message field if non-nil, zero value otherwise.

### GetMessageOk

`func (o *TransactionListItem) GetMessageOk() (*string, bool)`

GetMessageOk returns a tuple with the Message field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessage

`func (o *TransactionListItem) SetMessage(v string)`

SetMessage sets Message field to given value.

### HasMessage

`func (o *TransactionListItem) HasMessage() bool`

HasMessage returns a boolean if a field has been set.

### SetMessageNil

`func (o *TransactionListItem) SetMessageNil(b bool)`

 SetMessageNil sets the value for Message to be an explicit nil

### UnsetMessage
`func (o *TransactionListItem) UnsetMessage()`

UnsetMessage ensures that no value is present for Message, not even an explicit nil
### GetTransactionType

`func (o *TransactionListItem) GetTransactionType() string`

GetTransactionType returns the TransactionType field if non-nil, zero value otherwise.

### GetTransactionTypeOk

`func (o *TransactionListItem) GetTransactionTypeOk() (*string, bool)`

GetTransactionTypeOk returns a tuple with the TransactionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionType

`func (o *TransactionListItem) SetTransactionType(v string)`

SetTransactionType sets TransactionType field to given value.

### HasTransactionType

`func (o *TransactionListItem) HasTransactionType() bool`

HasTransactionType returns a boolean if a field has been set.

### SetTransactionTypeNil

`func (o *TransactionListItem) SetTransactionTypeNil(b bool)`

 SetTransactionTypeNil sets the value for TransactionType to be an explicit nil

### UnsetTransactionType
`func (o *TransactionListItem) UnsetTransactionType()`

UnsetTransactionType ensures that no value is present for TransactionType, not even an explicit nil
### GetRetryDate

`func (o *TransactionListItem) GetRetryDate() time.Time`

GetRetryDate returns the RetryDate field if non-nil, zero value otherwise.

### GetRetryDateOk

`func (o *TransactionListItem) GetRetryDateOk() (*time.Time, bool)`

GetRetryDateOk returns a tuple with the RetryDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRetryDate

`func (o *TransactionListItem) SetRetryDate(v time.Time)`

SetRetryDate sets RetryDate field to given value.

### HasRetryDate

`func (o *TransactionListItem) HasRetryDate() bool`

HasRetryDate returns a boolean if a field has been set.

### SetRetryDateNil

`func (o *TransactionListItem) SetRetryDateNil(b bool)`

 SetRetryDateNil sets the value for RetryDate to be an explicit nil

### UnsetRetryDate
`func (o *TransactionListItem) UnsetRetryDate()`

UnsetRetryDate ensures that no value is present for RetryDate, not even an explicit nil
### GetAmount

`func (o *TransactionListItem) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *TransactionListItem) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *TransactionListItem) SetAmount(v int64)`

SetAmount sets Amount field to given value.

### HasAmount

`func (o *TransactionListItem) HasAmount() bool`

HasAmount returns a boolean if a field has been set.

### SetAmountNil

`func (o *TransactionListItem) SetAmountNil(b bool)`

 SetAmountNil sets the value for Amount to be an explicit nil

### UnsetAmount
`func (o *TransactionListItem) UnsetAmount()`

UnsetAmount ensures that no value is present for Amount, not even an explicit nil
### GetInitialMerchantTransactionId

`func (o *TransactionListItem) GetInitialMerchantTransactionId() string`

GetInitialMerchantTransactionId returns the InitialMerchantTransactionId field if non-nil, zero value otherwise.

### GetInitialMerchantTransactionIdOk

`func (o *TransactionListItem) GetInitialMerchantTransactionIdOk() (*string, bool)`

GetInitialMerchantTransactionIdOk returns a tuple with the InitialMerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInitialMerchantTransactionId

`func (o *TransactionListItem) SetInitialMerchantTransactionId(v string)`

SetInitialMerchantTransactionId sets InitialMerchantTransactionId field to given value.

### HasInitialMerchantTransactionId

`func (o *TransactionListItem) HasInitialMerchantTransactionId() bool`

HasInitialMerchantTransactionId returns a boolean if a field has been set.

### SetInitialMerchantTransactionIdNil

`func (o *TransactionListItem) SetInitialMerchantTransactionIdNil(b bool)`

 SetInitialMerchantTransactionIdNil sets the value for InitialMerchantTransactionId to be an explicit nil

### UnsetInitialMerchantTransactionId
`func (o *TransactionListItem) UnsetInitialMerchantTransactionId()`

UnsetInitialMerchantTransactionId ensures that no value is present for InitialMerchantTransactionId, not even an explicit nil
### GetStorageState

`func (o *TransactionListItem) GetStorageState() string`

GetStorageState returns the StorageState field if non-nil, zero value otherwise.

### GetStorageStateOk

`func (o *TransactionListItem) GetStorageStateOk() (*string, bool)`

GetStorageStateOk returns a tuple with the StorageState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStorageState

`func (o *TransactionListItem) SetStorageState(v string)`

SetStorageState sets StorageState field to given value.

### HasStorageState

`func (o *TransactionListItem) HasStorageState() bool`

HasStorageState returns a boolean if a field has been set.

### SetStorageStateNil

`func (o *TransactionListItem) SetStorageStateNil(b bool)`

 SetStorageStateNil sets the value for StorageState to be an explicit nil

### UnsetStorageState
`func (o *TransactionListItem) UnsetStorageState()`

UnsetStorageState ensures that no value is present for StorageState, not even an explicit nil
### GetCompletionStatus

`func (o *TransactionListItem) GetCompletionStatus() string`

GetCompletionStatus returns the CompletionStatus field if non-nil, zero value otherwise.

### GetCompletionStatusOk

`func (o *TransactionListItem) GetCompletionStatusOk() (*string, bool)`

GetCompletionStatusOk returns a tuple with the CompletionStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCompletionStatus

`func (o *TransactionListItem) SetCompletionStatus(v string)`

SetCompletionStatus sets CompletionStatus field to given value.

### HasCompletionStatus

`func (o *TransactionListItem) HasCompletionStatus() bool`

HasCompletionStatus returns a boolean if a field has been set.

### SetCompletionStatusNil

`func (o *TransactionListItem) SetCompletionStatusNil(b bool)`

 SetCompletionStatusNil sets the value for CompletionStatus to be an explicit nil

### UnsetCompletionStatus
`func (o *TransactionListItem) UnsetCompletionStatus()`

UnsetCompletionStatus ensures that no value is present for CompletionStatus, not even an explicit nil
### GetGatewaySpecificResponseFields

`func (o *TransactionListItem) GetGatewaySpecificResponseFields() map[string]interface{}`

GetGatewaySpecificResponseFields returns the GatewaySpecificResponseFields field if non-nil, zero value otherwise.

### GetGatewaySpecificResponseFieldsOk

`func (o *TransactionListItem) GetGatewaySpecificResponseFieldsOk() (*map[string]interface{}, bool)`

GetGatewaySpecificResponseFieldsOk returns a tuple with the GatewaySpecificResponseFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewaySpecificResponseFields

`func (o *TransactionListItem) SetGatewaySpecificResponseFields(v map[string]interface{})`

SetGatewaySpecificResponseFields sets GatewaySpecificResponseFields field to given value.

### HasGatewaySpecificResponseFields

`func (o *TransactionListItem) HasGatewaySpecificResponseFields() bool`

HasGatewaySpecificResponseFields returns a boolean if a field has been set.

### SetGatewaySpecificResponseFieldsNil

`func (o *TransactionListItem) SetGatewaySpecificResponseFieldsNil(b bool)`

 SetGatewaySpecificResponseFieldsNil sets the value for GatewaySpecificResponseFields to be an explicit nil

### UnsetGatewaySpecificResponseFields
`func (o *TransactionListItem) UnsetGatewaySpecificResponseFields()`

UnsetGatewaySpecificResponseFields ensures that no value is present for GatewaySpecificResponseFields, not even an explicit nil
### GetGatewaySpecificFields

`func (o *TransactionListItem) GetGatewaySpecificFields() map[string]interface{}`

GetGatewaySpecificFields returns the GatewaySpecificFields field if non-nil, zero value otherwise.

### GetGatewaySpecificFieldsOk

`func (o *TransactionListItem) GetGatewaySpecificFieldsOk() (*map[string]interface{}, bool)`

GetGatewaySpecificFieldsOk returns a tuple with the GatewaySpecificFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewaySpecificFields

`func (o *TransactionListItem) SetGatewaySpecificFields(v map[string]interface{})`

SetGatewaySpecificFields sets GatewaySpecificFields field to given value.

### HasGatewaySpecificFields

`func (o *TransactionListItem) HasGatewaySpecificFields() bool`

HasGatewaySpecificFields returns a boolean if a field has been set.

### SetGatewaySpecificFieldsNil

`func (o *TransactionListItem) SetGatewaySpecificFieldsNil(b bool)`

 SetGatewaySpecificFieldsNil sets the value for GatewaySpecificFields to be an explicit nil

### UnsetGatewaySpecificFields
`func (o *TransactionListItem) UnsetGatewaySpecificFields()`

UnsetGatewaySpecificFields ensures that no value is present for GatewaySpecificFields, not even an explicit nil
### GetAcquirerAuthCode

`func (o *TransactionListItem) GetAcquirerAuthCode() string`

GetAcquirerAuthCode returns the AcquirerAuthCode field if non-nil, zero value otherwise.

### GetAcquirerAuthCodeOk

`func (o *TransactionListItem) GetAcquirerAuthCodeOk() (*string, bool)`

GetAcquirerAuthCodeOk returns a tuple with the AcquirerAuthCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcquirerAuthCode

`func (o *TransactionListItem) SetAcquirerAuthCode(v string)`

SetAcquirerAuthCode sets AcquirerAuthCode field to given value.

### HasAcquirerAuthCode

`func (o *TransactionListItem) HasAcquirerAuthCode() bool`

HasAcquirerAuthCode returns a boolean if a field has been set.

### SetAcquirerAuthCodeNil

`func (o *TransactionListItem) SetAcquirerAuthCodeNil(b bool)`

 SetAcquirerAuthCodeNil sets the value for AcquirerAuthCode to be an explicit nil

### UnsetAcquirerAuthCode
`func (o *TransactionListItem) UnsetAcquirerAuthCode()`

UnsetAcquirerAuthCode ensures that no value is present for AcquirerAuthCode, not even an explicit nil
### GetGatewayTransactionId

`func (o *TransactionListItem) GetGatewayTransactionId() string`

GetGatewayTransactionId returns the GatewayTransactionId field if non-nil, zero value otherwise.

### GetGatewayTransactionIdOk

`func (o *TransactionListItem) GetGatewayTransactionIdOk() (*string, bool)`

GetGatewayTransactionIdOk returns a tuple with the GatewayTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayTransactionId

`func (o *TransactionListItem) SetGatewayTransactionId(v string)`

SetGatewayTransactionId sets GatewayTransactionId field to given value.

### HasGatewayTransactionId

`func (o *TransactionListItem) HasGatewayTransactionId() bool`

HasGatewayTransactionId returns a boolean if a field has been set.

### SetGatewayTransactionIdNil

`func (o *TransactionListItem) SetGatewayTransactionIdNil(b bool)`

 SetGatewayTransactionIdNil sets the value for GatewayTransactionId to be an explicit nil

### UnsetGatewayTransactionId
`func (o *TransactionListItem) UnsetGatewayTransactionId()`

UnsetGatewayTransactionId ensures that no value is present for GatewayTransactionId, not even an explicit nil
### GetGatewayPaymentMethodId

`func (o *TransactionListItem) GetGatewayPaymentMethodId() string`

GetGatewayPaymentMethodId returns the GatewayPaymentMethodId field if non-nil, zero value otherwise.

### GetGatewayPaymentMethodIdOk

`func (o *TransactionListItem) GetGatewayPaymentMethodIdOk() (*string, bool)`

GetGatewayPaymentMethodIdOk returns a tuple with the GatewayPaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayPaymentMethodId

`func (o *TransactionListItem) SetGatewayPaymentMethodId(v string)`

SetGatewayPaymentMethodId sets GatewayPaymentMethodId field to given value.

### HasGatewayPaymentMethodId

`func (o *TransactionListItem) HasGatewayPaymentMethodId() bool`

HasGatewayPaymentMethodId returns a boolean if a field has been set.

### SetGatewayPaymentMethodIdNil

`func (o *TransactionListItem) SetGatewayPaymentMethodIdNil(b bool)`

 SetGatewayPaymentMethodIdNil sets the value for GatewayPaymentMethodId to be an explicit nil

### UnsetGatewayPaymentMethodId
`func (o *TransactionListItem) UnsetGatewayPaymentMethodId()`

UnsetGatewayPaymentMethodId ensures that no value is present for GatewayPaymentMethodId, not even an explicit nil
### GetEngagedRecoveryState

`func (o *TransactionListItem) GetEngagedRecoveryState() int32`

GetEngagedRecoveryState returns the EngagedRecoveryState field if non-nil, zero value otherwise.

### GetEngagedRecoveryStateOk

`func (o *TransactionListItem) GetEngagedRecoveryStateOk() (*int32, bool)`

GetEngagedRecoveryStateOk returns a tuple with the EngagedRecoveryState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEngagedRecoveryState

`func (o *TransactionListItem) SetEngagedRecoveryState(v int32)`

SetEngagedRecoveryState sets EngagedRecoveryState field to given value.

### HasEngagedRecoveryState

`func (o *TransactionListItem) HasEngagedRecoveryState() bool`

HasEngagedRecoveryState returns a boolean if a field has been set.

### SetEngagedRecoveryStateNil

`func (o *TransactionListItem) SetEngagedRecoveryStateNil(b bool)`

 SetEngagedRecoveryStateNil sets the value for EngagedRecoveryState to be an explicit nil

### UnsetEngagedRecoveryState
`func (o *TransactionListItem) UnsetEngagedRecoveryState()`

UnsetEngagedRecoveryState ensures that no value is present for EngagedRecoveryState, not even an explicit nil
### GetCurrencyCode

`func (o *TransactionListItem) GetCurrencyCode() string`

GetCurrencyCode returns the CurrencyCode field if non-nil, zero value otherwise.

### GetCurrencyCodeOk

`func (o *TransactionListItem) GetCurrencyCodeOk() (*string, bool)`

GetCurrencyCodeOk returns a tuple with the CurrencyCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrencyCode

`func (o *TransactionListItem) SetCurrencyCode(v string)`

SetCurrencyCode sets CurrencyCode field to given value.

### HasCurrencyCode

`func (o *TransactionListItem) HasCurrencyCode() bool`

HasCurrencyCode returns a boolean if a field has been set.

### SetCurrencyCodeNil

`func (o *TransactionListItem) SetCurrencyCodeNil(b bool)`

 SetCurrencyCodeNil sets the value for CurrencyCode to be an explicit nil

### UnsetCurrencyCode
`func (o *TransactionListItem) UnsetCurrencyCode()`

UnsetCurrencyCode ensures that no value is present for CurrencyCode, not even an explicit nil
### GetMerchantTransactionId

`func (o *TransactionListItem) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *TransactionListItem) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *TransactionListItem) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.

### HasMerchantTransactionId

`func (o *TransactionListItem) HasMerchantTransactionId() bool`

HasMerchantTransactionId returns a boolean if a field has been set.

### SetMerchantTransactionIdNil

`func (o *TransactionListItem) SetMerchantTransactionIdNil(b bool)`

 SetMerchantTransactionIdNil sets the value for MerchantTransactionId to be an explicit nil

### UnsetMerchantTransactionId
`func (o *TransactionListItem) UnsetMerchantTransactionId()`

UnsetMerchantTransactionId ensures that no value is present for MerchantTransactionId, not even an explicit nil
### GetMerchantAccountReferenceId

`func (o *TransactionListItem) GetMerchantAccountReferenceId() string`

GetMerchantAccountReferenceId returns the MerchantAccountReferenceId field if non-nil, zero value otherwise.

### GetMerchantAccountReferenceIdOk

`func (o *TransactionListItem) GetMerchantAccountReferenceIdOk() (*string, bool)`

GetMerchantAccountReferenceIdOk returns a tuple with the MerchantAccountReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantAccountReferenceId

`func (o *TransactionListItem) SetMerchantAccountReferenceId(v string)`

SetMerchantAccountReferenceId sets MerchantAccountReferenceId field to given value.

### HasMerchantAccountReferenceId

`func (o *TransactionListItem) HasMerchantAccountReferenceId() bool`

HasMerchantAccountReferenceId returns a boolean if a field has been set.

### SetMerchantAccountReferenceIdNil

`func (o *TransactionListItem) SetMerchantAccountReferenceIdNil(b bool)`

 SetMerchantAccountReferenceIdNil sets the value for MerchantAccountReferenceId to be an explicit nil

### UnsetMerchantAccountReferenceId
`func (o *TransactionListItem) UnsetMerchantAccountReferenceId()`

UnsetMerchantAccountReferenceId ensures that no value is present for MerchantAccountReferenceId, not even an explicit nil
### GetCustomerId

`func (o *TransactionListItem) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *TransactionListItem) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *TransactionListItem) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *TransactionListItem) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *TransactionListItem) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *TransactionListItem) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetOrderId

`func (o *TransactionListItem) GetOrderId() string`

GetOrderId returns the OrderId field if non-nil, zero value otherwise.

### GetOrderIdOk

`func (o *TransactionListItem) GetOrderIdOk() (*string, bool)`

GetOrderIdOk returns a tuple with the OrderId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderId

`func (o *TransactionListItem) SetOrderId(v string)`

SetOrderId sets OrderId field to given value.

### HasOrderId

`func (o *TransactionListItem) HasOrderId() bool`

HasOrderId returns a boolean if a field has been set.

### SetOrderIdNil

`func (o *TransactionListItem) SetOrderIdNil(b bool)`

 SetOrderIdNil sets the value for OrderId to be an explicit nil

### UnsetOrderId
`func (o *TransactionListItem) UnsetOrderId()`

UnsetOrderId ensures that no value is present for OrderId, not even an explicit nil
### GetStatementDescriptor

`func (o *TransactionListItem) GetStatementDescriptor() string`

GetStatementDescriptor returns the StatementDescriptor field if non-nil, zero value otherwise.

### GetStatementDescriptorOk

`func (o *TransactionListItem) GetStatementDescriptorOk() (*string, bool)`

GetStatementDescriptorOk returns a tuple with the StatementDescriptor field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStatementDescriptor

`func (o *TransactionListItem) SetStatementDescriptor(v string)`

SetStatementDescriptor sets StatementDescriptor field to given value.

### HasStatementDescriptor

`func (o *TransactionListItem) HasStatementDescriptor() bool`

HasStatementDescriptor returns a boolean if a field has been set.

### SetStatementDescriptorNil

`func (o *TransactionListItem) SetStatementDescriptorNil(b bool)`

 SetStatementDescriptorNil sets the value for StatementDescriptor to be an explicit nil

### UnsetStatementDescriptor
`func (o *TransactionListItem) UnsetStatementDescriptor()`

UnsetStatementDescriptor ensures that no value is present for StatementDescriptor, not even an explicit nil
### GetPaymentMethodId

`func (o *TransactionListItem) GetPaymentMethodId() string`

GetPaymentMethodId returns the PaymentMethodId field if non-nil, zero value otherwise.

### GetPaymentMethodIdOk

`func (o *TransactionListItem) GetPaymentMethodIdOk() (*string, bool)`

GetPaymentMethodIdOk returns a tuple with the PaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodId

`func (o *TransactionListItem) SetPaymentMethodId(v string)`

SetPaymentMethodId sets PaymentMethodId field to given value.

### HasPaymentMethodId

`func (o *TransactionListItem) HasPaymentMethodId() bool`

HasPaymentMethodId returns a boolean if a field has been set.

### SetPaymentMethodIdNil

`func (o *TransactionListItem) SetPaymentMethodIdNil(b bool)`

 SetPaymentMethodIdNil sets the value for PaymentMethodId to be an explicit nil

### UnsetPaymentMethodId
`func (o *TransactionListItem) UnsetPaymentMethodId()`

UnsetPaymentMethodId ensures that no value is present for PaymentMethodId, not even an explicit nil
### GetPaymentMethodStorageState

`func (o *TransactionListItem) GetPaymentMethodStorageState() string`

GetPaymentMethodStorageState returns the PaymentMethodStorageState field if non-nil, zero value otherwise.

### GetPaymentMethodStorageStateOk

`func (o *TransactionListItem) GetPaymentMethodStorageStateOk() (*string, bool)`

GetPaymentMethodStorageStateOk returns a tuple with the PaymentMethodStorageState field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodStorageState

`func (o *TransactionListItem) SetPaymentMethodStorageState(v string)`

SetPaymentMethodStorageState sets PaymentMethodStorageState field to given value.

### HasPaymentMethodStorageState

`func (o *TransactionListItem) HasPaymentMethodStorageState() bool`

HasPaymentMethodStorageState returns a boolean if a field has been set.

### SetPaymentMethodStorageStateNil

`func (o *TransactionListItem) SetPaymentMethodStorageStateNil(b bool)`

 SetPaymentMethodStorageStateNil sets the value for PaymentMethodStorageState to be an explicit nil

### UnsetPaymentMethodStorageState
`func (o *TransactionListItem) UnsetPaymentMethodStorageState()`

UnsetPaymentMethodStorageState ensures that no value is present for PaymentMethodStorageState, not even an explicit nil
### GetPaymentMethodType

`func (o *TransactionListItem) GetPaymentMethodType() string`

GetPaymentMethodType returns the PaymentMethodType field if non-nil, zero value otherwise.

### GetPaymentMethodTypeOk

`func (o *TransactionListItem) GetPaymentMethodTypeOk() (*string, bool)`

GetPaymentMethodTypeOk returns a tuple with the PaymentMethodType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodType

`func (o *TransactionListItem) SetPaymentMethodType(v string)`

SetPaymentMethodType sets PaymentMethodType field to given value.

### HasPaymentMethodType

`func (o *TransactionListItem) HasPaymentMethodType() bool`

HasPaymentMethodType returns a boolean if a field has been set.

### SetPaymentMethodTypeNil

`func (o *TransactionListItem) SetPaymentMethodTypeNil(b bool)`

 SetPaymentMethodTypeNil sets the value for PaymentMethodType to be an explicit nil

### UnsetPaymentMethodType
`func (o *TransactionListItem) UnsetPaymentMethodType()`

UnsetPaymentMethodType ensures that no value is present for PaymentMethodType, not even an explicit nil
### GetPaymentMethodMerchantAccountReferenceId

`func (o *TransactionListItem) GetPaymentMethodMerchantAccountReferenceId() string`

GetPaymentMethodMerchantAccountReferenceId returns the PaymentMethodMerchantAccountReferenceId field if non-nil, zero value otherwise.

### GetPaymentMethodMerchantAccountReferenceIdOk

`func (o *TransactionListItem) GetPaymentMethodMerchantAccountReferenceIdOk() (*string, bool)`

GetPaymentMethodMerchantAccountReferenceIdOk returns a tuple with the PaymentMethodMerchantAccountReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodMerchantAccountReferenceId

`func (o *TransactionListItem) SetPaymentMethodMerchantAccountReferenceId(v string)`

SetPaymentMethodMerchantAccountReferenceId sets PaymentMethodMerchantAccountReferenceId field to given value.

### HasPaymentMethodMerchantAccountReferenceId

`func (o *TransactionListItem) HasPaymentMethodMerchantAccountReferenceId() bool`

HasPaymentMethodMerchantAccountReferenceId returns a boolean if a field has been set.

### SetPaymentMethodMerchantAccountReferenceIdNil

`func (o *TransactionListItem) SetPaymentMethodMerchantAccountReferenceIdNil(b bool)`

 SetPaymentMethodMerchantAccountReferenceIdNil sets the value for PaymentMethodMerchantAccountReferenceId to be an explicit nil

### UnsetPaymentMethodMerchantAccountReferenceId
`func (o *TransactionListItem) UnsetPaymentMethodMerchantAccountReferenceId()`

UnsetPaymentMethodMerchantAccountReferenceId ensures that no value is present for PaymentMethodMerchantAccountReferenceId, not even an explicit nil
### GetVaultToken

`func (o *TransactionListItem) GetVaultToken() string`

GetVaultToken returns the VaultToken field if non-nil, zero value otherwise.

### GetVaultTokenOk

`func (o *TransactionListItem) GetVaultTokenOk() (*string, bool)`

GetVaultTokenOk returns a tuple with the VaultToken field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetVaultToken

`func (o *TransactionListItem) SetVaultToken(v string)`

SetVaultToken sets VaultToken field to given value.

### HasVaultToken

`func (o *TransactionListItem) HasVaultToken() bool`

HasVaultToken returns a boolean if a field has been set.

### SetVaultTokenNil

`func (o *TransactionListItem) SetVaultTokenNil(b bool)`

 SetVaultTokenNil sets the value for VaultToken to be an explicit nil

### UnsetVaultToken
`func (o *TransactionListItem) UnsetVaultToken()`

UnsetVaultToken ensures that no value is present for VaultToken, not even an explicit nil
### GetErrorCode

`func (o *TransactionListItem) GetErrorCode() string`

GetErrorCode returns the ErrorCode field if non-nil, zero value otherwise.

### GetErrorCodeOk

`func (o *TransactionListItem) GetErrorCodeOk() (*string, bool)`

GetErrorCodeOk returns a tuple with the ErrorCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetErrorCode

`func (o *TransactionListItem) SetErrorCode(v string)`

SetErrorCode sets ErrorCode field to given value.

### HasErrorCode

`func (o *TransactionListItem) HasErrorCode() bool`

HasErrorCode returns a boolean if a field has been set.

### SetErrorCodeNil

`func (o *TransactionListItem) SetErrorCodeNil(b bool)`

 SetErrorCodeNil sets the value for ErrorCode to be an explicit nil

### UnsetErrorCode
`func (o *TransactionListItem) UnsetErrorCode()`

UnsetErrorCode ensures that no value is present for ErrorCode, not even an explicit nil
### GetErrorDetail

`func (o *TransactionListItem) GetErrorDetail() string`

GetErrorDetail returns the ErrorDetail field if non-nil, zero value otherwise.

### GetErrorDetailOk

`func (o *TransactionListItem) GetErrorDetailOk() (*string, bool)`

GetErrorDetailOk returns a tuple with the ErrorDetail field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetErrorDetail

`func (o *TransactionListItem) SetErrorDetail(v string)`

SetErrorDetail sets ErrorDetail field to given value.

### HasErrorDetail

`func (o *TransactionListItem) HasErrorDetail() bool`

HasErrorDetail returns a boolean if a field has been set.

### SetErrorDetailNil

`func (o *TransactionListItem) SetErrorDetailNil(b bool)`

 SetErrorDetailNil sets the value for ErrorDetail to be an explicit nil

### UnsetErrorDetail
`func (o *TransactionListItem) UnsetErrorDetail()`

UnsetErrorDetail ensures that no value is present for ErrorDetail, not even an explicit nil
### GetAvsCode

`func (o *TransactionListItem) GetAvsCode() string`

GetAvsCode returns the AvsCode field if non-nil, zero value otherwise.

### GetAvsCodeOk

`func (o *TransactionListItem) GetAvsCodeOk() (*string, bool)`

GetAvsCodeOk returns a tuple with the AvsCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAvsCode

`func (o *TransactionListItem) SetAvsCode(v string)`

SetAvsCode sets AvsCode field to given value.

### HasAvsCode

`func (o *TransactionListItem) HasAvsCode() bool`

HasAvsCode returns a boolean if a field has been set.

### SetAvsCodeNil

`func (o *TransactionListItem) SetAvsCodeNil(b bool)`

 SetAvsCodeNil sets the value for AvsCode to be an explicit nil

### UnsetAvsCode
`func (o *TransactionListItem) UnsetAvsCode()`

UnsetAvsCode ensures that no value is present for AvsCode, not even an explicit nil
### GetGateway

`func (o *TransactionListItem) GetGateway() TransactionGateway`

GetGateway returns the Gateway field if non-nil, zero value otherwise.

### GetGatewayOk

`func (o *TransactionListItem) GetGatewayOk() (*TransactionGateway, bool)`

GetGatewayOk returns a tuple with the Gateway field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGateway

`func (o *TransactionListItem) SetGateway(v TransactionGateway)`

SetGateway sets Gateway field to given value.

### HasGateway

`func (o *TransactionListItem) HasGateway() bool`

HasGateway returns a boolean if a field has been set.

### SetGatewayNil

`func (o *TransactionListItem) SetGatewayNil(b bool)`

 SetGatewayNil sets the value for Gateway to be an explicit nil

### UnsetGateway
`func (o *TransactionListItem) UnsetGateway()`

UnsetGateway ensures that no value is present for Gateway, not even an explicit nil
### GetPaymentMethod

`func (o *TransactionListItem) GetPaymentMethod() PaymentMethodResponse`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *TransactionListItem) GetPaymentMethodOk() (*PaymentMethodResponse, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *TransactionListItem) SetPaymentMethod(v PaymentMethodResponse)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *TransactionListItem) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.

### SetPaymentMethodNil

`func (o *TransactionListItem) SetPaymentMethodNil(b bool)`

 SetPaymentMethodNil sets the value for PaymentMethod to be an explicit nil

### UnsetPaymentMethod
`func (o *TransactionListItem) UnsetPaymentMethod()`

UnsetPaymentMethod ensures that no value is present for PaymentMethod, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


