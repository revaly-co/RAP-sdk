# ThreeDS

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **string** | 3DS protocol version used for the auth result. | [optional]
**exemption_type** | **string** | Requested/declared SCA exemption routed to the gateway (e.g., &#39;moto&#39;, &#39;low_value&#39;). | [optional]
**eci** | **string** | Electronic Commerce Indicator (scheme-specific). Visa: 05/06/07, MC: 02/01/00. | [optional]
**cryptogram** | **string** | Cardholder Authentication Verification Value (CAVV/AVV/UCAF cryptogram). Base64 of a 20-byte value (28 chars). | [optional]
**ds_transaction_id** | **string** | Directory Server transaction ID (UUID, 36 chars). | [optional]
**acs_transaction_id** | **string** | ACS (issuer) transaction ID (UUID, 36 chars). | [optional]
**xid** | **string** | Authentication transaction ID (legacy 3DS1, Base64 of 20 bytes, 28 chars). | [optional]
**cavv_algorithm** | **string** | Algorithm used to generate the cryptogram. Often &#39;1&#39;. | [optional]
**directory_status** | **string** | Directory Server response status (TransStatus). Typical: Y, N, U, A, R. | [optional]
**authentication_status** | **string** | Final cardholder authentication status from ACS/3DS Server (TransStatus). Typical: Y, N, U, A, R. | [optional]
**enrolled_status** | **string** | Enrollment status (legacy 3DS1, Verify Enrollment Response). Typical: Y, N, U. | [optional]
**server_trans_id** | **string** | 3DS Server transaction ID (UUID, 36 chars). | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
