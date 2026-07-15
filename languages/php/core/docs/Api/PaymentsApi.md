# Revaly\Sdk\Core\PaymentsApi

Operations related to processing payments

All URIs are relative to https://api.revaly.co, except if the operation defines another base path.

| Method | HTTP request | Description |
| ------------- | ------------- | ------------- |
| [**authorizePayment()**](PaymentsApi.md#authorizePayment) | **POST** /payments/authorize | Authorize a payment |
| [**capturePayment()**](PaymentsApi.md#capturePayment) | **POST** /payments/capture/{transactionId} | Capture an authorized payment |
| [**chargePayment()**](PaymentsApi.md#chargePayment) | **POST** /payments | Process a payment (charge) |
| [**refundCancelPaymentByMerchantTransactionId()**](PaymentsApi.md#refundCancelPaymentByMerchantTransactionId) | **POST** /payments/refund-cancel/merchant/{merchantTransactionId} | Refund or cancel a payment transaction by merchant transaction ID |
| [**refundPayment()**](PaymentsApi.md#refundPayment) | **POST** /payments/refund/{transactionId} | Refund a payment transaction by TransactionId |
| [**voidPayment()**](PaymentsApi.md#voidPayment) | **POST** /payments/void/{transactionId} | Void a payment transaction |


## `authorizePayment()`

```php
authorizePayment($authorize_request, $x_api_version): \Revaly\Sdk\Core\Model\TransactionResponse
```

Authorize a payment

Authorize a payment without immediately capturing funds.  This endpoint creates an authorization hold on the customer's payment method. The authorized amount can later be captured using the capture endpoint.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id  To charge a previously stored payment method, omit `paymentMethodType` and supply `paymentMethod.paymentMethodId`.

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


$apiInstance = new Revaly\Sdk\Core\Api\PaymentsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$authorize_request = {"paymentMethodType":"creditCard","gatewayRoutingId":"PCFXF23ORZJEXMJLXJZCDISP6A","amount":2500,"merchantTransactionId":"auth_order_12345","mitStoredTransactionId":"mit_txn_001","initiatedBy":"MIT","currency":"USD","customerId":"customer_123456","customerIp":"192.168.1.100","orderId":"order_67890","description":"Authorization for subscription renewal","storeOnSuccess":true,"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025","cardType":"visa"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}},"threeDS":{"version":"2.2.0","exemptionType":"low_value","eci":"05","cryptogram":"BwABBJQ1AgAAAAAgJDUCAAAAAAA=","dsTransactionId":"c7aa28c2-e2c5-4e5c-a9d3-2f8b3c4d5e6f","acsTransactionId":"d8bb39d3-f3d6-5f6d-b0e4-3f9c4d5e6f70","xid":"MDAwMDAwMDAwMDAwMDAwMzIyNzY=","cavvAlgorithm":"1","directoryStatus":"Y","authenticationStatus":"Y","enrolledStatus":"Y","serverTransId":"e9cc40e4-04e7-6076-c1f5-409d5e6f7081"},"recovery":{"disableCustomerRecovery":false,"customerAccountNumber":"ACC-456789","customerBalance":1922,"disableSMSNotification":false,"disableEmailNotification":false,"retryCount":1,"paymentReferenceData":"initial_txn_ref_456","dateFirstAttempt":"2025-01-10T08:00:00Z"},"paymentPlanData":{"sku":"PREMIUM_MONTHLY","category":"FDT","billingPlan":"monthly","billingCycle":1,"productDisplayName":"Premium Monthly Plan","paymentModel":"recurring","subscriptionId":"sub_abc123def456"}}; // \Revaly\Sdk\Core\Model\AuthorizeRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->authorizePayment($authorize_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentsApi->authorizePayment: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **authorize_request** | [**\Revaly\Sdk\Core\Model\AuthorizeRequest**](../Model/AuthorizeRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\TransactionResponse**](../Model/TransactionResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `capturePayment()`

```php
capturePayment($transaction_id, $capture_request, $x_api_version): \Revaly\Sdk\Core\Model\TransactionResponse
```

Capture an authorized payment

Capture funds from a previously authorized payment transaction.  This endpoint captures the full or partial amount from an authorization. Once captured, the funds will be settled to your account.

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


$apiInstance = new Revaly\Sdk\Core\Api\PaymentsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$transaction_id = 06CQR5TMB800000G0011NCFRVY37A; // string | Unique identifier of the authorization transaction to capture
$capture_request = {"merchantTransactionId":"capture_order_12345"}; // \Revaly\Sdk\Core\Model\CaptureRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->capturePayment($transaction_id, $capture_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentsApi->capturePayment: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **transaction_id** | **string**| Unique identifier of the authorization transaction to capture | |
| **capture_request** | [**\Revaly\Sdk\Core\Model\CaptureRequest**](../Model/CaptureRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\TransactionResponse**](../Model/TransactionResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `chargePayment()`

```php
chargePayment($payment_request, $x_api_version): \Revaly\Sdk\Core\Model\TransactionResponse
```

Process a payment (charge)

Process a direct payment charge against a payment method.  This endpoint performs an immediate charge and settlement of funds. Unlike authorization, the funds are immediately captured and transferred.  **Payment Method Types:** - **creditCard**: Process using raw credit card details - **gatewayPaymentMethodId**: Process using an existing gateway payment method id  To charge a previously stored payment method, omit `paymentMethodType` and supply `paymentMethod.paymentMethodId`.

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


$apiInstance = new Revaly\Sdk\Core\Api\PaymentsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$payment_request = {"paymentMethodType":"creditCard","gatewayRoutingId":"PCFXF23ORZJEXMJLXJZCDISP6A","amount":2500,"merchantTransactionId":"charge_order_12345","mitStoredTransactionId":"mit_txn_001","initiatedBy":"MIT","currency":"USD","customerId":"customer_123456","customerIp":"192.168.1.100","orderId":"order_67890","description":"Payment for online purchase","storeOnSuccess":true,"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025","cardType":"visa"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}},"threeDS":{"version":"2.2.0","exemptionType":"low_value","eci":"05","cryptogram":"BwABBJQ1AgAAAAAgJDUCAAAAAAA=","dsTransactionId":"c7aa28c2-e2c5-4e5c-a9d3-2f8b3c4d5e6f","acsTransactionId":"d8bb39d3-f3d6-5f6d-b0e4-3f9c4d5e6f70","xid":"MDAwMDAwMDAwMDAwMDAwMzIyNzY=","cavvAlgorithm":"1","directoryStatus":"Y","authenticationStatus":"Y","enrolledStatus":"Y","serverTransId":"e9cc40e4-04e7-6076-c1f5-409d5e6f7081"},"recovery":{"disableCustomerRecovery":false,"customerAccountNumber":"ACC-456789","customerBalance":1922,"disableSMSNotification":false,"disableEmailNotification":false,"retryCount":1,"paymentReferenceData":"initial_txn_ref_456","dateFirstAttempt":"2025-01-10T08:00:00Z"},"paymentPlanData":{"sku":"PREMIUM_MONTHLY","category":"FDT","billingPlan":"monthly","billingCycle":1,"productDisplayName":"Premium Monthly Plan","paymentModel":"recurring","subscriptionId":"sub_abc123def456"}}; // \Revaly\Sdk\Core\Model\PaymentRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->chargePayment($payment_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentsApi->chargePayment: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **payment_request** | [**\Revaly\Sdk\Core\Model\PaymentRequest**](../Model/PaymentRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\TransactionResponse**](../Model/TransactionResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `refundCancelPaymentByMerchantTransactionId()`

```php
refundCancelPaymentByMerchantTransactionId($merchant_transaction_id, $refund_cancel_request, $x_api_version): \Revaly\Sdk\Core\Model\TransactionResponse
```

Refund or cancel a payment transaction by merchant transaction ID

Refund a previously settled payment transaction using Merchant Transaction ID.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer's payment method.  This endpoint also cancels payments that are currently in the Revaly approvals flow using MerchantTransactionId.

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


$apiInstance = new Revaly\Sdk\Core\Api\PaymentsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$merchant_transaction_id = merchant_auth_12345638934760478405277; // string | Merchant-provided unique identifier of the transaction to refund or cancel
$refund_cancel_request = {"merchantTransactionId":"refund_order_12345","customerId":"customer_12345"}; // \Revaly\Sdk\Core\Model\RefundCancelRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->refundCancelPaymentByMerchantTransactionId($merchant_transaction_id, $refund_cancel_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentsApi->refundCancelPaymentByMerchantTransactionId: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **merchant_transaction_id** | **string**| Merchant-provided unique identifier of the transaction to refund or cancel | |
| **refund_cancel_request** | [**\Revaly\Sdk\Core\Model\RefundCancelRequest**](../Model/RefundCancelRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\TransactionResponse**](../Model/TransactionResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `refundPayment()`

```php
refundPayment($transaction_id, $refund_request, $x_api_version): \Revaly\Sdk\Core\Model\TransactionResponse
```

Refund a payment transaction by TransactionId

Refund a previously settled payment transaction using the Revaly transactionId.  This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer's payment method.

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


$apiInstance = new Revaly\Sdk\Core\Api\PaymentsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$transaction_id = 06CQR5TMB800000G0011NCFRVY37A; // string | Unique identifier of the transaction to refund
$refund_request = {"merchantTransactionId":"refund_order_12345"}; // \Revaly\Sdk\Core\Model\RefundRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->refundPayment($transaction_id, $refund_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentsApi->refundPayment: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **transaction_id** | **string**| Unique identifier of the transaction to refund | |
| **refund_request** | [**\Revaly\Sdk\Core\Model\RefundRequest**](../Model/RefundRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\TransactionResponse**](../Model/TransactionResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `voidPayment()`

```php
voidPayment($transaction_id, $void_request, $x_api_version): \Revaly\Sdk\Core\Model\TransactionResponse
```

Void a payment transaction

Void (cancel) a payment transaction that has not yet been settled.  This endpoint cancels an authorization or unsettled sale transaction. Voided transactions cannot be captured or refunded.

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


$apiInstance = new Revaly\Sdk\Core\Api\PaymentsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$transaction_id = 06CQR5TMB800000G0011NCFRVY37A; // string | Unique identifier of the transaction to void
$void_request = {"merchantTransactionId":"void_order_12345"}; // \Revaly\Sdk\Core\Model\VoidRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->voidPayment($transaction_id, $void_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling PaymentsApi->voidPayment: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **transaction_id** | **string**| Unique identifier of the transaction to void | |
| **void_request** | [**\Revaly\Sdk\Core\Model\VoidRequest**](../Model/VoidRequest.md)|  | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\TransactionResponse**](../Model/TransactionResponse.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)
