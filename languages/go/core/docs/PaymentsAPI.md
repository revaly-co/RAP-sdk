# \PaymentsAPI

All URIs are relative to *https://api.revaly.co*

Method | HTTP request | Description
------------- | ------------- | -------------
[**AuthorizePayment**](PaymentsAPI.md#AuthorizePayment) | **Post** /payments/authorize | Authorize a payment
[**CapturePayment**](PaymentsAPI.md#CapturePayment) | **Post** /payments/capture/{transactionId} | Capture an authorized payment
[**ChargePayment**](PaymentsAPI.md#ChargePayment) | **Post** /payments | Process a payment (charge)
[**RefundCancelPaymentByMerchantTransactionId**](PaymentsAPI.md#RefundCancelPaymentByMerchantTransactionId) | **Post** /payments/refund-cancel/merchant/{merchantTransactionId} | Refund or cancel a payment transaction by merchant transaction ID
[**RefundPayment**](PaymentsAPI.md#RefundPayment) | **Post** /payments/refund/{transactionId} | Refund a payment transaction by TransactionId
[**VoidPayment**](PaymentsAPI.md#VoidPayment) | **Post** /payments/void/{transactionId} | Void a payment transaction



## AuthorizePayment

> TransactionResponse AuthorizePayment(ctx).AuthorizeRequest(authorizeRequest).XApiVersion(xApiVersion).Execute()

Authorize a payment



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
	authorizeRequest := *openapiclient.NewAuthorizeRequest(int64(2500), "auth_order_12345") // AuthorizeRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentsAPI.AuthorizePayment(context.Background()).AuthorizeRequest(authorizeRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentsAPI.AuthorizePayment``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `AuthorizePayment`: TransactionResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentsAPI.AuthorizePayment`: %v\n", resp)
}
```

### Path Parameters



### Other Parameters

Other parameters are passed through a pointer to a apiAuthorizePaymentRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorizeRequest** | [**AuthorizeRequest**](AuthorizeRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## CapturePayment

> TransactionResponse CapturePayment(ctx, transactionId).CaptureRequest(captureRequest).XApiVersion(xApiVersion).Execute()

Capture an authorized payment



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
	transactionId := "06CQR5TMB800000G0011NCFRVY37A" // string | Unique identifier of the authorization transaction to capture
	captureRequest := *openapiclient.NewCaptureRequest("capture_order_12345") // CaptureRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentsAPI.CapturePayment(context.Background(), transactionId).CaptureRequest(captureRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentsAPI.CapturePayment``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `CapturePayment`: TransactionResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentsAPI.CapturePayment`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**transactionId** | **string** | Unique identifier of the authorization transaction to capture | 

### Other Parameters

Other parameters are passed through a pointer to a apiCapturePaymentRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **captureRequest** | [**CaptureRequest**](CaptureRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## ChargePayment

> TransactionResponse ChargePayment(ctx).PaymentRequest(paymentRequest).XApiVersion(xApiVersion).Execute()

Process a payment (charge)



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
	paymentRequest := *openapiclient.NewPaymentRequest(int64(2500), "charge_order_12345") // PaymentRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentsAPI.ChargePayment(context.Background()).PaymentRequest(paymentRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentsAPI.ChargePayment``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `ChargePayment`: TransactionResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentsAPI.ChargePayment`: %v\n", resp)
}
```

### Path Parameters



### Other Parameters

Other parameters are passed through a pointer to a apiChargePaymentRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **paymentRequest** | [**PaymentRequest**](PaymentRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## RefundCancelPaymentByMerchantTransactionId

> TransactionResponse RefundCancelPaymentByMerchantTransactionId(ctx, merchantTransactionId).RefundCancelRequest(refundCancelRequest).XApiVersion(xApiVersion).Execute()

Refund or cancel a payment transaction by merchant transaction ID



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
	merchantTransactionId := "merchant_auth_12345638934760478405277" // string | Merchant-provided unique identifier of the transaction to refund or cancel
	refundCancelRequest := *openapiclient.NewRefundCancelRequest("refund_order_12345", "customer_12345") // RefundCancelRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentsAPI.RefundCancelPaymentByMerchantTransactionId(context.Background(), merchantTransactionId).RefundCancelRequest(refundCancelRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentsAPI.RefundCancelPaymentByMerchantTransactionId``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `RefundCancelPaymentByMerchantTransactionId`: TransactionResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentsAPI.RefundCancelPaymentByMerchantTransactionId`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**merchantTransactionId** | **string** | Merchant-provided unique identifier of the transaction to refund or cancel | 

### Other Parameters

Other parameters are passed through a pointer to a apiRefundCancelPaymentByMerchantTransactionIdRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **refundCancelRequest** | [**RefundCancelRequest**](RefundCancelRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## RefundPayment

> TransactionResponse RefundPayment(ctx, transactionId).RefundRequest(refundRequest).XApiVersion(xApiVersion).Execute()

Refund a payment transaction by TransactionId



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
	transactionId := "06CQR5TMB800000G0011NCFRVY37A" // string | Unique identifier of the transaction to refund
	refundRequest := *openapiclient.NewRefundRequest("refund_order_12345") // RefundRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentsAPI.RefundPayment(context.Background(), transactionId).RefundRequest(refundRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentsAPI.RefundPayment``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `RefundPayment`: TransactionResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentsAPI.RefundPayment`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**transactionId** | **string** | Unique identifier of the transaction to refund | 

### Other Parameters

Other parameters are passed through a pointer to a apiRefundPaymentRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **refundRequest** | [**RefundRequest**](RefundRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## VoidPayment

> TransactionResponse VoidPayment(ctx, transactionId).VoidRequest(voidRequest).XApiVersion(xApiVersion).Execute()

Void a payment transaction



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
	transactionId := "06CQR5TMB800000G0011NCFRVY37A" // string | Unique identifier of the transaction to void
	voidRequest := *openapiclient.NewVoidRequest("void_order_12345") // VoidRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentsAPI.VoidPayment(context.Background(), transactionId).VoidRequest(voidRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentsAPI.VoidPayment``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `VoidPayment`: TransactionResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentsAPI.VoidPayment`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**transactionId** | **string** | Unique identifier of the transaction to void | 

### Other Parameters

Other parameters are passed through a pointer to a apiVoidPaymentRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **voidRequest** | [**VoidRequest**](VoidRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)

