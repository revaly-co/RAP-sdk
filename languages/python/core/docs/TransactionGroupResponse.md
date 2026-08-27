# TransactionGroupResponse

Envelope returned by the V2 transaction-details lookups when `includeAllTransactions=true`. Contains the matched transaction plus every transaction belonging to the same payment — all attempts and lifecycle operations (capture, refund, void) that share the same initial transaction id. If the matched transaction has no initial transaction id, `transactions` contains only the matched record.  The required `transactions` member is always present and discriminates this envelope from a single `TransactionResponse`, which never carries a `transactions` member. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction** | [**TransactionResponse**](TransactionResponse.md) | The transaction matching the supplied id (the record the non-expanded lookup returns). | [optional] 
**transactions** | [**List[TransactionResponse]**](TransactionResponse.md) | Every transaction in the payment, ordered by transaction date ascending. Capped at 100. | 

## Example

```python
from revaly_sdk_core.models.transaction_group_response import TransactionGroupResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionGroupResponse from a JSON string
transaction_group_response_instance = TransactionGroupResponse.from_json(json)
# print the JSON string representation of the object
print(TransactionGroupResponse.to_json())

# convert the object into a dict
transaction_group_response_dict = transaction_group_response_instance.to_dict()
# create an instance of TransactionGroupResponse from a dict
transaction_group_response_from_dict = TransactionGroupResponse.from_dict(transaction_group_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


