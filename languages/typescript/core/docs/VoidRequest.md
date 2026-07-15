
# VoidRequest

Request to void (cancel) a payment transaction

## Properties

Name | Type
------------ | -------------
`merchantTransactionId` | string

## Example

```typescript
import type { VoidRequest } from ''

// TODO: Update the object below with actual values
const example = {
  "merchantTransactionId": void_order_12345,
} satisfies VoidRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as VoidRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


