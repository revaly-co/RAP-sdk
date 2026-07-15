# PaymentPlanData

Payment plan and subscription information for recurring transactions

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sku** | **str** | Stock Keeping Unit identifier for the product | [optional] 
**category** | **str** | Product category | [optional] 
**billing_plan** | [**BillingPlan**](BillingPlan.md) |  | [optional] 
**subscription_id** | **str** | Subscription identifier | [optional] 
**billing_cycle** | **int** | Number of billing cycles | [optional] 
**payment_model** | **str** | Payment model type | [optional] 
**product_display_name** | **str** | Human-readable product name | [optional] 

## Example

```python
from revaly_sdk_core.models.payment_plan_data import PaymentPlanData

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentPlanData from a JSON string
payment_plan_data_instance = PaymentPlanData.from_json(json)
# print the JSON string representation of the object
print(PaymentPlanData.to_json())

# convert the object into a dict
payment_plan_data_dict = payment_plan_data_instance.to_dict()
# create an instance of PaymentPlanData from a dict
payment_plan_data_from_dict = PaymentPlanData.from_dict(payment_plan_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


