
# TransactionGateway

Gateway information associated with a transaction

## Properties

Name | Type
------------ | -------------
`token` | string
`gatewayType` | string
`name` | string
`referenceId` | string

## Example

```typescript
import type { TransactionGateway } from ''

// TODO: Update the object below with actual values
const example = {
  "token": QN6YIMMMJZREZIFGAGGUG6AYJA,
  "gatewayType": ,
  "name": Chase Paymentech Orbital - TESTFLEXPAY01,
  "referenceId": 0417560,
} satisfies TransactionGateway

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as TransactionGateway
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


