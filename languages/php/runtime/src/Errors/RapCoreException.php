<?php

declare(strict_types=1);

namespace Revaly\Sdk\Errors;

/**
 * Base of the three typed failure classes (runtime-tdd §3; failover-contract §2). Every
 * typed error carries: the class, the HTTP status (if any), the wire `code` verbatim (if
 * any), the human `error` message, opaque `details`, the correlation id, and the raw
 * response body reference.
 *
 * The merchant API key never appears in exception messages (ADR-SDK-020); messages are
 * built from fixed text plus status/class/code tokens only.
 *
 * Note: {@see \Exception::getCode()} is PHP's integer exception code and carries the
 * HTTP status here; the wire's string `code` safety signal is {@see getErrorCode()}.
 */
abstract class RapCoreException extends \RuntimeException
{
    private readonly ?string $edgeReference;

    /**
     * @param mixed $details opaque additional error detail — never classify from it
     *        (the SDK itself reads exactly one key of it, `edgeRejection`, on a 403 —
     *        ADR-SDK-033 — surfaced as {@see isEdgeRejection()} / {@see getEdgeReference()})
     * @param bool $isEdgeRejection true when the edge firewall blocked the request before
     *        it reached the platform (403 + `details.edgeRejection: true`)
     * @param ?string $edgeReference the edge firewall's tracking reference
     *        (`details.reference`, equal to the `x-azure-ref` header); null unless
     *        `$isEdgeRejection`
     */
    public function __construct(
        string $message,
        private readonly ?int $statusCode = null,
        private readonly ?string $errorCode = null,
        private readonly ?string $apiError = null,
        private readonly mixed $details = null,
        private readonly ?string $correlationId = null,
        private readonly ?string $rawBody = null,
        ?\Throwable $previous = null,
        private readonly bool $isEdgeRejection = false,
        ?string $edgeReference = null,
    ) {
        parent::__construct($message, $statusCode ?? 0, $previous);
        $this->edgeReference = $isEdgeRejection ? $edgeReference : null;
    }

    /** The failure class driving the caller's failover decision. */
    abstract public function getFailureClass(): RapFailureClass;

    /** The HTTP status code, when a response was received. */
    public function getStatusCode(): ?int
    {
        return $this->statusCode;
    }

    /**
     * The wire's `ErrorResponse.code`, verbatim. An OPEN string: new values arrive with
     * OQ-2 and unrecognized values are treated as absent for classification — never a
     * closed enum (repo rule 5).
     */
    public function getErrorCode(): ?string
    {
        return $this->errorCode;
    }

    /** The human-readable `error` message from the response body, if any. Never classify from it. */
    public function getApiError(): ?string
    {
        return $this->apiError;
    }

    /**
     * Opaque additional details from the response body. Treat as opaque (§2): the SDK
     * reads exactly one key of it, `edgeRejection` on a 403 (ADR-SDK-033).
     */
    public function getDetails(): mixed
    {
        return $this->details;
    }

    /**
     * True when the production edge firewall blocked this request before it reached the
     * platform: an HTTP 403 whose body carries `details.edgeRejection: true` (ADR-SDK-033).
     * Such a failure is a {@see TransientFailureException} — the payment was definitively
     * not processed. Charge and authorize: fail over, or fix the request content and retry;
     * capture, void, refund and refund-cancel: retry the same request.
     */
    public function isEdgeRejection(): bool
    {
        return $this->isEdgeRejection;
    }

    /**
     * The edge firewall's tracking reference (`details.reference`, equal to the
     * `x-azure-ref` response header) when {@see isEdgeRejection()} is true; otherwise
     * null. Quote it to support — it identifies the exact firewall decision.
     */
    public function getEdgeReference(): ?string
    {
        return $this->edgeReference;
    }

    /** The `X-Correlation-ID` of the response, if one was received. Quote it in support tickets. */
    public function getCorrelationId(): ?string
    {
        return $this->correlationId;
    }

    /** The raw response body, for diagnostics. May be null when no response was received. */
    public function getRawBody(): ?string
    {
        return $this->rawBody;
    }
}
