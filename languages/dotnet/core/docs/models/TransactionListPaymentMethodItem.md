# Revaly.Sdk.Core.Model.TransactionListPaymentMethodItem
A payment-method operation (create, update, redact or recache) in the list transactions endpoint with the detailed response type. Its fields are wrapped in `transaction`, and its payment method is the flat `TransactionListPaymentMethod`. In simplified mode the same operations are returned as a flat `TransactionListItem`. A field with no value is omitted. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Transaction** | [**TransactionListPaymentMethodItemTransaction**](TransactionListPaymentMethodItemTransaction.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

