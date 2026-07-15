# CreatePaymentMethodRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_method_type** | **string** | Type of payment method to create: - **creditCard**: Use raw credit card details that will be tokenized - **gatewayPaymentMethodId**: Use an existing token from a supported payment gateway |
**customer_id** | **string** | Unique identifier for the customer | [optional]
**payment_method** | [**\Revaly\Sdk\Core\Model\PaymentMethod**](PaymentMethod.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
