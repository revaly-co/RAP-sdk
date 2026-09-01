

# PaymentMethodResponse

Payment method information associated with a transaction

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**paymentMethodId** | **String** | Unique identifier for the payment method |  [optional] |
|**creditCardNumber** | **String** | Masked credit card number |  [optional] |
|**expiryMonth** | **String** | Credit card expiry month |  [optional] |
|**expiryYear** | **String** | Credit card expiry year |  [optional] |
|**cvv** | **String** | Masked card verification value |  [optional] |
|**firstName** | **String** | Cardholder&#39;s first name |  [optional] |
|**lastName** | **String** | Cardholder&#39;s last name |  [optional] |
|**fullName** | **String** | Cardholder&#39;s full name |  [optional] |
|**customerId** | **String** | Customer identifier |  [optional] |
|**billingAddress** | [**Address**](Address.md) |  |  [optional] |
|**shippingAddress** | [**Address**](Address.md) |  |  [optional] |
|**email** | **String** | Customer&#39;s email address |  [optional] |
|**phoneNumber** | **String** | Customer&#39;s phone number |  [optional] |
|**paymentMethodType** | **String** | Type of payment method |  [optional] |
|**fingerprint** | **String** | Unique fingerprint for the payment method |  [optional] |
|**lastFourDigits** | **String** | Last four digits of the payment method |  [optional] |
|**firstSixDigits** | **String** | First six digits of the payment method (BIN) |  [optional] |
|**cardType** | **String** | Type of credit card |  [optional] |
|**dateCreated** | **OffsetDateTime** | Date when the payment method was created |  [optional] |
|**storageState** | **String** | Storage state of the payment method |  [optional] |
|**bin** | **String** | Bank Identification Number. Must contain exactly 6 or 8 digits. |  [optional] |
|**vaultToken** | **String** | Opaque reference to the stored card this payment method used, returned so a transaction can be tied back to its credential without a second lookup.  Present on the payment method nested inside a **charge or authorize** response, and on the **single-transaction reads** (&#x60;GET /transactions/{transactionId}&#x60; and &#x60;GET /transactions/merchant/{merchantTransactionId}&#x60;), whenever that transaction ran against a vault credential — either one you presented, or one this API created for you when it vaulted the card you sent. The paged list reports it too, but **flat on the row** rather than nested here. The transaction-group reads (&#x60;?includeAllTransactions&#x3D;true&#x60;) report it on every transaction in the group. Follow-up responses (capture, void, refund, refund-cancel) carry no payment method today, so they report no token. Always omitted on the stored payment method endpoints (&#x60;/paymentmethods&#x60; show, list): a stored payment method cannot be created from a vault token, so it never has one to report.  Reads are a snapshot of the value recorded at processing time and do not re-resolve the credential. Where the token can be resolved live, this is the token **currently live** for the credential, which is not always the token submitted — if the card was replaced by the Account Updater, the value is the new head of the lineage. Otherwise it is the token the transaction was dispatched with, and does not reflect a roll. Which of the two you get depends on how the transaction was processed, so treat it as optional throughout and do **not** treat a missing or unchanged value as proof the card was not rolled. Recording began with API version **2.6.0**: transactions processed earlier report no token at all and cannot be backfilled. This is the only place the token is reported — there is deliberately no copy at the transaction level. |  [optional] |



