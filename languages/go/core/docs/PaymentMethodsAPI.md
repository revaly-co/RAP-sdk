# \PaymentMethodsAPI

All URIs are relative to *https://api.revaly.co*

Method | HTTP request | Description
------------- | ------------- | -------------
[**CreatePaymentMethod**](PaymentMethodsAPI.md#CreatePaymentMethod) | **Post** /payment-methods/create | Create a payment method
[**GetPaymentMethod**](PaymentMethodsAPI.md#GetPaymentMethod) | **Get** /payment-methods/show/{paymentMethodId} | Get payment method details
[**ListPaymentMethods**](PaymentMethodsAPI.md#ListPaymentMethods) | **Get** /payment-methods/list | List payment methods
[**RecachePaymentMethod**](PaymentMethodsAPI.md#RecachePaymentMethod) | **Post** /payment-methods/recache/{paymentMethodId} | Recache payment method
[**RedactPaymentMethod**](PaymentMethodsAPI.md#RedactPaymentMethod) | **Post** /payment-methods/redact/{paymentMethodId} | Redact payment method
[**UpdatePaymentMethod**](PaymentMethodsAPI.md#UpdatePaymentMethod) | **Post** /payment-methods/update/{paymentMethodId} | Update payment method



## CreatePaymentMethod

> PaymentMethodWriteResponse CreatePaymentMethod(ctx).CreatePaymentMethodRequest(createPaymentMethodRequest).XApiVersion(xApiVersion).Execute()

Create a payment method



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
	createPaymentMethodRequest := *openapiclient.NewCreatePaymentMethodRequest("creditCard") // CreatePaymentMethodRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentMethodsAPI.CreatePaymentMethod(context.Background()).CreatePaymentMethodRequest(createPaymentMethodRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentMethodsAPI.CreatePaymentMethod``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `CreatePaymentMethod`: PaymentMethodWriteResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentMethodsAPI.CreatePaymentMethod`: %v\n", resp)
}
```

### Path Parameters



### Other Parameters

Other parameters are passed through a pointer to a apiCreatePaymentMethodRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **createPaymentMethodRequest** | [**CreatePaymentMethodRequest**](CreatePaymentMethodRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## GetPaymentMethod

> PaymentMethodResponse GetPaymentMethod(ctx, paymentMethodId).XApiVersion(xApiVersion).Execute()

Get payment method details



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
	paymentMethodId := "7DA6XQ33AIPUZLLDAGMXYHNTG434uyt" // string | Unique identifier for the payment method
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentMethodsAPI.GetPaymentMethod(context.Background(), paymentMethodId).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentMethodsAPI.GetPaymentMethod``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `GetPaymentMethod`: PaymentMethodResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentMethodsAPI.GetPaymentMethod`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**paymentMethodId** | **string** | Unique identifier for the payment method | 

### Other Parameters

Other parameters are passed through a pointer to a apiGetPaymentMethodRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**PaymentMethodResponse**](PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## ListPaymentMethods

> []PaymentMethodResponse ListPaymentMethods(ctx).XApiVersion(xApiVersion).Count(count).Order(order).SincePaymentMethodId(sincePaymentMethodId).Execute()

List payment methods



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
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")
	count := int32(20) // int32 | Number of payment methods to return (optional) (default to 20)
	order := "asc" // string | Sort order for results (optional) (default to "asc")
	sincePaymentMethodId := "7DA6XQ33AIPUZLLDAGMXYHNTG4" // string | Return payment methods after this ID (for pagination) (optional)

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentMethodsAPI.ListPaymentMethods(context.Background()).XApiVersion(xApiVersion).Count(count).Order(order).SincePaymentMethodId(sincePaymentMethodId).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentMethodsAPI.ListPaymentMethods``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `ListPaymentMethods`: []PaymentMethodResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentMethodsAPI.ListPaymentMethods`: %v\n", resp)
}
```

### Path Parameters



### Other Parameters

Other parameters are passed through a pointer to a apiListPaymentMethodsRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]
 **count** | **int32** | Number of payment methods to return | [default to 20]
 **order** | **string** | Sort order for results | [default to &quot;asc&quot;]
 **sincePaymentMethodId** | **string** | Return payment methods after this ID (for pagination) | 

### Return type

[**[]PaymentMethodResponse**](PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## RecachePaymentMethod

> PaymentMethodWriteResponse RecachePaymentMethod(ctx, paymentMethodId).PaymentMethodRecacheRequest(paymentMethodRecacheRequest).XApiVersion(xApiVersion).Execute()

Recache payment method



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
	paymentMethodId := "7DA6XQ33AIPUZLLDAGMXYHNTG4" // string | Unique identifier for the payment method
	paymentMethodRecacheRequest := *openapiclient.NewPaymentMethodRecacheRequest(*openapiclient.NewPaymentMethodRecacheRequestPaymentMethod(*openapiclient.NewPaymentMethodRecacheRequestPaymentMethodCreditCard("123"))) // PaymentMethodRecacheRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentMethodsAPI.RecachePaymentMethod(context.Background(), paymentMethodId).PaymentMethodRecacheRequest(paymentMethodRecacheRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentMethodsAPI.RecachePaymentMethod``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `RecachePaymentMethod`: PaymentMethodWriteResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentMethodsAPI.RecachePaymentMethod`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**paymentMethodId** | **string** | Unique identifier for the payment method | 

### Other Parameters

Other parameters are passed through a pointer to a apiRecachePaymentMethodRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **paymentMethodRecacheRequest** | [**PaymentMethodRecacheRequest**](PaymentMethodRecacheRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## RedactPaymentMethod

> PaymentMethodWriteResponse RedactPaymentMethod(ctx, paymentMethodId).XApiVersion(xApiVersion).Execute()

Redact payment method



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
	paymentMethodId := "7DA6XQ33AIPUZLLDAGMXYHNTG4" // string | Unique identifier for the payment method
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentMethodsAPI.RedactPaymentMethod(context.Background(), paymentMethodId).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentMethodsAPI.RedactPaymentMethod``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `RedactPaymentMethod`: PaymentMethodWriteResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentMethodsAPI.RedactPaymentMethod`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**paymentMethodId** | **string** | Unique identifier for the payment method | 

### Other Parameters

Other parameters are passed through a pointer to a apiRedactPaymentMethodRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## UpdatePaymentMethod

> PaymentMethodWriteResponse UpdatePaymentMethod(ctx, paymentMethodId).UpdatePaymentMethodRequest(updatePaymentMethodRequest).XApiVersion(xApiVersion).Execute()

Update payment method



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
	paymentMethodId := "7DA6XQ33AIPUZLLDAGMXYHNTG4" // string | Unique identifier for the payment method
	updatePaymentMethodRequest := *openapiclient.NewUpdatePaymentMethodRequest() // UpdatePaymentMethodRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.PaymentMethodsAPI.UpdatePaymentMethod(context.Background(), paymentMethodId).UpdatePaymentMethodRequest(updatePaymentMethodRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `PaymentMethodsAPI.UpdatePaymentMethod``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `UpdatePaymentMethod`: PaymentMethodWriteResponse
	fmt.Fprintf(os.Stdout, "Response from `PaymentMethodsAPI.UpdatePaymentMethod`: %v\n", resp)
}
```

### Path Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**paymentMethodId** | **string** | Unique identifier for the payment method | 

### Other Parameters

Other parameters are passed through a pointer to a apiUpdatePaymentMethodRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------

 **updatePaymentMethodRequest** | [**UpdatePaymentMethodRequest**](UpdatePaymentMethodRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)

