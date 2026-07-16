package co.revaly.sdk;

import co.revaly.sdk.core.model.PaymentRequest;
import co.revaly.sdk.testing.RapMockTransport;
import java.time.Duration;

/** Shared test wiring: a mock-backed client with synthetic-only configuration. */
final class TestClient {

    static final String API_KEY = "test-key-synthetic";
    static final String MTX = "mtx-synthetic-1";

    private TestClient() {}

    static RapClient client(RapMockTransport mock) {
        return client(mock, "2.1");
    }

    static RapClient client(RapMockTransport mock, String apiVersion) {
        return RapClient.builder()
                .apiKey(API_KEY)
                .baseUrl("https://sandbox.synthetic.test")
                .apiVersion(apiVersion)
                .overallDeadline(Duration.ofSeconds(5))
                .transport(mock)
                .build();
    }

    static PaymentRequest paymentRequest() {
        return new PaymentRequest().merchantTransactionId(MTX);
    }
}
