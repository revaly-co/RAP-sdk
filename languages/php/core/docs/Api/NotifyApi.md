# Revaly\Sdk\Core\NotifyApi

Operations for informing Revaly of events

All URIs are relative to https://api.revaly.co, except if the operation defines another base path.

| Method | HTTP request | Description |
| ------------- | ------------- | ------------- |
| [**notifyRevaly()**](NotifyApi.md#notifyRevaly) | **POST** /notify | Notify Revaly of payment events |


## `notifyRevaly()`

```php
notifyRevaly($notify_request, $x_api_version): \Revaly\Sdk\Core\Model\NotifyResponse
```

Notify Revaly of payment events

Notify Revaly of payment-related events and status changes.  This endpoint allows external systems to notify Revaly about specific business events related to payments, refunds, customer recovery, and customer updates.

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
// The API requires the `ApiKey` scheme prefix in the Authorization header:
//   Authorization: ApiKey YOUR_API_KEY
// setApiKeyPrefix joins prefix and key with a space — both calls below are required.
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'ApiKey');


$apiInstance = new Revaly\Sdk\Core\Api\NotifyApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$notify_request = {"eventType":"recordPayment","data":{"merchantTransactionId":"merch_txn_abc123","orderID":"order_456789","customerId":"customer_123","amount":2500,"currency":"USD","customerAccountNumber":"ACC-001234","disableSmsNotification":false,"disableEmailNotification":false}}; // \Revaly\Sdk\Core\Model\NotifyRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->notifyRevaly($notify_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling NotifyApi->notifyRevaly: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **notify_request** | [**\Revaly\Sdk\Core\Model\NotifyRequest**](../Model/NotifyRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\NotifyResponse**](../Model/NotifyResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)
