# PaymentMethod

Payment method details. Which fields are required depends on the payment-method type of the request: creditCard requires a cardholder name (fullName, or firstName together with lastName) plus creditCard.number/expiryMonth/expiryYear; gatewayPaymentMethodId requires gatewayPaymentMethod.gatewayPaymentMethodId and merchantAccountReferenceId; vaultToken requires vaultPaymentMethod.vaultToken plus the request-level customerId. When billing a stored payment method, supply paymentMethodId alone.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**first_name** | **str** | Customer&#39;s first name | [optional] 
**last_name** | **str** | Customer&#39;s last name | [optional] 
**full_name** | **str** | Customer&#39;s full name | [optional] 
**email** | **str** | Customer&#39;s email address | [optional] 
**merchant_account_reference_id** | **str** | Merchant account identifier at the gateway | [optional] 
**payment_method_id** | **str** | Existing payment method identifier (for updates) | [optional] 
**issuer_identification_number** | **str** | Bank Identification Number (BIN). Must contain exactly 6 or 8 digits. | [optional] 
**billing_address** | [**Address**](Address.md) |  | [optional] 
**shipping_address** | [**Address**](Address.md) |  | [optional] 
**credit_card** | [**CreditCard**](CreditCard.md) |  | [optional] 
**gateway_payment_method** | [**GatewayPaymentMethod**](GatewayPaymentMethod.md) |  | [optional] 
**vault_payment_method** | [**VaultPaymentMethod**](VaultPaymentMethod.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.payment_method import PaymentMethod

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethod from a JSON string
payment_method_instance = PaymentMethod.from_json(json)
# print the JSON string representation of the object
print(PaymentMethod.to_json())

# convert the object into a dict
payment_method_dict = payment_method_instance.to_dict()
# create an instance of PaymentMethod from a dict
payment_method_from_dict = PaymentMethod.from_dict(payment_method_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


