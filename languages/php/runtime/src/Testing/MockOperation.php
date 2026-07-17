<?php

declare(strict_types=1);

namespace Revaly\Sdk\Testing;

use GuzzleHttp\Exception\ConnectException;
use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Psr7\Response;
use Psr\Http\Message\RequestInterface;

/**
 * A scripted outcome queue for one stubbed operation. The scenario methods read as the
 * failover-contract taxonomy (DX contract §d): every §2 row has a method, and
 * consecutive outcomes can be scripted so merchants can test their
 * suppression/escalation logic. When the queue runs dry the LAST scripted outcome
 * repeats.
 *
 * Transport failures are simulated with the same structured curl `errno` handler
 * context the real curl handler produces — never message strings — so classification in
 * tests exercises the exact production code path.
 */
final class MockOperation
{
    /** @var list<\Closure(RequestInterface): (\Psr\Http\Message\ResponseInterface|\Throwable)> */
    private array $queue = [];

    /** @internal created via {@see RapMockTransport} */
    public function __construct()
    {
    }

    /** @internal the next scripted outcome for this operation */
    public function next(RequestInterface $request): mixed
    {
        if ($this->queue === []) {
            throw new \LogicException('mock: operation stubbed but no outcome scripted');
        }
        $item = count($this->queue) > 1 ? array_shift($this->queue) : $this->queue[0];

        return $item($request);
    }

    // ---- success outcomes -------------------------------------------------------

    /** 200 with a synthetic approved transaction (`transactionStatus` 1). */
    public function returnsApproved(): self
    {
        return $this->pushBody(200, SyntheticData::transaction(1));
    }

    /** 200 with a synthetic declined transaction (`transactionStatus` 2). */
    public function returnsDeclined(): self
    {
        return $this->pushBody(200, SyntheticData::transaction(2));
    }

    /** 200 with a synthetic terminal-error transaction (`transactionStatus` 3). */
    public function returnsErrorOutcome(): self
    {
        return $this->pushBody(200, SyntheticData::transaction(3));
    }

    /** 200 with a transaction carrying an unmapped `transactionStatus` (forward-compat drills). */
    public function returnsUnmappedStatus(int $transactionStatus): self
    {
        return $this->pushBody(200, SyntheticData::transaction($transactionStatus));
    }

    /** 200 with the grouped envelope shape. */
    public function returnsTransactionGroup(): self
    {
        return $this->pushBody(200, SyntheticData::transactionGroup());
    }

    // ---- PermanentRejection rows (§2) --------------------------------------------

    /** One of the §2 PermanentRejection statuses (400/401/403/404/422). */
    public function returnsPermanentRejection(int $status): self
    {
        return $this->pushBody($status, SyntheticData::errorBody('synthetic rejection'));
    }

    // ---- TransientFailure rows (§2) ----------------------------------------------

    /** 503 + `code: not_processed` — the provable non-dispatch signal (immediate failover). */
    public function returnsNotProcessed503(): self
    {
        return $this->pushBody(
            503,
            SyntheticData::errorBody('temporarily unable to process', 'not_processed'),
        );
    }

    /** Connection refused (curl errno 7) — provably never sent. */
    public function throwsConnectionRefused(): self
    {
        return $this->pushConnectFailure(7, 'synthetic: connection refused');
    }

    /** DNS resolution failure (curl errno 6) — provably never sent. */
    public function throwsDnsFailure(): self
    {
        return $this->pushConnectFailure(6, 'synthetic: could not resolve host');
    }

    /** TLS handshake failure (curl errno 35) — provably never sent. */
    public function throwsSslHandshakeFailure(): self
    {
        return $this->pushConnectFailure(35, 'synthetic: TLS handshake failed');
    }

    // ---- OutcomeUnknown rows (§2) ------------------------------------------------

    /** Bare 503 (no `code`) — may have been dispatched: OutcomeUnknown. */
    public function returnsBare503(): self
    {
        return $this->pushBody(503, SyntheticData::errorBody('service unavailable'));
    }

