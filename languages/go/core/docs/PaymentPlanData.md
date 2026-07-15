# PaymentPlanData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Sku** | Pointer to **NullableString** | Stock Keeping Unit identifier for the product | [optional] 
**Category** | Pointer to **NullableString** | Product category | [optional] 
**BillingPlan** | Pointer to [**NullableBillingPlan**](BillingPlan.md) |  | [optional] 
**SubscriptionId** | Pointer to **NullableString** | Subscription identifier | [optional] 
**BillingCycle** | Pointer to **NullableInt32** | Number of billing cycles | [optional] 
**PaymentModel** | Pointer to **NullableString** | Payment model type | [optional] 
**ProductDisplayName** | Pointer to **NullableString** | Human-readable product name | [optional] 

## Methods

### NewPaymentPlanData

`func NewPaymentPlanData() *PaymentPlanData`

NewPaymentPlanData instantiates a new PaymentPlanData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewPaymentPlanDataWithDefaults

`func NewPaymentPlanDataWithDefaults() *PaymentPlanData`

NewPaymentPlanDataWithDefaults instantiates a new PaymentPlanData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetSku

`func (o *PaymentPlanData) GetSku() string`

GetSku returns the Sku field if non-nil, zero value otherwise.

### GetSkuOk

`func (o *PaymentPlanData) GetSkuOk() (*string, bool)`

GetSkuOk returns a tuple with the Sku field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSku

`func (o *PaymentPlanData) SetSku(v string)`

SetSku sets Sku field to given value.

### HasSku

`func (o *PaymentPlanData) HasSku() bool`

HasSku returns a boolean if a field has been set.

### SetSkuNil

`func (o *PaymentPlanData) SetSkuNil(b bool)`

 SetSkuNil sets the value for Sku to be an explicit nil

### UnsetSku
`func (o *PaymentPlanData) UnsetSku()`

UnsetSku ensures that no value is present for Sku, not even an explicit nil
### GetCategory

`func (o *PaymentPlanData) GetCategory() string`

GetCategory returns the Category field if non-nil, zero value otherwise.

### GetCategoryOk

`func (o *PaymentPlanData) GetCategoryOk() (*string, bool)`

GetCategoryOk returns a tuple with the Category field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCategory

`func (o *PaymentPlanData) SetCategory(v string)`

SetCategory sets Category field to given value.

### HasCategory

`func (o *PaymentPlanData) HasCategory() bool`

HasCategory returns a boolean if a field has been set.

### SetCategoryNil

`func (o *PaymentPlanData) SetCategoryNil(b bool)`

 SetCategoryNil sets the value for Category to be an explicit nil

### UnsetCategory
`func (o *PaymentPlanData) UnsetCategory()`

UnsetCategory ensures that no value is present for Category, not even an explicit nil
### GetBillingPlan

`func (o *PaymentPlanData) GetBillingPlan() BillingPlan`

GetBillingPlan returns the BillingPlan field if non-nil, zero value otherwise.

### GetBillingPlanOk

`func (o *PaymentPlanData) GetBillingPlanOk() (*BillingPlan, bool)`

GetBillingPlanOk returns a tuple with the BillingPlan field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBillingPlan

`func (o *PaymentPlanData) SetBillingPlan(v BillingPlan)`

SetBillingPlan sets BillingPlan field to given value.

### HasBillingPlan

`func (o *PaymentPlanData) HasBillingPlan() bool`

HasBillingPlan returns a boolean if a field has been set.

### SetBillingPlanNil

`func (o *PaymentPlanData) SetBillingPlanNil(b bool)`

 SetBillingPlanNil sets the value for BillingPlan to be an explicit nil

### UnsetBillingPlan
`func (o *PaymentPlanData) UnsetBillingPlan()`

UnsetBillingPlan ensures that no value is present for BillingPlan, not even an explicit nil
### GetSubscriptionId

`func (o *PaymentPlanData) GetSubscriptionId() string`

GetSubscriptionId returns the SubscriptionId field if non-nil, zero value otherwise.

