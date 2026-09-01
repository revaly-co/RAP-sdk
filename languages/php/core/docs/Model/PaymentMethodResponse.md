# PaymentMethodResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_id** | **string** | Unique identifier for the payment method | [optional]
**credit_card_number** | **string** | Masked credit card number | [optional]
**expiry_month** | **string** | Credit card expiry month | [optional]
**expiry_year** | **string** | Credit card expiry year | [optional]
**cvv** | **string** | Masked card verification value | [optional]
**first_name** | **string** | Cardholder&#39;s first name | [optional]
**last_name** | **string** | Cardholder&#39;s last name | [optional]
**full_name** | **string** | Cardholder&#39;s full name | [optional]
**customer_id** | **string** | Customer identifier | [optional]
**billing_address** | [**\Revaly\Sdk\Core\Model\Address**](Address.md) |  | [optional]
**shipping_address** | [**\Revaly\Sdk\Core\Model\Address**](Address.md) |  | [optional]
**email** | **string** | Customer&#39;s email address | [optional]
**phone_number** | **string** | Customer&#39;s phone number | [optional]
**payment_method_type** | **string** | Type of payment method | [optional]
**fingerprint** | **string** | Unique fingerprint for the payment method | [optional]
**last_four_digits** | **string** | Last four digits of the payment method | [optional]
**first_six_digits** | **string** | First six digits of the payment method (BIN) | [optional]
**card_type** | **string** | Type of credit card | [optional]
**date_created** | **\DateTime** | Date when the payment method was created | [optional]
**storage_state** | **string** | Storage state of the payment method | [optional]
**bin** | **string** | Bank Identification Number. Must contain exactly 6 or 8 digits. | [optional]
**vault_token** | **string** | Opaque reference to the stored card this payment method used, returned so a transaction can be tied back to its credential without a second lookup.  Present on the payment method nested inside a **charge or authorize** response, and on the **single-transaction reads** (&#x60;GET /transactions/{transactionId}&#x60; and &#x60;GET /transactions/merchant/{merchantTransactionId}&#x60;), whenever that transaction ran against a vault credential — either one you presented, or one this API created for you when it vaulted the card you sent. The paged list reports it too, but **flat on the row** rather than nested here. The transaction-group reads (&#x60;?includeAllTransactions&#x3D;true&#x60;) report it on every transaction in the group. Follow-up responses (capture, void, refund, refund-cancel) carry no payment method today, so they report no token. Always omitted on the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list): a stored payment method cannot be created from a vault token, so it never has one to report.  Reads are a snapshot of the value recorded at processing time and do not re-resolve the credential. Where the token can be resolved live, this is the token **currently live** for the credential, which is not always the token submitted — if the card was replaced by the Account Updater, the value is the new head of the lineage. Otherwise it is the token the transaction was dispatched with, and does not reflect a roll. Which of the two you get depends on how the transaction was processed, so treat it as optional throughout and do **not** treat a missing or unchanged value as proof the card was not rolled. Recording began with API version **2.6.0**: transactions processed earlier report no token at all and cannot be backfilled. This is the only place the token is reported — there is deliberately no copy at the transaction level. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
