# PaymentRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PaymentMethodType** | Pointer to **NullableString** | Type of payment method to use: - **creditCard**: Use raw credit card details - **gatewayPaymentMethodId**: Use an existing gateway payment method identifier - **vaultToken**: Use a vault-issued token (any provider). Requires &#x60;paymentMethod.vaultPaymentMethod.vaultToken&#x60; and &#x60;paymentMethod.merchantAccountReferenceId&#x60;.  To bill a stored payment method, omit this property and send &#x60;paymentMethod.paymentMethodId&#x60;.  | [optional] 
**Amount** | **int64** | Payment amount in smallest currency unit (e.g., cents for USD) | 
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this transaction | 
**GatewayRoutingId** | Pointer to **NullableString** | Gateway-specific token for payment processing | [optional] 
**Currency** | Pointer to **NullableString** | Three-letter ISO currency code | [optional] 
**InitiatedBy** | Pointer to [**NullableInitiatedBy**](InitiatedBy.md) |  | [optional] 
**MitStoredTransactionId** | Pointer to **NullableString** | Merchant-initiated transaction stored credential ID | [optional] 
**StoredCredential** | Pointer to [**StoredCredential**](StoredCredential.md) |  | [optional] 
**PaymentMethod** | Pointer to [**PaymentMethod**](PaymentMethod.md) |  | [optional] 
**OrderId** | Pointer to **NullableString** | Order identifier from the merchant system | [optional] 
**StoreOnSuccess** | Pointer to **NullableBool** | Whether to store the payment method on successful transaction | [optional] 
**BypassPlatform** | Pointer to **bool** | When true, bypass the primary Revaly processor and execute only the fallback flow | [optional] [default to false]
**CustomerIp** | Pointer to **NullableString** | Customer&#39;s IP address | [optional] 
**CustomerId** | Pointer to **NullableString** | Customer identifier | [optional] 
**GatewayFields** | Pointer to **map[string]interface{}** | Additional gateway-specific fields | [optional] 
**RtnData** | Pointer to [**RtnData**](RtnData.md) |  | [optional] 
**Description** | Pointer to **NullableString** | Transaction description | [optional] 
**StatementDescriptor** | Pointer to **NullableString** | Merchant-supplied text intended to appear on the customer&#39;s bank/card statement. Accepted as free text; per-gateway length and character adaptation is applied at submission and never blocks the charge. | [optional] 
**ThreeDS** | Pointer to [**NullableThreeDS**](ThreeDS.md) |  | [optional] 
**PaymentPlanData** | Pointer to [**PaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**Recovery** | Pointer to [**Recovery**](Recovery.md) |  | [optional] 
**PreviousTransaction** | Pointer to [**PreviousTransaction**](PreviousTransaction.md) |  | [optional] 
**Gateway** | Pointer to [**Gateway**](Gateway.md) |  | [optional] 

## Methods

### NewPaymentRequest

`func NewPaymentRequest(amount int64, merchantTransactionId string, ) *PaymentRequest`

NewPaymentRequest instantiates a new PaymentRequest object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewPaymentRequestWithDefaults

`func NewPaymentRequestWithDefaults() *PaymentRequest`

NewPaymentRequestWithDefaults instantiates a new PaymentRequest object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetPaymentMethodType

`func (o *PaymentRequest) GetPaymentMethodType() string`

GetPaymentMethodType returns the PaymentMethodType field if non-nil, zero value otherwise.

### GetPaymentMethodTypeOk

`func (o *PaymentRequest) GetPaymentMethodTypeOk() (*string, bool)`

GetPaymentMethodTypeOk returns a tuple with the PaymentMethodType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodType

`func (o *PaymentRequest) SetPaymentMethodType(v string)`

SetPaymentMethodType sets PaymentMethodType field to given value.

### HasPaymentMethodType

`func (o *PaymentRequest) HasPaymentMethodType() bool`

HasPaymentMethodType returns a boolean if a field has been set.

### SetPaymentMethodTypeNil

`func (o *PaymentRequest) SetPaymentMethodTypeNil(b bool)`

 SetPaymentMethodTypeNil sets the value for PaymentMethodType to be an explicit nil

### UnsetPaymentMethodType
`func (o *PaymentRequest) UnsetPaymentMethodType()`

UnsetPaymentMethodType ensures that no value is present for PaymentMethodType, not even an explicit nil
### GetAmount

`func (o *PaymentRequest) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *PaymentRequest) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *PaymentRequest) SetAmount(v int64)`

SetAmount sets Amount field to given value.


### GetMerchantTransactionId

`func (o *PaymentRequest) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *PaymentRequest) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *PaymentRequest) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.


### GetGatewayRoutingId

`func (o *PaymentRequest) GetGatewayRoutingId() string`

GetGatewayRoutingId returns the GatewayRoutingId field if non-nil, zero value otherwise.

### GetGatewayRoutingIdOk

`func (o *PaymentRequest) GetGatewayRoutingIdOk() (*string, bool)`

GetGatewayRoutingIdOk returns a tuple with the GatewayRoutingId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayRoutingId

`func (o *PaymentRequest) SetGatewayRoutingId(v string)`

SetGatewayRoutingId sets GatewayRoutingId field to given value.

### HasGatewayRoutingId

`func (o *PaymentRequest) HasGatewayRoutingId() bool`

HasGatewayRoutingId returns a boolean if a field has been set.

### SetGatewayRoutingIdNil

`func (o *PaymentRequest) SetGatewayRoutingIdNil(b bool)`

 SetGatewayRoutingIdNil sets the value for GatewayRoutingId to be an explicit nil

### UnsetGatewayRoutingId
`func (o *PaymentRequest) UnsetGatewayRoutingId()`

UnsetGatewayRoutingId ensures that no value is present for GatewayRoutingId, not even an explicit nil
### GetCurrency

`func (o *PaymentRequest) GetCurrency() string`

GetCurrency returns the Currency field if non-nil, zero value otherwise.

### GetCurrencyOk

`func (o *PaymentRequest) GetCurrencyOk() (*string, bool)`

GetCurrencyOk returns a tuple with the Currency field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrency

`func (o *PaymentRequest) SetCurrency(v string)`

SetCurrency sets Currency field to given value.

### HasCurrency

`func (o *PaymentRequest) HasCurrency() bool`

HasCurrency returns a boolean if a field has been set.

### SetCurrencyNil

`func (o *PaymentRequest) SetCurrencyNil(b bool)`

 SetCurrencyNil sets the value for Currency to be an explicit nil

### UnsetCurrency
`func (o *PaymentRequest) UnsetCurrency()`

UnsetCurrency ensures that no value is present for Currency, not even an explicit nil
### GetInitiatedBy

`func (o *PaymentRequest) GetInitiatedBy() InitiatedBy`

GetInitiatedBy returns the InitiatedBy field if non-nil, zero value otherwise.

### GetInitiatedByOk

`func (o *PaymentRequest) GetInitiatedByOk() (*InitiatedBy, bool)`

GetInitiatedByOk returns a tuple with the InitiatedBy field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInitiatedBy

`func (o *PaymentRequest) SetInitiatedBy(v InitiatedBy)`

SetInitiatedBy sets InitiatedBy field to given value.

### HasInitiatedBy

`func (o *PaymentRequest) HasInitiatedBy() bool`

HasInitiatedBy returns a boolean if a field has been set.

### SetInitiatedByNil

`func (o *PaymentRequest) SetInitiatedByNil(b bool)`

 SetInitiatedByNil sets the value for InitiatedBy to be an explicit nil

### UnsetInitiatedBy
`func (o *PaymentRequest) UnsetInitiatedBy()`

UnsetInitiatedBy ensures that no value is present for InitiatedBy, not even an explicit nil
### GetMitStoredTransactionId

`func (o *PaymentRequest) GetMitStoredTransactionId() string`

GetMitStoredTransactionId returns the MitStoredTransactionId field if non-nil, zero value otherwise.

### GetMitStoredTransactionIdOk

`func (o *PaymentRequest) GetMitStoredTransactionIdOk() (*string, bool)`

GetMitStoredTransactionIdOk returns a tuple with the MitStoredTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMitStoredTransactionId

`func (o *PaymentRequest) SetMitStoredTransactionId(v string)`

SetMitStoredTransactionId sets MitStoredTransactionId field to given value.

### HasMitStoredTransactionId

`func (o *PaymentRequest) HasMitStoredTransactionId() bool`

HasMitStoredTransactionId returns a boolean if a field has been set.

### SetMitStoredTransactionIdNil

`func (o *PaymentRequest) SetMitStoredTransactionIdNil(b bool)`

 SetMitStoredTransactionIdNil sets the value for MitStoredTransactionId to be an explicit nil

### UnsetMitStoredTransactionId
`func (o *PaymentRequest) UnsetMitStoredTransactionId()`

UnsetMitStoredTransactionId ensures that no value is present for MitStoredTransactionId, not even an explicit nil
### GetStoredCredential

`func (o *PaymentRequest) GetStoredCredential() StoredCredential`

GetStoredCredential returns the StoredCredential field if non-nil, zero value otherwise.

### GetStoredCredentialOk

`func (o *PaymentRequest) GetStoredCredentialOk() (*StoredCredential, bool)`

GetStoredCredentialOk returns a tuple with the StoredCredential field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStoredCredential

`func (o *PaymentRequest) SetStoredCredential(v StoredCredential)`

SetStoredCredential sets StoredCredential field to given value.

### HasStoredCredential

`func (o *PaymentRequest) HasStoredCredential() bool`

HasStoredCredential returns a boolean if a field has been set.

### GetPaymentMethod

`func (o *PaymentRequest) GetPaymentMethod() PaymentMethod`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *PaymentRequest) GetPaymentMethodOk() (*PaymentMethod, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *PaymentRequest) SetPaymentMethod(v PaymentMethod)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *PaymentRequest) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.

### GetOrderId

`func (o *PaymentRequest) GetOrderId() string`

GetOrderId returns the OrderId field if non-nil, zero value otherwise.

### GetOrderIdOk

`func (o *PaymentRequest) GetOrderIdOk() (*string, bool)`

GetOrderIdOk returns a tuple with the OrderId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderId

`func (o *PaymentRequest) SetOrderId(v string)`

SetOrderId sets OrderId field to given value.

### HasOrderId

`func (o *PaymentRequest) HasOrderId() bool`

HasOrderId returns a boolean if a field has been set.

### SetOrderIdNil

`func (o *PaymentRequest) SetOrderIdNil(b bool)`

 SetOrderIdNil sets the value for OrderId to be an explicit nil

### UnsetOrderId
`func (o *PaymentRequest) UnsetOrderId()`

UnsetOrderId ensures that no value is present for OrderId, not even an explicit nil
### GetStoreOnSuccess

`func (o *PaymentRequest) GetStoreOnSuccess() bool`

GetStoreOnSuccess returns the StoreOnSuccess field if non-nil, zero value otherwise.

### GetStoreOnSuccessOk

`func (o *PaymentRequest) GetStoreOnSuccessOk() (*bool, bool)`

GetStoreOnSuccessOk returns a tuple with the StoreOnSuccess field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStoreOnSuccess

`func (o *PaymentRequest) SetStoreOnSuccess(v bool)`

SetStoreOnSuccess sets StoreOnSuccess field to given value.

### HasStoreOnSuccess

`func (o *PaymentRequest) HasStoreOnSuccess() bool`

HasStoreOnSuccess returns a boolean if a field has been set.

### SetStoreOnSuccessNil

`func (o *PaymentRequest) SetStoreOnSuccessNil(b bool)`

 SetStoreOnSuccessNil sets the value for StoreOnSuccess to be an explicit nil

### UnsetStoreOnSuccess
`func (o *PaymentRequest) UnsetStoreOnSuccess()`

UnsetStoreOnSuccess ensures that no value is present for StoreOnSuccess, not even an explicit nil
### GetBypassPlatform

`func (o *PaymentRequest) GetBypassPlatform() bool`

GetBypassPlatform returns the BypassPlatform field if non-nil, zero value otherwise.

### GetBypassPlatformOk

`func (o *PaymentRequest) GetBypassPlatformOk() (*bool, bool)`

GetBypassPlatformOk returns a tuple with the BypassPlatform field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBypassPlatform

`func (o *PaymentRequest) SetBypassPlatform(v bool)`

SetBypassPlatform sets BypassPlatform field to given value.

### HasBypassPlatform

`func (o *PaymentRequest) HasBypassPlatform() bool`

HasBypassPlatform returns a boolean if a field has been set.

### GetCustomerIp

`func (o *PaymentRequest) GetCustomerIp() string`

GetCustomerIp returns the CustomerIp field if non-nil, zero value otherwise.

### GetCustomerIpOk

`func (o *PaymentRequest) GetCustomerIpOk() (*string, bool)`

GetCustomerIpOk returns a tuple with the CustomerIp field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerIp

`func (o *PaymentRequest) SetCustomerIp(v string)`

SetCustomerIp sets CustomerIp field to given value.

### HasCustomerIp

`func (o *PaymentRequest) HasCustomerIp() bool`

HasCustomerIp returns a boolean if a field has been set.

### SetCustomerIpNil

`func (o *PaymentRequest) SetCustomerIpNil(b bool)`

 SetCustomerIpNil sets the value for CustomerIp to be an explicit nil

### UnsetCustomerIp
`func (o *PaymentRequest) UnsetCustomerIp()`

UnsetCustomerIp ensures that no value is present for CustomerIp, not even an explicit nil
### GetCustomerId

`func (o *PaymentRequest) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *PaymentRequest) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *PaymentRequest) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *PaymentRequest) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *PaymentRequest) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *PaymentRequest) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetGatewayFields

