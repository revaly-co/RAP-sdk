# RtnDataAdditionalTransactionData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ProviderAuthDecision** | Pointer to **string** | Authorization decision from the producer. Required for Trusted MID flows. | [optional] 
**ProviderAuthDecisionCode** | Pointer to **string** | Provider-specific reason code for the auth decision. Required for Trusted MID flows. | [optional] 
**PaymentRail** | Pointer to **string** | Payment routing rail. | [optional] 
**PosEntryMode** | Pointer to **string** | Credential capture method at the point of sale. | [optional] 
**RetrievalReferenceNumber** | Pointer to **string** | Transaction retrieval reference number. | [optional] 
**MerchantTrustLevel** | Pointer to **string** | Merchant trust classification assigned by the producer. | [optional] 
**MerchantTrustData** | Pointer to **string** | Producer metadata encoding the basis for the trust classification. | [optional] 
**CardBrand** | Pointer to **string** | Card product brand. | [optional] 
**MessageCategory** | Pointer to **string** | Message type: 1 &#x3D; Pre-Auth Approved, 2 &#x3D; Pre-Auth Declined, 3 &#x3D; Pre-Auth Test. | [optional] 
**FullPan** | Pointer to **string** | Full card Primary Account Number (cardholder data / CHD). Optional. Forwarded to RTN in-flight only — never persisted or logged at rest by RAP. Sending this field transmits cardholder data; ensure your integration is authorized under your PCI-DSS obligations. | [optional] 
**Dpan** | Pointer to **string** | Device Primary Account Number (tokenized card number from a digital wallet). | [optional] 

## Methods

### NewRtnDataAdditionalTransactionData

`func NewRtnDataAdditionalTransactionData() *RtnDataAdditionalTransactionData`

NewRtnDataAdditionalTransactionData instantiates a new RtnDataAdditionalTransactionData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataAdditionalTransactionDataWithDefaults

`func NewRtnDataAdditionalTransactionDataWithDefaults() *RtnDataAdditionalTransactionData`

NewRtnDataAdditionalTransactionDataWithDefaults instantiates a new RtnDataAdditionalTransactionData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetProviderAuthDecision

`func (o *RtnDataAdditionalTransactionData) GetProviderAuthDecision() string`

GetProviderAuthDecision returns the ProviderAuthDecision field if non-nil, zero value otherwise.

### GetProviderAuthDecisionOk

`func (o *RtnDataAdditionalTransactionData) GetProviderAuthDecisionOk() (*string, bool)`

GetProviderAuthDecisionOk returns a tuple with the ProviderAuthDecision field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetProviderAuthDecision

`func (o *RtnDataAdditionalTransactionData) SetProviderAuthDecision(v string)`

SetProviderAuthDecision sets ProviderAuthDecision field to given value.

### HasProviderAuthDecision

`func (o *RtnDataAdditionalTransactionData) HasProviderAuthDecision() bool`

HasProviderAuthDecision returns a boolean if a field has been set.

### GetProviderAuthDecisionCode

`func (o *RtnDataAdditionalTransactionData) GetProviderAuthDecisionCode() string`

GetProviderAuthDecisionCode returns the ProviderAuthDecisionCode field if non-nil, zero value otherwise.

### GetProviderAuthDecisionCodeOk

`func (o *RtnDataAdditionalTransactionData) GetProviderAuthDecisionCodeOk() (*string, bool)`

GetProviderAuthDecisionCodeOk returns a tuple with the ProviderAuthDecisionCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetProviderAuthDecisionCode

`func (o *RtnDataAdditionalTransactionData) SetProviderAuthDecisionCode(v string)`

SetProviderAuthDecisionCode sets ProviderAuthDecisionCode field to given value.

### HasProviderAuthDecisionCode

`func (o *RtnDataAdditionalTransactionData) HasProviderAuthDecisionCode() bool`

HasProviderAuthDecisionCode returns a boolean if a field has been set.

### GetPaymentRail

`func (o *RtnDataAdditionalTransactionData) GetPaymentRail() string`

GetPaymentRail returns the PaymentRail field if non-nil, zero value otherwise.

### GetPaymentRailOk

`func (o *RtnDataAdditionalTransactionData) GetPaymentRailOk() (*string, bool)`

GetPaymentRailOk returns a tuple with the PaymentRail field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPaymentRail

`func (o *RtnDataAdditionalTransactionData) SetPaymentRail(v string)`

SetPaymentRail sets PaymentRail field to given value.

### HasPaymentRail

`func (o *RtnDataAdditionalTransactionData) HasPaymentRail() bool`

HasPaymentRail returns a boolean if a field has been set.

### GetPosEntryMode

`func (o *RtnDataAdditionalTransactionData) GetPosEntryMode() string`

GetPosEntryMode returns the PosEntryMode field if non-nil, zero value otherwise.

### GetPosEntryModeOk

`func (o *RtnDataAdditionalTransactionData) GetPosEntryModeOk() (*string, bool)`

GetPosEntryModeOk returns a tuple with the PosEntryMode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPosEntryMode

`func (o *RtnDataAdditionalTransactionData) SetPosEntryMode(v string)`

SetPosEntryMode sets PosEntryMode field to given value.

### HasPosEntryMode

`func (o *RtnDataAdditionalTransactionData) HasPosEntryMode() bool`

