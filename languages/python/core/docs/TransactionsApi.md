# revaly_sdk_core.TransactionsApi

All URIs are relative to *https://api.revaly.co*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_transaction_by_id**](TransactionsApi.md#get_transaction_by_id) | **GET** /transactions/{transactionId} | Get transaction details
[**get_transaction_by_merchant_transaction_id**](TransactionsApi.md#get_transaction_by_merchant_transaction_id) | **GET** /transactions/merchant/{merchantTransactionId} | Get transaction details by merchant transaction ID
[**list_transactions**](TransactionsApi.md#list_transactions) | **GET** /transactions | List transactions


# **get_transaction_by_id**
> GetTransactionById200Response get_transaction_by_id(transaction_id, x_api_version=x_api_version, include_all_transactions=include_all_transactions)

Get transaction details

Retrieve detailed information about a specific transaction by its ID.

This endpoint returns complete transaction data including payment method details,
gateway response information, recovery data and status of transaction.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.get_transaction_by_id200_response import GetTransactionById200Response
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
    api_instance = revaly_sdk_core.TransactionsApi(api_client)
    transaction_id = '06CQR5TMB800000G0011NCFRVY37A' # str | Unique identifier for the transaction
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)
    include_all_transactions = true # bool | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned.  (optional)

    try:
        # Get transaction details
        api_response = api_instance.get_transaction_by_id(transaction_id, x_api_version=x_api_version, include_all_transactions=include_all_transactions)
        print("The response of TransactionsApi->get_transaction_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->get_transaction_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **str**| Unique identifier for the transaction | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]
 **include_all_transactions** | **bool**| When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | [optional] 

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
**200** | Successfully retrieved transaction details. Returns a single &#x60;TransactionResponse&#x60; by default, or a &#x60;TransactionGroupResponse&#x60; envelope when &#x60;includeAllTransactions&#x3D;true&#x60;.  |  * X-Correlation-ID -  <br>  |
**400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
**401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
**404** | Resource not found |  * X-Correlation-ID -  <br>  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
**500** | Internal server error |  * X-Correlation-ID -  <br>  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transaction_by_merchant_transaction_id**
> GetTransactionByMerchantTransactionId200Response get_transaction_by_merchant_transaction_id(merchant_transaction_id, x_api_version=x_api_version, include_all_transactions=include_all_transactions)

Get transaction details by merchant transaction ID

Retrieve detailed information about a specific transaction by its merchant transaction ID.

This endpoint returns complete transaction data including payment method details,
gateway response information, recovery data and status of transaction using the
merchant-provided transaction identifier.

**Inline-retry resolution:** platform-initiated inline retry attempts carry
platform-assigned transaction identifiers. This lookup resolves the payment submitted
under the merchant id and returns its definitive (latest) attempt, so an approval won
on a retry is found under the id the merchant submitted. In that case the returned
`merchantTransactionId` is the platform-assigned attempt id rather than the path value;
use the grouped view (`includeAllTransactions=true`) to list every attempt.

**Pending intent:** when the platform has accepted a payment with this
merchantTransactionId (intent recorded before gateway dispatch) but no transaction
record is visible yet, the lookup returns a `PendingTransactionResponse`
(`state: pending`) instead of 404 — hold and re-poll until it resolves to the full
transaction. A 404 means no payment with this id was ever accepted. Pending intents
are not returned on the grouped view (`includeAllTransactions=true`), which lists
only visible transaction records.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.get_transaction_by_merchant_transaction_id200_response import GetTransactionByMerchantTransactionId200Response
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
    api_instance = revaly_sdk_core.TransactionsApi(api_client)
    merchant_transaction_id = 'merchant_auth_12345638934760478405277' # str | Merchant-provided unique identifier for the transaction
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)
    include_all_transactions = true # bool | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned.  (optional)

    try:
        # Get transaction details by merchant transaction ID
        api_response = api_instance.get_transaction_by_merchant_transaction_id(merchant_transaction_id, x_api_version=x_api_version, include_all_transactions=include_all_transactions)
        print("The response of TransactionsApi->get_transaction_by_merchant_transaction_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->get_transaction_by_merchant_transaction_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **merchant_transaction_id** | **str**| Merchant-provided unique identifier for the transaction | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]
 **include_all_transactions** | **bool**| When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | [optional] 

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
**200** | Successfully retrieved transaction details. Returns a single &#x60;TransactionResponse&#x60; by default, or a &#x60;TransactionGroupResponse&#x60; envelope when &#x60;includeAllTransactions&#x3D;true&#x60;. Returns a &#x60;PendingTransactionResponse&#x60; (&#x60;state: pending&#x60;) when the payment intent was accepted but no transaction record is visible yet.  |  * X-Correlation-ID -  <br>  |
**400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
**401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
**404** | Resource not found |  * X-Correlation-ID -  <br>  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
**500** | Internal server error |  * X-Correlation-ID -  <br>  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_transactions**
> List[TransactionListItem] list_transactions(x_api_version=x_api_version, count=count, order=order, since_transaction_id=since_transaction_id, start_date=start_date, end_date=end_date, completed_only=completed_only, response_type=response_type)

List transactions

Retrieve a paginated list of transactions for the authenticated account.

This endpoint returns transaction data with optional filtering and pagination support.
Transactions are returned based on the specified order and count parameters.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.transaction_list_item import TransactionListItem
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
    api_instance = revaly_sdk_core.TransactionsApi(api_client)
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)
    count = 20 # int | Number of transactions to return per page (optional) (default to 20)
    order = asc # str | Sort order for results. Default is asc. (optional) (default to asc)
    since_transaction_id = '06CQR5TMB800000G0011NCFRVY37A' # str | Return transactions after this transaction ID (for pagination) (optional)
    start_date = '2024-09-12T00:00:00Z' # datetime | Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. (optional)
    end_date = '2024-09-13T00:00:00Z' # datetime | End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. (optional)
    completed_only = False # bool | Requests a list of transactions that have completed the approvals process. Default is false (all transactions). (optional) (default to False)
    response_type = detailed # str | Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields.  (optional) (default to detailed)

    try:
        # List transactions
        api_response = api_instance.list_transactions(x_api_version=x_api_version, count=count, order=order, since_transaction_id=since_transaction_id, start_date=start_date, end_date=end_date, completed_only=completed_only, response_type=response_type)
        print("The response of TransactionsApi->list_transactions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->list_transactions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]
 **count** | **int**| Number of transactions to return per page | [optional] [default to 20]
 **order** | **str**| Sort order for results. Default is asc. | [optional] [default to asc]
 **since_transaction_id** | **str**| Return transactions after this transaction ID (for pagination) | [optional] 
 **start_date** | **datetime**| Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional] 
 **end_date** | **datetime**| End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional] 
 **completed_only** | **bool**| Requests a list of transactions that have completed the approvals process. Default is false (all transactions). | [optional] [default to False]
 **response_type** | **str**| Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields.  | [optional] [default to detailed]

### Return type

[**List[TransactionListItem]**](TransactionListItem.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved transactions |  * X-Correlation-ID -  <br>  |
**400** | Bad request - invalid parameters or request body |  * X-Correlation-ID -  <br>  |
**401** | Unauthorized - invalid or missing API key |  * X-Correlation-ID -  <br>  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  * X-Correlation-ID -  <br>  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  * X-Correlation-ID -  <br>  |
**500** | Internal server error |  * X-Correlation-ID -  <br>  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  * X-Correlation-ID -  <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

