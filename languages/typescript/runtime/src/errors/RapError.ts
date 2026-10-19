/**
 * The three failure classes of failover-contract.md §2. The class — never the message
 * text, never latency — is what licenses (or forbids) failover. Values match the other
 * language runtimes' class tokens so cross-language log lines join cleanly.
 */
export type RapFailureClass = 'PermanentRejection' | 'TransientFailure' | 'OutcomeUnknown';

export interface RapErrorOptions {
    /** HTTP status of the classified response, when one was received. */
    status?: number;
    /** The `ErrorResponse.code` safety signal, VERBATIM off the wire (an open string — OQ-2 adds values later). */
    code?: string;
    /** The server's human-readable `error` message. Never used for classification. */
    apiError?: string;
    /**
     * The server's `details` field — opaque by contract. The runtime reads exactly one key
     * of it, `edgeRejection` on a 403 (ADR-SDK-033, surfaced as `isEdgeRejection` /
     * `edgeReference`), and never inspects the rest.
     */
    details?: unknown;
    /** `X-Correlation-ID` of the response; joins merchant tickets to RAP-core telemetry. */
    correlationId?: string;
    /** The raw response body the classification was read from. */
    rawBody?: string;
    /** The underlying transport failure, when there is one. */
    cause?: unknown;
    /**
     * True when the production edge firewall blocked this request before it reached the
     * platform: an HTTP 403 whose body carries `details.edgeRejection: true` (ADR-SDK-033).
     */
    isEdgeRejection?: boolean;
    /** The edge firewall's tracking reference (`details.reference`, equal to the `x-azure-ref` header). */
    edgeReference?: string;
}

/**
 * Base class of the three typed failure classes (runtime-tdd §3). Every instance
 * carries the class discriminant (`kind`), HTTP status (if any), the verbatim open
 * `code` (if any), the server's human message, opaque `details`, the correlation id,
 * and the raw response body. The merchant API key can never appear in `message` — no
 * constructor on this hierarchy ever receives it (ADR-SDK-020).
 */
export abstract class RapError extends Error {
    /** The failure class driving the caller's failover decision. */
    abstract readonly kind: RapFailureClass;

    readonly status?: number;
    readonly code?: string;
    readonly apiError?: string;
    readonly details?: unknown;
    readonly correlationId?: string;
    readonly rawBody?: string;
    /**
     * True when the production edge firewall blocked this request before it reached the
     * platform: an HTTP 403 whose body carries `details.edgeRejection: true` (ADR-SDK-033).
     * Such a failure is a `RapTransientFailure` — the payment was definitively not
     * processed. Charge and authorize: fail over, or fix the request content and retry;
     * capture, void, refund and refund-cancel: retry the same request.
     */
    readonly isEdgeRejection: boolean;
    /**
     * The edge firewall's tracking reference (`details.reference`, equal to the
     * `x-azure-ref` response header) when `isEdgeRejection` is true; otherwise undefined.
     * Quote it to support — it identifies the exact firewall decision.
     */
    readonly edgeReference?: string;

    constructor(message: string, options: RapErrorOptions = {}) {
        super(message, options.cause !== undefined ? { cause: options.cause } : undefined);
        this.status = options.status;
        this.code = options.code;
        this.apiError = options.apiError;
        this.details = options.details;
        this.correlationId = options.correlationId;
        this.rawBody = options.rawBody;
        this.isEdgeRejection = options.isEdgeRejection === true;
        if (this.isEdgeRejection && options.edgeReference !== undefined) {
            this.edgeReference = options.edgeReference;
        }
        // Restore the prototype chain for environments that transpile class extends.
        Object.setPrototypeOf(this, new.target.prototype);
    }
}

/**
 * Received and rejected (HTTP 400/401/404/422, or a 403 without the edge-rejection
 * marker). Fix or decline. **Never fail over** — the same request fails anywhere.
 */
export class RapPermanentRejection extends RapError {
    override readonly name: string = 'RapPermanentRejection';
    readonly kind = 'PermanentRejection';
}

/**
 * Definitively not processed (client-provable never-sent, 503 with
 * `code: not_processed`, or a 403 blocked at the edge firewall — `isEdgeRejection`,
 * ADR-SDK-033). Safe to route to your own gateway immediately.
 */
export class RapTransientFailure extends RapError {
    override readonly name: string = 'RapTransientFailure';
    readonly kind = 'TransientFailure';
}

/**
 * May have been processed (deadline after send, reset mid-flight, 5xx without the
 * `not_processed` proof). **Reconcile before acting** — failing over blind can
 * double-charge (failover-contract §3).
 */
export class RapOutcomeUnknown extends RapError {
    override readonly name: string = 'RapOutcomeUnknown';
    readonly kind = 'OutcomeUnknown';
}
