

# RefundCancelRequest

Request to refund or cancel a payment transaction using merchant transaction ID

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**merchantTransactionId** | **String** | Merchant-provided unique identifier for this refund/cancel transaction |  |
|**amount** | **Long** | Refund amount in smallest currency unit (e.g., cents for USD). If null or omitted, a full refund will be processed.  |  [optional] |
|**customerId** | **String** | Unique identifier of the customer associated with this transaction |  |



