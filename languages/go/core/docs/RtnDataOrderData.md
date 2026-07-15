# RtnDataOrderData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PurchaseDate** | Pointer to **time.Time** | ISO 8601 UTC timestamp of the purchase. | [optional] 
**ItemCount** | Pointer to **int32** | Total number of items in the order. | [optional] 
**HighestPriceItemPrice** | Pointer to **int32** | Price of the most expensive item in minor currency units. | [optional] 
**HighestPriceItemBrand** | Pointer to **string** | Brand of the most expensive item. | [optional] 
**HighestPriceItemCategory** | Pointer to **string** | Category of the most expensive item. | [optional] 
**IsPreOrderPurchase** | Pointer to **bool** | True if the order contains pre-order items. | [optional] 
**PreOrderDate** | Pointer to **string** | Expected availability date for pre-order items. Format YYYYMMDD. | [optional] 
**IsReorder** | Pointer to **bool** | True if the customer has previously purchased this item. | [optional] 
**InstallmentPaymentCount** | Pointer to **int32** | Number of installment payments for this transaction. | [optional] 
**IsRecurringPurchase** | Pointer to **bool** | True if this purchase is part of a recurring series. | [optional] 
**RecurringIntervalDays** | Pointer to **int32** | Days between recurring charges. | [optional] 
**RecurringEndDate** | Pointer to **string** | End date for recurring charges. Format YYYYMMDD. | [optional] 
**AlternatePaymentIndicator** | Pointer to **string** | Alternative payment method: 01 &#x3D; none, 02 &#x3D; coupon, 03 &#x3D; gift card, 04 &#x3D; store credit. | [optional] 
**GiftCardCount** | Pointer to **int32** | Number of gift cards applied to this order. | [optional] 
**GiftCardAmount** | Pointer to **int32** | Total gift card amount in minor currency units. | [optional] 
**GiftCardCurrency** | Pointer to **string** | ISO 4217 numeric currency code for gift card amount. | [optional] 
**InstallmentPaymentData** | Pointer to **string** | Number of installment payments as a string. String companion to installmentPaymentCount for FIs that expect a string. | [optional] 
**TopItemCategories** | Pointer to **string** | Up to five item-category codes concatenated as four-digit codes. | [optional] 
**HighestPriceItemSku** | Pointer to **string** | SKU of the most expensive item in the order. | [optional] 
**IsCouponUsed** | Pointer to **string** | Whether a coupon was used (Amex is_coupon_used). Narrower than alternatePaymentIndicator. | [optional] 

## Methods

### NewRtnDataOrderData

`func NewRtnDataOrderData() *RtnDataOrderData`

NewRtnDataOrderData instantiates a new RtnDataOrderData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataOrderDataWithDefaults

`func NewRtnDataOrderDataWithDefaults() *RtnDataOrderData`

NewRtnDataOrderDataWithDefaults instantiates a new RtnDataOrderData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetPurchaseDate

`func (o *RtnDataOrderData) GetPurchaseDate() time.Time`

GetPurchaseDate returns the PurchaseDate field if non-nil, zero value otherwise.

### GetPurchaseDateOk

`func (o *RtnDataOrderData) GetPurchaseDateOk() (*time.Time, bool)`

GetPurchaseDateOk returns a tuple with the PurchaseDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPurchaseDate

`func (o *RtnDataOrderData) SetPurchaseDate(v time.Time)`

SetPurchaseDate sets PurchaseDate field to given value.

### HasPurchaseDate

`func (o *RtnDataOrderData) HasPurchaseDate() bool`

HasPurchaseDate returns a boolean if a field has been set.

### GetItemCount

`func (o *RtnDataOrderData) GetItemCount() int32`

GetItemCount returns the ItemCount field if non-nil, zero value otherwise.

### GetItemCountOk

`func (o *RtnDataOrderData) GetItemCountOk() (*int32, bool)`

GetItemCountOk returns a tuple with the ItemCount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetItemCount

`func (o *RtnDataOrderData) SetItemCount(v int32)`

SetItemCount sets ItemCount field to given value.

### HasItemCount

`func (o *RtnDataOrderData) HasItemCount() bool`

HasItemCount returns a boolean if a field has been set.

### GetHighestPriceItemPrice

`func (o *RtnDataOrderData) GetHighestPriceItemPrice() int32`

GetHighestPriceItemPrice returns the HighestPriceItemPrice field if non-nil, zero value otherwise.

### GetHighestPriceItemPriceOk

`func (o *RtnDataOrderData) GetHighestPriceItemPriceOk() (*int32, bool)`

