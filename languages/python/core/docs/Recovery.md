# Recovery

Recovery settings and customer recovery information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**disable_customer_recovery** | **bool** | Whether customer recovery is disabled for this transaction | [optional] 
**external_approval** | **bool** | Describes whether the approval should be attributed to the merchant for billing purposes | [optional] 
**customer_account_number** | **str** | Customer account number for recovery purposes | [optional] 
**customer_balance** | **int** | Customer account balance in smallest currency unit (e.g., cents for USD) | [optional] 
**disable_sms_notification** | **bool** | Whether SMS notifications are disabled for recovery | [optional] 
**disable_email_notification** | **bool** | Whether email notifications are disabled for recovery | [optional] 
**retry_count** | **int** | Number of retry attempts for this billing cycle (initial attempt is 0) | [optional] 
**payment_reference_data** | **str** | Reference data received when a payment failed. This data should be returned on retry transactions for the same payment. | [optional] 
**date_first_attempt** | **datetime** | Date and time of the first transaction attempt for this billing cycle. Required when retry count is greater than 0. | [optional] 

## Example

```python
from revaly_sdk_core.models.recovery import Recovery

# TODO update the JSON string below
json = "{}"
# create an instance of Recovery from a JSON string
recovery_instance = Recovery.from_json(json)
# print the JSON string representation of the object
print(Recovery.to_json())

# convert the object into a dict
recovery_dict = recovery_instance.to_dict()
# create an instance of Recovery from a dict
recovery_from_dict = Recovery.from_dict(recovery_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


