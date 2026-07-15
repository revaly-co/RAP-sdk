# PreviousTransaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_date** | **\DateTime** | Date of the previous transaction | [optional]
**merchant_account_reference_id** | **string** | Merchant account reference ID from the previous transaction | [optional]
**gateway_code** | **string** | Gateway response code from the previous transaction | [optional]
**gateway_message** | **string** | Gateway response message from the previous transaction | [optional]
**gateway_message_key** | **string** | Gateway message key from the previous transaction | [optional]
**transaction_status** | **int** | Previous status of the transaction (1 &#x3D; Approved, 2 &#x3D; Declined, 3 &#x3D; Error) | [optional]
**avs_code** | **string** | AVS code from the previous transaction | [optional]
**avs_message** | **string** | AVS message from the previous transaction | [optional]
**cvv_code** | **string** | CVV code from the previous transaction | [optional]
**cvv_message** | **string** | CVV message from the previous transaction | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
