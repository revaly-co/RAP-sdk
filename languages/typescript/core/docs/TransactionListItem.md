
# TransactionListItem

Transaction item returned from the list transactions endpoint. In simplified mode, only a subset of fields is returned (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). In detailed mode, additional fields are returned (excludes customVariable1-5 and initialTransactionId). 

## Properties

Name | Type
------------ | -------------
`transactionId` | string
`transactionDate` | Date
`transactionStatus` | number
`responseCode` | string
`message` | string
`transactionType` | string
`retryDate` | Date
`amount` | number
`initialMerchantTransactionId` | string
`storageState` | string
`completionStatus` | string
`gatewaySpecificResponseFields` | { [key: string]: any; }
`gatewaySpecificFields` | { [key: string]: any; }
`acquirerAuthCode` | string
`gatewayTransactionId` | string
`gatewayPaymentMethodId` | string
`engagedRecoveryState` | number
`currencyCode` | string
`merchantTransactionId` | string
`merchantAccountReferenceId` | string
`customerId` | string
`orderId` | string
`statementDescriptor` | string
`paymentMethodId` | string
`paymentMethodStorageState` | string
`paymentMethodType` | string
`paymentMethodMerchantAccountReferenceId` | string
`errorCode` | string
`errorDetail` | string
`avsCode` | string
`gateway` | [TransactionGateway](TransactionGateway.md)
`paymentMethod` | [PaymentMethodResponse](PaymentMethodResponse.md)

## Example

```typescript
import type { TransactionListItem } from ''

// TODO: Update the object below with actual values
const example = {
  "transactionId": 06DDZ1ERC400002A0824GSJZHYWYA,
  "transactionDate": 2025-12-02T14:44:42.209Z,
  "transactionStatus": 1,
  "responseCode": 10000,
  "message": Approved.,
  "transactionType": Charge,
  "retryDate": null,
  "amount": 100,
  "initialMerchantTransactionId": dac0680e-87fd-4416-a8ee-019adf85d861,
  "storageState": null,
  "completionStatus": RecoverySuccessful,
  "gatewaySpecificResponseFields": {"chase_payment_tech":{"HostRespCode":"100","HostAVSRespCode":"I3","MITReceivedTransactionID":null,"trace_number":null,"proc_status":"0"}},
  "gatewaySpecificFields": {"chase_payment_tech":{"mit_msg_type":"CREC"}},
  "acquirerAuthCode": tst408,
  "gatewayTransactionId": 692EFB5B097CCCD300000FFB0000F00C41565301,
  "gatewayPaymentMethodId": 297909967,
  "engagedRecoveryState": 0,
  "currencyCode": USD,
  "merchantTransactionId": dac0680e-87fd-4416-a8ee-019adf85d861,
  "merchantAccountReferenceId": 0417560,
  "customerId": 24530178,
  "orderId": ABC123-000519,
  "statementDescriptor": ACME* SUBSCRIPTION,
  "paymentMethodId": WMJZ363LQLVUZEPZAGNN7BOYSA,
  "paymentMethodStorageState": Cached,
  "paymentMethodType": GatewayPaymentMethodId,
  "paymentMethodMerchantAccountReferenceId": 0417560,
  "errorCode": 00,
  "errorDetail": Approved,
  "avsCode": Y,
  "gateway": null,
  "paymentMethod": null,
} satisfies TransactionListItem

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionListItem
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


