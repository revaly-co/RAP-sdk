/**
 * One request observed by the mock transport, exactly as the wire would have seen it
 * (below the runtime's header injection).
 */
export class RecordedRequest {
    constructor(
        readonly method: string,
        readonly url: string,
        readonly path: string,
        readonly headers: Headers,
        readonly bodyText: string | undefined,
    ) {}

    static from(input: RequestInfo | URL, init: RequestInit): RecordedRequest {
        const url = typeof input === 'string' ? input : input instanceof URL ? input.toString() : input.url;
        return new RecordedRequest(
            (init.method ?? 'GET').toUpperCase(),
            url,
            new URL(url).pathname,
            new Headers(init.headers ?? undefined),
            typeof init.body === 'string' ? init.body : undefined,
        );
    }
}
