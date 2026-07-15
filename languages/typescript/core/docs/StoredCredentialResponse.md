
# StoredCredentialResponse

Stored credential information returned from the gateway for recurring, installment, or unscheduled transactions

## Properties

Name | Type
------------ | -------------
`reasonType` | [StoredCredentialReasonType](StoredCredentialReasonType.md)
`initialNetworkTransactionId` | string
`latestNetworkTransactionId` | string
`gatewayInitialTransactionId` | string
`gatewayLatestTransactionId` | string

## Example

```typescript
import type { StoredCredentialResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "reasonType": null,
  "initialNetworkTransactionId": 019078743540000,
  "latestNetworkTransactionId": 019078743540001,
  "gatewayInitialTransactionId": gw_initial_abc123,
  "gatewayLatestTransactionId": gw_latest_def456,
} satisfies StoredCredentialResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as StoredCredentialResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


