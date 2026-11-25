# Revaly.Sdk.Core.Model.NotifyRequest
Notification request to inform Revaly of specific business events

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**EventType** | **string** | Type of business event being reported. The event type determines how Revaly processes the notification.  - **recordPayment**: Record a payment transaction - **recordRefund**: Record a refund transaction. Requires &#x60;data.transactionId&#x60;. - **recordChargeback**: Record a chargeback on a transaction. Requires &#x60;data.transactionId&#x60;. - **endOutreach**: End an outreach campaign for a customer. Requires &#x60;data.customerId&#x60;. - **updateCustomerData**: Update customer information and contact details. Requires &#x60;data.customerId&#x60;.  | 
**Data** | [**NotifyData**](NotifyData.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

