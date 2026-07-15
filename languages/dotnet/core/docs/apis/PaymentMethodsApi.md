# Revaly.Sdk.Core.Api.PaymentMethodsApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|--------|--------------|-------------|
| [**CreatePaymentMethod**](PaymentMethodsApi.md#createpaymentmethod) | **POST** /payment-methods/create | Create a payment method |
| [**GetPaymentMethod**](PaymentMethodsApi.md#getpaymentmethod) | **GET** /payment-methods/show/{paymentMethodId} | Get payment method details |
| [**ListPaymentMethods**](PaymentMethodsApi.md#listpaymentmethods) | **GET** /payment-methods/list | List payment methods |
| [**RecachePaymentMethod**](PaymentMethodsApi.md#recachepaymentmethod) | **POST** /payment-methods/recache/{paymentMethodId} | Recache payment method |
| [**RedactPaymentMethod**](PaymentMethodsApi.md#redactpaymentmethod) | **POST** /payment-methods/redact/{paymentMethodId} | Redact payment method |
| [**UpdatePaymentMethod**](PaymentMethodsApi.md#updatepaymentmethod) | **POST** /payment-methods/update/{paymentMethodId} | Update payment method |

<a id="createpaymentmethod"></a>
# **CreatePaymentMethod**
> PaymentMethodWriteResponse CreatePaymentMethod (CreatePaymentMethodRequest createPaymentMethodRequest, string xApiVersion = null)

Create a payment method

Create and store a payment method in the vault. Supports both credit card details  and gatewayPaymentMethodIds from supported payment processors.  **Payment Method Types:** - **creditCard**: Credit card details that will be tokenized and stored - **gatewayPaymentMethodId**: Pre-existing gatewayPaymentMethodId from a supported payment gateway 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **createPaymentMethodRequest** | [**CreatePaymentMethodRequest**](CreatePaymentMethodRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method successfully created |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="getpaymentmethod"></a>
# **GetPaymentMethod**
> PaymentMethodResponse GetPaymentMethod (string paymentMethodId, string xApiVersion = null)

Get payment method details

Retrieve detailed information about a specific payment method.  Returns payment method data with sensitive information masked for security. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **paymentMethodId** | **string** | Unique identifier for the payment method |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**PaymentMethodResponse**](PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved payment method details |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **404** | Resource not found |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="listpaymentmethods"></a>
# **ListPaymentMethods**
> List&lt;PaymentMethodResponse&gt; ListPaymentMethods (string xApiVersion = null, int count = null, string order = null, string sincePaymentMethodId = null)

List payment methods

Retrieve a paginated list of stored payment methods.  Returns payment methods with sensitive information masked for security. Use pagination parameters to navigate through large result sets. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |
| **count** | **int** | Number of payment methods to return | [optional] [default to 20] |
| **order** | **string** | Sort order for results | [optional] [default to asc] |
| **sincePaymentMethodId** | **string** | Return payment methods after this ID (for pagination) | [optional]  |

### Return type

[**List&lt;PaymentMethodResponse&gt;**](PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successfully retrieved payment methods |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="recachepaymentmethod"></a>
# **RecachePaymentMethod**
> PaymentMethodWriteResponse RecachePaymentMethod (string paymentMethodId, PaymentMethodRecacheRequest paymentMethodRecacheRequest, string xApiVersion = null)

Recache payment method

Update a credit card verification value (CVV) so the card can be transacted against     


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **paymentMethodId** | **string** | Unique identifier for the payment method |  |
| **paymentMethodRecacheRequest** | [**PaymentMethodRecacheRequest**](PaymentMethodRecacheRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method recached successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="redactpaymentmethod"></a>
# **RedactPaymentMethod**
> PaymentMethodWriteResponse RedactPaymentMethod (string paymentMethodId, string xApiVersion = null)

Redact payment method

Redact sensitive payment method information for compliance purposes.  This operation permanently removes sensitive data while keeping the payment method record for historical and reporting purposes. This action cannot be undone. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **paymentMethodId** | **string** | Unique identifier for the payment method |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method redacted successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

<a id="updatepaymentmethod"></a>
# **UpdatePaymentMethod**
> PaymentMethodWriteResponse UpdatePaymentMethod (string paymentMethodId, UpdatePaymentMethodRequest updatePaymentMethodRequest, string xApiVersion = null)

Update payment method

Update an existing payment method's information.  Allows updating billing information, expiration dates, and other non-sensitive data. Sensitive card data cannot be updated directly. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **paymentMethodId** | **string** | Unique identifier for the payment method |  |
| **updatePaymentMethodRequest** | [**UpdatePaymentMethodRequest**](UpdatePaymentMethodRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Payment method updated successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