`func (o *PaymentRequest) GetGatewayFields() map[string]interface{}`

GetGatewayFields returns the GatewayFields field if non-nil, zero value otherwise.

### GetGatewayFieldsOk

`func (o *PaymentRequest) GetGatewayFieldsOk() (*map[string]interface{}, bool)`

GetGatewayFieldsOk returns a tuple with the GatewayFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayFields

`func (o *PaymentRequest) SetGatewayFields(v map[string]interface{})`

SetGatewayFields sets GatewayFields field to given value.

### HasGatewayFields

`func (o *PaymentRequest) HasGatewayFields() bool`

HasGatewayFields returns a boolean if a field has been set.

### SetGatewayFieldsNil

`func (o *PaymentRequest) SetGatewayFieldsNil(b bool)`

 SetGatewayFieldsNil sets the value for GatewayFields to be an explicit nil

### UnsetGatewayFields
`func (o *PaymentRequest) UnsetGatewayFields()`

UnsetGatewayFields ensures that no value is present for GatewayFields, not even an explicit nil
### GetRtnData

`func (o *PaymentRequest) GetRtnData() RtnData`

GetRtnData returns the RtnData field if non-nil, zero value otherwise.

### GetRtnDataOk

`func (o *PaymentRequest) GetRtnDataOk() (*RtnData, bool)`

