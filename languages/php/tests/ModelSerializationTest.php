<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Core\Model\ErrorResponse;
use Revaly\Sdk\Core\Model\GetTransactionById200Response;
use Revaly\Sdk\Core\Model\GetTransactionByMerchantTransactionId200Response;
use Revaly\Sdk\Core\Model\ListTransactions200ResponseInner;
use Revaly\Sdk\Core\Model\StoredCredentialReasonType;
use Revaly\Sdk\Core\Model\TransactionListPaymentMethod;
use Revaly\Sdk\Core\Model\TransactionListPaymentMethodItemTransaction;
use Revaly\Sdk\Core\ObjectSerializer;
use Revaly\Sdk\Errors\FailureClassifier;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Testing\SyntheticData;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * Pins of the generated core's (de)serialization behaviour that the runtime's safety
 * posture depends on — the per-language first-investigation probes, as regression tests.
 * If a regeneration flips any of these, the runtime design assumptions must be
 * re-checked before the pin is updated.
 */
final class ModelSerializationTest extends TestCase
{
    /** A flat `listTransactions` row (the TransactionListItem branch). Synthetic values. */
    private const LIST_FLAT_ROW = '{"transactionId":"t-1","transactionDate":"2025-09-13T03:19:54.86Z",'
        . '"transactionStatus":1,"responseCode":"10000","transactionType":"Charge","amount":2500,'
        . '"currencyCode":"USD"}';

    /** A payment-method `listTransactions` row (the TransactionListPaymentMethodItem branch). */
    private const LIST_PAYMENT_METHOD_ROW = '{"transaction":{"transactionId":"t-2",'
        . '"transactionDate":"2025-12-02T14:44:42.209Z","transactionStatus":1,"message":"Succeeded!",'
        . '"responseCode":"10000","transactionType":"CreateCreditCard","paymentMethod":{'
        . '"paymentMethodId":"pm-1","lastFourDigits":"1111","firstSixDigits":"411111","cardType":"VISA",'
        . '"storageState":"Cached","issuerIdentificationNumber":"41111111"}}}';

    public function testOneOfWrapperSilentlyMergesAllBranches(): void
    {
        // PROBE PIN: the core's oneOf response wrapper is ONE flattened class carrying
        // terminal, pending AND group fields side by side — deserialization performs NO
        // discrimination (DISCRIMINATOR = null). It never throws (unlike the java
        // core's pre-fork wrapper) and never mis-binds to a wrong branch type (unlike
        // dotnet's anyOf order trap) — it simply merges. This is why the runtime's
        // reconcile helper classifies from the RAW body instead (repo rule 5).
        $pending = ObjectSerializer::deserialize(
            json_decode(SyntheticData::pending()),
            GetTransactionByMerchantTransactionId200Response::class,
        );
        self::assertInstanceOf(GetTransactionByMerchantTransactionId200Response::class, $pending);
        self::assertSame('pending', $pending->getState());
        self::assertNull($pending->getTransactionId());

        $terminal = ObjectSerializer::deserialize(
            json_decode(SyntheticData::transaction(1)),
            GetTransactionByMerchantTransactionId200Response::class,
        );
        self::assertInstanceOf(GetTransactionByMerchantTransactionId200Response::class, $terminal);
        self::assertSame(SyntheticData::DEFAULT_TRANSACTION_ID, $terminal->getTransactionId());
        self::assertNull($terminal->getState());
    }

    public function testByIdWrapperHasTheSameMergedShape(): void
    {
        // The by-id wrapper merges the terminal and GROUP branches (it has no pending
        // branch — pending intents are keyed by merchant transaction id only).
        $group = ObjectSerializer::deserialize(
            json_decode(SyntheticData::transactionGroup()),
            GetTransactionById200Response::class,
        );
        self::assertInstanceOf(GetTransactionById200Response::class, $group);
        self::assertNotNull($group->getTransactions());
        self::assertCount(1, $group->getTransactions());
        self::assertNull($group->getTransactionId());

        $terminal = ObjectSerializer::deserialize(
            json_decode(SyntheticData::transaction(1)),
            GetTransactionById200Response::class,
        );
        self::assertInstanceOf(GetTransactionById200Response::class, $terminal);
        self::assertSame(SyntheticData::DEFAULT_TRANSACTION_ID, $terminal->getTransactionId());
        self::assertNull($terminal->getTransactions());
    }

