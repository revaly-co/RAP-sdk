# PaymentsApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**authorizePayment**](PaymentsApi.md#authorizePayment) | **POST** /payments/authorize | Authorize a payment |
| [**authorizePaymentWithHttpInfo**](PaymentsApi.md#authorizePaymentWithHttpInfo) | **POST** /payments/authorize | Authorize a payment |
| [**capturePayment**](PaymentsApi.md#capturePayment) | **POST** /payments/capture/{transactionId} | Capture an authorized payment |
| [**capturePaymentWithHttpInfo**](PaymentsApi.md#capturePaymentWithHttpInfo) | **POST** /payments/capture/{transactionId} | Capture an authorized payment |
| [**chargePayment**](PaymentsApi.md#chargePayment) | **POST** /payments | Process a payment (charge) |
| [**chargePaymentWithHttpInfo**](PaymentsApi.md#chargePaymentWithHttpInfo) | **POST** /payments | Process a payment (charge) |
| [**refundCancelPaymentByMerchantTransactionId**](PaymentsApi.md#refundCancelPaymentByMerchantTransactionId) | **POST** /payments/refund-cancel/merchant/{merchantTransactionId} | Refund or cancel a payment transaction by merchant transaction ID |
| [**refundCancelPaymentByMerchantTransactionIdWithHttpInfo**](PaymentsApi.md#refundCancelPaymentByMerchantTransactionIdWithHttpInfo) | **POST** /payments/refund-cancel/merchant/{merchantTransactionId} | Refund or cancel a payment transaction by merchant transaction ID |
| [**refundPayment**](PaymentsApi.md#refundPayment) | **POST** /payments/refund/{transactionId} | Refund a payment transaction by TransactionId |
| [**refundPaymentWithHttpInfo**](PaymentsApi.md#refundPaymentWithHttpInfo) | **POST** /payments/refund/{transactionId} | Refund a payment transaction by TransactionId |
| [**voidPayment**](PaymentsApi.md#voidPayment) | **POST** /payments/void/{transactionId} | Void a payment transaction |
| [**voidPaymentWithHttpInfo**](PaymentsApi.md#voidPaymentWithHttpInfo) | **POST** /payments/void/{transactionId} | Void a payment transaction |



## authorizePayment

> TransactionResponse authorizePayment(authorizeRequest, xApiVersion)

Authorize a payment

Authorize a payment without immediately capturing funds.  This endpoint creates an authorization hold on the customer&#39;s payment method. The authorized amount can later be captured using the capture endpoint.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id - **vaultToken**: Process using a vault-issued token (requires the request-level &#x60;customerId&#x60;)  &#x60;paymentMethodType&#x60; may be omitted when exactly one of &#x60;paymentMethod.creditCard&#x60;, &#x60;paymentMethod.gatewayPaymentMethod&#x60;, or &#x60;paymentMethod.vaultPaymentMethod&#x60; is supplied — the type is inferred. See the &#x60;AuthorizeRequest&#x60; schema for the per-type required fields.  To charge a previously stored payment method, omit &#x60;paymentMethodType&#x60; and supply &#x60;paymentMethod.paymentMethodId&#x60;. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        AuthorizeRequest authorizeRequest = new AuthorizeRequest(); // AuthorizeRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            TransactionResponse result = apiInstance.authorizePayment(authorizeRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#authorizePayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **authorizeRequest** | [**AuthorizeRequest**](AuthorizeRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

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
| **409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

## authorizePaymentWithHttpInfo

> ApiResponse<TransactionResponse> authorizePaymentWithHttpInfo(authorizeRequest, xApiVersion)

Authorize a payment

Authorize a payment without immediately capturing funds.  This endpoint creates an authorization hold on the customer&#39;s payment method. The authorized amount can later be captured using the capture endpoint.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id - **vaultToken**: Process using a vault-issued token (requires the request-level &#x60;customerId&#x60;)  &#x60;paymentMethodType&#x60; may be omitted when exactly one of &#x60;paymentMethod.creditCard&#x60;, &#x60;paymentMethod.gatewayPaymentMethod&#x60;, or &#x60;paymentMethod.vaultPaymentMethod&#x60; is supplied — the type is inferred. See the &#x60;AuthorizeRequest&#x60; schema for the per-type required fields.  To charge a previously stored payment method, omit &#x60;paymentMethodType&#x60; and supply &#x60;paymentMethod.paymentMethodId&#x60;. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        AuthorizeRequest authorizeRequest = new AuthorizeRequest(); // AuthorizeRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<TransactionResponse> response = apiInstance.authorizePaymentWithHttpInfo(authorizeRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#authorizePayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **authorizeRequest** | [**AuthorizeRequest**](AuthorizeRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**TransactionResponse**](TransactionResponse.md)>


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
| **409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |


## capturePayment

> TransactionResponse capturePayment(transactionId, captureRequest, xApiVersion)

Capture an authorized payment

Capture funds from a previously authorized payment transaction.  This endpoint captures the full or partial amount from an authorization. Once captured, the funds will be settled to your account. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        String transactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Unique identifier of the authorization transaction to capture
        CaptureRequest captureRequest = new CaptureRequest(); // CaptureRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            TransactionResponse result = apiInstance.capturePayment(transactionId, captureRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#capturePayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | **String**| Unique identifier of the authorization transaction to capture | |
| **captureRequest** | [**CaptureRequest**](CaptureRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

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

## capturePaymentWithHttpInfo

> ApiResponse<TransactionResponse> capturePaymentWithHttpInfo(transactionId, captureRequest, xApiVersion)

Capture an authorized payment

Capture funds from a previously authorized payment transaction.  This endpoint captures the full or partial amount from an authorization. Once captured, the funds will be settled to your account. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        String transactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Unique identifier of the authorization transaction to capture
        CaptureRequest captureRequest = new CaptureRequest(); // CaptureRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<TransactionResponse> response = apiInstance.capturePaymentWithHttpInfo(transactionId, captureRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#capturePayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | **String**| Unique identifier of the authorization transaction to capture | |
| **captureRequest** | [**CaptureRequest**](CaptureRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**TransactionResponse**](TransactionResponse.md)>


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


## chargePayment

> TransactionResponse chargePayment(paymentRequest, xApiVersion)

Process a payment (charge)

Process a direct payment charge against a payment method.  This endpoint performs an immediate charge and settlement of funds. Unlike authorization, the funds are immediately captured and transferred.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id - **vaultToken**: Process using a vault-issued token (requires the request-level &#x60;customerId&#x60;)  &#x60;paymentMethodType&#x60; may be omitted when exactly one of &#x60;paymentMethod.creditCard&#x60;, &#x60;paymentMethod.gatewayPaymentMethod&#x60;, or &#x60;paymentMethod.vaultPaymentMethod&#x60; is supplied — the type is inferred. See the &#x60;PaymentRequest&#x60; schema for the per-type required fields.  To charge a previously stored payment method, omit &#x60;paymentMethodType&#x60; and supply &#x60;paymentMethod.paymentMethodId&#x60;. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        PaymentRequest paymentRequest = new PaymentRequest(); // PaymentRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            TransactionResponse result = apiInstance.chargePayment(paymentRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#chargePayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **paymentRequest** | [**PaymentRequest**](PaymentRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

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
| **409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

## chargePaymentWithHttpInfo

> ApiResponse<TransactionResponse> chargePaymentWithHttpInfo(paymentRequest, xApiVersion)

Process a payment (charge)

Process a direct payment charge against a payment method.  This endpoint performs an immediate charge and settlement of funds. Unlike authorization, the funds are immediately captured and transferred.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id - **vaultToken**: Process using a vault-issued token (requires the request-level &#x60;customerId&#x60;)  &#x60;paymentMethodType&#x60; may be omitted when exactly one of &#x60;paymentMethod.creditCard&#x60;, &#x60;paymentMethod.gatewayPaymentMethod&#x60;, or &#x60;paymentMethod.vaultPaymentMethod&#x60; is supplied — the type is inferred. See the &#x60;PaymentRequest&#x60; schema for the per-type required fields.  To charge a previously stored payment method, omit &#x60;paymentMethodType&#x60; and supply &#x60;paymentMethod.paymentMethodId&#x60;. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        PaymentRequest paymentRequest = new PaymentRequest(); // PaymentRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<TransactionResponse> response = apiInstance.chargePaymentWithHttpInfo(paymentRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#chargePayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **paymentRequest** | [**PaymentRequest**](PaymentRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**TransactionResponse**](TransactionResponse.md)>


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
| **409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |


## refundCancelPaymentByMerchantTransactionId

> TransactionResponse refundCancelPaymentByMerchantTransactionId(merchantTransactionId, refundCancelRequest, xApiVersion)

Refund or cancel a payment transaction by merchant transaction ID

Refund a previously settled payment transaction using Merchant Transaction ID.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer&#39;s payment method.  This endpoint also cancels payments that are currently in the Revaly approvals flow using MerchantTransactionId. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        String merchantTransactionId = "merchant_auth_12345638934760478405277"; // String | Merchant-provided unique identifier of the transaction to refund or cancel
        RefundCancelRequest refundCancelRequest = new RefundCancelRequest(); // RefundCancelRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            TransactionResponse result = apiInstance.refundCancelPaymentByMerchantTransactionId(merchantTransactionId, refundCancelRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#refundCancelPaymentByMerchantTransactionId");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **merchantTransactionId** | **String**| Merchant-provided unique identifier of the transaction to refund or cancel | |
| **refundCancelRequest** | [**RefundCancelRequest**](RefundCancelRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

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

## refundCancelPaymentByMerchantTransactionIdWithHttpInfo

> ApiResponse<TransactionResponse> refundCancelPaymentByMerchantTransactionIdWithHttpInfo(merchantTransactionId, refundCancelRequest, xApiVersion)

Refund or cancel a payment transaction by merchant transaction ID

Refund a previously settled payment transaction using Merchant Transaction ID.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer&#39;s payment method.  This endpoint also cancels payments that are currently in the Revaly approvals flow using MerchantTransactionId. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        String merchantTransactionId = "merchant_auth_12345638934760478405277"; // String | Merchant-provided unique identifier of the transaction to refund or cancel
        RefundCancelRequest refundCancelRequest = new RefundCancelRequest(); // RefundCancelRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<TransactionResponse> response = apiInstance.refundCancelPaymentByMerchantTransactionIdWithHttpInfo(merchantTransactionId, refundCancelRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#refundCancelPaymentByMerchantTransactionId");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **merchantTransactionId** | **String**| Merchant-provided unique identifier of the transaction to refund or cancel | |
| **refundCancelRequest** | [**RefundCancelRequest**](RefundCancelRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**TransactionResponse**](TransactionResponse.md)>


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


## refundPayment

> TransactionResponse refundPayment(transactionId, refundRequest, xApiVersion)

Refund a payment transaction by TransactionId

Refund a previously settled payment transaction using the Revaly transactionId.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer&#39;s payment method. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        String transactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Unique identifier of the transaction to refund
        RefundRequest refundRequest = new RefundRequest(); // RefundRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            TransactionResponse result = apiInstance.refundPayment(transactionId, refundRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#refundPayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | **String**| Unique identifier of the transaction to refund | |
| **refundRequest** | [**RefundRequest**](RefundRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

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

## refundPaymentWithHttpInfo

> ApiResponse<TransactionResponse> refundPaymentWithHttpInfo(transactionId, refundRequest, xApiVersion)

Refund a payment transaction by TransactionId

Refund a previously settled payment transaction using the Revaly transactionId.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer&#39;s payment method. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        String transactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Unique identifier of the transaction to refund
        RefundRequest refundRequest = new RefundRequest(); // RefundRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<TransactionResponse> response = apiInstance.refundPaymentWithHttpInfo(transactionId, refundRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#refundPayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | **String**| Unique identifier of the transaction to refund | |
| **refundRequest** | [**RefundRequest**](RefundRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**TransactionResponse**](TransactionResponse.md)>


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


## voidPayment

> TransactionResponse voidPayment(transactionId, voidRequest, xApiVersion)

Void a payment transaction

Void (cancel) a payment transaction that has not yet been settled.  This endpoint cancels an authorization or unsettled sale transaction. Voided transactions cannot be captured or refunded. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        String transactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Unique identifier of the transaction to void
        VoidRequest voidRequest = new VoidRequest(); // VoidRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            TransactionResponse result = apiInstance.voidPayment(transactionId, voidRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#voidPayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | **String**| Unique identifier of the transaction to void | |
| **voidRequest** | [**VoidRequest**](VoidRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

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

## voidPaymentWithHttpInfo

> ApiResponse<TransactionResponse> voidPaymentWithHttpInfo(transactionId, voidRequest, xApiVersion)

Void a payment transaction

Void (cancel) a payment transaction that has not yet been settled.  This endpoint cancels an authorization or unsettled sale transaction. Voided transactions cannot be captured or refunded. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        PaymentsApi apiInstance = new PaymentsApi(defaultClient);
        String transactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Unique identifier of the transaction to void
        VoidRequest voidRequest = new VoidRequest(); // VoidRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<TransactionResponse> response = apiInstance.voidPaymentWithHttpInfo(transactionId, voidRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentsApi#voidPayment");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **transactionId** | **String**| Unique identifier of the transaction to void | |
| **voidRequest** | [**VoidRequest**](VoidRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**TransactionResponse**](TransactionResponse.md)>


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

