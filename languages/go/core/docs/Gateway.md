# Gateway

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Name** | Pointer to **NullableString** | Gateway name | [optional] 
**BankTypeCode** | Pointer to **NullableString** | Bank type code | [optional] 
**MerchantAccountReferenceId** | Pointer to **NullableString** | Merchant account reference ID at the gateway | [optional] 
**GatewayType** | Pointer to **NullableString** | Type of payment gateway | [optional] 
**CurrencyCode** | Pointer to **NullableString** | Primary currency code for this gateway | [optional] 
**AcceptedCurrencyCodes** | Pointer to **[]string** | List of accepted currency codes | [optional] 
**AcceptedCards** | Pointer to [**AcceptedCards**](AcceptedCards.md) |  | [optional] 
**AcceptRetries** | Pointer to **NullableBool** | Whether the gateway accepts retry transactions | [optional] 
**CvvRequired** | Pointer to **NullableBool** | Whether CVV is required for transactions | [optional] 
**ApprovedChargeOrCaptureRateFee** | Pointer to **NullableFloat64** | Rate fee for approved charges or captures | [optional] 
**ApprovedChargeOrCaptureFlatFee** | Pointer to **NullableFloat64** | Flat fee for approved charges or captures | [optional] 
**OtherTransactionFlatFee** | Pointer to **NullableFloat64** | Flat fee for other transaction types | [optional] 
**IssueRefundsThroughCredit** | Pointer to **NullableBool** | Whether refunds are issued through credit | [optional] 

## Methods

### NewGateway

`func NewGateway() *Gateway`

NewGateway instantiates a new Gateway object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewGatewayWithDefaults

`func NewGatewayWithDefaults() *Gateway`

NewGatewayWithDefaults instantiates a new Gateway object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetName

`func (o *Gateway) GetName() string`

GetName returns the Name field if non-nil, zero value otherwise.

### GetNameOk

`func (o *Gateway) GetNameOk() (*string, bool)`

GetNameOk returns a tuple with the Name field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetName

`func (o *Gateway) SetName(v string)`

SetName sets Name field to given value.

### HasName

`func (o *Gateway) HasName() bool`

HasName returns a boolean if a field has been set.

### SetNameNil

`func (o *Gateway) SetNameNil(b bool)`

 SetNameNil sets the value for Name to be an explicit nil

### UnsetName
`func (o *Gateway) UnsetName()`

UnsetName ensures that no value is present for Name, not even an explicit nil
### GetBankTypeCode

`func (o *Gateway) GetBankTypeCode() string`

GetBankTypeCode returns the BankTypeCode field if non-nil, zero value otherwise.

### GetBankTypeCodeOk

`func (o *Gateway) GetBankTypeCodeOk() (*string, bool)`

GetBankTypeCodeOk returns a tuple with the BankTypeCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBankTypeCode

`func (o *Gateway) SetBankTypeCode(v string)`

SetBankTypeCode sets BankTypeCode field to given value.

### HasBankTypeCode

`func (o *Gateway) HasBankTypeCode() bool`

HasBankTypeCode returns a boolean if a field has been set.

### SetBankTypeCodeNil

`func (o *Gateway) SetBankTypeCodeNil(b bool)`

 SetBankTypeCodeNil sets the value for BankTypeCode to be an explicit nil

### UnsetBankTypeCode
`func (o *Gateway) UnsetBankTypeCode()`

UnsetBankTypeCode ensures that no value is present for BankTypeCode, not even an explicit nil
### GetMerchantAccountReferenceId

`func (o *Gateway) GetMerchantAccountReferenceId() string`

GetMerchantAccountReferenceId returns the MerchantAccountReferenceId field if non-nil, zero value otherwise.

### GetMerchantAccountReferenceIdOk

`func (o *Gateway) GetMerchantAccountReferenceIdOk() (*string, bool)`

GetMerchantAccountReferenceIdOk returns a tuple with the MerchantAccountReferenceId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantAccountReferenceId

`func (o *Gateway) SetMerchantAccountReferenceId(v string)`

SetMerchantAccountReferenceId sets MerchantAccountReferenceId field to given value.

### HasMerchantAccountReferenceId

`func (o *Gateway) HasMerchantAccountReferenceId() bool`

