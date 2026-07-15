

# PaymentMethodWriteResponse

Response after creating or modifying a payment method

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transaction** | [**PaymentMethodWriteResponseTransaction**](PaymentMethodWriteResponseTransaction.md) |  |  [optional] |
|**paymentMethodId** | **String** | Unique identifier for the payment method |  [optional] |
|**creditCardNumber** | **String** | Masked credit card number |  [optional] |
|**expiryMonth** | **String** | Expiration month |  [optional] |
|**expiryYear** | **String** | Expiration year |  [optional] |
|**cvv** | **String** | Masked CVV |  [optional] |
|**firstName** | **String** | Customer&#39;s first name |  [optional] |
|**lastName** | **String** | Customer&#39;s last name |  [optional] |
|**fullName** | **String** | Customer&#39;s full name |  [optional] |
|**customerId** | **String** | Customer identifier |  [optional] |
|**billingAddress** | [**Address**](Address.md) |  |  [optional] |
|**shippingAddress** | [**Address**](Address.md) |  |  [optional] |
|**email** | **String** | Customer&#39;s email address |  [optional] |
|**phoneNumber** | **String** | Customer&#39;s phone number |  [optional] |
|**paymentMethodType** | **String** | Type of payment method |  [optional] |
|**fingerprint** | **String** | Unique fingerprint for the payment method |  [optional] |
|**lastFourDigits** | **String** | Last four digits of the payment method |  [optional] |
|**firstSixDigits** | **String** | First six digits (BIN) of the payment method |  [optional] |
|**cardType** | **String** | Type of credit card |  [optional] |
|**dateCreated** | **OffsetDateTime** | Date when the payment method was created |  [optional] |
|**storageState** | **String** | Storage state of the payment method |  [optional] |
|**bin** | **String** | Bank Identification Number. Must contain exactly 6 or 8 digits. |  [optional] |



