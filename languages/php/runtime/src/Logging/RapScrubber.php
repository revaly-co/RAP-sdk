<?php

declare(strict_types=1);

namespace Revaly\Sdk\Logging;

use Revaly\Sdk\Transport\RapHeaders;

/**
 * The single central scrub function of this runtime (ADR-SDK-020): applied to debug
 * logs, wire traces, and any payload surface the SDK emits. Scrubbing is by ALLOWLIST —
 * only known-safe identifier/status fields are emitted verbatim; every other scalar is
 * replaced with `[scrubbed]`, so schema evolution fails safe. PAN/CVV/PII can never
 * appear because card and customer fields are simply not on the list. API keys are
 * additionally redacted at the header layer.
 */
final class RapScrubber
{
    /** The replacement token for scrubbed scalar values. */
    public const SCRUBBED = '[scrubbed]';

    /** The replacement token for redacted header values. */
    public const REDACTED = '[redacted]';

    /**
     * Known-safe fields: identifiers, statuses and routing metadata designed for
     * support tickets and telemetry joins. Deliberately absent: every cardholder,
     * customer, address and amount field. Extending this list is a reviewed change to
     * the runtime's PCI posture — never add payload value fields. (Lowercased for
     * case-insensitive lookup.)
     */
    private const FIELD_ALLOWLIST = [
        'transactionid' => true,
        'merchanttransactionid' => true,
        'transactiontype' => true,
        'transactionstatus' => true,
        'transactiondate' => true,
        'responsecode' => true,
        'code' => true,
        'error' => true,
        'currency' => true,
        'gatewaytype' => true,
        'gatewaytransactionid' => true,
        'gatewayroutingid' => true,
        'correlationid' => true,
        'status' => true,
        'state' => true,
        'attempts' => true,
    ];

    /**
     * Known-safe headers. Authorization is never emitted, even redacted-by-length — the
     * merchant API key must not leak shape or presence into logs (ADR-SDK-020).
     * (Lowercased for case-insensitive lookup.)
     */
    private const HEADER_ALLOWLIST = [
        'content-type' => true,
        'content-length' => true,
        'user-agent' => true,
        'x-api-version' => true,
        'x-correlation-id' => true,
        'api-supported-versions' => true,
    ];

    private function __construct()
    {
    }

    /**
     * Scrubs a JSON payload: allowlisted scalar fields pass through verbatim, all other
     * scalars are replaced with {@see SCRUBBED}; object/array structure is preserved.
     * Non-JSON input returns a fixed placeholder (never the raw text).
     */
    public static function scrubJson(?string $payload): string
    {
        if ($payload === null || trim($payload) === '') {
            return '';
        }

        $root = json_decode($payload, false);
        if ($root === null && strtolower(trim($payload)) !== 'null') {
            return '[unparseable:scrubbed]';
        }

        $scrubbed = self::scrubNode($root, false);
        $encoded = json_encode($scrubbed);

        return $encoded === false ? self::SCRUBBED : $encoded;
    }

    /**
     * Scrubs an HTTP header set for tracing: allowlisted headers pass through,
     * everything else (including Authorization) becomes {@see REDACTED}. User-Agent is
     * a space-separated product-token list on the wire; other multi-valued headers join
     * with commas per RFC 9110.
     *
     * @param array<string, array<string>|string>|null $headers
     * @return array<string, string>
     */
    public static function scrubHeaders(?array $headers): array
    {
        $result = [];
        if ($headers === null) {
            return $result;
        }

        foreach ($headers as $name => $values) {
            if (!is_string($name)) {
                continue;
            }
            $values = is_array($values) ? array_values($values) : [$values];
            if (isset(self::HEADER_ALLOWLIST[strtolower($name)])) {
                $separator = strcasecmp($name, RapHeaders::USER_AGENT) === 0 ? ' ' : ', ';
                $result[$name] = implode($separator, array_map('strval', $values));
            } else {
                $result[$name] = self::REDACTED;
            }
        }

        ksort($result, SORT_FLAG_CASE | SORT_STRING);

        return $result;
    }

    private static function scrubNode(mixed $node, bool $parentKeyAllowlisted): mixed
    {
        if (is_object($node)) {
            $scrubbed = new \stdClass();
            foreach (get_object_vars($node) as $key => $child) {
                $allowlisted = isset(self::FIELD_ALLOWLIST[strtolower((string) $key)]);
                if (is_object($child) || is_array($child)) {
                    $scrubbed->{$key} = self::scrubNode($child, $allowlisted);
                } else {
                    $scrubbed->{$key} = $allowlisted ? $child : self::SCRUBBED;
                }
            }

            return $scrubbed;
        }

        if (is_array($node)) {
            $scrubbed = [];
            foreach ($node as $element) {
                if (is_object($element) || is_array($element)) {
                    // Scalars inside arrays keep only their parent key's status.
                    $scrubbed[] = self::scrubNode($element, $parentKeyAllowlisted);
                } else {
                    $scrubbed[] = $parentKeyAllowlisted ? $element : self::SCRUBBED;
                }
            }

            return $scrubbed;
        }

        // Bare scalar root.
        return $parentKeyAllowlisted ? $node : self::SCRUBBED;
    }
}
