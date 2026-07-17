/**
 * Header names and auth scheme used across the runtime. The RAP auth scheme is
 * `Authorization: ApiKey <key>` — the `ApiKey` prefix is mandatory (it is NOT a
 * Bearer scheme).
 */
export const AUTHORIZATION = 'Authorization';

/** The mandatory RAP auth scheme token: `Authorization: ApiKey <key>`. */
export const AUTH_SCHEME = 'ApiKey';

export const USER_AGENT = 'User-Agent';

/** Contract-version pin, sent on every request (runtime-tdd §1). */
export const API_VERSION = 'X-Api-Version';

/** Echoed on every response; joins merchant tickets to RAP-core telemetry. */
export const CORRELATION_ID = 'X-Correlation-ID';
