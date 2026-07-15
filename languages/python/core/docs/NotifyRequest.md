# NotifyRequest

Notification request to inform Revaly of specific business events

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_type** | **str** | Type of business event being reported. The event type determines how Revaly processes the notification.  - **recordPayment**: Record a payment transaction - **recordRefund**: Record a refund transaction - **recordChargeback**: Record a chargeback on a transaction - **endOutreach**: End an outreach campaign for a customer - **updateCustomerData**: Update customer information and contact details  | 
**data** | [**NotifyData**](NotifyData.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.notify_request import NotifyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of NotifyRequest from a JSON string
notify_request_instance = NotifyRequest.from_json(json)
# print the JSON string representation of the object
print(NotifyRequest.to_json())

# convert the object into a dict
notify_request_dict = notify_request_instance.to_dict()
# create an instance of NotifyRequest from a dict
notify_request_from_dict = NotifyRequest.from_dict(notify_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


