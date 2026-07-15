# PaymentMethodsApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createPaymentMethod**](PaymentMethodsApi.md#createPaymentMethod) | **POST** /payment-methods/create | Create a payment method |
| [**createPaymentMethodWithHttpInfo**](PaymentMethodsApi.md#createPaymentMethodWithHttpInfo) | **POST** /payment-methods/create | Create a payment method |
| [**getPaymentMethod**](PaymentMethodsApi.md#getPaymentMethod) | **GET** /payment-methods/show/{paymentMethodId} | Get payment method details |
| [**getPaymentMethodWithHttpInfo**](PaymentMethodsApi.md#getPaymentMethodWithHttpInfo) | **GET** /payment-methods/show/{paymentMethodId} | Get payment method details |
| [**listPaymentMethods**](PaymentMethodsApi.md#listPaymentMethods) | **GET** /payment-methods/list | List payment methods |
| [**listPaymentMethodsWithHttpInfo**](PaymentMethodsApi.md#listPaymentMethodsWithHttpInfo) | **GET** /payment-methods/list | List payment methods |
| [**recachePaymentMethod**](PaymentMethodsApi.md#recachePaymentMethod) | **POST** /payment-methods/recache/{paymentMethodId} | Recache payment method |
| [**recachePaymentMethodWithHttpInfo**](PaymentMethodsApi.md#recachePaymentMethodWithHttpInfo) | **POST** /payment-methods/recache/{paymentMethodId} | Recache payment method |
| [**redactPaymentMethod**](PaymentMethodsApi.md#redactPaymentMethod) | **POST** /payment-methods/redact/{paymentMethodId} | Redact payment method |
| [**redactPaymentMethodWithHttpInfo**](PaymentMethodsApi.md#redactPaymentMethodWithHttpInfo) | **POST** /payment-methods/redact/{paymentMethodId} | Redact payment method |
| [**updatePaymentMethod**](PaymentMethodsApi.md#updatePaymentMethod) | **POST** /payment-methods/update/{paymentMethodId} | Update payment method |
| [**updatePaymentMethodWithHttpInfo**](PaymentMethodsApi.md#updatePaymentMethodWithHttpInfo) | **POST** /payment-methods/update/{paymentMethodId} | Update payment method |



## createPaymentMethod

> PaymentMethodWriteResponse createPaymentMethod(createPaymentMethodRequest, xApiVersion)

Create a payment method

Create and store a payment method in the vault. Supports both credit card details  and gatewayPaymentMethodIds from supported payment processors.  **Payment Method Types:** - **creditCard**: Credit card details that will be tokenized and stored - **gatewayPaymentMethodId**: Pre-existing gatewayPaymentMethodId from a supported payment gateway 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        CreatePaymentMethodRequest createPaymentMethodRequest = new CreatePaymentMethodRequest(); // CreatePaymentMethodRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            PaymentMethodWriteResponse result = apiInstance.createPaymentMethod(createPaymentMethodRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#createPaymentMethod");
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
| **createPaymentMethodRequest** | [**CreatePaymentMethodRequest**](CreatePaymentMethodRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method successfully created |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

## createPaymentMethodWithHttpInfo

> ApiResponse<PaymentMethodWriteResponse> createPaymentMethodWithHttpInfo(createPaymentMethodRequest, xApiVersion)

Create a payment method

Create and store a payment method in the vault. Supports both credit card details  and gatewayPaymentMethodIds from supported payment processors.  **Payment Method Types:** - **creditCard**: Credit card details that will be tokenized and stored - **gatewayPaymentMethodId**: Pre-existing gatewayPaymentMethodId from a supported payment gateway 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        CreatePaymentMethodRequest createPaymentMethodRequest = new CreatePaymentMethodRequest(); // CreatePaymentMethodRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<PaymentMethodWriteResponse> response = apiInstance.createPaymentMethodWithHttpInfo(createPaymentMethodRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#createPaymentMethod");
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
| **createPaymentMethodRequest** | [**CreatePaymentMethodRequest**](CreatePaymentMethodRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method successfully created |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |


## getPaymentMethod

> PaymentMethodResponse getPaymentMethod(paymentMethodId, xApiVersion)

Get payment method details

Retrieve detailed information about a specific payment method.  Returns payment method data with sensitive information masked for security. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String paymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG434uyt"; // String | Unique identifier for the payment method
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            PaymentMethodResponse result = apiInstance.getPaymentMethod(paymentMethodId, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#getPaymentMethod");
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
| **paymentMethodId** | **String**| Unique identifier for the payment method | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

[**PaymentMethodResponse**](PaymentMethodResponse.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved payment method details |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **404** | Resource not found |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

## getPaymentMethodWithHttpInfo

> ApiResponse<PaymentMethodResponse> getPaymentMethodWithHttpInfo(paymentMethodId, xApiVersion)

Get payment method details

Retrieve detailed information about a specific payment method.  Returns payment method data with sensitive information masked for security. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String paymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG434uyt"; // String | Unique identifier for the payment method
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<PaymentMethodResponse> response = apiInstance.getPaymentMethodWithHttpInfo(paymentMethodId, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#getPaymentMethod");
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
| **paymentMethodId** | **String**| Unique identifier for the payment method | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**PaymentMethodResponse**](PaymentMethodResponse.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved payment method details |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **404** | Resource not found |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |


## listPaymentMethods

> List<PaymentMethodResponse> listPaymentMethods(xApiVersion, count, order, sincePaymentMethodId)

List payment methods

Retrieve a paginated list of stored payment methods.  Returns payment methods with sensitive information masked for security. Use pagination parameters to navigate through large result sets. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        Integer count = 20; // Integer | Number of payment methods to return
        String order = "asc"; // String | Sort order for results
        String sincePaymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG4"; // String | Return payment methods after this ID (for pagination)
        try {
            List<PaymentMethodResponse> result = apiInstance.listPaymentMethods(xApiVersion, count, order, sincePaymentMethodId);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#listPaymentMethods");
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
| **count** | **Integer**| Number of payment methods to return | [optional] [default to 20] |
| **order** | **String**| Sort order for results | [optional] [default to asc] [enum: asc, desc] |
| **sincePaymentMethodId** | **String**| Return payment methods after this ID (for pagination) | [optional] |

### Return type

[**List&lt;PaymentMethodResponse&gt;**](PaymentMethodResponse.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved payment methods |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

## listPaymentMethodsWithHttpInfo

> ApiResponse<List<PaymentMethodResponse>> listPaymentMethodsWithHttpInfo(xApiVersion, count, order, sincePaymentMethodId)

List payment methods

Retrieve a paginated list of stored payment methods.  Returns payment methods with sensitive information masked for security. Use pagination parameters to navigate through large result sets. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        Integer count = 20; // Integer | Number of payment methods to return
        String order = "asc"; // String | Sort order for results
        String sincePaymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG4"; // String | Return payment methods after this ID (for pagination)
        try {
            ApiResponse<List<PaymentMethodResponse>> response = apiInstance.listPaymentMethodsWithHttpInfo(xApiVersion, count, order, sincePaymentMethodId);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#listPaymentMethods");
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
| **count** | **Integer**| Number of payment methods to return | [optional] [default to 20] |
| **order** | **String**| Sort order for results | [optional] [default to asc] [enum: asc, desc] |
| **sincePaymentMethodId** | **String**| Return payment methods after this ID (for pagination) | [optional] |

### Return type

ApiResponse<[**List&lt;PaymentMethodResponse&gt;**](PaymentMethodResponse.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved payment methods |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |


## recachePaymentMethod

> PaymentMethodWriteResponse recachePaymentMethod(paymentMethodId, paymentMethodRecacheRequest, xApiVersion)

Recache payment method

Update a credit card verification value (CVV) so the card can be transacted against     

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String paymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG4"; // String | Unique identifier for the payment method
        PaymentMethodRecacheRequest paymentMethodRecacheRequest = new PaymentMethodRecacheRequest(); // PaymentMethodRecacheRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            PaymentMethodWriteResponse result = apiInstance.recachePaymentMethod(paymentMethodId, paymentMethodRecacheRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#recachePaymentMethod");
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
| **paymentMethodId** | **String**| Unique identifier for the payment method | |
| **paymentMethodRecacheRequest** | [**PaymentMethodRecacheRequest**](PaymentMethodRecacheRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method recached successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

## recachePaymentMethodWithHttpInfo

> ApiResponse<PaymentMethodWriteResponse> recachePaymentMethodWithHttpInfo(paymentMethodId, paymentMethodRecacheRequest, xApiVersion)

Recache payment method

Update a credit card verification value (CVV) so the card can be transacted against     

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String paymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG4"; // String | Unique identifier for the payment method
        PaymentMethodRecacheRequest paymentMethodRecacheRequest = new PaymentMethodRecacheRequest(); // PaymentMethodRecacheRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<PaymentMethodWriteResponse> response = apiInstance.recachePaymentMethodWithHttpInfo(paymentMethodId, paymentMethodRecacheRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#recachePaymentMethod");
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
| **paymentMethodId** | **String**| Unique identifier for the payment method | |
| **paymentMethodRecacheRequest** | [**PaymentMethodRecacheRequest**](PaymentMethodRecacheRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method recached successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |


## redactPaymentMethod

> PaymentMethodWriteResponse redactPaymentMethod(paymentMethodId, xApiVersion)

Redact payment method

Redact sensitive payment method information for compliance purposes.  This operation permanently removes sensitive data while keeping the payment method record for historical and reporting purposes. This action cannot be undone. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String paymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG4"; // String | Unique identifier for the payment method
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            PaymentMethodWriteResponse result = apiInstance.redactPaymentMethod(paymentMethodId, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#redactPaymentMethod");
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
| **paymentMethodId** | **String**| Unique identifier for the payment method | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method redacted successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

## redactPaymentMethodWithHttpInfo

> ApiResponse<PaymentMethodWriteResponse> redactPaymentMethodWithHttpInfo(paymentMethodId, xApiVersion)

Redact payment method

Redact sensitive payment method information for compliance purposes.  This operation permanently removes sensitive data while keeping the payment method record for historical and reporting purposes. This action cannot be undone. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String paymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG4"; // String | Unique identifier for the payment method
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<PaymentMethodWriteResponse> response = apiInstance.redactPaymentMethodWithHttpInfo(paymentMethodId, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#redactPaymentMethod");
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
| **paymentMethodId** | **String**| Unique identifier for the payment method | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method redacted successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |


## updatePaymentMethod

> PaymentMethodWriteResponse updatePaymentMethod(paymentMethodId, updatePaymentMethodRequest, xApiVersion)

Update payment method

Update an existing payment method&#39;s information.  Allows updating billing information, expiration dates, and other non-sensitive data. Sensitive card data cannot be updated directly. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String paymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG4"; // String | Unique identifier for the payment method
        UpdatePaymentMethodRequest updatePaymentMethodRequest = new UpdatePaymentMethodRequest(); // UpdatePaymentMethodRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            PaymentMethodWriteResponse result = apiInstance.updatePaymentMethod(paymentMethodId, updatePaymentMethodRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#updatePaymentMethod");
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
| **paymentMethodId** | **String**| Unique identifier for the payment method | |
| **updatePaymentMethodRequest** | [**UpdatePaymentMethodRequest**](UpdatePaymentMethodRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method updated successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

## updatePaymentMethodWithHttpInfo

> ApiResponse<PaymentMethodWriteResponse> updatePaymentMethodWithHttpInfo(paymentMethodId, updatePaymentMethodRequest, xApiVersion)

Update payment method

Update an existing payment method&#39;s information.  Allows updating billing information, expiration dates, and other non-sensitive data. Sensitive card data cannot be updated directly. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.PaymentMethodsApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        PaymentMethodsApi apiInstance = new PaymentMethodsApi(defaultClient);
        String paymentMethodId = "7DA6XQ33AIPUZLLDAGMXYHNTG4"; // String | Unique identifier for the payment method
        UpdatePaymentMethodRequest updatePaymentMethodRequest = new UpdatePaymentMethodRequest(); // UpdatePaymentMethodRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<PaymentMethodWriteResponse> response = apiInstance.updatePaymentMethodWithHttpInfo(paymentMethodId, updatePaymentMethodRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling PaymentMethodsApi#updatePaymentMethod");
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
| **paymentMethodId** | **String**| Unique identifier for the payment method | |
| **updatePaymentMethodRequest** | [**UpdatePaymentMethodRequest**](UpdatePaymentMethodRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method updated successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

