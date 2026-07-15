
# ThreeDS

3D Secure authentication data for payment processing

## Properties

Name | Type
------------ | -------------
`version` | string
`exemptionType` | string
`eci` | string
`cryptogram` | string
`dsTransactionId` | string
`acsTransactionId` | string
`xid` | string
`cavvAlgorithm` | string
`directoryStatus` | string
`authenticationStatus` | string
`enrolledStatus` | string
`serverTransId` | string

## Example

```typescript
import type { ThreeDS } from ''

// TODO: Update the object below with actual values
const example = {
  "version": 2.1.0,
  "exemptionType": low_value,
  "eci": 05,
  "cryptogram": AAABAWFlmQAAAABjRWWWAAAAAA==,
  "dsTransactionId": 550e8400-e29b-41d4-a716-446655440000,
  "acsTransactionId": 6ba7b810-9dad-11d1-80b4-00c04fd430c8,
  "xid": MDAwMDAwMDAwMDAwMDAwMzIyNzY=,
  "cavvAlgorithm": 1,
  "directoryStatus": Y,
  "authenticationStatus": Y,
  "enrolledStatus": Y,
  "serverTransId": 6ba7b811-9dad-11d1-80b4-00c04fd430c8,
} satisfies ThreeDS

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ThreeDS
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