HasMerchantAccountReferenceId returns a boolean if a field has been set.

### SetMerchantAccountReferenceIdNil

`func (o *Gateway) SetMerchantAccountReferenceIdNil(b bool)`

 SetMerchantAccountReferenceIdNil sets the value for MerchantAccountReferenceId to be an explicit nil

### UnsetMerchantAccountReferenceId
`func (o *Gateway) UnsetMerchantAccountReferenceId()`

UnsetMerchantAccountReferenceId ensures that no value is present for MerchantAccountReferenceId, not even an explicit nil
### GetGatewayType

`func (o *Gateway) GetGatewayType() string`

GetGatewayType returns the GatewayType field if non-nil, zero value otherwise.

### GetGatewayTypeOk

`func (o *Gateway) GetGatewayTypeOk() (*string, bool)`

GetGatewayTypeOk returns a tuple with the GatewayType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGatewayType

`func (o *Gateway) SetGatewayType(v string)`

SetGatewayType sets GatewayType field to given value.

### HasGatewayType

`func (o *Gateway) HasGatewayType() bool`

HasGatewayType returns a boolean if a field has been set.

### SetGatewayTypeNil

`func (o *Gateway) SetGatewayTypeNil(b bool)`

 SetGatewayTypeNil sets the value for GatewayType to be an explicit nil

### UnsetGatewayType
`func (o *Gateway) UnsetGatewayType()`

UnsetGatewayType ensures that no value is present for GatewayType, not even an explicit nil
### GetCurrencyCode

`func (o *Gateway) GetCurrencyCode() string`

GetCurrencyCode returns the CurrencyCode field if non-nil, zero value otherwise.

### GetCurrencyCodeOk

`func (o *Gateway) GetCurrencyCodeOk() (*string, bool)`

GetCurrencyCodeOk returns a tuple with the CurrencyCode field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCurrencyCode

`func (o *Gateway) SetCurrencyCode(v string)`

SetCurrencyCode sets CurrencyCode field to given value.

### HasCurrencyCode

`func (o *Gateway) HasCurrencyCode() bool`

HasCurrencyCode returns a boolean if a field has been set.

### SetCurrencyCodeNil

`func (o *Gateway) SetCurrencyCodeNil(b bool)`

 SetCurrencyCodeNil sets the value for CurrencyCode to be an explicit nil

### UnsetCurrencyCode
`func (o *Gateway) UnsetCurrencyCode()`

UnsetCurrencyCode ensures that no value is present for CurrencyCode, not even an explicit nil
### GetAcceptedCurrencyCodes

`func (o *Gateway) GetAcceptedCurrencyCodes() []string`

GetAcceptedCurrencyCodes returns the AcceptedCurrencyCodes field if non-nil, zero value otherwise.

### GetAcceptedCurrencyCodesOk

`func (o *Gateway) GetAcceptedCurrencyCodesOk() (*[]string, bool)`

GetAcceptedCurrencyCodesOk returns a tuple with the AcceptedCurrencyCodes field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcceptedCurrencyCodes

`func (o *Gateway) SetAcceptedCurrencyCodes(v []string)`

SetAcceptedCurrencyCodes sets AcceptedCurrencyCodes field to given value.

### HasAcceptedCurrencyCodes

`func (o *Gateway) HasAcceptedCurrencyCodes() bool`

HasAcceptedCurrencyCodes returns a boolean if a field has been set.

### SetAcceptedCurrencyCodesNil

`func (o *Gateway) SetAcceptedCurrencyCodesNil(b bool)`

 SetAcceptedCurrencyCodesNil sets the value for AcceptedCurrencyCodes to be an explicit nil

### UnsetAcceptedCurrencyCodes
`func (o *Gateway) UnsetAcceptedCurrencyCodes()`

UnsetAcceptedCurrencyCodes ensures that no value is present for AcceptedCurrencyCodes, not even an explicit nil
### GetAcceptedCards

`func (o *Gateway) GetAcceptedCards() AcceptedCards`

GetAcceptedCards returns the AcceptedCards field if non-nil, zero value otherwise.

### GetAcceptedCardsOk

`func (o *Gateway) GetAcceptedCardsOk() (*AcceptedCards, bool)`

