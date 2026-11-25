

# TransactionListPaymentMethodItemTransaction


## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transactionId** | **String** | Unique transaction identifier |  |
|**transactionDate** | **OffsetDateTime** | Date and time when the operation was processed (ISO 8601, UTC) |  |
|**transactionStatus** | **Integer** | Status of the operation (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) |  |
|**message** | **String** | Human-readable message about the result |  [optional] |
|**customerId** | **String** | Customer identifier associated with the operation |  [optional] |
|**responseCode** | **String** | Response code from the processing result |  [optional] |
|**transactionType** | **String** | The payment-method operation: CreateCreditCard, CreateGatewayPaymentMethod, UpdatePaymentMethod, RedactPaymentMethod or RecachePaymentMethod |  [optional] |
|**paymentMethod** | [**TransactionListPaymentMethod**](TransactionListPaymentMethod.md) |  |  [optional] |



