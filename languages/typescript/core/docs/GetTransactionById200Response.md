
# GetTransactionById200Response


## Properties

Name | Type
------------ | -------------
`transaction` | [TransactionResponse](TransactionResponse.md)
`transactions` | [Array&lt;TransactionResponse&gt;](TransactionResponse.md)
`transactionId` | string
`transactionDate` | Date
`transactionStatus` | number
`message` | string
`responseCode` | string
`transactionType` | string
`merchantTransactionId` | string
`customerId` | string
`gatewayRoutingId` | string
`currency` | string
`amount` | number
`gatewayType` | string
`gatewayTransactionId` | string
`acquirerAuthCode` | string
`inlineRetryPreviousTransactionId` | string
`inlineRetryPreviousMerchantTransactionId` | string
`isInlineRetry` | boolean
`retryDate` | Date
`mitStoredTransactionId` | string
`storedCredential` | [StoredCredentialResponse](StoredCredentialResponse.md)
`orderId` | string
`statementDescriptor` | string
`customerIp` | string
`engagedRecoveryState` | number
`description` | string
`gatewayFields` | { [key: string]: any; }
`gatewaySpecificResponseFields` | { [key: string]: any; }
`paymentPlanData` | [PaymentPlanData](PaymentPlanData.md)
`recovery` | [Recovery](Recovery.md)
`response` | [TransactionResponseDetails](TransactionResponseDetails.md)
`paymentMethod` | [PaymentMethodResponse](PaymentMethodResponse.md)

## Example

```typescript
import type { GetTransactionById200Response } from ''

// TODO: Update the object below with actual values
const example = {
  "transaction": null,
  "transactions": null,
  "transactionId": 06CQR5TMB800000G0011NCFRVY37A,
  "transactionDate": 2024-01-15T10:30Z,
  "transactionStatus": 1,
  "message": Transaction approved successfully,
  "responseCode": 00,
  "transactionType": Charge,
  "merchantTransactionId": order_12345,
  "customerId": cust_9876543210fedcba,
  "gatewayRoutingId": gateway_routing_id_abc123,
  "currency": USD,
  "amount": 2500,
  "gatewayType": stripe,
  "gatewayTransactionId": pi_1234567890abcdef,
  "acquirerAuthCode": AUTH1234,
  "inlineRetryPreviousTransactionId": txn_inline_123456,
  "inlineRetryPreviousMerchantTransactionId": merchant_txn_original,
  "isInlineRetry": true,
  "retryDate": 2024-01-16T10:30Z,
  "mitStoredTransactionId": mit_1234567890abcdef,
  "storedCredential": null,
  "orderId": order_67890,
  "statementDescriptor": ACME* SUBSCRIPTION,
  "customerIp": 192.168.1.100,
  "engagedRecoveryState": 0,
  "description": Payment for premium subscription,
  "gatewayFields": {processor_id=12345, network_transaction_id=abc123xyz789},
  "gatewaySpecificResponseFields": {gatewayCode=00, gatewayMessage=Approved},
  "paymentPlanData": null,
  "recovery": null,
  "response": null,
  "paymentMethod": null,
} satisfies GetTransactionById200Response

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GetTransactionById200Response
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


