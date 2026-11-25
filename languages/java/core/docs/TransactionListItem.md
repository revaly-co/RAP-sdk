

# TransactionListItem

A flat row of the list transactions endpoint: every payment operation, and every row in simplified mode. A payment-method operation (create, update, redact or recache) in detailed mode is returned as a `TransactionListPaymentMethodItem` instead. A field with no value is omitted. A row is recorded by Backbone or by Olympus, whichever records the transaction first; where the two differ, the field's description says so. In simplified mode, only a subset of fields is returned (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState or storageState, completionStatus). In detailed mode, additional fields are returned (excludes customVariable1-5 and initialTransactionId). 

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**transactionId** | **String** | Unique transaction identifier |  |
|**transactionDate** | **OffsetDateTime** | Date and time when the transaction was processed (ISO 8601) |  [optional] |
|**transactionStatus** | **Integer** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) |  [optional] |
|**responseCode** | **String** | Response code from the processing result |  [optional] |
|**message** | **String** | Human-readable message about the transaction result |  [optional] |
|**transactionType** | **String** | Type of transaction performed: Charge, PreAuth (an authorization), Capture, Void, Refund, RefundedPayment, SuccessfulPayment (a payment recorded through &#x60;/notify&#x60;), Verify, or, for a payment-method operation, CreateCreditCard, CreateGatewayPaymentMethod, UpdatePaymentMethod, RedactPaymentMethod or RecachePaymentMethod |  [optional] |
|**retryDate** | **OffsetDateTime** | Scheduled retry date, if applicable |  [optional] |
|**amount** | **Long** | Transaction amount in smallest currency unit (e.g., cents for USD) |  [optional] |
|**initialMerchantTransactionId** | **String** | The merchant transaction ID of the initial transaction in the recovery chain |  [optional] |
|**storageState** | **String** | Storage state of the payment method. Returned on rows Olympus records (simplified and detailed); rows Backbone records report it in &#x60;paymentMethodStorageState&#x60; instead. |  [optional] |
|**completionStatus** | **String** | Recovery completion status of the transaction (e.g., RecoverySuccessful, RecoveryDeclined) |  [optional] |
|**gatewaySpecificResponseFields** | **Map&lt;String, Object&gt;** | Gateway-specific response fields returned directly by the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle).  |  [optional] |
|**gatewaySpecificFields** | **Map&lt;String, Object&gt;** | Gateway-specific request fields sent to the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle).  |  [optional] |
|**acquirerAuthCode** | **String** | Authorization code returned by the acquiring bank |  [optional] |
|**gatewayTransactionId** | **String** | Gateway-specific transaction identifier |  [optional] |
|**gatewayPaymentMethodId** | **String** | Gateway-specific payment method identifier |  [optional] |
|**engagedRecoveryState** | **Integer** | Recovery state indicator (null/0 &#x3D; not engaged, 1+ &#x3D; recovery level) |  [optional] |
|**currencyCode** | **String** | Transaction currency code (ISO 4217) |  [optional] |
|**merchantTransactionId** | **String** | Merchant-provided transaction identifier |  [optional] |
|**merchantAccountReferenceId** | **String** | Merchant account reference identifier |  [optional] |
|**customerId** | **String** | Customer identifier associated with the transaction |  [optional] |
|**orderId** | **String** | Order identifier from the merchant system |  [optional] |
|**statementDescriptor** | **String** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. |  [optional] |
|**paymentMethodId** | **String** | Payment method identifier used for the transaction |  [optional] |
|**paymentMethodStorageState** | **String** | Storage state of the payment method. Returned on detailed rows and on simplified rows Backbone records; a simplified row Olympus records reports it in &#x60;storageState&#x60; instead. |  [optional] |
|**paymentMethodType** | **String** | Type of payment method used |  [optional] |
|**paymentMethodMerchantAccountReferenceId** | **String** | Merchant account reference ID associated with the payment method |  [optional] |
|**vaultToken** | **String** | Vault token for the credential this transaction ran against, reported flat on the row alongside the other &#x60;paymentMethod*&#x60; fields. Present only on rows that ran against a vault credential — omitted, not null or empty, on every other row. In practice this means the detailed response type: simplified rows carry no payment-method data to report a token from. |  [optional] |
|**errorCode** | **String** | Error code from the gateway response |  [optional] |
|**errorDetail** | **String** | Detailed error message from the gateway response |  [optional] |
|**avsCode** | **String** | Address Verification System result code from the gateway |  [optional] |
|**gateway** | [**TransactionGateway**](TransactionGateway.md) |  |  [optional] |
|**paymentMethod** | [**PaymentMethodResponse**](PaymentMethodResponse.md) | Not returned on a flat row. The payment method of a payment-method operation is reported in &#x60;transaction.paymentMethod&#x60; of a &#x60;TransactionListPaymentMethodItem&#x60;. |  [optional] |



