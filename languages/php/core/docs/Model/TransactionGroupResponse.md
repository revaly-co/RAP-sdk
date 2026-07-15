# TransactionGroupResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transaction** | [**\Revaly\Sdk\Core\Model\TransactionResponse**](TransactionResponse.md) | The transaction matching the supplied id (the record the non-expanded lookup returns). | [optional]
**transactions** | [**\Revaly\Sdk\Core\Model\TransactionResponse[]**](TransactionResponse.md) | Every transaction in the payment, ordered by transaction date ascending. Capped at 100. | [optional]

[[Back to Model list]](../../README.md#models) [[Back to API list]](../../README.md#endpoints) [[Back to README]](../../README.md)
