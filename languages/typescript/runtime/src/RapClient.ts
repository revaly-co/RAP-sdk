import type { ApiResponse } from '../../core/runtime';
import { Configuration } from '../../core/runtime';
import { NotifyApi, PaymentMethodsApi, PaymentsApi, TransactionsApi } from '../../core/apis/index';
import type {
    AuthorizeRequest,
    CaptureRequest,
    PaymentRequest,
    RefundCancelRequest,
    RefundRequest,
    TransactionResponse,
    VoidRequest,
} from '../../core/models/index';
import { RapError } from './errors/RapError';
import { loggerOrSilent, type RapLogger } from './logging/RapLogger';
import { scrubValue } from './logging/RapScrubber';
import type { RapWireTraceHook } from './logging/RapWireTrace';
import { RapReconciler, type ReconcileOptions } from './reconcile/RapReconciler';
import type { ReconcilePolicy } from './reconcile/ReconcilePolicy';
import type { RapReconcileVerdict } from './reconcile/verdicts';
import { CORRELATION_ID } from './transport/RapHeaders';
import { buildFetchApi, classificationMiddleware, type RapTransportLike } from './transport/RapTransport';
import { userAgentValue } from './transport/RapUserAgent';

export interface RapClientConfig {
    /**
     * The merchant API key (required). Sent as `Authorization: ApiKey <key>` on every
     * request; never persisted, never logged, never present in error messages
     * (ADR-SDK-020). The key also selects the environment: sandbox and live are
     * key-scoped, not URL-scoped (ADR-SDK-024).
     */
    readonly apiKey: string;
    /**
     * The API base URL. Defaults to `https://api.revaly.co` — sandbox and live share
     * this URL; the environment is selected by your API key's scope, not the URL.
     * Override only for internal/pre-release targets.
     */
    readonly baseUrl?: string;
    /**
     * The API contract version, pinned via `X-Api-Version` on every request. Default
     * "2.1"; "2.0" is selectable. Behavioural difference on "2.0": the
     * `ErrorResponse.code` field is not part of the 2.0 documented contract, so the
     * fast-failover class narrows to client-provable never-sent failures only — a 503
     * with `code: not_processed` classifies as OutcomeUnknown (reconcile) instead of
     * TransientFailure (immediate failover). Pin 2.1 unless you have a frozen 2.0
     * integration.
     */
    readonly apiVersion?: string;
    /**
     * Overall per-request deadline in milliseconds. Expiry after the request was sent
     * classifies as OutcomeUnknown (reconcile before acting) — never TransientFailure.
     * Default: {@link DEFAULT_OVERALL_DEADLINE_MS} (30 seconds, ratified from
     * production latency telemetry — ADR-SDK-027; it clips ~1 in 9,500 charges at the
     * platform's observed tail). Pass `null` to disable the SDK deadline and ride the
     * platform's own behaviour.
     *
     * There is no `connectTimeout` option: WHATWG fetch cannot bound the connect phase
     * per request. On Node the platform's own connect timeout applies (undici, default
     * 10s), is reported structurally, and classifies TransientFailure (provably never
     * sent); to tune it, pass a `dispatcher` (see the README's Agent recipe). A
     * client-side connect default awaits the OQ-11 edge verification (ADR-SDK-027).
     */
    readonly overallDeadlineMs?: number | null;
    /**
     * Console-compatible logger (`console` itself works). Default output is
     * VALUES-FREE: operation, status, class, and correlation id only; debug level
     * carries allowlist-scrubbed payloads (ADR-SDK-020). Omit for silence.
     */
    readonly logger?: RapLogger;
    /**
     * Optional request/response observer for Enablement escalations. Receives payloads
     * already scrubbed by the runtime's central allowlist scrubber — never raw
     * material. Observer exceptions are swallowed.
     */
    readonly wireTraceHook?: RapWireTraceHook;
    /**
     * Replacement wire transport: a fetch-compatible function or the mock transport
     * ({@link RapMockTransport}) in merchant tests. Omit for the real HTTP transport.
     */
    readonly transport?: RapTransportLike;
    /**
     * Optional merchant product token APPENDED after the SDK's User-Agent token
     * (ADR-SDK-005: the SDK prefix stays first and intact; it can never be replaced or
     * suppressed).
     */
    readonly userAgentSuffix?: string;
    /**
     * Optional undici dispatcher (Node only), passed through to fetch — the idiomatic
     * place to tune connection pooling and the connect-phase timeout (README recipe).
     */
    readonly dispatcher?: unknown;
}

/** Per-call options for the payment operations and reconcile. */
export interface RapCallOptions {
    /** Cancels the call. Cancellation rethrows the abort reason — it is not a payment outcome. */
    readonly signal?: AbortSignal;
}

/**
 * The overall-deadline default applied when `overallDeadlineMs` is omitted: 30 seconds,
 * ratified from production latency telemetry (ADR-SDK-027). Pass `overallDeadlineMs:
 * null` to disable the SDK deadline entirely.
 */
