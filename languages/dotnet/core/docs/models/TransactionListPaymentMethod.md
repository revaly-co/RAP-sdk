# Revaly.Sdk.Core.Model.TransactionListPaymentMethod
The payment method of a payment-method operation in the list transactions endpoint, as stored when the operation ran. It is flat: the billing address fields sit beside the shipping address fields, and the BIN is `issuerIdentificationNumber`. This is not the nested shape the payment-method endpoints return. A field with no value is omitted. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PaymentMethodId** | **string** | Payment method identifier | [optional] 
**CreditCardNumber** | **string** | Masked card number; the full number is never returned | [optional] 
**ExpiryMonth** | **string** | Card expiry month as stored | [optional] 
**ExpiryYear** | **string** | Card expiry year as stored | [optional] 
**FirstName** | **string** |  | [optional] 
**LastName** | **string** |  | [optional] 
**FullName** | **string** |  | [optional] 
**CustomerId** | **string** | Customer identifier of the operation | [optional] 
**Address1** | **string** | Billing address, first line | [optional] 
**Address2** | **string** | Billing address, second line | [optional] 
**City** | **string** | Billing address city | [optional] 
**State** | **string** | Billing address state or region | [optional] 
**PostalCode** | **string** | Billing address postal code | [optional] 
**Country** | **string** | Billing address country | [optional] 
**Email** | **string** |  | [optional] 
**PhoneNumber** | **string** |  | [optional] 
**ShippingAddress1** | **string** | Shipping address, first line | [optional] 
**ShippingAddress2** | **string** | Shipping address, second line | [optional] 
**ShippingCity** | **string** |  | [optional] 
**ShippingState** | **string** |  | [optional] 
**ShippingPostalCode** | **string** |  | [optional] 
**ShippingCountry** | **string** |  | [optional] 
**PaymentMethodType** | **string** | Type of the payment method | [optional] 
**LastFourDigits** | **string** | Last four digits of the card number | [optional] 
**FirstSixDigits** | **string** | First six digits of the card number | [optional] 
**CardType** | **string** | Card brand as reported for the card (for example VISA) | [optional] 
**DateCreated** | **string** | Date and time the payment method was created, as reported when the operation ran (ISO 8601). It may carry no UTC offset. | [optional] 
**StorageState** | **string** | Storage state of the payment method | [optional] 
**IssuerIdentificationNumber** | **string** | BIN of the card as reported when the operation ran | [optional] 
**MerchantAccountReferenceId** | **string** | Merchant account reference identifier | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

