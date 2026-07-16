package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import co.revaly.sdk.errors.RapCoreException;
import co.revaly.sdk.logging.RapWireTrace;
import co.revaly.sdk.testing.RapMockTransport;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;

/**
 * The ADR-SDK-020 / DX-contract §c CI log-capture obligations: values-free default output,
 * allowlist-scrubbed debug output, API keys nowhere, correlation id on every error path, and a
 * scrubbed-only wire-trace hook.
 */
class LogCaptureTests {

    private static final String SENSITIVE_DESCRIPTION = "SENSITIVE-DESC-4111111111111111";

    /** Captures everything logged under the SDK's logger namespace at the given level. */
    private static final class CapturedLogs implements AutoCloseable {
        private final Logger logger;
        private final ListAppender<ILoggingEvent> appender = new ListAppender<>();
        private final Level previousLevel;

        CapturedLogs(Level level) {
            logger = (Logger) LoggerFactory.getLogger("co.revaly.sdk");
            previousLevel = logger.getLevel();
            logger.setLevel(level);
            appender.start();
            logger.addAppender(appender);
        }

        String all() {
            return appender.list.stream()
                    .map(ILoggingEvent::getFormattedMessage)
                    .collect(Collectors.joining("\n"));
        }

        @Override
        public void close() {
            logger.detachAppender(appender);
            logger.setLevel(previousLevel);
        }
    }

    @Test
    void defaultLevelEmitsNoPayloadValues() throws Exception {
        try (CapturedLogs logs = new CapturedLogs(Level.INFO)) {
            RapMockTransport mock = new RapMockTransport();
            mock.charge().returnsApproved();
            RapClient client = TestClient.client(mock);

            client.charge(TestClient.paymentRequest().description(SENSITIVE_DESCRIPTION));

            String all = logs.all();
            assertTrue(all.contains("rap.request"), "the SDK does log its request line");
            assertTrue(all.contains("mock-corr-1"), "correlation id is safe metadata");
            assertFalse(all.contains(SENSITIVE_DESCRIPTION), "no payload values at default level");
            assertFalse(all.contains("4111"), "nothing PAN-shaped at default level");
        }
    }

    @Test
    void debugLevelEmitsOnlyAllowlistScrubbedPayloads() throws Exception {
        try (CapturedLogs logs = new CapturedLogs(Level.DEBUG)) {
            RapMockTransport mock = new RapMockTransport();
            mock.charge().returnsApproved();
            RapClient client = TestClient.client(mock);

            client.charge(TestClient.paymentRequest().description(SENSITIVE_DESCRIPTION));

            String all = logs.all();
            assertTrue(all.contains("rap.request payload"), "debug adds the payload line");
            assertTrue(all.contains("[scrubbed]"), "non-allowlisted scalars are masked");
            assertTrue(all.contains(TestClient.MTX), "allowlisted identifiers pass through");
            assertFalse(all.contains(SENSITIVE_DESCRIPTION), "debug is scrubbed, not raw");
        }
    }

    @Test
    void apiKeyNeverAppearsInLogsAtAnyLevel() throws Exception {
        try (CapturedLogs logs = new CapturedLogs(Level.DEBUG)) {
            RapMockTransport mock = new RapMockTransport();
            mock.charge().returnsBare503().thenFoundApproved();
            RapClient client = TestClient.client(mock);

            assertThrows(RapCoreException.class, () -> client.charge(TestClient.paymentRequest()));
            client.charge(TestClient.paymentRequest());

            assertFalse(logs.all().contains(TestClient.API_KEY));
        }
    }

    @Test
    void everyErrorPathLogsClassAndCorrelation() throws Exception {
        try (CapturedLogs logs = new CapturedLogs(Level.INFO)) {
            RapMockTransport mock = new RapMockTransport();
            mock.charge().returnsBare503();
            RapClient client = TestClient.client(mock);

            assertThrows(RapCoreException.class, () -> client.charge(TestClient.paymentRequest()));

            String all = logs.all();
            assertTrue(all.contains("class=OUTCOME_UNKNOWN"));
            assertTrue(all.contains("mock-corr-1"));
        }
    }

    @Test
    void typedErrorToStringNeverCarriesKeyOrBody() {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsNotProcessed503();
        RapClient client = TestClient.client(mock);

        RapCoreException e =
                assertThrows(
                        RapCoreException.class, () -> client.charge(TestClient.paymentRequest()));
        assertFalse(e.toString().contains(TestClient.API_KEY));
        assertFalse(e.toString().contains("platform breaker open"));
    }

    @Test
    void wireTraceHookReceivesOnlyScrubbedMaterial() throws Exception {
        List<RapWireTrace> traces = new ArrayList<>();
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsApproved();
        RapClient client =
                RapClient.builder()
                        .apiKey(TestClient.API_KEY)
                        .baseUrl("https://sandbox.synthetic.test")
                        .wireTraceHook(traces::add)
                        .transport(mock)
                        .build();

        client.charge(TestClient.paymentRequest().description(SENSITIVE_DESCRIPTION));

        assertEquals(1, traces.size());
        RapWireTrace trace = traces.get(0);
        assertEquals("charge", trace.getOperation());
        assertNotNull(trace.getRequestBody());
        assertTrue(trace.getRequestBody().contains("[scrubbed]"));
        assertFalse(trace.getRequestBody().contains(SENSITIVE_DESCRIPTION));
        assertTrue(trace.getRequestBody().contains(TestClient.MTX));
    }

    @Test
    void wireTraceObserverExceptionsAreSwallowed() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.charge().returnsApproved();
        RapClient client =
                RapClient.builder()
                        .apiKey(TestClient.API_KEY)
                        .baseUrl("https://sandbox.synthetic.test")
                        .wireTraceHook(
                                trace -> {
                                    throw new IllegalStateException("observer bug");
                                })
                        .transport(mock)
                        .build();

        assertEquals(1, client.charge(TestClient.paymentRequest()).getTransactionStatus());
    }
}
