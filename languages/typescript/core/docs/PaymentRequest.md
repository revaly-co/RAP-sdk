
# PaymentRequest

Request to process a payment (charge) transaction

## Properties

Name | Type
------------ | -------------
`paymentMethodType` | string
`amount` | number
`merchantTransactionId` | string
`gatewayRoutingId` | string
`currency` | string
`initiatedBy` | [InitiatedBy](InitiatedBy.md)
`mitStoredTransactionId` | string
`storedCredential` | [StoredCredential](StoredCredential.md)
`paymentMethod` | [PaymentMethod](PaymentMethod.md)
`orderId` | string
`storeOnSuccess` | boolean
`bypassPlatform` | boolean
`customerIp` | string
`customerId` | string
`gatewayFields` | { [key: string]: any; }
`rtnData` | [RtnData](RtnData.md)
`description` | string
`threeDS` | [ThreeDS](ThreeDS.md)
`paymentPlanData` | [PaymentPlanData](PaymentPlanData.md)
`recovery` | [Recovery](Recovery.md)
`previousTransaction` | [PreviousTransaction](PreviousTransaction.md)
`gateway` | [Gateway](Gateway.md)

## Example

```typescript
import type { PaymentRequest } from ''

// TODO: Update the object below with actual values
const example = {
  "paymentMethodType": creditCard,
  "amount": 2500,
  "merchantTransactionId": charge_order_12345,
  "gatewayRoutingId": gateway_routing_id_abc123,
  "currency": USD,
  "initiatedBy": null,
  "mitStoredTransactionId": mit_stored_transaction_001,
  "storedCredential": null,
  "paymentMethod": null,
  "orderId": order_67890,
  "storeOnSuccess": true,
  "bypassPlatform": false,
  "customerIp": 192.168.1.100,
  "customerId": customer_123456,
  "gatewayFields": {"processor_id":"12345","merchant_category_code":"5999"},
  "rtnData": null,
  "description": Payment for online purchase,
  "threeDS": null,
  "paymentPlanData": null,
  "recovery": null,
  "previousTransaction": null,
  "gateway": null,
} satisfies PaymentRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PaymentRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


