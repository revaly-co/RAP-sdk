<?php

declare(strict_types=1);

namespace Revaly\Sdk\Errors;

/**
 * Definitively not processed — safe to fail over immediately (failover-contract §2).
 * Raised only on client-provable never-sent transport failures (DNS, TCP connect, TLS
 * handshake — proven by the transport's own phase semantics), on `503` with
 * `code: not_processed` (the platform's provable non-dispatch signal, P-1), and on a
 * `403` blocked at the edge firewall whose body carries `details.edgeRejection: true`
 * ({@see isEdgeRejection()}, ADR-SDK-033).
 */
final class TransientFailureException extends RapCoreException
{
    public function getFailureClass(): RapFailureClass
    {
        return RapFailureClass::TransientFailure;
    }
}
