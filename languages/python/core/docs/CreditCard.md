# CreditCard

Credit card details for payment processing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number** | **str** | Credit card number (will be tokenized) | 
**card_verification_code** | **str** | Card verification code (CVV/CVC) | [optional] 
**expiry_month** | **str** | Expiration month (01-12) | 
**expiry_year** | **str** | Expiration year (YYYY) | 
**company** | **str** | Card issuing company | [optional] 
**card_type** | **str** | Type of credit card | [optional] 

## Example

```python
from revaly_sdk_core.models.credit_card import CreditCard

# TODO update the JSON string below
json = "{}"
# create an instance of CreditCard from a JSON string
credit_card_instance = CreditCard.from_json(json)
# print the JSON string representation of the object
print(CreditCard.to_json())

# convert the object into a dict
credit_card_dict = credit_card_instance.to_dict()
# create an instance of CreditCard from a dict
credit_card_from_dict = CreditCard.from_dict(credit_card_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


