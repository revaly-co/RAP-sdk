import type { PaymentRequest, RapClientConfig } from '../../runtime/src/index';
import { RapClient, RapMockTransport } from '../../runtime/src/index';

/** The synthetic merchant API key used across the suite (never a real credential). */
export const SYNTHETIC_API_KEY = 'sk-synthetic-test-key-1';

/** The Visa test PAN — synthetic data only (ADR-SDK-020). */
export const SYNTHETIC_PAN = '4111111111111111';
export const SYNTHETIC_CVV = '999';

/** A full card payment request, with every sensitive field carrying an obvious synthetic value. */
export function syntheticCardPayment(merchantTransactionId = 'mtx-synthetic-1'): PaymentRequest {
    return {
        amount: 1999,
        currency: 'USD',
        merchantTransactionId,
        paymentMethodType: 'creditCard',
        paymentMethod: {
            firstName: 'Sandbox',
            lastName: 'Shopper',
            email: 'shopper@example.test',
            creditCard: {
                number: SYNTHETIC_PAN,
                cardVerificationCode: SYNTHETIC_CVV,
                expiryMonth: '12',
                expiryYear: '2030',
            },
        },
    };
}

/** A client wired to the given mock transport (config overridable per test). */
export function mockedClient(mock: RapMockTransport, overrides: Partial<RapClientConfig> = {}): RapClient {
    return new RapClient({
        apiKey: SYNTHETIC_API_KEY,
        transport: mock,
        ...overrides,
    });
}
