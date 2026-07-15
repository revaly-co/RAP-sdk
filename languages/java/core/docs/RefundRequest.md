

# RefundRequest

Request to refund a payment transaction

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**merchantTransactionId** | **String** | Merchant-provided unique identifier for this refund transaction |  |
|**amount** | **Long** | Refund amount in smallest currency unit (e.g., cents for USD). If null or omitted, a full refund will be processed.  |  [optional] |



