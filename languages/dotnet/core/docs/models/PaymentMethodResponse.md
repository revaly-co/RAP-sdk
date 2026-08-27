# Revaly.Sdk.Core.Model.PaymentMethodResponse
Payment method information associated with a transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PaymentMethodId** | **string** | Unique identifier for the payment method | [optional] 
**CreditCardNumber** | **string** | Masked credit card number | [optional] 
**ExpiryMonth** | **string** | Credit card expiry month | [optional] 
**ExpiryYear** | **string** | Credit card expiry year | [optional] 
**Cvv** | **string** | Masked card verification value | [optional] 
**FirstName** | **string** | Cardholder&#39;s first name | [optional] 
**LastName** | **string** | Cardholder&#39;s last name | [optional] 
**FullName** | **string** | Cardholder&#39;s full name | [optional] 
**CustomerId** | **string** | Customer identifier | [optional] 
**BillingAddress** | [**Address**](Address.md) |  | [optional] 
**ShippingAddress** | [**Address**](Address.md) |  | [optional] 
**Email** | **string** | Customer&#39;s email address | [optional] 
**PhoneNumber** | **string** | Customer&#39;s phone number | [optional] 
**PaymentMethodType** | **string** | Type of payment method | [optional] 
**Fingerprint** | **string** | Unique fingerprint for the payment method | [optional] 
**LastFourDigits** | **string** | Last four digits of the payment method | [optional] 
**FirstSixDigits** | **string** | First six digits of the payment method (BIN) | [optional] 
**CardType** | **string** | Type of credit card | [optional] 
**DateCreated** | **DateTime** | Date when the payment method was created | [optional] 
**StorageState** | **string** | Storage state of the payment method | [optional] 
**Bin** | **string** | Bank Identification Number. Must contain exactly 6 or 8 digits. | [optional] 
**VaultToken** | **string** | Opaque reference to the stored card this payment method used, returned so a transaction can be tied back to its credential without a second lookup.  Present only on the payment method nested inside a **charge or authorize** response, and only when that transaction ran against a vault credential — either one you presented, or one this API created for you when it vaulted the card you sent. Always omitted on the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list): a stored payment method cannot be created from a vault token, so it never has one to report. Also omitted on every transaction read endpoint — the token is not persisted and is never replayed on a read.  Where the token can be resolved live, this is the token **currently live** for the credential, which is not always the token submitted — if the card was replaced by the Account Updater, the value is the new head of the lineage. Otherwise it is the token the transaction was dispatched with, and does not reflect a roll. Which of the two you get depends on how the transaction was processed, so treat it as optional throughout and do **not** treat a missing or unchanged value as proof the card was not rolled. This is the only place the token is reported — there is deliberately no copy at the transaction level. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