GetRtnDataOk returns a tuple with the RtnData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRtnData

`func (o *PaymentRequest) SetRtnData(v RtnData)`

SetRtnData sets RtnData field to given value.

### HasRtnData

`func (o *PaymentRequest) HasRtnData() bool`

HasRtnData returns a boolean if a field has been set.

### GetDescription

`func (o *PaymentRequest) GetDescription() string`

GetDescription returns the Description field if non-nil, zero value otherwise.

### GetDescriptionOk

`func (o *PaymentRequest) GetDescriptionOk() (*string, bool)`

GetDescriptionOk returns a tuple with the Description field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDescription

`func (o *PaymentRequest) SetDescription(v string)`

SetDescription sets Description field to given value.

### HasDescription

`func (o *PaymentRequest) HasDescription() bool`

HasDescription returns a boolean if a field has been set.

### SetDescriptionNil

`func (o *PaymentRequest) SetDescriptionNil(b bool)`

 SetDescriptionNil sets the value for Description to be an explicit nil

### UnsetDescription
`func (o *PaymentRequest) UnsetDescription()`

UnsetDescription ensures that no value is present for Description, not even an explicit nil
### GetStatementDescriptor

`func (o *PaymentRequest) GetStatementDescriptor() string`

GetStatementDescriptor returns the StatementDescriptor field if non-nil, zero value otherwise.

