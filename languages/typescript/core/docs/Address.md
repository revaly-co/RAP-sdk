
# Address

Address information for billing or shipping

## Properties

Name | Type
------------ | -------------
`address1` | string
`address2` | string
`city` | string
`state` | string
`zip` | string
`country` | string
`phoneNumber` | string

## Example

```typescript
import type { Address } from ''

// TODO: Update the object below with actual values
const example = {
  "address1": 123 Main St,
  "address2": Apt 4B,
  "city": New York,
  "state": NY,
  "zip": 10001,
  "country": US,
  "phoneNumber": +1-555-123-4567,
} satisfies Address

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as Address
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


