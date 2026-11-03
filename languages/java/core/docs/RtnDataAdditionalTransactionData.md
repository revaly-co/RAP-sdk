

# RtnDataAdditionalTransactionData

Core transaction signals supplied by the request producer. Transaction-routing fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) and the RTN reporting keys and timing instants (merchantIdentifier, orderIdentifier, producerProcessStartedAt, producerRequestSentAt) are derived by Revaly at submission time and must not be sent.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**providerAuthDecision** | [**ProviderAuthDecisionEnum**](#ProviderAuthDecisionEnum) | Authorization decision from the producer. Required for Trusted MID flows. |  [optional] |
|**providerAuthDecisionCode** | **String** | Provider-specific reason code for the auth decision. Required for Trusted MID flows. |  [optional] |
|**paymentRail** | [**PaymentRailEnum**](#PaymentRailEnum) | Payment routing rail. |  [optional] |
|**posEntryMode** | [**PosEntryModeEnum**](#PosEntryModeEnum) | Credential capture method at the point of sale. |  [optional] |
|**retrievalReferenceNumber** | **String** | Transaction retrieval reference number. |  [optional] |
|**merchantTrustLevel** | [**MerchantTrustLevelEnum**](#MerchantTrustLevelEnum) | Merchant trust classification assigned by the producer, on three trust tiers plus not trusted: TRUSTED (high trust), MODERATELY_TRUSTED (moderate trust), CONDITIONALLY_TRUSTED (low trust), NOT_TRUSTED (not trusted). UNKNOWN means the producer holds no classification; financial institutions whose format carries only these tiers receive it as not trusted. |  [optional] |
|**merchantTrustData** | **String** | Trusted signal code: the evidence behind merchantTrustLevel, as three fixed-position two-character pairs. Position 1 is customer tenure with the merchant (T0 unknown, T1 0 to 3 months, T2 3 to 12 months, T3 1 to 3 years, T4 over 3 years), position 2 is device trust (D0 unknown, D1 first seen, D2 seen once before, D3 frequently seen, D4 previously trusted), position 3 is location match (L0 unknown, L1 new location, L2 regional match, L3 full match). Any pair may be the neutral N0 (no evidence). RTN forwards a conforming code unchanged; a value in any other format is accepted but treated as absent, and RTN then derives the code from the account, device and address signals. Omit the field when the transaction is in no trust program and no evidence is available. |  [optional] |
|**cardBrand** | [**CardBrandEnum**](#CardBrandEnum) | Card product brand. |  [optional] |
|**messageCategory** | [**MessageCategoryEnum**](#MessageCategoryEnum) | Message type: 1 &#x3D; Pre-Auth Approved, 2 &#x3D; Pre-Auth Declined, 3 &#x3D; Pre-Auth Test. |  [optional] |
|**fraudPreventionPlatform** | **String** | Name of the fraud prevention platform whose score or decision this rtnData carries, as the platform is known in your own system. RTN calibrates a score by its source, so it requires the name: Revaly submits rtnData to RTN only when this field is present, and otherwise processes the payment without an RTN submission. 1 to 128 characters: letters, digits, &#39;.&#39;, &#39;_&#39;, &#39;:&#39; and &#39;-&#39;. |  [optional] |
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
| MODERATELY_TRUSTED | &quot;MODERATELY_TRUSTED&quot; |
| CONDITIONALLY_TRUSTED | &quot;CONDITIONALLY_TRUSTED&quot; |
| NOT_TRUSTED | &quot;NOT_TRUSTED&quot; |
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



