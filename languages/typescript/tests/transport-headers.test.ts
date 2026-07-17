import { readFileSync } from 'node:fs';
import { describe, expect, test } from 'vitest';
import { RapMockTransport, RapOutcomeUnknown, SDK_VERSION } from '../runtime/src/index';
import { mockedClient, SYNTHETIC_API_KEY, syntheticCardPayment } from './support/TestClients';

/**
 * Transport-level injection (runtime-tdd §5): auth scheme, User-Agent grammar
 * (ADR-SDK-005), and the X-Api-Version pin — all set where the core cannot bypass
 * them, all visible to the mock exactly as the wire would see them.
 */

async function firstRequest(mock: RapMockTransport, overrides = {}) {
    mock.charge().returnsApproved();
    await mockedClient(mock, overrides).charge(syntheticCardPayment());
    expect(mock.requests.length).toBeGreaterThan(0);
    return mock.requests[0]!;
}

describe('Authorization', () => {
    test('sends `ApiKey <key>` — the mandatory scheme prefix, not Bearer', async () => {
        const request = await firstRequest(new RapMockTransport());
        expect(request.headers.get('Authorization')).toBe(`ApiKey ${SYNTHETIC_API_KEY}`);
    });

    test('the API key is never placed on the core Configuration', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const client = mockedClient(mock);
        await client.charge(syntheticCardPayment());

        const coreConfiguration = (client.payments as unknown as { configuration: { apiKey?: unknown } })
            .configuration;
        expect(coreConfiguration.apiKey).toBeUndefined();
    });
});

describe('User-Agent (ADR-SDK-005)', () => {
    test('matches the normative grammar', async () => {
        const request = await firstRequest(new RapMockTransport());
        expect(request.headers.get('User-Agent')).toMatch(
            /^revaly-sdk-typescript\/\d+\.\d+\.\d+ \(node \d+\.\d+; (windows|linux|darwin|other)\)$/,
        );
    });

    test('carries the package version', async () => {
        const request = await firstRequest(new RapMockTransport());
        expect(request.headers.get('User-Agent')).toContain(`revaly-sdk-typescript/${SDK_VERSION}`);
    });

    test('SDK_VERSION stays in sync with package.json', () => {
        const packageJson = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8')) as {
            version: string;
        };
        expect(SDK_VERSION).toBe(packageJson.version);
    });

    test('a merchant token is APPENDED after the SDK token, never in front', async () => {
        const request = await firstRequest(new RapMockTransport(), { userAgentSuffix: 'acme-checkout/2.3' });
        const userAgent = request.headers.get('User-Agent')!;
        expect(userAgent.startsWith('revaly-sdk-typescript/')).toBe(true);
        expect(userAgent.endsWith(' acme-checkout/2.3')).toBe(true);
    });

    test('the mock transport asserts User-Agent presence for merchant tests', async () => {
        const bare = new RapMockTransport();
        bare.charge().returnsApproved();
        // Calling the mock's fetch without the runtime in front (no UA header) trips the guard.
        await expect(bare.fetch('https://api.revaly.co/payments', { method: 'POST' })).rejects.toThrow(
            'missing the SDK User-Agent',
        );
    });
});

describe('X-Api-Version pin (runtime-tdd §1)', () => {
    test('defaults to 2.1 on every request', async () => {
        const request = await firstRequest(new RapMockTransport());
        expect(request.headers.get('X-Api-Version')).toBe('2.1');
    });

    test('honors the configured version', async () => {
        const request = await firstRequest(new RapMockTransport(), { apiVersion: '2.0' });
        expect(request.headers.get('X-Api-Version')).toBe('2.0');
    });

    test('an explicit per-call version through the generated api wins over the pin', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const client = mockedClient(mock);
        await client.payments.chargePayment({ paymentRequest: syntheticCardPayment(), xApiVersion: '2.0' });

        expect(mock.requests[0]!.headers.get('X-Api-Version')).toBe('2.0');
    });
});

describe('transport shape', () => {
    test('requests never follow redirects (redirect: manual)', async () => {
        let observedRedirect: string | undefined;
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const client = mockedClient(mock, {
            transport: (input, init) => {
                observedRedirect = init?.redirect;
                return mock.fetch(input, init ?? {});
            },
        });
        await client.charge(syntheticCardPayment());

        expect(observedRedirect).toBe('manual');
    });

    test('a plain fetch-compatible function works as the transport', async () => {
        const client = mockedClient(new RapMockTransport(), {
            transport: () =>
                Promise.resolve(
                    new Response(JSON.stringify({ error: 'service unavailable' }), {
                        status: 503,
                        headers: { 'Content-Type': 'application/json' },
                    }),
                ),
        });

        await expect(client.charge(syntheticCardPayment())).rejects.toBeInstanceOf(RapOutcomeUnknown);
    });

    test('the dispatcher passthrough reaches the wire call', async () => {
        const dispatcher = { synthetic: true };
        let observed: unknown;
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const client = mockedClient(mock, {
            dispatcher,
            transport: (input, init) => {
                observed = (init as Record<string, unknown> | undefined)?.['dispatcher'];
                return mock.fetch(input, init ?? {});
            },
        });
        await client.charge(syntheticCardPayment());

        expect(observed).toBe(dispatcher);
    });

    test('correlation id from the response lands on the typed error', async () => {
        const mock = new RapMockTransport();
        mock.charge().returns(500, JSON.stringify({ error: 'boom' }), {
            'X-Correlation-ID': 'corr-numbered-42',
        });

        await expect(mockedClient(mock).charge(syntheticCardPayment())).rejects.toMatchObject({
            correlationId: 'corr-numbered-42',
        });
    });
});

describe('client construction', () => {
    test.each([
        [{ apiKey: '' }, 'apiKey is required'],
        [{ apiKey: 'sk-x', baseUrl: '/' }, 'baseUrl is required'],
        [{ apiKey: 'sk-x', apiVersion: ' ' }, 'apiVersion is required'],
        [{ apiKey: 'sk-x', overallDeadlineMs: 0 }, 'overallDeadlineMs must be positive'],
    ])('rejects invalid config %j', (config, message) => {
        expect(() => mockedClient(new RapMockTransport(), config)).toThrow(message);
    });

    test('trailing slashes on baseUrl are trimmed', async () => {
        const mock = new RapMockTransport();
        mock.charge().returnsApproved();
        const client = mockedClient(mock, { baseUrl: 'https://api.revaly.co///' });
        await client.charge(syntheticCardPayment());

        expect(mock.requests[0]!.url).toBe('https://api.revaly.co/payments');
    });
});
