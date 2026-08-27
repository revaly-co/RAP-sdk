

# TransactionGroupResponse

Envelope returned by the V2 transaction-details lookups when `includeAllTransactions=true`. Contains the matched transaction plus every transaction belonging to the same payment — all attempts and lifecycle operations (capture, refund, void) that share the same initial transaction id. If the matched transaction has no initial transaction id, `transactions` contains only the matched record.  The required `transactions` member is always present and discriminates this envelope from a single `TransactionResponse`, which never carries a `transactions` member. 

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transaction** | [**TransactionResponse**](TransactionResponse.md) | The transaction matching the supplied id (the record the non-expanded lookup returns). |  [optional] |
|**transactions** | [**List&lt;TransactionResponse&gt;**](TransactionResponse.md) | Every transaction in the payment, ordered by transaction date ascending. Capped at 100. |  |



