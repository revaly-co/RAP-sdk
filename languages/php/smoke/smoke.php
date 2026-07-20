<?php

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
 * Scenarios mirror the quickstart shape (README). Output is values-free
 * (ADR-SDK-020): identifiers, statuses, classes and correlation ids only —
 * never payload values, never the key, never the target host.
 *
 * Exit codes: 0 all pass (skips allowed) · 1 at least one failed · 2 not
 * configured.
 */

declare(strict_types=1);

use Psr\Http\Message\RequestInterface;
use Revaly\Sdk\Core\Model\CreditCard;
use Revaly\Sdk\Core\Model\PaymentMethod;
use Revaly\Sdk\Core\Model\PaymentRequest;
use Revaly\Sdk\Errors\PermanentRejectionException;
use Revaly\Sdk\Errors\RapCoreException;
use Revaly\Sdk\Errors\TransientFailureException;
use Revaly\Sdk\RapClient;
use Revaly\Sdk\Reconcile\Found;
use Revaly\Sdk\Reconcile\NotFoundYet;
use Revaly\Sdk\Reconcile\RapReconcileVerdict;
use Revaly\Sdk\Reconcile\RapTransactionOutcome;
use Revaly\Sdk\Reconcile\ReconcilePolicy;

require __DIR__ . '/../vendor/autoload.php';

// The platform's executor fault seam (Backbone ADR 014 test affordance):
// value "pre-dispatch" makes the charge fail between intent reservation and
// gateway dispatch — the only deterministic live trigger for the
// 503 + code=not_processed fast-failover row.
const FAULT_INJECT_HEADER = 'X-Backbone-Fault-Inject';
// One synthetic test PAN; the EXPIRY drives the outcome (staging-verified
// matrix 2026-07-18: 12/2027 approves, 12/2020 declines).
const TEST_PAN = '4111111111111111';

/** A scenario assertion failure (values-free message). */
final class SmokeFailure extends \RuntimeException
{
}

/** A scenario that cannot run in this environment (reported, never silent). */
final class SmokeSkip extends \RuntimeException
{
}

/** Unique merchantTransactionId (≤ 100 chars) — every reconcile scenario uses a fresh one (ADR-SDK-024). */
function freshId(string $label): string
{
    return sprintf('smoke-php-%s-%d-%s', $label, (int) (microtime(true) * 1000), bin2hex(random_bytes(4)));
}

/**
 * Charge request with the minimal live-approving field set (staging-verified
 * 2026-07-18): a cardholder name is SERVER-required for creditCard (per-type
 * rule, spec-documented since 2.3.0); paymentMethodType is optional since
 * spec 2.3.0 (Backbone #251 inference) — sent explicitly here to keep the
 * wire shape deterministic across the six languages. orderId + email are
 * additionally required by the staging simulator for an approval. Synthetic
 * test cards only.
 */
function buildCharge(string $mtid, string $pan, string $expiryYear, ?string $routingId, bool $withName = true): PaymentRequest
{
    $card = new CreditCard();
    $card->setNumber($pan);
    $card->setExpiryMonth('12');
    $card->setExpiryYear($expiryYear);
    $card->setCardVerificationCode('123');

    $method = new PaymentMethod();
    if ($withName) {
        $method->setFullName('Smoke Test');
    }
    $method->setEmail('smoke@example.com');
    $method->setCreditCard($card);

    $request = new PaymentRequest();
    $request->setAmount(1999);
    $request->setPaymentMethodType('creditCard');
    $request->setCurrency('USD');
    $request->setMerchantTransactionId($mtid);
    $request->setOrderId($mtid);
    $request->setPaymentMethod($method);
    if ($routingId !== null && $routingId !== '') {
        $request->setGatewayRoutingId($routingId);
    }

    return $request;
}

/**
 * Values-free rendering of an unexpected failure: typed classes carry
 * status/code/correlation-only messages; anything else reports its type only,
 * so transport error chains cannot leak endpoint details into CI logs.
 */
function classified(string $context, \Throwable $err): SmokeFailure
{
    if ($err instanceof RapCoreException) {
        return new SmokeFailure(sprintf('%s, got: %s', $context, $err->getMessage()));
    }

    return new SmokeFailure(sprintf('%s, got %s', $context, $err::class));
}

