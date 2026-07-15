# RtnDataPartnerRiskData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionRiskScore** | Pointer to **string** | Transaction-level risk score assigned by the producer. String to accommodate decimal scores. | [optional] 
**IsTrustedMidPartner** | Pointer to **bool** | True if the producer is operating in Trusted MID capacity for this transaction. | [optional] 
**CustomerRiskScore** | Pointer to **string** | Customer-level risk score. | [optional] 
**DeviceRiskScore** | Pointer to **string** | Device-level risk score. | [optional] 
**IpRiskScore** | Pointer to **string** | IP address risk score. | [optional] 
**MerchantRiskScore** | Pointer to **string** | Merchant-level risk score. | [optional] 

## Methods

### NewRtnDataPartnerRiskData

`func NewRtnDataPartnerRiskData() *RtnDataPartnerRiskData`

NewRtnDataPartnerRiskData instantiates a new RtnDataPartnerRiskData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataPartnerRiskDataWithDefaults

`func NewRtnDataPartnerRiskDataWithDefaults() *RtnDataPartnerRiskData`

NewRtnDataPartnerRiskDataWithDefaults instantiates a new RtnDataPartnerRiskData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetTransactionRiskScore

`func (o *RtnDataPartnerRiskData) GetTransactionRiskScore() string`

GetTransactionRiskScore returns the TransactionRiskScore field if non-nil, zero value otherwise.

### GetTransactionRiskScoreOk

`func (o *RtnDataPartnerRiskData) GetTransactionRiskScoreOk() (*string, bool)`

GetTransactionRiskScoreOk returns a tuple with the TransactionRiskScore field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetTransactionRiskScore

`func (o *RtnDataPartnerRiskData) SetTransactionRiskScore(v string)`

SetTransactionRiskScore sets TransactionRiskScore field to given value.

### HasTransactionRiskScore

`func (o *RtnDataPartnerRiskData) HasTransactionRiskScore() bool`

HasTransactionRiskScore returns a boolean if a field has been set.

### GetIsTrustedMidPartner

`func (o *RtnDataPartnerRiskData) GetIsTrustedMidPartner() bool`

GetIsTrustedMidPartner returns the IsTrustedMidPartner field if non-nil, zero value otherwise.

### GetIsTrustedMidPartnerOk

`func (o *RtnDataPartnerRiskData) GetIsTrustedMidPartnerOk() (*bool, bool)`

GetIsTrustedMidPartnerOk returns a tuple with the IsTrustedMidPartner field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIsTrustedMidPartner

`func (o *RtnDataPartnerRiskData) SetIsTrustedMidPartner(v bool)`

SetIsTrustedMidPartner sets IsTrustedMidPartner field to given value.

### HasIsTrustedMidPartner

`func (o *RtnDataPartnerRiskData) HasIsTrustedMidPartner() bool`

HasIsTrustedMidPartner returns a boolean if a field has been set.

### GetCustomerRiskScore

`func (o *RtnDataPartnerRiskData) GetCustomerRiskScore() string`

GetCustomerRiskScore returns the CustomerRiskScore field if non-nil, zero value otherwise.

### GetCustomerRiskScoreOk

`func (o *RtnDataPartnerRiskData) GetCustomerRiskScoreOk() (*string, bool)`

GetCustomerRiskScoreOk returns a tuple with the CustomerRiskScore field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerRiskScore

`func (o *RtnDataPartnerRiskData) SetCustomerRiskScore(v string)`

SetCustomerRiskScore sets CustomerRiskScore field to given value.

### HasCustomerRiskScore

`func (o *RtnDataPartnerRiskData) HasCustomerRiskScore() bool`

HasCustomerRiskScore returns a boolean if a field has been set.

### GetDeviceRiskScore

`func (o *RtnDataPartnerRiskData) GetDeviceRiskScore() string`

GetDeviceRiskScore returns the DeviceRiskScore field if non-nil, zero value otherwise.

### GetDeviceRiskScoreOk

`func (o *RtnDataPartnerRiskData) GetDeviceRiskScoreOk() (*string, bool)`

GetDeviceRiskScoreOk returns a tuple with the DeviceRiskScore field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeviceRiskScore

`func (o *RtnDataPartnerRiskData) SetDeviceRiskScore(v string)`

SetDeviceRiskScore sets DeviceRiskScore field to given value.

### HasDeviceRiskScore

`func (o *RtnDataPartnerRiskData) HasDeviceRiskScore() bool`

HasDeviceRiskScore returns a boolean if a field has been set.

### GetIpRiskScore

`func (o *RtnDataPartnerRiskData) GetIpRiskScore() string`

GetIpRiskScore returns the IpRiskScore field if non-nil, zero value otherwise.

### GetIpRiskScoreOk

`func (o *RtnDataPartnerRiskData) GetIpRiskScoreOk() (*string, bool)`

GetIpRiskScoreOk returns a tuple with the IpRiskScore field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetIpRiskScore

`func (o *RtnDataPartnerRiskData) SetIpRiskScore(v string)`

SetIpRiskScore sets IpRiskScore field to given value.

### HasIpRiskScore

`func (o *RtnDataPartnerRiskData) HasIpRiskScore() bool`

HasIpRiskScore returns a boolean if a field has been set.

### GetMerchantRiskScore

`func (o *RtnDataPartnerRiskData) GetMerchantRiskScore() string`

GetMerchantRiskScore returns the MerchantRiskScore field if non-nil, zero value otherwise.

### GetMerchantRiskScoreOk

`func (o *RtnDataPartnerRiskData) GetMerchantRiskScoreOk() (*string, bool)`

GetMerchantRiskScoreOk returns a tuple with the MerchantRiskScore field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantRiskScore

`func (o *RtnDataPartnerRiskData) SetMerchantRiskScore(v string)`

SetMerchantRiskScore sets MerchantRiskScore field to given value.

### HasMerchantRiskScore

`func (o *RtnDataPartnerRiskData) HasMerchantRiskScore() bool`

HasMerchantRiskScore returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


