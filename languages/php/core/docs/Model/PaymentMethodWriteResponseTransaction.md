# PaymentMethodWriteResponseTransaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **string** | Unique identifier for the transaction | [optional]
**transaction_date** | **\DateTime** | Date and time when the transaction was processed | [optional]
**transaction_status** | **int** | Current status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional]
**message** | **string** | Human-readable message about the transaction | [optional]
**response_code** | **string** | Gateway response code | [optional]
**transaction_type** | **string** | Type of transaction | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
