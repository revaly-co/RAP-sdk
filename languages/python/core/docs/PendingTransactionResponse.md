# PendingTransactionResponse

Pending payment intent. Returned by the merchant-transaction lookup when the platform has accepted a payment with this merchantTransactionId (the intent was durably recorded before gateway dispatch) but no transaction record is visible yet. Poll the same lookup again: it resolves to the full TransactionResponse once the transaction becomes visible. This shape is deliberately distinct from TransactionResponse — use the required `state` field as the discriminator.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state** | **str** | Always &#x60;pending&#x60; — discriminates this shape from a completed transaction. | 
**merchant_transaction_id** | **str** | Merchant-provided transaction identifier the intent was recorded under | 
**transaction_type** | **str** | Operation the intent was recorded for — \&quot;Charge\&quot; or \&quot;Authorize\&quot; (same vocabulary as TransactionResponse.transactionType). | [optional] 
**received_at** | **datetime** | When the platform recorded the payment intent (ISO 8601) | [optional] 

## Example

```python
from revaly_sdk_core.models.pending_transaction_response import PendingTransactionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PendingTransactionResponse from a JSON string
pending_transaction_response_instance = PendingTransactionResponse.from_json(json)
# print the JSON string representation of the object
print(PendingTransactionResponse.to_json())

# convert the object into a dict
pending_transaction_response_dict = pending_transaction_response_instance.to_dict()
# create an instance of PendingTransactionResponse from a dict
pending_transaction_response_from_dict = PendingTransactionResponse.from_dict(pending_transaction_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


