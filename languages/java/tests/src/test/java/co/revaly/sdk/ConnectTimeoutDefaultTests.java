package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.Duration;
import org.junit.jupiter.api.Test;

/**
 * ADR-SDK-029 connect-timeout-default semantics: unset resolves to the 10-second edge-ratified
 * default, noConnectTimeout() opts out entirely, explicit values pass through, and zero/negative
 * values are rejected at build.
 */
class ConnectTimeoutDefaultTests {

    @Test
    void unsetResolvesToTheRatifiedDefault() {
        assertEquals(Duration.ofSeconds(10), RapClient.DEFAULT_CONNECT_TIMEOUT);
        assertEquals(
                RapClient.DEFAULT_CONNECT_TIMEOUT, RapClient.builder().effectiveConnectTimeout());
    }

    @Test
    void noConnectTimeoutOptsOutOfAnySdkConnectBound() {
        assertNull(RapClient.builder().noConnectTimeout().effectiveConnectTimeout());
        assertNull(RapClient.builder().connectTimeout(null).effectiveConnectTimeout());
    }

    @Test
    void explicitValuesPassThroughUnchanged() {
        RapClient.Builder builder = RapClient.builder().connectTimeout(Duration.ofSeconds(3));
        assertEquals(Duration.ofSeconds(3), builder.effectiveConnectTimeout());
    }

    @Test
    void zeroAndNegativeConnectTimeoutsAreRejectedAtBuild() {
        RapClient.Builder zero = RapClient.builder().apiKey("sk-synthetic-test");
        zero.connectTimeout(Duration.ZERO);
        assertThrows(IllegalArgumentException.class, zero::build);

        RapClient.Builder negative = RapClient.builder().apiKey("sk-synthetic-test");
        negative.connectTimeout(Duration.ofSeconds(-5));
        assertThrows(IllegalArgumentException.class, negative::build);
    }
}
