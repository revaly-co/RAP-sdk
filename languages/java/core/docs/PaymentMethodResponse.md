

# PaymentMethodResponse

Payment method information associated with a transaction

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**paymentMethodId** | **String** | Unique identifier for the payment method |  [optional] |
|**creditCardNumber** | **String** | Masked credit card number |  [optional] |
|**expiryMonth** | **String** | Credit card expiry month |  [optional] |
|**expiryYear** | **String** | Credit card expiry year |  [optional] |
|**cvv** | **String** | Masked card verification value |  [optional] |
|**firstName** | **String** | Cardholder&#39;s first name |  [optional] |
|**lastName** | **String** | Cardholder&#39;s last name |  [optional] |
|**fullName** | **String** | Cardholder&#39;s full name |  [optional] |
|**customerId** | **String** | Customer identifier |  [optional] |
|**billingAddress** | [**Address**](Address.md) |  |  [optional] |
|**shippingAddress** | [**Address**](Address.md) |  |  [optional] |
|**email** | **String** | Customer&#39;s email address |  [optional] |
|**phoneNumber** | **String** | Customer&#39;s phone number |  [optional] |
|**paymentMethodType** | **String** | Type of payment method |  [optional] |
|**fingerprint** | **String** | Unique fingerprint for the payment method |  [optional] |
|**lastFourDigits** | **String** | Last four digits of the payment method |  [optional] |
|**firstSixDigits** | **String** | First six digits of the payment method (BIN) |  [optional] |
|**cardType** | **String** | Type of credit card |  [optional] |
|**dateCreated** | **OffsetDateTime** | Date when the payment method was created |  [optional] |
|**storageState** | **String** | Storage state of the payment method |  [optional] |
|**bin** | **String** | Bank Identification Number. Must contain exactly 6 or 8 digits. |  [optional] |



