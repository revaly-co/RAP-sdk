# Revaly\Sdk\Core\PaymentMethodsApi



All URIs are relative to https://api.revaly.co, except if the operation defines another base path.

| Method | HTTP request | Description |
| ------------- | ------------- | ------------- |
| [**createPaymentMethod()**](PaymentMethodsApi.md#createPaymentMethod) | **POST** /payment-methods/create | Create a payment method |
| [**getPaymentMethod()**](PaymentMethodsApi.md#getPaymentMethod) | **GET** /payment-methods/show/{paymentMethodId} | Get payment method details |
| [**listPaymentMethods()**](PaymentMethodsApi.md#listPaymentMethods) | **GET** /payment-methods/list | List payment methods |
| [**recachePaymentMethod()**](PaymentMethodsApi.md#recachePaymentMethod) | **POST** /payment-methods/recache/{paymentMethodId} | Recache payment method |
| [**redactPaymentMethod()**](PaymentMethodsApi.md#redactPaymentMethod) | **POST** /payment-methods/redact/{paymentMethodId} | Redact payment method |
| [**updatePaymentMethod()**](PaymentMethodsApi.md#updatePaymentMethod) | **POST** /payment-methods/update/{paymentMethodId} | Update payment method |


## `createPaymentMethod()`

```php
createPaymentMethod($create_payment_method_request, $x_api_version): \Revaly\Sdk\Core\Model\PaymentMethodWriteResponse
```

Create a payment method

Create and store a payment method in the vault. Supports both credit card details  and gatewayPaymentMethodIds from supported payment processors.  **Payment Method Types:** - **creditCard**: Credit card details that will be tokenized and stored - **gatewayPaymentMethodId**: Pre-existing gatewayPaymentMethodId from a supported payment gateway

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\PaymentMethodsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$create_payment_method_request = {"paymentMethodType":"creditCard","customerId":"customer_123456","paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}}}; // \Revaly\Sdk\Core\Model\CreatePaymentMethodRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->createPaymentMethod($create_payment_method_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentMethodsApi->createPaymentMethod: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **create_payment_method_request** | [**\Revaly\Sdk\Core\Model\CreatePaymentMethodRequest**](../Model/CreatePaymentMethodRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\PaymentMethodWriteResponse**](../Model/PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `getPaymentMethod()`

```php
getPaymentMethod($payment_method_id, $x_api_version): \Revaly\Sdk\Core\Model\PaymentMethodResponse
```

Get payment method details

Retrieve detailed information about a specific payment method.  Returns payment method data with sensitive information masked for security.

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\PaymentMethodsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$payment_method_id = 7DA6XQ33AIPUZLLDAGMXYHNTG434uyt; // string | Unique identifier for the payment method
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->getPaymentMethod($payment_method_id, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentMethodsApi->getPaymentMethod: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **payment_method_id** | **string**| Unique identifier for the payment method | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\PaymentMethodResponse**](../Model/PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `listPaymentMethods()`

```php
listPaymentMethods($x_api_version, $count, $order, $since_payment_method_id): \Revaly\Sdk\Core\Model\PaymentMethodResponse[]
```

List payment methods

Retrieve a paginated list of stored payment methods.  Returns payment methods with sensitive information masked for security. Use pagination parameters to navigate through large result sets.

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\PaymentMethodsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
$count = 20; // int | Number of payment methods to return
$order = asc; // string | Sort order for results
$since_payment_method_id = 7DA6XQ33AIPUZLLDAGMXYHNTG4; // string | Return payment methods after this ID (for pagination)

try {
    $result = $apiInstance->listPaymentMethods($x_api_version, $count, $order, $since_payment_method_id);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentMethodsApi->listPaymentMethods: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |
| **count** | **int**| Number of payment methods to return | [optional] [default to 20] |
| **order** | **string**| Sort order for results | [optional] [default to &#39;asc&#39;] |
| **since_payment_method_id** | **string**| Return payment methods after this ID (for pagination) | [optional] |

### Return type

[**\Revaly\Sdk\Core\Model\PaymentMethodResponse[]**](../Model/PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `recachePaymentMethod()`

```php
recachePaymentMethod($payment_method_id, $payment_method_recache_request, $x_api_version): \Revaly\Sdk\Core\Model\PaymentMethodWriteResponse
```

Recache payment method

Update a credit card verification value (CVV) so the card can be transacted against

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\PaymentMethodsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$payment_method_id = 7DA6XQ33AIPUZLLDAGMXYHNTG4; // string | Unique identifier for the payment method
$payment_method_recache_request = {"paymentMethod":{"creditCard":{"verificationValue":"123"}}}; // \Revaly\Sdk\Core\Model\PaymentMethodRecacheRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->recachePaymentMethod($payment_method_id, $payment_method_recache_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentMethodsApi->recachePaymentMethod: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **payment_method_id** | **string**| Unique identifier for the payment method | |
| **payment_method_recache_request** | [**\Revaly\Sdk\Core\Model\PaymentMethodRecacheRequest**](../Model/PaymentMethodRecacheRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\PaymentMethodWriteResponse**](../Model/PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `redactPaymentMethod()`

```php
redactPaymentMethod($payment_method_id, $x_api_version): \Revaly\Sdk\Core\Model\PaymentMethodWriteResponse
```

Redact payment method

Redact sensitive payment method information for compliance purposes.  This operation permanently removes sensitive data while keeping the payment method record for historical and reporting purposes. This action cannot be undone.

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\PaymentMethodsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$payment_method_id = 7DA6XQ33AIPUZLLDAGMXYHNTG4; // string | Unique identifier for the payment method
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->redactPaymentMethod($payment_method_id, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentMethodsApi->redactPaymentMethod: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **payment_method_id** | **string**| Unique identifier for the payment method | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\PaymentMethodWriteResponse**](../Model/PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `updatePaymentMethod()`

```php
updatePaymentMethod($payment_method_id, $update_payment_method_request, $x_api_version): \Revaly\Sdk\Core\Model\PaymentMethodWriteResponse
```

Update payment method

Update an existing payment method's information.  Allows updating billing information, expiration dates, and other non-sensitive data. Sensitive card data cannot be updated directly.

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\PaymentMethodsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$payment_method_id = 7DA6XQ33AIPUZLLDAGMXYHNTG4; // string | Unique identifier for the payment method
$update_payment_method_request = {"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe.updated@example.com","billingAddress":{"address1":"456 Oak Avenue","city":"Los Angeles","state":"CA","zip":"90210","country":"US","phoneNumber":"+1-555-987-6543"},"shippingAddress":{"address1":"789 Pine Street","city":"Los Angeles","state":"CA","zip":"90211","country":"US","phoneNumber":"+1-555-654-3210"}}}; // \Revaly\Sdk\Core\Model\UpdatePaymentMethodRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->updatePaymentMethod($payment_method_id, $update_payment_method_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentMethodsApi->updatePaymentMethod: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **payment_method_id** | **string**| Unique identifier for the payment method | |
| **update_payment_method_request** | [**\Revaly\Sdk\Core\Model\UpdatePaymentMethodRequest**](../Model/UpdatePaymentMethodRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\PaymentMethodWriteResponse**](../Model/PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)
