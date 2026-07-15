# Revaly.Sdk.Core.Api.NotifyApi

All URIs are relative to *https://api.revaly.co*

| Method | HTTP request | Description |
|--------|--------------|-------------|
| [**NotifyRevaly**](NotifyApi.md#notifyrevaly) | **POST** /notify | Notify Revaly of payment events |

<a id="notifyrevaly"></a>
# **NotifyRevaly**
> NotifyResponse NotifyRevaly (NotifyRequest notifyRequest, string xApiVersion = null)

Notify Revaly of payment events

Notify Revaly of payment-related events and status changes.  This endpoint allows external systems to notify Revaly about specific business events related to payments, refunds, customer recovery, and customer updates. 


### Parameters

| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **notifyRequest** | [**NotifyRequest**](NotifyRequest.md) |  |  |
| **xApiVersion** | **string** | Selects the RAP API version for this request. New integrations should pin &#x60;2.1&#x60; (identical to &#x60;2.0&#x60; today; future refinements land there). Omit to use the base version (&#x60;2.0&#x60;). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy. | [optional] [default to 2.0] |

### Return type

[**NotifyResponse**](NotifyResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Notification received and processed successfully |  -  |
| **400** | Bad request - invalid parameters or request body |  -  |
| **401** | Unauthorized - invalid or missing API key |  -  |
| **403** | Forbidden - the authenticated principal is not permitted to perform this action |  -  |
| **404** | Resource not found |  -  |
| **422** | Unprocessable entity - validation succeeded but the request cannot be processed |  -  |
| **500** | Internal server error |  -  |
| **503** | Service unavailable - upstream dependency temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../README.md#documentation-for-models) [[Back to README]](../../README.md)

