/**
 * Stage-4 contract smoke (ADR-SDK-024, pipeline stage 4): a thin, live
 * runtime-contract check of THIS SDK against the environment named by
 * RAP_SMOKE_BASE_URL / RAP_SMOKE_API_KEY (interim: Backbone staging; at GA:
 * the merchant sandbox key-scope). Its single purpose is proving the SDK's
 * classification against reality — it deliberately does not replicate
 * platform test coverage.
 *
 * Environment contract (same across all six languages):
 * RAP_SMOKE_BASE_URL (required), RAP_SMOKE_API_KEY (required),
 * RAP_SMOKE_GATEWAY_ROUTING_ID (optional — included in charge payloads when
 * set), RAP_SMOKE_FAULT_INJECT (optional — sent as the platform's
 * X-Backbone-Fault-Inject header to trigger the 503+not_processed row; the
 * scenario SKIPs when unset).
 *
 * Run with `npm run smoke` (vitest transforms the TS; scenarios execute
 * sequentially in declaration order). Output is values-free (ADR-SDK-020):
 * identifiers, statuses, classes and correlation ids only — never payload
 * values, never the key; unexpected non-SDK errors are reported by type name
 * only so transport error chains cannot leak endpoint details into CI logs.
 */
import { test } from 'vitest';
import {
    RapClient,
    RapError,
    RapPermanentRejection,
    RapTransientFailure,
    type RapReconcileVerdict,
    type RapTransactionOutcome,
    type RapWireTrace,
} from '../runtime/src/index';

// The platform's executor fault seam (Backbone ADR 014 test affordance):
// value "pre-dispatch" makes the charge fail between intent reservation and
// gateway dispatch — the only deterministic live trigger for the
// 503 + code=not_processed fast-failover row.
const FAULT_INJECT_HEADER = 'X-Backbone-Fault-Inject';
// One synthetic test PAN; the EXPIRY drives the outcome (staging-verified
// matrix 2026-07-18: 12/2027 approves, 12/2020 declines).
const TEST_PAN = '4111111111111111';

const baseUrl = process.env.RAP_SMOKE_BASE_URL;
const apiKey = process.env.RAP_SMOKE_API_KEY;
const routingId = process.env.RAP_SMOKE_GATEWAY_ROUTING_ID;
const faultValue = process.env.RAP_SMOKE_FAULT_INJECT;
if (!baseUrl || !apiKey) {
    throw new Error('smoke: RAP_SMOKE_BASE_URL and RAP_SMOKE_API_KEY must be set (ADR-SDK-024) — refusing to run.');
}

// One client per configuration, quickstart-shaped. The wire-trace hook is the
// designed observer for correlation ids on the success path (DX §c); events
// arrive already scrubbed by the runtime.
let lastTrace: RapWireTrace | undefined;
const client = new RapClient({
    apiKey,
    baseUrl,
    overallDeadlineMs: 15_000,
    wireTraceHook: (trace) => {
        lastTrace = trace;
    },
});

// A separately configured client whose key is a synthetic invalid value — the
// auth-rejection row.
const badKeyClient = new RapClient({
    apiKey: 'sk_smoke_synthetic_invalid',
    baseUrl,
    overallDeadlineMs: 15_000,
});

// A client whose transport stamps the platform's fault-inject header — every
// charge through it deterministically fails pre-dispatch
// (503 + code=not_processed). The transport seam sits INSIDE the runtime's
// own header injection, so auth/UA/version behaviour is unchanged.
const faultClient = faultValue
    ? new RapClient({
          apiKey,
          baseUrl,
          overallDeadlineMs: 15_000,
          transport: (input: RequestInfo | URL, init?: RequestInit) => {
              const headers = new Headers(init?.headers);
              headers.set(FAULT_INJECT_HEADER, faultValue);
              return fetch(input, { ...init, headers });
          },
      })
    : undefined;

/** Unique merchantTransactionId (≤ 100 chars) — every reconcile scenario uses a fresh one (ADR-SDK-024). */
function freshId(label: string): string {
    return `smoke-typescript-${label}-${Date.now()}-${Math.random().toString(16).slice(2, 10)}`;
}