    public function testListTransactionsFlatRowBindsTheTransactionListItemFields(): void
    {
        // PROBE PIN: the listTransactions item wrapper is the same merged shape — ONE
        // class carrying the TransactionListItem fields AND the payment-method row's
        // `transaction` side by side (DISCRIMINATOR = null). "Which branch" reads as which
        // branch's fields are populated: a flat row sets the top-level fields and leaves
        // getTransaction() null.
        $row = ObjectSerializer::deserialize(
            json_decode(self::LIST_FLAT_ROW),
            ListTransactions200ResponseInner::class,
        );
        self::assertListFlatRow($row);
    }

    public function testListTransactionsPaymentMethodRowBindsTheNestedTransaction(): void
    {
        // The payment-method row populates only getTransaction(); the top-level flat
        // fields stay null. The nested card fields are read through
        // getTransaction()->getPaymentMethod().
        $row = ObjectSerializer::deserialize(
            json_decode(self::LIST_PAYMENT_METHOD_ROW),
            ListTransactions200ResponseInner::class,
        );
        self::assertListPaymentMethodRow($row);
    }

    public function testListTransactionsFlatRowWithAnUnknownAdditiveFieldStillBindsTheFlatFields(): void
    {
        // A server-newer additive top-level field is dropped (the deserializer walks only
        // the declared properties); it does not change which fields bind.
        $flat = json_decode(self::LIST_FLAT_ROW);
        $flat->futureAdditiveField = 'x';
        self::assertListFlatRow(
            ObjectSerializer::deserialize($flat, ListTransactions200ResponseInner::class),
        );
    }

    public function testListTransactionsPaymentMethodRowWithAnUnknownAdditiveFieldStillBindsTheNestedTransaction(): void
    {
        $paymentMethod = json_decode(self::LIST_PAYMENT_METHOD_ROW);
        $paymentMethod->futureAdditiveField = 'x';
        self::assertListPaymentMethodRow(
            ObjectSerializer::deserialize($paymentMethod, ListTransactions200ResponseInner::class),
        );
    }

    public function testListTransactionsArrayOfWrapperDeserializesBothShapes(): void
    {
        $rows = ObjectSerializer::deserialize(
            json_decode('[' . self::LIST_FLAT_ROW . ',' . self::LIST_PAYMENT_METHOD_ROW . ']'),
            '\Revaly\Sdk\Core\Model\ListTransactions200ResponseInner[]',
        );
        self::assertIsArray($rows);
        self::assertCount(2, $rows);
        self::assertListFlatRow($rows[0]);
        self::assertListPaymentMethodRow($rows[1]);
    }

    public function testListTransactionsCallThroughTheMockDecodesBothShapes(): void
    {
        $mock = new RapMockTransport();
        $mock->stub('GET', '/transactions')
            ->returns(200, '[' . self::LIST_FLAT_ROW . ',' . self::LIST_PAYMENT_METHOD_ROW . ']');

        $rows = TestClients::withMock($mock)->transactions()->listTransactions();

        self::assertIsArray($rows);
        self::assertCount(2, $rows);
        self::assertListFlatRow($rows[0]);
        self::assertListPaymentMethodRow($rows[1]);
    }

