# ThreeDS

3D Secure authentication data for payment processing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **str** | 3DS protocol version used for the auth result. | [optional] 
**exemption_type** | **str** | Requested/declared SCA exemption routed to the gateway (e.g., &#39;moto&#39;, &#39;low_value&#39;). | [optional] 
**eci** | **str** | Electronic Commerce Indicator (scheme-specific). Visa: 05/06/07, MC: 02/01/00. | [optional] 
**cryptogram** | **str** | Cardholder Authentication Verification Value (CAVV/AVV/UCAF cryptogram). Base64 of a 20-byte value (28 chars). | [optional] 
**ds_transaction_id** | **UUID** | Directory Server transaction ID (UUID, 36 chars). | [optional] 
**acs_transaction_id** | **UUID** | ACS (issuer) transaction ID (UUID, 36 chars). | [optional] 
**xid** | **str** | Authentication transaction ID (legacy 3DS1, Base64 of 20 bytes, 28 chars). | [optional] 
**cavv_algorithm** | **str** | Algorithm used to generate the cryptogram. Often &#39;1&#39;. | [optional] 
**directory_status** | **str** | Directory Server response status (TransStatus). Typical: Y, N, U, A, R. | [optional] 
**authentication_status** | **str** | Final cardholder authentication status from ACS/3DS Server (TransStatus). Typical: Y, N, U, A, R. | [optional] 
**enrolled_status** | **str** | Enrollment status (legacy 3DS1, Verify Enrollment Response). Typical: Y, N, U. | [optional] 
**server_trans_id** | **UUID** | 3DS Server transaction ID (UUID, 36 chars). | [optional] 

## Example

```python
from revaly_sdk_core.models.three_ds import ThreeDS

# TODO update the JSON string below
json = "{}"
# create an instance of ThreeDS from a JSON string
three_ds_instance = ThreeDS.from_json(json)
# print the JSON string representation of the object
print(ThreeDS.to_json())

# convert the object into a dict
three_ds_dict = three_ds_instance.to_dict()
# create an instance of ThreeDS from a dict
three_ds_from_dict = ThreeDS.from_dict(three_ds_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


