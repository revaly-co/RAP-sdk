
# RtnDataCustomData

Producer-reserved custom fields for metadata not covered by the canonical schema.

## Properties

Name | Type
------------ | -------------
`customField1` | string

## Example

```typescript
import type { RtnDataCustomData } from ''

// TODO: Update the object below with actual values
const example = {
  "customField1": campaignId=WINTER26;checkoutVariant=B,
} satisfies RtnDataCustomData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataCustomData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


