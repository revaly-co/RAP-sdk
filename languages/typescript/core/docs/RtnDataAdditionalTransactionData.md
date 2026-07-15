
# RtnDataAdditionalTransactionData

Core transaction signals supplied by the request producer. Transaction-routing fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) are derived by Revaly at submission time and must not be sent.

## Properties

Name | Type
------------ | -------------
`providerAuthDecision` | string
`providerAuthDecisionCode` | string
`paymentRail` | string
`posEntryMode` | string
`retrievalReferenceNumber` | string
`merchantTrustLevel` | string
`merchantTrustData` | string
`cardBrand` | string
`messageCategory` | string
`fullPan` | string
`dpan` | string

## Example

```typescript
import type { RtnDataAdditionalTransactionData } from ''

// TODO: Update the object below with actual values
const example = {
  "providerAuthDecision": APPROVE,
  "providerAuthDecisionCode": 00,
  "paymentRail": VISA,
  "posEntryMode": ECOMMERCE,
  "retrievalReferenceNumber": 123456789012,
  "merchantTrustLevel": TRUSTED,
  "merchantTrustData": tool=KOUNT;riskScore=12;program=TRUSTED_AUTH;version=1,
  "cardBrand": VISA,
  "messageCategory": 1,
  "fullPan": 4147202000001234,
  "dpan": 4761739001010010,
} satisfies RtnDataAdditionalTransactionData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataAdditionalTransactionData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


