
# RtnDataSellerData

Seller details for marketplace or platform transactions where the client submits on behalf of a third-party seller (maps to Amex seller_information). All fields optional; omit rather than send nulls.

## Properties

Name | Type
------------ | -------------
`sellerId` | string
`sellerBusinessName` | string
`sellerOwnerName` | string
`sellerTenure` | number
`sellerLatitude` | string
`sellerLongitude` | string
`sellerAddress` | string
`sellerPhone` | string
`sellerEmail` | string
`sellerPostalCode` | string
`sellerRegion` | string
`sellerCountryCode` | string
`transactionTypeIndicator` | string

## Example

```typescript
import type { RtnDataSellerData } from ''

// TODO: Update the object below with actual values
const example = {
  "sellerId": 1234567890,
  "sellerBusinessName": ACME Marketplace Vendor,
  "sellerOwnerName": Betty Smith,
  "sellerTenure": 36,
  "sellerLatitude": -1.5459487,
  "sellerLongitude": 52.2768309,
  "sellerAddress": 400 Maple Court,
  "sellerPhone": 5555552222,
  "sellerEmail": seller@example.com,
  "sellerPostalCode": 12345,
  "sellerRegion": USA,
  "sellerCountryCode": 840,
  "transactionTypeIndicator": P2M,
} satisfies RtnDataSellerData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataSellerData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


