# \TransactionsAPI

All URIs are relative to *https://api.revaly.co*

Method | HTTP request | Description
------------- | ------------- | -------------
[**GetTransactionById**](TransactionsAPI.md#GetTransactionById) | **Get** /transactions/{transactionId} | Get transaction details
[**GetTransactionByMerchantTransactionId**](TransactionsAPI.md#GetTransactionByMerchantTransactionId) | **Get** /transactions/merchant/{merchantTransactionId} | Get transaction details by merchant transaction ID
[**ListTransactions**](TransactionsAPI.md#ListTransactions) | **Get** /transactions | List transactions



## GetTransactionById

> GetTransactionById200Response GetTransactionById(ctx, transactionId).XApiVersion(xApiVersion).IncludeAllTransactions(includeAllTransactions).Execute()

Get transaction details



### Example

```go
package main

import (
	"context"
	"fmt"
	"os"
	openapiclient "github.com/GIT_USER_ID/GIT_REPO_ID"
)

func main() {
	transactionId := "06CQR5TMB800000G0011NCFRVY37A" // string | Unique identifier for the transaction
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")
	includeAllTransactions := true // bool | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned.  (optional)

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.TransactionsAPI.GetTransactionById(context.Background(), transactionId).XApiVersion(xApiVersion).IncludeAllTransactions(includeAllTransactions).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `TransactionsAPI.GetTransactionById``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `GetTransactionById`: GetTransactionById200Response
	fmt.Fprintf(os.Stdout, "Response from `TransactionsAPI.GetTransactionById`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**transactionId** | **string** | Unique identifier for the transaction | 

### Other Parameters

Other parameters are passed through a pointer to a apiGetTransactionByIdRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]
 **includeAllTransactions** | **bool** | When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | 

### Return type

[**GetTransactionById200Response**](GetTransactionById200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## GetTransactionByMerchantTransactionId

> GetTransactionByMerchantTransactionId200Response GetTransactionByMerchantTransactionId(ctx, merchantTransactionId).XApiVersion(xApiVersion).IncludeAllTransactions(includeAllTransactions).Execute()

Get transaction details by merchant transaction ID



### Example

```go
package main

import (
	"context"
	"fmt"
	"os"
	openapiclient "github.com/GIT_USER_ID/GIT_REPO_ID"
)

func main() {
	merchantTransactionId := "merchant_auth_12345638934760478405277" // string | Merchant-provided unique identifier for the transaction
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")
	includeAllTransactions := true // bool | When `true`, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a `TransactionGroupResponse` envelope, instead of the single matching `TransactionResponse`. Supported only on repository-backed lookups; otherwise returns `400`. If the matched transaction has no initial transaction id, only that single transaction is returned.  (optional)

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.TransactionsAPI.GetTransactionByMerchantTransactionId(context.Background(), merchantTransactionId).XApiVersion(xApiVersion).IncludeAllTransactions(includeAllTransactions).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `TransactionsAPI.GetTransactionByMerchantTransactionId``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `GetTransactionByMerchantTransactionId`: GetTransactionByMerchantTransactionId200Response
	fmt.Fprintf(os.Stdout, "Response from `TransactionsAPI.GetTransactionByMerchantTransactionId`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**merchantTransactionId** | **string** | Merchant-provided unique identifier for the transaction | 

### Other Parameters

Other parameters are passed through a pointer to a apiGetTransactionByMerchantTransactionIdRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]
 **includeAllTransactions** | **bool** | When &#x60;true&#x60;, returns every transaction belonging to the same payment (all attempts and lifecycle operations sharing the initial transaction id) as a &#x60;TransactionGroupResponse&#x60; envelope, instead of the single matching &#x60;TransactionResponse&#x60;. Supported only on repository-backed lookups; otherwise returns &#x60;400&#x60;. If the matched transaction has no initial transaction id, only that single transaction is returned.  | 

### Return type

[**GetTransactionByMerchantTransactionId200Response**](GetTransactionByMerchantTransactionId200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## ListTransactions

> []TransactionListItem ListTransactions(ctx).XApiVersion(xApiVersion).Count(count).Order(order).SinceTransactionId(sinceTransactionId).StartDate(startDate).EndDate(endDate).CompletedOnly(completedOnly).ResponseType(responseType).Execute()

List transactions



### Example

```go
package main

import (
	"context"
	"fmt"
	"os"
    "time"
	openapiclient "github.com/GIT_USER_ID/GIT_REPO_ID"
)

func main() {
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")
	count := int32(20) // int32 | Number of transactions to return per page (optional) (default to 20)
	order := "asc" // string | Sort order for results. Default is asc. (optional) (default to "asc")
	sinceTransactionId := "06CQR5TMB800000G0011NCFRVY37A" // string | Return transactions after this transaction ID (for pagination) (optional)
	startDate := time.Now() // time.Time | Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. (optional)
	endDate := time.Now() // time.Time | End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. (optional)
	completedOnly := true // bool | Requests a list of transactions that have completed the approvals process. Default is false (all transactions). (optional) (default to false)
	responseType := "detailed" // string | Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields.  (optional) (default to "detailed")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.TransactionsAPI.ListTransactions(context.Background()).XApiVersion(xApiVersion).Count(count).Order(order).SinceTransactionId(sinceTransactionId).StartDate(startDate).EndDate(endDate).CompletedOnly(completedOnly).ResponseType(responseType).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `TransactionsAPI.ListTransactions``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `ListTransactions`: []TransactionListItem
	fmt.Fprintf(os.Stdout, "Response from `TransactionsAPI.ListTransactions`: %v\n", resp)
}
```

### Path Parameters



### Other Parameters

Other parameters are passed through a pointer to a apiListTransactionsRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]
 **count** | **int32** | Number of transactions to return per page | [default to 20]
 **order** | **string** | Sort order for results. Default is asc. | [default to &quot;asc&quot;]
 **sinceTransactionId** | **string** | Return transactions after this transaction ID (for pagination) | 
 **startDate** | **time.Time** | Start of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | 
 **endDate** | **time.Time** | End of the date range for returned transactions. Format YYYY-MM-DDTHH:MM:SS. | 
 **completedOnly** | **bool** | Requests a list of transactions that have completed the approvals process. Default is false (all transactions). | [default to false]
 **responseType** | **string** | Determines response verbosity. simplified returns limited fields (transactionId, transactionDate, transactionStatus, responseCode, message, transactionType, retryDate, amount, initialMerchantTransactionId, paymentMethodStorageState, completionStatus). detailed returns all available fields.  | [default to &quot;detailed&quot;]

### Return type

[**[]TransactionListItem**](TransactionListItem.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)

