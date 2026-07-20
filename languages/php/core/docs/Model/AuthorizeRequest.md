# AuthorizeRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_type** | **string** | Type of payment method to use: - **creditCard**: Use raw credit card details. Requires &#x60;paymentMethod.creditCard&#x60;   (&#x60;number&#x60;, &#x60;expiryMonth&#x60;, &#x60;expiryYear&#x60;) and a cardholder name — &#x60;paymentMethod.fullName&#x60;,   or &#x60;paymentMethod.firstName&#x60; together with &#x60;paymentMethod.lastName&#x60;. - **gatewayPaymentMethodId**: Use an existing gateway payment method identifier. Requires   &#x60;paymentMethod.gatewayPaymentMethod.gatewayPaymentMethodId&#x60; and   &#x60;paymentMethod.merchantAccountReferenceId&#x60;. - **vaultToken**: Use a vault-issued token (any provider). Requires   &#x60;paymentMethod.vaultPaymentMethod.vaultToken&#x60; and the request-level &#x60;customerId&#x60; — the   token is scoped to the customer it was minted for and cannot be detokenized without it.   Vault tokens are gateway-agnostic and can be processed on any gateway.  **Omitting this property.** When exactly one of &#x60;paymentMethod.creditCard&#x60;, &#x60;paymentMethod.gatewayPaymentMethod&#x60;, or &#x60;paymentMethod.vaultPaymentMethod&#x60; is supplied, the type is inferred from it. Supplying more than one of those objects without an explicit type is rejected with &#x60;400&#x60;. To bill a stored payment method, omit this property (and the objects above) and send &#x60;paymentMethod.paymentMethodId&#x60;; recommendation flows (&#x60;previousTransaction&#x60; / &#x60;gateway&#x60;) also carry no type. | [optional]
**amount** | **int** | Authorization amount in smallest currency unit (e.g., cents for USD) |
**merchant_transaction_id** | **string** | Merchant-provided unique identifier for this authorization. The platform accepts up to 100 characters, but downstream gateways may enforce shorter limits on merchant references (limits near 50 characters have been observed); keep ids at or below 48 characters for the broadest gateway compatibility. |
**gateway_routing_id** | **string** | Gateway-specific token for payment processing | [optional]
**currency** | **string** | Three-letter ISO currency code | [optional]
**initiated_by** | [**\Revaly\Sdk\Core\Model\InitiatedBy**](InitiatedBy.md) |  | [optional]
**mit_stored_transaction_id** | **string** | Merchant-initiated transaction stored credential ID | [optional]
**stored_credential** | [**\Revaly\Sdk\Core\Model\StoredCredential**](StoredCredential.md) |  | [optional]
**payment_method** | [**\Revaly\Sdk\Core\Model\PaymentMethod**](PaymentMethod.md) |  | [optional]
**order_id** | **string** | Order identifier from the merchant system | [optional]
**store_on_success** | **bool** | Whether to store the payment method on successful authorization | [optional]
**bypass_platform** | **bool** | When true, bypass the primary Revaly processor and execute only the fallback flow | [optional] [default to false]
**customer_ip** | **string** | Customer&#39;s IP address | [optional]
**customer_id** | **string** | Customer identifier | [optional]
**gateway_fields** | **array<string,mixed>** | Additional gateway-specific fields | [optional]
**rtn_data** | [**\Revaly\Sdk\Core\Model\RtnData**](RtnData.md) |  | [optional]
**description** | **string** | Authorization description | [optional]
**statement_descriptor** | **string** | Merchant-supplied text intended to appear on the customer&#39;s bank/card statement. Accepted as free text; per-gateway length and character adaptation is applied at submission and never blocks the charge. | [optional]
**three_ds** | [**\Revaly\Sdk\Core\Model\ThreeDS**](ThreeDS.md) |  | [optional]
**payment_plan_data** | [**\Revaly\Sdk\Core\Model\PaymentPlanData**](PaymentPlanData.md) |  | [optional]
**recovery** | [**\Revaly\Sdk\Core\Model\Recovery**](Recovery.md) |  | [optional]
**previous_transaction** | [**\Revaly\Sdk\Core\Model\PreviousTransaction**](PreviousTransaction.md) |  | [optional]
**gateway** | [**\Revaly\Sdk\Core\Model\Gateway**](Gateway.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
