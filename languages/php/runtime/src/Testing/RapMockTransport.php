<?php

declare(strict_types=1);

namespace Revaly\Sdk\Testing;

use GuzzleHttp\Promise\Create;
use GuzzleHttp\Promise\PromiseInterface;
use Psr\Http\Message\RequestInterface;
use Revaly\Sdk\Transport\RapUserAgent;

/**
 * The first-class no-network test double (DX contract §d; runtime-tdd §8): a Guzzle
 * handler that scripts every row of the failover-contract §2 table and both §3
 * verdicts, so a merchant can unit-test their failover handler with no network.
 *
 * Pass it as the client's `transport`:
 *
 * ```php
 * $mock = new RapMockTransport();
 * $mock->charge()->returnsNotProcessed503();
 * $client = new RapClient(apiKey: 'sk-synthetic', transport: $mock);
 * ```
 *
 * Every request is recorded ({@see getRequests()}) and asserted to carry the SDK
 * User-Agent (ADR-SDK-005) — the mock sits where the wire would be, below the runtime
 * middlewares, so it sees exactly what the network would.
 */
final class RapMockTransport
{
    /** @var list<array{method: string, prefix: string, operation: MockOperation}> */
    private array $stubs = [];

    /** @var list<RecordedRequest> */
    private array $requests = [];

    private bool $assertUserAgent = true;

    /** Disables the User-Agent presence assertion (for tests of the assertion itself). */
    public function withoutUserAgentAssertion(): self
    {
        $this->assertUserAgent = false;

        return $this;
    }

    /** Every request this transport has served, in order. */
    public function getRequests(): array
    {
        return $this->requests;
    }

    /** Stubs `POST /payments` (charge). */
    public function charge(): MockOperation
    {
        return $this->stub('POST', '/payments');
    }

    /** Stubs `POST /payments/authorize`. */
    public function authorize(): MockOperation
    {
        return $this->stub('POST', '/payments/authorize');
    }

    /** Stubs the reconcile GET for one merchantTransactionId. */
    public function reconcile(string $merchantTransactionId): MockOperation
    {
        return $this->stub('GET', '/transactions/merchant/' . rawurlencode($merchantTransactionId));
    }

    /** Stubs an arbitrary method + path prefix; the longest matching prefix wins. */
    public function stub(string $method, string $pathPrefix): MockOperation
    {
        $operation = new MockOperation();
        $this->stubs[] = [
            'method' => strtoupper($method),
            'prefix' => $pathPrefix,
            'operation' => $operation,
        ];

        return $operation;
    }

    /** The Guzzle handler contract. */
    public function __invoke(RequestInterface $request, array $options): PromiseInterface
    {
        $this->requests[] = RecordedRequest::from($request);

        if ($this->assertUserAgent) {
            $userAgent = $request->getHeaderLine('User-Agent');
            if (!str_starts_with($userAgent, RapUserAgent::PRODUCT_NAME . '/')) {
                throw new \LogicException(sprintf(
                    'mock: request is missing the SDK User-Agent (ADR-SDK-005); got "%s"',
                    $userAgent,
                ));
            }
        }

        $operation = $this->match($request->getMethod(), $request->getUri()->getPath());
        if ($operation === null) {
            throw new \LogicException(sprintf(
                'mock: no stub for %s %s',
                $request->getMethod(),
                $request->getUri()->getPath(),
            ));
        }

        $outcome = $operation->next($request);
        if ($outcome instanceof \Throwable) {
            return Create::rejectionFor($outcome);
        }

        return Create::promiseFor($outcome);
    }

    private function match(string $method, string $path): ?MockOperation
    {
        $best = null;
        $bestLength = -1;
        foreach ($this->stubs as $stub) {
            if ($stub['method'] !== strtoupper($method)) {
                continue;
            }
            if (!str_starts_with($path, $stub['prefix'])) {
                continue;
            }
            if (strlen($stub['prefix']) > $bestLength) {
                $best = $stub['operation'];
                $bestLength = strlen($stub['prefix']);
            }
        }

        return $best;
    }
}
