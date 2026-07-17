<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use PHPUnit\Framework\TestCase;
use Revaly\Sdk\Reconcile\ReconcilePolicy;
use Revaly\Sdk\Testing\RapMockTransport;
use Revaly\Sdk\Testing\SyntheticData;
use Revaly\Sdk\Tests\Support\TestClients;
use Revaly\Sdk\Transport\RapHeaders;

/**
 * Transport-level header enforcement (runtime-tdd §5; ADR-SDK-005): User-Agent grammar,
 * X-Api-Version pin, and the mandatory `ApiKey` auth scheme — set where the core cannot
 * bypass them.
 */
final class TransportHeadersTest extends TestCase
{
    public function testUserAgentFollowsTheNormativeGrammar(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        TestClients::withMock($mock)->charge(TestClients::chargeRequest());

        $userAgent = $mock->getRequests()[0]->header(RapHeaders::USER_AGENT);

        self::assertNotNull($userAgent);
        self::assertMatchesRegularExpression(
            '#^revaly-sdk-php/\d+\.\d+\.\d+ \(php \d+\.\d+; (windows|linux|darwin|other)\)$#',
            $userAgent,
        );
    }

    public function testCorePlaceholderUserAgentNeverEscapes(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        TestClients::withMock($mock)->charge(TestClients::chargeRequest());

        $userAgent = $mock->getRequests()[0]->header(RapHeaders::USER_AGENT);

        self::assertStringNotContainsString('unwrapped-core', (string) $userAgent);
    }

    public function testMerchantSuffixAppendsAfterTheSdkToken(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        TestClients::withMock($mock, userAgentSuffix: 'merchant-app/2.0')
            ->charge(TestClients::chargeRequest());

        $userAgent = (string) $mock->getRequests()[0]->header(RapHeaders::USER_AGENT);

        // ADR-SDK-005: the SDK token stays FIRST and intact; merchant tokens append.
        self::assertStringStartsWith('revaly-sdk-php/', $userAgent);
        self::assertStringEndsWith(') merchant-app/2.0', $userAgent);
    }

    public function testApiVersionPinsTwoDotOneByDefault(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        TestClients::withMock($mock)->charge(TestClients::chargeRequest());

        self::assertSame('2.1', $mock->getRequests()[0]->header(RapHeaders::API_VERSION));
    }

    public function testApiVersionOverrideIsSent(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        TestClients::withMock($mock, apiVersion: '2.0')->charge(TestClients::chargeRequest());

        self::assertSame('2.0', $mock->getRequests()[0]->header(RapHeaders::API_VERSION));
    }

    public function testAuthorizationUsesTheApiKeySchemeNotBearer(): void
    {
        $mock = new RapMockTransport();
        $mock->charge()->returnsApproved();
        TestClients::withMock($mock)->charge(TestClients::chargeRequest());

        // The RAP scheme is `ApiKey <key>` — the prefix is mandatory and NOT Bearer.
        self::assertSame(
            'ApiKey ' . TestClients::API_KEY,
            $mock->getRequests()[0]->header(RapHeaders::AUTHORIZATION),
        );
    }

    public function testReconcileRequestsCarryTheSameHeaderSet(): void
    {
        $mock = new RapMockTransport();
        $mock->reconcile(SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID)->returnsApproved();
        TestClients::withMock($mock)->reconcile(
            SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID,
            new ReconcilePolicy(1, 5.0, 0.0),
        );

        $request = $mock->getRequests()[0];

        self::assertSame('GET', $request->method);
        self::assertSame(
            '/transactions/merchant/' . SyntheticData::DEFAULT_MERCHANT_TRANSACTION_ID,
            $request->path,
        );
        self::assertSame('ApiKey ' . TestClients::API_KEY, $request->header(RapHeaders::AUTHORIZATION));
        self::assertSame('2.1', $request->header(RapHeaders::API_VERSION));
        self::assertStringStartsWith('revaly-sdk-php/', (string) $request->header(RapHeaders::USER_AGENT));
    }

    public function testMockAssertsTheUserAgentContract(): void
    {
        $mock = new RapMockTransport();
        $mock->stub('GET', '/')->returnsApproved();

        // A bare Guzzle request without the runtime middlewares must fail the mock's
        // ADR-SDK-005 assertion (DX contract §d: the mock asserts User-Agent presence).
        $bareClient = new \GuzzleHttp\Client(['handler' => \GuzzleHttp\HandlerStack::create($mock)]);

        $this->expectException(\LogicException::class);
        $this->expectExceptionMessageMatches('/User-Agent/');
        $bareClient->get('https://sandbox.synthetic.test/anything');
    }
}
