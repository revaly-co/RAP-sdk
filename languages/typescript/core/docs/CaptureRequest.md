
# CaptureRequest

Request to capture an authorized payment transaction

## Properties

Name | Type
------------ | -------------
`merchantTransactionId` | string
`amount` | number

## Example

```typescript
import type { CaptureRequest } from ''

// TODO: Update the object below with actual values
const example = {
  "merchantTransactionId": capture_order_12345,
  "amount": 1500,
} satisfies CaptureRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CaptureRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


