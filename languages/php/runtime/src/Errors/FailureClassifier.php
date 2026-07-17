<?php

declare(strict_types=1);

namespace Revaly\Sdk\Errors;

use GuzzleHttp\Exception\ConnectException;
use GuzzleHttp\Exception\RequestException;

/**
 * The normative failure-classification algorithm of failover-contract.md §2. Every rule
 * here is contract, not heuristic:
 *
 *     if transport error and request provably never sent          → TransientFailure
 *     if HTTP status in {400, 401, 403, 404, 422}                 → PermanentRejection
 *     if HTTP status == 503 and body.code == "not_processed"      → TransientFailure
 *     if HTTP status >= 500                                       → OutcomeUnknown
 *     if deadline exceeded after send / reset / ambiguous         → OutcomeUnknown
 *
 * Never classify from `error` message text; treat `details` as opaque; unrecognized
 * `code` values are treated as absent; when the stack cannot prove the request was never
 * sent, classify OutcomeUnknown — never guess toward "safe".
 *
 * `code` is read from the RAW body as an OPEN string — deliberately never through the
 * generated core's ErrorResponse model, whose setter coerces unrecognized wire values to
 * `unknown_default_open_api` (ADR-SDK-023 uniform safety rule; repo rule 5): new values
 * arrive with OQ-2 and must never break classification.
 */
final class FailureClassifier
{
    /** The provable-non-dispatch safety signal (platform P-1, ADR-SDK-007). */
    public const NOT_PROCESSED = 'not_processed';

    /**
     * curl error numbers that prove the request was never sent, read as STRUCTURED
     * values from Guzzle's handler context (`errno`) — never parsed out of message
     * text. All of these fail before any HTTP bytes leave the client: name resolution,
     * TCP connection establishment, or the TLS handshake.
     */
    private const NEVER_SENT_CURL_ERRNOS = [
        5,  // CURLE_COULDNT_RESOLVE_PROXY
        6,  // CURLE_COULDNT_RESOLVE_HOST
        7,  // CURLE_COULDNT_CONNECT
        35, // CURLE_SSL_CONNECT_ERROR      (TLS handshake)
        58, // CURLE_SSL_CERTPROBLEM       (local client cert — handshake)
        59, // CURLE_SSL_CIPHER            (handshake)
        60, // CURLE_PEER_FAILED_VERIFICATION (incl. legacy CURLE_SSL_CACERT)
        66, // CURLE_SSL_ENGINE_INITFAILED (before connection)
        77, // CURLE_SSL_CACERT_BADFILE    (handshake setup)
        83, // CURLE_SSL_ISSUER_ERROR      (handshake)
        90, // CURLE_SSL_PINNEDPUBKEYNOTMATCH (handshake)
        91, // CURLE_SSL_INVALIDCERTSTATUS (handshake)
    ];

    /**
     * CURLE_OPERATION_TIMEDOUT. curl reports the SAME error number for a
     * connect-phase timeout and for the overall deadline expiring while waiting for the
     * response, so PHP cannot structurally prove the request was never sent on a
     * timeout. Both classify OutcomeUnknown — the contract forbids guessing toward
     * "safe" (this is deliberately more conservative than runtimes whose HTTP stack
     * types the connect timeout distinctly).
     */
    private const CURLE_OPERATION_TIMEDOUT = 28;

    private function __construct()
    {
    }

    /**
     * Classifies a received non-success HTTP response. Statuses outside the §2 table
     * (e.g. 409, 3xx) are ambiguous and classify as OutcomeUnknown — reconcile reveals
     * the true state.
     *
     * @param string $apiVersion the pinned X-Api-Version. On "2.0" the
     *        `ErrorResponse.code` field is not part of the documented contract, so the
     *        fast-failover class narrows to client-provable never-sent failures only:
     *        503 + `not_processed` is NOT honored and falls through to OutcomeUnknown
     *        (runtime-tdd §1 [Decided]).
     */
    public static function classifyResponse(
        int $statusCode,
        ?string $rawBody,
        string $apiVersion,
        ?string $correlationId,
    ): RapCoreException {
        [$code, $error, $details] = self::parseErrorBody($rawBody);

        if (in_array($statusCode, [400, 401, 403, 404, 422], true)) {
            return new PermanentRejectionException(
                sprintf('[%d] permanent rejection: %s', $statusCode, $error ?? 'request rejected'),
                $statusCode,
                $code,
                $error,
                $details,
                $correlationId,
                $rawBody,
            );
        }

        if ($statusCode === 503 && $code === self::NOT_PROCESSED && $apiVersion !== '2.0') {
            return new TransientFailureException(
                '[503] not processed — provably never dispatched; safe to fail over',
                $statusCode,
                $code,
                $error,
                $details,
                $correlationId,
                $rawBody,
            );
        }

        return new OutcomeUnknownException(
            sprintf('[%d] outcome unknown; reconcile before acting', $statusCode),
            $statusCode,
            $code,
            $error,
            $details,
            $correlationId,
            $rawBody,
        );
    }

    /**
     * Classifies a transport-level failure (no HTTP response was received). Never-sent
     * proof uses curl's own phase semantics via the STRUCTURED `errno` in Guzzle's
     * handler context; a rejection without a recognized errno carries no proof and
     * classifies OutcomeUnknown. Already-typed failures pass through unchanged.
     */
    public static function classifyTransportRejection(\Throwable $reason): RapCoreException
    {
        if ($reason instanceof RapCoreException) {
            return $reason;
        }

        $errno = self::curlErrno($reason);

        if ($errno !== null && in_array($errno, self::NEVER_SENT_CURL_ERRNOS, true)) {
            return new TransientFailureException(
                sprintf('request provably never sent (curl errno %d)', $errno),
                previous: $reason,
            );
        }

        if ($errno === self::CURLE_OPERATION_TIMEDOUT) {
            return new OutcomeUnknownException(
                'timeout: curl cannot prove the request was never sent (errno 28 covers both '
                    . 'connect-phase and after-send timeouts); reconcile before acting',
                previous: $reason,
            );
        }

        return new OutcomeUnknownException(
            sprintf(
                'transport failure without never-sent proof (%s); reconcile before acting',
                self::shortClass($reason),
            ),
            previous: $reason,
        );
    }

    /**
     * Reads `code`, `error`, and `details` from the raw error body. `code` is an OPEN
     * string straight off the wire. Anything unparseable is treated as absent (→ the
     * conservative branch).
     *
     * @return array{0: ?string, 1: ?string, 2: mixed}
     */
    public static function parseErrorBody(?string $rawBody): array
    {
        if ($rawBody === null || trim($rawBody) === '') {
            return [null, null, null];
        }

        $root = json_decode($rawBody, false);
        if (!is_object($root)) {
            return [null, null, null];
        }

        $code = isset($root->code) && is_string($root->code) ? $root->code : null;
        $error = isset($root->error) && is_string($root->error) ? $root->error : null;
        $details = $root->details ?? null;

        return [$code, $error, $details];
    }

    /** The structured curl errno from Guzzle's handler context, when the failure carries one. */
    private static function curlErrno(\Throwable $reason): ?int
    {
        if (!$reason instanceof ConnectException && !$reason instanceof RequestException) {
            return null;
        }

        $context = $reason->getHandlerContext();
        if (isset($context['errno']) && is_numeric($context['errno'])) {
            return (int) $context['errno'];
        }

        return null;
    }

    private static function shortClass(\Throwable $reason): string
    {
        $name = get_class($reason);
        $slash = strrpos($name, '\\');

        return $slash === false ? $name : substr($name, $slash + 1);
    }
}
