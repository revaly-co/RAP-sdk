# Revaly.Sdk.Core.Api.PaymentsApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|--------|--------------|-------------|
| [**AuthorizePayment**](PaymentsApi.md#authorizepayment) | **POST** /payments/authorize | Authorize a payment |
| [**CapturePayment**](PaymentsApi.md#capturepayment) | **POST** /payments/capture/{transactionId} | Capture an authorized payment |
| [**ChargePayment**](PaymentsApi.md#chargepayment) | **POST** /payments | Process a payment (charge) |
| [**RefundCancelPaymentByMerchantTransactionId**](PaymentsApi.md#refundcancelpaymentbymerchanttransactionid) | **POST** /payments/refund-cancel/merchant/{merchantTransactionId} | Refund or cancel a payment transaction by merchant transaction ID |
| [**RefundPayment**](PaymentsApi.md#refundpayment) | **POST** /payments/refund/{transactionId} | Refund a payment transaction by TransactionId |
| [**VoidPayment**](PaymentsApi.md#voidpayment) | **POST** /payments/void/{transactionId} | Void a payment transaction |

<a id="authorizepayment"></a>
# **AuthorizePayment**
> TransactionResponse AuthorizePayment (AuthorizeRequest authorizeRequest, string xApiVersion = null)

Authorize a payment

Authorize a payment without immediately capturing funds.  This endpoint creates an authorization hold on the customer's payment method. The authorized amount can later be captured using the capture endpoint.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id - **vaultToken**: Process using a vault-issued token (requires the request-level `customerId`)  `paymentMethodType` may be omitted when exactly one of `paymentMethod.creditCard`, `paymentMethod.gatewayPaymentMethod`, or `paymentMethod.vaultPaymentMethod` is supplied — the type is inferred. See the `AuthorizeRequest` schema for the per-type required fields.  To charge a previously stored payment method, omit `paymentMethodType` and supply `paymentMethod.paymentMethodId`.  A `404` originates from the fallback-processor path (reached when `bypassPlatform: true` routes the payment directly to it, or when platform failover dispatches it): the fallback processor could not find a resource the request references. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **authorizeRequest** | [**AuthorizeRequest**](AuthorizeRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment authorized successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **404** | Resource not found |  * X-Correlation-ID -  <br>  |
| **409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="capturepayment"></a>
# **CapturePayment**
> TransactionResponse CapturePayment (string transactionId, CaptureRequest captureRequest, string xApiVersion = null)

Capture an authorized payment

Capture funds from a previously authorized payment transaction.  This endpoint captures the full or partial amount from an authorization. Once captured, the funds will be settled to your account. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **transactionId** | **string** | Unique identifier of the authorization transaction to capture |  |
| **captureRequest** | [**CaptureRequest**](CaptureRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment captured successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="chargepayment"></a>
# **ChargePayment**
> TransactionResponse ChargePayment (PaymentRequest paymentRequest, string xApiVersion = null)

Process a payment (charge)

Process a direct payment charge against a payment method.  This endpoint performs an immediate charge and settlement of funds. Unlike authorization, the funds are immediately captured and transferred.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id - **vaultToken**: Process using a vault-issued token (requires the request-level `customerId`)  `paymentMethodType` may be omitted when exactly one of `paymentMethod.creditCard`, `paymentMethod.gatewayPaymentMethod`, or `paymentMethod.vaultPaymentMethod` is supplied — the type is inferred. See the `PaymentRequest` schema for the per-type required fields.  To charge a previously stored payment method, omit `paymentMethodType` and supply `paymentMethod.paymentMethodId`.  A `404` originates from the fallback-processor path (reached when `bypassPlatform: true` routes the payment directly to it, or when platform failover dispatches it): the fallback processor could not find a resource the request references. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **paymentRequest** | [**PaymentRequest**](PaymentRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment processed successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **404** | Resource not found |  * X-Correlation-ID -  <br>  |
| **409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="refundcancelpaymentbymerchanttransactionid"></a>
# **RefundCancelPaymentByMerchantTransactionId**
> TransactionResponse RefundCancelPaymentByMerchantTransactionId (string merchantTransactionId, RefundCancelRequest refundCancelRequest, string xApiVersion = null)

Refund or cancel a payment transaction by merchant transaction ID

Refund a previously settled payment transaction using Merchant Transaction ID.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer's payment method.  This endpoint also cancels payments that are currently in the Revaly approvals flow using MerchantTransactionId. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **merchantTransactionId** | **string** | Merchant-provided unique identifier of the transaction to refund or cancel |  |
| **refundCancelRequest** | [**RefundCancelRequest**](RefundCancelRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Refund or cancellation processed successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="refundpayment"></a>
# **RefundPayment**
> TransactionResponse RefundPayment (string transactionId, RefundRequest refundRequest, string xApiVersion = null)

Refund a payment transaction by TransactionId

Refund a previously settled payment transaction using the Revaly transactionId.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer's payment method. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **transactionId** | **string** | Unique identifier of the transaction to refund |  |
| **refundRequest** | [**RefundRequest**](RefundRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Refund processed successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="voidpayment"></a>
# **VoidPayment**
> TransactionResponse VoidPayment (string transactionId, VoidRequest voidRequest, string xApiVersion = null)

Void a payment transaction

Void (cancel) a payment transaction that has not yet been settled.  This endpoint cancels an authorization or unsettled sale transaction. Voided transactions cannot be captured or refunded. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **transactionId** | **string** | Unique identifier of the transaction to void |  |
| **voidRequest** | [**VoidRequest**](VoidRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment voided successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

