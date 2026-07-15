# Revaly.Sdk.Core.Model.ErrorResponse
Standard error response format used across all API endpoints

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Error** | **string** | A human-readable error message describing what went wrong | 
**Details** | **Object** | Optional additional details about the error; structure varies by error type (may be an object, a string, or null) | [optional] 
**Code** | **string** | Machine-readable safety signal, present on every 5xx error response and never on 4xx responses. &#x60;not_processed&#x60; is emitted only when the platform can prove the request was never dispatched to a payment gateway or upstream (for example, the upstream circuit breaker was already open), so the caller may safely fail over without risking a duplicate charge. &#x60;outcome_unknown&#x60; means the request may have reached an upstream and the outcome cannot be proven; reconcile the transaction before retrying. Emission is conservative — any 5xx without a provable determination carries &#x60;outcome_unknown&#x60;. | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

