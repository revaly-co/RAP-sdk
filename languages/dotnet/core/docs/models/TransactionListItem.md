# Revaly.Sdk.Core.Model.TransactionListItem
Transaction item returned from the list transactions endpoint. In simplified mode, only a subset of fields is returned (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). In detailed mode, additional fields are returned (excludes customVariable1-5 and initialTransactionId). 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**TransactionId** | **string** | Unique transaction identifier | [optional] 
**TransactionDate** | **DateTime** | Date and time when the transaction was processed (ISO 8601) | [optional] 
**TransactionStatus** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**ResponseCode** | **string** | Response code from the processing result | [optional] 
**Message** | **string** | Human-readable message about the transaction result | [optional] 
**TransactionType** | **string** | Type of transaction performed | [optional] 
**RetryDate** | **DateTime** | Scheduled retry date, if applicable | [optional] 
**Amount** | **long** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**InitialMerchantTransactionId** | **string** | The merchant transaction ID of the initial transaction in the recovery chain | [optional] 
**StorageState** | **string** | Payment method storage state at the time of transaction | [optional] 
**CompletionStatus** | **string** | Recovery completion status of the transaction (e.g., RecoverySuccessful, RecoveryDeclined) | [optional] 
**GatewaySpecificResponseFields** | **Dictionary&lt;string, Object&gt;** | Gateway-specific response fields returned directly by the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle).  | [optional] 
**GatewaySpecificFields** | **Dictionary&lt;string, Object&gt;** | Gateway-specific request fields sent to the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle).  | [optional] 
**AcquirerAuthCode** | **string** | Authorization code returned by the acquiring bank | [optional] 
**GatewayTransactionId** | **string** | Gateway-specific transaction identifier | [optional] 
**GatewayPaymentMethodId** | **string** | Gateway-specific payment method identifier | [optional] 
**EngagedRecoveryState** | **int** | Recovery state indicator (null/0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional] 
**CurrencyCode** | **string** | Transaction currency code (ISO 4217) | [optional] 
**MerchantTransactionId** | **string** | Merchant-provided transaction identifier | [optional] 
**MerchantAccountReferenceId** | **string** | Merchant account reference identifier | [optional] 
**CustomerId** | **string** | Customer identifier associated with the transaction | [optional] 
**OrderId** | **string** | Order identifier from the merchant system | [optional] 
**StatementDescriptor** | **string** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. | [optional] 
**PaymentMethodId** | **string** | Payment method identifier used for the transaction | [optional] 
**PaymentMethodStorageState** | **string** | Storage state of the payment method | [optional] 
**PaymentMethodType** | **string** | Type of payment method used | [optional] 
**PaymentMethodMerchantAccountReferenceId** | **string** | Merchant account reference ID associated with the payment method | [optional] 
**ErrorCode** | **string** | Error code from the gateway response | [optional] 
**ErrorDetail** | **string** | Detailed error message from the gateway response | [optional] 
**AvsCode** | **string** | Address Verification System result code from the gateway | [optional] 
**Gateway** | [**TransactionGateway**](TransactionGateway.md) |  | [optional] 
**PaymentMethod** | [**PaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

