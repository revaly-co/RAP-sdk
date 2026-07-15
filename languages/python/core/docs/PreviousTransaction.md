# PreviousTransaction

Information about a previous transaction for reference

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_date** | **datetime** | Date of the previous transaction | [optional] 
**merchant_account_reference_id** | **str** | Merchant account reference ID from the previous transaction | [optional] 
**gateway_code** | **str** | Gateway response code from the previous transaction | [optional] 
**gateway_message** | **str** | Gateway response message from the previous transaction | [optional] 
**gateway_message_key** | **str** | Gateway message key from the previous transaction | [optional] 
**transaction_status** | **int** | Previous status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**avs_code** | **str** | AVS code from the previous transaction | [optional] 
**avs_message** | **str** | AVS message from the previous transaction | [optional] 
**cvv_code** | **str** | CVV code from the previous transaction | [optional] 
**cvv_message** | **str** | CVV message from the previous transaction | [optional] 

## Example

```python
from revaly_sdk_core.models.previous_transaction import PreviousTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of PreviousTransaction from a JSON string
previous_transaction_instance = PreviousTransaction.from_json(json)
# print the JSON string representation of the object
print(PreviousTransaction.to_json())

# convert the object into a dict
previous_transaction_dict = previous_transaction_instance.to_dict()
# create an instance of PreviousTransaction from a dict
previous_transaction_from_dict = PreviousTransaction.from_dict(previous_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


