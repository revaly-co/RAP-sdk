# RtnDataCustomerData

Customer account and profile signals. All fields optional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**first_name** | **str** | Customer first name. | [optional] 
**last_name** | **str** | Customer last name. | [optional] 
**email** | **str** | Customer email address. | [optional] 
**home_phone** | **str** | Home phone number. Digits only, no formatting. | [optional] 
**mobile_phone** | **str** | Mobile phone number. Digits only, no formatting. | [optional] 
**work_phone** | **str** | Work phone number. Digits only, no formatting. | [optional] 
**account_opened_date** | **str** | Account creation date. Format YYYYMMDD. | [optional] 
**account_age_indicator** | **str** | Account age token: 01 &#x3D; created during transaction, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**is_free_account** | **bool** | True if the customer account is a free (non-paying) account. | [optional] 
**account_last_changed_date** | **str** | Last account modification date. Format YYYYMMDD. | [optional] 
**account_change_indicator** | **str** | Account change age token: 01 &#x3D; during transaction, 02 &#x3D; &lt;30 days, 03 &#x3D; 30–60 days, 04 &#x3D; &gt;60 days. | [optional] 
**password_last_changed_date** | **str** | Last password change date. Format YYYYMMDD. | [optional] 
**password_change_indicator** | **str** | Password change age: 01 &#x3D; never reset, 02 &#x3D; during transaction, 03 &#x3D; &lt;30 days, 04 &#x3D; 30–60 days, 05 &#x3D; &gt;60 days. | [optional] 
**transaction_successful_count_last_six_months** | **int** | Count of successful purchases in the past 6 months. | [optional] 
**transaction_attempted_count_last24_hours** | **int** | Count of transaction attempts in the past 24 hours. | [optional] 
**transaction_attempted_count_last_year** | **int** | Count of transaction attempts in the past year. | [optional] 
**payment_method_added_date** | **str** | Date payment method was added. Format YYYYMMDD. | [optional] 
**payment_method_age_indicator** | **str** | Payment method age token. | [optional] 
**payment_method_add_attempt_count_last24_hours** | **int** | Number of payment method add attempts in the past 24 hours. | [optional] 
**is_payment_method_on_file** | **bool** | True if the payment method is stored on file for the customer. | [optional] 
**is_account_suspicious** | **bool** | True if the merchant considers the account suspicious. | [optional] 
**customer_id** | **str** | Merchant&#39;s internal customer identifier. | [optional] 
**account_authentication_method** | **str** | Method used to authenticate the customer for this session. | [optional] 
**is_tenured_customer** | **bool** | True if the customer has a long-standing, established account relationship. | [optional] 
**is_email_known_to_customer** | **bool** | True if the email address on file is associated with a known customer account. | [optional] 
**is_registered_customer** | **str** | Whether the purchaser is a registered member (Y) or guest (N). | [optional] 
**is_registration_updated** | **str** | Whether any registration information changed since account creation. | [optional] 
**registered_account_tenure** | **int** | Number of days the customer has been registered with the merchant. | [optional] 
**registered_name** | **str** | Customer name as registered with the merchant. | [optional] 
**registered_email** | **str** | Registered email address with the merchant. | [optional] 
**registered_postal_code** | **str** | Registered postal code with the merchant. | [optional] 
**registered_address** | **str** | Registered address with the merchant (no city/state). | [optional] 
**registered_phone** | **str** | Registered phone number. Digits only. | [optional] 
**days_since_name_change** | **int** | Days between the last registered-name change and the purchase date. | [optional] 
**days_since_email_change** | **int** | Days between the last registered-email change and the purchase date. | [optional] 
**days_since_password_change** | **int** | Days between the last password change and the purchase date. | [optional] 
**days_since_postal_code_change** | **int** | Days between the last registered-postal-code change and the purchase date. | [optional] 
**days_since_address_change** | **int** | Days between the last registered-address change and the purchase date. | [optional] 
**days_since_phone_change** | **int** | Days between the last registered-phone change and the purchase date. | [optional] 
**days_since_ship_to_name_change** | **int** | Days between the last ship-to-name change and the purchase date. | [optional] 
**customer_ani** | **str** | ANI 10-digit phone number used to place a phone order. Digits only. | [optional] 
**customer_ani_digits** | **str** | ANI Information Identifier (II) digits: e.g. cellular &#x3D; 61–63, payphone &#x3D; 27, toll-free &#x3D; 24/25. | [optional] 
**is_email_associated_with_fraud** | **bool** | True if the email has been associated with confirmed/suspected fraud (distinct from isAccountSuspicious). Carrier for BofA emailAssociatedWithFraudFlag. | [optional] 

## Example

```python
from revaly_sdk_core.models.rtn_data_customer_data import RtnDataCustomerData

# TODO update the JSON string below
json = "{}"
# create an instance of RtnDataCustomerData from a JSON string
rtn_data_customer_data_instance = RtnDataCustomerData.from_json(json)
# print the JSON string representation of the object
print(RtnDataCustomerData.to_json())

# convert the object into a dict
rtn_data_customer_data_dict = rtn_data_customer_data_instance.to_dict()
# create an instance of RtnDataCustomerData from a dict
rtn_data_customer_data_from_dict = RtnDataCustomerData.from_dict(rtn_data_customer_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


