

# CreatePaymentMethodRequest

Request to create a new payment method

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**paymentMethodType** | [**PaymentMethodTypeEnum**](#PaymentMethodTypeEnum) | Type of payment method to create: - **creditCard**: Use raw credit card details that will be tokenized - **gatewayPaymentMethodId**: Use an existing token from a supported payment gateway  |  |
|**customerId** | **String** | Unique identifier for the customer |  [optional] |
|**paymentMethod** | [**PaymentMethod**](PaymentMethod.md) |  |  [optional] |



## Enum: PaymentMethodTypeEnum

| Name | Value |
|---- | -----|
| CREDIT_CARD | &quot;creditCard&quot; |
| GATEWAY_PAYMENT_METHOD_ID | &quot;gatewayPaymentMethodId&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



