# revaly_sdk_core.PaymentsApi

All URIs are relative to *https://api.revaly.co*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authorize_payment**](PaymentsApi.md#authorize_payment) | **POST** /payments/authorize | Authorize a payment
[**capture_payment**](PaymentsApi.md#capture_payment) | **POST** /payments/capture/{transactionId} | Capture an authorized payment
[**charge_payment**](PaymentsApi.md#charge_payment) | **POST** /payments | Process a payment (charge)
[**refund_cancel_payment_by_merchant_transaction_id**](PaymentsApi.md#refund_cancel_payment_by_merchant_transaction_id) | **POST** /payments/refund-cancel/merchant/{merchantTransactionId} | Refund or cancel a payment transaction by merchant transaction ID
[**refund_payment**](PaymentsApi.md#refund_payment) | **POST** /payments/refund/{transactionId} | Refund a payment transaction by TransactionId
[**void_payment**](PaymentsApi.md#void_payment) | **POST** /payments/void/{transactionId} | Void a payment transaction


# **authorize_payment**
> TransactionResponse authorize_payment(authorize_request, x_api_version=x_api_version)

Authorize a payment

Authorize a payment without immediately capturing funds.

This endpoint creates an authorization hold on the customer's payment method.
The authorized amount can later be captured using the capture endpoint.

**Payment Method Types:**
- **creditCard**: Process using raw credit card details
- **gatewayPaymentMethodId**: Process using an existing gateway payment method id

To charge a previously stored payment method, omit `paymentMethodType` and supply `paymentMethod.paymentMethodId`.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.authorize_request import AuthorizeRequest
from revaly_sdk_core.models.transaction_response import TransactionResponse
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
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with revaly_sdk_core.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = revaly_sdk_core.PaymentsApi(api_client)
    authorize_request = {"paymentMethodType":"creditCard","gatewayRoutingId":"PCFXF23ORZJEXMJLXJZCDISP6A","amount":2500,"merchantTransactionId":"auth_order_12345","mitStoredTransactionId":"mit_txn_001","initiatedBy":"MIT","currency":"USD","customerId":"customer_123456","customerIp":"192.168.1.100","orderId":"order_67890","description":"Authorization for subscription renewal","storeOnSuccess":true,"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025","cardType":"visa"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}},"threeDS":{"version":"2.2.0","exemptionType":"low_value","eci":"05","cryptogram":"BwABBJQ1AgAAAAAgJDUCAAAAAAA=","dsTransactionId":"c7aa28c2-e2c5-4e5c-a9d3-2f8b3c4d5e6f","acsTransactionId":"d8bb39d3-f3d6-5f6d-b0e4-3f9c4d5e6f70","xid":"MDAwMDAwMDAwMDAwMDAwMzIyNzY=","cavvAlgorithm":"1","directoryStatus":"Y","authenticationStatus":"Y","enrolledStatus":"Y","serverTransId":"e9cc40e4-04e7-6076-c1f5-409d5e6f7081"},"recovery":{"disableCustomerRecovery":false,"customerAccountNumber":"ACC-456789","customerBalance":1922,"disableSMSNotification":false,"disableEmailNotification":false,"retryCount":1,"paymentReferenceData":"initial_txn_ref_456","dateFirstAttempt":"2025-01-10T08:00:00Z"},"paymentPlanData":{"sku":"PREMIUM_MONTHLY","category":"FDT","billingPlan":"monthly","billingCycle":1,"productDisplayName":"Premium Monthly Plan","paymentModel":"recurring","subscriptionId":"sub_abc123def456"}} # AuthorizeRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Authorize a payment
        api_response = api_instance.authorize_payment(authorize_request, x_api_version=x_api_version)
        print("The response of PaymentsApi->authorize_payment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentsApi->authorize_payment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorize_request** | [**AuthorizeRequest**](AuthorizeRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Payment authorized successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **capture_payment**
> TransactionResponse capture_payment(transaction_id, capture_request, x_api_version=x_api_version)

Capture an authorized payment

Capture funds from a previously authorized payment transaction.

This endpoint captures the full or partial amount from an authorization.
Once captured, the funds will be settled to your account.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.capture_request import CaptureRequest
from revaly_sdk_core.models.transaction_response import TransactionResponse
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
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with revaly_sdk_core.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = revaly_sdk_core.PaymentsApi(api_client)
    transaction_id = '06CQR5TMB800000G0011NCFRVY37A' # str | Unique identifier of the authorization transaction to capture
    capture_request = {"merchantTransactionId":"capture_order_12345"} # CaptureRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Capture an authorized payment
        api_response = api_instance.capture_payment(transaction_id, capture_request, x_api_version=x_api_version)
        print("The response of PaymentsApi->capture_payment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentsApi->capture_payment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **str**| Unique identifier of the authorization transaction to capture | 
 **capture_request** | [**CaptureRequest**](CaptureRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Payment captured successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **charge_payment**
> TransactionResponse charge_payment(payment_request, x_api_version=x_api_version)

Process a payment (charge)

Process a direct payment charge against a payment method.

This endpoint performs an immediate charge and settlement of funds.
Unlike authorization, the funds are immediately captured and transferred.

**Payment Method Types:**
- **creditCard**: Process using raw credit card details
- **gatewayPaymentMethodId**: Process using an existing gateway payment method id

To charge a previously stored payment method, omit `paymentMethodType` and supply `paymentMethod.paymentMethodId`.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.payment_request import PaymentRequest
from revaly_sdk_core.models.transaction_response import TransactionResponse
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
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with revaly_sdk_core.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = revaly_sdk_core.PaymentsApi(api_client)
    payment_request = {"paymentMethodType":"creditCard","gatewayRoutingId":"PCFXF23ORZJEXMJLXJZCDISP6A","amount":2500,"merchantTransactionId":"charge_order_12345","mitStoredTransactionId":"mit_txn_001","initiatedBy":"MIT","currency":"USD","customerId":"customer_123456","customerIp":"192.168.1.100","orderId":"order_67890","description":"Payment for online purchase","storeOnSuccess":true,"paymentMethod":{"firstName":"John","lastName":"Doe","fullName":"John Doe","email":"john.doe@example.com","creditCard":{"number":"4242424242424242","cardVerificationCode":"123","expiryMonth":"12","expiryYear":"2025","cardType":"visa"},"billingAddress":{"address1":"123 Main Street","address2":"Apt 4B","city":"New York","state":"NY","zip":"10001","country":"US","phoneNumber":"+1-555-123-4567"},"shippingAddress":{"address1":"456 Oak Avenue","city":"Brooklyn","state":"NY","zip":"11201","country":"US"}},"threeDS":{"version":"2.2.0","exemptionType":"low_value","eci":"05","cryptogram":"BwABBJQ1AgAAAAAgJDUCAAAAAAA=","dsTransactionId":"c7aa28c2-e2c5-4e5c-a9d3-2f8b3c4d5e6f","acsTransactionId":"d8bb39d3-f3d6-5f6d-b0e4-3f9c4d5e6f70","xid":"MDAwMDAwMDAwMDAwMDAwMzIyNzY=","cavvAlgorithm":"1","directoryStatus":"Y","authenticationStatus":"Y","enrolledStatus":"Y","serverTransId":"e9cc40e4-04e7-6076-c1f5-409d5e6f7081"},"recovery":{"disableCustomerRecovery":false,"customerAccountNumber":"ACC-456789","customerBalance":1922,"disableSMSNotification":false,"disableEmailNotification":false,"retryCount":1,"paymentReferenceData":"initial_txn_ref_456","dateFirstAttempt":"2025-01-10T08:00:00Z"},"paymentPlanData":{"sku":"PREMIUM_MONTHLY","category":"FDT","billingPlan":"monthly","billingCycle":1,"productDisplayName":"Premium Monthly Plan","paymentModel":"recurring","subscriptionId":"sub_abc123def456"}} # PaymentRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Process a payment (charge)
        api_response = api_instance.charge_payment(payment_request, x_api_version=x_api_version)
        print("The response of PaymentsApi->charge_payment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentsApi->charge_payment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payment_request** | [**PaymentRequest**](PaymentRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Payment processed successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**409** | Conflict - a payment with this merchantTransactionId has already been received for this account. Duplicate submissions are rejected deterministically instead of double-charging (per-account idempotency on merchantTransactionId). Retrieve the payment&#39;s status via GET /transactions/merchant/{merchantTransactionId}. Exception: a submission previously rejected with a 5xx carrying code &#x60;not_processed&#x60; released the id — resubmitting it is permitted and will not conflict. |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refund_cancel_payment_by_merchant_transaction_id**
> TransactionResponse refund_cancel_payment_by_merchant_transaction_id(merchant_transaction_id, refund_cancel_request, x_api_version=x_api_version)

Refund or cancel a payment transaction by merchant transaction ID

Refund a previously settled payment transaction using Merchant Transaction ID.

This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer's payment method.

This endpoint also cancels payments that are currently in the Revaly approvals flow using MerchantTransactionId.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.refund_cancel_request import RefundCancelRequest
from revaly_sdk_core.models.transaction_response import TransactionResponse
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
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with revaly_sdk_core.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = revaly_sdk_core.PaymentsApi(api_client)
    merchant_transaction_id = 'merchant_auth_12345638934760478405277' # str | Merchant-provided unique identifier of the transaction to refund or cancel
    refund_cancel_request = {"merchantTransactionId":"refund_order_12345","customerId":"customer_12345"} # RefundCancelRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Refund or cancel a payment transaction by merchant transaction ID
        api_response = api_instance.refund_cancel_payment_by_merchant_transaction_id(merchant_transaction_id, refund_cancel_request, x_api_version=x_api_version)
        print("The response of PaymentsApi->refund_cancel_payment_by_merchant_transaction_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentsApi->refund_cancel_payment_by_merchant_transaction_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **merchant_transaction_id** | **str**| Merchant-provided unique identifier of the transaction to refund or cancel | 
 **refund_cancel_request** | [**RefundCancelRequest**](RefundCancelRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Refund or cancellation processed successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refund_payment**
> TransactionResponse refund_payment(transaction_id, refund_request, x_api_version=x_api_version)

Refund a payment transaction by TransactionId

Refund a previously settled payment transaction using the Revaly transactionId.

This endpoint processes full or partial refunds for completed payments. Refunded amounts will be returned to the customer's payment method.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.refund_request import RefundRequest
from revaly_sdk_core.models.transaction_response import TransactionResponse
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
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with revaly_sdk_core.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = revaly_sdk_core.PaymentsApi(api_client)
    transaction_id = '06CQR5TMB800000G0011NCFRVY37A' # str | Unique identifier of the transaction to refund
    refund_request = {"merchantTransactionId":"refund_order_12345"} # RefundRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Refund a payment transaction by TransactionId
        api_response = api_instance.refund_payment(transaction_id, refund_request, x_api_version=x_api_version)
        print("The response of PaymentsApi->refund_payment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentsApi->refund_payment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **str**| Unique identifier of the transaction to refund | 
 **refund_request** | [**RefundRequest**](RefundRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Refund processed successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **void_payment**
> TransactionResponse void_payment(transaction_id, void_request, x_api_version=x_api_version)

Void a payment transaction

Void (cancel) a payment transaction that has not yet been settled.

This endpoint cancels an authorization or unsettled sale transaction.
Voided transactions cannot be captured or refunded.


### Example

* Api Key Authentication (ApiKeyAuth):

```python
import revaly_sdk_core
from revaly_sdk_core.models.transaction_response import TransactionResponse
from revaly_sdk_core.models.void_request import VoidRequest
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
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with revaly_sdk_core.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = revaly_sdk_core.PaymentsApi(api_client)
    transaction_id = '06CQR5TMB800000G0011NCFRVY37A' # str | Unique identifier of the transaction to void
    void_request = {"merchantTransactionId":"void_order_12345"} # VoidRequest | 
    x_api_version = 2.0 # str | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. (optional) (default to 2.0)

    try:
        # Void a payment transaction
        api_response = api_instance.void_payment(transaction_id, void_request, x_api_version=x_api_version)
        print("The response of PaymentsApi->void_payment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentsApi->void_payment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **str**| Unique identifier of the transaction to void | 
 **void_request** | [**VoidRequest**](VoidRequest.md)|  | 
 **x_api_version** | **str**| Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0]

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Payment voided successfully |  -  |
**400** | Bad request - invalid parameters or request body |  -  |
**401** | Unauthorized - invalid or missing API key |  -  |
**403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
**422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
**500** | Internal server error |  -  |
**503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

