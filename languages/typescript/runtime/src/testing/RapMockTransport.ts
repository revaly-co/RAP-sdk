import { PRODUCT_NAME } from '../transport/RapUserAgent';
import { USER_AGENT } from '../transport/RapHeaders';
import { MockOperation } from './MockOperation';
import { RecordedRequest } from './RecordedRequest';

/**
 * The first-class no-network test double (DX contract §d; runtime-tdd §8): a fetch
 * replacement that scripts every row of the failover-contract §2 table and both §3
 * verdicts, so a merchant can unit-test their failover handler with no network.
 *
 * Pass it as the client's `transport`:
 *
 * ```ts
 * const mock = new RapMockTransport();
 * mock.charge().returnsNotProcessed503();
 * const client = new RapClient({ apiKey: 'sk-synthetic', transport: mock });
 * ```
 *
 * Every request is recorded ({@link requests}) and asserted to carry the SDK
 * User-Agent (ADR-SDK-005) — the mock sits where the wire would be, below the
 * runtime's header injection, so it sees exactly what the network would.
 */
export class RapMockTransport {
    private readonly stubs: Array<{ method: string; prefix: string; operation: MockOperation }> = [];
    private readonly recorded: RecordedRequest[] = [];
    private assertUserAgent = true;

    /** Disables the User-Agent presence assertion (for tests of the assertion itself). */
    withoutUserAgentAssertion(): this {
        this.assertUserAgent = false;
        return this;
    }

    /** Every request this transport has served, in order. */
    get requests(): readonly RecordedRequest[] {
        return this.recorded;
    }

    /** Stubs `POST /payments` (charge). */
    charge(): MockOperation {
        return this.stub('POST', '/payments');
    }

    /** Stubs `POST /payments/authorize`. */
    authorize(): MockOperation {
        return this.stub('POST', '/payments/authorize');
    }

    /** Stubs the reconcile GET for one merchantTransactionId. */
    reconcile(merchantTransactionId: string): MockOperation {
        return this.stub('GET', `/transactions/merchant/${encodeURIComponent(merchantTransactionId)}`);
    }

    /** Stubs an arbitrary method + path prefix; the longest matching prefix wins. */
    stub(method: string, pathPrefix: string): MockOperation {
        const operation = new MockOperation();
        this.stubs.push({ method: method.toUpperCase(), prefix: pathPrefix, operation });
        return operation;
    }

    /** The fetch contract — what the client's `transport` option consumes. */
    async fetch(input: string | URL | Request, init: RequestInit = {}): Promise<Response> {
        if (init.signal?.aborted) {
            // Real fetch rejects an already-aborted call before any network activity —
            // so the request is neither dispatched nor recorded.
            throw init.signal.reason ?? new DOMException('This operation was aborted', 'AbortError');
        }

        const request = RecordedRequest.from(input, init);
        this.recorded.push(request);

        if (this.assertUserAgent) {
            const userAgent = request.headers.get(USER_AGENT) ?? '';
            if (!userAgent.startsWith(`${PRODUCT_NAME}/`)) {
                throw new Error(
                    `mock: request is missing the SDK User-Agent (ADR-SDK-005); got "${userAgent}"`,
                );
            }
        }

        const operation = this.match(request.method, request.path);
        if (operation === undefined) {
            throw new Error(`mock: no stub for ${request.method} ${request.path}`);
        }

        return operation.next()(init);
    }

    private match(method: string, path: string): MockOperation | undefined {
        let best: MockOperation | undefined;
        let bestLength = -1;
        for (const stub of this.stubs) {
            if (stub.method !== method || !path.startsWith(stub.prefix)) {
                continue;
            }
            if (stub.prefix.length > bestLength) {
                best = stub.operation;
                bestLength = stub.prefix.length;
            }
        }
        return best;
    }
}
