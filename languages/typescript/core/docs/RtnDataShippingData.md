
# RtnDataShippingData

Shipping address and delivery signals. All fields optional.

## Properties

Name | Type
------------ | -------------
`shippingIndicator` | string
`addressLine1` | string
`addressLine2` | string
`addressLine3` | string
`city` | string
`region` | string
`postalCode` | string
`country` | string
`addressFirstUsedDate` | string
`addressFirstUsedIndicator` | string
`isShippingNameMatch` | boolean
`deliveryEmailAddress` | string
`deliveryTimeframeIndicator` | string
`shippingFirstName` | string
`shippingLastName` | string
`shippingPhone` | string
`shippingAddressCount` | number
`daysSinceShipToAddressChange` | number

## Example

```typescript
import type { RtnDataShippingData } from ''

// TODO: Update the object below with actual values
const example = {
  "shippingIndicator": 01,
  "addressLine1": 200 King St W,
  "addressLine2": Unit 18,
  "addressLine3": Suite 400,
  "city": Montreal,
  "region": Quebec,
  "postalCode": H3G 1T1,
  "country": CA,
  "addressFirstUsedDate": 20250601,
  "addressFirstUsedIndicator": 04,
  "isShippingNameMatch": true,
  "deliveryEmailAddress": deliveries@example.com,
  "deliveryTimeframeIndicator": 03,
  "shippingFirstName": Adam,
  "shippingLastName": Underhill,
  "shippingPhone": 5555552222,
  "shippingAddressCount": 2,
  "daysSinceShipToAddressChange": 31,
} satisfies RtnDataShippingData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataShippingData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


