# PaymentMethodsApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createPaymentMethod**](PaymentMethodsApi.md#createpaymentmethodoperation) | **POST** /payment-methods/create | Create a payment method |
| [**getPaymentMethod**](PaymentMethodsApi.md#getpaymentmethod) | **GET** /payment-methods/show/{paymentMethodId} | Get payment method details |
| [**listPaymentMethods**](PaymentMethodsApi.md#listpaymentmethods) | **GET** /payment-methods/list | List payment methods |
| [**recachePaymentMethod**](PaymentMethodsApi.md#recachepaymentmethod) | **POST** /payment-methods/recache/{paymentMethodId} | Recache payment method |
| [**redactPaymentMethod**](PaymentMethodsApi.md#redactpaymentmethod) | **POST** /payment-methods/redact/{paymentMethodId} | Redact payment method |
| [**updatePaymentMethod**](PaymentMethodsApi.md#updatepaymentmethodoperation) | **POST** /payment-methods/update/{paymentMethodId} | Update payment method |



## createPaymentMethod

> PaymentMethodWriteResponse createPaymentMethod(createPaymentMethodRequest, xApiVersion)

Create a payment method

Create and store a payment method in the vault. Supports both credit card details  and gatewayPaymentMethodIds from supported payment processors.  **Payment Method Types:** - **creditCard**: Credit card details that will be tokenized and stored - **gatewayPaymentMethodId**: Pre-existing gatewayPaymentMethodId from a supported payment gateway 

### Example

```ts
import {
  Configuration,
  PaymentMethodsApi,
} from '';
import type { CreatePaymentMethodOperationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    apiKey: "YOUR API KEY",
  });
  const api = new PaymentMethodsApi(config);

  const body = {
    // CreatePaymentMethodRequest
    createPaymentMethodRequest: {"paymentMethodType":"creditCard","customerId":"customer_123456","paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}}},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies CreatePaymentMethodOperationRequest;

  try {
    const data = await api.createPaymentMethod(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **createPaymentMethodRequest** | [CreatePaymentMethodRequest](CreatePaymentMethodRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


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

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getPaymentMethod

> PaymentMethodResponse getPaymentMethod(paymentMethodId, xApiVersion)

Get payment method details

Retrieve detailed information about a specific payment method.  Returns payment method data with sensitive information masked for security. 

### Example

```ts
import {
  Configuration,
  PaymentMethodsApi,
} from '';
import type { GetPaymentMethodRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    apiKey: "YOUR API KEY",
  });
  const api = new PaymentMethodsApi(config);

  const body = {
    // string | Unique identifier for the payment method
    paymentMethodId: 7DA6XQ33AIPUZLLDAGMXYHNTG434uyt,
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies GetPaymentMethodRequest;

  try {
    const data = await api.getPaymentMethod(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **paymentMethodId** | `string` | Unique identifier for the payment method | [Defaults to `undefined`] |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**PaymentMethodResponse**](PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


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

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listPaymentMethods

> Array&lt;PaymentMethodResponse&gt; listPaymentMethods(xApiVersion, count, order, sincePaymentMethodId)

List payment methods

Retrieve a paginated list of stored payment methods.  Returns payment methods with sensitive information masked for security. Use pagination parameters to navigate through large result sets. 

### Example

```ts
import {
  Configuration,
  PaymentMethodsApi,
} from '';
import type { ListPaymentMethodsRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    apiKey: "YOUR API KEY",
  });
  const api = new PaymentMethodsApi(config);

  const body = {
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
    // number | Number of payment methods to return (optional)
    count: 20,
    // 'asc' | 'desc' | Sort order for results (optional)
    order: asc,
    // string | Return payment methods after this ID (for pagination) (optional)
    sincePaymentMethodId: 7DA6XQ33AIPUZLLDAGMXYHNTG4,
  } satisfies ListPaymentMethodsRequest;

  try {
    const data = await api.listPaymentMethods(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |
| **count** | `number` | Number of payment methods to return | [Optional] [Defaults to `20`] |
| **order** | `asc`, `desc` | Sort order for results | [Optional] [Defaults to `&#39;asc&#39;`] [Enum: asc, desc] |
| **sincePaymentMethodId** | `string` | Return payment methods after this ID (for pagination) | [Optional] [Defaults to `undefined`] |

### Return type

[**Array&lt;PaymentMethodResponse&gt;**](PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


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

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## recachePaymentMethod

> PaymentMethodWriteResponse recachePaymentMethod(paymentMethodId, paymentMethodRecacheRequest, xApiVersion)

Recache payment method

Update a credit card verification value (CVV) so the card can be transacted against     

### Example

```ts
import {
  Configuration,
  PaymentMethodsApi,
} from '';
import type { RecachePaymentMethodRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    apiKey: "YOUR API KEY",
  });
  const api = new PaymentMethodsApi(config);

  const body = {
    // string | Unique identifier for the payment method
    paymentMethodId: 7DA6XQ33AIPUZLLDAGMXYHNTG4,
    // PaymentMethodRecacheRequest
    paymentMethodRecacheRequest: {"paymentMethod":{"creditCard":{"verificationValue":"123"}}},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies RecachePaymentMethodRequest;

  try {
    const data = await api.recachePaymentMethod(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **paymentMethodId** | `string` | Unique identifier for the payment method | [Defaults to `undefined`] |
| **paymentMethodRecacheRequest** | [PaymentMethodRecacheRequest](PaymentMethodRecacheRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


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

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## redactPaymentMethod

> PaymentMethodWriteResponse redactPaymentMethod(paymentMethodId, xApiVersion)

Redact payment method

Redact sensitive payment method information for compliance purposes.  This operation permanently removes sensitive data while keeping the payment method record for historical and reporting purposes. This action cannot be undone. 

### Example

```ts
import {
  Configuration,
  PaymentMethodsApi,
} from '';
import type { RedactPaymentMethodRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    apiKey: "YOUR API KEY",
  });
  const api = new PaymentMethodsApi(config);

  const body = {
    // string | Unique identifier for the payment method
    paymentMethodId: 7DA6XQ33AIPUZLLDAGMXYHNTG4,
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies RedactPaymentMethodRequest;

  try {
    const data = await api.redactPaymentMethod(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **paymentMethodId** | `string` | Unique identifier for the payment method | [Defaults to `undefined`] |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


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

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## updatePaymentMethod

> PaymentMethodWriteResponse updatePaymentMethod(paymentMethodId, updatePaymentMethodRequest, xApiVersion)

Update payment method

Update an existing payment method\&#39;s information.  Allows updating billing information, expiration dates, and other non-sensitive data. Sensitive card data cannot be updated directly. 

### Example

```ts
import {
  Configuration,
  PaymentMethodsApi,
} from '';
import type { UpdatePaymentMethodOperationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // To configure API key authorization: ApiKeyAuth
    apiKey: "YOUR API KEY",
  });
  const api = new PaymentMethodsApi(config);

  const body = {
    // string | Unique identifier for the payment method
    paymentMethodId: 7DA6XQ33AIPUZLLDAGMXYHNTG4,
    // UpdatePaymentMethodRequest
    updatePaymentMethodRequest: {"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe.updated@example.com","billingAddress":{"address1":"456 Oak Avenue","city":"Los Angeles","state":"CA","zip":"90210","country":"US","phoneNumber":"+1-555-987-6543"},"shippingAddress":{"address1":"789 Pine Street","city":"Los Angeles","state":"CA","zip":"90211","country":"US","phoneNumber":"+1-555-654-3210"}}},
    // '2.0' | '2.1' | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional)
    xApiVersion: 2.1,
  } satisfies UpdatePaymentMethodOperationRequest;

  try {
    const data = await api.updatePaymentMethod(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **paymentMethodId** | `string` | Unique identifier for the payment method | [Defaults to `undefined`] |
| **updatePaymentMethodRequest** | [UpdatePaymentMethodRequest](UpdatePaymentMethodRequest.md) |  | |
| **xApiVersion** | `2.0`, `2.1` | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [Optional] [Defaults to `&#39;2.0&#39;`] [Enum: 2.0, 2.1] |

### Return type

[**PaymentMethodWriteResponse**](PaymentMethodWriteResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


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

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

