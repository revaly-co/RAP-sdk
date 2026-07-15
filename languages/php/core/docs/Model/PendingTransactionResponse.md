# PendingTransactionResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state** | **string** | Always &#x60;pending&#x60; — discriminates this shape from a completed transaction. |
**merchant_transaction_id** | **string** | Merchant-provided transaction identifier the intent was recorded under |
**transaction_type** | **string** | Operation the intent was recorded for — \&quot;Charge\&quot; or \&quot;Authorize\&quot; (same vocabulary as TransactionResponse.transactionType). | [optional]
**received_at** | **\DateTime** | When the platform recorded the payment intent (ISO 8601) | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
