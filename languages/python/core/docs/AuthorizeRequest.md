# AuthorizeRequest

Request to authorize a payment transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_type** | **str** | Type of payment method to use: - **creditCard**: Use raw credit card details. Requires &#x60;paymentMethod.creditCard&#x60;   (&#x60;number&#x60;, &#x60;expiryMonth&#x60;, &#x60;expiryYear&#x60;) and a cardholder name — &#x60;paymentMethod.fullName&#x60;,   or &#x60;paymentMethod.firstName&#x60; together with &#x60;paymentMethod.lastName&#x60;. - **gatewayPaymentMethodId**: Use an existing gateway payment method identifier. Requires   &#x60;paymentMethod.gatewayPaymentMethod.gatewayPaymentMethodId&#x60; and   &#x60;paymentMethod.merchantAccountReferenceId&#x60;. - **vaultToken**: Use a vault-issued token (any provider). Requires   &#x60;paymentMethod.vaultPaymentMethod.vaultToken&#x60; and the request-level &#x60;customerId&#x60; — the   token is scoped to the customer it was minted for and cannot be detokenized without it.   Vault tokens are gateway-agnostic and can be processed on any gateway.  **Omitting this property.** When exactly one of &#x60;paymentMethod.creditCard&#x60;, &#x60;paymentMethod.gatewayPaymentMethod&#x60;, or &#x60;paymentMethod.vaultPaymentMethod&#x60; is supplied, the type is inferred from it. Supplying more than one of those objects without an explicit type is rejected with &#x60;400&#x60;. To bill a stored payment method, omit this property (and the objects above) and send &#x60;paymentMethod.paymentMethodId&#x60;; recommendation flows (&#x60;previousTransaction&#x60; / &#x60;gateway&#x60;) also carry no type.  | [optional] 
**amount** | **int** | Authorization amount in smallest currency unit (e.g., cents for USD) | 
**merchant_transaction_id** | **str** | Merchant-provided unique identifier for this authorization. The platform accepts up to 100 characters, but downstream gateways may enforce shorter limits on merchant references (limits near 50 characters have been observed); keep ids at or below 48 characters for the broadest gateway compatibility. | 
**gateway_routing_id** | **str** | Gateway-specific token for payment processing | [optional] 
**currency** | **str** | Three-letter ISO currency code | [optional] 
**initiated_by** | [**InitiatedBy**](InitiatedBy.md) |  | [optional] 
**mit_stored_transaction_id** | **str** | Merchant-initiated transaction stored credential ID | [optional] 
**stored_credential** | [**StoredCredential**](StoredCredential.md) |  | [optional] 
**payment_method** | [**PaymentMethod**](PaymentMethod.md) |  | [optional] 
**order_id** | **str** | Order identifier from the merchant system | [optional] 
**store_on_success** | **bool** | Whether to store the payment method on successful authorization | [optional] 
**bypass_platform** | **bool** | When true, bypass the primary Revaly processor and execute only the fallback flow | [optional] [default to False]
**customer_ip** | **str** | Customer&#39;s IP address | [optional] 
**customer_id** | **str** | Customer identifier | [optional] 
**gateway_fields** | **Dict[str, object]** | Additional gateway-specific fields | [optional] 
**rtn_data** | [**RtnData**](RtnData.md) |  | [optional] 
**description** | **str** | Authorization description | [optional] 
**statement_descriptor** | **str** | Merchant-supplied text intended to appear on the customer&#39;s bank/card statement. Accepted as free text; per-gateway length and character adaptation is applied at submission and never blocks the charge. | [optional] 
**three_ds** | [**ThreeDS**](ThreeDS.md) |  | [optional] 
**payment_plan_data** | [**PaymentPlanData**](PaymentPlanData.md) |  | [optional] 
**recovery** | [**Recovery**](Recovery.md) |  | [optional] 
**previous_transaction** | [**PreviousTransaction**](PreviousTransaction.md) |  | [optional] 
**gateway** | [**Gateway**](Gateway.md) |  | [optional] 

## Example

```python
from revaly_sdk_core.models.authorize_request import AuthorizeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AuthorizeRequest from a JSON string
authorize_request_instance = AuthorizeRequest.from_json(json)
# print the JSON string representation of the object
print(AuthorizeRequest.to_json())

# convert the object into a dict
authorize_request_dict = authorize_request_instance.to_dict()
# create an instance of AuthorizeRequest from a dict
authorize_request_from_dict = AuthorizeRequest.from_dict(authorize_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


