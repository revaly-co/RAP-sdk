# Revaly.Sdk.Core.Model.RtnDataAdditionalTransactionData
Core transaction signals supplied by the request producer. Transaction-routing fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) are derived by Revaly at submission time and must not be sent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ProviderAuthDecision** | **string** | Authorization decision from the producer. Required for Trusted MID flows. | [optional] 
**ProviderAuthDecisionCode** | **string** | Provider-specific reason code for the auth decision. Required for Trusted MID flows. | [optional] 
**PaymentRail** | **string** | Payment routing rail. | [optional] 
**PosEntryMode** | **string** | Credential capture method at the point of sale. | [optional] 
**RetrievalReferenceNumber** | **string** | Transaction retrieval reference number. | [optional] 
**MerchantTrustLevel** | **string** | Merchant trust classification assigned by the producer. | [optional] 
**MerchantTrustData** | **string** | Producer metadata encoding the basis for the trust classification. | [optional] 
**CardBrand** | **string** | Card product brand. | [optional] 
**MessageCategory** | **string** | Message type: 1 &#x3D; Pre-Auth Approved, 2 &#x3D; Pre-Auth Declined, 3 &#x3D; Pre-Auth Test. | [optional] 
**FullPan** | **string** | Full card Primary Account Number (cardholder data / CHD). Optional. Forwarded to RTN in-flight only — never persisted or logged at rest by RAP. Sending this field transmits cardholder data; ensure your integration is authorized under your PCI-DSS obligations. | [optional] 
**Dpan** | **string** | Device Primary Account Number (tokenized card number from a digital wallet). | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

