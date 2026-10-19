# ThreeDSContext

Shopper device and browser context (RFC-068). Optional. Values are passed through unchanged to the payment gateway layer, which uses only what the routed gateway supports. Sending this block never changes the authorization. Backbone does not store the block; the only part it records is the channel, reduced to one of BROWSER, MOBILE_APP, SDK, POS or OTHER (any other value is recorded as OTHER), on the transaction's 3DS context usage treatment record.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel** | **str** | Interaction channel: BROWSER, MOBILE_APP, SDK, POS or OTHER. Passed to the gateway unchanged; recorded on the 3DS context usage treatment record as one of those five values, matched case-insensitively, with any other value recorded as OTHER. | [optional] 
**user_agent** | **str** | Browser user agent. | [optional] 
**accept_header** | **str** | Browser HTTP Accept header. | [optional] 
**browser_language** | **str** | Browser language (IETF BCP 47). | [optional] 
**color_depth** | **int** | Screen colour depth in bits. | [optional] 
**screen_height** | **int** | Screen height in pixels. | [optional] 
**screen_width** | **int** | Screen width in pixels. | [optional] 
**timezone_offset_minutes** | **int** | Browser UTC offset in minutes. | [optional] 
**is_java_enabled** | **bool** | Whether the browser has Java enabled. | [optional] 
**is_javascript_enabled** | **bool** | Whether the browser has JavaScript enabled. | [optional] 
**device_id** | **str** | Merchant or RTN device identifier. | [optional] 
**device_fingerprint** | **str** | Opaque fingerprint produced by the routed gateway&#39;s client-side script. | [optional] 

## Example

```python
from revaly_sdk_core.models.three_ds_context import ThreeDSContext

# TODO update the JSON string below
json = "{}"
# create an instance of ThreeDSContext from a JSON string
three_ds_context_instance = ThreeDSContext.from_json(json)
# print the JSON string representation of the object
print(ThreeDSContext.to_json())

# convert the object into a dict
three_ds_context_dict = three_ds_context_instance.to_dict()
# create an instance of ThreeDSContext from a dict
three_ds_context_from_dict = ThreeDSContext.from_dict(three_ds_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


