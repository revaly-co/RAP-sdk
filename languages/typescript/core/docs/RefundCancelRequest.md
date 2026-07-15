
# RefundCancelRequest

Request to refund or cancel a payment transaction using merchant transaction ID

## Properties

Name | Type
------------ | -------------
`merchantTransactionId` | string
`amount` | number
`customerId` | string

## Example

```typescript
import type { RefundCancelRequest } from ''

// TODO: Update the object below with actual values
const example = {
  "merchantTransactionId": refund_order_12345,
  "amount": 1000,
  "customerId": customer_12345,
} satisfies RefundCancelRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RefundCancelRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


