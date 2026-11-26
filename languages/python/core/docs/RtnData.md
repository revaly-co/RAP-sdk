# RtnData

Typed RTN fraud-signal payload (customer signals only). Transaction-core fields (bin, lastFourCardNumber, purchaseAmount, purchaseCurrency, clientInitiatedDate, traceId, providerId) and the RTN reporting keys and timing instants (merchantIdentifier, orderIdentifier, producerProcessStartedAt, producerRequestSentAt) are derived by Revaly at submission time and must not be sent. The full PAN (additionalTransactionData.fullPan) is optional and, if sent, is forwarded to RTN in-flight only. Every field is an optional signal, and no rtnData value ever refuses the payment that carries it. The lengths, formats and value lists below describe what the card issuers can use. A value outside them is accepted, and RTN trims, converts, shortens or leaves out that one value before it reaches an issuer. A value of the wrong JSON type (text where a number or a boolean is expected, for example) is left out the same way, and the rest of rtnData is still sent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**additional_transaction_data** | [**RtnDataAdditionalTransactionData**](RtnDataAdditionalTransactionData.md) |  | [optional] 
**billing_data** | [**RtnDataBillingData**](RtnDataBillingData.md) |  | [optional] 
**custom_data** | [**RtnDataCustomData**](RtnDataCustomData.md) |  | [optional] 
**customer_data** | [**RtnDataCustomerData**](RtnDataCustomerData.md) |  | [optional] 
**device_data** | [**RtnDataDeviceData**](RtnDataDeviceData.md) |  | [optional] 
**merchant_data** | [**RtnDataMerchantData**](RtnDataMerchantData.md) |  | [optional] 
**order_data** | [**RtnDataOrderData**](RtnDataOrderData.md) |  | [optional] 
**partner_risk_data** | [**RtnDataPartnerRiskData**](RtnDataPartnerRiskData.md) |  | [optional] 
**shipping_data** | [**RtnDataShippingData**](RtnDataShippingData.md) |  | [optional] 
**seller_data** | [**RtnDataSellerData**](RtnDataSellerData.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data import RtnData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnData from a JSON string
rtn_data_instance = RtnData.from_json(json)
# print the JSON string representation of the object
print(RtnData.to_json())

# convert the object into a dict
rtn_data_dict = rtn_data_instance.to_dict()
# create an instance of RtnData from a dict
rtn_data_from_dict = RtnData.from_dict(rtn_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


