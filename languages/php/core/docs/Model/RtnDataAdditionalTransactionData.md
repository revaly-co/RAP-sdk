# RtnDataAdditionalTransactionData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**provider_auth_decision** | **string** | Authorization decision from the producer. Required for Trusted MID flows. | [optional]
**provider_auth_decision_code** | **string** | Provider-specific reason code for the auth decision. Required for Trusted MID flows. | [optional]
**payment_rail** | **string** | Payment routing rail. | [optional]
**pos_entry_mode** | **string** | Credential capture method at the point of sale. | [optional]
**retrieval_reference_number** | **string** | Transaction retrieval reference number. | [optional]
**merchant_trust_level** | **string** | Merchant trust classification assigned by the producer. | [optional]
**merchant_trust_data** | **string** | Producer metadata encoding the basis for the trust classification. | [optional]
**card_brand** | **string** | Card product brand. | [optional]
**message_category** | **string** | Message type: 1 &#x3D; Pre-Auth Approved, 2 &#x3D; Pre-Auth Declined, 3 &#x3D; Pre-Auth Test. | [optional]
**full_pan** | **string** | Full card Primary Account Number (cardholder data / CHD). Optional. Forwarded to RTN in-flight only — never persisted or logged at rest by RAP. Sending this field transmits cardholder data; ensure your integration is authorized under your PCI-DSS obligations. | [optional]
**dpan** | **string** | Device Primary Account Number (tokenized card number from a digital wallet). | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
