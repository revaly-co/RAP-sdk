<?php

declare(strict_types=1);

namespace Revaly\Sdk\Reconcile;

use GuzzleHttp\ClientInterface;
use GuzzleHttp\Psr7\Request;
use GuzzleHttp\RequestOptions;
use Psr\Http\Message\ResponseInterface;
use Psr\Log\LoggerInterface;
use Revaly\Sdk\Core\Model\PendingTransactionResponse;
use Revaly\Sdk\Core\Model\TransactionResponse;
use Revaly\Sdk\Core\ObjectSerializer;
use Revaly\Sdk\Errors\FailureClassifier;
use Revaly\Sdk\Errors\RapCoreException;
use Revaly\Sdk\Errors\RapFailureClass;
use Revaly\Sdk\Logging\RapScrubber;
use Revaly\Sdk\Logging\RapWireTrace;
use Revaly\Sdk\Transport\RapHeaders;

/**
 * The OutcomeUnknown reconciliation procedure (failover-contract §3): GET-only,
 * side-effect-free, caller-bounded — the only loop the runtime owns (ADR-SDK-004).
 *
 * This helper issues the merchant-transaction GET at the raw HTTP level (through the
 * same shared Guzzle client and header middleware as every other SDK request) instead of
 * the generated core binding, for a safety reason: the core's generated wrapper for this
 * endpoint merges ALL response branches into one property blob with no discrimination
 * (`GetTransactionByMerchantTransactionId200Response` carries terminal, pending AND
 * group fields side by side). Classification here therefore works from the RAW body: the
 * required `state` field discriminates a pending intent (it exists only on the pending
 * schema), and terminal records bind directly to {@see TransactionResponse} — classify
 * from raw bodies, never core wrappers (repo rule 5).
 */
final class RapReconciler
{
    public function __construct(
        private readonly ClientInterface $client,
        private readonly string $baseUrl,
        private readonly string $apiVersion,
        private readonly LoggerInterface $logger,
        private readonly ?\Closure $wireTraceHook,
    ) {
    }

    /**
     * Runs the reconcile loop until a record is visible or the policy bounds are spent.
     *
     * @throws RapCoreException only for a rejected READ that polling can never fix
     *         (PermanentRejection other than 404 — bad credentials, malformed id); 404
     *         is the NotFoundYet signal, and degraded reads (5xx/timeouts/transport)
     *         keep polling within the budget.
     */
    public function reconcile(string $merchantTransactionId, ReconcilePolicy $policy): RapReconcileVerdict
    {
        if (trim($merchantTransactionId) === '') {
            throw new \InvalidArgumentException('merchantTransactionId is required');
        }

        $path = '/transactions/merchant/' . rawurlencode($merchantTransactionId);
        $start = microtime(true);
        $attempts = 0;
        $lastCorrelationId = null;
        $lastHttpStatus = null;

        while (true) {
            $attempts++;

            $response = null;
            try {
                $response = $this->client->send(
                    new Request('GET', $this->baseUrl . $path, ['Accept' => 'application/json']),
                    [RequestOptions::HTTP_ERRORS => false],
                );
            } catch (\Throwable $failure) {
                // Transport failure on the READ: never-sent proof or not, the WRITE's
                // status is still unknown — keep polling within the caller's budget.
                $classified = FailureClassifier::classifyTransportRejection($failure);
                $this->logger->warning(
                    'rap.reconcile attempt {attempt} transport failure ({class}); continuing within policy',
                    ['attempt' => $attempts, 'class' => $classified->getFailureClass()->value],
                );
                $this->trace($path, null, null, null);
            }

            if ($response !== null) {
                $lastHttpStatus = $response->getStatusCode();
                $correlationId = $response->getHeaderLine(RapHeaders::CORRELATION_ID);
                $correlationId = $correlationId === '' ? null : $correlationId;
                if ($correlationId !== null) {
                    $lastCorrelationId = $correlationId;
                }
                $body = (string) $response->getBody();
                $this->trace($path, $response->getStatusCode(), $correlationId, $body);

                if (intdiv($response->getStatusCode(), 100) === 2) {
                    $found = $this->readFound($body, $lastCorrelationId, $attempts);
                    if ($found !== null) {
                        return $found;
                    }
                    // 2xx that did not parse: ambiguous read — poll again within budget.
                } elseif ($response->getStatusCode() === 404) {
                    // Not yet visible — the NotFoundYet signal, not an error (§3).
                    $this->logger->debug(
                        'rap.reconcile attempt {attempt} not visible yet (404)',
                        ['attempt' => $attempts],
                    );
                } else {
                    $classified = FailureClassifier::classifyResponse(
                        $response->getStatusCode(),
                        $body,
                        $this->apiVersion,
                        $correlationId,
                    );
                    if ($classified->getFailureClass() === RapFailureClass::PermanentRejection) {
                        // 400/401/403/422 escape: polling will never fix a rejected read
                        // (bad credentials, malformed id) — the caller must see it.
                        throw $classified;
                    }
                    // Degraded read path (5xx/timeout on the GET) — exactly the window
                    // where visibility is widest; keep polling within the budget.
                    $this->logger->warning(
                        'rap.reconcile attempt {attempt} degraded read [status={status} class={class}]; continuing within policy',
                        [
                            'attempt' => $attempts,
                            'status' => $response->getStatusCode(),
                            'class' => $classified->getFailureClass()->value,
                        ],
                    );
                }
            }

            if ($attempts >= $policy->getMaxAttempts()) {
                break;
            }

            $elapsed = microtime(true) - $start;
            $delay = $policy->delayForAttempt($attempts);
            if ($elapsed + $delay >= $policy->getOverallBudgetSeconds()) {
                break;
            }

            if ($delay > 0) {
                usleep((int) round($delay * 1_000_000));
            }
        }

        $elapsed = microtime(true) - $start;
        $this->logger->info(
            'rap.reconcile verdict=NotFoundYet attempts={attempts} elapsedMs={elapsedMs} lastStatus={lastStatus} correlation={correlation}',
            [
                'attempts' => $attempts,
                'elapsedMs' => (int) round($elapsed * 1000),
                'lastStatus' => $lastHttpStatus,
                'correlation' => $lastCorrelationId,
            ],
        );

        return new NotFoundYet($attempts, $elapsed, $lastCorrelationId, $lastHttpStatus);
    }