HasPosEntryMode returns a boolean if a field has been set.

### GetRetrievalReferenceNumber

`func (o *RtnDataAdditionalTransactionData) GetRetrievalReferenceNumber() string`

GetRetrievalReferenceNumber returns the RetrievalReferenceNumber field if non-nil, zero value otherwise.

### GetRetrievalReferenceNumberOk

`func (o *RtnDataAdditionalTransactionData) GetRetrievalReferenceNumberOk() (*string, bool)`

GetRetrievalReferenceNumberOk returns a tuple with the RetrievalReferenceNumber field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetRetrievalReferenceNumber

`func (o *RtnDataAdditionalTransactionData) SetRetrievalReferenceNumber(v string)`

SetRetrievalReferenceNumber sets RetrievalReferenceNumber field to given value.

### HasRetrievalReferenceNumber

`func (o *RtnDataAdditionalTransactionData) HasRetrievalReferenceNumber() bool`

HasRetrievalReferenceNumber returns a boolean if a field has been set.

### GetMerchantTrustLevel

`func (o *RtnDataAdditionalTransactionData) GetMerchantTrustLevel() string`

GetMerchantTrustLevel returns the MerchantTrustLevel field if non-nil, zero value otherwise.

### GetMerchantTrustLevelOk

`func (o *RtnDataAdditionalTransactionData) GetMerchantTrustLevelOk() (*string, bool)`

GetMerchantTrustLevelOk returns a tuple with the MerchantTrustLevel field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTrustLevel

`func (o *RtnDataAdditionalTransactionData) SetMerchantTrustLevel(v string)`

SetMerchantTrustLevel sets MerchantTrustLevel field to given value.

### HasMerchantTrustLevel

`func (o *RtnDataAdditionalTransactionData) HasMerchantTrustLevel() bool`

HasMerchantTrustLevel returns a boolean if a field has been set.

### GetMerchantTrustData

`func (o *RtnDataAdditionalTransactionData) GetMerchantTrustData() string`

GetMerchantTrustData returns the MerchantTrustData field if non-nil, zero value otherwise.

### GetMerchantTrustDataOk

`func (o *RtnDataAdditionalTransactionData) GetMerchantTrustDataOk() (*string, bool)`

GetMerchantTrustDataOk returns a tuple with the MerchantTrustData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantTrustData

`func (o *RtnDataAdditionalTransactionData) SetMerchantTrustData(v string)`

SetMerchantTrustData sets MerchantTrustData field to given value.

### HasMerchantTrustData

`func (o *RtnDataAdditionalTransactionData) HasMerchantTrustData() bool`

HasMerchantTrustData returns a boolean if a field has been set.

### GetCardBrand

`func (o *RtnDataAdditionalTransactionData) GetCardBrand() string`

GetCardBrand returns the CardBrand field if non-nil, zero value otherwise.

### GetCardBrandOk

`func (o *RtnDataAdditionalTransactionData) GetCardBrandOk() (*string, bool)`

GetCardBrandOk returns a tuple with the CardBrand field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCardBrand

`func (o *RtnDataAdditionalTransactionData) SetCardBrand(v string)`

SetCardBrand sets CardBrand field to given value.

### HasCardBrand

`func (o *RtnDataAdditionalTransactionData) HasCardBrand() bool`

HasCardBrand returns a boolean if a field has been set.

### GetMessageCategory

`func (o *RtnDataAdditionalTransactionData) GetMessageCategory() string`

GetMessageCategory returns the MessageCategory field if non-nil, zero value otherwise.

### GetMessageCategoryOk

`func (o *RtnDataAdditionalTransactionData) GetMessageCategoryOk() (*string, bool)`

GetMessageCategoryOk returns a tuple with the MessageCategory field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMessageCategory

`func (o *RtnDataAdditionalTransactionData) SetMessageCategory(v string)`

SetMessageCategory sets MessageCategory field to given value.

### HasMessageCategory

`func (o *RtnDataAdditionalTransactionData) HasMessageCategory() bool`

HasMessageCategory returns a boolean if a field has been set.

### GetFullPan

`func (o *RtnDataAdditionalTransactionData) GetFullPan() string`

GetFullPan returns the FullPan field if non-nil, zero value otherwise.

### GetFullPanOk

`func (o *RtnDataAdditionalTransactionData) GetFullPanOk() (*string, bool)`

GetFullPanOk returns a tuple with the FullPan field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetFullPan

`func (o *RtnDataAdditionalTransactionData) SetFullPan(v string)`

SetFullPan sets FullPan field to given value.

### HasFullPan

`func (o *RtnDataAdditionalTransactionData) HasFullPan() bool`

HasFullPan returns a boolean if a field has been set.

### GetDpan

`func (o *RtnDataAdditionalTransactionData) GetDpan() string`

GetDpan returns the Dpan field if non-nil, zero value otherwise.

### GetDpanOk

`func (o *RtnDataAdditionalTransactionData) GetDpanOk() (*string, bool)`

GetDpanOk returns a tuple with the Dpan field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDpan

`func (o *RtnDataAdditionalTransactionData) SetDpan(v string)`

SetDpan sets Dpan field to given value.

### HasDpan

`func (o *RtnDataAdditionalTransactionData) HasDpan() bool`

HasDpan returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


