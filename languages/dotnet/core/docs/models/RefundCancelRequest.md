# Revaly.Sdk.Core.Model.RefundCancelRequest
Request to refund or cancel a payment transaction using merchant transaction ID

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**MerchantTransactionId** | **string** | Merchant-provided unique identifier for this refund/cancel transaction | 
**CustomerId** | **string** | Unique identifier of the customer associated with this transaction | 
**Amount** | **long** | Refund amount in smallest currency unit (e.g., cents for USD). If null or omitted, a full refund will be processed.  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