### GetStatementDescriptorOk

`func (o *PaymentRequest) GetStatementDescriptorOk() (*string, bool)`

GetStatementDescriptorOk returns a tuple with the StatementDescriptor field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStatementDescriptor

`func (o *PaymentRequest) SetStatementDescriptor(v string)`

SetStatementDescriptor sets StatementDescriptor field to given value.

### HasStatementDescriptor

`func (o *PaymentRequest) HasStatementDescriptor() bool`

HasStatementDescriptor returns a boolean if a field has been set.

### SetStatementDescriptorNil

`func (o *PaymentRequest) SetStatementDescriptorNil(b bool)`

 SetStatementDescriptorNil sets the value for StatementDescriptor to be an explicit nil

### UnsetStatementDescriptor
`func (o *PaymentRequest) UnsetStatementDescriptor()`

UnsetStatementDescriptor ensures that no value is present for StatementDescriptor, not even an explicit nil
### GetThreeDS

`func (o *PaymentRequest) GetThreeDS() ThreeDS`

GetThreeDS returns the ThreeDS field if non-nil, zero value otherwise.

### GetThreeDSOk

`func (o *PaymentRequest) GetThreeDSOk() (*ThreeDS, bool)`

GetThreeDSOk returns a tuple with the ThreeDS field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetThreeDS

