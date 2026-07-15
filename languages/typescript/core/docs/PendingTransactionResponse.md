
# PendingTransactionResponse

Pending payment intent. Returned by the merchant-transaction lookup when the platform has accepted a payment with this merchantTransactionId (the intent was durably recorded before gateway dispatch) but no transaction record is visible yet. Poll the same lookup again: it resolves to the full TransactionResponse once the transaction becomes visible. This shape is deliberately distinct from TransactionResponse — use the required `state` field as the discriminator.

## Properties

Name | Type
------------ | -------------
`state` | string
`merchantTransactionId` | string
`transactionType` | string
`receivedAt` | Date

## Example

```typescript
import type { PendingTransactionResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "state": pending,
  "merchantTransactionId": charge_order_12345,
  "transactionType": Charge,
  "receivedAt": 2026-07-13T18:30Z,
} satisfies PendingTransactionResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PendingTransactionResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