/**
 * Charge request with the minimal live-approving field set (staging-verified
 * 2026-07-18): paymentMethodType + a cardholder name are SERVER-required
 * (business validation; the spec marks them optional — ADR-SDK-024), and
 * orderId + email are additionally required by the staging simulator for an
 * approval. Synthetic test cards only.
 */
function buildCharge(merchantTransactionId: string, pan: string, expiryYear: string) {
    return {
        amount: 1999,
        currency: 'USD',
        merchantTransactionId,
        orderId: merchantTransactionId,
        ...(routingId ? { gatewayRoutingId: routingId } : {}),
        paymentMethodType: 'creditCard' as const,
        paymentMethod: {
            fullName: 'Smoke Test',
            email: 'smoke@example.com',
            creditCard: {
                number: pan,
                cardVerificationCode: '123',
                expiryMonth: '12',
                expiryYear,
            },
        },
    };
}

/**
 * Runs a scenario body with values-free failure rendering: SDK typed classes
 * rethrow as-is (their messages carry status/code/correlation only); anything
 * else rethrows by type name so transport chains never reach CI logs.
 */
async function guard<T>(run: () => Promise<T>): Promise<T> {
    try {
        return await run();
    } catch (failure) {
        if (failure instanceof RapError || failure instanceof SmokeFailure) {
            throw failure;
        }
        throw new SmokeFailure(`unexpected ${failure?.constructor?.name ?? typeof failure}`);
    }
}

class SmokeFailure extends Error {}

/** Runs a charge expected to fail, returning the typed failure. */
async function expectFailure(run: () => Promise<unknown>, expectation: string): Promise<RapError> {
    try {
        await run();
    } catch (failure) {
        if (failure instanceof RapError) {
            return failure;
        }
        throw new SmokeFailure(`${expectation}, got unexpected ${failure?.constructor?.name ?? typeof failure}`);
    }
    throw new SmokeFailure(`server accepted the request — ${expectation}`);
}

/**
 * Asserts a Found verdict carrying the wanted outcome and a correlation id.
 * The verdict set is open — an unrecognized verdict is a real finding here,
 * not a pass.
 */
function expectFound(verdict: RapReconcileVerdict, want: RapTransactionOutcome): void {
    if (verdict.kind === 'found') {
        if (verdict.outcome !== want) {
            throw new SmokeFailure(`expected outcome ${want}, got ${verdict.outcome}`);
        }
        if (!verdict.correlationId) {
            throw new SmokeFailure('no X-Correlation-ID on the Found verdict (DX §c)');
        }
        return;
    }
    if (verdict.kind === 'notFoundYet') {
        throw new SmokeFailure(`charge not visible after ${verdict.attempts} attempts (${verdict.elapsedMs}ms) — expected Found`);
    }
    throw new SmokeFailure(`unrecognized verdict ${(verdict as { kind: string }).kind}`);
}

// Charged ids feed the reconcile scenarios: the verdicts — through the
// runtime's own outcome mapping — are the proof the charge outcomes were what
// the smoke claims.
const chargedId = freshId('charge');
const declinedId = freshId('decline');

test('charge-approved', () =>
    guard(async () => {
        const transaction = await client.charge(buildCharge(chargedId, TEST_PAN, '2027'));
        if (!transaction.transactionId) {
            throw new SmokeFailure('transactionId is empty on the success surface');
        }
        if (!lastTrace?.correlationId) {
            throw new SmokeFailure('no X-Correlation-ID observed on the success path (DX §c)');
        }
    }));

test('charge-declined', () =>
    guard(async () => {
        // An expired expiry declines deterministically (same PAN). A decline is a business
        // outcome on the SUCCESS surface — not a failure class;
        // reconcile-found-declined proves the mapping below.
        const transaction = await client.charge(buildCharge(declinedId, TEST_PAN, '2020'));
        if (!transaction.transactionId) {
            throw new SmokeFailure('transactionId is empty on the declined-charge surface');
        }
        if (!lastTrace?.correlationId) {
            throw new SmokeFailure('no X-Correlation-ID observed on the declined-charge path (DX §c)');
        }
    }));

