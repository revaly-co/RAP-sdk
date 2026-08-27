# PaymentMethodResponse

Payment method information associated with a transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_id** | **str** | Unique identifier for the payment method | [optional] 
**credit_card_number** | **str** | Masked credit card number | [optional] 
**expiry_month** | **str** | Credit card expiry month | [optional] 
**expiry_year** | **str** | Credit card expiry year | [optional] 
**cvv** | **str** | Masked card verification value | [optional] 
**first_name** | **str** | Cardholder&#39;s first name | [optional] 
**last_name** | **str** | Cardholder&#39;s last name | [optional] 
**full_name** | **str** | Cardholder&#39;s full name | [optional] 
**customer_id** | **str** | Customer identifier | [optional] 
**billing_address** | [**Address**](Address.md) |  | [optional] 
**shipping_address** | [**Address**](Address.md) |  | [optional] 
**email** | **str** | Customer&#39;s email address | [optional] 
**phone_number** | **str** | Customer&#39;s phone number | [optional] 
**payment_method_type** | **str** | Type of payment method | [optional] 
**fingerprint** | **str** | Unique fingerprint for the payment method | [optional] 
**last_four_digits** | **str** | Last four digits of the payment method | [optional] 
**first_six_digits** | **str** | First six digits of the payment method (BIN) | [optional] 
**card_type** | **str** | Type of credit card | [optional] 
**date_created** | **datetime** | Date when the payment method was created | [optional] 
**storage_state** | **str** | Storage state of the payment method | [optional] 
**bin** | **str** | Bank Identification Number. Must contain exactly 6 or 8 digits. | [optional] 
**vault_token** | **str** | Opaque reference to the stored card this payment method used, returned so a transaction can be tied back to its credential without a second lookup.  Present only on the payment method nested inside a **charge or authorize** response, and only when that transaction ran against a vault credential — either one you presented, or one this API created for you when it vaulted the card you sent. Always omitted on the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list): a stored payment method cannot be created from a vault token, so it never has one to report. Also omitted on every transaction read endpoint — the token is not persisted and is never replayed on a read.  Where the token can be resolved live, this is the token **currently live** for the credential, which is not always the token submitted — if the card was replaced by the Account Updater, the value is the new head of the lineage. Otherwise it is the token the transaction was dispatched with, and does not reflect a roll. Which of the two you get depends on how the transaction was processed, so treat it as optional throughout and do **not** treat a missing or unchanged value as proof the card was not rolled. This is the only place the token is reported — there is deliberately no copy at the transaction level. | [optional] 

## Example

```python
from revaly_sdk_core.models.payment_method_response import PaymentMethodResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethodResponse from a JSON string
payment_method_response_instance = PaymentMethodResponse.from_json(json)
# print the JSON string representation of the object
print(PaymentMethodResponse.to_json())

# convert the object into a dict
payment_method_response_dict = payment_method_response_instance.to_dict()
# create an instance of PaymentMethodResponse from a dict
payment_method_response_from_dict = PaymentMethodResponse.from_dict(payment_method_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


