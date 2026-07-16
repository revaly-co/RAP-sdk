# TransactionListItem

Transaction item returned from the list transactions endpoint. In simplified mode, only a subset of fields is returned (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). In detailed mode, additional fields are returned (excludes customVariable1-5 and initialTransactionId). 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | Unique transaction identifier | [optional] 
**transaction_date** | **datetime** | Date and time when the transaction was processed (ISO 8601) | [optional] 
**transaction_status** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**response_code** | **str** | Response code from the processing result | [optional] 
**message** | **str** | Human-readable message about the transaction result | [optional] 
**transaction_type** | **str** | Type of transaction performed | [optional] 
**retry_date** | **datetime** | Scheduled retry date, if applicable | [optional] 
**amount** | **int** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**initial_merchant_transaction_id** | **str** | The merchant transaction ID of the initial transaction in the recovery chain | [optional] 
**storage_state** | **str** | Payment method storage state at the time of transaction | [optional] 
**completion_status** | **str** | Recovery completion status of the transaction (e.g., RecoverySuccessful, RecoveryDeclined) | [optional] 
**gateway_specific_response_fields** | **Dict[str, object]** | Gateway-specific response fields returned directly by the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle).  | [optional] 
**gateway_specific_fields** | **Dict[str, object]** | Gateway-specific request fields sent to the payment processor. Keyed by gateway type (e.g., chase_payment_tech, stripe_payment_intents, worldpay_litle).  | [optional] 
**acquirer_auth_code** | **str** | Authorization code returned by the acquiring bank | [optional] 
**gateway_transaction_id** | **str** | Gateway-specific transaction identifier | [optional] 
**gateway_payment_method_id** | **str** | Gateway-specific payment method identifier | [optional] 
**engaged_recovery_state** | **int** | Recovery state indicator (null/0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional] 
**currency_code** | **str** | Transaction currency code (ISO 4217) | [optional] 
**merchant_transaction_id** | **str** | Merchant-provided transaction identifier | [optional] 
**merchant_account_reference_id** | **str** | Merchant account reference identifier | [optional] 
**customer_id** | **str** | Customer identifier associated with the transaction | [optional] 
**order_id** | **str** | Order identifier from the merchant system | [optional] 
**statement_descriptor** | **str** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. | [optional] 
**payment_method_id** | **str** | Payment method identifier used for the transaction | [optional] 
**payment_method_storage_state** | **str** | Storage state of the payment method | [optional] 
**payment_method_type** | **str** | Type of payment method used | [optional] 
**payment_method_merchant_account_reference_id** | **str** | Merchant account reference ID associated with the payment method | [optional] 
**error_code** | **str** | Error code from the gateway response | [optional] 
**error_detail** | **str** | Detailed error message from the gateway response | [optional] 
**avs_code** | **str** | Address Verification System result code from the gateway | [optional] 
**gateway** | [**TransactionGateway**](TransactionGateway.md) |  | [optional] 
**payment_method** | [**PaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.transaction_list_item import TransactionListItem

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionListItem from a JSON string
transaction_list_item_instance = TransactionListItem.from_json(json)
# print the JSON string representation of the object
print(TransactionListItem.to_json())

# convert the object into a dict
transaction_list_item_dict = transaction_list_item_instance.to_dict()
# create an instance of TransactionListItem from a dict
transaction_list_item_from_dict = TransactionListItem.from_dict(transaction_list_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


