# PaymentMethod

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**FirstName** | Pointer to **NullableString** | Customer&#39;s first name | [optional] 
**LastName** | Pointer to **NullableString** | Customer&#39;s last name | [optional] 
**FullName** | Pointer to **NullableString** | Customer&#39;s full name | [optional] 
**Email** | Pointer to **NullableString** | Customer&#39;s email address | [optional] 
**MerchantAccountReferenceId** | Pointer to **NullableString** | Merchant account identifier at the gateway | [optional] 
**PaymentMethodId** | Pointer to **NullableString** | Existing payment method identifier (for updates) | [optional] 
**IssuerIdentificationNumber** | Pointer to **NullableString** | Bank Identification Number (BIN). Must contain exactly 6 or 8 digits. | [optional] 
**BillingAddress** | Pointer to [**Address**](Address.md) |  | [optional] 
**ShippingAddress** | Pointer to [**Address**](Address.md) |  | [optional] 
**CreditCard** | Pointer to [**CreditCard**](CreditCard.md) |  | [optional] 
**GatewayPaymentMethod** | Pointer to [**GatewayPaymentMethod**](GatewayPaymentMethod.md) |  | [optional] 
**VaultPaymentMethod** | Pointer to [**VaultPaymentMethod**](VaultPaymentMethod.md) |  | [optional] 

## Methods

### NewPaymentMethod

`func NewPaymentMethod() *PaymentMethod`

NewPaymentMethod instantiates a new PaymentMethod object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewPaymentMethodWithDefaults

`func NewPaymentMethodWithDefaults() *PaymentMethod`

NewPaymentMethodWithDefaults instantiates a new PaymentMethod object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetFirstName

`func (o *PaymentMethod) GetFirstName() string`

GetFirstName returns the FirstName field if non-nil, zero value otherwise.

### GetFirstNameOk

`func (o *PaymentMethod) GetFirstNameOk() (*string, bool)`

GetFirstNameOk returns a tuple with the FirstName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFirstName

`func (o *PaymentMethod) SetFirstName(v string)`

SetFirstName sets FirstName field to given value.

### HasFirstName

`func (o *PaymentMethod) HasFirstName() bool`

HasFirstName returns a boolean if a field has been set.

### SetFirstNameNil

`func (o *PaymentMethod) SetFirstNameNil(b bool)`

 SetFirstNameNil sets the value for FirstName to be an explicit nil

### UnsetFirstName
`func (o *PaymentMethod) UnsetFirstName()`

UnsetFirstName ensures that no value is present for FirstName, not even an explicit nil
### GetLastName

`func (o *PaymentMethod) GetLastName() string`

GetLastName returns the LastName field if non-nil, zero value otherwise.

### GetLastNameOk

`func (o *PaymentMethod) GetLastNameOk() (*string, bool)`

GetLastNameOk returns a tuple with the LastName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetLastName

`func (o *PaymentMethod) SetLastName(v string)`

SetLastName sets LastName field to given value.

### HasLastName

`func (o *PaymentMethod) HasLastName() bool`

HasLastName returns a boolean if a field has been set.

### SetLastNameNil

`func (o *PaymentMethod) SetLastNameNil(b bool)`

 SetLastNameNil sets the value for LastName to be an explicit nil

### UnsetLastName
`func (o *PaymentMethod) UnsetLastName()`

UnsetLastName ensures that no value is present for LastName, not even an explicit nil
### GetFullName

`func (o *PaymentMethod) GetFullName() string`

GetFullName returns the FullName field if non-nil, zero value otherwise.

### GetFullNameOk

`func (o *PaymentMethod) GetFullNameOk() (*string, bool)`

GetFullNameOk returns a tuple with the FullName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFullName

`func (o *PaymentMethod) SetFullName(v string)`

SetFullName sets FullName field to given value.

### HasFullName

`func (o *PaymentMethod) HasFullName() bool`

HasFullName returns a boolean if a field has been set.

### SetFullNameNil

`func (o *PaymentMethod) SetFullNameNil(b bool)`

 SetFullNameNil sets the value for FullName to be an explicit nil

### UnsetFullName
`func (o *PaymentMethod) UnsetFullName()`

