
# TransactionGroupResponse

Envelope returned by the V2 transaction-details lookups when `includeAllTransactions=true`. Contains the matched transaction plus every transaction belonging to the same payment — all attempts and lifecycle operations (capture, refund, void) that share the same initial transaction id. If the matched transaction has no initial transaction id, `transactions` contains only the matched record. 

## Properties

Name | Type
------------ | -------------
`transaction` | [TransactionResponse](TransactionResponse.md)
`transactions` | [Array&lt;TransactionResponse&gt;](TransactionResponse.md)

## Example

```typescript
import type { TransactionGroupResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "transaction": null,
  "transactions": null,
} satisfies TransactionGroupResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionGroupResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


