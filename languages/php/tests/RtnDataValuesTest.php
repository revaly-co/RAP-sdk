<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Core\Model\ModelInterface;
use Revaly\Sdk\Core\Model\RtnData;
use Revaly\Sdk\Core\Model\RtnDataCustomerData;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Tests\Support\TestClients;

/**
 * ADR-SDK-034 amendment of 2026-11-26 (SC-1018, OQ-19): for the rtnData block (RtnData and
 * its ten nested models, the only schemas the platform exempts) the setters neither refuse a
 * value that breaks a documented pattern, minimum or minLength nor replace an unlisted value
 * with the unknown_default_open_api sentinel; the platform's own rule decides. Each table
 * below breaks every such rule the spec documents in the family, so a change that misses one
 * field, shape or file fails here. The non-null guards, the *_UNKNOWN_DEFAULT_OPEN_API
 * constants and the get*AllowableValues() methods stay.
 *
 * Every value goes through the public setter and is read back from the getter and from the
 * mock transport's recorded request. The checks kept outside rtnData are pinned in
 * LengthBoundsTest. All values are synthetic (ADR-SDK-020); none is card data.
 */
final class RtnDataValuesTest extends TestCase
{
    private const DASHED_DATE = '2024-01-15'; // every rtnData date field documents ^\d{8}$
    private const UNLISTED = 'unlisted_synthetic_value';

    /** rtnData block => [wire key => a value that breaks the field's documented pattern]. */
    private const PATTERN_BREAKS = [
        'additionalTransactionData' => [
            'fraudPreventionPlatform' => 'not allowed!', // ^[A-Za-z0-9._:-]{1,128}$
            'fullPan' => '1234-5678-9012', // ^\d{13,19}$, and long enough for minLength 13
        ],
        'customerData' => [
            'accountOpenedDate' => self::DASHED_DATE,
            'accountLastChangedDate' => self::DASHED_DATE,
            'passwordLastChangedDate' => self::DASHED_DATE,
            'paymentMethodAddedDate' => self::DASHED_DATE,
        ],
        'merchantData' => ['merchantAccountOpenedDate' => self::DASHED_DATE],
        'orderData' => ['preOrderDate' => self::DASHED_DATE, 'recurringEndDate' => self::DASHED_DATE],
        'shippingData' => ['addressFirstUsedDate' => self::DASHED_DATE],
    ];

    /** rtnData block => [wire key => a value under the field's documented minimum]. */
    private const MINIMUM_BREAKS = [
        'customerData' => [
            'transactionSuccessfulCountLastSixMonths' => -1,
            'transactionAttemptedCountLast24Hours' => -1,
            'transactionAttemptedCountLastYear' => -1,
            'paymentMethodAddAttemptCountLast24Hours' => -1,
            'registeredAccountTenure' => -1,
            'daysSinceNameChange' => -1,
            'daysSinceEmailChange' => -1,
            'daysSincePasswordChange' => -1,
            'daysSincePostalCodeChange' => -1,
            'daysSinceAddressChange' => -1,
            'daysSincePhoneChange' => -1,
            'daysSinceShipToNameChange' => -1,
        ],
        'orderData' => [
            'itemCount' => -1,
            'highestPriceItemPrice' => -1,
            'installmentPaymentCount' => -1,
            'recurringIntervalDays' => 0, // the one minimum of 1
            'giftCardCount' => -1,
            'giftCardAmount' => -1,
        ],
        'shippingData' => ['shippingAddressCount' => -1, 'daysSinceShipToAddressChange' => -1],
    ];

    /** rtnData block => [wire key => a value shorter than the field's documented minLength]. */
    private const MIN_LENGTH_BREAKS = [
        'additionalTransactionData' => ['fullPan' => '1234'], // minLength 13
        'billingData' => ['country' => 'U'], // minLength 2
        'deviceData' => ['country' => 'U'],
        'shippingData' => ['country' => 'U'],
    ];