UnsetFullName ensures that no value is present for FullName, not even an explicit nil
### GetEmail

`func (o *PaymentMethod) GetEmail() string`

GetEmail returns the Email field if non-nil, zero value otherwise.

### GetEmailOk

`func (o *PaymentMethod) GetEmailOk() (*string, bool)`

GetEmailOk returns a tuple with the Email field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEmail

`func (o *PaymentMethod) SetEmail(v string)`

SetEmail sets Email field to given value.

### HasEmail

`func (o *PaymentMethod) HasEmail() bool`

HasEmail returns a boolean if a field has been set.

### SetEmailNil

`func (o *PaymentMethod) SetEmailNil(b bool)`

 SetEmailNil sets the value for Email to be an explicit nil

### UnsetEmail
`func (o *PaymentMethod) UnsetEmail()`

UnsetEmail ensures that no value is present for Email, not even an explicit nil
### GetMerchantAccountReferenceId

`func (o *PaymentMethod) GetMerchantAccountReferenceId() string`

GetMerchantAccountReferenceId returns the MerchantAccountReferenceId field if non-nil, zero value otherwise.

### GetMerchantAccountReferenceIdOk

`func (o *PaymentMethod) GetMerchantAccountReferenceIdOk() (*string, bool)`

GetMerchantAccountReferenceIdOk returns a tuple with the MerchantAccountReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantAccountReferenceId

`func (o *PaymentMethod) SetMerchantAccountReferenceId(v string)`

SetMerchantAccountReferenceId sets MerchantAccountReferenceId field to given value.

### HasMerchantAccountReferenceId

`func (o *PaymentMethod) HasMerchantAccountReferenceId() bool`

HasMerchantAccountReferenceId returns a boolean if a field has been set.

### SetMerchantAccountReferenceIdNil

`func (o *PaymentMethod) SetMerchantAccountReferenceIdNil(b bool)`

 SetMerchantAccountReferenceIdNil sets the value for MerchantAccountReferenceId to be an explicit nil

### UnsetMerchantAccountReferenceId
`func (o *PaymentMethod) UnsetMerchantAccountReferenceId()`

UnsetMerchantAccountReferenceId ensures that no value is present for MerchantAccountReferenceId, not even an explicit nil
### GetPaymentMethodId

`func (o *PaymentMethod) GetPaymentMethodId() string`

GetPaymentMethodId returns the PaymentMethodId field if non-nil, zero value otherwise.

### GetPaymentMethodIdOk

`func (o *PaymentMethod) GetPaymentMethodIdOk() (*string, bool)`

GetPaymentMethodIdOk returns a tuple with the PaymentMethodId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentMethodId

`func (o *PaymentMethod) SetPaymentMethodId(v string)`

SetPaymentMethodId sets PaymentMethodId field to given value.

### HasPaymentMethodId

`func (o *PaymentMethod) HasPaymentMethodId() bool`

HasPaymentMethodId returns a boolean if a field has been set.

### SetPaymentMethodIdNil

`func (o *PaymentMethod) SetPaymentMethodIdNil(b bool)`

 SetPaymentMethodIdNil sets the value for PaymentMethodId to be an explicit nil

### UnsetPaymentMethodId
`func (o *PaymentMethod) UnsetPaymentMethodId()`

UnsetPaymentMethodId ensures that no value is present for PaymentMethodId, not even an explicit nil
### GetIssuerIdentificationNumber

`func (o *PaymentMethod) GetIssuerIdentificationNumber() string`

GetIssuerIdentificationNumber returns the IssuerIdentificationNumber field if non-nil, zero value otherwise.

### GetIssuerIdentificationNumberOk

`func (o *PaymentMethod) GetIssuerIdentificationNumberOk() (*string, bool)`

GetIssuerIdentificationNumberOk returns a tuple with the IssuerIdentificationNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIssuerIdentificationNumber

`func (o *PaymentMethod) SetIssuerIdentificationNumber(v string)`

SetIssuerIdentificationNumber sets IssuerIdentificationNumber field to given value.

### HasIssuerIdentificationNumber

`func (o *PaymentMethod) HasIssuerIdentificationNumber() bool`

