
# TransactionResponseDetails

Detailed transaction processing response information from the payment gateway

## Properties

Name | Type
------------ | -------------
`avsCode` | string
`avsMessage` | string
`cvvCode` | string
`cvvMessage` | string
`errorCode` | string
`errorDetail` | string

## Example

```typescript
import type { TransactionResponseDetails } from ''

// TODO: Update the object below with actual values
const example = {
  "avsCode": Y,
  "avsMessage": Address verification successful,
  "cvvCode": M,
  "cvvMessage": CVV verification successful,
  "errorCode": DECLINED,
  "errorDetail": Insufficient funds available,
} satisfies TransactionResponseDetails

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionResponseDetails
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