export const DEFAULT_OVERALL_DEADLINE_MS = 30_000;

/**
 * Resolves the configured overall deadline: omitted (`undefined`) → the ratified
 * default; `null` → disabled; a positive number → itself.
 */
export function resolveOverallDeadlineMs(
    configured: number | null | undefined,
): number | undefined {
    if (configured === null) {
        return undefined;
    }
    return configured ?? DEFAULT_OVERALL_DEADLINE_MS;
}

/**
 * The RAP TypeScript SDK client (runtime-tdd §§1-2): one client object per
 * configuration — create it once and reuse it (no global singletons).
 *
 * Payment operations return the core's {@link TransactionResponse} on success and
 * reject with exactly one of the three typed failure classes on failure
 * (docs/failover-contract.md §2):
 *
 * - {@link RapPermanentRejection} — fix or decline; never fail over.
 * - {@link RapTransientFailure} — definitively not processed; safe to fail over
 *   immediately.
 * - {@link RapOutcomeUnknown} — may have been processed; {@link reconcile} before
 *   acting.
 *
 * Prefer `try/catch` with `instanceof`, or fold into the discriminated-union result
 * with {@link toRapResult}. The full generated V2 surface stays available through
 * {@link payments}, {@link transactions}, {@link paymentMethods} and {@link notify} —
 * every request they make flows through the same transport, headers and
 * classification, so they reject with the same three classes. One dependency, one
 * package to import.
 */
export class RapClient {
    /** The generated payments api, sharing this client's transport and headers. */
    readonly payments: PaymentsApi;
    /** The generated transactions api, sharing this client's transport and headers. */
    readonly transactions: TransactionsApi;
    /** The generated payment-methods api, sharing this client's transport and headers. */
    readonly paymentMethods: PaymentMethodsApi;
    /** The generated notify api, sharing this client's transport and headers. */
    readonly notify: NotifyApi;

    private readonly logger;
    private readonly wireTraceHook: RapWireTraceHook | undefined;
    private readonly emitPayloadTraces: boolean;
    private readonly reconciler: RapReconciler;

    constructor(config: RapClientConfig) {
        if (config.apiKey === undefined || config.apiKey.trim() === '') {
            throw new TypeError('apiKey is required');
        }
        const baseUrl = (config.baseUrl ?? 'https://api.revaly.co').replace(/\/+$/, '');
        if (baseUrl === '') {
            throw new TypeError('baseUrl is required');
        }
        const apiVersion = config.apiVersion ?? '2.1';
        if (apiVersion.trim() === '') {
            throw new TypeError('apiVersion is required');
        }
        if (
            config.overallDeadlineMs !== undefined &&
            config.overallDeadlineMs !== null &&
            !(config.overallDeadlineMs > 0)
        ) {
            throw new TypeError(
                'overallDeadlineMs must be positive when set (null disables the SDK deadline)',
            );
        }

        this.logger = loggerOrSilent(config.logger);
        this.wireTraceHook = config.wireTraceHook;
        this.emitPayloadTraces = config.wireTraceHook !== undefined || config.logger?.debug !== undefined;

        // The core Configuration deliberately never receives the API key — the
        // fetchApi wrapper is the single injection point (ADR-SDK-020), where the core
        // cannot bypass it (ADR-SDK-005); the classification middleware types every
        // HTTP failure from the raw body before any core code sees it.
        const coreConfig = new Configuration({
            basePath: baseUrl,
            fetchApi: buildFetchApi({
                apiKey: config.apiKey,
                apiVersion,
                userAgent: userAgentValue(config.userAgentSuffix),
                overallDeadlineMs: resolveOverallDeadlineMs(config.overallDeadlineMs),
                transport: config.transport,
                dispatcher: config.dispatcher,
            }),
            middleware: [classificationMiddleware(apiVersion)],
        });

        this.payments = new PaymentsApi(coreConfig);
        this.transactions = new TransactionsApi(coreConfig);
        this.paymentMethods = new PaymentMethodsApi(coreConfig);
        this.notify = new NotifyApi(coreConfig);
        this.reconciler = new RapReconciler(this.transactions, this.logger, this.wireTraceHook);
    }

    /** Charges a payment (`POST /payments`). */
    charge(request: PaymentRequest, options: RapCallOptions = {}): Promise<TransactionResponse> {
        return this.execute('charge', 'POST', '/payments', request, () =>
            this.payments.chargePaymentRaw({ paymentRequest: request }, { signal: options.signal ?? null }),
        );
    }

    /** Authorizes a payment for later capture (`POST /payments/authorize`). */
    authorize(request: AuthorizeRequest, options: RapCallOptions = {}): Promise<TransactionResponse> {
        return this.execute('authorize', 'POST', '/payments/authorize', request, () =>
            this.payments.authorizePaymentRaw({ authorizeRequest: request }, { signal: options.signal ?? null }),
        );
    }

