import * as RapHeaders from '../transport/RapHeaders';

/**
 * The single central scrub function of this runtime (ADR-SDK-020): applied to debug
 * logs, wire traces, and any payload surface the SDK emits. Scrubbing is by ALLOWLIST —
 * only known-safe identifier/status fields are emitted verbatim; every other scalar is
 * replaced with `[scrubbed]`, so schema evolution fails safe. PAN/CVV/PII can never
 * appear because card and customer fields are simply not on the list. API keys are
 * additionally redacted at the header layer.
 */

/** The replacement token for scrubbed scalar values. */
export const SCRUBBED = '[scrubbed]';

/** The replacement token for redacted header values. */
export const REDACTED = '[redacted]';

/**
 * Known-safe fields: identifiers, statuses and routing metadata designed for support
 * tickets and telemetry joins. Deliberately absent: every cardholder, customer, address
 * and amount field. Extending this list is a reviewed change to the runtime's PCI
 * posture — never add payload value fields. (Lowercased for case-insensitive lookup.)
 */
const FIELD_ALLOWLIST = new Set([
    'transactionid',
    'merchanttransactionid',
    'transactiontype',
    'transactionstatus',
    'transactiondate',
    'responsecode',
    'code',
    'error',
    'currency',
    'gatewaytype',
    'gatewaytransactionid',
    'gatewayroutingid',
    'correlationid',
    'status',
    'state',
    'attempts',
]);

/**
 * Known-safe headers. Authorization is never emitted, even redacted-by-length — the
 * merchant API key must not leak shape or presence into logs (ADR-SDK-020).
 * (Lowercased for case-insensitive lookup.)
 */
const HEADER_ALLOWLIST = new Set([
    'content-type',
    'content-length',
    'user-agent',
    'x-api-version',
    'x-correlation-id',
    'api-supported-versions',
]);

/**
 * Scrubs a JSON payload string: allowlisted scalar fields pass through verbatim, all
 * other scalars are replaced with {@link SCRUBBED}; object/array structure is
 * preserved. Non-JSON input returns a fixed placeholder (never the raw text).
 */
export function scrubJson(payload: string | undefined | null): string {
    if (payload == null || payload.trim() === '') {
        return '';
    }

    let root: unknown;
    try {
        root = JSON.parse(payload);
    } catch {
        return '[unparseable:scrubbed]';
    }

    return JSON.stringify(scrubNode(root, false));
}

/**
 * Scrubs an already-parsed payload (the runtime's models are plain objects), returning
 * the scrubbed JSON string. Values that cannot serialize scrub to the fixed token.
 */
export function scrubValue(value: unknown): string {
    try {
        const encoded = JSON.stringify(value);
        return scrubJson(encoded);
    } catch {
        return SCRUBBED;
    }
}

/**
 * Scrubs an HTTP header set for tracing: allowlisted headers pass through, everything
 * else (including Authorization) becomes {@link REDACTED}. User-Agent is a
 * space-separated product-token list on the wire; other multi-valued headers join with
 * commas per RFC 9110.
 */
export function scrubHeaders(
    headers: Headers | Record<string, string | string[]> | undefined | null,
): Record<string, string> {
    const result: Record<string, string> = {};
    if (headers == null) {
        return result;
    }

    const entries: Array<[string, string]> =
        headers instanceof Headers
            ? [...headers.entries()]
            : Object.entries(headers).map(([name, values]): [string, string] => {
                  const list = Array.isArray(values) ? values : [values];
                  const separator = name.toLowerCase() === RapHeaders.USER_AGENT.toLowerCase() ? ' ' : ', ';
                  return [name, list.map(String).join(separator)];
              });

    for (const [name, value] of entries) {
        result[name] = HEADER_ALLOWLIST.has(name.toLowerCase()) ? value : REDACTED;
    }

    return Object.fromEntries(
        Object.entries(result).sort(([a], [b]) => a.toLowerCase().localeCompare(b.toLowerCase())),
    );
}

function scrubNode(node: unknown, parentKeyAllowlisted: boolean): unknown {
    if (Array.isArray(node)) {
        // Scalars inside arrays keep only their parent key's status.
        return node.map((element) =>
            typeof element === 'object' && element !== null
                ? scrubNode(element, parentKeyAllowlisted)
                : parentKeyAllowlisted
                  ? element
                  : SCRUBBED,
        );
    }

    if (typeof node === 'object' && node !== null) {
        const scrubbed: Record<string, unknown> = {};
        for (const [key, child] of Object.entries(node)) {
            const allowlisted = FIELD_ALLOWLIST.has(key.toLowerCase());
            if (typeof child === 'object' && child !== null) {
                scrubbed[key] = scrubNode(child, allowlisted);
            } else {
                scrubbed[key] = allowlisted ? child : SCRUBBED;
            }
        }
        return scrubbed;
    }

    // Bare scalar root.
    return parentKeyAllowlisted ? node : SCRUBBED;
}