test('charge-validation-rejected', () =>
    guard(async () => {
        // An empty card number passes every client-side model but fails the
        // server's required-field validation — the rejection is proven to come
        // from reality (HTTP 400; 4xx carries no code).
        const failure = await expectFailure(
            () => client.charge(buildCharge(freshId('validation'), '', '2027')),
            'expected RapPermanentRejection',
        );
        if (!(failure instanceof RapPermanentRejection)) {
            throw new SmokeFailure(`expected RapPermanentRejection, got ${failure.constructor.name}`);
        }
        if (failure.status !== 400 && failure.status !== 422) {
            throw new SmokeFailure(`expected HTTP 400/422, got ${failure.status}`);
        }
        if (!failure.correlationId) {
            throw new SmokeFailure('no X-Correlation-ID on the rejection (DX §c)');
        }
    }));

test('charge-auth-rejected', () =>
    guard(async () => {
        const failure = await expectFailure(
            () => badKeyClient.charge(buildCharge(freshId('auth'), TEST_PAN, '2027')),
            'expected RapPermanentRejection',
        );
        if (!(failure instanceof RapPermanentRejection)) {
            throw new SmokeFailure(`expected RapPermanentRejection, got ${failure.constructor.name}`);
        }
        if (failure.status !== 401 && failure.status !== 403) {
            throw new SmokeFailure(`expected HTTP 401/403, got ${failure.status}`);
        }
        if (!failure.correlationId) {
            throw new SmokeFailure('no X-Correlation-ID on the auth rejection (DX §c)');
        }
    }));

// The fast-failover row (503 + code=not_processed): valid input cannot reach
// it deterministically, so the platform's fault injector fails the charge
// pre-dispatch. RapTransientFailure is the ONLY acceptable class here — it is
// the row that licenses immediate failover. Skipped when the injector is
// unavailable (it is structurally inert outside staging/testing).
test.skipIf(!faultClient)('charge-not-processed-503', () =>
    guard(async () => {
        const failure = await expectFailure(
            () => faultClient!.charge(buildCharge(freshId('fault'), TEST_PAN, '2027')),
            'expected RapTransientFailure',
        );
        if (!(failure instanceof RapTransientFailure)) {
            throw new SmokeFailure(`expected RapTransientFailure, got ${failure.constructor.name}`);
        }
        if (failure.status !== 503) {
            throw new SmokeFailure(`expected HTTP 503, got ${failure.status}`);
        }
        if (failure.code !== 'not_processed') {
            throw new SmokeFailure(`expected code=not_processed, got "${failure.code}"`);
        }
        if (!failure.correlationId) {
            throw new SmokeFailure('no X-Correlation-ID on the not-processed failure (DX §c)');
        }
    }));

test('reconcile-found-approved', () =>
    guard(async () => {
        // Found(Approved) through the runtime's own outcome mapping is the
        // approval proof for the first charge; visibility is asynchronous,
        // hence the budget.
        const verdict = await client.reconcile(chargedId, {
            maxAttempts: 5,
            overallBudgetMs: 30_000,
            initialDelayMs: 1_000,
        });
        expectFound(verdict, 'Approved');
    }));

test('reconcile-found-declined', () =>
    guard(async () => {
        // The declined charge must reconcile as Found(Declined) — the outcome
        // branch that tells a merchant their own gateway is safe.
        const verdict = await client.reconcile(declinedId, {
            maxAttempts: 5,
            overallBudgetMs: 30_000,
            initialDelayMs: 1_000,
        });
        expectFound(verdict, 'Declined');
    }));

test('reconcile-not-found-yet', () =>
    guard(async () => {
        // A fresh, never-used merchantTransactionId (ADR-SDK-024): the only
        // correct verdict is NotFoundYet, and it must come from real 404s —
        // not from a transport that never reached the API.
        const verdict = await client.reconcile(freshId('absent'), {
            maxAttempts: 2,
            overallBudgetMs: 10_000,
            initialDelayMs: 500,
        });
        if (verdict.kind === 'found') {
            throw new SmokeFailure('a never-used id reconciled as Found');
        }
        if (verdict.kind !== 'notFoundYet') {
            throw new SmokeFailure(`unrecognized verdict ${(verdict as { kind: string }).kind}`);
        }
        if (verdict.lastHttpStatus !== 404) {
            throw new SmokeFailure(`expected last HTTP status 404, got ${verdict.lastHttpStatus}`);
        }
        if (!verdict.lastCorrelationId) {
            throw new SmokeFailure('no X-Correlation-ID on the NotFoundYet verdict (DX §c)');
        }
    }));