    /** rtnData block => [wire key => a value its documented value list does not hold]. */
    private const UNLISTED_VALUES = [
        'additionalTransactionData' => [
            'providerAuthDecision' => self::UNLISTED,
            'paymentRail' => self::UNLISTED,
            'posEntryMode' => self::UNLISTED,
            'merchantTrustLevel' => self::UNLISTED,
            'cardBrand' => self::UNLISTED,
            'messageCategory' => self::UNLISTED,
        ],
        'customerData' => [
            'accountAgeIndicator' => '05', // documented values 01 to 04
            'accountChangeIndicator' => self::UNLISTED,
            'passwordChangeIndicator' => self::UNLISTED,
            'paymentMethodAgeIndicator' => self::UNLISTED,
            'accountAuthenticationMethod' => self::UNLISTED,
            'isRegisteredCustomer' => self::UNLISTED,
            'isRegistrationUpdated' => self::UNLISTED,
        ],
        'deviceData' => ['channel' => self::UNLISTED, 'deviceType' => self::UNLISTED],
        'merchantData' => ['merchantAccountAgeIndicator' => self::UNLISTED],
        'orderData' => ['alternatePaymentIndicator' => self::UNLISTED, 'isCouponUsed' => self::UNLISTED],
        'sellerData' => ['sellerRegion' => self::UNLISTED, 'transactionTypeIndicator' => self::UNLISTED],
        'shippingData' => [
            'shippingIndicator' => self::UNLISTED,
            'addressFirstUsedIndicator' => self::UNLISTED,
            'deliveryTimeframeIndicator' => self::UNLISTED,
        ],
    ];

    /** @return array<string, array{array<string, array<string, int|string>>}> */
    public static function rules(): array
    {
        return [
            'pattern' => [self::PATTERN_BREAKS],
            'minimum' => [self::MINIMUM_BREAKS],
            'minLength' => [self::MIN_LENGTH_BREAKS],
            'value list' => [self::UNLISTED_VALUES],
        ];
    }

    /** @param array<string, array<string, int|string>> $values */
    #[DataProvider('rules')]
    public function testChargeSendsTheValueAsGiven(array $values): void
    {
        // AC4: before the change the setter threw (pattern, minimum, minLength) or stored
        // unknown_default_open_api (value list).
        $rtnData = self::rtnData($values);
        self::assertStoredAsGiven($values, $rtnData);
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        $request = TestClients::chargeRequest();
        $request->setRtnData($rtnData);

        TestClients::withMock($mock)->charge($request);

        self::assertSentAsGiven($values, $mock);
    }

    /** @param array<string, array<string, int|string>> $values */
    #[DataProvider('rules')]
    public function testAuthorizeSendsTheValueAsGiven(array $values): void
    {
        // AC4: rtnData rides AuthorizeRequest too.
        $rtnData = self::rtnData($values);
        self::assertStoredAsGiven($values, $rtnData);
        $mock = new RapMockTransport();
        $mock->authorize()->returnsApproved();
        $request = TestClients::authorizeRequest();
        $request->setRtnData($rtnData);

        TestClients::withMock($mock)->authorize($request);

        self::assertSentAsGiven($values, $mock);
    }

    public function testFamilyModelsHoldingBreakingAndUnlistedValuesReportNothingInvalid(): void
    {
        // X3 (Gate 2 option A): listInvalidProperties() drops the pattern, minimum and
        // minLength entries and the value-list entries too, so a model the SDK sends by
        // design never reports itself invalid. No rtnData field is required.
        foreach (self::allBreaks() as $block => $fields) {
            $model = self::model($block, $fields);

            self::assertSame([], $model->listInvalidProperties(), $block);
            self::assertTrue($model->valid(), $block);
        }
    }

