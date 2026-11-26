

# RtnData

Typed RTN fraud-signal payload (customer signals only). Transaction-core fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) and the RTN reporting keys and timing instants (merchantIdentifier, orderIdentifier, producerProcessStartedAt, producerRequestSentAt) are derived by Revaly at submission time and must not be sent. The full PAN (additionalTransactionData.fullPan) is optional and, if sent, is forwarded to RTN in-flight only. Every field is an optional signal, and no rtnData value ever refuses the payment that carries it. The lengths, formats and value lists below describe what the card issuers can use. A value outside them is accepted, and RTN trims, converts, shortens or leaves out that one value before it reaches an issuer. A value of the wrong JSON type (text where a number or a boolean is expected, for example) is left out the same way, and the rest of rtnData is still sent.

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



