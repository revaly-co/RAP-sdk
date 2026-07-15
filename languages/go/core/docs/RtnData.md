# RtnData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**AdditionalTransactionData** | Pointer to [**RtnDataAdditionalTransactionData**](RtnDataAdditionalTransactionData.md) |  | [optional] 
**BillingData** | Pointer to [**RtnDataBillingData**](RtnDataBillingData.md) |  | [optional] 
**CustomData** | Pointer to [**RtnDataCustomData**](RtnDataCustomData.md) |  | [optional] 
**CustomerData** | Pointer to [**RtnDataCustomerData**](RtnDataCustomerData.md) |  | [optional] 
**DeviceData** | Pointer to [**RtnDataDeviceData**](RtnDataDeviceData.md) |  | [optional] 
**MerchantData** | Pointer to [**RtnDataMerchantData**](RtnDataMerchantData.md) |  | [optional] 
**OrderData** | Pointer to [**RtnDataOrderData**](RtnDataOrderData.md) |  | [optional] 
**PartnerRiskData** | Pointer to [**RtnDataPartnerRiskData**](RtnDataPartnerRiskData.md) |  | [optional] 
**ShippingData** | Pointer to [**RtnDataShippingData**](RtnDataShippingData.md) |  | [optional] 
**SellerData** | Pointer to [**RtnDataSellerData**](RtnDataSellerData.md) |  | [optional] 

## Methods

### NewRtnData

`func NewRtnData() *RtnData`

NewRtnData instantiates a new RtnData object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewRtnDataWithDefaults

`func NewRtnDataWithDefaults() *RtnData`

NewRtnDataWithDefaults instantiates a new RtnData object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetAdditionalTransactionData

`func (o *RtnData) GetAdditionalTransactionData() RtnDataAdditionalTransactionData`

GetAdditionalTransactionData returns the AdditionalTransactionData field if non-nil, zero value otherwise.

### GetAdditionalTransactionDataOk

`func (o *RtnData) GetAdditionalTransactionDataOk() (*RtnDataAdditionalTransactionData, bool)`

GetAdditionalTransactionDataOk returns a tuple with the AdditionalTransactionData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAdditionalTransactionData

`func (o *RtnData) SetAdditionalTransactionData(v RtnDataAdditionalTransactionData)`

SetAdditionalTransactionData sets AdditionalTransactionData field to given value.

### HasAdditionalTransactionData

`func (o *RtnData) HasAdditionalTransactionData() bool`

HasAdditionalTransactionData returns a boolean if a field has been set.

### GetBillingData

`func (o *RtnData) GetBillingData() RtnDataBillingData`

GetBillingData returns the BillingData field if non-nil, zero value otherwise.

### GetBillingDataOk

`func (o *RtnData) GetBillingDataOk() (*RtnDataBillingData, bool)`

GetBillingDataOk returns a tuple with the BillingData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetBillingData

`func (o *RtnData) SetBillingData(v RtnDataBillingData)`

SetBillingData sets BillingData field to given value.

### HasBillingData

`func (o *RtnData) HasBillingData() bool`

HasBillingData returns a boolean if a field has been set.

### GetCustomData

`func (o *RtnData) GetCustomData() RtnDataCustomData`

GetCustomData returns the CustomData field if non-nil, zero value otherwise.

### GetCustomDataOk

`func (o *RtnData) GetCustomDataOk() (*RtnDataCustomData, bool)`

GetCustomDataOk returns a tuple with the CustomData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomData

`func (o *RtnData) SetCustomData(v RtnDataCustomData)`

SetCustomData sets CustomData field to given value.

### HasCustomData

`func (o *RtnData) HasCustomData() bool`

HasCustomData returns a boolean if a field has been set.

### GetCustomerData

`func (o *RtnData) GetCustomerData() RtnDataCustomerData`

GetCustomerData returns the CustomerData field if non-nil, zero value otherwise.

### GetCustomerDataOk

`func (o *RtnData) GetCustomerDataOk() (*RtnDataCustomerData, bool)`

GetCustomerDataOk returns a tuple with the CustomerData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCustomerData

