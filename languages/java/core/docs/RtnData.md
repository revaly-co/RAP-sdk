

# RtnData

Typed RTN 1.1 fraud-signal payload (customer signals only). Transaction-core fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) are derived by Revaly at submission time and must not be sent. The full PAN (additionalTransactionData.fullPan) is optional and, if sent, is forwarded to RTN in-flight only.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**additionalTransactionData** | [**RtnDataAdditionalTransactionData**](RtnDataAdditionalTransactionData.md) |  |  [optional] |
|**billingData** | [**RtnDataBillingData**](RtnDataBillingData.md) |  |  [optional] |
|**customData** | [**RtnDataCustomData**](RtnDataCustomData.md) |  |  [optional] |
|**customerData** | [**RtnDataCustomerData**](RtnDataCustomerData.md) |  |  [optional] |
|**deviceData** | [**RtnDataDeviceData**](RtnDataDeviceData.md) |  |  [optional] |
|**merchantData** | [**RtnDataMerchantData**](RtnDataMerchantData.md) |  |  [optional] |
|**orderData** | [**RtnDataOrderData**](RtnDataOrderData.md) |  |  [optional] |
|**partnerRiskData** | [**RtnDataPartnerRiskData**](RtnDataPartnerRiskData.md) |  |  [optional] |
|**shippingData** | [**RtnDataShippingData**](RtnDataShippingData.md) |  |  [optional] |
|**sellerData** | [**RtnDataSellerData**](RtnDataSellerData.md) |  |  [optional] |



