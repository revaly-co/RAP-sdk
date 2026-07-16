# PaymentRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_type** | **string** | Type of payment method to use: - **creditCard**: Use raw credit card details - **gatewayPaymentMethodId**: Use an existing gateway payment method identifier - **vaultToken**: Use a vault-issued token (any provider). Requires &#x60;paymentMethod.vaultPaymentMethod.vaultToken&#x60; and &#x60;paymentMethod.merchantAccountReferenceId&#x60;.  To bill a stored payment method, omit this property and send &#x60;paymentMethod.paymentMethodId&#x60;. | [optional]
**amount** | **int** | Payment amount in smallest currency unit (e.g., cents for USD) |
**merchant_transaction_id** | **string** | Merchant-provided unique identifier for this transaction |
**gateway_routing_id** | **string** | Gateway-specific token for payment processing | [optional]
**currency** | **string** | Three-letter ISO currency code | [optional]
**initiated_by** | [**\Revaly\Sdk\Core\Model\InitiatedBy**](InitiatedBy.md) |  | [optional]
**mit_stored_transaction_id** | **string** | Merchant-initiated transaction stored credential ID | [optional]
**stored_credential** | [**\Revaly\Sdk\Core\Model\StoredCredential**](StoredCredential.md) |  | [optional]
**payment_method** | [**\Revaly\Sdk\Core\Model\PaymentMethod**](PaymentMethod.md) |  | [optional]
**order_id** | **string** | Order identifier from the merchant system | [optional]
**store_on_success** | **bool** | Whether to store the payment method on successful transaction | [optional]
**bypass_platform** | **bool** | When true, bypass the primary Revaly processor and execute only the fallback flow | [optional] [default to false]
**customer_ip** | **string** | Customer&#39;s IP address | [optional]
**customer_id** | **string** | Customer identifier | [optional]
**gateway_fields** | **array<string,mixed>** | Additional gateway-specific fields | [optional]
**rtn_data** | [**\Revaly\Sdk\Core\Model\RtnData**](RtnData.md) |  | [optional]
**description** | **string** | Transaction description | [optional]
**statement_descriptor** | **string** | Merchant-supplied text intended to appear on the customer&#39;s bank/card statement. Accepted as free text; per-gateway length and character adaptation is applied at submission and never blocks the charge. | [optional]
**three_ds** | [**\Revaly\Sdk\Core\Model\ThreeDS**](ThreeDS.md) |  | [optional]
**payment_plan_data** | [**\Revaly\Sdk\Core\Model\PaymentPlanData**](PaymentPlanData.md) |  | [optional]
**recovery** | [**\Revaly\Sdk\Core\Model\Recovery**](Recovery.md) |  | [optional]
**previous_transaction** | [**\Revaly\Sdk\Core\Model\PreviousTransaction**](PreviousTransaction.md) |  | [optional]
**gateway** | [**\Revaly\Sdk\Core\Model\Gateway**](Gateway.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