/**
 * Asserts a Found verdict carrying the wanted outcome and a correlation id.
 * The verdict set is open — an unrecognized verdict is a real finding here,
 * not a pass.
 */
function expectFound(RapReconcileVerdict $verdict, RapTransactionOutcome $want): string
{
    if ($verdict instanceof Found) {
        if ($verdict->getOutcome() !== $want) {
            throw new SmokeFailure(sprintf('expected outcome %s, got %s', $want->value, $verdict->getOutcome()->value));
        }
        if (($verdict->getCorrelationId() ?? '') === '') {
            throw new SmokeFailure('no X-Correlation-ID on the Found verdict (DX §c)');
        }

        return sprintf(' (outcome=%s correlation=%s)', $verdict->getOutcome()->value, $verdict->getCorrelationId());
    }
    if ($verdict instanceof NotFoundYet) {
        throw new SmokeFailure(sprintf(
            'charge not visible after %d attempts (%.1fs) — expected Found',
            $verdict->getAttempts(),
            $verdict->getElapsedSeconds(),
        ));
    }

    throw new SmokeFailure(sprintf('unrecognized verdict %s', $verdict::class));
}

$baseUrl = getenv('RAP_SMOKE_BASE_URL') ?: '';
$apiKey = getenv('RAP_SMOKE_API_KEY') ?: '';
$routingId = getenv('RAP_SMOKE_GATEWAY_ROUTING_ID') ?: null;
$faultValue = getenv('RAP_SMOKE_FAULT_INJECT') ?: null;
if ($baseUrl === '' || $apiKey === '') {
    fwrite(STDERR, "smoke: RAP_SMOKE_BASE_URL and RAP_SMOKE_API_KEY must be set (ADR-SDK-024) — refusing to run.\n");
    exit(2);
}

// One client per configuration, quickstart-shaped. The wire-trace hook is the
// designed observer for correlation ids on the success path (DX §c); events
// arrive already scrubbed by the runtime.
$lastCorrelation = null;
$client = new RapClient(
    apiKey: $apiKey,
    baseUrl: $baseUrl,
    connectTimeout: 5.0,
    overallDeadline: 15.0,
    wireTraceHook: function ($trace) use (&$lastCorrelation): void {
        $lastCorrelation = $trace->correlationId;
    },
);

// A separately configured client whose key is a synthetic invalid value — the
// auth-rejection row.
$badKeyClient = new RapClient(
    apiKey: 'sk_smoke_synthetic_invalid',
    baseUrl: $baseUrl,
    connectTimeout: 5.0,
    overallDeadline: 15.0,
);

// A client whose Guzzle handler stamps the platform's fault-inject header —
// every charge through it deterministically fails pre-dispatch
// (503 + code=not_processed). The handler seam sits INSIDE the runtime's own
// header injection, so auth/UA/version behaviour is unchanged.
$faultClient = null;
if ($faultValue !== null && $faultValue !== '') {
    $innerHandler = \GuzzleHttp\Utils::chooseHandler();
    $faultClient = new RapClient(
        apiKey: $apiKey,
        baseUrl: $baseUrl,
        overallDeadline: 15.0,
        transport: static fn (RequestInterface $request, array $options) => $innerHandler(
            $request->withHeader(FAULT_INJECT_HEADER, $faultValue),
            $options,
        ),
    );
}

// Charged ids feed the reconcile scenarios: the verdicts — through the
// runtime's own outcome mapping — are the proof the charge outcomes were what
// the smoke claims.
$chargedId = freshId('charge');
$declinedId = freshId('decline');

