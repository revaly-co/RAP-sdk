
# PreviousTransaction

Information about a previous transaction for reference

## Properties

Name | Type
------------ | -------------
`transactionDate` | Date
`merchantAccountReferenceId` | string
`gatewayCode` | string
`gatewayMessage` | string
`gatewayMessageKey` | string
`transactionStatus` | number
`avsCode` | string
`avsMessage` | string
`cvvCode` | string
`cvvMessage` | string

## Example

```typescript
import type { PreviousTransaction } from ''

// TODO: Update the object below with actual values
const example = {
  "transactionDate": 2024-01-14T15:30Z,
  "merchantAccountReferenceId": merch_acct_ref_123,
  "gatewayCode": 00,
  "gatewayMessage": Transaction approved,
  "gatewayMessageKey": APPROVED,
  "transactionStatus": 1,
  "avsCode": Y,
  "avsMessage": Address verification successful,
  "cvvCode": M,
  "cvvMessage": CVV verification successful,
} satisfies PreviousTransaction

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PreviousTransaction
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


