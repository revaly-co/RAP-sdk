# Revaly.Sdk.Core.Model.RtnData
Typed RTN 1.1 fraud-signal payload (customer signals only). Transaction-core fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) are derived by Revaly at submission time and must not be sent. The full PAN (additionalTransactionData.fullPan) is optional and, if sent, is forwarded to RTN in-flight only.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**AdditionalTransactionData** | [**RtnDataAdditionalTransactionData**](RtnDataAdditionalTransactionData.md) |  | [optional] 
**BillingData** | [**RtnDataBillingData**](RtnDataBillingData.md) |  | [optional] 
**CustomData** | [**RtnDataCustomData**](RtnDataCustomData.md) |  | [optional] 
**CustomerData** | [**RtnDataCustomerData**](RtnDataCustomerData.md) |  | [optional] 
**DeviceData** | [**RtnDataDeviceData**](RtnDataDeviceData.md) |  | [optional] 
**MerchantData** | [**RtnDataMerchantData**](RtnDataMerchantData.md) |  | [optional] 
**OrderData** | [**RtnDataOrderData**](RtnDataOrderData.md) |  | [optional] 
**PartnerRiskData** | [**RtnDataPartnerRiskData**](RtnDataPartnerRiskData.md) |  | [optional] 
**ShippingData** | [**RtnDataShippingData**](RtnDataShippingData.md) |  | [optional] 
**SellerData** | [**RtnDataSellerData**](RtnDataSellerData.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

