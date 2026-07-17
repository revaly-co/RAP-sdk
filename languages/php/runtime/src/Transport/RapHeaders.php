<?php

declare(strict_types=1);

namespace Revaly\Sdk\Transport;

/**
 * Header names and auth scheme used across the runtime. The RAP auth scheme is
 * `Authorization: ApiKey <key>` — the `ApiKey` prefix is mandatory (it is NOT a
 * Bearer scheme).
 */
final class RapHeaders
{
    public const AUTHORIZATION = 'Authorization';

    /** The mandatory RAP auth scheme token: `Authorization: ApiKey <key>`. */
    public const AUTH_SCHEME = 'ApiKey';

    public const USER_AGENT = 'User-Agent';

    /** Contract-version pin, sent on every request (runtime-tdd §1). */
    public const API_VERSION = 'X-Api-Version';

    /** Echoed on every response; joins merchant tickets to RAP-core telemetry. */
    public const CORRELATION_ID = 'X-Correlation-ID';
}
