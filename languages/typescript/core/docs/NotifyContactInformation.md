
# NotifyContactInformation

Contact information for customer notifications

## Properties

Name | Type
------------ | -------------
`firstName` | string
`lastName` | string
`phoneNumber` | string
`email` | string

## Example

```typescript
import type { NotifyContactInformation } from ''

// TODO: Update the object below with actual values
const example = {
  "firstName": John,
  "lastName": Doe,
  "phoneNumber": +1234567890,
  "email": john.doe@example.com,
} satisfies NotifyContactInformation

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as NotifyContactInformation
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


