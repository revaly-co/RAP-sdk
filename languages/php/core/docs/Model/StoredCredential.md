# StoredCredential

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reason_type** | [**\Revaly\Sdk\Core\Model\StoredCredentialReasonType**](StoredCredentialReasonType.md) |  | [optional]
**initial_network_transaction_id** | **string** | Network transaction ID from the initial transaction that established the stored credential | [optional]
**latest_network_transaction_id** | **string** | Network transaction ID from the most recent transaction using this stored credential | [optional]
**initial_gateway_transaction_id** | **string** | Gateway transaction ID from the initial transaction that established the stored credential | [optional]
**latest_gateway_transaction_id** | **string** | Gateway transaction ID from the most recent transaction using this stored credential | [optional]
**transaction_link_id** | **string** | Mastercard Transaction Link ID. Optional and accepted on every charge, but sent to the network only on connections Revaly has enabled for it, and only on merchant-initiated Mastercard charges. Send the value returned by the approved charge that set up the agreement, or, if the agreement was set up elsewhere, by the first approved charge after it. Never send a value from a declined response. Omit it and Revaly sends the value it keeps for the card, where it keeps one. Exactly 22 characters: letters, digits, hyphen and underscore. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
