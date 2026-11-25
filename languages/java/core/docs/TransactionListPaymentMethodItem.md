

# TransactionListPaymentMethodItem

A payment-method operation (create, update, redact or recache) in the list transactions endpoint with the detailed response type. Its fields are wrapped in `transaction`, and its payment method is the flat `TransactionListPaymentMethod`. In simplified mode the same operations are returned as a flat `TransactionListItem`. A field with no value is omitted. 

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transaction** | [**TransactionListPaymentMethodItemTransaction**](TransactionListPaymentMethodItemTransaction.md) |  |  |



