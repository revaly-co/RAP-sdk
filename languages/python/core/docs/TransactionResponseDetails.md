# TransactionResponseDetails

Detailed transaction processing response information from the payment gateway

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avs_code** | **str** | Address Verification System result code | [optional] 
**avs_message** | **str** | Address Verification System result message | [optional] 
**cvv_code** | **str** | Card Verification Value result code | [optional] 
**cvv_message** | **str** | Card Verification Value result message | [optional] 
**error_code** | **str** | Error code if transaction failed | [optional] 
**error_detail** | **str** | Detailed error message if transaction failed | [optional] 

## Example

```python
from revaly_sdk_core.models.transaction_response_details import TransactionResponseDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionResponseDetails from a JSON string
transaction_response_details_instance = TransactionResponseDetails.from_json(json)
# print the JSON string representation of the object
print(TransactionResponseDetails.to_json())

# convert the object into a dict
transaction_response_details_dict = transaction_response_details_instance.to_dict()
# create an instance of TransactionResponseDetails from a dict
transaction_response_details_from_dict = TransactionResponseDetails.from_dict(transaction_response_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