    public function testErrorResponseCoercesUnknownCodesButTheClassifierReadsRaw(): void
    {
        // PROBE PIN: the core model REWRITES unrecognized `code` values to
        // `unknown_default_open_api` (enumUnknownDefaultCase). The §2 contract needs
        // the verbatim open string, which is why FailureClassifier parses the raw body
        // and never the core model.
        $model = new ErrorResponse();
        $model->setCode('brand_new_code_from_oq2');
        self::assertSame('unknown_default_open_api', $model->getCode());

        [$code] = FailureClassifier::parseErrorBody(
            SyntheticData::errorBody('synthetic', 'brand_new_code_from_oq2'),
        );
        self::assertSame('brand_new_code_from_oq2', $code);
    }

    public function testOptionalEnumTypedFieldsAreOmittedWhenUnset(): void
    {
        // PROBE PIN: the dotnet core's optional-inner-enum serializer defect does NOT
        // reproduce here — unset optionals are omitted from the serialized body and no
        // enum validation runs on null values.
        $serialized = ObjectSerializer::sanitizeForSerialization(TestClients::chargeRequest());
        $json = json_encode($serialized, JSON_THROW_ON_ERROR);

        self::assertIsObject($serialized);
        self::assertObjectNotHasProperty('storedCredential', $serialized);
        self::assertObjectNotHasProperty('initiatedBy', $serialized);
        self::assertStringContainsString('"merchantTransactionId":"mtx-synthetic-1"', $json);
        self::assertStringContainsString('"amount":1999', $json);
    }

    public function testStandaloneEnumDeserializeThrowsOnUnknownWireValues(): void
    {
        // PROBE PIN (generator-bakeoff §A3): standalone-enum-typed properties THROW on
        // server-newer-than-spec wire values instead of coercing. The runtime contains
        // this on response paths by classifying an unreadable 2xx as OutcomeUnknown
        // (see ClassificationTest::testUnreadable200ClassifiesOutcomeUnknown).
        $this->expectException(\InvalidArgumentException::class);
        ObjectSerializer::deserialize('brand_new_reason', StoredCredentialReasonType::class);
    }

    public function testKnownEnumValuesDeserializeVerbatim(): void
    {
        self::assertSame(
            'recurring',
            ObjectSerializer::deserialize('recurring', StoredCredentialReasonType::class),
        );
    }

    private static function assertListFlatRow(mixed $row): void
    {
        self::assertInstanceOf(ListTransactions200ResponseInner::class, $row);
        self::assertSame('t-1', $row->getTransactionId());
        self::assertInstanceOf(\DateTime::class, $row->getTransactionDate());
        self::assertSame(1, $row->getTransactionStatus());
        self::assertSame('10000', $row->getResponseCode());
        self::assertSame('Charge', $row->getTransactionType());
        self::assertSame(2500, $row->getAmount());
        self::assertSame('USD', $row->getCurrencyCode());
        self::assertNull($row->getTransaction());
    }

    private static function assertListPaymentMethodRow(mixed $row): void
    {
        self::assertInstanceOf(ListTransactions200ResponseInner::class, $row);
        self::assertNull($row->getTransactionId());
        self::assertNull($row->getResponseCode());

        $transaction = $row->getTransaction();
        self::assertInstanceOf(TransactionListPaymentMethodItemTransaction::class, $transaction);
        self::assertSame('t-2', $transaction->getTransactionId());
        self::assertInstanceOf(\DateTime::class, $transaction->getTransactionDate());
        self::assertSame(1, $transaction->getTransactionStatus());
        self::assertSame('Succeeded!', $transaction->getMessage());
        self::assertSame('CreateCreditCard', $transaction->getTransactionType());

        $paymentMethod = $transaction->getPaymentMethod();
        self::assertInstanceOf(TransactionListPaymentMethod::class, $paymentMethod);
        self::assertSame('pm-1', $paymentMethod->getPaymentMethodId());
        self::assertSame('1111', $paymentMethod->getLastFourDigits());
        self::assertSame('411111', $paymentMethod->getFirstSixDigits());
        self::assertSame('VISA', $paymentMethod->getCardType());
    }
}
