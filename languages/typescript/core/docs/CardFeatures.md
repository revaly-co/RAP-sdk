
# CardFeatures

Features and acceptance configuration for a specific card type

## Properties

Name | Type
------------ | -------------
`acceptCreditCard` | boolean
`acceptPrepaidCard` | boolean
`acceptDebitCard` | boolean

## Example

```typescript
import type { CardFeatures } from ''

// TODO: Update the object below with actual values
const example = {
  "acceptCreditCard": true,
  "acceptPrepaidCard": true,
  "acceptDebitCard": false,
} satisfies CardFeatures

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CardFeatures
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


