<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Core\Model\ErrorResponse;
use Revaly\Sdk\Core\Model\GetTransactionById200Response;
use Revaly\Sdk\Core\Model\GetTransactionByMerchantTransactionId200Response;
use Revaly\Sdk\Core\Model\StoredCredentialReasonType;
use Revaly\Sdk\Core\ObjectSerializer;
use Revaly\Sdk\Errors\FailureClassifier;
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
}
