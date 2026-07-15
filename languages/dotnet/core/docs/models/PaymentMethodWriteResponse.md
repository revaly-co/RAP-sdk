# Revaly.Sdk.Core.Model.PaymentMethodWriteResponse
Response after creating or modifying a payment method

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Transaction** | [**PaymentMethodWriteResponseTransaction**](PaymentMethodWriteResponseTransaction.md) |  | [optional] 
**PaymentMethodId** | **string** | Unique identifier for the payment method | [optional] 
**CreditCardNumber** | **string** | Masked credit card number | [optional] 
**ExpiryMonth** | **string** | Expiration month | [optional] 
**ExpiryYear** | **string** | Expiration year | [optional] 
**Cvv** | **string** | Masked CVV | [optional] 
**FirstName** | **string** | Customer&#39;s first name | [optional] 
**LastName** | **string** | Customer&#39;s last name | [optional] 
**FullName** | **string** | Customer&#39;s full name | [optional] 
**CustomerId** | **string** | Customer identifier | [optional] 
**BillingAddress** | [**Address**](Address.md) |  | [optional] 
**ShippingAddress** | [**Address**](Address.md) |  | [optional] 
**Email** | **string** | Customer&#39;s email address | [optional] 
**PhoneNumber** | **string** | Customer&#39;s phone number | [optional] 
**PaymentMethodType** | **string** | Type of payment method | [optional] 
**Fingerprint** | **string** | Unique fingerprint for the payment method | [optional] 
**LastFourDigits** | **string** | Last four digits of the payment method | [optional] 
**FirstSixDigits** | **string** | First six digits (BIN) of the payment method | [optional] 
**CardType** | **string** | Type of credit card | [optional] 
**DateCreated** | **DateTime** | Date when the payment method was created | [optional] 
**StorageState** | **string** | Storage state of the payment method | [optional] 
**Bin** | **string** | Bank Identification Number. Must contain exactly 6 or 8 digits. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

