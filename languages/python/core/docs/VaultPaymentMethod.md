# VaultPaymentMethod

Vault-issued payment token details for payment processing

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vault_token** | **str** | Vault-issued token (any provider) used to authorize a payment. Valid only on &#x60;/payments/charge&#x60; and &#x60;/payments/authorize&#x60; when &#x60;paymentMethodType&#x60; is &#x60;vaultToken&#x60;. Requires &#x60;paymentMethod.merchantAccountReferenceId&#x60; for gateway routing. Must not be combined with &#x60;creditCard&#x60; or &#x60;gatewayPaymentMethod&#x60;.  | [optional] 
**bin** | **str** | Bank Identification Number (first 6 or 8 digits) | [optional] 
**last_four_digits** | **str** | Last four digits of the payment method | [optional] 
**expiry_year** | **str** | Expiration year (YYYY) | [optional] 
**expiry_month** | **str** | Expiration month (01-12) | [optional] 

## Example

```python
from revaly_sdk_core.models.vault_payment_method import VaultPaymentMethod

# TODO update the JSON string below
json = "{}"
# create an instance of VaultPaymentMethod from a JSON string
vault_payment_method_instance = VaultPaymentMethod.from_json(json)
# print the JSON string representation of the object
print(VaultPaymentMethod.to_json())

# convert the object into a dict
vault_payment_method_dict = vault_payment_method_instance.to_dict()
# create an instance of VaultPaymentMethod from a dict
vault_payment_method_from_dict = VaultPaymentMethod.from_dict(vault_payment_method_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


