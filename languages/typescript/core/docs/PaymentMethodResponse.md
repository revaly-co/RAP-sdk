
# PaymentMethodResponse

Payment method information associated with a transaction

## Properties

Name | Type
------------ | -------------
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
import type { PaymentMethodResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "paymentMethodId": 7DA6XQ33AIPUZLLDAGMXYHNTG4,
  "creditCardNumber": ****-****-****-4242,
  "expiryMonth": 12,
  "expiryYear": 2025,
  "cvv": ***,
  "firstName": John,
  "lastName": Doe,
  "fullName": John Doe,
  "customerId": cust_9876543210fedcba,
  "billingAddress": null,
  "shippingAddress": null,
  "email": john.doe@example.com,
  "phoneNumber": +1234567890,
  "paymentMethodType": creditCard,
  "fingerprint": abc123def456,
  "lastFourDigits": 4242,
  "firstSixDigits": 424242,
  "cardType": visa,
  "dateCreated": 2024-01-15T10:30Z,
  "storageState": stored,
  "bin": 424242,
} satisfies PaymentMethodResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PaymentMethodResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


