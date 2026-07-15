# NotifyRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_type** | **string** | Type of business event being reported. The event type determines how Revaly processes the notification.  - **recordPayment**: Record a payment transaction - **recordRefund**: Record a refund transaction - **recordChargeback**: Record a chargeback on a transaction - **endOutreach**: End an outreach campaign for a customer - **updateCustomerData**: Update customer information and contact details |
**data** | [**\Revaly\Sdk\Core\Model\NotifyData**](NotifyData.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
