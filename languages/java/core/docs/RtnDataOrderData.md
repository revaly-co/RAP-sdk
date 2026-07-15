

# RtnDataOrderData

Order and purchase details. All fields optional.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**purchaseDate** | **OffsetDateTime** | ISO 8601 UTC timestamp of the purchase. |  [optional] |
|**itemCount** | **Integer** | Total number of items in the order. |  [optional] |
|**highestPriceItemPrice** | **Integer** | Price of the most expensive item in minor currency units. |  [optional] |
|**highestPriceItemBrand** | **String** | Brand of the most expensive item. |  [optional] |
|**highestPriceItemCategory** | **String** | Category of the most expensive item. |  [optional] |
|**isPreOrderPurchase** | **Boolean** | True if the order contains pre-order items. |  [optional] |
|**preOrderDate** | **String** | Expected availability date for pre-order items. Format YYYYMMDD. |  [optional] |
|**isReorder** | **Boolean** | True if the customer has previously purchased this item. |  [optional] |
|**installmentPaymentCount** | **Integer** | Number of installment payments for this transaction. |  [optional] |
|**isRecurringPurchase** | **Boolean** | True if this purchase is part of a recurring series. |  [optional] |
|**recurringIntervalDays** | **Integer** | Days between recurring charges. |  [optional] |
|**recurringEndDate** | **String** | End date for recurring charges. Format YYYYMMDD. |  [optional] |
|**alternatePaymentIndicator** | [**AlternatePaymentIndicatorEnum**](#AlternatePaymentIndicatorEnum) | Alternative payment method: 01 &#x3D; none, 02 &#x3D; coupon, 03 &#x3D; gift card, 04 &#x3D; store credit. |  [optional] |
|**giftCardCount** | **Integer** | Number of gift cards applied to this order. |  [optional] |
|**giftCardAmount** | **Integer** | Total gift card amount in minor currency units. |  [optional] |
|**giftCardCurrency** | **String** | ISO 4217 numeric currency code for gift card amount. |  [optional] |
|**installmentPaymentData** | **String** | Number of installment payments as a string. String companion to installmentPaymentCount for FIs that expect a string. |  [optional] |
|**topItemCategories** | **String** | Up to five item-category codes concatenated as four-digit codes. |  [optional] |
|**highestPriceItemSku** | **String** | SKU of the most expensive item in the order. |  [optional] |
|**isCouponUsed** | [**IsCouponUsedEnum**](#IsCouponUsedEnum) | Whether a coupon was used (Amex is_coupon_used). Narrower than alternatePaymentIndicator. |  [optional] |



## Enum: AlternatePaymentIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: IsCouponUsedEnum

| Name | Value |
|---- | -----|
| Y | &quot;Y&quot; |
| N | &quot;N&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



