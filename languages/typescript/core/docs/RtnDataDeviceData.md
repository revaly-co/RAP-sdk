
# RtnDataDeviceData

Device and IP signals. All fields optional.

## Properties

Name | Type
------------ | -------------
`ipAddress` | string
`city` | string
`region` | string
`country` | string
`deviceId` | string
`isJavascriptEnabled` | boolean
`isJavaEnabled` | boolean
`userAgent` | string
`timezone` | string
`timezoneOffsetMinutes` | number
`browserLanguage` | string
`deviceLongitude` | string
`deviceLatitude` | string
`channel` | string
`digitalWalletProviderId` | string
`isDeviceFraudAssociated` | boolean
`isKnownDevice` | boolean
`deviceType` | string
`browserTimezoneOffset` | string
`sessionCookie` | string
`purchaseHostName` | string

## Example

```typescript
import type { RtnDataDeviceData } from ''

// TODO: Update the object below with actual values
const example = {
  "ipAddress": 203.0.113.42,
  "city": Montreal,
  "region": Quebec,
  "country": CA,
  "deviceId": dev_8f2c1a9b3d4e,
  "isJavascriptEnabled": true,
  "isJavaEnabled": false,
  "userAgent": Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36,
  "timezone": America/Montreal,
  "timezoneOffsetMinutes": -300,
  "browserLanguage": fr-CA,
  "deviceLongitude": -73.5673,
  "deviceLatitude": 45.5019,
  "channel": BROWSER,
  "digitalWalletProviderId": APPLE_PAY,
  "isDeviceFraudAssociated": false,
  "isKnownDevice": true,
  "deviceType": 03,
  "browserTimezoneOffset": -300,
  "sessionCookie": sess_8f2c1a9b,
  "purchaseHostName": checkout.example.com,
} satisfies RtnDataDeviceData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataDeviceData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


