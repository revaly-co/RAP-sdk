

# StoredCredentialResponse

Stored credential information returned from the gateway for recurring, installment, or unscheduled transactions

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**reasonType** | **StoredCredentialReasonType** |  |  [optional] |
|**initialNetworkTransactionId** | **String** | Network transaction ID from the initial transaction that established the stored credential, returned by the gateway |  [optional] |
|**latestNetworkTransactionId** | **String** | Network transaction ID from the most recent transaction using this stored credential, returned by the gateway |  [optional] |
|**gatewayInitialTransactionId** | **String** | Gateway&#39;s own transaction ID from the initial transaction that established the stored credential |  [optional] |
|**gatewayLatestTransactionId** | **String** | Gateway&#39;s own transaction ID from the most recent transaction using this stored credential |  [optional] |



