# Revaly.Sdk.Core.Model.NotifyRequest
Notification request to inform Revaly of specific business events

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**EventType** | **string** | Type of business event being reported. The event type determines how Revaly processes the notification.  - **recordPayment**: Record a payment transaction - **recordRefund**: Record a refund transaction - **recordChargeback**: Record a chargeback on a transaction - **endOutreach**: End an outreach campaign for a customer - **updateCustomerData**: Update customer information and contact details  | 
**Data** | [**NotifyData**](NotifyData.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

