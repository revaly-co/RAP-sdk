# Revaly.Sdk.Core.Model.CreatePaymentMethodRequest
Request to create a new payment method

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**PaymentMethodType** | **string** | Type of payment method to create: - **creditCard**: Use raw credit card details that will be tokenized - **gatewayPaymentMethodId**: Use an existing token from a supported payment gateway  | 
**CustomerId** | **string** | Unique identifier for the customer | [optional] 
**PaymentMethod** | [**PaymentMethod**](PaymentMethod.md) |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

