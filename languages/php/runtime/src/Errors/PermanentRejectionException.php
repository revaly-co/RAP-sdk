<?php

declare(strict_types=1);

namespace Revaly\Sdk\Errors;

/**
 * HTTP 400/401/403/404/422: received and rejected — the payment did not and will not
 * happen from this request. Fix the request or decline. NEVER fail over: the same
 * request fails at any gateway (failover-contract §2).
 */
final class PermanentRejectionException extends RapCoreException
{
    public function getFailureClass(): RapFailureClass
    {
        return RapFailureClass::PermanentRejection;
    }
}
