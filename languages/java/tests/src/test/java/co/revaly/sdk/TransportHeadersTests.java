package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import co.revaly.sdk.reconcile.ReconcilePolicy;
import co.revaly.sdk.testing.RapMockTransport;
import co.revaly.sdk.testing.RecordedRequest;
import co.revaly.sdk.transport.RapUserAgent;
import java.time.Duration;
import java.util.regex.Pattern;
import org.junit.jupiter.api.Test;

/** ADR-SDK-005 User-Agent grammar + the runtime-owned auth and version headers. */
class TransportHeadersTests {

    private static final Pattern UA_GRAMMAR =
            Pattern.compile(
                    "^revaly-sdk-java/\\d+\\.\\d+\\.\\d+ \\(OpenJDK \\d+; (linux|windows|darwin|other)\\)$");

    @Test
    void userAgentMatchesTheNormativeGrammarExactly() {
        assertTrue(
                UA_GRAMMAR.matcher(RapUserAgent.VALUE).matches(),
                "contract with platform dashboards; saw '" + RapUserAgent.VALUE + "'");
        assertEquals("revaly-sdk-java", RapUserAgent.PRODUCT_NAME);
    }

    @Test
    void everyChargeCarriesTheExactUserAgent() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsApproved();
        RapClient client = TestClient.client(mock);

        client.charge(TestClient.paymentRequest());

        RecordedRequest request = mock.getRequests().get(0);
        assertEquals(RapUserAgent.VALUE, request.getHeaders().get("User-Agent"));
    }

    @Test
    void reconcileGetsCarryTheSameTransportHeaders() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).thenFoundApproved();
        RapClient client = TestClient.client(mock);

        client.reconcile(
                TestClient.MTX, new ReconcilePolicy(1, Duration.ofSeconds(1), Duration.ZERO));

        RecordedRequest request = mock.getRequests().get(0);
        assertEquals(RapUserAgent.VALUE, request.getHeaders().get("User-Agent"));
        assertEquals("ApiKey " + TestClient.API_KEY, request.getHeaders().get("Authorization"));
        assertEquals("2.1", request.getHeaders().get("X-Api-Version"));
    }

    @Test
    void merchantTokenAppendsAfterTheSdkTokenNeverReplacing() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsApproved();
        RapClient client =
                RapClient.builder()
                        .apiKey(TestClient.API_KEY)
                        .baseUrl("https://sandbox.synthetic.test")
                        .userAgentSuffix("acme-shop/2.0")
                        .transport(mock)
                        .build();

        client.charge(TestClient.paymentRequest());

        String userAgent = mock.getRequests().get(0).getHeaders().get("User-Agent");
        assertEquals(RapUserAgent.VALUE + " acme-shop/2.0", userAgent);
        assertTrue(userAgent.startsWith(RapUserAgent.PRODUCT_NAME + "/"));
    }

    @Test
    void authorizationUsesTheApiKeySchemeNotBearer() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsApproved();
        RapClient client = TestClient.client(mock);

        client.charge(TestClient.paymentRequest());

        String authorization = mock.getRequests().get(0).getHeaders().get("Authorization");
        assertEquals("ApiKey " + TestClient.API_KEY, authorization);
    }

    @Test
    void apiVersionPinDefaultsTo21AndIsSelectable() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsApproved();
        TestClient.client(mock).charge(TestClient.paymentRequest());
        assertEquals("2.1", mock.getRequests().get(0).getHeaders().get("X-Api-Version"));

        RapMockTransport mock20 = new RapMockTransport();
        mock20.charge().returnsApproved();
        TestClient.client(mock20, "2.0").charge(TestClient.paymentRequest());
        assertEquals("2.0", mock20.getRequests().get(0).getHeaders().get("X-Api-Version"));
    }
}
