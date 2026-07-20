<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests;

use GuzzleHttp\Client as GuzzleClient;
use GuzzleHttp\RequestOptions;
use PHPUnit\Framework\TestCase;
use Revaly\Sdk\RapClient;
use Revaly\Sdk\Testing\RapMockTransport;

/**
 * ADR-SDK-027 deadline-default semantics: an omitted overallDeadline resolves to the
 * 30-second ratified default, an explicit null opts out entirely, explicit values pass
 * through, and zero/negative values are rejected at construction.
 */
final class DeadlineDefaultTest extends TestCase
{
    /** Reads the TIMEOUT the client actually configured on its Guzzle wire. */
    private static function wiredTimeout(RapClient $client): mixed
    {
        $prop = new \ReflectionProperty(RapClient::class, 'guzzle');
        $prop->setAccessible(true);
        /** @var GuzzleClient $guzzle */
        $guzzle = $prop->getValue($client);

        return $guzzle->getConfig(RequestOptions::TIMEOUT);
    }

    public function testOmittedResolvesToTheRatified30sDefault(): void
    {
        self::assertSame(30.0, RapClient::DEFAULT_OVERALL_DEADLINE_SECONDS);

        $client = new RapClient(apiKey: 'sk-synthetic-test', transport: new RapMockTransport());

        self::assertSame(30.0, self::wiredTimeout($client));
    }

    public function testExplicitNullOptsOutOfAnySdkDeadline(): void
    {
        $client = new RapClient(
            apiKey: 'sk-synthetic-test',
            overallDeadline: null,
            transport: new RapMockTransport(),
        );

        // 0 is Guzzle's "no timeout" — the pre-ADR-027 unset behaviour.
        self::assertSame(0, self::wiredTimeout($client));
    }

    public function testExplicitValuesPassThroughUnchanged(): void
    {
        $client = new RapClient(
            apiKey: 'sk-synthetic-test',
            overallDeadline: 5.0,
            transport: new RapMockTransport(),
        );

        self::assertSame(5.0, self::wiredTimeout($client));
    }

    public function testZeroDeadlineIsRejected(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        new RapClient(apiKey: 'sk-synthetic-test', overallDeadline: 0.0);
    }

    public function testNegativeDeadlineIsRejected(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        new RapClient(apiKey: 'sk-synthetic-test', overallDeadline: -5.0);
    }
}