HasIssuerIdentificationNumber returns a boolean if a field has been set.

### SetIssuerIdentificationNumberNil

`func (o *PaymentMethod) SetIssuerIdentificationNumberNil(b bool)`

 SetIssuerIdentificationNumberNil sets the value for IssuerIdentificationNumber to be an explicit nil

### UnsetIssuerIdentificationNumber
`func (o *PaymentMethod) UnsetIssuerIdentificationNumber()`

UnsetIssuerIdentificationNumber ensures that no value is present for IssuerIdentificationNumber, not even an explicit nil
### GetBillingAddress

`func (o *PaymentMethod) GetBillingAddress() Address`

GetBillingAddress returns the BillingAddress field if non-nil, zero value otherwise.

### GetBillingAddressOk

`func (o *PaymentMethod) GetBillingAddressOk() (*Address, bool)`

GetBillingAddressOk returns a tuple with the BillingAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBillingAddress

`func (o *PaymentMethod) SetBillingAddress(v Address)`

SetBillingAddress sets BillingAddress field to given value.

### HasBillingAddress

`func (o *PaymentMethod) HasBillingAddress() bool`

HasBillingAddress returns a boolean if a field has been set.

### GetShippingAddress

`func (o *PaymentMethod) GetShippingAddress() Address`

GetShippingAddress returns the ShippingAddress field if non-nil, zero value otherwise.

### GetShippingAddressOk

`func (o *PaymentMethod) GetShippingAddressOk() (*Address, bool)`

GetShippingAddressOk returns a tuple with the ShippingAddress field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingAddress

`func (o *PaymentMethod) SetShippingAddress(v Address)`

SetShippingAddress sets ShippingAddress field to given value.

### HasShippingAddress

`func (o *PaymentMethod) HasShippingAddress() bool`

HasShippingAddress returns a boolean if a field has been set.

### GetCreditCard

`func (o *PaymentMethod) GetCreditCard() CreditCard`

GetCreditCard returns the CreditCard field if non-nil, zero value otherwise.

### GetCreditCardOk

`func (o *PaymentMethod) GetCreditCardOk() (*CreditCard, bool)`

GetCreditCardOk returns a tuple with the CreditCard field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCreditCard

`func (o *PaymentMethod) SetCreditCard(v CreditCard)`

SetCreditCard sets CreditCard field to given value.

### HasCreditCard

`func (o *PaymentMethod) HasCreditCard() bool`

HasCreditCard returns a boolean if a field has been set.

### GetGatewayPaymentMethod

`func (o *PaymentMethod) GetGatewayPaymentMethod() GatewayPaymentMethod`

GetGatewayPaymentMethod returns the GatewayPaymentMethod field if non-nil, zero value otherwise.

### GetGatewayPaymentMethodOk

`func (o *PaymentMethod) GetGatewayPaymentMethodOk() (*GatewayPaymentMethod, bool)`

GetGatewayPaymentMethodOk returns a tuple with the GatewayPaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayPaymentMethod

`func (o *PaymentMethod) SetGatewayPaymentMethod(v GatewayPaymentMethod)`

SetGatewayPaymentMethod sets GatewayPaymentMethod field to given value.

### HasGatewayPaymentMethod

`func (o *PaymentMethod) HasGatewayPaymentMethod() bool`

HasGatewayPaymentMethod returns a boolean if a field has been set.

### GetVaultPaymentMethod

`func (o *PaymentMethod) GetVaultPaymentMethod() VaultPaymentMethod`

GetVaultPaymentMethod returns the VaultPaymentMethod field if non-nil, zero value otherwise.

### GetVaultPaymentMethodOk

`func (o *PaymentMethod) GetVaultPaymentMethodOk() (*VaultPaymentMethod, bool)`

GetVaultPaymentMethodOk returns a tuple with the VaultPaymentMethod field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetVaultPaymentMethod

`func (o *PaymentMethod) SetVaultPaymentMethod(v VaultPaymentMethod)`

SetVaultPaymentMethod sets VaultPaymentMethod field to given value.

### HasVaultPaymentMethod

`func (o *PaymentMethod) HasVaultPaymentMethod() bool`

HasVaultPaymentMethod returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


