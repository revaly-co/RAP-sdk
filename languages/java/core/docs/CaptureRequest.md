

# CaptureRequest

Request to capture an authorized payment transaction

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**merchantTransactionId** | **String** | Merchant-provided unique identifier for this capture transaction |  |
|**amount** | **Long** | Capture amount in smallest currency unit (e.g., cents for USD). If null or omitted, the full authorized amount will be captured.  |  [optional] |



