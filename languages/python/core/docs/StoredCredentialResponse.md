# StoredCredentialResponse

Stored credential information returned from the gateway for recurring, installment, or unscheduled transactions

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason_type** | [**StoredCredentialReasonType**](StoredCredentialReasonType.md) |  | [optional] 
**initial_network_transaction_id** | **str** | Network transaction ID from the initial transaction that established the stored credential, returned by the gateway | [optional] 
**latest_network_transaction_id** | **str** | Network transaction ID from the most recent transaction using this stored credential, returned by the gateway | [optional] 
**gateway_initial_transaction_id** | **str** | Gateway&#39;s own transaction ID from the initial transaction that established the stored credential | [optional] 
**gateway_latest_transaction_id** | **str** | Gateway&#39;s own transaction ID from the most recent transaction using this stored credential | [optional] 

## Example

```python
from revaly_sdk_core.models.stored_credential_response import StoredCredentialResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StoredCredentialResponse from a JSON string
stored_credential_response_instance = StoredCredentialResponse.from_json(json)
# print the JSON string representation of the object
print(StoredCredentialResponse.to_json())

# convert the object into a dict
stored_credential_response_dict = stored_credential_response_instance.to_dict()
# create an instance of StoredCredentialResponse from a dict
stored_credential_response_from_dict = StoredCredentialResponse.from_dict(stored_credential_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


