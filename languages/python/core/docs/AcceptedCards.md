# AcceptedCards

Configuration for accepted card types and their features

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**visa** | [**CardFeatures**](CardFeatures.md) |  | [optional] 
**master_card** | [**CardFeatures**](CardFeatures.md) |  | [optional] 
**amex** | [**CardFeatures**](CardFeatures.md) |  | [optional] 
**discover** | [**CardFeatures**](CardFeatures.md) |  | [optional] 
**diners_club** | [**CardFeatures**](CardFeatures.md) |  | [optional] 
**jcb** | [**CardFeatures**](CardFeatures.md) |  | [optional] 
**maestro** | [**CardFeatures**](CardFeatures.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.accepted_cards import AcceptedCards

# TODO update the JSON string below
json = "{}"
# create an instance of AcceptedCards from a JSON string
accepted_cards_instance = AcceptedCards.from_json(json)
# print the JSON string representation of the object
print(AcceptedCards.to_json())

# convert the object into a dict
accepted_cards_dict = accepted_cards_instance.to_dict()
# create an instance of AcceptedCards from a dict
accepted_cards_from_dict = AcceptedCards.from_dict(accepted_cards_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