$scenarios = [
    'charge-approved' => function () use ($client, $chargedId, $routingId, &$lastCorrelation): string {
        $transaction = $client->charge(buildCharge($chargedId, TEST_PAN, '2027', $routingId));
        if (($transaction->getTransactionId() ?? '') === '') {
            throw new SmokeFailure('transactionId is empty on the success surface');
        }
        if (($lastCorrelation ?? '') === '') {
            throw new SmokeFailure('no X-Correlation-ID observed on the success path (DX §c)');
        }

        return sprintf(' (txn=%s correlation=%s)', $transaction->getTransactionId(), $lastCorrelation);
    },

    'charge-declined' => function () use ($client, $declinedId, $routingId, &$lastCorrelation): string {
        // An expired expiry declines deterministically (same PAN). A decline is a business
        // outcome on the SUCCESS surface — not a failure class;
        // reconcile-found-declined proves the mapping below.
        $transaction = $client->charge(buildCharge($declinedId, TEST_PAN, '2020', $routingId));
        if (($transaction->getTransactionId() ?? '') === '') {
            throw new SmokeFailure('transactionId is empty on the declined-charge surface');
        }
        if (($lastCorrelation ?? '') === '') {
            throw new SmokeFailure('no X-Correlation-ID observed on the declined-charge path (DX §c)');
        }

        return sprintf(' (txn=%s correlation=%s)', $transaction->getTransactionId(), $lastCorrelation);
    },

    'charge-validation-rejected' => function () use ($client, $routingId): string {
        // A NAMELESS charge (no fullName/firstName/lastName) passes every
        // client-side model — the php/python cores reject an empty PAN locally,
        // so the PAN stays valid — and fails the server's cardholder-name
        // business validation: the rejection is proven to come from reality
        // (HTTP 400; 4xx carries no code).
        try {
            $client->charge(buildCharge(freshId('validation'), TEST_PAN, '2027', $routingId, withName: false));
        } catch (PermanentRejectionException $rejection) {
            if (!in_array($rejection->getStatusCode(), [400, 422], true)) {
                throw new SmokeFailure(sprintf('expected HTTP 400/422, got %d', $rejection->getStatusCode() ?? 0));
            }
            if (($rejection->getCorrelationId() ?? '') === '') {
                throw new SmokeFailure('no X-Correlation-ID on the rejection (DX §c)');
            }

            return sprintf(' (status=%d correlation=%s)', $rejection->getStatusCode(), $rejection->getCorrelationId());
        } catch (SmokeFailure $failure) {
            throw $failure;
        } catch (\Throwable $err) {
            throw classified('expected PermanentRejectionException', $err);
        }

        throw new SmokeFailure('server accepted a nameless charge — expected PermanentRejectionException');
    },

    'charge-auth-rejected' => function () use ($badKeyClient, $routingId): string {
        try {
            $badKeyClient->charge(buildCharge(freshId('auth'), TEST_PAN, '2027', $routingId));
        } catch (PermanentRejectionException $rejection) {
            if (!in_array($rejection->getStatusCode(), [401, 403], true)) {
                throw new SmokeFailure(sprintf('expected HTTP 401/403, got %d', $rejection->getStatusCode() ?? 0));
            }
            if (($rejection->getCorrelationId() ?? '') === '') {
                throw new SmokeFailure('no X-Correlation-ID on the auth rejection (DX §c)');
            }

            return sprintf(' (status=%d correlation=%s)', $rejection->getStatusCode(), $rejection->getCorrelationId());
        } catch (SmokeFailure $failure) {
            throw $failure;
        } catch (\Throwable $err) {
            throw classified('expected PermanentRejectionException', $err);
        }

        throw new SmokeFailure('server accepted a synthetic invalid key — expected PermanentRejectionException');
    },

    'charge-not-processed-503' => function () use ($faultClient, $routingId): string {
        // The fast-failover row (503 + code=not_processed): valid input cannot
        // reach it deterministically, so the platform's fault injector fails
        // the charge pre-dispatch. TransientFailureException is the ONLY
        // acceptable class here — it is the row that licenses immediate
        // failover.
        if ($faultClient === null) {
            throw new SmokeSkip('RAP_SMOKE_FAULT_INJECT not set (injector is staging-only)');
        }
        try {
            $faultClient->charge(buildCharge(freshId('fault'), TEST_PAN, '2027', $routingId));
        } catch (TransientFailureException $transient) {
            if ($transient->getStatusCode() !== 503) {
                throw new SmokeFailure(sprintf('expected HTTP 503, got %d', $transient->getStatusCode() ?? 0));
            }
            if ($transient->getErrorCode() !== 'not_processed') {
                throw new SmokeFailure(sprintf('expected code=not_processed, got "%s"', $transient->getErrorCode() ?? ''));
            }
            if (($transient->getCorrelationId() ?? '') === '') {
                throw new SmokeFailure('no X-Correlation-ID on the not-processed failure (DX §c)');
            }

            return sprintf(' (status=503 code=%s correlation=%s)', $transient->getErrorCode(), $transient->getCorrelationId());
        } catch (SmokeFailure $failure) {
            throw $failure;
        } catch (\Throwable $err) {
            throw classified('expected TransientFailureException', $err);
        }

        throw new SmokeFailure('fault-injected charge succeeded — expected TransientFailureException');
    },

    'reconcile-found-approved' => function () use ($client, $chargedId): string {
        // Found(Approved) through the runtime's own outcome mapping is the
        // approval proof for the first charge; visibility is asynchronous,
        // hence the budget.
        $verdict = $client->reconcile($chargedId, new ReconcilePolicy(
            maxAttempts: 5,
            overallBudgetSeconds: 30.0,
            initialDelaySeconds: 1.0,
        ));

        return expectFound($verdict, RapTransactionOutcome::Approved);
    },

    'reconcile-found-declined' => function () use ($client, $declinedId): string {
        // The declined charge must reconcile as Found(Declined) — the outcome
        // branch that tells a merchant their own gateway is safe.
        $verdict = $client->reconcile($declinedId, new ReconcilePolicy(
            maxAttempts: 5,
            overallBudgetSeconds: 30.0,
            initialDelaySeconds: 1.0,
        ));

        return expectFound($verdict, RapTransactionOutcome::Declined);
    },

    'reconcile-not-found-yet' => function () use ($client): string {
        // A fresh, never-used merchantTransactionId (ADR-SDK-024): the only
        // correct verdict is NotFoundYet, and it must come from real 404s —
        // not from a transport that never reached the API.
        $verdict = $client->reconcile(freshId('absent'), new ReconcilePolicy(
            maxAttempts: 2,
            overallBudgetSeconds: 10.0,
            initialDelaySeconds: 0.5,
        ));
        if ($verdict instanceof NotFoundYet) {
            if ($verdict->getLastHttpStatus() !== 404) {
                throw new SmokeFailure(sprintf('expected last HTTP status 404, got %d', $verdict->getLastHttpStatus() ?? 0));
            }
            if (($verdict->getCorrelationId() ?? '') === '') {
                throw new SmokeFailure('no X-Correlation-ID on the NotFoundYet verdict (DX §c)');
            }

            return sprintf(' (attempts=%d correlation=%s)', $verdict->getAttempts(), $verdict->getCorrelationId());
        }
        if ($verdict instanceof Found) {
            throw new SmokeFailure('a never-used id reconciled as Found');
        }

        throw new SmokeFailure(sprintf('unrecognized verdict %s', $verdict::class));
    },
];

