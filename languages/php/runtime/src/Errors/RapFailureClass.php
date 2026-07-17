<?php

declare(strict_types=1);

namespace Revaly\Sdk\Errors;

/**
 * The three failure classes of failover-contract.md §2. The class — never the message
 * text, never latency — is what licenses (or forbids) failover.
 */
enum RapFailureClass: string
{
    /** Received and rejected. Fix or decline. Never fail over — the same request fails anywhere. */
    case PermanentRejection = 'PermanentRejection';

    /** Definitively not processed. Safe to route to your own gateway immediately. */
    case TransientFailure = 'TransientFailure';

    /** May have been processed. Reconcile before acting — failing over blind can double-charge. */
    case OutcomeUnknown = 'OutcomeUnknown';
}
