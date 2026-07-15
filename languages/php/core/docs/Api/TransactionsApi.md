# Revaly\Sdk\Core\TransactionsApi

Operations related to transactions

All URIs are relative to https://api.revaly.co, except if the operation defines another base path.

| Method | HTTP request | Description |
| ------------- | ------------- | ------------- |
| [**getTransactionById()**](TransactionsApi.md#getTransactionById) | **GET** /transactions/{transactionId} | Get transaction details |
| [**getTransactionByMerchantTransactionId()**](TransactionsApi.md#getTransactionByMerchantTransactionId) | **GET** /transactions/merchant/{merchantTransactionId} | Get transaction details by merchant transaction ID |
| [**listTransactions()**](TransactionsApi.md#listTransactions) | **GET** /transactions | List transactions |


## `getTransactionById()`

```php
getTransactionById($transaction_id, $x_api_version, $include_all_transactions): \Revaly\Sdk\Core\Model\GetTransactionById200Response
```

Get transaction details

Retrieve detailed information about a specific transaction by its ID.  This endpoint returns complete transaction data including payment method details, gateway response information, recovery data and status of transaction.

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\TransactionsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$transaction_id = 06CQR5TMB800000G0011NCFRVY37A; // string | Unique identifier for the transaction
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
$include_all_transactions = true; // bool | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned.

try {
    $result = $apiInstance->getTransactionById($transaction_id, $x_api_version, $include_all_transactions);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling TransactionsApi->getTransactionById: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **transaction_id** | **string**| Unique identifier for the transaction | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |
| **include_all_transactions** | **bool**| When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned. | [optional] |

### Return type

[**\Revaly\Sdk\Core\Model\GetTransactionById200Response**](../Model/GetTransactionById200Response.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `getTransactionByMerchantTransactionId()`

```php
getTransactionByMerchantTransactionId($merchant_transaction_id, $x_api_version, $include_all_transactions): \Revaly\Sdk\Core\Model\GetTransactionByMerchantTransactionId200Response
```

Get transaction details by merchant transaction ID

Retrieve detailed information about a specific transaction by its merchant transaction ID.  This endpoint returns complete transaction data including payment method details, gateway response information, recovery data and status of transaction using the merchant-provided transaction identifier.  **Inline-retry resolution:** platform-initiated inline retry attempts carry platform-assigned transaction identifiers. This lookup resolves the payment submitted under the merchant id and returns its definitive (latest) attempt, so an approval won on a retry is found under the id the merchant submitted. In that case the returned `merchantTransactionId` is the platform-assigned attempt id rather than the path value; use the grouped view (`includeAllTransactions=true`) to list every attempt.  **Pending intent:** when the platform has accepted a payment with this merchantTransactionId (intent recorded before gateway dispatch) but no transaction record is visible yet, the lookup returns a `PendingTransactionResponse` (`state: pending`) instead of 404 — hold and re-poll until it resolves to the full transaction. A 404 means no payment with this id was ever accepted. Pending intents are not returned on the grouped view (`includeAllTransactions=true`), which lists only visible transaction records.

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\TransactionsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$merchant_transaction_id = merchant_auth_12345638934760478405277; // string | Merchant-provided unique identifier for the transaction
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
$include_all_transactions = true; // bool | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned.

try {
    $result = $apiInstance->getTransactionByMerchantTransactionId($merchant_transaction_id, $x_api_version, $include_all_transactions);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling TransactionsApi->getTransactionByMerchantTransactionId: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **merchant_transaction_id** | **string**| Merchant-provided unique identifier for the transaction | |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |
| **include_all_transactions** | **bool**| When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned. | [optional] |

### Return type

[**\Revaly\Sdk\Core\Model\GetTransactionByMerchantTransactionId200Response**](../Model/GetTransactionByMerchantTransactionId200Response.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)

## `listTransactions()`

```php
listTransactions($x_api_version, $count, $order, $since_transaction_id, $start_date, $end_date, $completed_only, $response_type): \Revaly\Sdk\Core\Model\TransactionListItem[]
```

List transactions

Retrieve a paginated list of transactions for the authenticated account.  This endpoint returns transaction data with optional filtering and pagination support. Transactions are returned based on the specified order and count parameters.

### Example

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');


// Configure API key authorization: ApiKeyAuth
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
// Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
// $config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'Bearer');


$apiInstance = new Revaly\Sdk\Core\Api\TransactionsApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.
$count = 20; // int | Number of transactions to return per page
$order = asc; // string | Sort order for results. Default is asc.
$since_transaction_id = 06CQR5TMB800000G0011NCFRVY37A; // string | Return transactions after this transaction ID (for pagination)
$start_date = 2024-09-12T00:00:00Z; // \DateTime | Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS.
$end_date = 2024-09-13T00:00:00Z; // \DateTime | End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS.
$completed_only = true; // bool | Requests a list of transactions that have completed the approvals process. Default is false (all transactions).
$response_type = detailed; // string | Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields.

try {
    $result = $apiInstance->listTransactions($x_api_version, $count, $order, $since_transaction_id, $start_date, $end_date, $completed_only, $response_type);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling TransactionsApi->listTransactions: ', $e->getMessage(), PHP_EOL;
}
```

### Parameters

| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **x_api_version** | **string**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to &#39;2.0&#39;] |
| **count** | **int**| Number of transactions to return per page | [optional] [default to 20] |
| **order** | **string**| Sort order for results. Default is asc. | [optional] [default to &#39;asc&#39;] |
| **since_transaction_id** | **string**| Return transactions after this transaction ID (for pagination) | [optional] |
| **start_date** | **\DateTime**| Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional] |
| **end_date** | **\DateTime**| End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional] |
| **completed_only** | **bool**| Requests a list of transactions that have completed the approvals process. Default is false (all transactions). | [optional] [default to false] |
| **response_type** | **string**| Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields. | [optional] [default to &#39;detailed&#39;] |

### Return type

[**\Revaly\Sdk\Core\Model\TransactionListItem[]**](../Model/TransactionListItem.md)

### Authorization

[ApiKeyAuth](../../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

[[Back to top]](#) [[Back to API list]](../../README.md#endpoints)
[[Back to Model list]](../../README.md#models)
[[Back to README]](../../README.md)