GetAcceptedCardsOk returns a tuple with the AcceptedCards field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcceptedCards

`func (o *Gateway) SetAcceptedCards(v AcceptedCards)`

SetAcceptedCards sets AcceptedCards field to given value.

### HasAcceptedCards

`func (o *Gateway) HasAcceptedCards() bool`

HasAcceptedCards returns a boolean if a field has been set.

### GetAcceptRetries

`func (o *Gateway) GetAcceptRetries() bool`

GetAcceptRetries returns the AcceptRetries field if non-nil, zero value otherwise.

### GetAcceptRetriesOk

`func (o *Gateway) GetAcceptRetriesOk() (*bool, bool)`

GetAcceptRetriesOk returns a tuple with the AcceptRetries field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcceptRetries

`func (o *Gateway) SetAcceptRetries(v bool)`

SetAcceptRetries sets AcceptRetries field to given value.

### HasAcceptRetries

`func (o *Gateway) HasAcceptRetries() bool`

HasAcceptRetries returns a boolean if a field has been set.

### SetAcceptRetriesNil

`func (o *Gateway) SetAcceptRetriesNil(b bool)`

 SetAcceptRetriesNil sets the value for AcceptRetries to be an explicit nil

### UnsetAcceptRetries
`func (o *Gateway) UnsetAcceptRetries()`

UnsetAcceptRetries ensures that no value is present for AcceptRetries, not even an explicit nil
### GetCvvRequired

`func (o *Gateway) GetCvvRequired() bool`

GetCvvRequired returns the CvvRequired field if non-nil, zero value otherwise.

### GetCvvRequiredOk

`func (o *Gateway) GetCvvRequiredOk() (*bool, bool)`

GetCvvRequiredOk returns a tuple with the CvvRequired field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCvvRequired

`func (o *Gateway) SetCvvRequired(v bool)`

SetCvvRequired sets CvvRequired field to given value.

### HasCvvRequired

`func (o *Gateway) HasCvvRequired() bool`

HasCvvRequired returns a boolean if a field has been set.

### SetCvvRequiredNil

`func (o *Gateway) SetCvvRequiredNil(b bool)`

 SetCvvRequiredNil sets the value for CvvRequired to be an explicit nil

### UnsetCvvRequired
`func (o *Gateway) UnsetCvvRequired()`

UnsetCvvRequired ensures that no value is present for CvvRequired, not even an explicit nil
### GetApprovedChargeOrCaptureRateFee

`func (o *Gateway) GetApprovedChargeOrCaptureRateFee() float64`

GetApprovedChargeOrCaptureRateFee returns the ApprovedChargeOrCaptureRateFee field if non-nil, zero value otherwise.

### GetApprovedChargeOrCaptureRateFeeOk

`func (o *Gateway) GetApprovedChargeOrCaptureRateFeeOk() (*float64, bool)`

GetApprovedChargeOrCaptureRateFeeOk returns a tuple with the ApprovedChargeOrCaptureRateFee field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetApprovedChargeOrCaptureRateFee

`func (o *Gateway) SetApprovedChargeOrCaptureRateFee(v float64)`

SetApprovedChargeOrCaptureRateFee sets ApprovedChargeOrCaptureRateFee field to given value.

### HasApprovedChargeOrCaptureRateFee

`func (o *Gateway) HasApprovedChargeOrCaptureRateFee() bool`

HasApprovedChargeOrCaptureRateFee returns a boolean if a field has been set.

### SetApprovedChargeOrCaptureRateFeeNil

`func (o *Gateway) SetApprovedChargeOrCaptureRateFeeNil(b bool)`

 SetApprovedChargeOrCaptureRateFeeNil sets the value for ApprovedChargeOrCaptureRateFee to be an explicit nil

### UnsetApprovedChargeOrCaptureRateFee
`func (o *Gateway) UnsetApprovedChargeOrCaptureRateFee()`

UnsetApprovedChargeOrCaptureRateFee ensures that no value is present for ApprovedChargeOrCaptureRateFee, not even an explicit nil
### GetApprovedChargeOrCaptureFlatFee

`func (o *Gateway) GetApprovedChargeOrCaptureFlatFee() float64`

