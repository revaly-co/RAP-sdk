# OpenAPIClient-php

Payment processing API for transaction and payment method management.

## API Versioning

RAP supports an explicit, selectable API version so you can build against a
stable, pinned contract while existing integrations keep working unchanged.

- **How to select a version:** send the `X-Api-Version` request header
  (e.g. `X-Api-Version: 2.0`). The version lives in the header — request
  URLs do not change.
- **Default when omitted:** requests without the header (or with an
  unrecognised header name) bind to the **base version `2.0`**, which is the
  current contract. Existing integrations therefore continue unchanged.
- **Unsupported versions:** a header naming a version that does not exist
  returns **HTTP 400** with a structured error listing the supported
  versions — a request is never silently bound to a different contract.
  This includes an **empty or whitespace value**: if the `X-Api-Version`
  header is present, it must name a supported version. Only a fully
  absent header binds to the default.
- **Supported versions** are advertised via the `api-supported-versions`
  header on every response from the versioned API endpoints (payments,
  payment methods, transactions, notify). Currently: `2.0`, `2.1`.
- **Which version to use:** new integrations should pin **`2.1`**. It is
  behaviourally identical to `2.0` today, and it is where future contract
  refinements will land — pinning it now means you never migrate the
  header. `2.0` is the frozen launch contract and remains the binding for
  requests that send no version header.



## Installation & Usage

### Requirements

PHP 8.1 and later.

### Composer

