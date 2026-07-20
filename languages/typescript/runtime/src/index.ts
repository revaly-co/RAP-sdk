/**
 * revaly-sdk — the RAP TypeScript SDK (runtime-tdd §2: one package to import).
 *
 * The hand-written runtime surface (client, typed failure classes, reconcile helper,
 * scrubbed logging, mock transport) plus the full generated V2 core, re-exported so
 * every request/response model and generated api is reachable from this single entry.
 */

// Client
export {
    DEFAULT_OVERALL_DEADLINE_MS,
    RapClient,
    type RapCallOptions,
    type RapClientConfig,
} from './RapClient';

// Typed failure classes + classification (failover-contract §2)
export {
    RapError,
    RapOutcomeUnknown,
    RapPermanentRejection,
    RapTransientFailure,
    type RapErrorOptions,
    type RapFailureClass,
} from './errors/RapError';
export {
    classifyResponse,
    classifyTransportRejection,
    NOT_PROCESSED,
    parseErrorBody,
    type ParsedErrorBody,
} from './errors/FailureClassifier';
export { toRapResult, type RapResult } from './errors/RapResult';

// Reconcile (failover-contract §3)
export { RapReconciler, type ReconcileOptions } from './reconcile/RapReconciler';
export type { ReconcilePolicy } from './reconcile/ReconcilePolicy';
export type {
    Found,
    NotFoundYet,
    RapReconcileVerdict,
    RapTransactionOutcome,
    ReconcileVerdictExtension,
} from './reconcile/verdicts';

// Logging + scrubbing (runtime-tdd §6; ADR-SDK-020)
export type { RapLogger } from './logging/RapLogger';
export type { RapWireTrace, RapWireTraceHook } from './logging/RapWireTrace';
export { REDACTED, SCRUBBED, scrubHeaders, scrubJson, scrubValue } from './logging/RapScrubber';

// Transport (runtime-tdd §5)
export {
    buildFetchApi,
    classificationMiddleware,
    type RapTransportLike,
    type RapTransportOptions,
} from './transport/RapTransport';
export * as RapHeaders from './transport/RapHeaders';
export { PRODUCT_NAME, userAgentValue } from './transport/RapUserAgent';
export { SDK_VERSION } from './version';

// Mock transport (DX contract §d; runtime-tdd §8)
export { MockOperation } from './testing/MockOperation';
export { RapMockTransport } from './testing/RapMockTransport';
export { RecordedRequest } from './testing/RecordedRequest';
export * as SyntheticData from './testing/SyntheticData';

// The generated core — full V2 surface through the same package (runtime-tdd §2)
export * from '../../core/index';