    /** 503 with an unrecognized `code` — treated as absent: OutcomeUnknown. */
    public function returnsUnknownCode503(string $code): self
    {
        return $this->pushBody(503, SyntheticData::errorBody('service unavailable', $code));
    }

    /** 500 internal error — OutcomeUnknown. */
    public function returnsServerError(): self
    {
        return $this->pushBody(500, SyntheticData::errorBody('internal error', 'outcome_unknown'));
    }

    /** 502 (edge) — OutcomeUnknown. */
    public function returnsBadGateway(): self
    {
        return $this->pushBody(502, SyntheticData::errorBody('bad gateway'));
    }

    /** 504 (edge) — OutcomeUnknown. */
    public function returnsGatewayTimeout(): self
    {
        return $this->pushBody(504, SyntheticData::errorBody('gateway timeout'));
    }

    /**
     * Deadline expired while waiting for the response (curl errno 28) — OutcomeUnknown.
     */
    public function throwsTimeoutAfterSend(): self
    {
        return $this->pushConnectFailure(28, 'synthetic: operation timed out');
    }

    /**
     * Connect-phase timeout. curl reports the SAME errno 28 as an after-send timeout,
     * so PHP classifies this OutcomeUnknown — deliberately more conservative than
     * runtimes whose HTTP stack types the connect timeout distinctly (never guess
     * toward "safe").
     */
    public function throwsConnectTimeout(): self
    {
        return $this->pushConnectFailure(28, 'synthetic: connection timed out');
    }

    /** Connection reset mid-flight (curl errno 56, no response) — OutcomeUnknown. */
    public function throwsConnectionReset(): self
    {
        $this->queue[] = static fn (RequestInterface $request): \Throwable => new RequestException(
            'synthetic: recv failure — connection reset by peer',
            $request,
            null,
            null,
            ['errno' => 56, 'error' => 'synthetic: recv failure'],
        );

        return $this;
    }

    // ---- reconcile scripting (§3) ------------------------------------------------

    /** 404 not-visible-yet, `$times` in a row (then the next scripted outcome). */
    public function notFoundYet(int $times = 1): self
    {
        for ($i = 0; $i < $times; $i++) {
            $this->pushBody(404, SyntheticData::errorBody('transaction not found'));
        }

        return $this;
    }

    /** 200 pending intent (post-P-2 shape). */
    public function pending(): self
    {
        return $this->pushBody(200, SyntheticData::pending());
    }

    /** Then a 200 approved terminal record (chain after notFoundYet()/pending()). */
    public function thenFoundApproved(): self
    {
        return $this->returnsApproved();
    }

    /** Then a 200 declined terminal record (chain after notFoundYet()/pending()). */
    public function thenFoundDeclined(): self
    {
        return $this->returnsDeclined();
    }

    // ---- raw escapes -------------------------------------------------------------

    /**
     * A raw scripted response.
     *
     * @param array<string, string> $headers extra headers; the synthetic correlation id
     *        and JSON content type are always present unless overridden
     */
    public function returns(int $status, string $body, array $headers = []): self
    {
        return $this->pushBody($status, $body, $headers);
    }

    /** A raw scripted transport failure (rejected without a response). */
    public function throwsIo(\Throwable $failure): self
    {
        $this->queue[] = static fn (RequestInterface $request): \Throwable => $failure;

        return $this;
    }

    /**
     * @param array<string, string> $extraHeaders
     */
    private function pushBody(int $status, string $body, array $extraHeaders = []): self
    {
        $headers = array_merge(
            [
                'Content-Type' => 'application/json',
                'X-Correlation-ID' => SyntheticData::DEFAULT_CORRELATION_ID,
                'api-supported-versions' => '2.0, 2.1',
            ],
            $extraHeaders,
        );
        $this->queue[] = static fn (RequestInterface $request): Response => new Response($status, $headers, $body);

        return $this;
    }

    private function pushConnectFailure(int $errno, string $message): self
    {
        $this->queue[] = static fn (RequestInterface $request): \Throwable => new ConnectException(
            $message,
            $request,
            null,
            ['errno' => $errno, 'error' => $message],
        );

        return $this;
    }
}
