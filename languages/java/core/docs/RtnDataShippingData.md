

# RtnDataShippingData

Shipping address and delivery signals. All fields optional.

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**shippingIndicator** | [**ShippingIndicatorEnum**](#ShippingIndicatorEnum) | Relationship between billing and shipping address: 01 &#x3D; Same as billing, 02 &#x3D; Different (verified), 03 &#x3D; Different (unverified), 04 &#x3D; Retail store pickup, 05 &#x3D; Digital delivery, 06 &#x3D; Not shipped, 07 &#x3D; Other. |  [optional] |
|**addressLine1** | **String** | First line of the shipping address. |  [optional] |
|**addressLine2** | **String** | Second line of the shipping address. |  [optional] |
|**addressLine3** | **String** | Third line of the shipping address. |  [optional] |
|**city** | **String** | City of the shipping address. |  [optional] |
|**region** | **String** | State or province of the shipping address. |  [optional] |
|**postalCode** | **String** | Postal or ZIP code of the shipping address. |  [optional] |
|**country** | **String** | ISO 3166-1 alpha-2 country code. |  [optional] |
|**addressFirstUsedDate** | **String** | Date this shipping address was first used. Format YYYYMMDD. |  [optional] |
|**addressFirstUsedIndicator** | [**AddressFirstUsedIndicatorEnum**](#AddressFirstUsedIndicatorEnum) | Address age: 01 &#x3D; first time, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. |  [optional] |
|**isShippingNameMatch** | **Boolean** | True if the shipping name matches the cardholder name. |  [optional] |
|**deliveryEmailAddress** | **String** | Email address for electronic/digital delivery. |  [optional] |
|**deliveryTimeframeIndicator** | [**DeliveryTimeframeIndicatorEnum**](#DeliveryTimeframeIndicatorEnum) | Delivery timeframe: 01 &#x3D; electronic, 02 &#x3D; same day, 03 &#x3D; next day, 04 &#x3D; 2+ days. |  [optional] |
|**shippingFirstName** | **String** | First name of the shipping recipient. |  [optional] |
|**shippingLastName** | **String** | Last name of the shipping recipient. |  [optional] |
|**shippingPhone** | **String** | Phone number of the shipping recipient. Digits only. |  [optional] |
|**shippingAddressCount** | **Integer** | Number of shipping addresses on the customer&#39;s merchant account. |  [optional] |
|**daysSinceShipToAddressChange** | **Integer** | Days between the last ship-to-address change and the purchase date. |  [optional] |



## Enum: ShippingIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| _05 | &quot;05&quot; |
| _06 | &quot;06&quot; |
| _07 | &quot;07&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: AddressFirstUsedIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: DeliveryTimeframeIndicatorEnum

| Name | Value |
|---- | -----|
| _01 | &quot;01&quot; |
| _02 | &quot;02&quot; |
| _03 | &quot;03&quot; |
| _04 | &quot;04&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



