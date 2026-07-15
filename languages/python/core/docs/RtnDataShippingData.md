# RtnDataShippingData

Shipping address and delivery signals. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_indicator** | **str** | Relationship between billing and shipping address: 01 &#x3D; Same as billing, 02 &#x3D; Different (verified), 03 &#x3D; Different (unverified), 04 &#x3D; Retail store pickup, 05 &#x3D; Digital delivery, 06 &#x3D; Not shipped, 07 &#x3D; Other. | [optional] 
**address_line1** | **str** | First line of the shipping address. | [optional] 
**address_line2** | **str** | Second line of the shipping address. | [optional] 
**address_line3** | **str** | Third line of the shipping address. | [optional] 
**city** | **str** | City of the shipping address. | [optional] 
**region** | **str** | State or province of the shipping address. | [optional] 
**postal_code** | **str** | Postal or ZIP code of the shipping address. | [optional] 
**country** | **str** | ISO 3166-1 alpha-2 country code. | [optional] 
**address_first_used_date** | **str** | Date this shipping address was first used. Format YYYYMMDD. | [optional] 
**address_first_used_indicator** | **str** | Address age: 01 &#x3D; first time, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**is_shipping_name_match** | **bool** | True if the shipping name matches the cardholder name. | [optional] 
**delivery_email_address** | **str** | Email address for electronic/digital delivery. | [optional] 
**delivery_timeframe_indicator** | **str** | Delivery timeframe: 01 &#x3D; electronic, 02 &#x3D; same day, 03 &#x3D; next day, 04 &#x3D; 2+ days. | [optional] 
**shipping_first_name** | **str** | First name of the shipping recipient. | [optional] 
**shipping_last_name** | **str** | Last name of the shipping recipient. | [optional] 
**shipping_phone** | **str** | Phone number of the shipping recipient. Digits only. | [optional] 
**shipping_address_count** | **int** | Number of shipping addresses on the customer&#39;s merchant account. | [optional] 
**days_since_ship_to_address_change** | **int** | Days between the last ship-to-address change and the purchase date. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_shipping_data import RtnDataShippingData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataShippingData from a JSON string
rtn_data_shipping_data_instance = RtnDataShippingData.from_json(json)
# print the JSON string representation of the object
print(RtnDataShippingData.to_json())

# convert the object into a dict
rtn_data_shipping_data_dict = rtn_data_shipping_data_instance.to_dict()
# create an instance of RtnDataShippingData from a dict
rtn_data_shipping_data_from_dict = RtnDataShippingData.from_dict(rtn_data_shipping_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