    /** Captures a previously authorized payment. */
    capture(
        transactionId: string,
        request: CaptureRequest,
        options: RapCallOptions = {},
    ): Promise<TransactionResponse> {
        return this.execute('capture', 'POST', '/payments/capture/{transactionId}', request, () =>
            this.payments.capturePaymentRaw(
                { transactionId, captureRequest: request },
                { signal: options.signal ?? null },
            ),
        );
    }

    /** Voids a previously authorized payment. */
    voidPayment(
        transactionId: string,
        request: VoidRequest,
        options: RapCallOptions = {},
    ): Promise<TransactionResponse> {
        return this.execute('void', 'POST', '/payments/void/{transactionId}', request, () =>
            this.payments.voidPaymentRaw({ transactionId, voidRequest: request }, { signal: options.signal ?? null }),
        );
    }

    /** Refunds a settled payment. */
    refund(
        transactionId: string,
        request: RefundRequest,
        options: RapCallOptions = {},
    ): Promise<TransactionResponse> {
        return this.execute('refund', 'POST', '/payments/refund/{transactionId}', request, () =>
            this.payments.refundPaymentRaw(
                { transactionId, refundRequest: request },
                { signal: options.signal ?? null },
            ),
        );
    }

    /** Cancels a refund by merchant transaction id. */
    refundCancel(
        merchantTransactionId: string,
        request: RefundCancelRequest,
        options: RapCallOptions = {},
    ): Promise<TransactionResponse> {
        return this.execute(
            'refundCancel',
            'POST',
            '/payments/refund-cancel/merchant/{merchantTransactionId}',
            request,
            () =>
                this.payments.refundCancelPaymentByMerchantTransactionIdRaw(
                    { merchantTransactionId, refundCancelRequest: request },
                    { signal: options.signal ?? null },
                ),
        );
    }

    /**
     * The OutcomeUnknown reconciliation procedure (failover-contract §3): polls the
     * merchant-transaction lookup within the caller-bounded {@link ReconcilePolicy}
     * and returns a {@link RapReconcileVerdict}. ALWAYS branch with a default —
     * verdicts are open for extension (SafeToFailover arrives with platform P-2 as a
     * minor release).
     */
    reconcile(
        merchantTransactionId: string,
        policy: ReconcilePolicy,
        options: ReconcileOptions = {},
    ): Promise<RapReconcileVerdict> {
        return this.reconciler.reconcile(merchantTransactionId, policy, options);
    }

    private async execute(
        operation: string,
        method: string,
        path: string,
        requestModel: unknown,
        call: () => Promise<ApiResponse<TransactionResponse>>,
    ): Promise<TransactionResponse> {
        try {
            const apiResponse = await call();
            const status = apiResponse.raw.status;
            const correlationId = apiResponse.raw.headers.get(CORRELATION_ID) ?? undefined;
            this.logger.info('rap.request', { operation, status, correlation: correlationId });
            if (this.emitPayloadTraces) {
                const responseValue = await apiResponse.raw
                    .clone()
                    .json()
                    .catch(() => undefined);
                this.trace(operation, method, path, status, correlationId, requestModel, responseValue);
            }
            return await apiResponse.value();
        } catch (failure) {
            if (failure instanceof RapError) {
                this.logger.warn('rap.request failed', {
                    operation,
                    class: failure.kind,
                    status: failure.status,
                    code: failure.code,
                    correlation: failure.correlationId,
                });
                if (this.emitPayloadTraces) {
                    this.trace(
                        operation,
                        method,
                        path,
                        failure.status,
                        failure.correlationId,
                        requestModel,
                        undefined,
                    );
                }
            }
            // Everything else (caller cancellation, request validation, programming
            // errors) is not a payment outcome and rethrows untyped.
            throw failure;
        }
    }

    private trace(
        operation: string,
        method: string,
        path: string,
        status: number | undefined,
        correlationId: string | undefined,
        requestModel: unknown,
        responseValue: unknown,
    ): void {
        const scrubbedRequestBody = requestModel === undefined ? undefined : scrubValue(requestModel);
        const scrubbedResponseBody = responseValue === undefined ? undefined : scrubValue(responseValue);

        // Debug level carries allowlist-scrubbed payloads only (ADR-SDK-020).
        this.logger.debug('rap.request payload', {
            operation,
            request: scrubbedRequestBody,
            response: scrubbedResponseBody,
        });

        if (this.wireTraceHook !== undefined) {
            try {
                this.wireTraceHook({
                    operation,
                    method,
                    path,
                    status,
                    correlationId,
                    scrubbedRequestBody,
                    scrubbedResponseBody,
                });
            } catch (hookFailure) {
                // Observer exceptions are swallowed (runtime-tdd §6).
                this.logger.debug('rap.wiretrace hook threw; ignored', {
                    exception: hookFailure instanceof Error ? hookFailure.name : typeof hookFailure,
                });
            }
        }
    }
}
