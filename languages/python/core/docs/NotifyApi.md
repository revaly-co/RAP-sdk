# revaly_sdk_core.NotifyApi

All URIs are relative to *https://api.revaly.co*

Method | HTTP request | Description
------------- | ------------- | -------------
[**notify_revaly**](NotifyApi.md#notify_revaly) | **POST** /notify | Notify Revaly of payment events


# **notify_revaly**
> NotifyResponse notify_revaly(notify_request, x_api_version=x_api_version)

Notify Revaly of payment events

Notify Revaly of payment-related events and status changes.

This endpoint allows external systems to notify Revaly about specific
business events related to payments, refunds, customer recovery, and customer updates.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.notify_request import NotifyRequest
from revaly_sdk_core.models.notify_response import NotifyResponse
from revaly_sdk_core.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.revaly.co
# See configuration.py for a list of all supported configuration parameters.
configuration = revaly_sdk_core.Configuration(
    host = "https://api.revaly.co"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
# The API requires the `ApiKey` scheme prefix in the Authorization header:
#   Authorization: ApiKey YOUR_API_KEY
# api_key_prefix joins prefix and key with a space — both lines below are required.
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]
configuration.api_key_prefix['ApiKeyAuth'] = 'ApiKey'

# Enter a context with an instance of the API client
with revaly_sdk_core.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = revaly_sdk_core.NotifyApi(api_client)
    notify_request = {"eventType":"recordPayment","data":{"merchantTransactionId":"merch_txn_abc123","orderID":"order_456789","customerId":"customer_123","amount":2500,"currency":"USD","customerAccountNumber":"ACC-001234","disableSmsNotification":false,"disableEmailNotification":false}} # NotifyRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Notify Revaly of payment events
        api_response = api_instance.notify_revaly(notify_request, x_api_version=x_api_version)
        print("The response of NotifyApi->notify_revaly:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotifyApi->notify_revaly: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notify_request** | [**NotifyRequest**](NotifyRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

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
**200** | Notification received and processed successfully |  * X-Correlation-ID -  <br>  |
**400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
**401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
**404** | Resource not found |  * X-Correlation-ID -  <br>  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
**500** | Internal server error |  * X-Correlation-ID -  <br>  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

