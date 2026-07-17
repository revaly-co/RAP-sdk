<?php

declare(strict_types=1);

namespace Revaly\Sdk\Transport;

/**
 * Builds the adoption-telemetry User-Agent per the ADR-SDK-005 normative grammar:
 * `revaly-sdk-php/<semver> (php <major.minor>; <os>)`. The exact string is a contract
 * with platform dashboards; it carries only the coarse tokens below — no hostnames, no
 * distro fingerprints. A merchant token may be APPENDED after the SDK token
 * (`userAgentSuffix`); the SDK prefix stays first and intact — it can never be replaced
 * or suppressed (enforced at transport level, where the core cannot bypass it).
 */
final class RapUserAgent
{
    /** The fixed lowercase language token (ADR-SDK-005 grammar). */
    public const PRODUCT_NAME = 'revaly-sdk-php';

    /**
     * The package semver, no `v` prefix. Stage 5 stamps release versions at packaging
     * time; development and test runs carry the placeholder.
     */
    public const SEMVER = '0.0.0';

    private function __construct()
    {
    }

    /** The full header value, e.g. `revaly-sdk-php/1.2.0 (php 8.3; linux)`. */
    public static function value(?string $merchantSuffix = null): string
    {
        $value = sprintf(
            '%s/%s (php %d.%d; %s)',
            self::PRODUCT_NAME,
            self::SEMVER,
            PHP_MAJOR_VERSION,
            PHP_MINOR_VERSION,
            self::os()
        );

        if ($merchantSuffix !== null && trim($merchantSuffix) !== '') {
            $value .= ' ' . trim($merchantSuffix);
        }

        return $value;
    }

    /** Coarse platform token: `linux` / `windows` / `darwin` / `other`. */
    public static function os(): string
    {
        return match (PHP_OS_FAMILY) {
            'Windows' => 'windows',
            'Linux' => 'linux',
            'Darwin' => 'darwin',
            default => 'other',
        };
    }
}
