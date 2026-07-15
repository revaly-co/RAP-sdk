# StoredCredentialResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason_type** | [**\Revaly\Sdk\Core\Model\StoredCredentialReasonType**](StoredCredentialReasonType.md) |  | [optional]
**initial_network_transaction_id** | **string** | Network transaction ID from the initial transaction that established the stored credential, returned by the gateway | [optional]
**latest_network_transaction_id** | **string** | Network transaction ID from the most recent transaction using this stored credential, returned by the gateway | [optional]
**gateway_initial_transaction_id** | **string** | Gateway&#39;s own transaction ID from the initial transaction that established the stored credential | [optional]
**gateway_latest_transaction_id** | **string** | Gateway&#39;s own transaction ID from the most recent transaction using this stored credential | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
