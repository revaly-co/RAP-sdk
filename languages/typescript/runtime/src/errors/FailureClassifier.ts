import { RapError, RapOutcomeUnknown, RapPermanentRejection, RapTransientFailure } from './RapError';

/**
 * The normative failure-classification algorithm of failover-contract.md §2. Every rule
 * here is contract, not heuristic:
 *
 *     if transport error and request provably never sent          → TransientFailure
 *     if HTTP status in {400, 401, 403, 404, 422}                 → PermanentRejection
 *     if HTTP status == 503 and body.code == "not_processed"      → TransientFailure
 *     if HTTP status >= 500                                        → OutcomeUnknown
 *     if deadline exceeded after send / reset / ambiguous          → OutcomeUnknown
 *
 * Never classify from `error` message text; treat `details` as opaque; unrecognized
 * `code` values are treated as absent; when the stack cannot prove the request was
 * never sent, classify OutcomeUnknown — never guess toward "safe".
 *
 * `code` is read from the RAW body as an OPEN string — deliberately never through the
 * generated core's ErrorResponse model (repo rule 5): new values arrive with OQ-2 and
 * must never break classification. (The typescript-fetch core happens to pass unknown
 * wire values through verbatim, but classification never depends on that.)
 */

/** The provable-non-dispatch safety signal (platform P-1, ADR-SDK-007). */
export const NOT_PROCESSED = 'not_processed';

const PERMANENT_REJECTION_STATUSES = new Set([400, 401, 403, 404, 422]);

/**
 * Error codes that prove the request was never sent, read as STRUCTURED `code` values
 * from the fetch rejection's cause chain (Node's fetch rejects with
 * `TypeError('fetch failed')` whose `cause` is the undici/system error) — never parsed
 * out of message text. All of these fail before any HTTP bytes leave the client: name
 * resolution, TCP connection establishment, or the TLS handshake.
 *
 * Unlike curl (whose errno 28 covers both phases, forcing the PHP runtime to classify
 * every timeout OutcomeUnknown), undici types its connect-phase timeout distinctly
 * (`UND_ERR_CONNECT_TIMEOUT`), so it carries never-sent proof — same stance as the Java
 * runtime's HttpConnectTimeoutException.
 */
const NEVER_SENT_CAUSE_CODES = new Set([
    // Name resolution
    'ENOTFOUND',
    'EAI_AGAIN',
    // TCP connection establishment
    'ECONNREFUSED',
    'EHOSTUNREACH',
    'ENETUNREACH',
    'EADDRNOTAVAIL',
    // undici connect-phase timeout (distinct from headers/body timeouts)
    'UND_ERR_CONNECT_TIMEOUT',
    // TLS handshake: certificate verification (OpenSSL verify codes on cause.code)
    'CERT_HAS_EXPIRED',
    'CERT_NOT_YET_VALID',
    'CERT_UNTRUSTED',
    'CERT_SIGNATURE_FAILURE',
    'DEPTH_ZERO_SELF_SIGNED_CERT',
    'SELF_SIGNED_CERT_IN_CHAIN',
    'UNABLE_TO_VERIFY_LEAF_SIGNATURE',
    'UNABLE_TO_GET_ISSUER_CERT',
    'UNABLE_TO_GET_ISSUER_CERT_LOCALLY',
    'HOSTNAME_MISMATCH',
    // TLS handshake: protocol failures (Node error codes)
    'ERR_TLS_CERT_ALTNAME_INVALID',
    'ERR_TLS_HANDSHAKE_TIMEOUT',
    'ERR_TLS_INVALID_PROTOCOL_VERSION',
    'ERR_SSL_WRONG_VERSION_NUMBER',
]);

/** The `code`/`error`/`details` triple read from a raw error body (open strings off the wire). */
export interface ParsedErrorBody {
    code?: string;
    error?: string;
    details?: unknown;
}

