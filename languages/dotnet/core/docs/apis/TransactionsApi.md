# Revaly.Sdk.Core.Api.TransactionsApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|--------|--------------|-------------|
| [**GetTransactionById**](TransactionsApi.md#gettransactionbyid) | **GET** /transactions/{transactionId} | Get transaction details |
| [**GetTransactionByMerchantTransactionId**](TransactionsApi.md#gettransactionbymerchanttransactionid) | **GET** /transactions/merchant/{merchantTransactionId} | Get transaction details by merchant transaction ID |
| [**ListTransactions**](TransactionsApi.md#listtransactions) | **GET** /transactions | List transactions |

<a id="gettransactionbyid"></a>
# **GetTransactionById**
> GetTransactionById200Response GetTransactionById (string transactionId, string xApiVersion = null, bool includeAllTransactions = null)

Get transaction details

Retrieve detailed information about a specific transaction by its ID.  This endpoint returns complete transaction data including payment method details, gateway response information, recovery data and status of transaction. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **transactionId** | **string** | Unique identifier for the transaction |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |
| **includeAllTransactions** | **bool** | When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | [optional]  |

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

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="gettransactionbymerchanttransactionid"></a>
# **GetTransactionByMerchantTransactionId**
> GetTransactionByMerchantTransactionId200Response GetTransactionByMerchantTransactionId (string merchantTransactionId, string xApiVersion = null, bool includeAllTransactions = null)

Get transaction details by merchant transaction ID

Retrieve detailed information about a specific transaction by its merchant transaction ID.  This endpoint returns complete transaction data including payment method details, gateway response information, recovery data and status of transaction using the merchant-provided transaction identifier.  **Inline-retry resolution:** platform-initiated inline retry attempts carry platform-assigned transaction identifiers. This lookup resolves the payment submitted under the merchant id and returns its definitive (latest) attempt, so an approval won on a retry is found under the id the merchant submitted. In that case the returned `merchantTransactionId` is the platform-assigned attempt id rather than the path value; use the grouped view (`includeAllTransactions=true`) to list every attempt.  **Pending intent:** when the platform has accepted a payment with this merchantTransactionId (intent recorded before gateway dispatch) but no transaction record is visible yet, the lookup returns a `PendingTransactionResponse` (`state: pending`) instead of 404 — hold and re-poll until it resolves to the full transaction. A 404 means no payment with this id was ever accepted. Pending intents are not returned on the grouped view (`includeAllTransactions=true`), which lists only visible transaction records. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **merchantTransactionId** | **string** | Merchant-provided unique identifier for the transaction |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |
| **includeAllTransactions** | **bool** | When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | [optional]  |

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

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="listtransactions"></a>
# **ListTransactions**
> List&lt;TransactionListItem&gt; ListTransactions (string xApiVersion = null, int count = null, string order = null, string sinceTransactionId = null, DateTime startDate = null, DateTime endDate = null, bool completedOnly = null, string responseType = null)

List transactions

Retrieve a paginated list of transactions for the authenticated account.  This endpoint returns transaction data with optional filtering and pagination support. Transactions are returned based on the specified order and count parameters. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |
| **count** | **int** | Number of transactions to return per page | [optional] [default to 20] |
| **order** | **string** | Sort order for results. Default is asc. | [optional] [default to asc] |
| **sinceTransactionId** | **string** | Return transactions after this transaction ID (for pagination) | [optional]  |
| **startDate** | **DateTime** | Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional]  |
| **endDate** | **DateTime** | End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | [optional]  |
| **completedOnly** | **bool** | Requests a list of transactions that have completed the approvals process. Default is false (all transactions). | [optional] [default to false] |
| **responseType** | **string** | Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields.  | [optional] [default to detailed] |

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

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

