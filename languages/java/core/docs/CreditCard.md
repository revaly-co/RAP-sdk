

# CreditCard

Credit card details for payment processing

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**number** | **String** | Credit card number (will be tokenized) |  |
|**cardVerificationCode** | **String** | Card verification code (CVV/CVC) |  [optional] |
|**expiryMonth** | **String** | Expiration month (01-12) |  |
|**expiryYear** | **String** | Expiration year (YYYY) |  |
|**company** | **String** | Card issuing company |  [optional] |
|**cardType** | [**CardTypeEnum**](#CardTypeEnum) | Type of credit card |  [optional] |



## Enum: CardTypeEnum

| Name | Value |
|---- | -----|
| VISA | &quot;visa&quot; |
| MASTERCARD | &quot;mastercard&quot; |
| AMEX | &quot;amex&quot; |
| DISCOVER | &quot;discover&quot; |
| JCB | &quot;jcb&quot; |
| DINERS | &quot;diners&quot; |
| UNKNOWN | &quot;unknown&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



