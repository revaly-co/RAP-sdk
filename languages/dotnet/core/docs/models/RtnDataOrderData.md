# Revaly.Sdk.Core.Model.RtnDataOrderData
Order and purchase details. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PurchaseDate** | **DateTime** | ISO 8601 UTC timestamp of the purchase. | [optional] 
**ItemCount** | **int** | Total number of items in the order. | [optional] 
**HighestPriceItemPrice** | **int** | Price of the most expensive item in minor currency units. | [optional] 
**HighestPriceItemBrand** | **string** | Brand of the most expensive item. | [optional] 
**HighestPriceItemCategory** | **string** | Category of the most expensive item. | [optional] 
**IsPreOrderPurchase** | **bool** | True if the order contains pre-order items. | [optional] 
**PreOrderDate** | **string** | Expected availability date for pre-order items. Format YYYYMMDD. | [optional] 
**IsReorder** | **bool** | True if the customer has previously purchased this item. | [optional] 
**InstallmentPaymentCount** | **int** | Number of installment payments for this transaction. | [optional] 
**IsRecurringPurchase** | **bool** | True if this purchase is part of a recurring series. | [optional] 
**RecurringIntervalDays** | **int** | Days between recurring charges. | [optional] 
**RecurringEndDate** | **string** | End date for recurring charges. Format YYYYMMDD. | [optional] 
**AlternatePaymentIndicator** | **string** | Alternative payment method: 01 &#x3D; none, 02 &#x3D; coupon, 03 &#x3D; gift card, 04 &#x3D; store credit. | [optional] 
**GiftCardCount** | **int** | Number of gift cards applied to this order. | [optional] 
**GiftCardAmount** | **int** | Total gift card amount in minor currency units. | [optional] 
**GiftCardCurrency** | **string** | ISO 4217 numeric currency code for gift card amount. | [optional] 
**InstallmentPaymentData** | **string** | Number of installment payments as a string. String companion to installmentPaymentCount for FIs that expect a string. | [optional] 
**TopItemCategories** | **string** | Up to five item-category codes concatenated as four-digit codes. | [optional] 
**HighestPriceItemSku** | **string** | SKU of the most expensive item in the order. | [optional] 
**IsCouponUsed** | **string** | Whether a coupon was used (Amex is_coupon_used). Narrower than alternatePaymentIndicator. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

