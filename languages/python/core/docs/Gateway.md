# Gateway

Gateway configuration and settings

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Gateway name | [optional] 
**bank_type_code** | **str** | Bank type code | [optional] 
**merchant_account_reference_id** | **str** | Merchant account reference ID at the gateway | [optional] 
**gateway_type** | **str** | Type of payment gateway | [optional] 
**currency_code** | **str** | Primary currency code for this gateway | [optional] 
**accepted_currency_codes** | **List[str]** | List of accepted currency codes | [optional] 
**accepted_cards** | [**AcceptedCards**](AcceptedCards.md) |  | [optional] 
**accept_retries** | **bool** | Whether the gateway accepts retry transactions | [optional] 
**cvv_required** | **bool** | Whether CVV is required for transactions | [optional] 
**approved_charge_or_capture_rate_fee** | **float** | Rate fee for approved charges or captures | [optional] 
**approved_charge_or_capture_flat_fee** | **float** | Flat fee for approved charges or captures | [optional] 
**other_transaction_flat_fee** | **float** | Flat fee for other transaction types | [optional] 
**issue_refunds_through_credit** | **bool** | Whether refunds are issued through credit | [optional] 

## Example

```python
from revaly_sdk_core.models.gateway import Gateway

# TODO update the JSON string below
json = "{}"
# create an instance of Gateway from a JSON string
gateway_instance = Gateway.from_json(json)
# print the JSON string representation of the object
print(Gateway.to_json())

# convert the object into a dict
gateway_dict = gateway_instance.to_dict()
# create an instance of Gateway from a dict
gateway_from_dict = Gateway.from_dict(gateway_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


