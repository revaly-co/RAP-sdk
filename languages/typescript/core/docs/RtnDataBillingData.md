
# RtnDataBillingData

Cardholder billing address. All fields optional; omit rather than send nulls.

## Properties

Name | Type
------------ | -------------
`addressLine1` | string
`addressLine2` | string
`addressLine3` | string
`city` | string
`region` | string
`postalCode` | string
`country` | string

## Example

```typescript
import type { RtnDataBillingData } from ''

// TODO: Update the object below with actual values
const example = {
  "addressLine1": 1455 Rue Sainte-Catherine O,
  "addressLine2": Apt 1204,
  "addressLine3": Building B,
  "city": Montreal,
  "region": Quebec,
  "postalCode": H3G 1T1,
  "country": CA,
} satisfies RtnDataBillingData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataBillingData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


