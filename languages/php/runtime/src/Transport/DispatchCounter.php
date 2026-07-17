<?php

declare(strict_types=1);

namespace Revaly\Sdk\Transport;

/**
 * Counts requests as they pass the transport middleware. Lets the runtime distinguish a
 * failure raised BEFORE dispatch (a caller error from the core's request validation)
 * from one raised AFTER a response was received (e.g. the core failing to deserialize a
 * 2xx body) — only the latter may classify as OutcomeUnknown. One client per
 * configuration; PHP's request-per-process model needs no cross-thread guard.
 *
 * @internal
 */
final class DispatchCounter
{
    public int $count = 0;
}
