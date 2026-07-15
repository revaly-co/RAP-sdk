# RtnDataSellerData

Seller details for marketplace or platform transactions where the client submits on behalf of a third-party seller (maps to Amex seller_information). All fields optional; omit rather than send nulls.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_id** | **str** | The client&#39;s identifier for the seller. | [optional] 
**seller_business_name** | **str** | Business name of the seller. | [optional] 
**seller_owner_name** | **str** | Name of the seller or the seller&#39;s owner. | [optional] 
**seller_tenure** | **int** | Number of months the seller has used the client&#39;s services. | [optional] 
**seller_latitude** | **str** | Latitude (decimal degrees) where the purchase was made — seller location, not the cardholder device. | [optional] 
**seller_longitude** | **str** | Longitude (decimal degrees) where the purchase was made — seller location. | [optional] 
**seller_address** | **str** | Business or contact address of the seller. | [optional] 
**seller_phone** | **str** | Primary phone number of the seller. | [optional] 
**seller_email** | **str** | Primary email address of the seller. | [optional] 
**seller_postal_code** | **str** | Postal code of the seller&#39;s primary address. | [optional] 
**seller_region** | **str** | Seller region. APA&#x3D;Asia Pacific &amp; Australia; EMEA&#x3D;Europe/Middle East/Africa; LA/C&#x3D;Latin America &amp; Caribbean. | [optional] 
**seller_country_code** | **str** | Country of the seller, ISO 3166-1 numeric code as a string. | [optional] 
**transaction_type_indicator** | **str** | Seller transaction classification. P2P&#x3D;Person to Person; P2M&#x3D;Person to Merchant; CSH&#x3D;Cash. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_seller_data import RtnDataSellerData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataSellerData from a JSON string
rtn_data_seller_data_instance = RtnDataSellerData.from_json(json)
# print the JSON string representation of the object
print(RtnDataSellerData.to_json())

# convert the object into a dict
rtn_data_seller_data_dict = rtn_data_seller_data_instance.to_dict()
# create an instance of RtnDataSellerData from a dict
rtn_data_seller_data_from_dict = RtnDataSellerData.from_dict(rtn_data_seller_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


