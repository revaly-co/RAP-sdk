<?php

declare(strict_types=1);

namespace Revaly\Sdk\Errors;

/**
 * The payment MAY have been processed — reconcile before acting (failover-contract §3).
 * Failing over on OutcomeUnknown without reconciling risks charging the cardholder
 * twice. Use {@see \Revaly\Sdk\RapClient::reconcile()}.
 */
final class OutcomeUnknownException extends RapCoreException
{
    public function getFailureClass(): RapFailureClass
    {
        return RapFailureClass::OutcomeUnknown;
    }
}
