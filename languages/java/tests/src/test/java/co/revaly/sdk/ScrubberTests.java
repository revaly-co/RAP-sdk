package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import co.revaly.sdk.logging.RapScrubber;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/** The single central allowlist scrubber (ADR-SDK-020): emit-known-safe, mask the rest. */
class ScrubberTests {

    @Test
    void allowlistedIdentifiersPassThroughVerbatim() {
        String scrubbed =
                RapScrubber.scrubJson(
                        "{\"merchantTransactionId\":\"mtx-1\",\"transactionStatus\":1,\"code\":\"not_processed\"}");

        assertTrue(scrubbed.contains("\"merchantTransactionId\":\"mtx-1\""));
        assertTrue(scrubbed.contains("\"transactionStatus\":1"));
        assertTrue(scrubbed.contains("\"code\":\"not_processed\""));
    }

    @Test
    void everythingElseIsScrubbedIncludingUnknownFutureFields() {
        String scrubbed =
                RapScrubber.scrubJson(
                        "{\"cardNumber\":\"4111111111111111\",\"cvv\":\"123\",\"someNewField\":\"value\"}");

        assertFalse(scrubbed.contains("4111111111111111"));
        assertFalse(scrubbed.contains("123"));
        assertFalse(scrubbed.contains("value"));
        assertTrue(scrubbed.contains(RapScrubber.SCRUBBED));
    }

    @Test
    void nestedStructureIsPreservedAndScrubbedRecursively() {
        String scrubbed =
                RapScrubber.scrubJson(
                        "{\"paymentMethod\":{\"creditCard\":{\"cardNumber\":\"4111111111111111\"},"
                                + "\"transactionId\":\"txn-1\"}}");

        assertFalse(scrubbed.contains("4111111111111111"));
        assertTrue(scrubbed.contains("\"transactionId\":\"txn-1\""));
        assertTrue(scrubbed.contains("\"paymentMethod\""));
        assertTrue(scrubbed.contains("\"creditCard\""));
    }

    @Test
    void arrayScalarsFollowTheParentKeysStatus() {
        String scrubbed =
                RapScrubber.scrubJson("{\"attempts\":[1,2],\"phoneNumbers\":[\"555-0100\"]}");

        assertTrue(scrubbed.contains("\"attempts\":[1,2]"));
        assertFalse(scrubbed.contains("555-0100"));
    }

    @Test
    void unparseableInputNeverEchoesTheRawText() {
        assertEquals("[unparseable:scrubbed]", RapScrubber.scrubJson("PAN=4111111111111111"));
        assertEquals("", RapScrubber.scrubJson(null));
        assertEquals("", RapScrubber.scrubJson("  "));
    }

    @Test
    void authorizationHeaderIsAlwaysRedacted() {
        Map<String, List<String>> headers = new HashMap<>();
        headers.put("Authorization", Collections.singletonList("ApiKey secret-key"));
        headers.put("Content-Type", Collections.singletonList("application/json"));
        headers.put("X-Correlation-ID", Collections.singletonList("corr-1"));
        headers.put("X-Custom-Internal", Collections.singletonList("internal-value"));

        Map<String, String> scrubbed = RapScrubber.scrubHeaders(headers);

        assertEquals(RapScrubber.REDACTED, scrubbed.get("Authorization"));
        assertEquals("application/json", scrubbed.get("Content-Type"));
        assertEquals("corr-1", scrubbed.get("X-Correlation-ID"));
        assertEquals(RapScrubber.REDACTED, scrubbed.get("X-Custom-Internal"));
        assertFalse(scrubbed.toString().contains("secret-key"));
    }

    @Test
    void headerLookupIsCaseInsensitive() {
        Map<String, List<String>> headers = new HashMap<>();
        headers.put("authorization", Collections.singletonList("ApiKey secret-key"));

        Map<String, String> scrubbed = RapScrubber.scrubHeaders(headers);

        assertEquals(RapScrubber.REDACTED, scrubbed.get("Authorization"));
    }
}
