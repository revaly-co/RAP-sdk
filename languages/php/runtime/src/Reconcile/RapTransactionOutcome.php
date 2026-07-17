<?php

declare(strict_types=1);

namespace Revaly\Sdk\Reconcile;

/**
 * The terminal-or-pending outcome carried by a {@see Found} reconcile verdict. Mapped
 * from the wire's `transactionStatus` (1/2/3) or the pending `state` discriminator;
 * anything unrecognized maps to {@see Unknown} — always branch with a default
 * (runtime-tdd §4: verdicts and outcomes are open for extension).
 */
enum RapTransactionOutcome: string
{
    /** The payment succeeded at RAP-core. Failing over now would double-charge. */
    case Approved = 'Approved';

    /** Terminal decline — your own gateway is now safe, per your risk policy (§3). */
    case Declined = 'Declined';

    /** Terminal error recorded at RAP-core — merchant decision, as with a decline. */
    case Error = 'Error';

    /**
     * A pending payment intent (post-P-2 surface): the platform accepted the payment
     * but no transaction record is visible yet. Hold and re-poll.
     */
    case Pending = 'Pending';

    /**
     * Found, but this SDK version cannot map the record (new status value, envelope
     * shape, or post-P-2 variant). A sighting is still a sighting — treat
     * conservatively; do not fail over on Unknown.
     */
    case Unknown = 'Unknown';
}
