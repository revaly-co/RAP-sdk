# revaly_sdk_core.PaymentMethodsApi

All URIs are relative to *https://api.revaly.co*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_payment_method**](PaymentMethodsApi.md#create_payment_method) | **POST** /payment-methods/create | Create a payment method
[**get_payment_method**](PaymentMethodsApi.md#get_payment_method) | **GET** /payment-methods/show/{paymentMethodId} | Get payment method details
[**list_payment_methods**](PaymentMethodsApi.md#list_payment_methods) | **GET** /payment-methods/list | List payment methods
[**recache_payment_method**](PaymentMethodsApi.md#recache_payment_method) | **POST** /payment-methods/recache/{paymentMethodId} | Recache payment method
[**redact_payment_method**](PaymentMethodsApi.md#redact_payment_method) | **POST** /payment-methods/redact/{paymentMethodId} | Redact payment method
[**update_payment_method**](PaymentMethodsApi.md#update_payment_method) | **POST** /payment-methods/update/{paymentMethodId} | Update payment method


# **create_payment_method**
> PaymentMethodWriteResponse create_payment_method(create_payment_method_request, x_api_version=x_api_version)

Create a payment method

Create and store a payment method in the vault. Supports both credit card details 
and gatewayPaymentMethodIds from supported payment processors.

**Payment Method Types:**
- **creditCard**: Credit card details that will be tokenized and stored
- **gatewayPaymentMethodId**: Pre-existing gatewayPaymentMethodId from a supported payment gateway


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.create_payment_method_request import CreatePaymentMethodRequest
from revaly_sdk_core.models.payment_method_write_response import PaymentMethodWriteResponse
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
    api_instance = revaly_sdk_core.PaymentMethodsApi(api_client)
    create_payment_method_request = {"paymentMethodType":"creditCard","customerId":"customer_123456","paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}}} # CreatePaymentMethodRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Create a payment method
        api_response = api_instance.create_payment_method(create_payment_method_request, x_api_version=x_api_version)
        print("The response of PaymentMethodsApi->create_payment_method:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentMethodsApi->create_payment_method: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_payment_method_request** | [**CreatePaymentMethodRequest**](CreatePaymentMethodRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

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
**200** | Payment method successfully created |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_payment_method**
> PaymentMethodResponse get_payment_method(payment_method_id, x_api_version=x_api_version)

Get payment method details

Retrieve detailed information about a specific payment method.

Returns payment method data with sensitive information masked for security.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.payment_method_response import PaymentMethodResponse
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
    api_instance = revaly_sdk_core.PaymentMethodsApi(api_client)
    payment_method_id = '7DA6XQ33AIPUZLLDAGMXYHNTG434uyt' # str | Unique identifier for the payment method
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Get payment method details
        api_response = api_instance.get_payment_method(payment_method_id, x_api_version=x_api_version)
        print("The response of PaymentMethodsApi->get_payment_method:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentMethodsApi->get_payment_method: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_method_id** | **str**| Unique identifier for the payment method | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

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
**200** | Successfully retrieved payment method details |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**404** | Resource not found |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_payment_methods**
> List[PaymentMethodResponse] list_payment_methods(x_api_version=x_api_version, count=count, order=order, since_payment_method_id=since_payment_method_id)

List payment methods

Retrieve a paginated list of stored payment methods.

Returns payment methods with sensitive information masked for security.
Use pagination parameters to navigate through large result sets.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.payment_method_response import PaymentMethodResponse
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
    api_instance = revaly_sdk_core.PaymentMethodsApi(api_client)
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)
    count = 20 # int | Number of payment methods to return (optional) (default to 20)
    order = asc # str | Sort order for results (optional) (default to asc)
    since_payment_method_id = '7DA6XQ33AIPUZLLDAGMXYHNTG4' # str | Return payment methods after this ID (for pagination) (optional)

    try:
        # List payment methods
        api_response = api_instance.list_payment_methods(x_api_version=x_api_version, count=count, order=order, since_payment_method_id=since_payment_method_id)
        print("The response of PaymentMethodsApi->list_payment_methods:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentMethodsApi->list_payment_methods: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]
 **count** | **int**| Number of payment methods to return | [optional] [default to 20]
 **order** | **str**| Sort order for results | [optional] [default to asc]
 **since_payment_method_id** | **str**| Return payment methods after this ID (for pagination) | [optional] 

### Return type

[**List[PaymentMethodResponse]**](PaymentMethodResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved payment methods |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **recache_payment_method**
> PaymentMethodWriteResponse recache_payment_method(payment_method_id, payment_method_recache_request, x_api_version=x_api_version)

Recache payment method

Update a credit card verification value (CVV) so the card can be transacted against    


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.payment_method_recache_request import PaymentMethodRecacheRequest
from revaly_sdk_core.models.payment_method_write_response import PaymentMethodWriteResponse
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
    api_instance = revaly_sdk_core.PaymentMethodsApi(api_client)
    payment_method_id = '7DA6XQ33AIPUZLLDAGMXYHNTG4' # str | Unique identifier for the payment method
    payment_method_recache_request = {"paymentMethod":{"creditCard":{"verificationValue":"123"}}} # PaymentMethodRecacheRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Recache payment method
        api_response = api_instance.recache_payment_method(payment_method_id, payment_method_recache_request, x_api_version=x_api_version)
        print("The response of PaymentMethodsApi->recache_payment_method:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentMethodsApi->recache_payment_method: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_method_id** | **str**| Unique identifier for the payment method | 
 **payment_method_recache_request** | [**PaymentMethodRecacheRequest**](PaymentMethodRecacheRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

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
**200** | Payment method recached successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **redact_payment_method**
> PaymentMethodWriteResponse redact_payment_method(payment_method_id, x_api_version=x_api_version)

Redact payment method

Redact sensitive payment method information for compliance purposes.

This operation permanently removes sensitive data while keeping
the payment method record for historical and reporting purposes.
This action cannot be undone.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.payment_method_write_response import PaymentMethodWriteResponse
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
    api_instance = revaly_sdk_core.PaymentMethodsApi(api_client)
    payment_method_id = '7DA6XQ33AIPUZLLDAGMXYHNTG4' # str | Unique identifier for the payment method
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Redact payment method
        api_response = api_instance.redact_payment_method(payment_method_id, x_api_version=x_api_version)
        print("The response of PaymentMethodsApi->redact_payment_method:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentMethodsApi->redact_payment_method: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_method_id** | **str**| Unique identifier for the payment method | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

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
**200** | Payment method redacted successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_payment_method**
> PaymentMethodWriteResponse update_payment_method(payment_method_id, update_payment_method_request, x_api_version=x_api_version)

Update payment method

Update an existing payment method's information.

Allows updating billing information, expiration dates, and other
non-sensitive data. Sensitive card data cannot be updated directly.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.payment_method_write_response import PaymentMethodWriteResponse
from revaly_sdk_core.models.update_payment_method_request import UpdatePaymentMethodRequest
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
    api_instance = revaly_sdk_core.PaymentMethodsApi(api_client)
    payment_method_id = '7DA6XQ33AIPUZLLDAGMXYHNTG4' # str | Unique identifier for the payment method
    update_payment_method_request = {"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe.updated@example.com","billingAddress":{"address1":"456 Oak Avenue","city":"Los Angeles","state":"CA","zip":"90210","country":"US","phoneNumber":"+1-555-987-6543"},"shippingAddress":{"address1":"789 Pine Street","city":"Los Angeles","state":"CA","zip":"90211","country":"US","phoneNumber":"+1-555-654-3210"}}} # UpdatePaymentMethodRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Update payment method
        api_response = api_instance.update_payment_method(payment_method_id, update_payment_method_request, x_api_version=x_api_version)
        print("The response of PaymentMethodsApi->update_payment_method:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentMethodsApi->update_payment_method: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_method_id** | **str**| Unique identifier for the payment method | 
 **update_payment_method_request** | [**UpdatePaymentMethodRequest**](UpdatePaymentMethodRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

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
**200** | Payment method updated successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

