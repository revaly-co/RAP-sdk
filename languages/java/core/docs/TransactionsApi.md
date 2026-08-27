# TransactionsApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**getTransactionById**](TransactionsApi.md#getTransactionById) | **GET** /transactions/{transactionId} | Get transaction details |
| [**getTransactionByIdWithHttpInfo**](TransactionsApi.md#getTransactionByIdWithHttpInfo) | **GET** /transactions/{transactionId} | Get transaction details |
| [**getTransactionByMerchantTransactionId**](TransactionsApi.md#getTransactionByMerchantTransactionId) | **GET** /transactions/merchant/{merchantTransactionId} | Get transaction details by merchant transaction ID |
| [**getTransactionByMerchantTransactionIdWithHttpInfo**](TransactionsApi.md#getTransactionByMerchantTransactionIdWithHttpInfo) | **GET** /transactions/merchant/{merchantTransactionId} | Get transaction details by merchant transaction ID |
| [**listTransactions**](TransactionsApi.md#listTransactions) | **GET** /transactions | List transactions |
| [**listTransactionsWithHttpInfo**](TransactionsApi.md#listTransactionsWithHttpInfo) | **GET** /transactions | List transactions |



## getTransactionById

> GetTransactionById200Response getTransactionById(transactionId, xApiVersion, includeAllTransactions)

Get transaction details

Retrieve detailed information about a specific transaction by its ID.  This endpoint returns complete transaction data including payment method details, gateway response information, recovery data and status of transaction. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.TransactionsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        TransactionsApi apiInstance = new TransactionsApi(defaultClient);
        String transactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Unique identifier for the transaction
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        Boolean includeAllTransactions = true; // Boolean | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned. 
        try {
            GetTransactionById200Response result = apiInstance.getTransactionById(transactionId, xApiVersion, includeAllTransactions);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling TransactionsApi#getTransactionById");
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
| **transactionId** | **String**| Unique identifier for the transaction | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |
| **includeAllTransactions** | **Boolean**| When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | [optional] |

### Return type

[**GetTransactionById200Response**](GetTransactionById200Response.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved transaction details. Returns a single &#x60;TransactionResponse&#x60; by default, or a &#x60;TransactionGroupResponse&#x60; envelope when &#x60;includeAllTransactions&#x3D;true&#x60;.  Discriminate by the required &#x60;transactions&#x60; member: present means the &#x60;TransactionGroupResponse&#x60; envelope, absent means a single &#x60;TransactionResponse&#x60;. Branches are ordered most-specific first for match-in-order deserializers.  |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **404** | Resource not found |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

## getTransactionByIdWithHttpInfo

> ApiResponse<GetTransactionById200Response> getTransactionByIdWithHttpInfo(transactionId, xApiVersion, includeAllTransactions)

Get transaction details

Retrieve detailed information about a specific transaction by its ID.  This endpoint returns complete transaction data including payment method details, gateway response information, recovery data and status of transaction. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.TransactionsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        TransactionsApi apiInstance = new TransactionsApi(defaultClient);
        String transactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Unique identifier for the transaction
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        Boolean includeAllTransactions = true; // Boolean | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned. 
        try {
            ApiResponse<GetTransactionById200Response> response = apiInstance.getTransactionByIdWithHttpInfo(transactionId, xApiVersion, includeAllTransactions);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling TransactionsApi#getTransactionById");
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
| **transactionId** | **String**| Unique identifier for the transaction | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |
| **includeAllTransactions** | **Boolean**| When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | [optional] |

### Return type

ApiResponse<[**GetTransactionById200Response**](GetTransactionById200Response.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved transaction details. Returns a single &#x60;TransactionResponse&#x60; by default, or a &#x60;TransactionGroupResponse&#x60; envelope when &#x60;includeAllTransactions&#x3D;true&#x60;.  Discriminate by the required &#x60;transactions&#x60; member: present means the &#x60;TransactionGroupResponse&#x60; envelope, absent means a single &#x60;TransactionResponse&#x60;. Branches are ordered most-specific first for match-in-order deserializers.  |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **404** | Resource not found |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |


## getTransactionByMerchantTransactionId

> GetTransactionByMerchantTransactionId200Response getTransactionByMerchantTransactionId(merchantTransactionId, xApiVersion, includeAllTransactions)

Get transaction details by merchant transaction ID

Retrieve detailed information about a specific transaction by its merchant transaction ID.  This endpoint returns complete transaction data including payment method details, gateway response information, recovery data and status of transaction using the merchant-provided transaction identifier.  **Inline-retry resolution:** platform-initiated inline retry attempts carry platform-assigned transaction identifiers. This lookup resolves the payment submitted under the merchant id and returns its definitive (latest) attempt, so an approval won on a retry is found under the id the merchant submitted. In that case the returned &#x60;merchantTransactionId&#x60; is the platform-assigned attempt id rather than the path value; use the grouped view (&#x60;includeAllTransactions&#x3D;true&#x60;) to list every attempt.  **Pending intent:** when the platform has accepted a payment with this merchantTransactionId (intent recorded before gateway dispatch) but no transaction record is visible yet, the lookup returns a &#x60;PendingTransactionResponse&#x60; (&#x60;state: pending&#x60;) instead of 404 — hold and re-poll until it resolves to the full transaction. A 404 means no payment with this id was ever accepted. Pending intents are not returned on the grouped view (&#x60;includeAllTransactions&#x3D;true&#x60;), which lists only visible transaction records. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.TransactionsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        TransactionsApi apiInstance = new TransactionsApi(defaultClient);
        String merchantTransactionId = "merchant_auth_12345638934760478405277"; // String | Merchant-provided unique identifier for the transaction
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        Boolean includeAllTransactions = true; // Boolean | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned. 
        try {
            GetTransactionByMerchantTransactionId200Response result = apiInstance.getTransactionByMerchantTransactionId(merchantTransactionId, xApiVersion, includeAllTransactions);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling TransactionsApi#getTransactionByMerchantTransactionId");
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
| **merchantTransactionId** | **String**| Merchant-provided unique identifier for the transaction | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |
| **includeAllTransactions** | **Boolean**| When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | [optional] |

### Return type

[**GetTransactionByMerchantTransactionId200Response**](GetTransactionByMerchantTransactionId200Response.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved transaction details. Returns a single &#x60;TransactionResponse&#x60; by default, or a &#x60;TransactionGroupResponse&#x60; envelope when &#x60;includeAllTransactions&#x3D;true&#x60;. Returns a &#x60;PendingTransactionResponse&#x60; (&#x60;state: pending&#x60;) when the payment intent was accepted but no transaction record is visible yet.  Discriminate by required members: a body with &#x60;state: \&quot;pending\&quot;&#x60; is a &#x60;PendingTransactionResponse&#x60;; a body with &#x60;transactions&#x60; is a &#x60;TransactionGroupResponse&#x60; envelope; otherwise it is a single &#x60;TransactionResponse&#x60;. Branches are ordered most-specific first for match-in-order deserializers.  |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **404** | Resource not found |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

## getTransactionByMerchantTransactionIdWithHttpInfo

> ApiResponse<GetTransactionByMerchantTransactionId200Response> getTransactionByMerchantTransactionIdWithHttpInfo(merchantTransactionId, xApiVersion, includeAllTransactions)

Get transaction details by merchant transaction ID

Retrieve detailed information about a specific transaction by its merchant transaction ID.  This endpoint returns complete transaction data including payment method details, gateway response information, recovery data and status of transaction using the merchant-provided transaction identifier.  **Inline-retry resolution:** platform-initiated inline retry attempts carry platform-assigned transaction identifiers. This lookup resolves the payment submitted under the merchant id and returns its definitive (latest) attempt, so an approval won on a retry is found under the id the merchant submitted. In that case the returned &#x60;merchantTransactionId&#x60; is the platform-assigned attempt id rather than the path value; use the grouped view (&#x60;includeAllTransactions&#x3D;true&#x60;) to list every attempt.  **Pending intent:** when the platform has accepted a payment with this merchantTransactionId (intent recorded before gateway dispatch) but no transaction record is visible yet, the lookup returns a &#x60;PendingTransactionResponse&#x60; (&#x60;state: pending&#x60;) instead of 404 — hold and re-poll until it resolves to the full transaction. A 404 means no payment with this id was ever accepted. Pending intents are not returned on the grouped view (&#x60;includeAllTransactions&#x3D;true&#x60;), which lists only visible transaction records. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.TransactionsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        TransactionsApi apiInstance = new TransactionsApi(defaultClient);
        String merchantTransactionId = "merchant_auth_12345638934760478405277"; // String | Merchant-provided unique identifier for the transaction
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        Boolean includeAllTransactions = true; // Boolean | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned. 
        try {
            ApiResponse<GetTransactionByMerchantTransactionId200Response> response = apiInstance.getTransactionByMerchantTransactionIdWithHttpInfo(merchantTransactionId, xApiVersion, includeAllTransactions);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling TransactionsApi#getTransactionByMerchantTransactionId");
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
| **merchantTransactionId** | **String**| Merchant-provided unique identifier for the transaction | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |
| **includeAllTransactions** | **Boolean**| When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | [optional] |

### Return type

ApiResponse<[**GetTransactionByMerchantTransactionId200Response**](GetTransactionByMerchantTransactionId200Response.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved transaction details. Returns a single &#x60;TransactionResponse&#x60; by default, or a &#x60;TransactionGroupResponse&#x60; envelope when &#x60;includeAllTransactions&#x3D;true&#x60;. Returns a &#x60;PendingTransactionResponse&#x60; (&#x60;state: pending&#x60;) when the payment intent was accepted but no transaction record is visible yet.  Discriminate by required members: a body with &#x60;state: \&quot;pending\&quot;&#x60; is a &#x60;PendingTransactionResponse&#x60;; a body with &#x60;transactions&#x60; is a &#x60;TransactionGroupResponse&#x60; envelope; otherwise it is a single &#x60;TransactionResponse&#x60;. Branches are ordered most-specific first for match-in-order deserializers.  |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **404** | Resource not found |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |


## listTransactions

> List<TransactionListItem> listTransactions(xApiVersion, count, order, sinceTransactionId, startDate, endDate, completedOnly, responseType)

List transactions

Retrieve a paginated list of transactions for the authenticated account.  This endpoint returns transaction data with optional filtering and pagination support. Transactions are returned based on the specified order and count parameters. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.TransactionsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        TransactionsApi apiInstance = new TransactionsApi(defaultClient);
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        Integer count = 20; // Integer | Number of transactions to return per page
        String order = "asc"; // String | Sort order for results. Default is asc.
        String sinceTransactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Return transactions after this transaction ID (for pagination)
        OffsetDateTime startDate = OffsetDateTime.parse("2024-09-12T00:00:00Z"); // OffsetDateTime | Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS.
        OffsetDateTime endDate = OffsetDateTime.parse("2024-09-13T00:00:00Z"); // OffsetDateTime | End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS.
        Boolean completedOnly = false; // Boolean | Requests a list of transactions that have completed the approvals process. Default is false (all transactions).
        String responseType = "detailed"; // String | Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields. 
        try {
            List<TransactionListItem> result = apiInstance.listTransactions(xApiVersion, count, order, sinceTransactionId, startDate, endDate, completedOnly, responseType);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling TransactionsApi#listTransactions");
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
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |
| **count** | **Integer**| Number of transactions to return per page | [optional] [default to 20] |
| **order** | **String**| Sort order for results. Default is asc. | [optional] [default to asc] [enum: asc, desc] |
| **sinceTransactionId** | **String**| Return transactions after this transaction ID (for pagination) | [optional] |
| **startDate** | **OffsetDateTime**| Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional] |
| **endDate** | **OffsetDateTime**| End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional] |
| **completedOnly** | **Boolean**| Requests a list of transactions that have completed the approvals process. Default is false (all transactions). | [optional] [default to false] |
| **responseType** | **String**| Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields.  | [optional] [default to detailed] [enum: detailed, simplified] |

### Return type

[**List&lt;TransactionListItem&gt;**](TransactionListItem.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved transactions |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

## listTransactionsWithHttpInfo

> ApiResponse<List<TransactionListItem>> listTransactionsWithHttpInfo(xApiVersion, count, order, sinceTransactionId, startDate, endDate, completedOnly, responseType)

List transactions

Retrieve a paginated list of transactions for the authenticated account.  This endpoint returns transaction data with optional filtering and pagination support. Transactions are returned based on the specified order and count parameters. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.TransactionsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth — this `native`-library core has no
        // auth helper classes; set the header on every request via the request interceptor.
        // The API requires the `ApiKey` scheme prefix:  Authorization: ApiKey YOUR_API_KEY
        defaultClient.setRequestInterceptor(builder ->
            builder.header("Authorization", "ApiKey " + System.getenv("RAP_API_KEY")));

        TransactionsApi apiInstance = new TransactionsApi(defaultClient);
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        Integer count = 20; // Integer | Number of transactions to return per page
        String order = "asc"; // String | Sort order for results. Default is asc.
        String sinceTransactionId = "06CQR5TMB800000G0011NCFRVY37A"; // String | Return transactions after this transaction ID (for pagination)
        OffsetDateTime startDate = OffsetDateTime.parse("2024-09-12T00:00:00Z"); // OffsetDateTime | Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS.
        OffsetDateTime endDate = OffsetDateTime.parse("2024-09-13T00:00:00Z"); // OffsetDateTime | End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS.
        Boolean completedOnly = false; // Boolean | Requests a list of transactions that have completed the approvals process. Default is false (all transactions).
        String responseType = "detailed"; // String | Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields. 
        try {
            ApiResponse<List<TransactionListItem>> response = apiInstance.listTransactionsWithHttpInfo(xApiVersion, count, order, sinceTransactionId, startDate, endDate, completedOnly, responseType);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling TransactionsApi#listTransactions");
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
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |
| **count** | **Integer**| Number of transactions to return per page | [optional] [default to 20] |
| **order** | **String**| Sort order for results. Default is asc. | [optional] [default to asc] [enum: asc, desc] |
| **sinceTransactionId** | **String**| Return transactions after this transaction ID (for pagination) | [optional] |
| **startDate** | **OffsetDateTime**| Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional] |
| **endDate** | **OffsetDateTime**| End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional] |
| **completedOnly** | **Boolean**| Requests a list of transactions that have completed the approvals process. Default is false (all transactions). | [optional] [default to false] |
| **responseType** | **String**| Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields.  | [optional] [default to detailed] [enum: detailed, simplified] |

### Return type

ApiResponse<[**List&lt;TransactionListItem&gt;**](TransactionListItem.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved transactions |  * X-Correlation-ID -  <br>  |
| **400** | Bad request - invalid parameters or request body. Validation failures carry a &#x60;details&#x60; object keyed by the offending fields; business-rule rejections may carry &#x60;error&#x60; alone. |  * X-Correlation-ID -  <br>  |
| **401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
| **500** | Internal server error |  * X-Correlation-ID -  <br>  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