printf("RAP contract smoke (php): %d scenarios\n", count($scenarios));
$failures = 0;
$skips = 0;
foreach ($scenarios as $name => $run) {
    try {
        $detail = $run();
        printf("PASS %s%s\n", $name, $detail);
    } catch (SmokeSkip $skip) {
        ++$skips;
        printf("SKIP %s (%s)\n", $name, $skip->getMessage());
    } catch (SmokeFailure $failure) {
        ++$failures;
        printf("FAIL %s: %s\n", $name, $failure->getMessage());
    } catch (RapCoreException $err) {
        // Typed-class messages are values-free by construction.
        ++$failures;
        printf("FAIL %s: unexpected %s\n", $name, $err->getMessage());
    } catch (\Throwable $err) {
        // Never print raw messages — transport error chains can carry endpoint
        // details into CI logs.
        ++$failures;
        printf("FAIL %s: unexpected %s\n", $name, $err::class);
    }
}

$passed = count($scenarios) - $failures - $skips;
if ($failures > 0) {
    printf("RESULT: FAIL (%d/%d passed, %d skipped)\n", $passed, count($scenarios), $skips);
    exit(1);
}
printf("RESULT: PASS (%d/%d passed, %d skipped)\n", $passed, count($scenarios), $skips);
exit(0);
