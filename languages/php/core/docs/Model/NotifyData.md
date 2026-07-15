# NotifyData

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction_id** | **string** | Revaly transaction identifier | [optional]
**merchant_transaction_id** | **string** | Merchant&#39;s transaction identifier | [optional]
**order_id** | **string** | Order identifier associated with the transaction | [optional]
**customer_id** | **string** | Customer identifier | [optional]
**amount** | **int** | Transaction amount in smallest currency unit (e.g., cents for USD) | [optional]
**currency** | **string** | Three-letter ISO currency code | [optional]
**customer_account_number** | **string** | Customer account number for recovery purposes | [optional]
**disable_sms_notification** | **bool** | Whether to disable SMS notifications for this customer | [optional]
**disable_email_notification** | **bool** | Whether to disable email notifications for this customer | [optional]
**contact_information** | [**\Revaly\Sdk\Core\Model\NotifyContactInformation**](NotifyContactInformation.md) |  | [optional]
**address** | [**\Revaly\Sdk\Core\Model\Address**](Address.md) |  | [optional]
**reason_code** | **string** | Network chargeback reason code (e.g. Visa \&quot;10.4\&quot;). Chargeback-only, optional. | [optional]
**arn** | **string** | Acquirer Reference Number or network case ID for the dispute. Chargeback-only, optional. | [optional]
**dispute_date** | **\DateTime** | When the dispute was raised. Chargeback-only, optional. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
