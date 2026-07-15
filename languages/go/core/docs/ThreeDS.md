# ThreeDS

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Version** | Pointer to **NullableString** | 3DS protocol version used for the auth result. | [optional] 
**ExemptionType** | Pointer to **NullableString** | Requested/declared SCA exemption routed to the gateway (e.g., &#39;moto&#39;, &#39;low_value&#39;). | [optional] 
**Eci** | Pointer to **NullableString** | Electronic Commerce Indicator (scheme-specific). Visa: 05/06/07, MC: 02/01/00. | [optional] 
**Cryptogram** | Pointer to **NullableString** | Cardholder Authentication Verification Value (CAVV/AVV/UCAF cryptogram). Base64 of a 20-byte value (28 chars). | [optional] 
**DsTransactionId** | Pointer to **NullableString** | Directory Server transaction ID (UUID, 36 chars). | [optional] 
**AcsTransactionId** | Pointer to **NullableString** | ACS (issuer) transaction ID (UUID, 36 chars). | [optional] 
**Xid** | Pointer to **NullableString** | Authentication transaction ID (legacy 3DS1, Base64 of 20 bytes, 28 chars). | [optional] 
**CavvAlgorithm** | Pointer to **NullableString** | Algorithm used to generate the cryptogram. Often &#39;1&#39;. | [optional] 
**DirectoryStatus** | Pointer to **NullableString** | Directory Server response status (TransStatus). Typical: Y, N, U, A, R. | [optional] 
**AuthenticationStatus** | Pointer to **NullableString** | Final cardholder authentication status from ACS/3DS Server (TransStatus). Typical: Y, N, U, A, R. | [optional] 
**EnrolledStatus** | Pointer to **NullableString** | Enrollment status (legacy 3DS1, Verify Enrollment Response). Typical: Y, N, U. | [optional] 
**ServerTransId** | Pointer to **NullableString** | 3DS Server transaction ID (UUID, 36 chars). | [optional] 

## Methods

### NewThreeDS

`func NewThreeDS() *ThreeDS`

NewThreeDS instantiates a new ThreeDS object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewThreeDSWithDefaults

`func NewThreeDSWithDefaults() *ThreeDS`

NewThreeDSWithDefaults instantiates a new ThreeDS object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetVersion

`func (o *ThreeDS) GetVersion() string`

GetVersion returns the Version field if non-nil, zero value otherwise.

### GetVersionOk

`func (o *ThreeDS) GetVersionOk() (*string, bool)`

GetVersionOk returns a tuple with the Version field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetVersion

`func (o *ThreeDS) SetVersion(v string)`

SetVersion sets Version field to given value.

### HasVersion

`func (o *ThreeDS) HasVersion() bool`

HasVersion returns a boolean if a field has been set.

### SetVersionNil

`func (o *ThreeDS) SetVersionNil(b bool)`

 SetVersionNil sets the value for Version to be an explicit nil

### UnsetVersion
`func (o *ThreeDS) UnsetVersion()`

UnsetVersion ensures that no value is present for Version, not even an explicit nil
### GetExemptionType

`func (o *ThreeDS) GetExemptionType() string`

GetExemptionType returns the ExemptionType field if non-nil, zero value otherwise.

### GetExemptionTypeOk

`func (o *ThreeDS) GetExemptionTypeOk() (*string, bool)`

GetExemptionTypeOk returns a tuple with the ExemptionType field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetExemptionType

`func (o *ThreeDS) SetExemptionType(v string)`

SetExemptionType sets ExemptionType field to given value.

### HasExemptionType

`func (o *ThreeDS) HasExemptionType() bool`

HasExemptionType returns a boolean if a field has been set.

### SetExemptionTypeNil

`func (o *ThreeDS) SetExemptionTypeNil(b bool)`

 SetExemptionTypeNil sets the value for ExemptionType to be an explicit nil

### UnsetExemptionType
`func (o *ThreeDS) UnsetExemptionType()`

UnsetExemptionType ensures that no value is present for ExemptionType, not even an explicit nil
### GetEci

`func (o *ThreeDS) GetEci() string`

GetEci returns the Eci field if non-nil, zero value otherwise.

### GetEciOk

`func (o *ThreeDS) GetEciOk() (*string, bool)`

GetEciOk returns a tuple with the Eci field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEci

`func (o *ThreeDS) SetEci(v string)`

SetEci sets Eci field to given value.

### HasEci

`func (o *ThreeDS) HasEci() bool`

HasEci returns a boolean if a field has been set.

### SetEciNil

`func (o *ThreeDS) SetEciNil(b bool)`

 SetEciNil sets the value for Eci to be an explicit nil

### UnsetEci
`func (o *ThreeDS) UnsetEci()`

UnsetEci ensures that no value is present for Eci, not even an explicit nil
### GetCryptogram

`func (o *ThreeDS) GetCryptogram() string`

GetCryptogram returns the Cryptogram field if non-nil, zero value otherwise.

### GetCryptogramOk

`func (o *ThreeDS) GetCryptogramOk() (*string, bool)`

GetCryptogramOk returns a tuple with the Cryptogram field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCryptogram

`func (o *ThreeDS) SetCryptogram(v string)`

SetCryptogram sets Cryptogram field to given value.

### HasCryptogram

`func (o *ThreeDS) HasCryptogram() bool`

HasCryptogram returns a boolean if a field has been set.

### SetCryptogramNil

`func (o *ThreeDS) SetCryptogramNil(b bool)`

 SetCryptogramNil sets the value for Cryptogram to be an explicit nil

### UnsetCryptogram
`func (o *ThreeDS) UnsetCryptogram()`

UnsetCryptogram ensures that no value is present for Cryptogram, not even an explicit nil
### GetDsTransactionId

`func (o *ThreeDS) GetDsTransactionId() string`

GetDsTransactionId returns the DsTransactionId field if non-nil, zero value otherwise.

### GetDsTransactionIdOk

`func (o *ThreeDS) GetDsTransactionIdOk() (*string, bool)`

GetDsTransactionIdOk returns a tuple with the DsTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDsTransactionId

`func (o *ThreeDS) SetDsTransactionId(v string)`

SetDsTransactionId sets DsTransactionId field to given value.

### HasDsTransactionId

`func (o *ThreeDS) HasDsTransactionId() bool`

HasDsTransactionId returns a boolean if a field has been set.

### SetDsTransactionIdNil

`func (o *ThreeDS) SetDsTransactionIdNil(b bool)`

 SetDsTransactionIdNil sets the value for DsTransactionId to be an explicit nil

### UnsetDsTransactionId
`func (o *ThreeDS) UnsetDsTransactionId()`

UnsetDsTransactionId ensures that no value is present for DsTransactionId, not even an explicit nil
### GetAcsTransactionId

`func (o *ThreeDS) GetAcsTransactionId() string`

GetAcsTransactionId returns the AcsTransactionId field if non-nil, zero value otherwise.

### GetAcsTransactionIdOk

`func (o *ThreeDS) GetAcsTransactionIdOk() (*string, bool)`

GetAcsTransactionIdOk returns a tuple with the AcsTransactionId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAcsTransactionId

`func (o *ThreeDS) SetAcsTransactionId(v string)`

SetAcsTransactionId sets AcsTransactionId field to given value.

### HasAcsTransactionId

`func (o *ThreeDS) HasAcsTransactionId() bool`

HasAcsTransactionId returns a boolean if a field has been set.

### SetAcsTransactionIdNil

`func (o *ThreeDS) SetAcsTransactionIdNil(b bool)`

 SetAcsTransactionIdNil sets the value for AcsTransactionId to be an explicit nil

### UnsetAcsTransactionId
`func (o *ThreeDS) UnsetAcsTransactionId()`

UnsetAcsTransactionId ensures that no value is present for AcsTransactionId, not even an explicit nil
### GetXid

`func (o *ThreeDS) GetXid() string`

GetXid returns the Xid field if non-nil, zero value otherwise.

### GetXidOk

`func (o *ThreeDS) GetXidOk() (*string, bool)`

GetXidOk returns a tuple with the Xid field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetXid

`func (o *ThreeDS) SetXid(v string)`

SetXid sets Xid field to given value.

### HasXid

`func (o *ThreeDS) HasXid() bool`

HasXid returns a boolean if a field has been set.

### SetXidNil

`func (o *ThreeDS) SetXidNil(b bool)`

 SetXidNil sets the value for Xid to be an explicit nil

### UnsetXid
`func (o *ThreeDS) UnsetXid()`

UnsetXid ensures that no value is present for Xid, not even an explicit nil
### GetCavvAlgorithm

`func (o *ThreeDS) GetCavvAlgorithm() string`

GetCavvAlgorithm returns the CavvAlgorithm field if non-nil, zero value otherwise.

### GetCavvAlgorithmOk

`func (o *ThreeDS) GetCavvAlgorithmOk() (*string, bool)`

GetCavvAlgorithmOk returns a tuple with the CavvAlgorithm field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetCavvAlgorithm

`func (o *ThreeDS) SetCavvAlgorithm(v string)`

SetCavvAlgorithm sets CavvAlgorithm field to given value.

### HasCavvAlgorithm

`func (o *ThreeDS) HasCavvAlgorithm() bool`

HasCavvAlgorithm returns a boolean if a field has been set.

### SetCavvAlgorithmNil

`func (o *ThreeDS) SetCavvAlgorithmNil(b bool)`

 SetCavvAlgorithmNil sets the value for CavvAlgorithm to be an explicit nil

### UnsetCavvAlgorithm
`func (o *ThreeDS) UnsetCavvAlgorithm()`

UnsetCavvAlgorithm ensures that no value is present for CavvAlgorithm, not even an explicit nil
### GetDirectoryStatus

`func (o *ThreeDS) GetDirectoryStatus() string`

GetDirectoryStatus returns the DirectoryStatus field if non-nil, zero value otherwise.

### GetDirectoryStatusOk

`func (o *ThreeDS) GetDirectoryStatusOk() (*string, bool)`

GetDirectoryStatusOk returns a tuple with the DirectoryStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDirectoryStatus

`func (o *ThreeDS) SetDirectoryStatus(v string)`

SetDirectoryStatus sets DirectoryStatus field to given value.

### HasDirectoryStatus

`func (o *ThreeDS) HasDirectoryStatus() bool`

HasDirectoryStatus returns a boolean if a field has been set.

### SetDirectoryStatusNil

`func (o *ThreeDS) SetDirectoryStatusNil(b bool)`

 SetDirectoryStatusNil sets the value for DirectoryStatus to be an explicit nil

### UnsetDirectoryStatus
`func (o *ThreeDS) UnsetDirectoryStatus()`

UnsetDirectoryStatus ensures that no value is present for DirectoryStatus, not even an explicit nil
### GetAuthenticationStatus

`func (o *ThreeDS) GetAuthenticationStatus() string`

GetAuthenticationStatus returns the AuthenticationStatus field if non-nil, zero value otherwise.

### GetAuthenticationStatusOk

`func (o *ThreeDS) GetAuthenticationStatusOk() (*string, bool)`

GetAuthenticationStatusOk returns a tuple with the AuthenticationStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetAuthenticationStatus

`func (o *ThreeDS) SetAuthenticationStatus(v string)`

SetAuthenticationStatus sets AuthenticationStatus field to given value.

### HasAuthenticationStatus

`func (o *ThreeDS) HasAuthenticationStatus() bool`

HasAuthenticationStatus returns a boolean if a field has been set.

### SetAuthenticationStatusNil

`func (o *ThreeDS) SetAuthenticationStatusNil(b bool)`

 SetAuthenticationStatusNil sets the value for AuthenticationStatus to be an explicit nil

### UnsetAuthenticationStatus
`func (o *ThreeDS) UnsetAuthenticationStatus()`

UnsetAuthenticationStatus ensures that no value is present for AuthenticationStatus, not even an explicit nil
### GetEnrolledStatus

`func (o *ThreeDS) GetEnrolledStatus() string`

GetEnrolledStatus returns the EnrolledStatus field if non-nil, zero value otherwise.

### GetEnrolledStatusOk

`func (o *ThreeDS) GetEnrolledStatusOk() (*string, bool)`

GetEnrolledStatusOk returns a tuple with the EnrolledStatus field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetEnrolledStatus

`func (o *ThreeDS) SetEnrolledStatus(v string)`

SetEnrolledStatus sets EnrolledStatus field to given value.

### HasEnrolledStatus

`func (o *ThreeDS) HasEnrolledStatus() bool`

HasEnrolledStatus returns a boolean if a field has been set.

### SetEnrolledStatusNil

`func (o *ThreeDS) SetEnrolledStatusNil(b bool)`

 SetEnrolledStatusNil sets the value for EnrolledStatus to be an explicit nil

### UnsetEnrolledStatus
`func (o *ThreeDS) UnsetEnrolledStatus()`

UnsetEnrolledStatus ensures that no value is present for EnrolledStatus, not even an explicit nil
### GetServerTransId

`func (o *ThreeDS) GetServerTransId() string`

GetServerTransId returns the ServerTransId field if non-nil, zero value otherwise.

### GetServerTransIdOk

`func (o *ThreeDS) GetServerTransIdOk() (*string, bool)`

GetServerTransIdOk returns a tuple with the ServerTransId field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetServerTransId

`func (o *ThreeDS) SetServerTransId(v string)`

SetServerTransId sets ServerTransId field to given value.

### HasServerTransId

`func (o *ThreeDS) HasServerTransId() bool`

HasServerTransId returns a boolean if a field has been set.

### SetServerTransIdNil

`func (o *ThreeDS) SetServerTransIdNil(b bool)`

 SetServerTransIdNil sets the value for ServerTransId to be an explicit nil

### UnsetServerTransId
`func (o *ThreeDS) UnsetServerTransId()`

UnsetServerTransId ensures that no value is present for ServerTransId, not even an explicit nil

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


