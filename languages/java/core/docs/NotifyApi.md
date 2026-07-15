# NotifyApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**notifyRevaly**](NotifyApi.md#notifyRevaly) | **POST** /notify | Notify Revaly of payment events |
| [**notifyRevalyWithHttpInfo**](NotifyApi.md#notifyRevalyWithHttpInfo) | **POST** /notify | Notify Revaly of payment events |



## notifyRevaly

> NotifyResponse notifyRevaly(notifyRequest, xApiVersion)

Notify Revaly of payment events

Notify Revaly of payment-related events and status changes.  This endpoint allows external systems to notify Revaly about specific business events related to payments, refunds, customer recovery, and customer updates. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.NotifyApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        NotifyApi apiInstance = new NotifyApi(defaultClient);
        NotifyRequest notifyRequest = new NotifyRequest(); // NotifyRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            NotifyResponse result = apiInstance.notifyRevaly(notifyRequest, xApiVersion);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling NotifyApi#notifyRevaly");
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
| **notifyRequest** | [**NotifyRequest**](NotifyRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

[**NotifyResponse**](NotifyResponse.md)


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Notification received and processed successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **404** | Resource not found |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

## notifyRevalyWithHttpInfo

> ApiResponse<NotifyResponse> notifyRevalyWithHttpInfo(notifyRequest, xApiVersion)

Notify Revaly of payment events

Notify Revaly of payment-related events and status changes.  This endpoint allows external systems to notify Revaly about specific business events related to payments, refunds, customer recovery, and customer updates. 

### Example

```java
// Import classes:
import co.revaly.sdk.core.ApiClient;
import co.revaly.sdk.core.ApiException;
import co.revaly.sdk.core.ApiResponse;
import co.revaly.sdk.core.Configuration;
import co.revaly.sdk.core.auth.*;
import co.revaly.sdk.core.models.*;
import co.revaly.sdk.core.api.NotifyApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("https://api.revaly.co");
        
        // Configure API key authorization: ApiKeyAuth
        ApiKeyAuth ApiKeyAuth = (ApiKeyAuth) defaultClient.getAuthentication("ApiKeyAuth");
        ApiKeyAuth.setApiKey("YOUR API KEY");
        // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
        //ApiKeyAuth.setApiKeyPrefix("Token");

        NotifyApi apiInstance = new NotifyApi(defaultClient);
        NotifyRequest notifyRequest = new NotifyRequest(); // NotifyRequest | 
        String xApiVersion = "2.0"; // String | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
        try {
            ApiResponse<NotifyResponse> response = apiInstance.notifyRevalyWithHttpInfo(notifyRequest, xApiVersion);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling NotifyApi#notifyRevaly");
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
| **notifyRequest** | [**NotifyRequest**](NotifyRequest.md)|  | |
| **xApiVersion** | **String**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] [enum: 2.0, 2.1] |

### Return type

ApiResponse<[**NotifyResponse**](NotifyResponse.md)>


### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Notification received and processed successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **404** | Resource not found |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

