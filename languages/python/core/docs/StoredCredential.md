# StoredCredential

Stored credential information for recurring, installment, or unscheduled transactions

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason_type** | [**StoredCredentialReasonType**](StoredCredentialReasonType.md) |  | [optional] 
**initial_network_transaction_id** | **str** | Network transaction ID from the initial transaction that established the stored credential | [optional] 
**latest_network_transaction_id** | **str** | Network transaction ID from the most recent transaction using this stored credential | [optional] 
**initial_gateway_transaction_id** | **str** | Gateway transaction ID from the initial transaction that established the stored credential | [optional] 
**latest_gateway_transaction_id** | **str** | Gateway transaction ID from the most recent transaction using this stored credential | [optional] 

## Example

```python
from revaly_sdk_core.models.stored_credential import StoredCredential

# TODO update the JSON string below
json = "{}"
# create an instance of StoredCredential from a JSON string
stored_credential_instance = StoredCredential.from_json(json)
# print the JSON string representation of the object
print(StoredCredential.to_json())

# convert the object into a dict
stored_credential_dict = stored_credential_instance.to_dict()
# create an instance of StoredCredential from a dict
stored_credential_from_dict = StoredCredential.from_dict(stored_credential_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


