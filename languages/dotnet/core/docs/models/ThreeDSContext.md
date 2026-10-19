# Revaly.Sdk.Core.Model.ThreeDSContext
Shopper device and browser context (RFC-068). Optional. Values are passed through unchanged to the payment gateway layer, which uses only what the routed gateway supports. Sending this block never changes the authorization. Backbone does not store the block; the only part it records is the channel, reduced to one of BROWSER, MOBILE_APP, SDK, POS or OTHER (any other value is recorded as OTHER), on the transaction's 3DS context usage treatment record.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Channel** | **string** | Interaction channel: BROWSER, MOBILE_APP, SDK, POS or OTHER. Passed to the gateway unchanged; recorded on the 3DS context usage treatment record as one of those five values, matched case-insensitively, with any other value recorded as OTHER. | [optional] 
**UserAgent** | **string** | Browser user agent. | [optional] 
**AcceptHeader** | **string** | Browser HTTP Accept header. | [optional] 
**BrowserLanguage** | **string** | Browser language (IETF BCP 47). | [optional] 
**ColorDepth** | **int** | Screen colour depth in bits. | [optional] 
**ScreenHeight** | **int** | Screen height in pixels. | [optional] 
**ScreenWidth** | **int** | Screen width in pixels. | [optional] 
**TimezoneOffsetMinutes** | **int** | Browser UTC offset in minutes. | [optional] 
**IsJavaEnabled** | **bool** | Whether the browser has Java enabled. | [optional] 
**IsJavascriptEnabled** | **bool** | Whether the browser has JavaScript enabled. | [optional] 
**DeviceId** | **string** | Merchant or RTN device identifier. | [optional] 
**DeviceFingerprint** | **string** | Opaque fingerprint produced by the routed gateway&#39;s client-side script. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

