
# RtnDataCustomerData

Customer account and profile signals. All fields optional.

## Properties

Name | Type
------------ | -------------
`firstName` | string
`lastName` | string
`email` | string
`homePhone` | string
`mobilePhone` | string
`workPhone` | string
`accountOpenedDate` | string
`accountAgeIndicator` | string
`isFreeAccount` | boolean
`accountLastChangedDate` | string
`accountChangeIndicator` | string
`passwordLastChangedDate` | string
`passwordChangeIndicator` | string
`transactionSuccessfulCountLastSixMonths` | number
`transactionAttemptedCountLast24Hours` | number
`transactionAttemptedCountLastYear` | number
`paymentMethodAddedDate` | string
`paymentMethodAgeIndicator` | string
`paymentMethodAddAttemptCountLast24Hours` | number
`isPaymentMethodOnFile` | boolean
`isAccountSuspicious` | boolean
`customerId` | string
`accountAuthenticationMethod` | string
`isTenuredCustomer` | boolean
`isEmailKnownToCustomer` | boolean
`isRegisteredCustomer` | string
`isRegistrationUpdated` | string
`registeredAccountTenure` | number
`registeredName` | string
`registeredEmail` | string
`registeredPostalCode` | string
`registeredAddress` | string
`registeredPhone` | string
`daysSinceNameChange` | number
`daysSinceEmailChange` | number
`daysSincePasswordChange` | number
`daysSincePostalCodeChange` | number
`daysSinceAddressChange` | number
`daysSincePhoneChange` | number
`daysSinceShipToNameChange` | number
`customerAni` | string
`customerAniDigits` | string
`isEmailAssociatedWithFraud` | boolean

## Example

```typescript
import type { RtnDataCustomerData } from ''

// TODO: Update the object below with actual values
const example = {
  "firstName": John,
  "lastName": Doe,
  "email": john.doe@example.com,
  "homePhone": 5145550100,
  "mobilePhone": 5145550199,
  "workPhone": 5145550123,
  "accountOpenedDate": 20240115,
  "accountAgeIndicator": 04,
  "isFreeAccount": false,
  "accountLastChangedDate": 20250101,
  "accountChangeIndicator": 04,
  "passwordLastChangedDate": 20250101,
  "passwordChangeIndicator": 01,
  "transactionSuccessfulCountLastSixMonths": 7,
  "transactionAttemptedCountLast24Hours": 1,
  "transactionAttemptedCountLastYear": 12,
  "paymentMethodAddedDate": 20240115,
  "paymentMethodAgeIndicator": 04,
  "paymentMethodAddAttemptCountLast24Hours": 0,
  "isPaymentMethodOnFile": true,
  "isAccountSuspicious": false,
  "customerId": cust_0294b7c1,
  "accountAuthenticationMethod": EMAIL_VERIFIED,
  "isTenuredCustomer": true,
  "isEmailKnownToCustomer": true,
  "isRegisteredCustomer": Y,
  "isRegistrationUpdated": N,
  "registeredAccountTenure": 720,
  "registeredName": Jane Smith,
  "registeredEmail": jane@example.com,
  "registeredPostalCode": 32121,
  "registeredAddress": 400 Maple Court,
  "registeredPhone": 5555551111,
  "daysSinceNameChange": 31,
  "daysSinceEmailChange": 31,
  "daysSincePasswordChange": 31,
  "daysSincePostalCodeChange": 31,
  "daysSinceAddressChange": 31,
  "daysSincePhoneChange": 31,
  "daysSinceShipToNameChange": 31,
  "customerAni": 5555551111,
  "customerAniDigits": 27,
  "isEmailAssociatedWithFraud": false,
} satisfies RtnDataCustomerData

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RtnDataCustomerData
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


