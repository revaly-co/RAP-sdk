# Revaly.Sdk.Core.Model.RtnDataCustomerData
Customer account and profile signals. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**FirstName** | **string** | Customer first name. | [optional] 
**LastName** | **string** | Customer last name. | [optional] 
**Email** | **string** | Customer email address. | [optional] 
**HomePhone** | **string** | Home phone number. Digits only, no formatting. | [optional] 
**MobilePhone** | **string** | Mobile phone number. Digits only, no formatting. | [optional] 
**WorkPhone** | **string** | Work phone number. Digits only, no formatting. | [optional] 
**AccountOpenedDate** | **string** | Account creation date. Format YYYYMMDD. | [optional] 
**AccountAgeIndicator** | **string** | Account age token: 01 &#x3D; created during transaction, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**IsFreeAccount** | **bool** | True if the customer account is a free (non-paying) account. | [optional] 
**AccountLastChangedDate** | **string** | Last account modification date. Format YYYYMMDD. | [optional] 
**AccountChangeIndicator** | **string** | Account change age token: 01 &#x3D; during transaction, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**PasswordLastChangedDate** | **string** | Last password change date. Format YYYYMMDD. | [optional] 
**PasswordChangeIndicator** | **string** | Password change age: 01 &#x3D; never reset, 02 &#x3D; during transaction, 03 &#x3D; &lt;30 days, 04 &#x3D; 30–60 days, 05 &#x3D; &gt;60 days. | [optional] 
**TransactionSuccessfulCountLastSixMonths** | **int** | Count of successful purchases in the past 6 months. | [optional] 
**TransactionAttemptedCountLast24Hours** | **int** | Count of transaction attempts in the past 24 hours. | [optional] 
**TransactionAttemptedCountLastYear** | **int** | Count of transaction attempts in the past year. | [optional] 
**PaymentMethodAddedDate** | **string** | Date payment method was added. Format YYYYMMDD. | [optional] 
**PaymentMethodAgeIndicator** | **string** | Payment method age token. | [optional] 
**PaymentMethodAddAttemptCountLast24Hours** | **int** | Number of payment method add attempts in the past 24 hours. | [optional] 
**IsPaymentMethodOnFile** | **bool** | True if the payment method is stored on file for the customer. | [optional] 
**IsAccountSuspicious** | **bool** | True if the merchant considers the account suspicious. | [optional] 
**CustomerId** | **string** | Merchant&#39;s internal customer identifier. | [optional] 
**AccountAuthenticationMethod** | **string** | Method used to authenticate the customer for this session. | [optional] 
**IsTenuredCustomer** | **bool** | True if the customer has a long-standing, established account relationship. | [optional] 
**IsEmailKnownToCustomer** | **bool** | True if the email address on file is associated with a known customer account. | [optional] 
**IsRegisteredCustomer** | **string** | Whether the purchaser is a registered member (Y) or guest (N). | [optional] 
**IsRegistrationUpdated** | **string** | Whether any registration information changed since account creation. | [optional] 
**RegisteredAccountTenure** | **int** | Number of days the customer has been registered with the merchant. | [optional] 
**RegisteredName** | **string** | Customer name as registered with the merchant. | [optional] 
**RegisteredEmail** | **string** | Registered email address with the merchant. | [optional] 
**RegisteredPostalCode** | **string** | Registered postal code with the merchant. | [optional] 
**RegisteredAddress** | **string** | Registered address with the merchant (no city/state). | [optional] 
**RegisteredPhone** | **string** | Registered phone number. Digits only. | [optional] 
**DaysSinceNameChange** | **int** | Days between the last registered-name change and the purchase date. | [optional] 
**DaysSinceEmailChange** | **int** | Days between the last registered-email change and the purchase date. | [optional] 
**DaysSincePasswordChange** | **int** | Days between the last password change and the purchase date. | [optional] 
**DaysSincePostalCodeChange** | **int** | Days between the last registered-postal-code change and the purchase date. | [optional] 
**DaysSinceAddressChange** | **int** | Days between the last registered-address change and the purchase date. | [optional] 
**DaysSincePhoneChange** | **int** | Days between the last registered-phone change and the purchase date. | [optional] 
**DaysSinceShipToNameChange** | **int** | Days between the last ship-to-name change and the purchase date. | [optional] 
**CustomerAni** | **string** | ANI 10-digit phone number used to place a phone order. Digits only. | [optional] 
**CustomerAniDigits** | **string** | ANI Information Identifier (II) digits: e.g. cellular &#x3D; 61–63, payphone &#x3D; 27, toll-free &#x3D; 24/25. | [optional] 
**IsEmailAssociatedWithFraud** | **bool** | True if the email has been associated with confirmed/suspected fraud (distinct from isAccountSuspicious). Carrier for BofA emailAssociatedWithFraudFlag. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