To install the bindings via [Composer](https://getcomposer.org/), add the following to `composer.json`:

```json
{
  "repositories": [
    {
      "type": "vcs",
      "url": "https://github.com/GIT_USER_ID/GIT_REPO_ID.git"
    }
  ],
  "require": {
    "GIT_USER_ID/GIT_REPO_ID": "*@dev"
  }
}
```

Then run `composer install`

### Manual Installation

Download the files and include `autoload.php`:

```php
<?php
require_once('/path/to/OpenAPIClient-php/vendor/autoload.php');
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```php
<?php
require_once(__DIR__ . '/vendor/autoload.php');



// Configure API key authorization: ApiKeyAuth
// The API requires the `ApiKey` scheme prefix in the Authorization header:
//   Authorization: ApiKey YOUR_API_KEY
// setApiKeyPrefix joins prefix and key with a space — both calls below are required.
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKey('Authorization', 'YOUR_API_KEY');
$config = Revaly\Sdk\Core\Configuration::getDefaultConfiguration()->setApiKeyPrefix('Authorization', 'ApiKey');


$apiInstance = new Revaly\Sdk\Core\Api\NotifyApi(
    // If you want use custom http client, pass your client which implements `GuzzleHttp\ClientInterface`.
    // This is optional, `GuzzleHttp\Client` will be used as default.
    new GuzzleHttp\Client(),
    $config
);
$notify_request = {"eventType":"recordPayment","data":{"merchantTransactionId":"merch_txn_abc123","orderID":"order_456789","customerId":"customer_123","amount":2500,"currency":"USD","customerAccountNumber":"ACC-001234","disableSmsNotification":false,"disableEmailNotification":false}}; // \Revaly\Sdk\Core\Model\NotifyRequest
$x_api_version = 2.1; // string | Selects the RAP API version for this request. New integrations should pin `2.1` (identical to `2.0` today; future refinements land there). Omit to use the base version (`2.0`). A value naming an unsupported version — including an empty value — returns HTTP 400; if the header is sent, it must name a supported version. See the API description for the full version policy.

try {
    $result = $apiInstance->notifyRevaly($notify_request, $x_api_version);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling NotifyApi->notifyRevaly: ', $e->getMessage(), PHP_EOL;
}

```

## API Endpoints

All URIs are relative to *https://api.revaly.co*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*NotifyApi* | [**notifyRevaly**](docs/Api/NotifyApi.md#notifyrevaly) | **POST** /notify | Notify Revaly of payment events
*PaymentMethodsApi* | [**createPaymentMethod**](docs/Api/PaymentMethodsApi.md#createpaymentmethod) | **POST** /payment-methods/create | Create a payment method
*PaymentMethodsApi* | [**getPaymentMethod**](docs/Api/PaymentMethodsApi.md#getpaymentmethod) | **GET** /payment-methods/show/{paymentMethodId} | Get payment method details
*PaymentMethodsApi* | [**listPaymentMethods**](docs/Api/PaymentMethodsApi.md#listpaymentmethods) | **GET** /payment-methods/list | List payment methods
*PaymentMethodsApi* | [**recachePaymentMethod**](docs/Api/PaymentMethodsApi.md#recachepaymentmethod) | **POST** /payment-methods/recache/{paymentMethodId} | Recache payment method
*PaymentMethodsApi* | [**redactPaymentMethod**](docs/Api/PaymentMethodsApi.md#redactpaymentmethod) | **POST** /payment-methods/redact/{paymentMethodId} | Redact payment method
*PaymentMethodsApi* | [**updatePaymentMethod**](docs/Api/PaymentMethodsApi.md#updatepaymentmethod) | **POST** /payment-methods/update/{paymentMethodId} | Update payment method
*PaymentsApi* | [**authorizePayment**](docs/Api/PaymentsApi.md#authorizepayment) | **POST** /payments/authorize | Authorize a payment
*PaymentsApi* | [**capturePayment**](docs/Api/PaymentsApi.md#capturepayment) | **POST** /payments/capture/{transactionId} | Capture an authorized payment
*PaymentsApi* | [**chargePayment**](docs/Api/PaymentsApi.md#chargepayment) | **POST** /payments | Process a payment (charge)
*PaymentsApi* | [**refundCancelPaymentByMerchantTransactionId**](docs/Api/PaymentsApi.md#refundcancelpaymentbymerchanttransactionid) | **POST** /payments/refund-cancel/merchant/{merchantTransactionId} | Refund or cancel a payment transaction by merchant transaction ID
*PaymentsApi* | [**refundPayment**](docs/Api/PaymentsApi.md#refundpayment) | **POST** /payments/refund/{transactionId} | Refund a payment transaction by TransactionId
*PaymentsApi* | [**voidPayment**](docs/Api/PaymentsApi.md#voidpayment) | **POST** /payments/void/{transactionId} | Void a payment transaction
*TransactionsApi* | [**getTransactionById**](docs/Api/TransactionsApi.md#gettransactionbyid) | **GET** /transactions/{transactionId} | Get transaction details
*TransactionsApi* | [**getTransactionByMerchantTransactionId**](docs/Api/TransactionsApi.md#gettransactionbymerchanttransactionid) | **GET** /transactions/merchant/{merchantTransactionId} | Get transaction details by merchant transaction ID
*TransactionsApi* | [**listTransactions**](docs/Api/TransactionsApi.md#listtransactions) | **GET** /transactions | List transactions

## Models

- [AcceptedCards](docs/Model/AcceptedCards.md)
- [Address](docs/Model/Address.md)
- [AuthorizeRequest](docs/Model/AuthorizeRequest.md)
- [BillingPlan](docs/Model/BillingPlan.md)
- [CaptureRequest](docs/Model/CaptureRequest.md)
- [CardFeatures](docs/Model/CardFeatures.md)
- [CreatePaymentMethodRequest](docs/Model/CreatePaymentMethodRequest.md)
- [CreditCard](docs/Model/CreditCard.md)
- [ErrorResponse](docs/Model/ErrorResponse.md)
- [Gateway](docs/Model/Gateway.md)
- [GatewayPaymentMethod](docs/Model/GatewayPaymentMethod.md)
- [GetTransactionById200Response](docs/Model/GetTransactionById200Response.md)
- [GetTransactionByMerchantTransactionId200Response](docs/Model/GetTransactionByMerchantTransactionId200Response.md)
- [InitiatedBy](docs/Model/InitiatedBy.md)
- [NotifyContactInformation](docs/Model/NotifyContactInformation.md)
- [NotifyData](docs/Model/NotifyData.md)
- [NotifyRequest](docs/Model/NotifyRequest.md)
- [NotifyResponse](docs/Model/NotifyResponse.md)
- [PaymentMethod](docs/Model/PaymentMethod.md)
- [PaymentMethodRecacheRequest](docs/Model/PaymentMethodRecacheRequest.md)
- [PaymentMethodRecacheRequestPaymentMethod](docs/Model/PaymentMethodRecacheRequestPaymentMethod.md)
- [PaymentMethodRecacheRequestPaymentMethodCreditCard](docs/Model/PaymentMethodRecacheRequestPaymentMethodCreditCard.md)
- [PaymentMethodResponse](docs/Model/PaymentMethodResponse.md)
- [PaymentMethodWriteResponse](docs/Model/PaymentMethodWriteResponse.md)
- [PaymentMethodWriteResponseTransaction](docs/Model/PaymentMethodWriteResponseTransaction.md)
- [PaymentPlanData](docs/Model/PaymentPlanData.md)
- [PaymentRequest](docs/Model/PaymentRequest.md)
- [PendingTransactionResponse](docs/Model/PendingTransactionResponse.md)
- [PreviousTransaction](docs/Model/PreviousTransaction.md)
- [Recovery](docs/Model/Recovery.md)
- [RefundCancelRequest](docs/Model/RefundCancelRequest.md)
- [RefundRequest](docs/Model/RefundRequest.md)
- [RtnData](docs/Model/RtnData.md)
- [RtnDataAdditionalTransactionData](docs/Model/RtnDataAdditionalTransactionData.md)
- [RtnDataBillingData](docs/Model/RtnDataBillingData.md)
- [RtnDataCustomData](docs/Model/RtnDataCustomData.md)
- [RtnDataCustomerData](docs/Model/RtnDataCustomerData.md)
- [RtnDataDeviceData](docs/Model/RtnDataDeviceData.md)
- [RtnDataMerchantData](docs/Model/RtnDataMerchantData.md)
- [RtnDataOrderData](docs/Model/RtnDataOrderData.md)
- [RtnDataPartnerRiskData](docs/Model/RtnDataPartnerRiskData.md)
- [RtnDataSellerData](docs/Model/RtnDataSellerData.md)
- [RtnDataShippingData](docs/Model/RtnDataShippingData.md)
- [StoredCredential](docs/Model/StoredCredential.md)
- [StoredCredentialReasonType](docs/Model/StoredCredentialReasonType.md)
- [StoredCredentialResponse](docs/Model/StoredCredentialResponse.md)
- [ThreeDS](docs/Model/ThreeDS.md)
- [TransactionGateway](docs/Model/TransactionGateway.md)
- [TransactionGroupResponse](docs/Model/TransactionGroupResponse.md)
- [TransactionListItem](docs/Model/TransactionListItem.md)
- [TransactionResponse](docs/Model/TransactionResponse.md)
- [TransactionResponseDetails](docs/Model/TransactionResponseDetails.md)
- [UpdatePaymentMethodRequest](docs/Model/UpdatePaymentMethodRequest.md)
- [VaultPaymentMethod](docs/Model/VaultPaymentMethod.md)
- [VoidRequest](docs/Model/VoidRequest.md)

## Authorization

Authentication schemes defined for the API:
### ApiKeyAuth

- **Type**: API key
- **API key parameter name**: Authorization
- **Location**: HTTP header


## Tests

To run the tests, use:

```bash
composer install
vendor/bin/phpunit
```

## Author



## About this package

This PHP package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: `2.2.0`
    - Generator version: `7.23.0`
- Build package: `org.openapitools.codegen.languages.PhpClientCodegen`
