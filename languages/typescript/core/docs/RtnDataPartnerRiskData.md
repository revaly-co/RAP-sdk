
# RtnDataPartnerRiskData

Risk scores and trust signals from the producer. All fields optional.

## Properties

Name | Type
------------ | -------------
`transactionRiskScore` | string
`isTrustedMidPartner` | boolean
`customerRiskScore` | string
`deviceRiskScore` | string
`ipRiskScore` | string
`merchantRiskScore` | string

## Example

```typescript
import type { RtnDataPartnerRiskData } from ''

// TODO: Update the object below with actual values
const example = {
  "transactionRiskScore": 12,
  "isTrustedMidPartner": false,
  "customerRiskScore": 5,
  "deviceRiskScore": 3,
  "ipRiskScore": 2,
  "merchantRiskScore": 44.6,
} satisfies RtnDataPartnerRiskData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataPartnerRiskData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