    /**
     * Maps a 2xx body to a Found verdict from the RAW json. Returns null for a body
     * this SDK cannot read at all (→ poll-continue: an ambiguous read is not a
     * sighting).
     */
    private function readFound(string $body, ?string $correlationId, int $attempt): ?RapReconcileVerdict
    {
        $root = json_decode($body, false);
        if (!is_object($root)) {
            $this->logger->warning(
                'rap.reconcile attempt {attempt} returned 2xx with an unreadable body; continuing within policy',
                ['attempt' => $attempt],
            );

            return null;
        }

        // `state` exists only on the pending schema — its presence is authoritative
        // (the spec marks it the discriminator).
        if (isset($root->state) && is_string($root->state)) {
            $pending = null;
            try {
                $bound = ObjectSerializer::deserialize($root, PendingTransactionResponse::class);
                $pending = $bound instanceof PendingTransactionResponse ? $bound : null;
            } catch (\Throwable $bindFailure) {
                // A pending-shaped record this SDK version cannot bind is still a
                // sighting — surface it conservatively rather than polling on.
            }
            if ($pending !== null) {
                $this->logger->info(
                    'rap.reconcile verdict=Found outcome=Pending correlation={correlation}',
                    ['correlation' => $correlationId],
                );

                return new Found(RapTransactionOutcome::Pending, null, $pending, $correlationId);
            }

            return new Found(RapTransactionOutcome::Unknown, null, null, $correlationId);
        }

        // Terminal records bind DIRECTLY to TransactionResponse — never through the
        // core's merged wrapper (see the class doc).
        try {
            $transaction = ObjectSerializer::deserialize($root, TransactionResponse::class);
            if (!$transaction instanceof TransactionResponse) {
                return new Found(RapTransactionOutcome::Unknown, null, null, $correlationId);
            }
            $outcome = self::mapOutcome($transaction->getTransactionStatus());
            $this->logger->info(
                'rap.reconcile verdict=Found outcome={outcome} correlation={correlation}',
                ['outcome' => $outcome->value, 'correlation' => $correlationId],
            );

            return new Found($outcome, $transaction, null, $correlationId);
        } catch (\Throwable $bindFailure) {
            // A response shape this SDK version does not recognize (e.g. a grouped
            // envelope, a new enum value, or a post-P-2 variant). Found-but-unmapped
            // is still FOUND.
            return new Found(RapTransactionOutcome::Unknown, null, null, $correlationId);
        }
    }

    private static function mapOutcome(?int $transactionStatus): RapTransactionOutcome
    {
        return match ($transactionStatus) {
            1 => RapTransactionOutcome::Approved,
            2 => RapTransactionOutcome::Declined,
            3 => RapTransactionOutcome::Error,
            default => RapTransactionOutcome::Unknown,
        };
    }

    private function trace(string $path, ?int $status, ?string $correlationId, ?string $rawResponseBody): void
    {
        if ($this->wireTraceHook === null) {
            return;
        }
        try {
            ($this->wireTraceHook)(new RapWireTrace(
                'reconcile',
                'GET',
                $path,
                $status,
                $correlationId,
                null,
                null,
                null,
                $rawResponseBody === null ? null : RapScrubber::scrubJson($rawResponseBody),
            ));
        } catch (\Throwable $hookFailure) {
            // Observer exceptions are swallowed (runtime-tdd §6) — tracing must never
            // change payment control flow.
            $this->logger->debug('rap.wiretrace hook threw; ignored', ['exception' => get_class($hookFailure)]);
        }
    }
}
