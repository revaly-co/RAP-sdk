# Revaly.Sdk.Core.Model.StoredCredentialResponse
Stored credential information returned from the gateway for recurring, installment, or unscheduled transactions

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ReasonType** | **StoredCredentialReasonType** |  | [optional] 
**InitialNetworkTransactionId** | **string** | Network transaction ID from the initial transaction that established the stored credential, returned by the gateway | [optional] 
**LatestNetworkTransactionId** | **string** | Network transaction ID from the most recent transaction using this stored credential, returned by the gateway | [optional] 
**GatewayInitialTransactionId** | **string** | Gateway&#39;s own transaction ID from the initial transaction that established the stored credential | [optional] 
**GatewayLatestTransactionId** | **string** | Gateway&#39;s own transaction ID from the most recent transaction using this stored credential | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

