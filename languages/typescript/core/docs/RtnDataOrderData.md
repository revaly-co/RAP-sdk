
# RtnDataOrderData

Order and purchase details. All fields optional.

## Properties

Name | Type
------------ | -------------
`purchaseDate` | Date
`itemCount` | number
`highestPriceItemPrice` | number
`highestPriceItemBrand` | string
`highestPriceItemCategory` | string
`isPreOrderPurchase` | boolean
`preOrderDate` | string
`isReorder` | boolean
`installmentPaymentCount` | number
`isRecurringPurchase` | boolean
`recurringIntervalDays` | number
`recurringEndDate` | string
`alternatePaymentIndicator` | string
`giftCardCount` | number
`giftCardAmount` | number
`giftCardCurrency` | string
`installmentPaymentData` | string
`topItemCategories` | string
`highestPriceItemSku` | string
`isCouponUsed` | string

## Example

```typescript
import type { RtnDataOrderData } from ''

// TODO: Update the object below with actual values
const example = {
  "purchaseDate": 2026-03-31T14:03:22.123Z,
  "itemCount": 2,
  "highestPriceItemPrice": 9999,
  "highestPriceItemBrand": Apple,
  "highestPriceItemCategory": Electronics,
  "isPreOrderPurchase": false,
  "preOrderDate": 20261201,
  "isReorder": false,
  "installmentPaymentCount": 3,
  "isRecurringPurchase": false,
  "recurringIntervalDays": 30,
  "recurringEndDate": 20271231,
  "alternatePaymentIndicator": 01,
  "giftCardCount": 0,
  "giftCardAmount": 5000,
  "giftCardCurrency": 840,
  "installmentPaymentData": 3,
  "topItemCategories": 10002000300040005,
  "highestPriceItemSku": TKDC315U,
  "isCouponUsed": N,
} satisfies RtnDataOrderData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataOrderData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


