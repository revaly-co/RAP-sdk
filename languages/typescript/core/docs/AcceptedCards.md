
# AcceptedCards

Configuration for accepted card types and their features

## Properties

Name | Type
------------ | -------------
`visa` | [CardFeatures](CardFeatures.md)
`masterCard` | [CardFeatures](CardFeatures.md)
`amex` | [CardFeatures](CardFeatures.md)
`discover` | [CardFeatures](CardFeatures.md)
`dinersClub` | [CardFeatures](CardFeatures.md)
`jcb` | [CardFeatures](CardFeatures.md)
`maestro` | [CardFeatures](CardFeatures.md)

## Example

```typescript
import type { AcceptedCards } from ''

// TODO: Update the object below with actual values
const example = {
  "visa": null,
  "masterCard": null,
  "amex": null,
  "discover": null,
  "dinersClub": null,
  "jcb": null,
  "maestro": null,
} satisfies AcceptedCards

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AcceptedCards
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


