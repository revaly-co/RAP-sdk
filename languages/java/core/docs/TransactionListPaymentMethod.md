

# TransactionListPaymentMethod

The payment method of a payment-method operation in the list transactions endpoint, as stored when the operation ran. It is flat: the billing address fields sit beside the shipping address fields, and the BIN is `issuerIdentificationNumber`. This is not the nested shape the payment-method endpoints return. A field with no value is omitted. 

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**paymentMethodId** | **String** | Payment method identifier |  [optional] |
|**creditCardNumber** | **String** | Masked card number; the full number is never returned |  [optional] |
|**expiryMonth** | **String** | Card expiry month as stored |  [optional] |
|**expiryYear** | **String** | Card expiry year as stored |  [optional] |
|**firstName** | **String** |  |  [optional] |
|**lastName** | **String** |  |  [optional] |
|**fullName** | **String** |  |  [optional] |
|**customerId** | **String** | Customer identifier of the operation |  [optional] |
|**address1** | **String** | Billing address, first line |  [optional] |
|**address2** | **String** | Billing address, second line |  [optional] |
|**city** | **String** | Billing address city |  [optional] |
|**state** | **String** | Billing address state or region |  [optional] |
|**postalCode** | **String** | Billing address postal code |  [optional] |
|**country** | **String** | Billing address country |  [optional] |
|**email** | **String** |  |  [optional] |
|**phoneNumber** | **String** |  |  [optional] |
|**shippingAddress1** | **String** | Shipping address, first line |  [optional] |
|**shippingAddress2** | **String** | Shipping address, second line |  [optional] |
|**shippingCity** | **String** |  |  [optional] |
|**shippingState** | **String** |  |  [optional] |
|**shippingPostalCode** | **String** |  |  [optional] |
|**shippingCountry** | **String** |  |  [optional] |
|**paymentMethodType** | **String** | Type of the payment method |  [optional] |
|**lastFourDigits** | **String** | Last four digits of the card number |  [optional] |
|**firstSixDigits** | **String** | First six digits of the card number |  [optional] |
|**cardType** | **String** | Card brand as reported for the card (for example VISA) |  [optional] |
|**dateCreated** | **String** | Date and time the payment method was created, as reported when the operation ran (ISO 8601). It may carry no UTC offset. |  [optional] |
|**storageState** | **String** | Storage state of the payment method |  [optional] |
|**issuerIdentificationNumber** | **String** | BIN of the card as reported when the operation ran |  [optional] |
|**merchantAccountReferenceId** | **String** | Merchant account reference identifier |  [optional] |



