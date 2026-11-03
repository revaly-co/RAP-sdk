# Revaly.Sdk.Core.Model.RtnDataAdditionalTransactionData
Core transaction signals supplied by the request producer. Transaction-routing fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) and the RTN reporting keys and timing instants (merchantIdentifier, orderIdentifier, producerProcessStartedAt, producerRequestSentAt) are derived by Revaly at submission time and must not be sent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ProviderAuthDecision** | **string** | Authorization decision from the producer. Required for Trusted MID flows. | [optional] 
**ProviderAuthDecisionCode** | **string** | Provider-specific reason code for the auth decision. Required for Trusted MID flows. | [optional] 
**PaymentRail** | **string** | Payment routing rail. | [optional] 
**PosEntryMode** | **string** | Credential capture method at the point of sale. | [optional] 
**RetrievalReferenceNumber** | **string** | Transaction retrieval reference number. | [optional] 
**MerchantTrustLevel** | **string** | Merchant trust classification assigned by the producer, on three trust tiers plus not trusted: TRUSTED (high trust), MODERATELY_TRUSTED (moderate trust), CONDITIONALLY_TRUSTED (low trust), NOT_TRUSTED (not trusted). UNKNOWN means the producer holds no classification; financial institutions whose format carries only these tiers receive it as not trusted. | [optional] 
**MerchantTrustData** | **string** | Trusted signal code: the evidence behind merchantTrustLevel, as three fixed-position two-character pairs. Position 1 is customer tenure with the merchant (T0 unknown, T1 0 to 3 months, T2 3 to 12 months, T3 1 to 3 years, T4 over 3 years), position 2 is device trust (D0 unknown, D1 first seen, D2 seen once before, D3 frequently seen, D4 previously trusted), position 3 is location match (L0 unknown, L1 new location, L2 regional match, L3 full match). Any pair may be the neutral N0 (no evidence). RTN forwards a conforming code unchanged; a value in any other format is accepted but treated as absent, and RTN then derives the code from the account, device and address signals. Omit the field when the transaction is in no trust program and no evidence is available. | [optional] 
**CardBrand** | **string** | Card product brand. | [optional] 
**MessageCategory** | **string** | Message type: 1 &#x3D; Pre-Auth Approved, 2 &#x3D; Pre-Auth Declined, 3 &#x3D; Pre-Auth Test. | [optional] 
**FraudPreventionPlatform** | **string** | Name of the fraud prevention platform whose score or decision this rtnData carries, as the platform is known in your own system. RTN calibrates a score by its source, so it requires the name: Revaly submits rtnData to RTN only when this field is present, and otherwise processes the payment without an RTN submission. 1 to 128 characters: letters, digits, &#39;.&#39;, &#39;_&#39;, &#39;:&#39; and &#39;-&#39;. | [optional] 
**FullPan** | **string** | Full card Primary Account Number (cardholder data / CHD). Optional. Forwarded to RTN in-flight only — never persisted or logged at rest by RAP. Sending this field transmits cardholder data; ensure your integration is authorized under your PCI-DSS obligations. | [optional] 
**Dpan** | **string** | Device Primary Account Number (tokenized card number from a digital wallet). | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

