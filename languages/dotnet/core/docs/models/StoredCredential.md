# Revaly.Sdk.Core.Model.StoredCredential
Stored credential information for recurring, installment, or unscheduled transactions

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ReasonType** | **StoredCredentialReasonType** |  | [optional] 
**InitialNetworkTransactionId** | **string** | Network transaction ID from the initial transaction that established the stored credential | [optional] 
**LatestNetworkTransactionId** | **string** | Network transaction ID from the most recent transaction using this stored credential | [optional] 
**InitialGatewayTransactionId** | **string** | Gateway transaction ID from the initial transaction that established the stored credential | [optional] 
**LatestGatewayTransactionId** | **string** | Gateway transaction ID from the most recent transaction using this stored credential | [optional] 
**TransactionLinkId** | **string** | Mastercard Transaction Link ID. Optional and accepted on every charge, but sent to the network only on connections Revaly has enabled for it, and only on merchant-initiated Mastercard charges. Send the value returned by the approved charge that set up the agreement, or, if the agreement was set up elsewhere, by the first approved charge after it. Never send a value from a declined response. Omit it and Revaly sends the value it keeps for the card, where it keeps one. Exactly 22 characters: letters, digits, hyphen and underscore. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