GetApprovedChargeOrCaptureFlatFee returns the ApprovedChargeOrCaptureFlatFee field if non-nil, zero value otherwise.

### GetApprovedChargeOrCaptureFlatFeeOk

`func (o *Gateway) GetApprovedChargeOrCaptureFlatFeeOk() (*float64, bool)`

GetApprovedChargeOrCaptureFlatFeeOk returns a tuple with the ApprovedChargeOrCaptureFlatFee field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetApprovedChargeOrCaptureFlatFee

`func (o *Gateway) SetApprovedChargeOrCaptureFlatFee(v float64)`

SetApprovedChargeOrCaptureFlatFee sets ApprovedChargeOrCaptureFlatFee field to given value.

### HasApprovedChargeOrCaptureFlatFee

`func (o *Gateway) HasApprovedChargeOrCaptureFlatFee() bool`

HasApprovedChargeOrCaptureFlatFee returns a boolean if a field has been set.

### SetApprovedChargeOrCaptureFlatFeeNil

`func (o *Gateway) SetApprovedChargeOrCaptureFlatFeeNil(b bool)`

 SetApprovedChargeOrCaptureFlatFeeNil sets the value for ApprovedChargeOrCaptureFlatFee to be an explicit nil

### UnsetApprovedChargeOrCaptureFlatFee
`func (o *Gateway) UnsetApprovedChargeOrCaptureFlatFee()`

UnsetApprovedChargeOrCaptureFlatFee ensures that no value is present for ApprovedChargeOrCaptureFlatFee, not even an explicit nil
### GetOtherTransactionFlatFee

`func (o *Gateway) GetOtherTransactionFlatFee() float64`

GetOtherTransactionFlatFee returns the OtherTransactionFlatFee field if non-nil, zero value otherwise.

### GetOtherTransactionFlatFeeOk

`func (o *Gateway) GetOtherTransactionFlatFeeOk() (*float64, bool)`

GetOtherTransactionFlatFeeOk returns a tuple with the OtherTransactionFlatFee field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOtherTransactionFlatFee

`func (o *Gateway) SetOtherTransactionFlatFee(v float64)`

SetOtherTransactionFlatFee sets OtherTransactionFlatFee field to given value.

### HasOtherTransactionFlatFee

`func (o *Gateway) HasOtherTransactionFlatFee() bool`

HasOtherTransactionFlatFee returns a boolean if a field has been set.

### SetOtherTransactionFlatFeeNil

`func (o *Gateway) SetOtherTransactionFlatFeeNil(b bool)`

 SetOtherTransactionFlatFeeNil sets the value for OtherTransactionFlatFee to be an explicit nil

### UnsetOtherTransactionFlatFee
`func (o *Gateway) UnsetOtherTransactionFlatFee()`

UnsetOtherTransactionFlatFee ensures that no value is present for OtherTransactionFlatFee, not even an explicit nil
### GetIssueRefundsThroughCredit

`func (o *Gateway) GetIssueRefundsThroughCredit() bool`

GetIssueRefundsThroughCredit returns the IssueRefundsThroughCredit field if non-nil, zero value otherwise.

### GetIssueRefundsThroughCreditOk

`func (o *Gateway) GetIssueRefundsThroughCreditOk() (*bool, bool)`

GetIssueRefundsThroughCreditOk returns a tuple with the IssueRefundsThroughCredit field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIssueRefundsThroughCredit

`func (o *Gateway) SetIssueRefundsThroughCredit(v bool)`

SetIssueRefundsThroughCredit sets IssueRefundsThroughCredit field to given value.

### HasIssueRefundsThroughCredit

`func (o *Gateway) HasIssueRefundsThroughCredit() bool`

HasIssueRefundsThroughCredit returns a boolean if a field has been set.

### SetIssueRefundsThroughCreditNil

`func (o *Gateway) SetIssueRefundsThroughCreditNil(b bool)`

 SetIssueRefundsThroughCreditNil sets the value for IssueRefundsThroughCredit to be an explicit nil

### UnsetIssueRefundsThroughCredit
`func (o *Gateway) UnsetIssueRefundsThroughCredit()`

UnsetIssueRefundsThroughCredit ensures that no value is present for IssueRefundsThroughCredit, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


