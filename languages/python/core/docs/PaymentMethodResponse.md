# PaymentMethodResponse

Payment method information associated with a transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_id** | **str** | Unique identifier for the payment method | [optional] 
**credit_card_number** | **str** | Masked credit card number | [optional] 
**expiry_month** | **str** | Credit card expiry month, two digits.  On a **charge or authorize** response this is the expiry month you sent (a one-digit month is returned padded to two digits), unless this API holds a newer, confirmed expiry for the same card: from the card vault&#39;s Account Updater, or from the real-time account updater of Chase Orbital or Worldpay Litle. Then it is the newer month. When the Account Updater has replaced the card behind the vault token you presented, the response returns the replacement&#39;s &#x60;vaultToken&#x60; with &#x60;cardReplaced&#x60;; the expiry month is the replacement card&#39;s when this API holds a confirmed expiry for that card, and otherwise the month you sent. A newer expiry is never a date this API estimated, never earlier than the expiry you sent for the same card, and never part of a card number. When you sent no expiry and nothing newer is known, the field is omitted. For a &#x60;gatewayPaymentMethodId&#x60;, it can be the expiry recorded for that payment method rather than the one you sent.  The **single-transaction reads** and the transaction-group reads return the value recorded when the transaction was processed. The paged list reports this field only for payment method operations. On the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list) it is the expiry stored on the payment method, which a newer expiry returned on a transaction does not update. | [optional] 
**expiry_year** | **str** | Credit card expiry year.  On a **charge or authorize** response this is the expiry year you sent, unless this API holds a newer, confirmed expiry for the same card: from the card vault&#39;s Account Updater, or from the real-time account updater of Chase Orbital or Worldpay Litle. Then it is the newer year. When the Account Updater has replaced the card behind the vault token you presented, the response returns the replacement&#39;s &#x60;vaultToken&#x60; with &#x60;cardReplaced&#x60;; the expiry year is the replacement card&#39;s when this API holds a confirmed expiry for that card, and otherwise the year you sent. A newer expiry is never a date this API estimated, never earlier than the expiry you sent for the same card, and never part of a card number. When you sent no expiry and nothing newer is known, the field is omitted. For a &#x60;gatewayPaymentMethodId&#x60;, it can be the expiry recorded for that payment method rather than the one you sent.  The **single-transaction reads** and the transaction-group reads return the value recorded when the transaction was processed. The paged list reports this field only for payment method operations. On the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list) it is the expiry stored on the payment method, which a newer expiry returned on a transaction does not update. | [optional] 
**expiry_updated** | **bool** | &#x60;true&#x60; when the expiry this response returns in &#x60;expiryMonth&#x60; and &#x60;expiryYear&#x60; differs from the expiry you sent, because this API holds a newer, confirmed expiry for the card (see &#x60;expiryMonth&#x60;). Present, and then &#x60;true&#x60;, only on the payment method nested inside a **charge or authorize** response; omitted otherwise, and never &#x60;false&#x60;.  The **single-transaction reads** and the transaction-group reads return the value recorded when the transaction was processed. Always omitted on follow-up responses (capture, void, refund, refund-cancel) and on the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list). | [optional] 
**card_replaced** | **bool** | &#x60;true&#x60; when this API learned that the card behind this payment method was replaced: the card vault&#39;s Account Updater replaced the card behind the vault token you presented (the response then returns the replacement&#39;s &#x60;vaultToken&#x60;), or the real-time account updater of Chase Orbital or Worldpay Litle reported a replacement card. A replacement card&#39;s expiry is returned in &#x60;expiryMonth&#x60; and &#x60;expiryYear&#x60; only with &#x60;cardReplaced&#x60;, and only when this API holds a confirmed expiry for that card. Present, and then &#x60;true&#x60;, only on the payment method nested inside a **charge or authorize** response; omitted otherwise, and never &#x60;false&#x60;. Gateway-specific response blocks are passed through as received and are not covered by &#x60;cardReplaced&#x60;.  The **single-transaction reads** and the transaction-group reads return the value recorded when the transaction was processed. Always omitted on follow-up responses (capture, void, refund, refund-cancel) and on the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list). | [optional] 
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
**vault_token** | **str** | Opaque reference to the stored card this payment method used, returned so a transaction can be tied back to its credential without a second lookup.  Present on the payment method nested inside a **charge or authorize** response, and on the **single-transaction reads** (&#x60;GET /transactions/{transactionId}&#x60; and &#x60;GET /transactions/merchant/{merchantTransactionId}&#x60;), whenever that transaction ran against a vault credential — either one you presented, or one this API created for you when it vaulted the card you sent. The paged list reports it too, but **flat on the row** rather than nested here. The transaction-group reads (&#x60;?includeAllTransactions&#x3D;true&#x60;) report it on every transaction in the group. Follow-up responses (capture, void, refund, refund-cancel) carry no payment method today, so they report no token. Always omitted on the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list): a stored payment method cannot be created from a vault token, so it never has one to report.  Reads are a snapshot of the value recorded at processing time and do not re-resolve the credential. Where the token can be resolved live, this is the token **currently live** for the credential, which is not always the token submitted — if the card was replaced by the Account Updater, the value is the new head of the lineage. Otherwise it is the token the transaction was dispatched with, and does not reflect a roll. Which of the two you get depends on how the transaction was processed, so treat it as optional throughout and do **not** treat a missing or unchanged value as proof the card was not rolled. Recording began with API version **2.6.0**: transactions processed earlier report no token at all and cannot be backfilled. This is the only place the token is reported — there is deliberately no copy at the transaction level. | [optional] 

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


