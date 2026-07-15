
# InitiatedBy

Indicates who initiated the payment transaction: - **MIT**: Merchant-Initiated Transaction - Transaction initiated by the merchant without customer involvement - **CIT**: Customer-Initiated Transaction - Transaction initiated by the customer 

## Properties

Name | Type
------------ | -------------

## Example

```typescript
import type { InitiatedBy } from ''

// TODO: Update the object below with actual values
const example = {
} satisfies InitiatedBy

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as InitiatedBy
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


