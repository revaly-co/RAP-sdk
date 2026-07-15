# \NotifyAPI

All URIs are relative to *https://api.revaly.co*

Method | HTTP request | Description
------------- | ------------- | -------------
[**NotifyRevaly**](NotifyAPI.md#NotifyRevaly) | **Post** /notify | Notify Revaly of payment events



## NotifyRevaly

> NotifyResponse NotifyRevaly(ctx).NotifyRequest(notifyRequest).XApiVersion(xApiVersion).Execute()

Notify Revaly of payment events



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
	notifyRequest := *openapiclient.NewNotifyRequest("recordPayment") // NotifyRequest | 
	xApiVersion := "2.1" // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to "2.0")

	configuration := openapiclient.NewConfiguration()
	apiClient := openapiclient.NewAPIClient(configuration)
	resp, r, err := apiClient.NotifyAPI.NotifyRevaly(context.Background()).NotifyRequest(notifyRequest).XApiVersion(xApiVersion).Execute()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `NotifyAPI.NotifyRevaly``: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}
	// response from `NotifyRevaly`: NotifyResponse
	fmt.Fprintf(os.Stdout, "Response from `NotifyAPI.NotifyRevaly`: %v\n", resp)
}
```

### Path Parameters



### Other Parameters

Other parameters are passed through a pointer to a apiNotifyRevalyRequest struct via the builder pattern


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notifyRequest** | [**NotifyRequest**](NotifyRequest.md) |  | 
 **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [default to &quot;2.0&quot;]

### Return type

[**NotifyResponse**](NotifyResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)