    public function testValueListConstantsAndGettersStayPublic(): void
    {
        // D6 (patch release): the public API the value lists generate stays, though the
        // setters no longer use it.
        $checked = 0;
        foreach (self::UNLISTED_VALUES as $block => $fields) {
            $class = self::modelClass($block);
            foreach (array_keys($fields) as $key) {
                $constant = $class . '::'
                    . strtoupper((string) preg_replace('/(?<!^)[A-Z]/', '_$0', $key))
                    . '_UNKNOWN_DEFAULT_OPEN_API';
                $getter = 'get' . ucfirst($key) . 'AllowableValues';

                self::assertTrue(defined($constant), $constant);
                self::assertSame('unknown_default_open_api', constant($constant));
                self::assertTrue(method_exists($class, $getter), $class . '::' . $getter);
                $allowed = (new $class())->{$getter}();
                self::assertContains(constant($constant), $allowed);
                self::assertGreaterThan(1, count($allowed), $class . '::' . $getter);
                $checked++;
            }
        }
        self::assertSame(23, $checked);
        // The name merchants reference directly (it was the stored sentinel until SC-1018).
        self::assertSame(
            'unknown_default_open_api',
            RtnDataCustomerData::ACCOUNT_AGE_INDICATOR_UNKNOWN_DEFAULT_OPEN_API,
        );
    }

    public function testNonNullGuardsStay(): void
    {
        // D3: "The non-null guards stay", on every setter the change edits.
        $checked = 0;
        foreach (self::allBreaks() as $block => $fields) {
            $class = self::modelClass($block);
            foreach (array_keys($fields) as $key) {
                $setter = 'set' . ucfirst($key);
                try {
                    (new $class())->{$setter}(null);
                    self::fail($class . '::' . $setter . ' accepted null');
                } catch (\InvalidArgumentException $refused) {
                    self::assertStringContainsString('cannot be null', $refused->getMessage(), $setter);
                }
                $checked++;
            }
        }
        // 10 pattern, 20 minimum, 4 minLength (fullPan has both) and 23 value-list fields.
        self::assertSame(56, $checked);
    }

    /** @return array<string, array<string, int|string>> every table merged, one value per field */
    private static function allBreaks(): array
    {
        return array_replace_recursive(
            self::PATTERN_BREAKS,
            self::MINIMUM_BREAKS,
            self::MIN_LENGTH_BREAKS,
            self::UNLISTED_VALUES,
        );
    }

    /** @return class-string<ModelInterface> */
    private static function modelClass(string $block): string
    {
        $class = 'Revaly\\Sdk\\Core\\Model\\RtnData' . ucfirst($block);
        self::assertTrue(class_exists($class), $class);

        return $class;
    }

    /** @param array<string, int|string> $fields */
    private static function model(string $block, array $fields): ModelInterface
    {
        $class = self::modelClass($block);
        $model = new $class();
        foreach ($fields as $key => $value) {
            $setter = 'set' . ucfirst($key);
            self::assertTrue(method_exists($model, $setter), $class . '::' . $setter);
            $model->{$setter}($value);
        }

        return $model;
    }

    /** @param array<string, array<string, int|string>> $values */
    private static function rtnData(array $values): RtnData
    {
        $rtnData = new RtnData();
        foreach ($values as $block => $fields) {
            $rtnData->{'set' . ucfirst($block)}(self::model($block, $fields));
        }

        return $rtnData;
    }

    /** @param array<string, array<string, int|string>> $values */
    private static function assertStoredAsGiven(array $values, RtnData $rtnData): void
    {
        foreach ($values as $block => $fields) {
            $model = $rtnData->{'get' . ucfirst($block)}();
            foreach ($fields as $key => $value) {
                self::assertSame($value, $model->{'get' . ucfirst($key)}(), $block . '.' . $key);
            }
        }
    }

    /** @param array<string, array<string, int|string>> $values */
    private static function assertSentAsGiven(array $values, RapMockTransport $mock): void
    {
        $requests = $mock->getRequests();
        self::assertCount(1, $requests);
        $body = json_decode($requests[0]->body, true, 512, JSON_THROW_ON_ERROR);

        self::assertSame(self::sortedKeys($values), self::sortedKeys($body['rtnData']));
    }

    /**
     * @param array<mixed> $value
     * @return array<mixed>
     */
    private static function sortedKeys(array $value): array
    {
        ksort($value);
        foreach ($value as $key => $item) {
            if (is_array($item)) {
                $value[$key] = self::sortedKeys($item);
            }
        }

        return $value;
    }
}
