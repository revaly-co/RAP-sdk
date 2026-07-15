# CardFeatures

Features and acceptance configuration for a specific card type

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accept_credit_card** | **bool** | Whether to accept credit cards of this type | [optional] 
**accept_prepaid_card** | **bool** | Whether to accept prepaid cards of this type | [optional] 
**accept_debit_card** | **bool** | Whether to accept debit cards of this type | [optional] 

## Example

```python
from revaly_sdk_core.models.card_features import CardFeatures

# TODO update the JSON string below
json = "{}"
# create an instance of CardFeatures from a JSON string
card_features_instance = CardFeatures.from_json(json)
# print the JSON string representation of the object
print(CardFeatures.to_json())

# convert the object into a dict
card_features_dict = card_features_instance.to_dict()
# create an instance of CardFeatures from a dict
card_features_from_dict = CardFeatures.from_dict(card_features_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