### GetSubscriptionIdOk

`func (o *PaymentPlanData) GetSubscriptionIdOk() (*string, bool)`

GetSubscriptionIdOk returns a tuple with the SubscriptionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSubscriptionId

`func (o *PaymentPlanData) SetSubscriptionId(v string)`

SetSubscriptionId sets SubscriptionId field to given value.

### HasSubscriptionId

`func (o *PaymentPlanData) HasSubscriptionId() bool`

HasSubscriptionId returns a boolean if a field has been set.

### SetSubscriptionIdNil

`func (o *PaymentPlanData) SetSubscriptionIdNil(b bool)`

 SetSubscriptionIdNil sets the value for SubscriptionId to be an explicit nil

### UnsetSubscriptionId
`func (o *PaymentPlanData) UnsetSubscriptionId()`

UnsetSubscriptionId ensures that no value is present for SubscriptionId, not even an explicit nil
### GetBillingCycle

`func (o *PaymentPlanData) GetBillingCycle() int32`

GetBillingCycle returns the BillingCycle field if non-nil, zero value otherwise.

### GetBillingCycleOk

`func (o *PaymentPlanData) GetBillingCycleOk() (*int32, bool)`

GetBillingCycleOk returns a tuple with the BillingCycle field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBillingCycle

`func (o *PaymentPlanData) SetBillingCycle(v int32)`

SetBillingCycle sets BillingCycle field to given value.

### HasBillingCycle

`func (o *PaymentPlanData) HasBillingCycle() bool`

HasBillingCycle returns a boolean if a field has been set.

### SetBillingCycleNil

`func (o *PaymentPlanData) SetBillingCycleNil(b bool)`

 SetBillingCycleNil sets the value for BillingCycle to be an explicit nil

### UnsetBillingCycle
`func (o *PaymentPlanData) UnsetBillingCycle()`

UnsetBillingCycle ensures that no value is present for BillingCycle, not even an explicit nil
### GetPaymentModel

`func (o *PaymentPlanData) GetPaymentModel() string`

GetPaymentModel returns the PaymentModel field if non-nil, zero value otherwise.

### GetPaymentModelOk

`func (o *PaymentPlanData) GetPaymentModelOk() (*string, bool)`

GetPaymentModelOk returns a tuple with the PaymentModel field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentModel

`func (o *PaymentPlanData) SetPaymentModel(v string)`

SetPaymentModel sets PaymentModel field to given value.

### HasPaymentModel

`func (o *PaymentPlanData) HasPaymentModel() bool`

HasPaymentModel returns a boolean if a field has been set.

### SetPaymentModelNil

`func (o *PaymentPlanData) SetPaymentModelNil(b bool)`

 SetPaymentModelNil sets the value for PaymentModel to be an explicit nil

### UnsetPaymentModel
`func (o *PaymentPlanData) UnsetPaymentModel()`

UnsetPaymentModel ensures that no value is present for PaymentModel, not even an explicit nil
### GetProductDisplayName

`func (o *PaymentPlanData) GetProductDisplayName() string`

GetProductDisplayName returns the ProductDisplayName field if non-nil, zero value otherwise.

### GetProductDisplayNameOk

`func (o *PaymentPlanData) GetProductDisplayNameOk() (*string, bool)`

GetProductDisplayNameOk returns a tuple with the ProductDisplayName field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetProductDisplayName

`func (o *PaymentPlanData) SetProductDisplayName(v string)`

SetProductDisplayName sets ProductDisplayName field to given value.

### HasProductDisplayName

`func (o *PaymentPlanData) HasProductDisplayName() bool`

HasProductDisplayName returns a boolean if a field has been set.

### SetProductDisplayNameNil

`func (o *PaymentPlanData) SetProductDisplayNameNil(b bool)`

 SetProductDisplayNameNil sets the value for ProductDisplayName to be an explicit nil

### UnsetProductDisplayName
`func (o *PaymentPlanData) UnsetProductDisplayName()`

UnsetProductDisplayName ensures that no value is present for ProductDisplayName, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


