/**
 * One observed request/response pair for the wire-trace hook (runtime-tdd §6; DX
 * contract §c). Payloads and headers arrive ALREADY scrubbed by the runtime's central
 * allowlist scrubber — never raw material — so the hook can be pointed at any sink
 * during an Enablement escalation.
 */
export interface RapWireTrace {
    readonly operation: string;
    readonly method: string;
    readonly path: string;
    readonly status?: number;
    readonly correlationId?: string;
    /** Scrubbed request headers (Authorization is always redacted). */
    readonly requestHeaders?: Record<string, string>;
    readonly scrubbedRequestBody?: string;
    /** Scrubbed response headers. */
    readonly responseHeaders?: Record<string, string>;
    readonly scrubbedResponseBody?: string;
}

/** The wire-trace observer contract. Observer exceptions are swallowed by the runtime. */
export type RapWireTraceHook = (trace: RapWireTrace) => void;
