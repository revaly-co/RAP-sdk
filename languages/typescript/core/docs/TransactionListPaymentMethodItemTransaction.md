
# TransactionListPaymentMethodItemTransaction


## Properties

Name | Type
------------ | -------------
`transactionId` | string
`transactionDate` | Date
`transactionStatus` | number
`message` | string
`customerId` | string
`responseCode` | string
`transactionType` | string
`paymentMethod` | [TransactionListPaymentMethod](TransactionListPaymentMethod.md)

## Example

```typescript
import type { TransactionListPaymentMethodItemTransaction } from ''

// TODO: Update the object below with actual values
const example = {
  "transactionId": 06DDZ1ERC400002A0824GSJZHYWYA,
  "transactionDate": 2025-12-02T14:44:42.209Z,
  "transactionStatus": 1,
  "message": Succeeded!,
  "customerId": 24530178,
  "responseCode": 10000,
  "transactionType": CreateCreditCard,
  "paymentMethod": null,
} satisfies TransactionListPaymentMethodItemTransaction

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionListPaymentMethodItemTransaction
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


