

# RtnDataAdditionalTransactionData

Core transaction signals supplied by the request producer. Transaction-routing fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) are derived by Revaly at submission time and must not be sent.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**providerAuthDecision** | [**ProviderAuthDecisionEnum**](#ProviderAuthDecisionEnum) | Authorization decision from the producer. Required for Trusted MID flows. |  [optional] |
|**providerAuthDecisionCode** | **String** | Provider-specific reason code for the auth decision. Required for Trusted MID flows. |  [optional] |
|**paymentRail** | [**PaymentRailEnum**](#PaymentRailEnum) | Payment routing rail. |  [optional] |
|**posEntryMode** | [**PosEntryModeEnum**](#PosEntryModeEnum) | Credential capture method at the point of sale. |  [optional] |
|**retrievalReferenceNumber** | **String** | Transaction retrieval reference number. |  [optional] |
|**merchantTrustLevel** | [**MerchantTrustLevelEnum**](#MerchantTrustLevelEnum) | Merchant trust classification assigned by the producer. |  [optional] |
|**merchantTrustData** | **String** | Producer metadata encoding the basis for the trust classification. |  [optional] |
|**cardBrand** | [**CardBrandEnum**](#CardBrandEnum) | Card product brand. |  [optional] |
|**messageCategory** | [**MessageCategoryEnum**](#MessageCategoryEnum) | Message type: 1 &#x3D; Pre-Auth Approved, 2 &#x3D; Pre-Auth Declined, 3 &#x3D; Pre-Auth Test. |  [optional] |
|**fullPan** | **String** | Full card Primary Account Number (cardholder data / CHD). Optional. Forwarded to RTN in-flight only — never persisted or logged at rest by RAP. Sending this field transmits cardholder data; ensure your integration is authorized under your PCI-DSS obligations. |  [optional] |
|**dpan** | **String** | Device Primary Account Number (tokenized card number from a digital wallet). |  [optional] |



## Enum: ProviderAuthDecisionEnum

| Name | Value |
|---- | -----|
| APPROVE | &quot;APPROVE&quot; |
| DECLINE | &quot;DECLINE&quot; |
| REVIEW | &quot;REVIEW&quot; |
| UNKNOWN | &quot;UNKNOWN&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: PaymentRailEnum

| Name | Value |
|---- | -----|
| VISA | &quot;VISA&quot; |
| MASTERCARD | &quot;MASTERCARD&quot; |
| AMEX | &quot;AMEX&quot; |
| DISCOVER | &quot;DISCOVER&quot; |
| STAR | &quot;STAR&quot; |
| PULSE | &quot;PULSE&quot; |
| NYCE | &quot;NYCE&quot; |
| INTERAC | &quot;INTERAC&quot; |
| ACCEL | &quot;ACCEL&quot; |
| MAESTRO | &quot;MAESTRO&quot; |
| OTHER | &quot;OTHER&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: PosEntryModeEnum

| Name | Value |
|---- | -----|
| KEYED | &quot;KEYED&quot; |
| MAGSTRIPE | &quot;MAGSTRIPE&quot; |
| CHIP | &quot;CHIP&quot; |
| CONTACTLESS | &quot;CONTACTLESS&quot; |
| ECOMMERCE | &quot;ECOMMERCE&quot; |
| FALLBACK_MAGSTRIPE | &quot;FALLBACK_MAGSTRIPE&quot; |
| OTHER | &quot;OTHER&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: MerchantTrustLevelEnum

| Name | Value |
|---- | -----|
| UNKNOWN | &quot;UNKNOWN&quot; |
| TRUSTED | &quot;TRUSTED&quot; |
| NOT_TRUSTED | &quot;NOT_TRUSTED&quot; |
| CONDITIONALLY_TRUSTED | &quot;CONDITIONALLY_TRUSTED&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: CardBrandEnum

| Name | Value |
|---- | -----|
| VISA | &quot;VISA&quot; |
| MASTERCARD | &quot;MASTERCARD&quot; |
| AMEX | &quot;AMEX&quot; |
| DISCOVER | &quot;DISCOVER&quot; |
| JCB | &quot;JCB&quot; |
| UNIONPAY | &quot;UNIONPAY&quot; |
| OTHER | &quot;OTHER&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: MessageCategoryEnum

| Name | Value |
|---- | -----|
| _1 | &quot;1&quot; |
| _2 | &quot;2&quot; |
| _3 | &quot;3&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