`func (o *RtnData) SetCustomerData(v RtnDataCustomerData)`

SetCustomerData sets CustomerData field to given value.

### HasCustomerData

`func (o *RtnData) HasCustomerData() bool`

HasCustomerData returns a boolean if a field has been set.

### GetDeviceData

`func (o *RtnData) GetDeviceData() RtnDataDeviceData`

GetDeviceData returns the DeviceData field if non-nil, zero value otherwise.

### GetDeviceDataOk

`func (o *RtnData) GetDeviceDataOk() (*RtnDataDeviceData, bool)`

GetDeviceDataOk returns a tuple with the DeviceData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDeviceData

`func (o *RtnData) SetDeviceData(v RtnDataDeviceData)`

SetDeviceData sets DeviceData field to given value.

### HasDeviceData

`func (o *RtnData) HasDeviceData() bool`

HasDeviceData returns a boolean if a field has been set.

### GetMerchantData

`func (o *RtnData) GetMerchantData() RtnDataMerchantData`

GetMerchantData returns the MerchantData field if non-nil, zero value otherwise.

### GetMerchantDataOk

`func (o *RtnData) GetMerchantDataOk() (*RtnDataMerchantData, bool)`

GetMerchantDataOk returns a tuple with the MerchantData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetMerchantData

`func (o *RtnData) SetMerchantData(v RtnDataMerchantData)`

SetMerchantData sets MerchantData field to given value.

### HasMerchantData

`func (o *RtnData) HasMerchantData() bool`

HasMerchantData returns a boolean if a field has been set.

### GetOrderData

`func (o *RtnData) GetOrderData() RtnDataOrderData`

GetOrderData returns the OrderData field if non-nil, zero value otherwise.

### GetOrderDataOk

`func (o *RtnData) GetOrderDataOk() (*RtnDataOrderData, bool)`

GetOrderDataOk returns a tuple with the OrderData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetOrderData

`func (o *RtnData) SetOrderData(v RtnDataOrderData)`

SetOrderData sets OrderData field to given value.

### HasOrderData

`func (o *RtnData) HasOrderData() bool`

HasOrderData returns a boolean if a field has been set.

### GetPartnerRiskData

`func (o *RtnData) GetPartnerRiskData() RtnDataPartnerRiskData`

GetPartnerRiskData returns the PartnerRiskData field if non-nil, zero value otherwise.

### GetPartnerRiskDataOk

`func (o *RtnData) GetPartnerRiskDataOk() (*RtnDataPartnerRiskData, bool)`

GetPartnerRiskDataOk returns a tuple with the PartnerRiskData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetPartnerRiskData

`func (o *RtnData) SetPartnerRiskData(v RtnDataPartnerRiskData)`

SetPartnerRiskData sets PartnerRiskData field to given value.

### HasPartnerRiskData

`func (o *RtnData) HasPartnerRiskData() bool`

HasPartnerRiskData returns a boolean if a field has been set.

### GetShippingData

`func (o *RtnData) GetShippingData() RtnDataShippingData`

GetShippingData returns the ShippingData field if non-nil, zero value otherwise.

### GetShippingDataOk

`func (o *RtnData) GetShippingDataOk() (*RtnDataShippingData, bool)`

GetShippingDataOk returns a tuple with the ShippingData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetShippingData

`func (o *RtnData) SetShippingData(v RtnDataShippingData)`

SetShippingData sets ShippingData field to given value.

### HasShippingData

`func (o *RtnData) HasShippingData() bool`

HasShippingData returns a boolean if a field has been set.

### GetSellerData

`func (o *RtnData) GetSellerData() RtnDataSellerData`

GetSellerData returns the SellerData field if non-nil, zero value otherwise.

### GetSellerDataOk

`func (o *RtnData) GetSellerDataOk() (*RtnDataSellerData, bool)`

GetSellerDataOk returns a tuple with the SellerData field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSellerData

`func (o *RtnData) SetSellerData(v RtnDataSellerData)`

SetSellerData sets SellerData field to given value.

### HasSellerData

`func (o *RtnData) HasSellerData() bool`

HasSellerData returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


