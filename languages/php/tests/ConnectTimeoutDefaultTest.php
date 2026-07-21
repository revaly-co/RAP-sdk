<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use GuzzleHttp\Client as GuzzleClient;
use GuzzleHttp\RequestOptions;
use PHPUnit\Framework\TestCase;
use Revaly\Sdk\RapClient;
use Revaly\Sdk\Testing\RapMockTransport;

/**
 * ADR-SDK-029 connect-timeout-default semantics: an omitted connectTimeout resolves to
 * the 10-second edge-ratified default, an explicit null opts out entirely, explicit
 * values pass through, and zero/negative values are rejected at construction.
 */
final class ConnectTimeoutDefaultTest extends TestCase
{
    /** Reads the CONNECT_TIMEOUT the client actually configured on its Guzzle wire. */
    private static function wiredConnectTimeout(RapClient $client): mixed
    {
        $prop = new \ReflectionProperty(RapClient::class, 'guzzle');
        /** @var GuzzleClient $guzzle */
        $guzzle = $prop->getValue($client);

        return $guzzle->getConfig(RequestOptions::CONNECT_TIMEOUT);
    }

    public function testOmittedResolvesToTheRatifiedDefault(): void
    {
        self::assertSame(10.0, RapClient::DEFAULT_CONNECT_TIMEOUT_SECONDS);

        $client = new RapClient(apiKey: 'sk-synthetic-test', transport: new RapMockTransport());

        self::assertSame(10.0, self::wiredConnectTimeout($client));
    }

    public function testExplicitNullOptsOutOfAnySdkConnectBound(): void
    {
        $client = new RapClient(
            apiKey: 'sk-synthetic-test',
            connectTimeout: null,
            transport: new RapMockTransport(),
        );

        // 0 is Guzzle's "no connect timeout" — the pre-ADR-029 unset behaviour.
        self::assertSame(0, self::wiredConnectTimeout($client));
    }

    public function testExplicitValuesPassThroughUnchanged(): void
    {
        $client = new RapClient(
            apiKey: 'sk-synthetic-test',
            connectTimeout: 3.0,
            transport: new RapMockTransport(),
        );

        self::assertSame(3.0, self::wiredConnectTimeout($client));
    }

    public function testZeroConnectTimeoutIsRejected(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        new RapClient(apiKey: 'sk-synthetic-test', connectTimeout: 0.0);
    }

    public function testNegativeConnectTimeoutIsRejected(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        new RapClient(apiKey: 'sk-synthetic-test', connectTimeout: -5.0);
    }
}
