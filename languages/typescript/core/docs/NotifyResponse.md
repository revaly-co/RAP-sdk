
# NotifyResponse

Response to a notification request indicating processing status

## Properties

Name | Type
------------ | -------------
`success` | boolean
`message` | string

## Example

```typescript
import type { NotifyResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "success": true,
  "message": Notification processed successfully,
} satisfies NotifyResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as NotifyResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


