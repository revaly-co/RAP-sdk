# RtnDataOrderData

Order and purchase details. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_date** | **datetime** | ISO 8601 UTC timestamp of the purchase. | [optional] 
**item_count** | **int** | Total number of items in the order. | [optional] 
**highest_price_item_price** | **int** | Price of the most expensive item in minor currency units. | [optional] 
**highest_price_item_brand** | **str** | Brand of the most expensive item. | [optional] 
**highest_price_item_category** | **str** | Category of the most expensive item. | [optional] 
**is_pre_order_purchase** | **bool** | True if the order contains pre-order items. | [optional] 
**pre_order_date** | **str** | Expected availability date for pre-order items. Format YYYYMMDD. | [optional] 
**is_reorder** | **bool** | True if the customer has previously purchased this item. | [optional] 
**installment_payment_count** | **int** | Number of installment payments for this transaction. | [optional] 
**is_recurring_purchase** | **bool** | True if this purchase is part of a recurring series. | [optional] 
**recurring_interval_days** | **int** | Days between recurring charges. | [optional] 
**recurring_end_date** | **str** | End date for recurring charges. Format YYYYMMDD. | [optional] 
**alternate_payment_indicator** | **str** | Alternative payment method: 01 &#x3D; none, 02 &#x3D; coupon, 03 &#x3D; gift card, 04 &#x3D; store credit. | [optional] 
**gift_card_count** | **int** | Number of gift cards applied to this order. | [optional] 
**gift_card_amount** | **int** | Total gift card amount in minor currency units. | [optional] 
**gift_card_currency** | **str** | ISO 4217 numeric currency code for gift card amount. | [optional] 
**installment_payment_data** | **str** | Number of installment payments as a string. String companion to installmentPaymentCount for FIs that expect a string. | [optional] 
**top_item_categories** | **str** | Up to five item-category codes concatenated as four-digit codes. | [optional] 
**highest_price_item_sku** | **str** | SKU of the most expensive item in the order. | [optional] 
**is_coupon_used** | **str** | Whether a coupon was used (Amex is_coupon_used). Narrower than alternatePaymentIndicator. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_order_data import RtnDataOrderData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataOrderData from a JSON string
rtn_data_order_data_instance = RtnDataOrderData.from_json(json)
# print the JSON string representation of the object
print(RtnDataOrderData.to_json())

# convert the object into a dict
rtn_data_order_data_dict = rtn_data_order_data_instance.to_dict()
# create an instance of RtnDataOrderData from a dict
rtn_data_order_data_from_dict = RtnDataOrderData.from_dict(rtn_data_order_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


