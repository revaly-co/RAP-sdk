

# ThreeDSContext

Shopper device and browser context (RFC-068). Optional. Values are passed through unchanged to the payment gateway layer, which uses only what the routed gateway supports. Sending this block never changes the authorization. Backbone does not store the block; the only part it records is the channel, reduced to one of BROWSER, MOBILE_APP, SDK, POS or OTHER (any other value is recorded as OTHER), on the transaction's 3DS context usage treatment record.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**channel** | **String** | Interaction channel: BROWSER, MOBILE_APP, SDK, POS or OTHER. Passed to the gateway unchanged; recorded on the 3DS context usage treatment record as one of those five values, matched case-insensitively, with any other value recorded as OTHER. |  [optional] |
|**userAgent** | **String** | Browser user agent. |  [optional] |
|**acceptHeader** | **String** | Browser HTTP Accept header. |  [optional] |
|**browserLanguage** | **String** | Browser language (IETF BCP 47). |  [optional] |
|**colorDepth** | **Integer** | Screen colour depth in bits. |  [optional] |
|**screenHeight** | **Integer** | Screen height in pixels. |  [optional] |
|**screenWidth** | **Integer** | Screen width in pixels. |  [optional] |
|**timezoneOffsetMinutes** | **Integer** | Browser UTC offset in minutes. |  [optional] |
|**isJavaEnabled** | **Boolean** | Whether the browser has Java enabled. |  [optional] |
|**isJavascriptEnabled** | **Boolean** | Whether the browser has JavaScript enabled. |  [optional] |
|**deviceId** | **String** | Merchant or RTN device identifier. |  [optional] |
|**deviceFingerprint** | **String** | Opaque fingerprint produced by the routed gateway&#39;s client-side script. |  [optional] |



