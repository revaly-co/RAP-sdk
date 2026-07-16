# TransactionResponse

Complete transaction information including processing details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **str** | Unique identifier for the transaction | [optional] 
**transaction_date** | **datetime** | Date and time when the transaction was processed (ISO 8601) | [optional] 
**transaction_status** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional] 
**message** | **str** | Human-readable message about the transaction result | [optional] 
**response_code** | **str** | Gateway-specific response code | [optional] 
**transaction_type** | **str** | Type of transaction performed. Passthrough of the processing platform&#39;s transaction type — not a closed set. Payment operations return \&quot;Charge\&quot;, \&quot;Authorize\&quot;, \&quot;Capture\&quot;, \&quot;Void\&quot; or \&quot;Refund\&quot; (refund cancellation returns \&quot;Refund\&quot;). Transaction lookups can additionally return types created by other platform flows, e.g. \&quot;Verify\&quot;, \&quot;SuccessfulPayment\&quot;, \&quot;RefundedPayment\&quot;, \&quot;CreateCreditCard\&quot;, \&quot;UpdatePaymentMethod\&quot;, \&quot;RedactPaymentMethod\&quot;, \&quot;RecachePaymentMethod\&quot;, \&quot;CreateGatewayPaymentMethod\&quot;. Treat unrecognized values as informational. | [optional] 
**merchant_transaction_id** | **str** | Merchant-provided transaction identifier | [optional] 
**customer_id** | **str** | Customer identifier associated with the transaction | [optional] 
**gateway_routing_id** | **str** | Gateway-specific token for the transaction | [optional] 
**currency** | **str** | Transaction currency code (ISO 4217) | [optional] 
**amount** | **int** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional] 
**gateway_type** | **str** | Payment gateway used for processing | [optional] 
**gateway_transaction_id** | **str** | Gateway-specific transaction identifier | [optional] 
**acquirer_auth_code** | **str** | Authorization code returned by the acquiring bank or network | [optional] 
**inline_retry_previous_transaction_id** | **str** | Transaction identifier of the inline retry attempt when one was executed | [optional] 
**inline_retry_previous_merchant_transaction_id** | **str** | Original merchant transaction identifier before an inline retry was executed | [optional] 
**is_inline_retry** | **bool** | Indicates that an inline retry attempt occurred | [optional] 
**retry_date** | **datetime** | Date for retry attempt (if applicable) | [optional] 
**mit_stored_transaction_id** | **str** | Merchant-initiated transaction stored credential ID | [optional] 
**stored_credential** | [**StoredCredentialResponse**](StoredCredentialResponse.md) |  | [optional] 
**order_id** | **str** | Order identifier from the merchant system | [optional] 
**statement_descriptor** | **str** | Merchant-supplied text intended for the customer&#39;s card or bank statement, echoed back bounded to 255 characters. Adapted per gateway (length/charset) at submission and never blocks the charge. | [optional] 
**customer_ip** | **str** | Customer&#39;s IP address at time of transaction | [optional] 
**engaged_recovery_state** | **int** | Recovery state indicator (0 &#x3D; not engaged, 1+ &#x3D; recovery level) | [optional] 
**description** | **str** | Transaction description or notes | [optional] 
**gateway_fields** | **Dict[str, object]** | Additional gateway-specific fields | [optional] 
**gateway_specific_response_fields** | **Dict[str, object]** | Additional gateway-specific response details returned directly from the processor | [optional] 
**payment_plan_data** | [**PaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**recovery** | [**Recovery**](Recovery.md) |  | [optional] 
**response** | [**TransactionResponseDetails**](TransactionResponseDetails.md) |  | [optional] 
**payment_method** | [**PaymentMethodResponse**](PaymentMethodResponse.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.transaction_response import TransactionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionResponse from a JSON string
transaction_response_instance = TransactionResponse.from_json(json)
# print the JSON string representation of the object
print(TransactionResponse.to_json())

# convert the object into a dict
transaction_response_dict = transaction_response_instance.to_dict()
# create an instance of TransactionResponse from a dict
transaction_response_from_dict = TransactionResponse.from_dict(transaction_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


