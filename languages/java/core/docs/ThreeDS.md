

# ThreeDS

3D Secure authentication data for payment processing

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**version** | **String** | 3DS protocol version used for the auth result. |  [optional] |
|**exemptionType** | **String** | Requested/declared SCA exemption routed to the gateway (e.g., &#39;moto&#39;, &#39;low_value&#39;). |  [optional] |
|**eci** | **String** | Electronic Commerce Indicator (scheme-specific). Visa: 05/06/07, MC: 02/01/00. |  [optional] |
|**cryptogram** | **String** | Cardholder Authentication Verification Value (CAVV/AVV/UCAF cryptogram). Base64 of a 20-byte value (28 chars). |  [optional] |
|**dsTransactionId** | **UUID** | Directory Server transaction ID (UUID, 36 chars). |  [optional] |
|**acsTransactionId** | **UUID** | ACS (issuer) transaction ID (UUID, 36 chars). |  [optional] |
|**xid** | **String** | Authentication transaction ID (legacy 3DS1, Base64 of 20 bytes, 28 chars). |  [optional] |
|**cavvAlgorithm** | **String** | Algorithm used to generate the cryptogram. Often &#39;1&#39;. |  [optional] |
|**directoryStatus** | [**DirectoryStatusEnum**](#DirectoryStatusEnum) | Directory Server response status (TransStatus). Typical: Y, N, U, A, R. |  [optional] |
|**authenticationStatus** | [**AuthenticationStatusEnum**](#AuthenticationStatusEnum) | Final cardholder authentication status from ACS/3DS Server (TransStatus). Typical: Y, N, U, A, R. |  [optional] |
|**enrolledStatus** | [**EnrolledStatusEnum**](#EnrolledStatusEnum) | Enrollment status (legacy 3DS1, Verify Enrollment Response). Typical: Y, N, U. |  [optional] |
|**serverTransId** | **UUID** | 3DS Server transaction ID (UUID, 36 chars). |  [optional] |



## Enum: DirectoryStatusEnum

| Name | Value |
|---- | -----|
| Y | &quot;Y&quot; |
| N | &quot;N&quot; |
| U | &quot;U&quot; |
| A | &quot;A&quot; |
| R | &quot;R&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: AuthenticationStatusEnum

| Name | Value |
|---- | -----|
| Y | &quot;Y&quot; |
| N | &quot;N&quot; |
| U | &quot;U&quot; |
| A | &quot;A&quot; |
| R | &quot;R&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



## Enum: EnrolledStatusEnum

| Name | Value |
|---- | -----|
| Y | &quot;Y&quot; |
| N | &quot;N&quot; |
| U | &quot;U&quot; |
| UNKNOWN_DEFAULT_OPEN_API | &quot;unknown_default_open_api&quot; |



