

# PaymentMethodWriteResponseTransaction

Associated transaction information

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transactionId** | **String** | Unique identifier for the transaction |  [optional] |
|**transactionDate** | **OffsetDateTime** | Date and time when the transaction was processed |  [optional] |
|**transactionStatus** | **Integer** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) |  [optional] |
|**message** | **String** | Human-readable message about the transaction |  [optional] |
|**responseCode** | **String** | Gateway response code |  [optional] |
|**transactionType** | **String** | Type of transaction |  [optional] |



