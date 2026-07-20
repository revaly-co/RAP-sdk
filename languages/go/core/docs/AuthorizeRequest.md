# AuthorizeRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PaymentMethodType** | Pointer to **NullableString** | Type of payment method to use: - **creditCard**: Use raw credit card details. Requires &#x60;paymentMethod.creditCard&#x60;   (&#x60;number&#x60;, &#x60;expiryMonth&#x60;, &#x60;expiryYear&#x60;) and a cardholder name — &#x60;paymentMethod.fullName&#x60;,   or &#x60;paymentMethod.firstName&#x60; together with &#x60;paymentMethod.lastName&#x60;. - **gatewayPaymentMethodId**: Use an existing gateway payment method identifier. Requires   &#x60;paymentMethod.gatewayPaymentMethod.gatewayPaymentMethodId&#x60; and   &#x60;paymentMethod.merchantAccountReferenceId&#x60;. - **vaultToken**: Use a vault-issued token (any provider). Requires   &#x60;paymentMethod.vaultPaymentMethod.vaultToken&#x60; and the request-level &#x60;customerId&#x60; — the   token is scoped to the customer it was minted for and cannot be detokenized without it.   Vault tokens are gateway-agnostic and can be processed on any gateway.  **Omitting this property.** When exactly one of &#x60;paymentMethod.creditCard&#x60;, &#x60;paymentMethod.gatewayPaymentMethod&#x60;, or &#x60;paymentMethod.vaultPaymentMethod&#x60; is supplied, the type is inferred from it. Supplying more than one of those objects without an explicit type is rejected with &#x60;400&#x60;. To bill a stored payment method, omit this property (and the objects above) and send &#x60;paymentMethod.paymentMethodId&#x60;; recommendation flows (&#x60;previousTransaction&#x60; / &#x60;gateway&#x60;) also carry no type.  | [optional] 
**Amount** | **int64** | Authorization amount in smallest currency unit (e.g., cents for USD) | 
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this authorization. The platform accepts up to 100 characters, but downstream gateways may enforce shorter limits on merchant references (limits near 50 characters have been observed); keep ids at or below 48 characters for the broadest gateway compatibility. | 
**GatewayRoutingId** | Pointer to **NullableString** | Gateway-specific token for payment processing | [optional] 
**Currency** | Pointer to **NullableString** | Three-letter ISO currency code | [optional] 
**InitiatedBy** | Pointer to [**NullableInitiatedBy**](InitiatedBy.md) |  | [optional] 
**MitStoredTransactionId** | Pointer to **NullableString** | Merchant-initiated transaction stored credential ID | [optional] 
**StoredCredential** | Pointer to [**StoredCredential**](StoredCredential.md) |  | [optional] 
**PaymentMethod** | Pointer to [**PaymentMethod**](PaymentMethod.md) |  | [optional] 
**OrderId** | Pointer to **NullableString** | Order identifier from the merchant system | [optional] 
**StoreOnSuccess** | Pointer to **NullableBool** | Whether to store the payment method on successful authorization | [optional] 
**BypassPlatform** | Pointer to **bool** | When true, bypass the primary Revaly processor and execute only the fallback flow | [optional] [default to false]
**CustomerIp** | Pointer to **NullableString** | Customer&#39;s IP address | [optional] 
**CustomerId** | Pointer to **NullableString** | Customer identifier | [optional] 
**GatewayFields** | Pointer to **map[string]interface{}** | Additional gateway-specific fields | [optional] 
**RtnData** | Pointer to [**RtnData**](RtnData.md) |  | [optional] 
**Description** | Pointer to **NullableString** | Authorization description | [optional] 
**StatementDescriptor** | Pointer to **NullableString** | Merchant-supplied text intended to appear on the customer&#39;s bank/card statement. Accepted as free text; per-gateway length and character adaptation is applied at submission and never blocks the charge. | [optional] 
**ThreeDS** | Pointer to [**NullableThreeDS**](ThreeDS.md) |  | [optional] 
**PaymentPlanData** | Pointer to [**PaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**Recovery** | Pointer to [**Recovery**](Recovery.md) |  | [optional] 
**PreviousTransaction** | Pointer to [**PreviousTransaction**](PreviousTransaction.md) |  | [optional] 
**Gateway** | Pointer to [**Gateway**](Gateway.md) |  | [optional] 

## Methods

### NewAuthorizeRequest

`func NewAuthorizeRequest(amount int64, merchantTransactionId string, ) *AuthorizeRequest`

NewAuthorizeRequest instantiates a new AuthorizeRequest object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewAuthorizeRequestWithDefaults

`func NewAuthorizeRequestWithDefaults() *AuthorizeRequest`

NewAuthorizeRequestWithDefaults instantiates a new AuthorizeRequest object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetPaymentMethodType

`func (o *AuthorizeRequest) GetPaymentMethodType() string`

GetPaymentMethodType returns the PaymentMethodType field if non-nil, zero value otherwise.

### GetPaymentMethodTypeOk

`func (o *AuthorizeRequest) GetPaymentMethodTypeOk() (*string, bool)`

GetPaymentMethodTypeOk returns a tuple with the PaymentMethodType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodType

`func (o *AuthorizeRequest) SetPaymentMethodType(v string)`

SetPaymentMethodType sets PaymentMethodType field to given value.

### HasPaymentMethodType

`func (o *AuthorizeRequest) HasPaymentMethodType() bool`

HasPaymentMethodType returns a boolean if a field has been set.

### SetPaymentMethodTypeNil

`func (o *AuthorizeRequest) SetPaymentMethodTypeNil(b bool)`

 SetPaymentMethodTypeNil sets the value for PaymentMethodType to be an explicit nil

### UnsetPaymentMethodType
`func (o *AuthorizeRequest) UnsetPaymentMethodType()`

UnsetPaymentMethodType ensures that no value is present for PaymentMethodType, not even an explicit nil
### GetAmount

`func (o *AuthorizeRequest) GetAmount() int64`

GetAmount returns the Amount field if non-nil, zero value otherwise.

### GetAmountOk

`func (o *AuthorizeRequest) GetAmountOk() (*int64, bool)`

GetAmountOk returns a tuple with the Amount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAmount

`func (o *AuthorizeRequest) SetAmount(v int64)`

SetAmount sets Amount field to given value.


### GetMerchantTransactionId

`func (o *AuthorizeRequest) GetMerchantTransactionId() string`

GetMerchantTransactionId returns the MerchantTransactionId field if non-nil, zero value otherwise.

### GetMerchantTransactionIdOk

`func (o *AuthorizeRequest) GetMerchantTransactionIdOk() (*string, bool)`

GetMerchantTransactionIdOk returns a tuple with the MerchantTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTransactionId

`func (o *AuthorizeRequest) SetMerchantTransactionId(v string)`

SetMerchantTransactionId sets MerchantTransactionId field to given value.


### GetGatewayRoutingId

`func (o *AuthorizeRequest) GetGatewayRoutingId() string`

GetGatewayRoutingId returns the GatewayRoutingId field if non-nil, zero value otherwise.

### GetGatewayRoutingIdOk

`func (o *AuthorizeRequest) GetGatewayRoutingIdOk() (*string, bool)`

GetGatewayRoutingIdOk returns a tuple with the GatewayRoutingId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayRoutingId

`func (o *AuthorizeRequest) SetGatewayRoutingId(v string)`

SetGatewayRoutingId sets GatewayRoutingId field to given value.

### HasGatewayRoutingId

`func (o *AuthorizeRequest) HasGatewayRoutingId() bool`

HasGatewayRoutingId returns a boolean if a field has been set.

### SetGatewayRoutingIdNil

`func (o *AuthorizeRequest) SetGatewayRoutingIdNil(b bool)`

 SetGatewayRoutingIdNil sets the value for GatewayRoutingId to be an explicit nil

### UnsetGatewayRoutingId
`func (o *AuthorizeRequest) UnsetGatewayRoutingId()`

UnsetGatewayRoutingId ensures that no value is present for GatewayRoutingId, not even an explicit nil
### GetCurrency

`func (o *AuthorizeRequest) GetCurrency() string`

GetCurrency returns the Currency field if non-nil, zero value otherwise.

### GetCurrencyOk

`func (o *AuthorizeRequest) GetCurrencyOk() (*string, bool)`

GetCurrencyOk returns a tuple with the Currency field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrency

`func (o *AuthorizeRequest) SetCurrency(v string)`

SetCurrency sets Currency field to given value.

### HasCurrency

`func (o *AuthorizeRequest) HasCurrency() bool`

HasCurrency returns a boolean if a field has been set.

### SetCurrencyNil

`func (o *AuthorizeRequest) SetCurrencyNil(b bool)`

 SetCurrencyNil sets the value for Currency to be an explicit nil

### UnsetCurrency
`func (o *AuthorizeRequest) UnsetCurrency()`

UnsetCurrency ensures that no value is present for Currency, not even an explicit nil
### GetInitiatedBy

`func (o *AuthorizeRequest) GetInitiatedBy() InitiatedBy`

GetInitiatedBy returns the InitiatedBy field if non-nil, zero value otherwise.

### GetInitiatedByOk

`func (o *AuthorizeRequest) GetInitiatedByOk() (*InitiatedBy, bool)`

GetInitiatedByOk returns a tuple with the InitiatedBy field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInitiatedBy

`func (o *AuthorizeRequest) SetInitiatedBy(v InitiatedBy)`

SetInitiatedBy sets InitiatedBy field to given value.

### HasInitiatedBy

`func (o *AuthorizeRequest) HasInitiatedBy() bool`

HasInitiatedBy returns a boolean if a field has been set.

### SetInitiatedByNil

`func (o *AuthorizeRequest) SetInitiatedByNil(b bool)`

 SetInitiatedByNil sets the value for InitiatedBy to be an explicit nil

### UnsetInitiatedBy
`func (o *AuthorizeRequest) UnsetInitiatedBy()`

UnsetInitiatedBy ensures that no value is present for InitiatedBy, not even an explicit nil
### GetMitStoredTransactionId

`func (o *AuthorizeRequest) GetMitStoredTransactionId() string`

GetMitStoredTransactionId returns the MitStoredTransactionId field if non-nil, zero value otherwise.

### GetMitStoredTransactionIdOk

`func (o *AuthorizeRequest) GetMitStoredTransactionIdOk() (*string, bool)`

GetMitStoredTransactionIdOk returns a tuple with the MitStoredTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMitStoredTransactionId

`func (o *AuthorizeRequest) SetMitStoredTransactionId(v string)`

SetMitStoredTransactionId sets MitStoredTransactionId field to given value.

### HasMitStoredTransactionId

`func (o *AuthorizeRequest) HasMitStoredTransactionId() bool`

HasMitStoredTransactionId returns a boolean if a field has been set.

### SetMitStoredTransactionIdNil

`func (o *AuthorizeRequest) SetMitStoredTransactionIdNil(b bool)`

 SetMitStoredTransactionIdNil sets the value for MitStoredTransactionId to be an explicit nil

### UnsetMitStoredTransactionId
`func (o *AuthorizeRequest) UnsetMitStoredTransactionId()`

UnsetMitStoredTransactionId ensures that no value is present for MitStoredTransactionId, not even an explicit nil
### GetStoredCredential

`func (o *AuthorizeRequest) GetStoredCredential() StoredCredential`

GetStoredCredential returns the StoredCredential field if non-nil, zero value otherwise.

### GetStoredCredentialOk

`func (o *AuthorizeRequest) GetStoredCredentialOk() (*StoredCredential, bool)`

GetStoredCredentialOk returns a tuple with the StoredCredential field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStoredCredential

`func (o *AuthorizeRequest) SetStoredCredential(v StoredCredential)`

SetStoredCredential sets StoredCredential field to given value.

### HasStoredCredential

`func (o *AuthorizeRequest) HasStoredCredential() bool`

HasStoredCredential returns a boolean if a field has been set.

### GetPaymentMethod

`func (o *AuthorizeRequest) GetPaymentMethod() PaymentMethod`

GetPaymentMethod returns the PaymentMethod field if non-nil, zero value otherwise.

### GetPaymentMethodOk

`func (o *AuthorizeRequest) GetPaymentMethodOk() (*PaymentMethod, bool)`

GetPaymentMethodOk returns a tuple with the PaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethod

`func (o *AuthorizeRequest) SetPaymentMethod(v PaymentMethod)`

SetPaymentMethod sets PaymentMethod field to given value.

### HasPaymentMethod

`func (o *AuthorizeRequest) HasPaymentMethod() bool`

HasPaymentMethod returns a boolean if a field has been set.

### GetOrderId

`func (o *AuthorizeRequest) GetOrderId() string`

GetOrderId returns the OrderId field if non-nil, zero value otherwise.

### GetOrderIdOk

`func (o *AuthorizeRequest) GetOrderIdOk() (*string, bool)`

GetOrderIdOk returns a tuple with the OrderId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderId

`func (o *AuthorizeRequest) SetOrderId(v string)`

SetOrderId sets OrderId field to given value.

### HasOrderId

`func (o *AuthorizeRequest) HasOrderId() bool`

HasOrderId returns a boolean if a field has been set.

### SetOrderIdNil

`func (o *AuthorizeRequest) SetOrderIdNil(b bool)`

 SetOrderIdNil sets the value for OrderId to be an explicit nil

### UnsetOrderId
`func (o *AuthorizeRequest) UnsetOrderId()`

UnsetOrderId ensures that no value is present for OrderId, not even an explicit nil
### GetStoreOnSuccess

`func (o *AuthorizeRequest) GetStoreOnSuccess() bool`

GetStoreOnSuccess returns the StoreOnSuccess field if non-nil, zero value otherwise.

### GetStoreOnSuccessOk

`func (o *AuthorizeRequest) GetStoreOnSuccessOk() (*bool, bool)`

GetStoreOnSuccessOk returns a tuple with the StoreOnSuccess field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStoreOnSuccess

`func (o *AuthorizeRequest) SetStoreOnSuccess(v bool)`

SetStoreOnSuccess sets StoreOnSuccess field to given value.

### HasStoreOnSuccess

`func (o *AuthorizeRequest) HasStoreOnSuccess() bool`

HasStoreOnSuccess returns a boolean if a field has been set.

### SetStoreOnSuccessNil

`func (o *AuthorizeRequest) SetStoreOnSuccessNil(b bool)`

 SetStoreOnSuccessNil sets the value for StoreOnSuccess to be an explicit nil

### UnsetStoreOnSuccess
`func (o *AuthorizeRequest) UnsetStoreOnSuccess()`

UnsetStoreOnSuccess ensures that no value is present for StoreOnSuccess, not even an explicit nil
### GetBypassPlatform

`func (o *AuthorizeRequest) GetBypassPlatform() bool`

GetBypassPlatform returns the BypassPlatform field if non-nil, zero value otherwise.

### GetBypassPlatformOk

`func (o *AuthorizeRequest) GetBypassPlatformOk() (*bool, bool)`

GetBypassPlatformOk returns a tuple with the BypassPlatform field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBypassPlatform

`func (o *AuthorizeRequest) SetBypassPlatform(v bool)`

SetBypassPlatform sets BypassPlatform field to given value.

### HasBypassPlatform

`func (o *AuthorizeRequest) HasBypassPlatform() bool`

HasBypassPlatform returns a boolean if a field has been set.

### GetCustomerIp

`func (o *AuthorizeRequest) GetCustomerIp() string`

GetCustomerIp returns the CustomerIp field if non-nil, zero value otherwise.

### GetCustomerIpOk

`func (o *AuthorizeRequest) GetCustomerIpOk() (*string, bool)`

GetCustomerIpOk returns a tuple with the CustomerIp field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerIp

`func (o *AuthorizeRequest) SetCustomerIp(v string)`

SetCustomerIp sets CustomerIp field to given value.

### HasCustomerIp

`func (o *AuthorizeRequest) HasCustomerIp() bool`

HasCustomerIp returns a boolean if a field has been set.

### SetCustomerIpNil

`func (o *AuthorizeRequest) SetCustomerIpNil(b bool)`

 SetCustomerIpNil sets the value for CustomerIp to be an explicit nil

### UnsetCustomerIp
`func (o *AuthorizeRequest) UnsetCustomerIp()`

UnsetCustomerIp ensures that no value is present for CustomerIp, not even an explicit nil
### GetCustomerId

`func (o *AuthorizeRequest) GetCustomerId() string`

GetCustomerId returns the CustomerId field if non-nil, zero value otherwise.

### GetCustomerIdOk

`func (o *AuthorizeRequest) GetCustomerIdOk() (*string, bool)`

GetCustomerIdOk returns a tuple with the CustomerId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerId

`func (o *AuthorizeRequest) SetCustomerId(v string)`

SetCustomerId sets CustomerId field to given value.

### HasCustomerId

`func (o *AuthorizeRequest) HasCustomerId() bool`

HasCustomerId returns a boolean if a field has been set.

### SetCustomerIdNil

`func (o *AuthorizeRequest) SetCustomerIdNil(b bool)`

 SetCustomerIdNil sets the value for CustomerId to be an explicit nil

### UnsetCustomerId
`func (o *AuthorizeRequest) UnsetCustomerId()`

UnsetCustomerId ensures that no value is present for CustomerId, not even an explicit nil
### GetGatewayFields

`func (o *AuthorizeRequest) GetGatewayFields() map[string]interface{}`

GetGatewayFields returns the GatewayFields field if non-nil, zero value otherwise.

### GetGatewayFieldsOk

`func (o *AuthorizeRequest) GetGatewayFieldsOk() (*map[string]interface{}, bool)`

GetGatewayFieldsOk returns a tuple with the GatewayFields field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayFields

`func (o *AuthorizeRequest) SetGatewayFields(v map[string]interface{})`

SetGatewayFields sets GatewayFields field to given value.

### HasGatewayFields

`func (o *AuthorizeRequest) HasGatewayFields() bool`

HasGatewayFields returns a boolean if a field has been set.

### SetGatewayFieldsNil

`func (o *AuthorizeRequest) SetGatewayFieldsNil(b bool)`

 SetGatewayFieldsNil sets the value for GatewayFields to be an explicit nil

### UnsetGatewayFields
`func (o *AuthorizeRequest) UnsetGatewayFields()`

UnsetGatewayFields ensures that no value is present for GatewayFields, not even an explicit nil
### GetRtnData

`func (o *AuthorizeRequest) GetRtnData() RtnData`

GetRtnData returns the RtnData field if non-nil, zero value otherwise.

### GetRtnDataOk

`func (o *AuthorizeRequest) GetRtnDataOk() (*RtnData, bool)`

GetRtnDataOk returns a tuple with the RtnData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRtnData

`func (o *AuthorizeRequest) SetRtnData(v RtnData)`

SetRtnData sets RtnData field to given value.

### HasRtnData

`func (o *AuthorizeRequest) HasRtnData() bool`

HasRtnData returns a boolean if a field has been set.

### GetDescription

`func (o *AuthorizeRequest) GetDescription() string`

GetDescription returns the Description field if non-nil, zero value otherwise.

### GetDescriptionOk

`func (o *AuthorizeRequest) GetDescriptionOk() (*string, bool)`

GetDescriptionOk returns a tuple with the Description field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDescription

`func (o *AuthorizeRequest) SetDescription(v string)`

SetDescription sets Description field to given value.

### HasDescription

`func (o *AuthorizeRequest) HasDescription() bool`

HasDescription returns a boolean if a field has been set.

### SetDescriptionNil

`func (o *AuthorizeRequest) SetDescriptionNil(b bool)`

 SetDescriptionNil sets the value for Description to be an explicit nil

### UnsetDescription
`func (o *AuthorizeRequest) UnsetDescription()`

UnsetDescription ensures that no value is present for Description, not even an explicit nil
### GetStatementDescriptor

`func (o *AuthorizeRequest) GetStatementDescriptor() string`

GetStatementDescriptor returns the StatementDescriptor field if non-nil, zero value otherwise.

### GetStatementDescriptorOk

`func (o *AuthorizeRequest) GetStatementDescriptorOk() (*string, bool)`

GetStatementDescriptorOk returns a tuple with the StatementDescriptor field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetStatementDescriptor

`func (o *AuthorizeRequest) SetStatementDescriptor(v string)`

SetStatementDescriptor sets StatementDescriptor field to given value.

### HasStatementDescriptor

`func (o *AuthorizeRequest) HasStatementDescriptor() bool`

HasStatementDescriptor returns a boolean if a field has been set.

### SetStatementDescriptorNil

`func (o *AuthorizeRequest) SetStatementDescriptorNil(b bool)`

 SetStatementDescriptorNil sets the value for StatementDescriptor to be an explicit nil

### UnsetStatementDescriptor
`func (o *AuthorizeRequest) UnsetStatementDescriptor()`

UnsetStatementDescriptor ensures that no value is present for StatementDescriptor, not even an explicit nil
### GetThreeDS

`func (o *AuthorizeRequest) GetThreeDS() ThreeDS`

GetThreeDS returns the ThreeDS field if non-nil, zero value otherwise.

### GetThreeDSOk

`func (o *AuthorizeRequest) GetThreeDSOk() (*ThreeDS, bool)`

GetThreeDSOk returns a tuple with the ThreeDS field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetThreeDS

`func (o *AuthorizeRequest) SetThreeDS(v ThreeDS)`

SetThreeDS sets ThreeDS field to given value.

### HasThreeDS

`func (o *AuthorizeRequest) HasThreeDS() bool`

HasThreeDS returns a boolean if a field has been set.

### SetThreeDSNil

`func (o *AuthorizeRequest) SetThreeDSNil(b bool)`

 SetThreeDSNil sets the value for ThreeDS to be an explicit nil

### UnsetThreeDS
`func (o *AuthorizeRequest) UnsetThreeDS()`

UnsetThreeDS ensures that no value is present for ThreeDS, not even an explicit nil
### GetPaymentPlanData

`func (o *AuthorizeRequest) GetPaymentPlanData() PaymentPlanData`

GetPaymentPlanData returns the PaymentPlanData field if non-nil, zero value otherwise.

### GetPaymentPlanDataOk

`func (o *AuthorizeRequest) GetPaymentPlanDataOk() (*PaymentPlanData, bool)`

GetPaymentPlanDataOk returns a tuple with the PaymentPlanData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentPlanData

`func (o *AuthorizeRequest) SetPaymentPlanData(v PaymentPlanData)`

SetPaymentPlanData sets PaymentPlanData field to given value.

### HasPaymentPlanData

`func (o *AuthorizeRequest) HasPaymentPlanData() bool`

HasPaymentPlanData returns a boolean if a field has been set.

### GetRecovery

`func (o *AuthorizeRequest) GetRecovery() Recovery`

GetRecovery returns the Recovery field if non-nil, zero value otherwise.

### GetRecoveryOk

`func (o *AuthorizeRequest) GetRecoveryOk() (*Recovery, bool)`

GetRecoveryOk returns a tuple with the Recovery field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRecovery

`func (o *AuthorizeRequest) SetRecovery(v Recovery)`

SetRecovery sets Recovery field to given value.

### HasRecovery

`func (o *AuthorizeRequest) HasRecovery() bool`

HasRecovery returns a boolean if a field has been set.

### GetPreviousTransaction

`func (o *AuthorizeRequest) GetPreviousTransaction() PreviousTransaction`

GetPreviousTransaction returns the PreviousTransaction field if non-nil, zero value otherwise.

### GetPreviousTransactionOk

`func (o *AuthorizeRequest) GetPreviousTransactionOk() (*PreviousTransaction, bool)`

GetPreviousTransactionOk returns a tuple with the PreviousTransaction field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPreviousTransaction

`func (o *AuthorizeRequest) SetPreviousTransaction(v PreviousTransaction)`

SetPreviousTransaction sets PreviousTransaction field to given value.

### HasPreviousTransaction

`func (o *AuthorizeRequest) HasPreviousTransaction() bool`

HasPreviousTransaction returns a boolean if a field has been set.

### GetGateway

`func (o *AuthorizeRequest) GetGateway() Gateway`

GetGateway returns the Gateway field if non-nil, zero value otherwise.

### GetGatewayOk

`func (o *AuthorizeRequest) GetGatewayOk() (*Gateway, bool)`

GetGatewayOk returns a tuple with the Gateway field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGateway

`func (o *AuthorizeRequest) SetGateway(v Gateway)`

SetGateway sets Gateway field to given value.

### HasGateway

`func (o *AuthorizeRequest) HasGateway() bool`

HasGateway returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


