# PaymentsApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**authorizePayment**](PaymentsApi.md#authorizepayment) | **POST** /payments/authorize | Authorize a payment |
| [**capturePayment**](PaymentsApi.md#capturepayment) | **POST** /payments/capture/{transactionId} | Capture an authorized payment |
| [**chargePayment**](PaymentsApi.md#chargepayment) | **POST** /payments | Process a payment (charge) |
| [**refundCancelPaymentByMerchantTransactionId**](PaymentsApi.md#refundcancelpaymentbymerchanttransactionid) | **POST** /payments/refund-cancel/merchant/{merchantTransactionId} | Refund or cancel a payment transaction by merchant transaction ID |
| [**refundPayment**](PaymentsApi.md#refundpayment) | **POST** /payments/refund/{transactionId} | Refund a payment transaction by TransactionId |
| [**voidPayment**](PaymentsApi.md#voidpayment) | **POST** /payments/void/{transactionId} | Void a payment transaction |



## authorizePayment

> TransactionResponse authorizePayment(authorizeRequest, xApiVersion)

Authorize a payment

Authorize a payment without immediately capturing funds.  This endpoint creates an authorization hold on the customer\&#39;s payment method. The authorized amount can later be captured using the capture endpoint.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id  To charge a previously stored payment method, omit &#x60;paymentMethodType&#x60; and supply &#x60;paymentMethod.paymentMethodId&#x60;. 

### Example

```ts
import {
  Configuration,
  PaymentsApi,
} from '';
import type { AuthorizePaymentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    // The value is sent verbatim as the Authorization header — the API requires
    // the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
    apiKey: "ApiKey YOUR_API_KEY",
  });
  const api = new PaymentsApi(config);

  const body = {
    // AuthorizeRequest
    authorizeRequest: {"paymentMethodType":"creditCard","gatewayRoutingId":"PCFXF23ORZJEXMJLXJZCDISP6A","amount":2500,"merchantTransactionId":"auth_order_12345","mitStoredTransactionId":"mit_txn_001","initiatedBy":"MIT","currency":"USD","customerId":"customer_123456","customerIp":"192.168.1.100","orderId":"order_67890","description":"Authorization for subscription renewal","storeOnSuccess":true,"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025","cardType":"visa"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}},"threeDS":{"version":"2.2.0","exemptionType":"low_value","eci":"05","cryptogram":"BwABBJQ1AgAAAAAgJDUCAAAAAAA=","dsTransactionId":"c7aa28c2-e2c5-4e5c-a9d3-2f8b3c4d5e6f","acsTransactionId":"d8bb39d3-f3d6-5f6d-b0e4-3f9c4d5e6f70","xid":"MDAwMDAwMDAwMDAwMDAwMzIyNzY=","cavvAlgorithm":"1","directoryStatus":"Y","authenticationStatus":"Y","enrolledStatus":"Y","serverTransId":"e9cc40e4-04e7-6076-c1f5-409d5e6f7081"},"recovery":{"disableCustomerRecovery":false,"customerAccountNumber":"ACC-456789","customerBalance":1922,"disableSMSNotification":false,"disableEmailNotification":false,"retryCount":1,"paymentReferenceData":"initial_txn_ref_456","dateFirstAttempt":"2025-01-10T08:00:00Z"},"paymentPlanData":{"sku":"PREMIUM_MONTHLY","category":"FDT","billingPlan":"monthly","billingCycle":1,"productDisplayName":"Premium Monthly Plan","paymentModel":"recurring","subscriptionId":"sub_abc123def456"}},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies AuthorizePaymentRequest;

  try {
    const data = await api.authorizePayment(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **authorizeRequest** | [AuthorizeRequest](AuthorizeRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment authorized successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment\&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## capturePayment

> TransactionResponse capturePayment(transactionId, captureRequest, xApiVersion)

Capture an authorized payment

Capture funds from a previously authorized payment transaction.  This endpoint captures the full or partial amount from an authorization. Once captured, the funds will be settled to your account. 

### Example

```ts
import {
  Configuration,
  PaymentsApi,
} from '';
import type { CapturePaymentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    // The value is sent verbatim as the Authorization header — the API requires
    // the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
    apiKey: "ApiKey YOUR_API_KEY",
  });
  const api = new PaymentsApi(config);

  const body = {
    // string | Unique identifier of the authorization transaction to capture
    transactionId: 06CQR5TMB800000G0011NCFRVY37A,
    // CaptureRequest
    captureRequest: {"merchantTransactionId":"capture_order_12345"},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies CapturePaymentRequest;

  try {
    const data = await api.capturePayment(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | `string` | Unique identifier of the authorization transaction to capture | [Defaults to `undefined`] |
| **captureRequest** | [CaptureRequest](CaptureRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment captured successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## chargePayment

> TransactionResponse chargePayment(paymentRequest, xApiVersion)

Process a payment (charge)

Process a direct payment charge against a payment method.  This endpoint performs an immediate charge and settlement of funds. Unlike authorization, the funds are immediately captured and transferred.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id  To charge a previously stored payment method, omit &#x60;paymentMethodType&#x60; and supply &#x60;paymentMethod.paymentMethodId&#x60;. 

### Example

```ts
import {
  Configuration,
  PaymentsApi,
} from '';
import type { ChargePaymentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    // The value is sent verbatim as the Authorization header — the API requires
    // the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
    apiKey: "ApiKey YOUR_API_KEY",
  });
  const api = new PaymentsApi(config);

  const body = {
    // PaymentRequest
    paymentRequest: {"paymentMethodType":"creditCard","gatewayRoutingId":"PCFXF23ORZJEXMJLXJZCDISP6A","amount":2500,"merchantTransactionId":"charge_order_12345","mitStoredTransactionId":"mit_txn_001","initiatedBy":"MIT","currency":"USD","customerId":"customer_123456","customerIp":"192.168.1.100","orderId":"order_67890","description":"Payment for online purchase","storeOnSuccess":true,"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025","cardType":"visa"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}},"threeDS":{"version":"2.2.0","exemptionType":"low_value","eci":"05","cryptogram":"BwABBJQ1AgAAAAAgJDUCAAAAAAA=","dsTransactionId":"c7aa28c2-e2c5-4e5c-a9d3-2f8b3c4d5e6f","acsTransactionId":"d8bb39d3-f3d6-5f6d-b0e4-3f9c4d5e6f70","xid":"MDAwMDAwMDAwMDAwMDAwMzIyNzY=","cavvAlgorithm":"1","directoryStatus":"Y","authenticationStatus":"Y","enrolledStatus":"Y","serverTransId":"e9cc40e4-04e7-6076-c1f5-409d5e6f7081"},"recovery":{"disableCustomerRecovery":false,"customerAccountNumber":"ACC-456789","customerBalance":1922,"disableSMSNotification":false,"disableEmailNotification":false,"retryCount":1,"paymentReferenceData":"initial_txn_ref_456","dateFirstAttempt":"2025-01-10T08:00:00Z"},"paymentPlanData":{"sku":"PREMIUM_MONTHLY","category":"FDT","billingPlan":"monthly","billingCycle":1,"productDisplayName":"Premium Monthly Plan","paymentModel":"recurring","subscriptionId":"sub_abc123def456"}},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies ChargePaymentRequest;

  try {
    const data = await api.chargePayment(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **paymentRequest** | [PaymentRequest](PaymentRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment processed successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment\&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## refundCancelPaymentByMerchantTransactionId

> TransactionResponse refundCancelPaymentByMerchantTransactionId(merchantTransactionId, refundCancelRequest, xApiVersion)

Refund or cancel a payment transaction by merchant transaction ID

Refund a previously settled payment transaction using Merchant Transaction ID.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer\&#39;s payment method.  This endpoint also cancels payments that are currently in the Revaly approvals flow using MerchantTransactionId. 

### Example

```ts
import {
  Configuration,
  PaymentsApi,
} from '';
import type { RefundCancelPaymentByMerchantTransactionIdRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    // The value is sent verbatim as the Authorization header — the API requires
    // the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
    apiKey: "ApiKey YOUR_API_KEY",
  });
  const api = new PaymentsApi(config);

  const body = {
    // string | Merchant-provided unique identifier of the transaction to refund or cancel
    merchantTransactionId: merchant_auth_12345638934760478405277,
    // RefundCancelRequest
    refundCancelRequest: {"merchantTransactionId":"refund_order_12345","customerId":"customer_12345"},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies RefundCancelPaymentByMerchantTransactionIdRequest;

  try {
    const data = await api.refundCancelPaymentByMerchantTransactionId(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **merchantTransactionId** | `string` | Merchant-provided unique identifier of the transaction to refund or cancel | [Defaults to `undefined`] |
| **refundCancelRequest** | [RefundCancelRequest](RefundCancelRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Refund or cancellation processed successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## refundPayment

> TransactionResponse refundPayment(transactionId, refundRequest, xApiVersion)

Refund a payment transaction by TransactionId

Refund a previously settled payment transaction using the Revaly transactionId.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer\&#39;s payment method. 

### Example

```ts
import {
  Configuration,
  PaymentsApi,
} from '';
import type { RefundPaymentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    // The value is sent verbatim as the Authorization header — the API requires
    // the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
    apiKey: "ApiKey YOUR_API_KEY",
  });
  const api = new PaymentsApi(config);

  const body = {
    // string | Unique identifier of the transaction to refund
    transactionId: 06CQR5TMB800000G0011NCFRVY37A,
    // RefundRequest
    refundRequest: {"merchantTransactionId":"refund_order_12345"},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies RefundPaymentRequest;

  try {
    const data = await api.refundPayment(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | `string` | Unique identifier of the transaction to refund | [Defaults to `undefined`] |
| **refundRequest** | [RefundRequest](RefundRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Refund processed successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## voidPayment

> TransactionResponse voidPayment(transactionId, voidRequest, xApiVersion)

Void a payment transaction

Void (cancel) a payment transaction that has not yet been settled.  This endpoint cancels an authorization or unsettled sale transaction. Voided transactions cannot be captured or refunded. 

### Example

```ts
import {
  Configuration,
  PaymentsApi,
} from '';
import type { VoidPaymentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    // The value is sent verbatim as the Authorization header — the API requires
    // the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
    apiKey: "ApiKey YOUR_API_KEY",
  });
  const api = new PaymentsApi(config);

  const body = {
    // string | Unique identifier of the transaction to void
    transactionId: 06CQR5TMB800000G0011NCFRVY37A,
    // VoidRequest
    voidRequest: {"merchantTransactionId":"void_order_12345"},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies VoidPaymentRequest;

  try {
    const data = await api.voidPayment(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | `string` | Unique identifier of the transaction to void | [Defaults to `undefined`] |
| **voidRequest** | [VoidRequest](VoidRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment voided successfully |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

