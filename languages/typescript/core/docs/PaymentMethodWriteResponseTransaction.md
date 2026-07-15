
# PaymentMethodWriteResponseTransaction

Associated transaction information

## Properties

Name | Type
------------ | -------------
`transactionId` | string
`transactionDate` | Date
`transactionStatus` | number
`message` | string
`responseCode` | string
`transactionType` | string

## Example

```typescript
import type { PaymentMethodWriteResponseTransaction } from ''

// TODO: Update the object below with actual values
const example = {
  "transactionId": 06CQR5TMB800000G0011NCFRVY37A,
  "transactionDate": 2024-01-15T10:30Z,
  "transactionStatus": 1,
  "message": Payment method created successfully,
  "responseCode": 00,
  "transactionType": create_payment_method,
} satisfies PaymentMethodWriteResponseTransaction

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PaymentMethodWriteResponseTransaction
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