`func (o *PaymentRequest) SetThreeDS(v ThreeDS)`

SetThreeDS sets ThreeDS field to given value.

### HasThreeDS

`func (o *PaymentRequest) HasThreeDS() bool`

HasThreeDS returns a boolean if a field has been set.

### SetThreeDSNil

`func (o *PaymentRequest) SetThreeDSNil(b bool)`

 SetThreeDSNil sets the value for ThreeDS to be an explicit nil

### UnsetThreeDS
`func (o *PaymentRequest) UnsetThreeDS()`

UnsetThreeDS ensures that no value is present for ThreeDS, not even an explicit nil
### GetPaymentPlanData

`func (o *PaymentRequest) GetPaymentPlanData() PaymentPlanData`

GetPaymentPlanData returns the PaymentPlanData field if non-nil, zero value otherwise.

### GetPaymentPlanDataOk

`func (o *PaymentRequest) GetPaymentPlanDataOk() (*PaymentPlanData, bool)`

GetPaymentPlanDataOk returns a tuple with the PaymentPlanData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentPlanData

`func (o *PaymentRequest) SetPaymentPlanData(v PaymentPlanData)`

SetPaymentPlanData sets PaymentPlanData field to given value.

### HasPaymentPlanData

`func (o *PaymentRequest) HasPaymentPlanData() bool`

HasPaymentPlanData returns a boolean if a field has been set.

### GetRecovery

`func (o *PaymentRequest) GetRecovery() Recovery`

GetRecovery returns the Recovery field if non-nil, zero value otherwise.

### GetRecoveryOk

`func (o *PaymentRequest) GetRecoveryOk() (*Recovery, bool)`

GetRecoveryOk returns a tuple with the Recovery field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRecovery

`func (o *PaymentRequest) SetRecovery(v Recovery)`

SetRecovery sets Recovery field to given value.

### HasRecovery

`func (o *PaymentRequest) HasRecovery() bool`

HasRecovery returns a boolean if a field has been set.

### GetPreviousTransaction

`func (o *PaymentRequest) GetPreviousTransaction() PreviousTransaction`

GetPreviousTransaction returns the PreviousTransaction field if non-nil, zero value otherwise.

### GetPreviousTransactionOk

`func (o *PaymentRequest) GetPreviousTransactionOk() (*PreviousTransaction, bool)`

GetPreviousTransactionOk returns a tuple with the PreviousTransaction field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPreviousTransaction

`func (o *PaymentRequest) SetPreviousTransaction(v PreviousTransaction)`

SetPreviousTransaction sets PreviousTransaction field to given value.

### HasPreviousTransaction

`func (o *PaymentRequest) HasPreviousTransaction() bool`

HasPreviousTransaction returns a boolean if a field has been set.

### GetGateway

`func (o *PaymentRequest) GetGateway() Gateway`

GetGateway returns the Gateway field if non-nil, zero value otherwise.

### GetGatewayOk

`func (o *PaymentRequest) GetGatewayOk() (*Gateway, bool)`

GetGatewayOk returns a tuple with the Gateway field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGateway

`func (o *PaymentRequest) SetGateway(v Gateway)`

SetGateway sets Gateway field to given value.

### HasGateway

`func (o *PaymentRequest) HasGateway() bool`

HasGateway returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


