# Revaly.Sdk.Core.Model.CaptureRequest
Request to capture an authorized payment transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this capture transaction | 
**Amount** | **long** | Capture amount in smallest currency unit (e.g., cents for USD). If null or omitted, the full authorized amount will be captured.  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