/**
 * Classifies a received non-success HTTP response. Statuses outside the §2 table
 * (e.g. 409, 3xx) are ambiguous and classify as OutcomeUnknown — reconcile reveals the
 * true state.
 *
 * `apiVersion` is the pinned X-Api-Version. On "2.0" the `ErrorResponse.code` field is
 * not part of the documented contract, so the fast-failover class narrows to
 * client-provable never-sent failures only: 503 + `not_processed` is NOT honored and
 * falls through to OutcomeUnknown (runtime-tdd §1 [Decided]).
 */
export function classifyResponse(
    status: number,
    rawBody: string | undefined,
    apiVersion: string,
    correlationId: string | undefined,
): RapError {
    const { code, error, details } = parseErrorBody(rawBody);

    if (PERMANENT_REJECTION_STATUSES.has(status)) {
        return new RapPermanentRejection(`[${status}] permanent rejection: ${error ?? 'request rejected'}`, {
            status,
            code,
            apiError: error,
            details,
            correlationId,
            rawBody,
        });
    }

    if (status === 503 && code === NOT_PROCESSED && apiVersion !== '2.0') {
        return new RapTransientFailure('[503] not processed — provably never dispatched; safe to fail over', {
            status,
            code,
            apiError: error,
            details,
            correlationId,
            rawBody,
        });
    }

    return new RapOutcomeUnknown(`[${status}] outcome unknown; reconcile before acting`, {
        status,
        code,
        apiError: error,
        details,
        correlationId,
        rawBody,
    });
}

/**
 * Classifies a transport-level failure (no HTTP response was received). Never-sent
 * proof uses the STRUCTURED `code` values on the rejection's cause chain; a rejection
 * without a recognized code carries no proof and classifies OutcomeUnknown.
 * Already-typed failures pass through unchanged. Abort/deadline attribution is the
 * transport's job (it owns the signals) — by the time a rejection reaches here, it is
 * neither a caller cancellation nor this runtime's deadline.
 */
export function classifyTransportRejection(reason: unknown): RapError {
    if (reason instanceof RapError) {
        return reason;
    }

    const neverSentCode = collectCauseCodes(reason).find((code) => NEVER_SENT_CAUSE_CODES.has(code));
    if (neverSentCode !== undefined) {
        return new RapTransientFailure(`request provably never sent (${neverSentCode})`, { cause: reason });
    }

    return new RapOutcomeUnknown(
        `transport failure without never-sent proof (${shortName(reason)}); reconcile before acting`,
        { cause: reason },
    );
}

/**
 * Reads `code`, `error`, and `details` from the raw error body. `code` is an OPEN
 * string straight off the wire. Anything unparseable is treated as absent (→ the
 * conservative branch).
 */
export function parseErrorBody(rawBody: string | undefined): ParsedErrorBody {
    if (rawBody === undefined || rawBody.trim() === '') {
        return {};
    }

    let root: unknown;
    try {
        root = JSON.parse(rawBody);
    } catch {
        return {};
    }
    if (typeof root !== 'object' || root === null || Array.isArray(root)) {
        return {};
    }

    const record = root as Record<string, unknown>;
    return {
        code: typeof record['code'] === 'string' ? record['code'] : undefined,
        error: typeof record['error'] === 'string' ? record['error'] : undefined,
        details: record['details'],
    };
}

/**
 * The structured `code` values along a rejection's cause chain. Node's fetch nests the
 * real failure (`TypeError('fetch failed')` → undici error → system error), and
 * happy-eyeballs connect failures arrive as an `AggregateError` of per-address
 * failures — every node is walked, depth-capped against cause cycles.
 */
function collectCauseCodes(reason: unknown, depth = 0): string[] {
    if (depth > 8 || typeof reason !== 'object' || reason === null) {
        return [];
    }

    const codes: string[] = [];
    const code = (reason as { code?: unknown }).code;
    if (typeof code === 'string' && code !== '') {
        codes.push(code);
    }
    if (reason instanceof AggregateError) {
        for (const inner of reason.errors) {
            codes.push(...collectCauseCodes(inner, depth + 1));
        }
    }
    codes.push(...collectCauseCodes((reason as { cause?: unknown }).cause, depth + 1));

    return codes;
}

function shortName(reason: unknown): string {
    if (reason instanceof Error) {
        return reason.name;
    }
    return typeof reason;
}
