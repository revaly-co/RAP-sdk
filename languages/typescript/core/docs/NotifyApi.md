# NotifyApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**notifyRevaly**](NotifyApi.md#notifyrevaly) | **POST** /notify | Notify Revaly of payment events |



## notifyRevaly

> NotifyResponse notifyRevaly(notifyRequest, xApiVersion)

Notify Revaly of payment events

Notify Revaly of payment-related events and status changes.  This endpoint allows external systems to notify Revaly about specific business events related to payments, refunds, customer recovery, and customer updates. 

### Example

```ts
import {
  Configuration,
  NotifyApi,
} from '';
import type { NotifyRevalyRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    apiKey: "YOUR API KEY",
  });
  const api = new NotifyApi(config);

  const body = {
    // NotifyRequest
    notifyRequest: {"eventType":"recordPayment","data":{"merchantTransactionId":"merch_txn_abc123","orderID":"order_456789","customerId":"customer_123","amount":2500,"currency":"USD","customerAccountNumber":"ACC-001234","disableSmsNotification":false,"disableEmailNotification":false}},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies NotifyRevalyRequest;

  try {
    const data = await api.notifyRevaly(body);
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
| **notifyRequest** | [NotifyRequest](NotifyRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**NotifyResponse**](NotifyResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


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

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

