# Revaly.Sdk.Core.Model.ThreeDS
3D Secure authentication data for payment processing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**VarVersion** | **string** | 3DS protocol version used for the auth result. | [optional] 
**ExemptionType** | **string** | Requested/declared SCA exemption routed to the gateway (e.g., &#39;moto&#39;, &#39;low_value&#39;). | [optional] 
**Eci** | **string** | Electronic Commerce Indicator (scheme-specific). Visa: 05/06/07, MC: 02/01/00. | [optional] 
**Cryptogram** | **string** | Cardholder Authentication Verification Value (CAVV/AVV/UCAF cryptogram). Base64 of a 20-byte value (28 chars). | [optional] 
**DsTransactionId** | **Guid** | Directory Server transaction ID (UUID, 36 chars). | [optional] 
**AcsTransactionId** | **Guid** | ACS (issuer) transaction ID (UUID, 36 chars). | [optional] 
**Xid** | **string** | Authentication transaction ID (legacy 3DS1, Base64 of 20 bytes, 28 chars). | [optional] 
**CavvAlgorithm** | **string** | Algorithm used to generate the cryptogram. Often &#39;1&#39;. | [optional] 
**DirectoryStatus** | **string** | Directory Server response status (TransStatus). Typical: Y, N, U, A, R. | [optional] 
**AuthenticationStatus** | **string** | Final cardholder authentication status from ACS/3DS Server (TransStatus). Typical: Y, N, U, A, R. | [optional] 
**EnrolledStatus** | **string** | Enrollment status (legacy 3DS1, Verify Enrollment Response). Typical: Y, N, U. | [optional] 
**ServerTransId** | **Guid** | 3DS Server transaction ID (UUID, 36 chars). | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