GetHighestPriceItemPriceOk returns a tuple with the HighestPriceItemPrice field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetHighestPriceItemPrice

`func (o *RtnDataOrderData) SetHighestPriceItemPrice(v int32)`

SetHighestPriceItemPrice sets HighestPriceItemPrice field to given value.

### HasHighestPriceItemPrice

`func (o *RtnDataOrderData) HasHighestPriceItemPrice() bool`

HasHighestPriceItemPrice returns a boolean if a field has been set.

### GetHighestPriceItemBrand

`func (o *RtnDataOrderData) GetHighestPriceItemBrand() string`

GetHighestPriceItemBrand returns the HighestPriceItemBrand field if non-nil, zero value otherwise.

### GetHighestPriceItemBrandOk

`func (o *RtnDataOrderData) GetHighestPriceItemBrandOk() (*string, bool)`

GetHighestPriceItemBrandOk returns a tuple with the HighestPriceItemBrand field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetHighestPriceItemBrand

`func (o *RtnDataOrderData) SetHighestPriceItemBrand(v string)`

SetHighestPriceItemBrand sets HighestPriceItemBrand field to given value.

### HasHighestPriceItemBrand

`func (o *RtnDataOrderData) HasHighestPriceItemBrand() bool`

HasHighestPriceItemBrand returns a boolean if a field has been set.

### GetHighestPriceItemCategory

`func (o *RtnDataOrderData) GetHighestPriceItemCategory() string`

GetHighestPriceItemCategory returns the HighestPriceItemCategory field if non-nil, zero value otherwise.

### GetHighestPriceItemCategoryOk

`func (o *RtnDataOrderData) GetHighestPriceItemCategoryOk() (*string, bool)`

GetHighestPriceItemCategoryOk returns a tuple with the HighestPriceItemCategory field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetHighestPriceItemCategory

`func (o *RtnDataOrderData) SetHighestPriceItemCategory(v string)`

SetHighestPriceItemCategory sets HighestPriceItemCategory field to given value.

### HasHighestPriceItemCategory

`func (o *RtnDataOrderData) HasHighestPriceItemCategory() bool`

HasHighestPriceItemCategory returns a boolean if a field has been set.

### GetIsPreOrderPurchase

`func (o *RtnDataOrderData) GetIsPreOrderPurchase() bool`

GetIsPreOrderPurchase returns the IsPreOrderPurchase field if non-nil, zero value otherwise.

### GetIsPreOrderPurchaseOk

`func (o *RtnDataOrderData) GetIsPreOrderPurchaseOk() (*bool, bool)`

GetIsPreOrderPurchaseOk returns a tuple with the IsPreOrderPurchase field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsPreOrderPurchase

`func (o *RtnDataOrderData) SetIsPreOrderPurchase(v bool)`

SetIsPreOrderPurchase sets IsPreOrderPurchase field to given value.

### HasIsPreOrderPurchase

`func (o *RtnDataOrderData) HasIsPreOrderPurchase() bool`

HasIsPreOrderPurchase returns a boolean if a field has been set.

### GetPreOrderDate

`func (o *RtnDataOrderData) GetPreOrderDate() string`

GetPreOrderDate returns the PreOrderDate field if non-nil, zero value otherwise.

### GetPreOrderDateOk

`func (o *RtnDataOrderData) GetPreOrderDateOk() (*string, bool)`

GetPreOrderDateOk returns a tuple with the PreOrderDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPreOrderDate

`func (o *RtnDataOrderData) SetPreOrderDate(v string)`

SetPreOrderDate sets PreOrderDate field to given value.

### HasPreOrderDate

`func (o *RtnDataOrderData) HasPreOrderDate() bool`

HasPreOrderDate returns a boolean if a field has been set.

### GetIsReorder

`func (o *RtnDataOrderData) GetIsReorder() bool`

GetIsReorder returns the IsReorder field if non-nil, zero value otherwise.

### GetIsReorderOk

`func (o *RtnDataOrderData) GetIsReorderOk() (*bool, bool)`

GetIsReorderOk returns a tuple with the IsReorder field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsReorder

`func (o *RtnDataOrderData) SetIsReorder(v bool)`

SetIsReorder sets IsReorder field to given value.

### HasIsReorder

`func (o *RtnDataOrderData) HasIsReorder() bool`

HasIsReorder returns a boolean if a field has been set.

### GetInstallmentPaymentCount

`func (o *RtnDataOrderData) GetInstallmentPaymentCount() int32`

GetInstallmentPaymentCount returns the InstallmentPaymentCount field if non-nil, zero value otherwise.

