

# PreviousTransaction

Information about a previous transaction for reference

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transactionDate** | **OffsetDateTime** | Date of the previous transaction |  [optional] |
|**merchantAccountReferenceId** | **String** | Merchant account reference ID from the previous transaction |  [optional] |
|**gatewayCode** | **String** | Gateway response code from the previous transaction |  [optional] |
|**gatewayMessage** | **String** | Gateway response message from the previous transaction |  [optional] |
|**gatewayMessageKey** | **String** | Gateway message key from the previous transaction |  [optional] |
|**transactionStatus** | **Integer** | Previous status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) |  [optional] |
|**avsCode** | **String** | AVS code from the previous transaction |  [optional] |
|**avsMessage** | **String** | AVS message from the previous transaction |  [optional] |
|**cvvCode** | **String** | CVV code from the previous transaction |  [optional] |
|**cvvMessage** | **String** | CVV message from the previous transaction |  [optional] |



