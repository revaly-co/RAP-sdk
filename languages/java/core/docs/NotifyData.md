

# NotifyData

Event-specific data for notification requests

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transactionId** | **String** | Revaly transaction identifier |  [optional] |
|**merchantTransactionId** | **String** | Merchant&#39;s transaction identifier |  [optional] |
|**orderID** | **String** | Order identifier associated with the transaction |  [optional] |
|**customerId** | **String** | Customer identifier |  [optional] |
|**amount** | **Integer** | Transaction amount in smallest currency unit (e.g., cents for USD) |  [optional] |
|**currency** | **String** | Three-letter ISO currency code |  [optional] |
|**customerAccountNumber** | **String** | Customer account number for recovery purposes |  [optional] |
|**disableSmsNotification** | **Boolean** | Whether to disable SMS notifications for this customer |  [optional] |
|**disableEmailNotification** | **Boolean** | Whether to disable email notifications for this customer |  [optional] |
|**contactInformation** | [**NotifyContactInformation**](NotifyContactInformation.md) |  |  [optional] |
|**address** | [**Address**](Address.md) |  |  [optional] |
|**reasonCode** | **String** | Network chargeback reason code (e.g. Visa \&quot;10.4\&quot;). Chargeback-only, optional. |  [optional] |
|**arn** | **String** | Acquirer Reference Number or network case ID for the dispute. Chargeback-only, optional. |  [optional] |
|**disputeDate** | **OffsetDateTime** | When the dispute was raised. Chargeback-only, optional. |  [optional] |



