import * as SyntheticData from './SyntheticData';

/** @internal one scripted outcome: given the fetch init, produce a Response or fail like the wire would */
export type ScriptedOutcome = (init: RequestInit) => Promise<Response>;

/**
 * A scripted outcome queue for one stubbed operation. The scenario methods read as the
 * failover-contract taxonomy (DX contract §d): every §2 row has a method, and
 * consecutive outcomes can be scripted so merchants can test their
 * suppression/escalation logic. When the queue runs dry the LAST scripted outcome
 * repeats.
 *
 * Transport failures are simulated with the same structured error shapes Node's fetch
 * produces (`TypeError('fetch failed')` with a coded `cause`) — never message
 * strings — so classification in tests exercises the exact production code path.
 */
export class MockOperation {
    private readonly queue: ScriptedOutcome[] = [];

    /** @internal the next scripted outcome for this operation */
    next(): ScriptedOutcome {
        if (this.queue.length === 0) {
            throw new Error('mock: operation stubbed but no outcome scripted');
        }
        const item = this.queue.length > 1 ? this.queue.shift() : this.queue[0];
        return item as ScriptedOutcome;
    }

    // ---- success outcomes -------------------------------------------------------

    /** 200 with a synthetic approved transaction (`transactionStatus` 1). */
    returnsApproved(): this {
        return this.pushBody(200, SyntheticData.transaction(1));
    }

    /** 200 with a synthetic declined transaction (`transactionStatus` 2). */
    returnsDeclined(): this {
        return this.pushBody(200, SyntheticData.transaction(2));
    }

    /** 200 with a synthetic terminal-error transaction (`transactionStatus` 3). */
    returnsErrorOutcome(): this {
        return this.pushBody(200, SyntheticData.transaction(3));
    }

    /** 200 with a transaction carrying an unmapped `transactionStatus` (forward-compat drills). */
    returnsUnmappedStatus(transactionStatus: number): this {
        return this.pushBody(200, SyntheticData.transaction(transactionStatus));
    }

    /** 200 with the grouped envelope shape. */
    returnsTransactionGroup(): this {
        return this.pushBody(200, SyntheticData.transactionGroup());
    }

    // ---- PermanentRejection rows (§2) --------------------------------------------

    /** One of the §2 PermanentRejection statuses (400/401/403/404/422). */
    returnsPermanentRejection(status: number): this {
        return this.pushBody(status, SyntheticData.errorBody('synthetic rejection'));
    }

    // ---- TransientFailure rows (§2) ----------------------------------------------

    /** 503 + `code: not_processed` — the provable non-dispatch signal (immediate failover). */
    returnsNotProcessed503(): this {
        return this.pushBody(503, SyntheticData.errorBody('temporarily unable to process', 'not_processed'));
    }

    /**
     * Connection refused — provably never sent. Shaped exactly like Node's fetch:
     * `TypeError('fetch failed')` whose cause is the happy-eyeballs `AggregateError`
     * of per-address `ECONNREFUSED` failures.
     */
    throwsConnectionRefused(): this {
        const perAddress = codedError('Error', 'connect ECONNREFUSED 203.0.113.1:443 - synthetic', 'ECONNREFUSED');
        const aggregate = new AggregateError([perAddress], 'synthetic: connection refused');
        (aggregate as { code?: string }).code = 'ECONNREFUSED';
        return this.pushRejection(fetchFailed(aggregate));
    }

    /** DNS resolution failure (`ENOTFOUND`) — provably never sent. */
    throwsDnsFailure(): this {
        return this.pushRejection(
            fetchFailed(codedError('Error', 'getaddrinfo ENOTFOUND api.synthetic.invalid', 'ENOTFOUND')),
        );
    }

    /** TLS handshake failure (certificate verification) — provably never sent. */
    throwsSslHandshakeFailure(): this {
        return this.pushRejection(
            fetchFailed(codedError('Error', 'synthetic: self-signed certificate in chain', 'SELF_SIGNED_CERT_IN_CHAIN')),
        );
    }

    /**
     * Connect-phase timeout (`UND_ERR_CONNECT_TIMEOUT`). undici types this distinctly
     * from after-send timeouts, so — unlike the PHP runtime, whose curl errno 28
     * covers both phases — it carries never-sent proof and classifies
     * TransientFailure.
     */
    throwsConnectTimeout(): this {
        return this.pushRejection(
            fetchFailed(codedError('ConnectTimeoutError', 'synthetic: connect timeout', 'UND_ERR_CONNECT_TIMEOUT')),
        );
    }

    // ---- OutcomeUnknown rows (§2) ------------------------------------------------

    /** Bare 503 (no `code`) — may have been dispatched: OutcomeUnknown. */
    returnsBare503(): this {
        return this.pushBody(503, SyntheticData.errorBody('service unavailable'));
    }

    /** 503 with an unrecognized `code` — treated as absent: OutcomeUnknown. */
    returnsUnknownCode503(code: string): this {
        return this.pushBody(503, SyntheticData.errorBody('service unavailable', code));
    }

