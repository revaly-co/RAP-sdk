
# PaymentPlanData

Payment plan and subscription information for recurring transactions

## Properties

Name | Type
------------ | -------------
`sku` | string
`category` | string
`billingPlan` | [BillingPlan](BillingPlan.md)
`subscriptionId` | string
`billingCycle` | number
`paymentModel` | string
`productDisplayName` | string

## Example

```typescript
import type { PaymentPlanData } from ''

// TODO: Update the object below with actual values
const example = {
  "sku": PREMIUM_MONTHLY,
  "category": subscription,
  "billingPlan": null,
  "subscriptionId": sub_1234567890,
  "billingCycle": 1,
  "paymentModel": recurring,
  "productDisplayName": Premium Monthly Plan,
} satisfies PaymentPlanData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as PaymentPlanData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


