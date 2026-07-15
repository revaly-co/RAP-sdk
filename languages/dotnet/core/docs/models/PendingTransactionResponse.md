# Revaly.Sdk.Core.Model.PendingTransactionResponse
Pending payment intent. Returned by the merchant-transaction lookup when the platform has accepted a payment with this merchantTransactionId (the intent was durably recorded before gateway dispatch) but no transaction record is visible yet. Poll the same lookup again: it resolves to the full TransactionResponse once the transaction becomes visible. This shape is deliberately distinct from TransactionResponse — use the required `state` field as the discriminator.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**State** | **string** | Always &#x60;pending&#x60; — discriminates this shape from a completed transaction. | 
**MerchantTransactionId** | **string** | Merchant-provided transaction identifier the intent was recorded under | 
**TransactionType** | **string** | Operation the intent was recorded for — \&quot;Charge\&quot; or \&quot;Authorize\&quot; (same vocabulary as TransactionResponse.transactionType). | [optional] 
**ReceivedAt** | **DateTime** | When the platform recorded the payment intent (ISO 8601) | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

