<?php

declare(strict_types=1);

namespace Revaly\Sdk\Logging;

/**
 * One observed request/response pair for the wire-trace hook (runtime-tdd §6; DX
 * contract §c). Payloads and headers arrive ALREADY scrubbed by the runtime's central
 * allowlist scrubber — never raw material — so the hook can be pointed at any sink
 * during an Enablement escalation.
 */
final class RapWireTrace
{
    /**
     * @param array<string, string>|null $requestHeaders scrubbed request headers
     * @param array<string, string>|null $responseHeaders scrubbed response headers
     */
    public function __construct(
        public readonly string $operation,
        public readonly string $method,
        public readonly string $path,
        public readonly ?int $status,
        public readonly ?string $correlationId,
        public readonly ?array $requestHeaders,
        public readonly ?string $scrubbedRequestBody,
        public readonly ?array $responseHeaders,
        public readonly ?string $scrubbedResponseBody,
    ) {
    }
}
