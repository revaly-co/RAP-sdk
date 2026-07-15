
# PaymentMethodWriteResponse

Response after creating or modifying a payment method

## Properties

Name | Type
------------ | -------------
`transaction` | [PaymentMethodWriteResponseTransaction](PaymentMethodWriteResponseTransaction.md)
`paymentMethodId` | string
`creditCardNumber` | string
`expiryMonth` | string
`expiryYear` | string
`cvv` | string
`firstName` | string
`lastName` | string
`fullName` | string
`customerId` | string
`billingAddress` | [Address](Address.md)
`shippingAddress` | [Address](Address.md)
`email` | string
`phoneNumber` | string
`paymentMethodType` | string
`fingerprint` | string
`lastFourDigits` | string
`firstSixDigits` | string
`cardType` | string
`dateCreated` | Date
`storageState` | string
`bin` | string

## Example

```typescript
import type { PaymentMethodWriteResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "transaction": null,
  "paymentMethodId": 7DA6XQ33AIPUZLLDAGMXYHNTG4,
  "creditCardNumber": ************4242,
  "expiryMonth": 12,
  "expiryYear": 2025,
  "cvv": ***,
  "firstName": John,
  "lastName": Doe,
  "fullName": John Doe,
  "customerId": customer_123456,
  "billingAddress": null,
  "shippingAddress": null,
  "email": john.doe@example.com,
  "phoneNumber": +1-555-123-4567,
  "paymentMethodType": creditCard,
  "fingerprint": fp_abc123def456,
  "lastFourDigits": 4242,
  "firstSixDigits": 424242,
  "cardType": visa,
  "dateCreated": 2024-01-15T10:30Z,
  "storageState": stored,
  "bin": 424242,
} satisfies PaymentMethodWriteResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PaymentMethodWriteResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


