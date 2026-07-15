
# CreditCard

Credit card details for payment processing

## Properties

Name | Type
------------ | -------------
`number` | string
`cardVerificationCode` | string
`expiryMonth` | string
`expiryYear` | string
`company` | string
`cardType` | string

## Example

```typescript
import type { CreditCard } from ''

// TODO: Update the object below with actual values
const example = {
  "number": 4242424242424242,
  "cardVerificationCode": 123,
  "expiryMonth": 12,
  "expiryYear": 2025,
  "company": Visa,
  "cardType": visa,
} satisfies CreditCard

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as CreditCard
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


