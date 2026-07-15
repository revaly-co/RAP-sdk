# Gateway

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **string** | Gateway name | [optional]
**bank_type_code** | **string** | Bank type code | [optional]
**merchant_account_reference_id** | **string** | Merchant account reference ID at the gateway | [optional]
**gateway_type** | **string** | Type of payment gateway | [optional]
**currency_code** | **string** | Primary currency code for this gateway | [optional]
**accepted_currency_codes** | **string[]** | List of accepted currency codes | [optional]
**accepted_cards** | [**\Revaly\Sdk\Core\Model\AcceptedCards**](AcceptedCards.md) |  | [optional]
**accept_retries** | **bool** | Whether the gateway accepts retry transactions | [optional]
**cvv_required** | **bool** | Whether CVV is required for transactions | [optional]
**approved_charge_or_capture_rate_fee** | **float** | Rate fee for approved charges or captures | [optional]
**approved_charge_or_capture_flat_fee** | **float** | Flat fee for approved charges or captures | [optional]
**other_transaction_flat_fee** | **float** | Flat fee for other transaction types | [optional]
**issue_refunds_through_credit** | **bool** | Whether refunds are issued through credit | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
