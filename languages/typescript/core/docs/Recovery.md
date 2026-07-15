
# Recovery

Recovery settings and customer recovery information

## Properties

Name | Type
------------ | -------------
`disableCustomerRecovery` | boolean
`externalApproval` | boolean
`customerAccountNumber` | string
`customerBalance` | number
`disableSMSNotification` | boolean
`disableEmailNotification` | boolean
`retryCount` | number
`paymentReferenceData` | string
`dateFirstAttempt` | Date

## Example

```typescript
import type { Recovery } from ''

// TODO: Update the object below with actual values
const example = {
  "disableCustomerRecovery": false,
  "externalApproval": false,
  "customerAccountNumber": ACC123456,
  "customerBalance": 0,
  "disableSMSNotification": false,
  "disableEmailNotification": false,
  "retryCount": 0,
  "paymentReferenceData": ref_original_12345,
  "dateFirstAttempt": 2025-01-15T10:30Z,
} satisfies Recovery

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as Recovery
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


