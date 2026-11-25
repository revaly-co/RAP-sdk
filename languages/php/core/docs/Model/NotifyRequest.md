# NotifyRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_type** | **string** | Type of business event being reported. The event type determines how Revaly processes the notification.  - **recordPayment**: Record a payment transaction - **recordRefund**: Record a refund transaction. Requires &#x60;data.transactionId&#x60;. - **recordChargeback**: Record a chargeback on a transaction. Requires &#x60;data.transactionId&#x60;. - **endOutreach**: End an outreach campaign for a customer. Requires &#x60;data.customerId&#x60;. - **updateCustomerData**: Update customer information and contact details. Requires &#x60;data.customerId&#x60;. |
**data** | [**\Revaly\Sdk\Core\Model\NotifyData**](NotifyData.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
