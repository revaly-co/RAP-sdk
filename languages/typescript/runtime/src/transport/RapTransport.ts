import type { FetchAPI, Middleware } from '../../../core/runtime';
import { classifyResponse, classifyTransportRejection } from '../errors/FailureClassifier';
import { RapOutcomeUnknown } from '../errors/RapError';
import { API_VERSION, AUTHORIZATION, AUTH_SCHEME, CORRELATION_ID, USER_AGENT } from './RapHeaders';

/**
 * The wire transport surface. The runtime's `fetchApi` wrapper is the single injection
 * point for auth, User-Agent and the version pin — it sits below the generated core, so
 * the core cannot bypass it (runtime-tdd §5) — and the single place transport
 * rejections are typed. HTTP-status classification lives in the companion middleware,
 * which reads the raw body (repo rule 5).
 */

/** A replacement wire transport: a fetch-compatible function, or an object exposing one (the mock transport). */
export type RapTransportLike = FetchAPI | { fetch: FetchAPI };

/**
 * The minimal structural surface of an undici dispatcher (`Agent`, `ProxyAgent`,
 * `MockAgent`, …). Declared structurally so the public config never references undici
 * types and the SDK keeps zero runtime dependencies; any real undici `Dispatcher`
 * satisfies it (method-parameter bivariance makes the concrete option/handler types
 * assignable). The runtime never invokes it — the object is handed to `fetch`
 * verbatim.
 */
export interface RapDispatcherLike {
    dispatch(options: object, handler: object): boolean;
}

export interface RapTransportOptions {
    apiKey: string;
    apiVersion: string;
    userAgent: string;
    /**
     * Overall per-request deadline in milliseconds. Expiry after the request was sent
     * classifies as OutcomeUnknown — never TransientFailure.
     */
    overallDeadlineMs?: number;
    transport?: RapTransportLike;
    /**
     * Optional undici dispatcher (Node only), passed through to fetch. This is the
     * idiomatic place to tune connection behaviour — including the connect-phase
     * timeout, which WHATWG fetch itself cannot set per request (see the README's
     * `Agent` recipe). A connect-phase timeout is reported structurally
     * (`UND_ERR_CONNECT_TIMEOUT`) and classifies TransientFailure.
     */
    dispatcher?: RapDispatcherLike;
}

/**
 * Builds the runtime's `fetchApi` for the core Configuration:
 *
 * - injects `Authorization: ApiKey <key>` (REPLACES anything present — the core never
 *   holds the key, and a merchant-supplied header cannot override the scheme);
 * - injects the SDK User-Agent (ADR-SDK-005; merchant tokens are appended into the
 *   value at construction, never in front of it);
 * - pins `X-Api-Version` when absent (the core only sends it for explicit per-call
 *   overrides, and an absent header would silently bind the server default 2.0);
 * - never follows redirects — a followed 307/308 re-sends the payment body, a hidden
 *   resubmission; a 3xx response classifies OutcomeUnknown downstream;
 * - composes the caller's AbortSignal with the overall deadline;
 * - types every transport rejection per failover-contract §2: caller cancellations
 *   rethrow verbatim (not a payment outcome), deadline expiry is OutcomeUnknown (the
 *   request may already have been sent), everything else goes through the structured
 *   never-sent taxonomy.
 */
export function buildFetchApi(options: RapTransportOptions): FetchAPI {
    const baseFetch = resolveTransport(options.transport);

    return async (input: RequestInfo | URL, init: RequestInit = {}) => {
        const headers = new Headers(init.headers ?? undefined);
        headers.set(AUTHORIZATION, `${AUTH_SCHEME} ${options.apiKey}`);
        headers.set(USER_AGENT, options.userAgent);
        if (!headers.has(API_VERSION)) {
            headers.set(API_VERSION, options.apiVersion);
        }

        const callerSignal = init.signal ?? undefined;
        let deadlineSignal: AbortSignal | undefined;
        let signal = callerSignal;
        if (options.overallDeadlineMs !== undefined) {
            deadlineSignal = AbortSignal.timeout(options.overallDeadlineMs);
            signal = callerSignal ? AbortSignal.any([callerSignal, deadlineSignal]) : deadlineSignal;
        }

        const nextInit: RequestInit = { ...init, headers, redirect: 'manual', signal: signal ?? null };
        if (options.dispatcher !== undefined) {
            (nextInit as Record<string, unknown>).dispatcher = options.dispatcher;
        }

        try {
            return await baseFetch(input, nextInit);
        } catch (rejection) {
            if (callerSignal?.aborted) {
                // Caller cancellation is not a payment outcome — it rethrows verbatim.
                // If it happened after send, the outcome is unknown to the caller by
                // their own choice; reconcile applies (documented in the README).
                throw rejection;
            }
            if (deadlineSignal?.aborted) {
                throw new RapOutcomeUnknown(
                    'deadline exceeded; cannot prove the request was never sent — reconcile before acting',
                    { cause: rejection },
                );
            }
            throw classifyTransportRejection(rejection);
        }
    };
}

/**
 * The classification middleware for the core Configuration. `post` types every
 * non-success HTTP response from the RAW body per failover-contract §2 — so every
 * generated api method reachable through the client rejects with exactly one of the
 * three typed classes. `onError` rethrows transport rejections verbatim: they are
 * already typed by the fetchApi wrapper, and rethrowing from here propagates them
 * before the core can wrap them in its generic FetchError.
 */
export function classificationMiddleware(apiVersion: string): Middleware {
    return {
        onError: (context) => {
            // A synchronous rethrow: the core awaits this hook inside its own catch,
            // so the propagation is identical to an async rejection — verbatim, before
            // the core can wrap the rejection in its generic FetchError.
            throw context.error;
        },
        post: async ({ response }) => {
            const correlationId = response.headers.get(CORRELATION_ID) ?? undefined;

            if (!response.ok) {
                const rawBody = await response.clone().text();
                throw classifyResponse(response.status, rawBody, apiVersion, correlationId);
            }

            // Post-dispatch readability guard: the request WAS dispatched and a 2xx
            // arrived, but a body this SDK cannot parse makes the outcome unknowable
            // locally — reconcile resolves it from the raw record. Every RAP 2xx
            // carries a JSON body, so this reads the text regardless of content-type
            // (an intermediary that mangles the type has already mangled the wire).
            // The generated mappers themselves are throw-free — generator-bakeoff
            // §A3 — so JSON syntax is the only readability hazard downstream.
            if (response.status !== 204) {
                const rawBody = await response.clone().text();
                let readable = false;
                if (rawBody !== '') {
                    try {
                        JSON.parse(rawBody);
                        readable = true;
                    } catch {
                        readable = false;
                    }
                }
                if (!readable) {
                    throw new RapOutcomeUnknown(
                        'response received but unreadable by this SDK version; reconcile before acting',
                        { status: response.status, correlationId, rawBody },
                    );
                }
            }

            return undefined;
        },
    };
}

function resolveTransport(transport: RapTransportLike | undefined): FetchAPI {
    if (typeof transport === 'function') {
        return transport;
    }
    if (transport !== undefined) {
        return transport.fetch.bind(transport);
    }
    // Late-bound so a runtime-provided global fetch (or a test replacement) is honored,
    // and called on globalThis to avoid Illegal-invocation in browser environments.
    return (input, init) => globalThis.fetch(input, init);
}

