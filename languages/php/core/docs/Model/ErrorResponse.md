# ErrorResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **string** | A human-readable error message describing what went wrong |
**details** | **mixed** | Optional additional details about the error; structure varies by error type (may be an object, a string, or null) | [optional]
**code** | **string** | Machine-readable safety signal, present on every 5xx error response and never on 4xx responses. &#x60;not_processed&#x60; is emitted only when the platform can prove the request was never dispatched to a payment gateway or upstream (for example, the upstream circuit breaker was already open), so the caller may safely fail over without risking a duplicate charge. &#x60;outcome_unknown&#x60; means the request may have reached an upstream and the outcome cannot be proven; reconcile the transaction before retrying. Emission is conservative — any 5xx without a provable determination carries &#x60;outcome_unknown&#x60;. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
