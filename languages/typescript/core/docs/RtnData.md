
# RtnData

Typed RTN 1.1 fraud-signal payload (customer signals only). Transaction-core fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) are derived by Revaly at submission time and must not be sent. The full PAN (additionalTransactionData.fullPan) is optional and, if sent, is forwarded to RTN in-flight only.

## Properties

Name | Type
------------ | -------------
`additionalTransactionData` | [RtnDataAdditionalTransactionData](RtnDataAdditionalTransactionData.md)
`billingData` | [RtnDataBillingData](RtnDataBillingData.md)
`customData` | [RtnDataCustomData](RtnDataCustomData.md)
`customerData` | [RtnDataCustomerData](RtnDataCustomerData.md)
`deviceData` | [RtnDataDeviceData](RtnDataDeviceData.md)
`merchantData` | [RtnDataMerchantData](RtnDataMerchantData.md)
`orderData` | [RtnDataOrderData](RtnDataOrderData.md)
`partnerRiskData` | [RtnDataPartnerRiskData](RtnDataPartnerRiskData.md)
`shippingData` | [RtnDataShippingData](RtnDataShippingData.md)
`sellerData` | [RtnDataSellerData](RtnDataSellerData.md)

## Example

```typescript
import type { RtnData } from ''

// TODO: Update the object below with actual values
const example = {
  "additionalTransactionData": null,
  "billingData": null,
  "customData": null,
  "customerData": null,
  "deviceData": null,
  "merchantData": null,
  "orderData": null,
  "partnerRiskData": null,
  "shippingData": null,
  "sellerData": null,
} satisfies RtnData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


