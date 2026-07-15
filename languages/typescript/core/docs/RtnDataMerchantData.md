
# RtnDataMerchantData

Merchant identification and account signals. acquirerMerchantId is hard-required by RTN downstream but optional in this API.

## Properties

Name | Type
------------ | -------------
`acquirerMerchantId` | string
`issuerMerchantId` | string
`acquirerBin` | string
`acquirerReferenceNumber` | string
`merchantName` | string
`merchantAccountAgeIndicator` | string
`merchantAccountOpenedDate` | string
`isTenuredMerchant` | boolean

## Example

```typescript
import type { RtnDataMerchantData } from ''

// TODO: Update the object below with actual values
const example = {
  "acquirerMerchantId": mid_98451234,
  "issuerMerchantId": V1234567,
  "acquirerBin": 476134,
  "acquirerReferenceNumber": 745103921234,
  "merchantName": ACME Fitness Online,
  "merchantAccountAgeIndicator": 03,
  "merchantAccountOpenedDate": 20220601,
  "isTenuredMerchant": true,
} satisfies RtnDataMerchantData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataMerchantData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