### GetInstallmentPaymentCountOk

`func (o *RtnDataOrderData) GetInstallmentPaymentCountOk() (*int32, bool)`

GetInstallmentPaymentCountOk returns a tuple with the InstallmentPaymentCount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInstallmentPaymentCount

`func (o *RtnDataOrderData) SetInstallmentPaymentCount(v int32)`

SetInstallmentPaymentCount sets InstallmentPaymentCount field to given value.

### HasInstallmentPaymentCount

`func (o *RtnDataOrderData) HasInstallmentPaymentCount() bool`

HasInstallmentPaymentCount returns a boolean if a field has been set.

### GetIsRecurringPurchase

`func (o *RtnDataOrderData) GetIsRecurringPurchase() bool`

GetIsRecurringPurchase returns the IsRecurringPurchase field if non-nil, zero value otherwise.

### GetIsRecurringPurchaseOk

`func (o *RtnDataOrderData) GetIsRecurringPurchaseOk() (*bool, bool)`

GetIsRecurringPurchaseOk returns a tuple with the IsRecurringPurchase field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsRecurringPurchase

`func (o *RtnDataOrderData) SetIsRecurringPurchase(v bool)`

SetIsRecurringPurchase sets IsRecurringPurchase field to given value.

### HasIsRecurringPurchase

`func (o *RtnDataOrderData) HasIsRecurringPurchase() bool`

HasIsRecurringPurchase returns a boolean if a field has been set.

### GetRecurringIntervalDays

`func (o *RtnDataOrderData) GetRecurringIntervalDays() int32`

GetRecurringIntervalDays returns the RecurringIntervalDays field if non-nil, zero value otherwise.

### GetRecurringIntervalDaysOk

`func (o *RtnDataOrderData) GetRecurringIntervalDaysOk() (*int32, bool)`

GetRecurringIntervalDaysOk returns a tuple with the RecurringIntervalDays field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRecurringIntervalDays

`func (o *RtnDataOrderData) SetRecurringIntervalDays(v int32)`

SetRecurringIntervalDays sets RecurringIntervalDays field to given value.

### HasRecurringIntervalDays

`func (o *RtnDataOrderData) HasRecurringIntervalDays() bool`

HasRecurringIntervalDays returns a boolean if a field has been set.

### GetRecurringEndDate

`func (o *RtnDataOrderData) GetRecurringEndDate() string`

GetRecurringEndDate returns the RecurringEndDate field if non-nil, zero value otherwise.

### GetRecurringEndDateOk

`func (o *RtnDataOrderData) GetRecurringEndDateOk() (*string, bool)`

GetRecurringEndDateOk returns a tuple with the RecurringEndDate field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRecurringEndDate

`func (o *RtnDataOrderData) SetRecurringEndDate(v string)`

SetRecurringEndDate sets RecurringEndDate field to given value.

### HasRecurringEndDate

`func (o *RtnDataOrderData) HasRecurringEndDate() bool`

HasRecurringEndDate returns a boolean if a field has been set.

### GetAlternatePaymentIndicator

`func (o *RtnDataOrderData) GetAlternatePaymentIndicator() string`

GetAlternatePaymentIndicator returns the AlternatePaymentIndicator field if non-nil, zero value otherwise.

### GetAlternatePaymentIndicatorOk

`func (o *RtnDataOrderData) GetAlternatePaymentIndicatorOk() (*string, bool)`

GetAlternatePaymentIndicatorOk returns a tuple with the AlternatePaymentIndicator field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAlternatePaymentIndicator

`func (o *RtnDataOrderData) SetAlternatePaymentIndicator(v string)`

SetAlternatePaymentIndicator sets AlternatePaymentIndicator field to given value.

### HasAlternatePaymentIndicator

`func (o *RtnDataOrderData) HasAlternatePaymentIndicator() bool`

HasAlternatePaymentIndicator returns a boolean if a field has been set.

### GetGiftCardCount

`func (o *RtnDataOrderData) GetGiftCardCount() int32`

GetGiftCardCount returns the GiftCardCount field if non-nil, zero value otherwise.

### GetGiftCardCountOk

`func (o *RtnDataOrderData) GetGiftCardCountOk() (*int32, bool)`

GetGiftCardCountOk returns a tuple with the GiftCardCount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGiftCardCount

`func (o *RtnDataOrderData) SetGiftCardCount(v int32)`

SetGiftCardCount sets GiftCardCount field to given value.

### HasGiftCardCount

`func (o *RtnDataOrderData) HasGiftCardCount() bool`

HasGiftCardCount returns a boolean if a field has been set.

