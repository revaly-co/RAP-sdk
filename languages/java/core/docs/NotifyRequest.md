

# NotifyRequest

Notification request to inform Revaly of specific business events

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**eventType** | [**EventTypeEnum**](#EventTypeEnum) | Type of business event being reported. The event type determines how Revaly processes the notification.  - **recordPayment**: Record a payment transaction - **recordRefund**: Record a refund transaction - **recordChargeback**: Record a chargeback on a transaction - **endOutreach**: End an outreach campaign for a customer - **updateCustomerData**: Update customer information and contact details  |  |
|**data** | [**NotifyData**](NotifyData.md) |  |  [optional] |



## Enum: EventTypeEnum

| Name | Value |
|---- | -----|
| RECORD_PAYMENT | &quot;recordPayment&quot; |
| RECORD_REFUND | &quot;recordRefund&quot; |
| RECORD_CHARGEBACK | &quot;recordChargeback&quot; |
| END_OUTREACH | &quot;endOutreach&quot; |
| UPDATE_CUSTOMER_DATA | &quot;updateCustomerData&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



