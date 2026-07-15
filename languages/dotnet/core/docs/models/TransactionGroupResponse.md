# Revaly.Sdk.Core.Model.TransactionGroupResponse
Envelope returned by the V2 transaction-details lookups when `includeAllTransactions=true`. Contains the matched transaction plus every transaction belonging to the same payment — all attempts and lifecycle operations (capture, refund, void) that share the same initial transaction id. If the matched transaction has no initial transaction id, `transactions` contains only the matched record. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Transaction** | [**TransactionResponse**](TransactionResponse.md) | The transaction matching the supplied id (the record the non-expanded lookup returns). | [optional] 
**Transactions** | [**List&lt;TransactionResponse&gt;**](TransactionResponse.md) | Every transaction in the payment, ordered by transaction date ascending. Capped at 100. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

