
# PaymentMethod

Payment method details for either credit card or gatewayPaymentMethodId

## Properties

Name | Type
------------ | -------------
`firstName` | string
`lastName` | string
`fullName` | string
`email` | string
`merchantAccountReferenceId` | string
`paymentMethodId` | string
`issuerIdentificationNumber` | string
`billingAddress` | [Address](Address.md)
`shippingAddress` | [Address](Address.md)
`creditCard` | [CreditCard](CreditCard.md)
`gatewayPaymentMethod` | [GatewayPaymentMethod](GatewayPaymentMethod.md)
`vaultPaymentMethod` | [VaultPaymentMethod](VaultPaymentMethod.md)

## Example

```typescript
import type { PaymentMethod } from ''

// TODO: Update the object below with actual values
const example = {
  "firstName": John,
  "lastName": Doe,
  "fullName": John Doe,
  "email": john.doe@example.com,
  "merchantAccountReferenceId": acct_9876543210fedcba,
  "paymentMethodId": 7DA6XQ33AIPUZLLDAGMXYHNTG4,
  "issuerIdentificationNumber": 424242,
  "billingAddress": null,
  "shippingAddress": null,
  "creditCard": null,
  "gatewayPaymentMethod": null,
  "vaultPaymentMethod": null,
} satisfies PaymentMethod

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PaymentMethod
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


