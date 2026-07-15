
# NotifyData

Event-specific data for notification requests

## Properties

Name | Type
------------ | -------------
`transactionId` | string
`merchantTransactionId` | string
`orderID` | string
`customerId` | string
`amount` | number
`currency` | string
`customerAccountNumber` | string
`disableSmsNotification` | boolean
`disableEmailNotification` | boolean
`contactInformation` | [NotifyContactInformation](NotifyContactInformation.md)
`address` | [Address](Address.md)
`reasonCode` | string
`arn` | string
`disputeDate` | Date

## Example

```typescript
import type { NotifyData } from ''

// TODO: Update the object below with actual values
const example = {
  "transactionId": u4363a234567890abcdef,
  "merchantTransactionId": merch_txn_abc123,
  "orderID": order_456789,
  "customerId": customer_123,
  "amount": 2500,
  "currency": USD,
  "customerAccountNumber": ACC-001234,
  "disableSmsNotification": false,
  "disableEmailNotification": false,
  "contactInformation": null,
  "address": null,
  "reasonCode": 10.4,
  "arn": 74123456789012345678901,
  "disputeDate": 2026-07-01T00:00Z,
} satisfies NotifyData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as NotifyData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


