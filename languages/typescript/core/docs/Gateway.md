
# Gateway

Gateway configuration and settings

## Properties

Name | Type
------------ | -------------
`name` | string
`bankTypeCode` | string
`merchantAccountReferenceId` | string
`gatewayType` | string
`currencyCode` | string
`acceptedCurrencyCodes` | Array&lt;string&gt;
`acceptedCards` | [AcceptedCards](AcceptedCards.md)
`acceptRetries` | boolean
`cvvRequired` | boolean
`approvedChargeOrCaptureRateFee` | number
`approvedChargeOrCaptureFlatFee` | number
`otherTransactionFlatFee` | number
`issueRefundsThroughCredit` | boolean

## Example

```typescript
import type { Gateway } from ''

// TODO: Update the object below with actual values
const example = {
  "name": Stripe Production,
  "bankTypeCode": VISA,
  "merchantAccountReferenceId": merch_acct_ref_123,
  "gatewayType": stripe,
  "currencyCode": USD,
  "acceptedCurrencyCodes": ["USD","EUR","GBP"],
  "acceptedCards": null,
  "acceptRetries": true,
  "cvvRequired": true,
  "approvedChargeOrCaptureRateFee": 0.029,
  "approvedChargeOrCaptureFlatFee": 0.3,
  "otherTransactionFlatFee": 0.15,
  "issueRefundsThroughCredit": true,
} satisfies Gateway

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as Gateway
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


