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

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

