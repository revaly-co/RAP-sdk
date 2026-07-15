
# NotifyRequest

Notification request to inform Revaly of specific business events

## Properties

Name | Type
------------ | -------------
`eventType` | string
`data` | [NotifyData](NotifyData.md)

## Example

```typescript
import type { NotifyRequest } from ''

// TODO: Update the object below with actual values
const example = {
  "eventType": recordPayment,
  "data": null,
} satisfies NotifyRequest

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as NotifyRequest
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