    /** 500 internal error — OutcomeUnknown. */
    returnsServerError(): this {
        return this.pushBody(500, SyntheticData.errorBody('internal error', 'outcome_unknown'));
    }

    /** 502 (edge) — OutcomeUnknown. */
    returnsBadGateway(): this {
        return this.pushBody(502, SyntheticData.errorBody('bad gateway'));
    }

    /** 504 (edge) — OutcomeUnknown. */
    returnsGatewayTimeout(): this {
        return this.pushBody(504, SyntheticData.errorBody('gateway timeout'));
    }

    /**
     * Response-phase timeout after the request was sent (`UND_ERR_HEADERS_TIMEOUT`) —
     * no never-sent proof: OutcomeUnknown.
     */
    throwsTimeoutAfterSend(): this {
        return this.pushRejection(
            fetchFailed(codedError('HeadersTimeoutError', 'synthetic: headers timeout', 'UND_ERR_HEADERS_TIMEOUT')),
        );
    }

    /** Connection reset mid-flight (`ECONNRESET`, no response) — OutcomeUnknown. */
    throwsConnectionReset(): this {
        return this.pushRejection(
            fetchFailed(codedError('SocketError', 'synthetic: read ECONNRESET', 'ECONNRESET')),
        );
    }

    /**
     * Never responds; rejects with the abort reason once the request's signal fires —
     * exactly like real fetch under the runtime's overall deadline (or a caller
     * abort). Script it with a small `overallDeadlineMs` to exercise the
     * deadline-after-send → OutcomeUnknown path end to end.
     */
    hangsUntilAborted(): this {
        this.queue.push(
            (init) =>
                new Promise<Response>((_resolve, reject) => {
                    const signal = init.signal;
                    if (signal == null) {
                        reject(new Error('mock: hangsUntilAborted() needs a deadline or caller signal to fire'));
                        return;
                    }
                    if (signal.aborted) {
                        // eslint-disable-next-line @typescript-eslint/prefer-promise-reject-errors -- mirrors real fetch exactly: the abort reason surfaces VERBATIM (it can be any value), so the transport's caller-cancellation path is exercised unaltered
                        reject(abortReason(signal));
                        return;
                    }
                    // eslint-disable-next-line @typescript-eslint/prefer-promise-reject-errors -- mirrors real fetch exactly: the abort reason surfaces VERBATIM (it can be any value), so the transport's caller-cancellation path is exercised unaltered
                    signal.addEventListener('abort', () => reject(abortReason(signal)), { once: true });
                }),
        );
        return this;
    }

    // ---- reconcile scripting (§3) ------------------------------------------------

    /** 404 not-visible-yet, `times` in a row (then the next scripted outcome). */
    notFoundYet(times = 1): this {
        for (let i = 0; i < times; i++) {
            this.pushBody(404, SyntheticData.errorBody('transaction not found'));
        }
        return this;
    }

    /** 200 pending intent (post-P-2 shape). */
    pending(): this {
        return this.pushBody(200, SyntheticData.pending());
    }

    /** Then a 200 approved terminal record (chain after notFoundYet()/pending()). */
    thenFoundApproved(): this {
        return this.returnsApproved();
    }

    /** Then a 200 declined terminal record (chain after notFoundYet()/pending()). */
    thenFoundDeclined(): this {
        return this.returnsDeclined();
    }

    // ---- raw escapes -------------------------------------------------------------

    /**
     * A raw scripted response. The synthetic correlation id and JSON content type are
     * always present unless overridden.
     */
    returns(status: number, body: string, headers: Record<string, string> = {}): this {
        return this.pushBody(status, body, headers);
    }

    /** A raw scripted transport failure (rejected without a response). */
    throwsIo(failure: unknown): this {
        // eslint-disable-next-line @typescript-eslint/prefer-promise-reject-errors -- documented raw escape: merchants script arbitrary rejection SHAPES (classification is structural, failover-contract §2), so the value is deliberately unconstrained
        this.queue.push(() => Promise.reject(failure));
        return this;
    }

    private pushBody(status: number, body: string, extraHeaders: Record<string, string> = {}): this {
        const headers = {
            'Content-Type': 'application/json',
            'X-Correlation-ID': SyntheticData.DEFAULT_CORRELATION_ID,
            'api-supported-versions': '2.0, 2.1',
            ...extraHeaders,
        };
        this.queue.push(() => Promise.resolve(new Response(body, { status, headers })));
        return this;
    }

    private pushRejection(failure: Error): this {
        this.queue.push(() => Promise.reject(failure));
        return this;
    }
}

/** The exact rejection shape of Node's fetch: `TypeError('fetch failed')` with the real failure as `cause`. */
function fetchFailed(cause: Error): TypeError {
    return new TypeError('fetch failed', { cause });
}

function codedError(name: string, message: string, code: string): Error {
    const error = new Error(message);
    error.name = name;
    (error as { code?: string }).code = code;
    return error;
}

function abortReason(signal: AbortSignal): unknown {
    return signal.reason ?? new DOMException('This operation was aborted', 'AbortError');
}
