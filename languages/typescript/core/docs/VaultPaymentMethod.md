
# VaultPaymentMethod

Vault-issued payment token details for payment processing

## Properties

Name | Type
------------ | -------------
`vaultToken` | string
`bin` | string
`lastFourDigits` | string
`expiryYear` | string
`expiryMonth` | string

## Example

```typescript
import type { VaultPaymentMethod } from ''

// TODO: Update the object below with actual values
const example = {
  "vaultToken": vt_01HX5J8QH8N1XK2D3T4B6Q7Z9C,
  "bin": 424242,
  "lastFourDigits": 4242,
  "expiryYear": 2025,
  "expiryMonth": 12,
} satisfies VaultPaymentMethod

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as VaultPaymentMethod
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


