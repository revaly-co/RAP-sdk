# ThreeDSContext

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel** | **string** | Interaction channel: BROWSER, MOBILE_APP, SDK, POS or OTHER. Passed to the gateway unchanged; recorded on the 3DS context usage treatment record as one of those five values, matched case-insensitively, with any other value recorded as OTHER. | [optional]
**user_agent** | **string** | Browser user agent. | [optional]
**accept_header** | **string** | Browser HTTP Accept header. | [optional]
**browser_language** | **string** | Browser language (IETF BCP 47). | [optional]
**color_depth** | **int** | Screen colour depth in bits. | [optional]
**screen_height** | **int** | Screen height in pixels. | [optional]
**screen_width** | **int** | Screen width in pixels. | [optional]
**timezone_offset_minutes** | **int** | Browser UTC offset in minutes. | [optional]
**is_java_enabled** | **bool** | Whether the browser has Java enabled. | [optional]
**is_javascript_enabled** | **bool** | Whether the browser has JavaScript enabled. | [optional]
**device_id** | **string** | Merchant or RTN device identifier. | [optional]
**device_fingerprint** | **string** | Opaque fingerprint produced by the routed gateway&#39;s client-side script. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
