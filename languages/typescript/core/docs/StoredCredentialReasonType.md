
# StoredCredentialReasonType

Indicates the reason for using a stored credential: - **unscheduled**: An unscheduled transaction using stored credentials - **recurring**: A recurring payment using stored credentials - **installment**: An installment payment using stored credentials 

## Properties

Name | Type
------------ | -------------

## Example

```typescript
import type { StoredCredentialReasonType } from ''

// TODO: Update the object below with actual values
const example = {
} satisfies StoredCredentialReasonType

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as StoredCredentialReasonType
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


