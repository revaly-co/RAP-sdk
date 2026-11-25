# TransactionListPaymentMethodItemTransaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **string** | Unique transaction identifier |
**transaction_date** | **\DateTime** | Date and time when the operation was processed (ISO 8601, UTC) |
**transaction_status** | **int** | Status of the operation (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) |
**message** | **string** | Human-readable message about the result | [optional]
**customer_id** | **string** | Customer identifier associated with the operation | [optional]
**response_code** | **string** | Response code from the processing result | [optional]
**transaction_type** | **string** | The payment-method operation: CreateCreditCard, CreateGatewayPaymentMethod, UpdatePaymentMethod, RedactPaymentMethod or RecachePaymentMethod | [optional]
**payment_method** | [**\Revaly\Sdk\Core\Model\TransactionListPaymentMethod**](TransactionListPaymentMethod.md) |  | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
