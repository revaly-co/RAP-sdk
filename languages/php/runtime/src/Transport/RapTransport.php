<?php

declare(strict_types=1);

namespace Revaly\Sdk\Transport;

use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Promise\Create;
use Psr\Http\Message\RequestInterface;
use Revaly\Sdk\Errors\FailureClassifier;

/**
 * The runtime's Guzzle middlewares. Both are pushed INSIDE the default stack (closest to
 * the wire), so header enforcement has the final say — the core cannot bypass it
 * (ADR-SDK-005) — and transport failures are typed from the handler's structured context
 * BEFORE the core can flatten them into message strings.
 */
final class RapTransport
{
    private function __construct()
    {
    }

    /**
     * Enforces the three runtime-owned headers on every outgoing request, replacing
     * whatever the core set (runtime-tdd §5): the ADR-SDK-005 User-Agent (merchant
     * tokens append, never replace — appending happened when the value was built), the
     * X-Api-Version pin, and `Authorization: ApiKey <key>`. The API key lives ONLY here
     * — it is never placed on the core Configuration, so no core surface (debug report,
     * exception, log) can carry it (ADR-SDK-020).
     */
    public static function headerMiddleware(
        string $apiKey,
        string $apiVersion,
        string $userAgent,
        DispatchCounter $dispatches,
    ): callable {
        return static function (callable $handler) use ($apiKey, $apiVersion, $userAgent, $dispatches): callable {
            return static function (RequestInterface $request, array $options) use (
                $handler,
                $apiKey,
                $apiVersion,
                $userAgent,
                $dispatches
            ) {
                $dispatches->count++;
                $request = $request
                    ->withHeader(RapHeaders::USER_AGENT, $userAgent)
                    ->withHeader(RapHeaders::API_VERSION, $apiVersion)
                    ->withHeader(RapHeaders::AUTHORIZATION, RapHeaders::AUTH_SCHEME . ' ' . $apiKey);

                return $handler($request, $options);
            };
        };
    }

    /**
     * Maps transport-level rejections (no HTTP response received) to the typed failure
     * classes via {@see FailureClassifier::classifyTransportRejection()}. Rejections
     * that DO carry an HTTP response pass through untouched — status classification
     * happens at the call site from the §2 table. The typed exceptions deliberately do
     * not extend Guzzle's exception types, so they surface from the generated core
     * unchanged instead of being flattened into `ApiException` message strings (which
     * would lose the structured never-sent proof).
     */
    public static function classificationMiddleware(): callable
    {
        return static function (callable $handler): callable {
            return static function (RequestInterface $request, array $options) use ($handler) {
                return $handler($request, $options)->then(
                    null,
                    static function ($reason) {
                        if ($reason instanceof RequestException && $reason->getResponse() !== null) {
                            return Create::rejectionFor($reason);
                        }
                        $failure = $reason instanceof \Throwable
                            ? $reason
                            : new \RuntimeException('non-exception transport rejection');

                        return Create::rejectionFor(FailureClassifier::classifyTransportRejection($failure));
                    },
                );
            };
        };
    }
}
