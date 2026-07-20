package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.Duration;
import org.junit.jupiter.api.Test;

/**
 * ADR-SDK-027 deadline-default semantics: unset resolves to the 30-second ratified default,
 * noOverallDeadline() opts out entirely, explicit values pass through, and zero/negative values are
 * rejected at build.
 */
class DeadlineDefaultTests {

    @Test
    void unsetResolvesToTheRatified30sDefault() {
        assertEquals(Duration.ofSeconds(30), RapClient.DEFAULT_OVERALL_DEADLINE);
        assertEquals(
                RapClient.DEFAULT_OVERALL_DEADLINE, RapClient.builder().effectiveOverallDeadline());
    }

    @Test
    void noOverallDeadlineOptsOutOfAnySdkDeadline() {
        assertNull(RapClient.builder().noOverallDeadline().effectiveOverallDeadline());
        assertNull(RapClient.builder().overallDeadline(null).effectiveOverallDeadline());
    }

    @Test
    void explicitValuesPassThroughUnchanged() {
        RapClient.Builder builder = RapClient.builder().overallDeadline(Duration.ofSeconds(5));
        assertEquals(Duration.ofSeconds(5), builder.effectiveOverallDeadline());
    }

    @Test
    void zeroAndNegativeDeadlinesAreRejectedAtBuild() {
        RapClient.Builder zero = RapClient.builder().apiKey("sk-synthetic-test");
        zero.overallDeadline(Duration.ZERO);
        assertThrows(IllegalArgumentException.class, zero::build);

        RapClient.Builder negative = RapClient.builder().apiKey("sk-synthetic-test");
        negative.overallDeadline(Duration.ofSeconds(-5));
        assertThrows(IllegalArgumentException.class, negative::build);
    }
}
