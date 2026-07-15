# RtnDataDeviceData

Device and IP signals. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ip_address** | **str** | IPv4 or IPv6 address of the device. | [optional] 
**city** | **str** | City derived from IP geolocation. | [optional] 
**region** | **str** | State or province derived from IP geolocation. | [optional] 
**country** | **str** | ISO 3166-1 alpha-2 country code from IP geolocation. | [optional] 
**device_id** | **str** | Device identifier or fingerprint token. | [optional] 
**is_javascript_enabled** | **bool** | True if JavaScript is enabled in the device browser. | [optional] 
**is_java_enabled** | **bool** | True if Java is enabled in the device browser. | [optional] 
**user_agent** | **str** | Browser User-Agent string. | [optional] 
**timezone** | **str** | IANA timezone identifier. | [optional] 
**timezone_offset_minutes** | **int** | UTC offset in minutes (negative for west of UTC). | [optional] 
**browser_language** | **str** | IETF BCP 47 language tag. | [optional] 
**device_longitude** | **str** | Device longitude in decimal degrees. West is negative. | [optional] 
**device_latitude** | **str** | Device latitude in decimal degrees. South is negative. | [optional] 
**channel** | **str** | Application channel through which the transaction was initiated. | [optional] 
**digital_wallet_provider_id** | **str** | Digital wallet provider identifier. | [optional] 
**is_device_fraud_associated** | **bool** | True if the device has a history of fraudulent transactions. | [optional] 
**is_known_device** | **bool** | True if the device has been seen before for this customer. | [optional] 
**device_type** | **str** | Hardware form factor, distinct from channel: 01 &#x3D; Phone, 02 &#x3D; Tablet, 03 &#x3D; Computer, 04 &#x3D; Other. | [optional] 
**browser_timezone_offset** | **str** | Browser timezone offset as a string. String companion to timezoneOffsetMinutes for producers/FIs that exchange it as a string. | [optional] 
**session_cookie** | **str** | Cookie associated with the purchaser&#39;s session. | [optional] 
**purchase_host_name** | **str** | Host name of the server where the customer placed the purchase. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_device_data import RtnDataDeviceData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataDeviceData from a JSON string
rtn_data_device_data_instance = RtnDataDeviceData.from_json(json)
# print the JSON string representation of the object
print(RtnDataDeviceData.to_json())

# convert the object into a dict
rtn_data_device_data_dict = rtn_data_device_data_instance.to_dict()
# create an instance of RtnDataDeviceData from a dict
rtn_data_device_data_from_dict = RtnDataDeviceData.from_dict(rtn_data_device_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