### GetGiftCardAmount

`func (o *RtnDataOrderData) GetGiftCardAmount() int32`

GetGiftCardAmount returns the GiftCardAmount field if non-nil, zero value otherwise.

### GetGiftCardAmountOk

`func (o *RtnDataOrderData) GetGiftCardAmountOk() (*int32, bool)`

GetGiftCardAmountOk returns a tuple with the GiftCardAmount field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGiftCardAmount

`func (o *RtnDataOrderData) SetGiftCardAmount(v int32)`

SetGiftCardAmount sets GiftCardAmount field to given value.

### HasGiftCardAmount

`func (o *RtnDataOrderData) HasGiftCardAmount() bool`

HasGiftCardAmount returns a boolean if a field has been set.

### GetGiftCardCurrency

`func (o *RtnDataOrderData) GetGiftCardCurrency() string`

GetGiftCardCurrency returns the GiftCardCurrency field if non-nil, zero value otherwise.

### GetGiftCardCurrencyOk

`func (o *RtnDataOrderData) GetGiftCardCurrencyOk() (*string, bool)`

GetGiftCardCurrencyOk returns a tuple with the GiftCardCurrency field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGiftCardCurrency

`func (o *RtnDataOrderData) SetGiftCardCurrency(v string)`

SetGiftCardCurrency sets GiftCardCurrency field to given value.

### HasGiftCardCurrency

`func (o *RtnDataOrderData) HasGiftCardCurrency() bool`

HasGiftCardCurrency returns a boolean if a field has been set.

### GetInstallmentPaymentData

`func (o *RtnDataOrderData) GetInstallmentPaymentData() string`

GetInstallmentPaymentData returns the InstallmentPaymentData field if non-nil, zero value otherwise.

### GetInstallmentPaymentDataOk

`func (o *RtnDataOrderData) GetInstallmentPaymentDataOk() (*string, bool)`

GetInstallmentPaymentDataOk returns a tuple with the InstallmentPaymentData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetInstallmentPaymentData

`func (o *RtnDataOrderData) SetInstallmentPaymentData(v string)`

SetInstallmentPaymentData sets InstallmentPaymentData field to given value.

### HasInstallmentPaymentData

`func (o *RtnDataOrderData) HasInstallmentPaymentData() bool`

HasInstallmentPaymentData returns a boolean if a field has been set.

### GetTopItemCategories

`func (o *RtnDataOrderData) GetTopItemCategories() string`

GetTopItemCategories returns the TopItemCategories field if non-nil, zero value otherwise.

### GetTopItemCategoriesOk

`func (o *RtnDataOrderData) GetTopItemCategoriesOk() (*string, bool)`

GetTopItemCategoriesOk returns a tuple with the TopItemCategories field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTopItemCategories

`func (o *RtnDataOrderData) SetTopItemCategories(v string)`

SetTopItemCategories sets TopItemCategories field to given value.

### HasTopItemCategories

`func (o *RtnDataOrderData) HasTopItemCategories() bool`

HasTopItemCategories returns a boolean if a field has been set.

### GetHighestPriceItemSku

`func (o *RtnDataOrderData) GetHighestPriceItemSku() string`

GetHighestPriceItemSku returns the HighestPriceItemSku field if non-nil, zero value otherwise.

### GetHighestPriceItemSkuOk

`func (o *RtnDataOrderData) GetHighestPriceItemSkuOk() (*string, bool)`

GetHighestPriceItemSkuOk returns a tuple with the HighestPriceItemSku field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetHighestPriceItemSku

`func (o *RtnDataOrderData) SetHighestPriceItemSku(v string)`

SetHighestPriceItemSku sets HighestPriceItemSku field to given value.

### HasHighestPriceItemSku

`func (o *RtnDataOrderData) HasHighestPriceItemSku() bool`

HasHighestPriceItemSku returns a boolean if a field has been set.

### GetIsCouponUsed

`func (o *RtnDataOrderData) GetIsCouponUsed() string`

GetIsCouponUsed returns the IsCouponUsed field if non-nil, zero value otherwise.

### GetIsCouponUsedOk

`func (o *RtnDataOrderData) GetIsCouponUsedOk() (*string, bool)`

GetIsCouponUsedOk returns a tuple with the IsCouponUsed field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsCouponUsed

`func (o *RtnDataOrderData) SetIsCouponUsed(v string)`

SetIsCouponUsed sets IsCouponUsed field to given value.

### HasIsCouponUsed

`func (o *RtnDataOrderData) HasIsCouponUsed() bool`

HasIsCouponUsed returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


