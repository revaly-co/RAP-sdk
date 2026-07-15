

# Gateway

Gateway configuration and settings

## Properties

| Name | Type | Description | Notes |
|------------ | ------------- | ------------- | -------------|
|**name** | **String** | Gateway name |  [optional] |
|**bankTypeCode** | **String** | Bank type code |  [optional] |
|**merchantAccountReferenceId** | **String** | Merchant account reference ID at the gateway |  [optional] |
|**gatewayType** | **String** | Type of payment gateway |  [optional] |
|**currencyCode** | **String** | Primary currency code for this gateway |  [optional] |
|**acceptedCurrencyCodes** | **List&lt;String&gt;** | List of accepted currency codes |  [optional] |
|**acceptedCards** | [**AcceptedCards**](AcceptedCards.md) |  |  [optional] |
|**acceptRetries** | **Boolean** | Whether the gateway accepts retry transactions |  [optional] |
|**cvvRequired** | **Boolean** | Whether CVV is required for transactions |  [optional] |
|**approvedChargeOrCaptureRateFee** | **Double** | Rate fee for approved charges or captures |  [optional] |
|**approvedChargeOrCaptureFlatFee** | **Double** | Flat fee for approved charges or captures |  [optional] |
|**otherTransactionFlatFee** | **Double** | Flat fee for other transaction types |  [optional] |
|**issueRefundsThroughCredit** | **Boolean** | Whether refunds are issued through credit |  [optional] |



