

# RtnDataCustomerData

Customer account and profile signals. All fields optional.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**firstName** | **String** | Customer first name. |  [optional] |
|**lastName** | **String** | Customer last name. |  [optional] |
|**email** | **String** | Customer email address. |  [optional] |
|**homePhone** | **String** | Home phone number. Digits only, no formatting. |  [optional] |
|**mobilePhone** | **String** | Mobile phone number. Digits only, no formatting. |  [optional] |
|**workPhone** | **String** | Work phone number. Digits only, no formatting. |  [optional] |
|**accountOpenedDate** | **String** | Account creation date. Format YYYYMMDD. |  [optional] |
|**accountAgeIndicator** | [**AccountAgeIndicatorEnum**](#AccountAgeIndicatorEnum) | Account age token: 01 &#x3D; created during transaction, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. |  [optional] |
|**isFreeAccount** | **Boolean** | True if the customer account is a free (non-paying) account. |  [optional] |
|**accountLastChangedDate** | **String** | Last account modification date. Format YYYYMMDD. |  [optional] |
|**accountChangeIndicator** | [**AccountChangeIndicatorEnum**](#AccountChangeIndicatorEnum) | Account change age token: 01 &#x3D; during transaction, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. |  [optional] |
|**passwordLastChangedDate** | **String** | Last password change date. Format YYYYMMDD. |  [optional] |
|**passwordChangeIndicator** | [**PasswordChangeIndicatorEnum**](#PasswordChangeIndicatorEnum) | Password change age: 01 &#x3D; never reset, 02 &#x3D; during transaction, 03 &#x3D; &lt;30 days, 04 &#x3D; 30–60 days, 05 &#x3D; &gt;60 days. |  [optional] |
|**transactionSuccessfulCountLastSixMonths** | **Integer** | Count of successful purchases in the past 6 months. |  [optional] |
|**transactionAttemptedCountLast24Hours** | **Integer** | Count of transaction attempts in the past 24 hours. |  [optional] |
|**transactionAttemptedCountLastYear** | **Integer** | Count of transaction attempts in the past year. |  [optional] |
|**paymentMethodAddedDate** | **String** | Date payment method was added. Format YYYYMMDD. |  [optional] |
|**paymentMethodAgeIndicator** | [**PaymentMethodAgeIndicatorEnum**](#PaymentMethodAgeIndicatorEnum) | Payment method age token. |  [optional] |
|**paymentMethodAddAttemptCountLast24Hours** | **Integer** | Number of payment method add attempts in the past 24 hours. |  [optional] |
|**isPaymentMethodOnFile** | **Boolean** | True if the payment method is stored on file for the customer. |  [optional] |
|**isAccountSuspicious** | **Boolean** | True if the merchant considers the account suspicious. |  [optional] |
|**customerId** | **String** | Merchant&#39;s internal customer identifier. |  [optional] |
|**accountAuthenticationMethod** | [**AccountAuthenticationMethodEnum**](#AccountAuthenticationMethodEnum) | Method used to authenticate the customer for this session. |  [optional] |
|**isTenuredCustomer** | **Boolean** | True if the customer has a long-standing, established account relationship. |  [optional] |
|**isEmailKnownToCustomer** | **Boolean** | True if the email address on file is associated with a known customer account. |  [optional] |
|**isRegisteredCustomer** | [**IsRegisteredCustomerEnum**](#IsRegisteredCustomerEnum) | Whether the purchaser is a registered member (Y) or guest (N). |  [optional] |
|**isRegistrationUpdated** | [**IsRegistrationUpdatedEnum**](#IsRegistrationUpdatedEnum) | Whether any registration information changed since account creation. |  [optional] |
|**registeredAccountTenure** | **Integer** | Number of days the customer has been registered with the merchant. |  [optional] |
|**registeredName** | **String** | Customer name as registered with the merchant. |  [optional] |
|**registeredEmail** | **String** | Registered email address with the merchant. |  [optional] |
|**registeredPostalCode** | **String** | Registered postal code with the merchant. |  [optional] |
|**registeredAddress** | **String** | Registered address with the merchant (no city/state). |  [optional] |
|**registeredPhone** | **String** | Registered phone number. Digits only. |  [optional] |
|**daysSinceNameChange** | **Integer** | Days between the last registered-name change and the purchase date. |  [optional] |
|**daysSinceEmailChange** | **Integer** | Days between the last registered-email change and the purchase date. |  [optional] |
|**daysSincePasswordChange** | **Integer** | Days between the last password change and the purchase date. |  [optional] |
|**daysSincePostalCodeChange** | **Integer** | Days between the last registered-postal-code change and the purchase date. |  [optional] |
|**daysSinceAddressChange** | **Integer** | Days between the last registered-address change and the purchase date. |  [optional] |
|**daysSincePhoneChange** | **Integer** | Days between the last registered-phone change and the purchase date. |  [optional] |
|**daysSinceShipToNameChange** | **Integer** | Days between the last ship-to-name change and the purchase date. |  [optional] |
|**customerAni** | **String** | ANI 10-digit phone number used to place a phone order. Digits only. |  [optional] |
|**customerAniDigits** | **String** | ANI Information Identifier (II) digits: e.g. cellular &#x3D; 61–63, payphone &#x3D; 27, toll-free &#x3D; 24/25. |  [optional] |
|**isEmailAssociatedWithFraud** | **Boolean** | True if the email has been associated with confirmed/suspected fraud (distinct from isAccountSuspicious). Carrier for BofA emailAssociatedWithFraudFlag. |  [optional] |



## Enum: AccountAgeIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: AccountChangeIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: PasswordChangeIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| _05 | &quot;05&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: PaymentMethodAgeIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| _05 | &quot;05&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: AccountAuthenticationMethodEnum

| Name | Value |
|---- | -----|
| EMAIL_VERIFIED | &quot;EMAIL_VERIFIED&quot; |
| SMS_OTP | &quot;SMS_OTP&quot; |
| SSO | &quot;SSO&quot; |
| SOCIAL_LOGIN | &quot;SOCIAL_LOGIN&quot; |
| IDV | &quot;IDV&quot; |
| NONE | &quot;NONE&quot; |
| OTHER | &quot;OTHER&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: IsRegisteredCustomerEnum

| Name | Value |
|---- | -----|
| Y | &quot;Y&quot; |
| N | &quot;N&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: IsRegistrationUpdatedEnum

| Name | Value |
|---- | -----|
| Y | &quot;Y&quot; |
| N | &quot;N&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



