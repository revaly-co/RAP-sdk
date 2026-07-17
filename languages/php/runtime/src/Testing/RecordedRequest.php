<?php

declare(strict_types=1);

namespace Revaly\Sdk\Testing;

use Psr\Http\Message\RequestInterface;

/** One request observed by {@see RapMockTransport}, for merchant test assertions. */
final class RecordedRequest
{
    /**
     * @param array<string, array<string>> $headers
     */
    public function __construct(
        public readonly string $method,
        public readonly string $uri,
        public readonly string $path,
        public readonly array $headers,
        public readonly string $body,
    ) {
    }

    public static function from(RequestInterface $request): self
    {
        return new self(
            $request->getMethod(),
            (string) $request->getUri(),
            $request->getUri()->getPath(),
            $request->getHeaders(),
            (string) $request->getBody(),
        );
    }

    /** The first value of the named header (case-insensitive), or null. */
    public function header(string $name): ?string
    {
        foreach ($this->headers as $headerName => $values) {
            if (strcasecmp($headerName, $name) === 0) {
                return $values[0] ?? null;
            }
        }

        return null;
    }
}
