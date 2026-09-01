# NotifyData

Event-specific data for notification requests

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | Revaly transaction identifier | [optional] 
**merchant_transaction_id** | **str** | Merchant&#39;s transaction identifier. For &#x60;recordRefund&#x60; events referencing a transaction that was processed through Revaly gateway routing, this field is required, must be at most 50 characters, and must not have been used by any previous transaction — it becomes the recorded refund&#39;s own merchant transaction id, retrievable via &#x60;GET /transactions/merchant/{merchantTransactionId}&#x60;. | [optional] 
**order_id** | **str** | Order identifier associated with the transaction | [optional] 
**customer_id** | **str** | Customer identifier | [optional] 
**amount** | **int** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**currency** | **str** | Three-letter ISO currency code | [optional] 
**customer_account_number** | **str** | Customer account number for recovery purposes | [optional] 
**disable_sms_notification** | **bool** | Whether to disable SMS notifications for this customer | [optional] 
**disable_email_notification** | **bool** | Whether to disable email notifications for this customer | [optional] 
**contact_information** | [**NotifyContactInformation**](NotifyContactInformation.md) |  | [optional] 
**address** | [**Address**](Address.md) |  | [optional] 
**reason_code** | **str** | Network chargeback reason code (e.g. Visa \&quot;10.4\&quot;). Chargeback-only, optional. | [optional] 
**arn** | **str** | Acquirer Reference Number or network case ID for the dispute. Chargeback-only, optional. | [optional] 
**dispute_date** | **datetime** | When the dispute was raised. Chargeback-only, optional. | [optional] 

## Example

```python
from revaly_sdk_core.models.notify_data import NotifyData

# TODO update the JSON string below
json = "{}"
# create an instance of NotifyData from a JSON string
notify_data_instance = NotifyData.from_json(json)
# print the JSON string representation of the object
print(NotifyData.to_json())

# convert the object into a dict
notify_data_dict = notify_data_instance.to_dict()
# create an instance of NotifyData from a dict
notify_data_from_dict = NotifyData.from_dict(notify_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


