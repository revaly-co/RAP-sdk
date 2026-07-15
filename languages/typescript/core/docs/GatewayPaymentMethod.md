
# GatewayPaymentMethod

GatewayPaymentMethodId details for payment processing

## Properties

Name | Type
------------ | -------------
`gatewayPaymentMethodId` | string
`bin` | string
`lastFourDigits` | string
`expiryYear` | string
`expiryMonth` | string

## Example

```typescript
import type { GatewayPaymentMethod } from ''

// TODO: Update the object below with actual values
const example = {
  "gatewayPaymentMethodId": tok_1234567890abcdef,
  "bin": 424242,
  "lastFourDigits": 4242,
  "expiryYear": 2025,
  "expiryMonth": 12,
} satisfies GatewayPaymentMethod

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as GatewayPaymentMethod
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


