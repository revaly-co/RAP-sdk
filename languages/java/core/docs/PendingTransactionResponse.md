

# PendingTransactionResponse

Pending payment intent. Returned by the merchant-transaction lookup when the platform has accepted a payment with this merchantTransactionId (the intent was durably recorded before gateway dispatch) but no transaction record is visible yet. Poll the same lookup again: it resolves to the full TransactionResponse once the transaction becomes visible. This shape is deliberately distinct from TransactionResponse — use the required `state` field as the discriminator.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**state** | [**StateEnum**](#StateEnum) | Always &#x60;pending&#x60; — discriminates this shape from a completed transaction. |  |
|**merchantTransactionId** | **String** | Merchant-provided transaction identifier the intent was recorded under |  |
|**transactionType** | **String** | Operation the intent was recorded for — \&quot;Charge\&quot; or \&quot;Authorize\&quot; (same vocabulary as TransactionResponse.transactionType). |  [optional] |
|**receivedAt** | **OffsetDateTime** | When the platform recorded the payment intent (ISO 8601) |  [optional] |



## Enum: StateEnum

| Name | Value |
|---- | -----|
| PENDING | &quot;pending&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



