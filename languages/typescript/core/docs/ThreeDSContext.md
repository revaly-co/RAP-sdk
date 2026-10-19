
# ThreeDSContext

Shopper device and browser context (RFC-068). Optional. Values are passed through unchanged to the payment gateway layer, which uses only what the routed gateway supports. Sending this block never changes the authorization. Backbone does not store the block; the only part it records is the channel, reduced to one of BROWSER, MOBILE_APP, SDK, POS or OTHER (any other value is recorded as OTHER), on the transaction\'s 3DS context usage treatment record.

## Properties

Name | Type
------------ | -------------
`channel` | string
`userAgent` | string
`acceptHeader` | string
`browserLanguage` | string
`colorDepth` | number
`screenHeight` | number
`screenWidth` | number
`timezoneOffsetMinutes` | number
`isJavaEnabled` | boolean
`isJavascriptEnabled` | boolean
`deviceId` | string
`deviceFingerprint` | string

## Example

```typescript
import type { ThreeDSContext } from ''

// TODO: Update the object below with actual values
const example = {
  "channel": BROWSER,
  "userAgent": Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36,
  "acceptHeader": text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,
  "browserLanguage": en-US,
  "colorDepth": 24,
  "screenHeight": 1080,
  "screenWidth": 1920,
  "timezoneOffsetMinutes": -300,
  "isJavaEnabled": false,
  "isJavascriptEnabled": true,
  "deviceId": device-7f3c2a,
  "deviceFingerprint": fp_9d1e4b0e,
} satisfies ThreeDSContext

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ThreeDSContext
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


