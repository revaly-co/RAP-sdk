
# TransactionListPaymentMethod

The payment method of a payment-method operation in the list transactions endpoint, as stored when the operation ran. It is flat: the billing address fields sit beside the shipping address fields, and the BIN is `issuerIdentificationNumber`. This is not the nested shape the payment-method endpoints return. A field with no value is omitted. 

## Properties

Name | Type
------------ | -------------
`paymentMethodId` | string
`creditCardNumber` | string
`expiryMonth` | string
`expiryYear` | string
`firstName` | string
`lastName` | string
`fullName` | string
`customerId` | string
`address1` | string
`address2` | string
`city` | string
`state` | string
`postalCode` | string
`country` | string
`email` | string
`phoneNumber` | string
`shippingAddress1` | string
`shippingAddress2` | string
`shippingCity` | string
`shippingState` | string
`shippingPostalCode` | string
`shippingCountry` | string
`paymentMethodType` | string
`lastFourDigits` | string
`firstSixDigits` | string
`cardType` | string
`dateCreated` | string
`storageState` | string
`issuerIdentificationNumber` | string
`merchantAccountReferenceId` | string

## Example

```typescript
import type { TransactionListPaymentMethod } from ''

// TODO: Update the object below with actual values
const example = {
  "paymentMethodId": WMJZ363LQLVUZEPZAGNN7BOYSA,
  "creditCardNumber": ************1111,
  "expiryMonth": 12,
  "expiryYear": 2030,
  "firstName": Jane,
  "lastName": Doe,
  "fullName": Jane Doe,
  "customerId": 24530178,
  "address1": 1 Main St,
  "address2": null,
  "city": Austin,
  "state": TX,
  "postalCode": 78701,
  "country": US,
  "email": jane.doe@example.com,
  "phoneNumber": 5125550100,
  "shippingAddress1": null,
  "shippingAddress2": null,
  "shippingCity": null,
  "shippingState": null,
  "shippingPostalCode": null,
  "shippingCountry": null,
  "paymentMethodType": CreditCard,
  "lastFourDigits": 1111,
  "firstSixDigits": 411111,
  "cardType": VISA,
  "dateCreated": 2025-12-02T14:44:42,
  "storageState": Cached,
  "issuerIdentificationNumber": 41111111,
  "merchantAccountReferenceId": 0417560,
} satisfies TransactionListPaymentMethod

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionListPaymentMethod
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


